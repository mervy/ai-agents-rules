---
paths:
  - "**/*.php"
  - "**/composer.json"
---

# PHP

- Composer + PSR-4 com namespaces; `declare(strict_types=1);` em todo arquivo.
- Rotas em arquivo à parte.
- Mínimo de frameworks. Aprovados de imediato: `league/plates` (templates) e
  `vlucas/phpdotenv` (`.env`). Qualquer outro: pergunte antes.
- PDO com prepared statements; escapar toda saída no template.
- Ferramentas (só dev): PHPUnit ou Pest nos testes, PHPStan para análise estática,
  PHP-CS-Fixer (`@PER-CS`) para formatação, Infection para mutação e `composer audit`.
  Use as que o projeto já tem; ao introduzir uma, justifique e registre no README.
- `composer.json` com `scripts` para `test`, `lint` e `format`, usados também pelo CI.
- **URLs de conteúdo**: cada projeto define o padrão no próprio README.
