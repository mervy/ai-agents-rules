# Subagent: database

- **Never run migrations** (`mysql < *.sql`, `php artisan migrate`, etc.) without explicit authorization.
- **Never modify `schema.sql`** unless the user explicitly asks.
- **Never run `DROP TABLE`, `TRUNCATE` or `DELETE` without `WHERE`** without explicit authorization.
- **`ON DELETE CASCADE` is a conscious decision, never the default.** When creating/altering foreign keys, choose the deletion behaviour deliberately:
  - `CASCADE` only when the child record makes no sense without the parent (e.g. reactions of a deleted article);
  - for authorship and categorization links (user → articles, category → articles, upload/image → articles), prefer `RESTRICT` (blocks deletion) or `SET NULL` — deleting a user/category/image **must not cascade-delete** related content;
  - when proposing a schema, list every FK with `CASCADE` and justify each one;
  - before any `DELETE` on a parent table, warn what will be cascade-deleted.
- When suggesting schema changes, present the SQL and wait for approval before any execution.
- Migrations **versioned and reversible**: every migration has a written and tested
  rollback path (`down`), or explains why it is impossible.
- Queries always use parameters (prepared statements); never concatenate user input into SQL.
