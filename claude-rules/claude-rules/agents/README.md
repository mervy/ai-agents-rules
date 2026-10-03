# Sub-Agents

Este diretório contém agentes especializados. O `CLAUDE.md` raiz delega para eles.

## Quando usar cada um

| Agente | Quando chamar |
|---|---|
| `code-reviewer` | Revisar código, checar SOLID, KISS, nomenclatura, imports |
| `test-runner` | Escrever/rodar testes, TDD, cobertura, mutação |
| `security-auditor` | Mudança com entrada externa, auth, upload, segredos, OWASP |
| `git-manager` | Commit, branch, PR, tag, push, rebase, histórico |
| `database-manager` | Schema, migration, FK, CASCADE, SQL |
| `qa-runner` | Rodar pipeline completo de QA (9 etapas) |
| `doc-writer` | README, ADR, docs, artigos, .env.example |
| `metrics-collector` | Tokens por sessão, $METRICS_DIR, -continue.md |

## Protocolo

1. Orquestrador define escopo fechado (arquivos tocáveis)
2. Delega tarefa com: objetivo, arquivos, requisitos, critérios de pronto
3. Sub-agente executa e retorna: o que fez, comandos com saída, o que não verificou
4. Orquestrador valida DoD

Nenhum sub-agente faz push, migration ou rm sem confirmação do orquestrador.
