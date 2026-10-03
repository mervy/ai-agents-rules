# Regras para Assistentes de IA

## Sobre este arquivo
- Núcleo das regras globais: só o que vale para **toda** tarefa. Lido pelo Claude Code
  (import em `~/.claude/CLAUDE.md`) e pelo Codex (symlink `~/.codex/AGENTS.md`).
- O resto fica ao lado, na mesma pasta (veja o `README.md`):
  - `rules/<linguagem>.md`: convenções por linguagem, lidas só quando a tarefa toca
    aqueles arquivos;
  - `agents/<nome>.md`: subagentes com contexto próprio, para QA, revisão e documentação.
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

## Processo de trabalho
- **Escopo fechado**: no início, defina (ou peça) a lista de arquivos e pastas que podem
  ser alterados. Precisa sair dela? Pergunte.
- **Conflito de regras**: se um requisito conflita com uma regra, pare e pergunte.
- **TDD** em código com lógica: teste que falha → confirme a falha → implemente → refatore
  com a suite verde. Bug começa por um teste que o reproduz.
- **Mudanças pequenas**: um PR = uma responsabilidade, idealmente até ~400 linhas
  alteradas (sem lockfiles e gerados).
- **ADR**: decisão técnica relevante vira `docs/adr/NNNN-titulo.md` (contexto, decisão,
  alternativas descartadas, consequências).

### QA proporcional à tarefa
- **Sem código alterado** (versionar, mover pasta, só docs): nada de suite de QA.
  Confira só o que a tarefa pede (ex.: `.env` fora do commit, segredos no diff).
- **Durante a implementação**: ciclo rápido, só formatação, lint e os testes da parte
  alterada.
- **Antes de entregar**: o procedimento completo vai para o subagente `qa-runner`, em
  segundo plano, enquanto você segue com docs e relatório.
- **O portão de verdade é o CI**: ele roda o procedimento completo e bloqueia o merge.

### Subagentes
Subagente trabalha em contexto separado e devolve só o resumo. Use-o para trabalho
verboso ou independente; não use para ajustes rápidos que precisam da conversa.

| Subagente | Quando chamar | Pode editar? |
|---|---|---|
| `qa-runner` | Antes de entregar código: procedimento completo de QA | Não |
| `code-reviewer` | Mudança não trivial: revisão independente (diff + requisitos) | Não |
| `security-reviewer` | Mudança que toca entrada externa, auth, upload, segredos | Não |
| `db-reviewer` | Schema, migration, FK ou SQL novo | Não |
| `docs-writer` | README, ADR, `.env.example`, `.docs/plan.md` e `tasks.md` | Só docs |
| `ci-builder` | Criar ou ajustar pipeline de CI/deploy | Só CI |

- Passe sempre: objetivo, requisitos, escopo (arquivos) e a branch/diff de base. O
  subagente **não vê a conversa**.
- Revisões e QA são independentes: rode em **paralelo**.
- Revisão cruzada (outro fornecedor de IA) em mudança grande: `codex exec review --base <branch>`.
- Subagente **nunca** autoriza operação destrutiva, push, deploy ou migration: ele
  aponta, o agente principal pergunta ao usuário.
- Revisão pedida pelo usuário segue o formato do `code-reviewer`: problemas reais
  primeiro (não compila, bug, segurança, perda de dados), depois melhorias opcionais,
  cada um com o motivo em uma linha.

### Definição de pronto
- [ ] Requisito atendido, dentro do escopo combinado
- [ ] Testes novos cobrindo a mudança (erro e borda incluídos)
- [ ] Relatório do `qa-runner` sem falhas (ou etapa marcada "não se aplica" com motivo)
- [ ] Imports, dependências, nomes de pacotes e versões conferidos
- [ ] Sem segredos no diff
- [ ] README / ADR / `.env.example` atualizados quando a mudança pede
- [ ] Relatório final: o que mudou, como testar, o que foi e o que **não** foi verificado

## Regras por linguagem
Ao ler ou editar arquivos de uma linguagem, siga `rules/<arquivo>` (no Claude Code
carregam sozinhas pelo `paths`; nos outros agentes, leia o arquivo antes de editar):
`php.md`, `javascript.md`, `frontend.md`, `python.md`, `go.md`, `rust.md`, `c.md`,
`cpp.md`, `csharp.md`, `java.md`, `database.md` (SQL e migrations), `testing.md`
(ao escrever testes).

## Métricas de tokens por sessão
- **Antes de começar**, crie em `$METRICS_DIR` o arquivo `AAAAMMDD-HHMM-<pasta>.md`
  (`<pasta>` = nome literal da pasta do projeto, com `_` inicial se houver; agente que
  não é o Claude Code acrescenta `-<agente>`). Linha 1: `AAAA-MM-DD HH:MM`. Linha 2:
  agente + modelo.
- Anote os tokens por etapa numa tabela; no fim, mostre e grave o total.
- Números só do registro real da ferramenta, **nunca estimados**. Claude Code:
  `$METRICS_SCRIPT [transcript]` (deduplica por `message.id`). Outro agente: use ou crie
  `$METRICS_DIR/ai-metrics-<agente>.sh`, conferindo o formato num log real. Sem dado:
  escreva "sem dado de uso" e avise.
- **Sessão cara**: contexto da última resposta > 150 mil ou total > 5 milhões → pare num
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
- Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`),
  descrição em português. **Sem** `Co-Authored-By`, "Generated with" ou assinatura.
- Branch curta por tarefa (`feature/...`, `fix/...`, `chore/...`); entra por PR com o que
  mudou, por quê e como testar. Tags sempre anotadas (`git tag -a`).
- Produção: branch → PR → merge → deploy automático pelo CI. Nunca editar no servidor.

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
- KISS, YAGNI, SOLID com bom senso: interface só com mais de uma implementação real ou
  necessidade concreta de teste.
- Nomes claros, funções curtas, sem código morto; código completo, sem `...` ou
  "implemente aqui".
- Identificadores em inglês; comentários em português, só para o **porquê**.
- Erros tratados em todos os caminhos (nunca `catch` vazio); timeout em toda chamada de
  rede; UTF-8 e acentos do português (slug, ordenação, busca).
- Configuração por variáveis de ambiente; validar as obrigatórias ao subir e falhar cedo.
- Logs num formato único, sem dados sensíveis; erro ao usuário é genérico.
- Serviço web: rota `/health` e orçamento de desempenho definido no README.
- Entrada externa: checklist OWASP (validação, injeção, XSS, upload, auth, CSRF, rate
  limit); o detalhe está no `security-reviewer`. Nunca usar credenciais de produção.

## Projetos novos
- Estrutura de pastas, README, arquivo de dependências, `.env.example`, instruções de
  instalar/rodar/testar, testes, lint e CI (com QA antes do deploy) desde o primeiro
  commit. Seguir a convenção da linguagem para lockfiles.

## Conteúdo e documentação
- Artigos e aulas: tom didático, tamanho médio, código com destaque de sintaxe.
- HTML quando for para publicação; Markdown quando for para repositório.
