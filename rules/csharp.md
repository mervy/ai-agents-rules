---
paths:
  - "**/*.cs"
  - "**/*.csproj"
---

# C#

- .NET LTS atual (.NET 10, C# 14), `<Nullable>enable</Nullable>`, `dotnet format` limpo.
- `async`/`await` de ponta a ponta; nunca `.Result` ou `.Wait()`.
- Minimal APIs antes de MVC completo; configuração por variáveis de ambiente, sem
  segredos em `appsettings.json`.

## Recursos modernos (não instalado no WSL: confira com `dotnet --version`)
`record` e `required`, construtores primários, expressões de coleção (`[1, 2, 3]`),
*raw strings* (`"""`), `namespace` de arquivo, `global using`, pattern matching; C# 14:
palavra-chave `field` em propriedades e *extension members*.
