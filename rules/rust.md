---
paths:
  - "**/*.rs"
  - "**/Cargo.toml"
---

# Rust

- Stable; `cargo fmt` e `cargo clippy -- -D warnings` limpos.
- Sem `unwrap()`/`expect()` fora de testes: propague com `?`; `thiserror` em
  bibliotecas, `anyhow` em binários.
- `Cargo.lock` versionado em binários, não em bibliotecas; `dotenvy` para ler `.env`.
- Propriedade com `proptest`; mutação com `cargo-mutants`; auditoria com `cargo audit`.

## Recursos modernos (Rust 1.98 instalado)
`edition = "2024"` e `rust-version` no `Cargo.toml`; prefira:
- `let ... else` e *let chains* (`if let Some(x) = a && x > 0`).
- `async fn` em traits; `std::sync::LazyLock` em vez de `lazy_static`/`once_cell`.
- `#[expect(lint)]` em vez de `#[allow]` quando a exceção é pontual.
