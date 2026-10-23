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
- Ferramentas (só dev): PHPUnit ou Pest para testes básicos, PHPStan para análise
  estática, PHP-CS-Fixer (`@PER-CS`) para formatação e `composer audit`.
  Use as que o projeto já tem; ao introduzir uma, justifique e registre no README.
- `composer.json` com `scripts` para `test`, `lint` e `format`.
- **URLs de conteúdo**: cada projeto define o padrão no próprio README.

## Recursos modernos (PHP 8.4+; 8.5 instalado)
Declare `"php": ">=8.4"` no `composer.json` e prefira:
- **Promoção de propriedades no construtor** + `readonly`:
  ```php
  final class User
  {
      public function __construct(
          public readonly int $id,
          private string $name,
      ) {}
  }
  ```
- `enum` (com métodos e `cases()`) em vez de constantes soltas; `readonly class` para
  objetos de valor; `match` em vez de `switch`; argumentos nomeados; `?->`.
- Callable de primeira classe (`strlen(...)`), `new` em inicializadores, tipos `never`,
  DNF e constantes de classe tipadas; `#[\Override]` ao sobrescrever.
- 8.4: *property hooks*, visibilidade assimétrica (`public private(set)`),
  `new Foo()->metodo()` sem parênteses extras, `array_find()`, `array_any()`, `array_all()`.
- 8.5: operador pipe (`$x |> trim(...) |> strtoupper(...)`), `array_first()`,
  `array_last()`, `#[\NoDiscard]`.
