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
