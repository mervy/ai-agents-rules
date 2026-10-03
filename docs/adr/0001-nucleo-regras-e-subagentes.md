# 0001 — Núcleo enxuto, regras por linguagem e subagentes por responsabilidade

Data: 2026-10-03

## Contexto
O `AGENTS.md` global chegou a ~380 linhas. Tudo carregava em toda sessão: regras de
C++ numa tarefa de CSS, o procedimento de QA inteiro numa tarefa de `git init`. Na
prática o agente rodava QA completo em tarefas que não pediam, enchendo o contexto
com saída de testes e travando a conversa.

A documentação do Claude Code recomenda menos de 200 linhas por arquivo de memória
(arquivos longos reduzem a aderência) e regras com `paths` para o que vale só para
parte do código. Guias de AGENTS.md de 2026 falam em menos de 150 linhas. Claude
Code, Codex (desde mar/2026) e opencode suportam subagentes com contexto próprio,
execução em paralelo e restrição de ferramentas.

Foram avaliadas cinco propostas anteriores (DeepSeek, `ai-rules`, `ai_agents_rules`,
`claude-rules`, `ai-rules-improved`).

## Decisão
Três camadas:
1. **`AGENTS.md`**: só invariantes (comunicação, processo, confirmações, git,
   segredos, métricas, código geral), com uma regra nova de **QA proporcional**:
   sem código, sem QA; durante a implementação, ciclo rápido; QA completo delegado ao
   `qa-runner` em segundo plano; o CI é o portão.
2. **`rules/*.md`**: convenções por linguagem e por tema (banco, testes), com
   `paths` para o Claude Code carregar sob demanda; os outros agentes leem pelo índice
   do núcleo.
3. **`agents/*.md`**: seis subagentes **por responsabilidade** (`qa-runner`,
   `code-reviewer`, `security-reviewer`, `db-reviewer`, `docs-writer`, `ci-builder`),
   com ferramentas restritas (revisores não editam) e modelo mais barato onde cabe.
   O Codex usa wrappers TOML que apontam para os mesmos `.md`.

## Alternativas descartadas
- **Subagente por linguagem** (`lang-php` etc., proposta do DeepSeek): convenção de
  linguagem precisa estar no contexto de quem **escreve** o código, não num agente
  separado. Virou regra com `paths`.
- **Subagente para tudo** (`git`, `auto-mode`, `metrics`, `communication`, proposta
  `ai-rules`): são regras do próprio agente principal, de poucas linhas, ou precisam
  da conversa. Um subagente começa sem contexto e não decide nada disso.
- **Núcleo que importa todos os módulos com `@`** (proposta do chat): imports
  carregam tudo na abertura, então o custo de contexto não cai.
- **Copiar as instruções nos TOML do Codex**: duas cópias divergem. O wrapper lê o `.md`.

## Consequências
- O núcleo cai de ~380 para ~150 linhas; as regras de linguagem só entram quando
  usadas.
- QA e revisões rodam em paralelo e fora do contexto principal.
- É preciso instalar por symlink (`~/.claude/agents`, `~/.claude/rules`,
  `~/.codex/agents`); até lá, os agentes leem os arquivos pelo índice do núcleo.
- Um gist não guarda pastas: o versionamento público precisa ir para um repositório.
- Regras em Markdown continuam sendo pedido, não garantia: o que não pode falhar
  (push, `reset --hard`, commitar `.env`) pede hooks determinísticos, ainda não feitos.
