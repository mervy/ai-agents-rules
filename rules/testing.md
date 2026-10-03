---
paths:
  - "**/tests/**"
  - "**/test/**"
  - "**/*{.test,.spec,_test,Test}.*"
  - "**/features/**"
---

# Escrevendo testes

Bloqueante: o código do agente não é lido linha a linha; a confiança vem dos testes.

- **Nunca** apague testes, nem use `skip`/`ignore`/`only`, apague asserção, afrouxe
  comparação, aumente tolerância ou mocke o próprio código sob teste para ficar verde.
  Teste errado? Explique e pergunte.
- Antes de mexer em código que já tem testes, rode-os e confirme o verde.
- Ao remover classe/método, veja que testes o cobrem antes de apagar.

## Que teste usar
- **Unitário**: toda regra de negócio e função com lógica.
- **Gherkin/BDD** (`Dado / Quando / Então`): comportamento visível ao usuário, a partir
  dos requisitos (Behat, Cucumber, behave).
- **Integração**: banco, filas, APIs externas, sistema de arquivos. **Ponta a ponta**:
  fluxos principais.
- **Propriedade**: funções puras com entrada ampla (parser, slug, cálculo).
- **Contrato**: API com OpenAPI/JSON Schema valida requisição e resposta contra ele.
- **Arquitetura**: limites entre camadas (deptrac, dependency-cruiser, ArchUnit).

## Metas
- Cobertura mínima de 80% de linhas e branches; a cobertura existente nunca cai.
- Mutação no código alterado: mutante sobrevivente = teste faltando (ou justificativa).
