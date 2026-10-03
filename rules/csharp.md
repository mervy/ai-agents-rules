---
paths:
  - "**/*.cs"
  - "**/*.csproj"
---

# C#

- .NET LTS atual, `<Nullable>enable</Nullable>`, `dotnet format` limpo.
- `async`/`await` de ponta a ponta; nunca `.Result` ou `.Wait()`.
- Minimal APIs antes de MVC completo; configuração por variáveis de ambiente, sem
  segredos em `appsettings.json`.
