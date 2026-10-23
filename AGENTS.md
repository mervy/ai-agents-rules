# Regras para Assistentes de IA

## Sobre este arquivo
- Núcleo das regras globais: só o que vale para **toda** tarefa. Lido pelo Claude Code,
  Codex e Copilot (import em `~/.claude/CLAUDE.md`, symlinks `~/.codex/AGENTS.md` e
  `~/.copilot/copilot-instructions.md`). Hooks em `hooks/` garantem as confirmações.
- O resto fica ao lado, na mesma pasta (veja o `README.md`):
  - `rules/<linguagem>.md`: convenções por linguagem, lidas só quando a tarefa toca
    aqueles arquivos;
  - `agents/<nome>.md`: subagentes com contexto próprio, para revisão e documentação.
- Versionado em repositório público: nada de segredos, dados pessoais, caminhos da
  máquina ou nomes de projetos. Regra de um projeto só vai no README/AGENTS.md dele.
- **Valores locais** ficam no `.env` desta pasta (não versionado) e aparecem aqui como
  `$NOME`. Claude Code: já importado pelo `~/.claude/CLAUDE.md`. Outros agentes: leia
  `$(dirname "$(readlink -f ~/.codex/AGENTS.md)")/.env` antes de começar. Variável
  faltando: **pergunte**. Variável nova: atualize `.env` e `.env.example`.

## Comunicação
- Responder em português do Brasil; direto, curto por padrão, aprofundar quando pedido.
- Ambíguo e caro de errar: perguntar antes. Barato de refazer: assumir a leitura mais
  razoável e dizer qual foi.
- Nunca inventar fatos, APIs, versões ou funções. Não sabe? Diga que não sabe.
- Não mudar o escopo: se algo extra vale a pena, sugerir em vez de fazer.
- **Honestidade verificável**: todo "testado", "passou" ou "funciona" vem com o comando
  executado e a saída relevante. Diga também o que **não** foi verificado.
- Citar as fontes quando a informação vier de pesquisa na web.

## Rígido x opcional
- **Sempre, em todo projeto**: confirmações de operações destrutivas, segredos fora do
  repositório, versionamento (`main`/`dev`, branches curtas, merge `--no-ff`), tags,
  sugestão de release e `.docs/plan.md` + `.docs/tasks.md`.
- **Opcional (oferecer no final)**: ADR, CI, métricas de tokens, subagentes revisores
  (`code-reviewer`, `security-reviewer`, `db-reviewer`, revisão cruzada), lint, rota
  `/health`, orçamento de desempenho e o restante da estrutura de projeto novo. Não faça
  durante o trabalho; na entrega, liste o que ficou de fora e pergunte se quer agora.
- **Testes bem básicos**: só o essencial da parte alterada (o caminho principal
  funciona), rodando localmente. Sem TDD, cobertura, mutação, suite de QA nem testes no
  CI/deploy. Se um projeto precisar de mais, a regra fica no README/AGENTS.md dele.

## Processo de trabalho
- **Escopo fechado**: no início, defina (ou peça) a lista de arquivos e pastas que podem
  ser alterados. Precisa sair dela? Pergunte.
- **Conflito de regras**: se um requisito conflita com uma regra, pare e pergunte.
- **Mudanças pequenas**: um PR = uma responsabilidade, idealmente até ~400 linhas
  alteradas (sem lockfiles e gerados).
- **ADR** (opcional, oferecer no final): decisão técnica relevante vira `.docs/adr/NNNN-titulo.md` (contexto, decisão,
  alternativas descartadas, consequências).

### Subagentes
Opcionais (oferecer no final), exceto o `docs-writer` para manter `.docs`. Subagente trabalha em contexto separado e devolve só o resumo. Use-o para trabalho
verboso ou independente; não use para ajustes rápidos que precisam da conversa.

| Subagente | Quando chamar | Pode editar? |
|---|---|---|
| `code-reviewer` | Mudança não trivial: revisão independente (diff + requisitos) | Não |
| `security-reviewer` | Mudança que toca entrada externa, auth, upload, segredos | Não |
| `db-reviewer` | Schema, migration, FK ou SQL novo | Não |
| `docs-writer` | README, ADR, `.env.example`, `.docs/plan.md` e `tasks.md` | Só docs |
| `ci-builder` | Criar ou ajustar pipeline de CI/deploy | Só CI |

- Passe sempre: objetivo, requisitos, escopo (arquivos) e a branch/diff de base. O
  subagente **não vê a conversa**.
- Revisões são independentes: rode em **paralelo**.
- Revisão cruzada (outro fornecedor de IA) em mudança grande: `codex exec review --base <branch>`.
- Subagente **nunca** autoriza operação destrutiva, push, deploy ou migration: ele
  aponta, o agente principal pergunta ao usuário.
- Revisão pedida pelo usuário segue o formato do `code-reviewer`: problemas reais
  primeiro (não compila, bug, segurança, perda de dados), depois melhorias opcionais,
  cada um com o motivo em uma linha.

### Definição de pronto
- [ ] Requisito atendido, dentro do escopo combinado
- [ ] Imports, dependências, nomes de pacotes e versões conferidos
- [ ] Sem segredos no diff
- [ ] README e `.docs` atualizados (`.env.example` quando a mudança pede)
- [ ] Opcionais que ficaram de fora listados, com a oferta de fazer agora
- [ ] Relatório final: o que mudou, como testar, o que foi e o que **não** foi verificado

## Regras por linguagem
Ao ler ou editar arquivos de uma linguagem, siga `rules/<arquivo>` (no Claude Code
carregam sozinhas pelo `paths`; nos outros agentes, leia o arquivo antes de editar):
`php.md`, `javascript.md`, `frontend.md`, `python.md`, `go.md`, `rust.md`, `c.md`,
`cpp.md`, `csharp.md`, `java.md`, `database.md` (SQL e migrations).

## Métricas de tokens por sessão (opcional)
Só se o usuário pedir ou aceitar na oferta do final.
- Crie em `$METRICS_DIR` o arquivo `AAAAMMDD-HHMM-<pasta>.md`
  (`<pasta>` = nome literal da pasta do projeto, com `_` inicial se houver; agente que
  não é o Claude Code acrescenta `-<agente>`). Linha 1: `AAAA-MM-DD HH:MM`. Linha 2:
  agente + modelo.
- Anote os tokens por etapa numa tabela; no fim, mostre e grave o total.
- Números só do registro real da ferramenta, **nunca estimados**. Claude Code:
  `$METRICS_SCRIPT [transcript]` (deduplica por `message.id`). Outro agente: use ou crie
  `$METRICS_DIR/ai-metrics-<agente>.sh`, conferindo o formato num log real. Sem dado:
  escreva "sem dado de uso" e avise.
- **Sessão cara**: contexto da última resposta > 150 mil ou total > 10 milhões → pare num
  ponto estável, grave `...-continue.md` (objetivo, feito, falta em ordem, decisões,
  arquivos, comandos, próximo passo) e sugira nova sessão.

## Modo auto (permission mode)
- **Nunca comece a trabalhar em modo auto.** Se a sessão iniciar nele, avise na primeira
  resposta e pergunte se o usuário quer permanecer. Sem resposta = não.
- Troca para auto no meio da sessão: avise na hora. (O modo é do harness; a obrigação
  é detectar, avisar e perguntar.)

## Operações que sempre pedem confirmação
- Apagar arquivos, sobrescrever de forma irreversível, encerrar processos, `chmod 777`,
  `chown -R`, publicar para fora (deploy, gist, post, serviço externo).
- Git: push, force-push, `reset --hard`, amend de commit publicado, apagar branch.
- Banco: migrations, alterar `schema.sql`, `DROP`, `TRUNCATE`, `DELETE` sem `WHERE`.
- Dependências: `composer update`, `npm update`, `cargo update` e afins
  (`composer install`, `composer dump-autoload` e `npm ci` são livres).
- Arquivos críticos: `.env`, lockfiles, `schema.sql`, `public/.htaccess`, migrations já
  aplicadas em produção.
- Renomear = `mv` real, nunca recriar; confira tamanho/hash antes e depois.

## Git e deploy
- **Todo projeto é versionado**, com duas branches fixas: `main` (estável/produção) e
  `dev` (trabalho do dia a dia; nunca `develop`). Projeto novo: `git init -b main`,
  commit inicial, `dev` a partir dela. Já tem git? Preserve o histórico.
- **Toda mudança**, mesmo pequena (fix, docs, ajuste de config), vai numa branch curta
  saindo de `dev` (`feature/...`, `fix/...`, `chore/...`, `docs/...`) e volta para
  `dev`; nada de commit direto em `dev` ou `main` (exceção: o commit inicial do
  projeto). `dev` → `main` por PR com o que mudou, por quê e como testar.
- **Preservar ramificações no histórico**: toda integração entre branches
  (`feature/*`, `fix/*`, `chore/*` → `dev` e `dev` → `main`) deve criar um commit
  de merge quando houver commits novos a integrar. Em merges locais, usar
  `git merge --no-ff <branch>`; não usar fast-forward, squash ou rebase para integrar.
  No GitHub, usar **Create a merge commit**; configurar o repositório para permitir
  merge commits e desabilitar squash/rebase merging, sem exigir histórico linear.
  Alterar configurações remotas continua sujeito à confirmação do usuário.
  Conferir com `git log --graph --oneline --decorate --all` e
  `git log --merges --oneline`. Não reescrever histórico antigo para mudar o desenho.
- Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`),
  descrição em português. **Sem** `Co-Authored-By`, "Generated with" ou assinatura.
- **Tag anotada** (`git tag -a vX.Y.Z -m "..."`, SemVer) a cada entrega que chega à
  `main`. Marco relevante (primeira versão funcional, feature grande): **sugira** uma
  release no GitHub/Codeberg com notas; publicar pede confirmação.
- Produção: `dev` → PR → `main` → deploy (automático pelo CI, quando houver). Nunca editar no servidor.

## Dependências e segredos
- Dependência nova só se necessária, justificada em uma linha. Lockfile versionado em
  aplicação; nada de `*` ou `latest`.
- Antes de todo commit, procure no diff senhas, chaves, tokens, connection strings e
  dados pessoais (`gitleaks` quando houver).
- Segredo já versionado: avise na hora; precisa **rotacionar** (e limpar o histórico,
  com autorização). Segredo em log/saída da sessão: aponte e recomende rotação.
- Nunca copie valores do `.env`; use placeholders (`DB_PASS=troque-aqui`). Todo projeto
  tem `.env.example`.

## Código — regras gerais
- KISS, YAGNI, SOLID com bom senso: interface só com mais de uma implementação real.
- Nomes claros, funções curtas, sem código morto; código completo, sem `...` ou
  "implemente aqui".
- Identificadores em inglês; comentários em português, só para o **porquê**.
- Erros tratados em todos os caminhos (nunca `catch` vazio); timeout em toda chamada de
  rede; UTF-8 e acentos do português (slug, ordenação, busca).
- Configuração por variáveis de ambiente; validar as obrigatórias ao subir e falhar cedo.
- Logs num formato único, sem dados sensíveis; erro ao usuário é genérico.
- Serviço web (opcional, oferecer no final): rota `/health` e orçamento de desempenho
  definido no README.
- Entrada externa: checklist OWASP (validação, injeção, XSS, upload, auth, CSRF, rate
  limit); o detalhe está no `security-reviewer`. Nunca usar credenciais de produção.

## Projetos
- **Nome** da pasta e do repositório: `<linguagem>-<nome>`, minúsculas e hífens
  (`cpp-jogo-da-cobrinha`, `php-full-ecommerce`). Prefixos: `php`, `node`, `react`,
  `reactnative`, `go`, `rust`, `python`, `csharp`, `java`, `c`, `cpp`, `html`
  (estático); várias stacks: `multi`.
- **Versão nova da linguagem**: use a versão estável mais recente instalada e os
  recursos modernos dela (lista em `rules/<linguagem>.md`). Confira a versão antes
  (`php -v`, `node -v`...) e declare a mínima no projeto (`composer.json`, `engines`,
  `go.mod`...). Recurso que você não sabe se existe na versão: verifique, não chute.
- **Documentação viva** em todo projeto, criada no início e mantida a cada entrega
  (detalhes no `docs-writer`):
  - `.docs/plan.md`: o que é, como funciona, para que serve, features e stack, e a
    **data de início** (criação do arquivo ou pasta mais antiga; cite a fonte);
  - `.docs/tasks.md`: tudo que está sendo feito, **em ordem**; mudou o plano,
    reordene; terminou, marque `[x]`. Nunca marque o que não foi feito.
- Projeto novo nasce com estrutura de pastas, README, arquivo de dependências,
  `.env.example` e instruções de instalar/rodar. Lint e CI são opcionais, oferecidos
  no final. Seguir a convenção da linguagem para lockfiles.

## Conteúdo e documentação
- Artigos e aulas: tom didático, tamanho médio, código com destaque de sintaxe.
- HTML quando for para publicação; Markdown quando for para repositório.
