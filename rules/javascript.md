---
paths:
  - "**/*.{js,mjs,cjs,ts,mts,jsx,tsx}"
  - "**/package.json"
---

# JavaScript / Node

- Sempre ES Modules (`import`/`export`); `"type": "module"` no `package.json`.
- **Sem classes**: funções e módulos.
- `.env` lido pelo próprio Node (`node --env-file=.env` ou `process.loadEnvFile()`),
  sem `dotenv`. Desenvolvimento com `node --watch`, sem nodemon.
- Node LTS atual. TypeScript, quando usado, roda direto pelo *type stripping* do Node
  (só sintaxe apagável: nada de `enum`, `namespace`, parameter properties) e
  `tsc --noEmit` faz a checagem de tipos.
- Testes com `node:test` por padrão; Vitest só se o projeto já usar ou precisar
  (front-end com bundler).
- Erros tratados em todos os casos: `try/catch` em `async`, handler central no
  servidor, `AbortSignal.timeout()` em todo `fetch`.
- Scripts `test`, `lint` e `format` no `package.json`; CI usa `npm ci`.
