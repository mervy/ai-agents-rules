---
paths:
  - "**/*.py"
  - "**/pyproject.toml"
---

# Python

- Python 3.12+, `venv`, dependências em `pyproject.toml`.
- Type hints, `ruff` (lint + format), `pathlib`, f-strings.
- Nunca `except:` nu; capture a exceção específica.
- Biblioteca padrão primeiro; `requests`/`httpx` sempre com `timeout=`.
- Testes com `pytest`; propriedade com Hypothesis; mutação com `mutmut`; auditoria com
  `pip-audit`.

## Recursos modernos (3.13 no WSL, 3.14 no Windows)
Declare `requires-python = ">=3.12"` e prefira:
- `match`/`case`; tipos `X | None`; `type Alias = ...` e genéricos `def f[T](x: T)`;
  `@override` (de `typing`).
- `@dataclass(slots=True, kw_only=True)`; `tomllib`; `pathlib.Path.walk()`;
  `itertools.batched()`; `copy.replace()` (3.13).
- `asyncio.TaskGroup` e `except*` para erros concorrentes.
- Só 3.14: *template strings* (`t"..."`) e anotações avaliadas sob demanda; use apenas
  se o projeto declarar `>=3.14`.
