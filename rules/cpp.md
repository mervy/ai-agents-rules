---
paths:
  - "**/*.{cpp,cc,cxx,hpp,hh}"
  - "**/CMakeLists.txt"
---

# C++

- C++20, CMake, mesmos avisos do C tratados como erro.
- RAII sempre; `std::unique_ptr`/`std::shared_ptr`, nunca `new`/`delete` soltos.
- Contêineres e algoritmos da STL antes de código próprio; `const` por padrão.
- Evitar macros e herança profunda.
