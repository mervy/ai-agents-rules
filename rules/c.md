---
paths:
  - "**/*.{c,h}"
---

# C

- **C23** (`-std=c23`, GCC 14+); C17 só se o compilador não suportar. Compilado com `-Wall -Wextra -Wpedantic -Werror`; em debug,
  `-fsanitize=address,undefined`.
- Checar o retorno de **toda** chamada que pode falhar (`malloc`, `fopen`, `read`...).
- Nada de `gets`, `strcpy`, `sprintf`: use `fgets`, `snprintf` e tamanhos explícitos.
- Cada `malloc` com seu `free` claro; um `Makefile` simples para o build.

## Recursos modernos (C23, GCC 14 instalado)
`nullptr`, `bool`/`true`/`false` sem include, `constexpr` em objetos, `typeof`,
`auto` em declarações, atributos `[[nodiscard]]` (em funções) e `[[maybe_unused]]`, literais
binários (`0b1010`) e separador de dígitos (`1'000'000`), `static_assert` sem mensagem.
