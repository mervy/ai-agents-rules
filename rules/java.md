---
paths:
  - "**/*.java"
  - "**/pom.xml"
  - "**/build.gradle*"
---

# Java

- LTS atual (25+), um build por projeto (Maven **ou** Gradle).
- `record` para dados, `try-with-resources` para recursos, `Optional` só em retorno.
- Nunca engolir exceção; sem frameworks pesados (Spring etc.) sem pedido explícito.
- Mutação com PIT; arquitetura com ArchUnit quando houver camadas.

## Recursos modernos (Java 25; não instalado no WSL: confira com `java -version`)
`record` e `sealed`, pattern matching no `switch` e *record patterns*, *virtual
threads*, *text blocks*, `var`, coleções sequenciadas (`getFirst()`), arquivos-fonte
compactos com `void main()`, import de módulo, corpo de construtor flexível e
*scoped values*.
