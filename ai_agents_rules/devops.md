# DevOps Agent Rules

## Git e Controle de Versão
- Nunca faça push, force-push, `reset --hard` ou delete branches sem aprovação explícita.
- Tags devem ser anotadas (`git tag -a`), nunca leves.
- Commits no padrão Conventional Commits (`feat:`, `fix:`, etc) em português.
- Proibido adicionar assinaturas geradas por IA (`Co-Authored-By`, `Generated with`).

## Segurança e Segredos
- Varredura de diff: Bloqueie a entrega se contiver senhas, chaves ou tokens.
- Se um segredo já foi versionado, exija rotação imediata, não apenas a exclusão do arquivo.
- OWASP: Valide e normalize entradas no backend. Escape saídas para evitar XSS. Autenticação estrita.
- Menor privilégio: Nunca use credenciais de produção para operações rotineiras.

## Dependências e Operações
- Nunca rode `update` solto (ex: `npm update`, `composer update`). Use `install` ou `ci` para respeitar lockfiles.
- Lockfiles abertos (ex: `*`, `latest`) são proibidos.
- Logs: Devem ser estruturados, sem dados sensíveis (cartões, senhas, documentos).
- A aplicação deve falhar imediatamente na inicialização se faltar uma variável de ambiente essencial.
- Exija a implementação de rota de health check (ex: `/health`) em serviços web.
