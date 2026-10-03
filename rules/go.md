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

## Recursos modernos (Go 1.27 instalado)
`go.mod` com a versão instalada (`go 1.27`) e prefira:
- `for i := range 10`; variável de loop nova a cada iteração (sem `v := v`).
- Rotas com método e parâmetro: `mux.HandleFunc("GET /items/{id}", h)` + `r.PathValue("id")`.
- Iteradores (`range` sobre funções), pacotes `slices`, `maps` e `cmp`
  (`slices.Sorted(maps.Keys(m))`), `min`/`max`/`clear` nativos, `errors.Join`.
- Testes: `b.Loop()` em benchmarks, `t.Context()`; ferramentas com a diretiva `tool`
  no `go.mod`; `sync.WaitGroup.Go()`; `os.Root` para acesso restrito a uma pasta.
