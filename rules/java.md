---
paths:
  - "**/*.java"
  - "**/pom.xml"
  - "**/build.gradle*"
---

# Java

- Versão mais recente instalada (27; mínimo 25 LTS), um build por projeto (Maven **ou** Gradle).
- `record` para dados, `try-with-resources` para recursos, `Optional` só em retorno.
- Nunca engolir exceção; sem frameworks pesados (Spring etc.) sem pedido explícito.
- Mutação com PIT; arquitetura com ArchUnit quando houver camadas.

## Recursos modernos (JDK 27 instalado)
`record` e `sealed`, pattern matching no `switch` e *record patterns*, *virtual
threads*, *text blocks*, `var`, coleções sequenciadas (`getFirst()`), arquivos-fonte
compactos com `void main()` e `IO.println` (rodam com `java Main.java`), import de módulo
(`import module java.base;`), corpo de construtor flexível e
*scoped values*.
