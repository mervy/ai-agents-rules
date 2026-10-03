---
paths:
  - "**/*.{cpp,cc,cxx,hpp,hh}"
  - "**/CMakeLists.txt"
---

# C++

- **C++23** (`-std=c++23`), CMake 4 (`set(CMAKE_CXX_STANDARD 23)`), mesmos avisos do C tratados como erro.
- RAII sempre; `std::unique_ptr`/`std::shared_ptr`, nunca `new`/`delete` soltos.
- Contêineres e algoritmos da STL antes de código próprio; `const` por padrão.
- Evitar macros e herança profunda.

## Recursos modernos (C++23, GCC 14 instalado)
`std::print`/`std::println` em vez de `iostream`/`printf`, `std::expected` para erros
sem exceção, `std::ranges::to`, *deducing this*, `std::format`, ranges e `views`,
`constexpr` e `consteval`. Módulos: só quando o build estiver pronto para eles.
