# Subagent: dependencies

- **Never run `composer update`** (nor `npm update`, `cargo update` and similar)
  without authorization — can break production versions.
- `composer install`, `composer dump-autoload` and `npm ci` are safe; may run without asking.
- Do not add a dependency without need; when adding, justify in one line.
- **Locked versions**: lockfile always versioned in applications; no open ranges
  (`*`, `latest`). Do not update a package without request.
