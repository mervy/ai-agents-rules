# 0002 — Hooks para confirmações, subagentes sem modelo fixo e Copilot

Data: 2026-10-03

## Contexto
As confirmações do `AGENTS.md` (push, `reset --hard`, `.env`...) são texto: o modelo
segue na maioria das vezes, não sempre. No Claude Code, a decisão `ask` de um hook só
vira pergunta no modo padrão; nos modos auto/acceptEdits o fluxo do modo decide.

O DeepSeek V4 Pro é usado pelo Copilot no VS Code, que lê `~/.claude/agents` no formato
do Claude Code e, sem `model`, usa o modelo do seletor.

## Decisão
- `hooks/guard.py` (PreToolUse, Python sem dependências): `ask` no modo padrão; `deny`
  nos outros, orientando o usuário a rodar o comando com `!`; `.env` no git negado
  sempre.
- Subagentes sem `model`: usam o modelo da sessão em cada ferramenta.
- Copilot usa os mesmos `agents/*.md`; o núcleo entra por
  `~/.copilot/copilot-instructions.md`.

## Alternativas descartadas
- `deny` sempre: impediria até o push autorizado no modo padrão.
- Arquivos `.agent.md` separados para o Copilot: duplicariam os agentes que ele já lê
  em `~/.claude/agents`.
- Manter `model: sonnet`: no Copilot podia trocar o DeepSeek por um modelo pago da
  assinatura.

## Consequências
- No modo auto, push e afins precisam ser rodados pelo usuário (`! git push`).
- Subagentes no Claude Code gastam o modelo da sessão (sem economia do sonnet).
- Hooks valem só no Claude Code; Codex e Copilot dependem das regras escritas.
