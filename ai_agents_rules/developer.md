# Developer Agent Rules

## Princípios de Código
- Pratique TDD: Teste vermelho, implementação, teste verde, refatoração.
- KISS e YAGNI: Faça a solução mais simples. Só implemente o que será usado agora.
- SOLID com pragmatismo: Interfaces apenas para múltiplas implementações reais ou mock de testes.
- Tratamento de Erros: Explícito em todos os caminhos. Nunca engula exceções (`catch` vazio).
- Código completo: Entregue a implementação inteira. É proibido usar `...` ou "implemente aqui".

## Regras por Linguagem
- **Front-end**: Tailwind ou Bootstrap via CDN (não misture). Zero CSS inline. Ícones via CDN. HTML semântico.
- **Node.js**: ES Modules obrigatório. Funções sobre classes. `.env` via `node --env-file`, sem `dotenv`.
- **PHP**: Composer, PSR-4, namespaces estritos (`declare(strict_types=1)`). PDO com prepared statements.
- **Go**: Use Standard Library primeiro (`net/http` ServeMux 1.22+). `gofmt` limpo. Propague erros com `fmt.Errorf`.
- **C/C++**: C17/C++20. Padrão `-Wall -Wextra -Wpedantic -Werror`. Controle estrito de memória (`free` para cada `malloc`, ou RAII no C++).
- **C#**: .NET LTS. `async/await` de ponta a ponta (proibido `.Result`). Nullable ativado.
- **Rust**: Stable. `cargo fmt` e `clippy` limpos. Sem `unwrap()` fora de testes.
- **Python**: 3.12+, `venv`, `pyproject.toml`. Type hints obrigatórios. Lint com `ruff`.
- **Java**: LTS (21+). `record` para dados. Sem frameworks pesados exceto se solicitado.
