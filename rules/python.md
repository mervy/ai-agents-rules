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
