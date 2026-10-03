# QA Agent Rules

## Regras Bloqueantes de Teste
- Não entregue código sem testes. Correções de bug começam reproduzindo a falha no teste.
- Proibido pular testes (`skip`, `ignore`, baixar tolerância, apagar asserções).
- Nunca delete arquivos de teste sem aprovação explícita.

## Tipos de Teste Exigidos
- Unitários: Para regras de negócio.
- BDD/Gherkin: Para fluxos de usuário.
- Integração/E2E: Bancos, APIs e filas.
- Mutação: Exigido para validar a eficácia da suite (Stryker, Infection, etc).

## Procedimento de Validação (Ordem Fixa)
1. Formatação.
2. Lint e Types.
3. Testes unitários / propriedade.
4. Testes de integração / arquitetura.
5. E2E.
6. Relatório de Cobertura (Mínimo absoluto de 80%, estritamente proibido baixar a métrica existente).
7. Testes de mutação.
8. Auditoria de dependências (`npm audit`, etc).
9. Varredura de segredos.
- Relate os resultados ao final. Qualquer falha bloqueia a continuidade.
