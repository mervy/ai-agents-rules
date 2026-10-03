---
paths:
  - "**/*.sql"
  - "**/migrations/**"
  - "**/database/**"
---

# Banco de dados e migrations

As proibições (executar migration, `DROP`, `TRUNCATE`, `DELETE` sem `WHERE`, alterar
`schema.sql`) estão no `AGENTS.md` e valem sempre. Aqui fica o **como fazer**.

- Consultas sempre parametrizadas; nunca concatenar entrada do usuário em SQL.
- Ao propor mudança de schema, apresente o SQL e aguarde aprovação.
- Migrations versionadas e reversíveis: todo `up` tem `down` escrito e testado, ou o
  motivo por que não é possível.
- **`ON DELETE CASCADE` é decisão consciente, nunca padrão:**
  - `CASCADE` só quando o filho não faz sentido sem o pai (ex.: reações de um artigo);
  - autoria e categorização (usuário → artigos, categoria → artigos, imagem → artigos):
    `RESTRICT` ou `SET NULL`; apagar usuário/categoria/imagem não apaga conteúdo;
  - ao propor schema, liste toda FK com `CASCADE` e justifique cada uma;
  - antes de `DELETE` em tabela-pai, avise o que sai em cascata.
- Usuário de banco da aplicação sem permissão de DDL em produção.
- Para revisão completa (locks, índices, backfill), chame o `db-reviewer`.
