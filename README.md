# Regras e subagentes para assistentes de IA

Regras globais para Claude Code, Codex e outros agentes, divididas em três camadas
para gastar menos contexto e rodar trabalho pesado (QA, revisão) em paralelo.

| Camada | Onde | Quando carrega |
|---|---|---|
| **Núcleo** | `AGENTS.md` | Sempre, em toda sessão (~150 linhas) |
| **Regras por linguagem** | `rules/*.md` | Só quando a tarefa lê/edita arquivos daquele tipo |
| **Subagentes** | `agents/*.md` (Claude) e `codex/agents/*.toml` (Codex) | Quando o agente principal delega; rodam em contexto próprio |

A decisão e as alternativas estão em [docs/adr/0001-nucleo-regras-e-subagentes.md](docs/adr/0001-nucleo-regras-e-subagentes.md).

## Subagentes

| Nome | Faz | Edita? | Modelo (Claude) |
|---|---|---|---|
| `qa-runner` | Procedimento de QA em 9 etapas, com tabela de evidências | Não | sonnet, em segundo plano |
| `code-reviewer` | Revisão independente do diff contra os requisitos | Não | o da sessão |
| `security-reviewer` | OWASP, segredos, autorização, uploads | Não | o da sessão |
| `db-reviewer` | Schema, migrations, FKs, SQL; nunca executa | Não | o da sessão |
| `docs-writer` | README, ADR, `.env.example`, `.docs/plan.md` e `tasks.md` | Só docs | sonnet |
| `ci-builder` | GitHub Actions com QA antes do deploy | Só CI | sonnet |

Fluxo típico de uma entrega:

```text
agente principal implementa (TDD, ciclo rápido de testes)
        │
        ├──► qa-runner          ┐
        ├──► code-reviewer      ├─ em paralelo, cada um no seu contexto
        ├──► security-reviewer  ┘  (db-reviewer se mexeu em banco)
        │
        ├──► docs-writer (README/.docs/ADR)
        ▼
relatório final ──► PR ──► CI roda o mesmo QA e bloqueia o merge
```

Revisão cruzada com outro fornecedor (Codex revisando o que o Claude fez, ou o
contrário):

```bash
codex exec review --base main "Requisitos: <cole aqui>"
```

## Instalação

Esta pasta é a fonte única; as ferramentas apontam para ela por symlink.

```bash
DIR=/caminho/para/esta/pasta

# Claude Code: núcleo (já feito se o ~/.claude/CLAUDE.md importa o AGENTS.md)
mkdir -p ~/.claude/agents ~/.claude/rules
ln -s "$DIR"/agents/*.md ~/.claude/agents/
ln -s "$DIR"/rules/*.md  ~/.claude/rules/

# Codex: núcleo + subagentes
ln -sf "$DIR/AGENTS.md" ~/.codex/AGENTS.md
mkdir -p ~/.codex/agents
ln -s "$DIR"/codex/agents/*.toml ~/.codex/agents/
```

Os wrappers do Codex não copiam as instruções: mandam ler `agents/<nome>.md` na pasta
do `AGENTS.md`, então editar o `.md` vale para as duas ferramentas.

Para conferir no Claude Code: `/agents` lista os subagentes; `/memory` mostra as
regras carregadas.

## Variáveis locais

Ficam no `.env` desta pasta (não versionado). O `.env.example` lista as variáveis com
placeholders. Ao criar variável nova, atualize os dois.

## Como mudar uma regra

- Vale para toda tarefa? `AGENTS.md`, e mantenha-o abaixo de ~150 linhas.
- Vale só para uma linguagem/tipo de arquivo? `rules/<linguagem>.md`, com `paths`.
- É um trabalho que roda isolado e devolve um resumo? `agents/<nome>.md` + wrapper em
  `codex/agents/<nome>.toml`, e uma linha na tabela do `AGENTS.md`.
