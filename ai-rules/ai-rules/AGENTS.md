# AI Assistants — Global Rules

## About this file
- Single source of global rules, loaded by Claude Code (import in `~/.claude/CLAUDE.md`)
  and Codex (symlink `~/.codex/AGENTS.md`).
- Versioned in a **public gist**: no secrets, personal data, machine paths or project
  names. Project-specific rules live in that project's `README` / `AGENTS.md`.
- **Local values** (paths, folders, names) live in the `.env` next to this file,
  which is **not versioned**. Here they appear as `$NAME` (e.g. `$METRICS_DIR`).
  - Claude Code: `.env` is already imported by `~/.claude/CLAUDE.md`.
  - Other agents: read `$(dirname "$(readlink -f ~/.codex/AGENTS.md)")/.env`
    before starting.
  - Missing variable or absent `.env`: **ask** instead of guessing the path.
  - The versioned `.env.example` lists variables with placeholders. When adding a
    new variable, update both files.
- Domain-specific rules are split into **subagents** under `subagents/`.
  Load only the ones relevant to the current task to keep context small.

## Core principles (always on)
- Respond in Brazilian Portuguese.
- Be direct; short answers by default, go deeper only when asked.
- Ambiguous and expensive to get wrong → ask first. Cheap to redo → assume the
  most reasonable reading and state it.
- Never invent facts, APIs, versions or functions. Don't know? Say so.
- Don't expand scope: if something extra is worth doing, suggest it instead of doing it.
- Report what was **actually** verified (tests run, commands executed) and what was not.
- **Verifiable honesty**: every claim of "tested", "passed" or "works" must include
  the command and relevant output. No output → don't claim verification.
- Cite sources when information comes from web research.

## Subagents
Specialized rule sets. Load only what the task needs:

| Subagent              | When to load                                      |
|-----------------------|---------------------------------------------------|
| `communication`       | Always (core interaction rules)                   |
| `workflow`            | Any non-trivial task                              |
| `metrics`             | Token tracking / long sessions                    |
| `auto-mode`           | Permission mode detection                         |
| `file-ops`            | Rename, move, delete, overwrite                   |
| `git`                 | Any git or deploy action                          |
| `database`            | Schema, migrations, queries                       |
| `dependencies`        | Install / update packages                         |
| `testing`             | Writing or running tests, QA pipeline             |
| `code-review`         | Reviewing diffs                                   |
| `security`            | Input handling, auth, OWASP checklist             |
| `operations`          | Logs, health checks, performance budgets          |
| `destructive-ops`     | Anything irreversible or external                 |
| `secrets`             | Commits, logs, `.env` handling                    |
| `code-style`          | Language-specific conventions                     |
| `frontend`            | HTML / CSS / JS UI work                           |
| `new-projects`        | Scaffolding a new repository                      |
| `production`          | Server / deploy practices                         |
| `content`             | Articles, lessons, documentation                  |

See `subagents/<name>.md` for the full rules of each.
