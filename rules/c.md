---
paths:
  - "**/*.{c,h}"
---

# C

- C17, compilado com `-Wall -Wextra -Wpedantic -Werror`; em debug,
  `-fsanitize=address,undefined`.
- Checar o retorno de **toda** chamada que pode falhar (`malloc`, `fopen`, `read`...).
- Nada de `gets`, `strcpy`, `sprintf`: use `fgets`, `snprintf` e tamanhos explícitos.
- Cada `malloc` com seu `free` claro; um `Makefile` simples para o build.
