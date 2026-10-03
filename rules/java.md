---
paths:
  - "**/*.java"
  - "**/pom.xml"
  - "**/build.gradle*"
---

# Java

- LTS atual (21+), um build por projeto (Maven **ou** Gradle).
- `record` para dados, `try-with-resources` para recursos, `Optional` só em retorno.
- Nunca engolir exceção; sem frameworks pesados (Spring etc.) sem pedido explícito.
- Mutação com PIT; arquitetura com ArchUnit quando houver camadas.
