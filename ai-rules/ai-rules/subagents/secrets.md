# Subagent: secrets

- **Before every commit**, check that the diff does not include passwords, API keys,
  tokens, connection strings or personal data (search for `PASS`, `KEY`, `SECRET`,
  `TOKEN`, URLs with embedded credentials).
- If a secret **has already been versioned**, warn immediately: removing it from the
  code is not enough — it remains in git history. The credential must be **rotated**
  and, if the repo is public/shared, history cleaned (with authorization).
- If a secret appears in a log, terminal output or error message during the session,
  point it out at once and recommend rotation.
- Never copy values from `.env` into versioned files, examples or documentation —
  use placeholders (`DB_PASS=change-me`). Every project has a `.env.example`.

## Critical files — never overwrite without asking
- `.env` — environment credentials
- Lockfiles (`composer.lock`, `package-lock.json`, `Cargo.lock`, `go.sum`...) — locked versions
- `schema.sql` — source of truth for the database
- `public/.htaccess` — rewrite and security rules
- Any migration file already applied in production
