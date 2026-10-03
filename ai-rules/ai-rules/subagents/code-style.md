# Subagent: code-style

## General
- **KISS**: the simplest solution that works. **YAGNI**: only what will be used now.
- **SOLID** with common sense; interface only when there is more than one real
  implementation or a concrete need for testing — no interface "just in case".
- Clean code: clear names, short single-responsibility functions, no dead code.
- Deliver complete, working code — no `...` or "implement here".
  Before calling it done, review imports, declared dependencies, package names and versions.
- Identifiers in English; comments in Portuguese.
- Comment the **why** in complex code or functions (business rule, decision,
  trap, non-trivial algorithm). **Do not comment the obvious** or repeat what the code already says.
- Handle errors explicitly on every path; never empty `catch` or swallowed errors.
- Timeout on every network call (HTTP, database, queues).
- UTF-8 everywhere; handle Portuguese accents (slug, sorting, search).
- Configuration via environment variables (local `.env`, never versioned).

## JavaScript / Node
- Always ES Modules (`import`/`export`); `"type": "module"` in `package.json`.
- **No classes**: functions and modules.
- `.env` read by Node itself (`node --env-file=.env` or `process.loadEnvFile()`),
  no `dotenv`.
- Development with `node --watch` (no nodemon).
- Modular projects; errors handled in all cases (`try/catch` in `async`,
  central error handler on the server, `AbortSignal.timeout()` on `fetch`).

## PHP
- Composer + PSR-4 always, with namespaces; `declare(strict_types=1);` in files.
- Routes in a separate file.
- Minimal frameworks. Immediately approved: `league/plates` (templates) and
  `vlucas/phpdotenv` (`.env`). Any other, ask first.
- PDO with prepared statements; escape every output in the template.
- **Content URLs**: each project defines the pattern in its own README.

## Go
- Standard library first (`net/http` with Go 1.22+ pattern `ServeMux`,
  `database/sql`, `log/slog`).
- `gofmt` and `go vet` clean; `go mod tidy` before committing.
- Errors returned and wrapped with `fmt.Errorf("...: %w", err)`; `panic` only for
  programming bugs.
- `context.Context` with timeout on I/O; no ownerless goroutine that never ends.

## C
- C17, compile with `-Wall -Wextra -Wpedantic -Werror`; in debug,
  `-fsanitize=address,undefined`.
- Check the return of **every** call that can fail (`malloc`, `fopen`, `read`...).
- No `gets`, `strcpy`, `sprintf`: use `fgets`, `snprintf` and explicit sizes.
- Every `malloc` with its clear `free`; a simple `Makefile` for build.

## C++
- C++20, CMake, same warnings as C treated as errors.
- RAII always; `std::unique_ptr`/`std::shared_ptr`, never bare `new`/`delete`.
- STL containers and algorithms before custom code; `const` by default.
- Avoid macros and deep inheritance.

## C#
- Current .NET LTS, `<Nullable>enable</Nullable>`, `dotnet format` clean.
- `async`/`await` end-to-end; never `.Result` or `.Wait()`.
- Minimal APIs before full MVC; configuration via environment variables, no
  secrets in `appsettings.json`.

## Rust
- Stable; `cargo fmt` and `cargo clippy -- -D warnings` clean.
- No `unwrap()`/`expect()` outside tests: propagate with `?`; `thiserror` in
  libraries, `anyhow` in binaries.
- `Cargo.lock` versioned in binaries; `dotenvy` to read `.env`.

## Python
- Python 3.12+, virtual environment (`venv`), dependencies in `pyproject.toml`.
- Type hints, `ruff` (lint + format), `pathlib`, f-strings.
- Never bare `except:`; catch the specific exception.
- Standard library first; `requests`/`httpx` always with `timeout=`.

## Java
- Current LTS (21+), one build system per project (Maven **or** Gradle).
- `record` for data, `try-with-resources` for resources, `Optional` only on return.
- Never swallow exceptions; no heavy frameworks (Spring etc.) without explicit request.
