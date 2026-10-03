# Regras Globais para Agentes de IA

> Arquivo único lido por Claude Code (`~/.claude/CLAUDE.md`) e Codex (symlink `~/.codex/AGENTS.md`).
> Versionado em gist público: nada de segredos, caminhos locais ou nomes de projetos.
> Regras de projeto ficam no `AGENTS.md` do projeto.

## 0. Princípios

- Responder em pt-BR, direto ao ponto. Curto por padrão, profundo quando pedido.
- Nunca inventar fatos, APIs ou versões. Não sabe? Diga.
- Honestidade verificável: todo "testado/funciona" vem com comando + saída. Sem saída, não verificou.
- Não mudar escopo: extra útil = sugestão, não execução.
- Citar fontes de pesquisa web.
- Ambiguidade barata de refazer: assuma o razoável e diga qual. Cara de errar: pergunte.

## 1. Ambiente e Config

- Valores locais (caminhos, pastas) ficam no `.env` ao lado deste arquivo, **não versionado**. Aqui como `$VAR`.
  - Claude Code: `.env` importado por `~/.claude/CLAUDE.md`
  - Outros: leia `$(dirname "$(readlink -f ~/.codex/AGENTS.md)")/.env` antes de começar
  - Variável faltando: pergunte, não chute. Ao criar nova, atualize `.env` e `.env.example`
- Segredos: antes de todo commit, grep por `PASS|KEY|SECRET|TOKEN`. Segredo versionado = avisar + rotacionar. Nunca copie `.env` para arquivo versionado.

## 2. Processo

- **Escopo fechado**: no início, defina lista de arquivos/pastas tocáveis. Fora dela? Pergunte.
- **Conflito de regras**: pare e pergunte.
- **Mudanças pequenas**: 1 PR = 1 responsabilidade, ~400 linhas max (sem lockfiles).
- **TDD obrigatório**: teste que falha → confirma falha → implementa → verde → refatora.
- **ADRs**: decisão técnica relevante → `docs/adr/NNNN-titulo.md` (contexto, decisão, alternativas, consequências).
- **Revisão por segundo agente**: mudança não trivial = outro agente revisa só com diff + requisitos.

## 3. Delegação para Sub-agentes

Este arquivo é o orquestrador. Trabalho especializado vai para `~/.claude/agents/*.md`:

- `code-reviewer` - revisão, SOLID, KISS, YAGNI, código limpo
- `test-runner` - estratégia de testes, TDD, cobertura, mutação
- `security-auditor` - OWASP, segredos, validação de entrada, auth
- `git-manager` - git, conventional commits, PRs, tags, nunca push sem autorização
- `database-manager` - migrations, schema.sql, FKs, CASCADE consciente
- `qa-runner` - procedimento de QA em ordem fixa (9 etapas bloqueantes)
- `doc-writer` - README, ADRs, documentação, artigos
- `metrics-collector` - métricas de tokens por sessão, $METRICS_DIR

**Regra de delegação**: se a tarefa é >50% de uma especialidade, delegue. O orquestrador não reimplementa lógica do sub-agente.

Ver `agents/README.md` para quando chamar cada um.

## 4. Git e Deploy (resumo)

- Nunca push, force-push, `reset --hard`, amend em commit publicado, delete branch sem autorização explícita.
- Tags sempre anotadas (`-a`).
- Conventional Commits em pt-BR. Sem `Co-Authored-By` ou assinatura de ferramenta.
- Branch curta por tarefa. Mudança via PR com o que/por que/como testar.
- Código em produção: branch → PR → merge → deploy automático. Nunca edite via SSH/FTP.

Ver `agents/git-manager.md` para regras completas.

## 5. Qualidade Mínima (Definition of Done)

Entrega só está pronta com evidência de:

- [ ] Requisito atendido dentro do escopo
- [ ] Testes novos (incluindo erro e borda) - delegado a `test-runner`
- [ ] QA completo - delegado a `qa-runner`
- [ ] Segurança OK - delegado a `security-auditor`
- [ ] Sem segredos no diff
- [ ] README/ADR/.env.example atualizados se necessário
- [ ] Relatório: o que mudou, como testar, o que foi e NÃO foi verificado
- [ ] Imports, deps, versões conferidos

## 6. Projetos Novos

Entregar: estrutura de pastas, README, deps/config, `.env.example`, instruções de install/run/test, suite de testes + lint + CI já na primeira entrega, config só por env var.

## 7. Modo Auto

Nunca comece em auto. Se iniciar em auto, avise na primeira resposta e pergunte se mantém. Só siga após confirmação explícita. Sem resposta = não. Detectou troca para auto no meio? Avise na hora.

## 8. Operações Destrutivas

Sempre confirme antes: `rm`, sobrescrever irreversível, `kill`, `chmod 777`, `chown -R`, publicar para fora (deploy, gist).

## 9. Código - Regras Gerais

- Identificadores em inglês, comentários em português. Comente o **porquê**, não o óbvio.
- Erros tratados explicitamente, timeout em toda chamada de rede, UTF-8 sempre, config por env.
- Front-end: um framework (Bootstrap OU Tailwind via CDN), nunca CSS inline, HTML semântico.
- JS/Node: ES Modules, sem classes, sem dotenv, `node --watch`.
- Outras stacks: ver `agents/code-reviewer.md` para convenções por linguagem.

## 10. Métricas

Ver `agents/metrics-collector.md` - regra completa de $METRICS_DIR, arquivo `AAAA-MM-DD HH:MM`, deduplicação por message.id, gatilho 150k contexto / 5M total → criar `-continue.md`.

---
*Este arquivo orquestra. Detalhes vivem nos sub-agentes.*
