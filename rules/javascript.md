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

## Recursos modernos (Node 26 instalado)
Declare `"engines": { "node": ">=24" }` e prefira o que já vem no Node a pacotes:
- `.env`: `node --env-file=.env` ou `process.loadEnvFile()`; reload: `node --watch`
  (`--watch-path` para pastas); scripts com `node --run <script>`.
- Testes: `node --test` (com `--watch` e `--experimental-test-coverage`); `fetch`,
  `AbortSignal.timeout()` e `structuredClone()` globais; `import.meta.dirname`.
- CLI e terminal: `util.parseArgs()`, `util.styleText()` (sem chalk/yargs).
- Linguagem: `Object.groupBy()`, `toSorted()`/`toReversed()`/`with()`,
  `Promise.withResolvers()`, métodos de `Set` (`union`, `intersection`), iterator
  helpers, `using` só se a versão suportar.
- `node:sqlite` para SQLite sem dependência: confira antes com
  `node -e "import('node:sqlite').then(()=>console.log('ok'))"`.
