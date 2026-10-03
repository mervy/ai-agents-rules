# ai-rules-improved

Refatoração do arquivo global de regras em um núcleo pequeno e sub-agentes especializados.

## Estrutura

- `AGENTS.md`: regras globais e invariantes.
- `agents/qa-engineer.md`: validação e QA.
- `agents/security-reviewer.md`: revisão de segurança.
- `agents/code-reviewer.md`: segunda revisão independente.
- `agents/database-reviewer.md`: banco e migrations.
- `agents/docs-writer.md`: documentação.
- `agents/metrics-reporter.md`: métricas e handoff de sessão.
- `original.md`: cópia do arquivo recebido.

## Princípio

Sub-agentes reduzem ruído de contexto e especializam checklists, mas não substituem o agente principal. Autorizações, escopo, segurança destrutiva e decisão final permanecem centralizados em `AGENTS.md`.

Os nomes dos sub-agentes estão em inglês e minúsculas, como solicitado.
