# Subagent: git

- **Never push**: always ask; execute only after explicit authorization.
- **Never force-push** (`--force`, `--force-with-lease`) without explicit authorization.
- **Never run `git reset --hard`** without explicit authorization.
- **Never amend already-published commits** (`git commit --amend` on a commit that has been pushed).
- **Never delete branches** without confirmation.
- **Tags always annotated** (`git tag -a`), never lightweight: every tag must carry
  author, date and its own message.
- Messages follow **Conventional Commits** (`feat:`, `fix:`, `docs:`, `refactor:`,
  `chore:`, `test:`), description in Portuguese.
- Short branch, one per task: `feature/...`, `fix/...`, `chore/...`.
- Changes enter via Pull Request, with description of **what changed**, **why**
  and **how to test**.
- **No co-authorship trailers or tool signatures in commits**: do not add
  `Co-Authored-By: ...`, "Generated with ..." or similar to commit or PR messages.
  The message describes the change, nothing more.
