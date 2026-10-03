---
paths:
  - "**/*.go"
  - "**/go.mod"
---

# Go

- Biblioteca padrão primeiro: `net/http` com o `ServeMux` de padrões (Go 1.22+),
  `database/sql`, `log/slog`.
- `gofmt` e `go vet` limpos; `go mod tidy` antes de commitar.
- Erros retornados e embrulhados com `fmt.Errorf("...: %w", err)`; `panic` só para bug
  de programação.
- `context.Context` com timeout em I/O; nenhuma goroutine sem dono que a encerre.
- Testes com `go test ./...` (tabela de casos); auditoria com `govulncheck`.
