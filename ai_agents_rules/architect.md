# Architect Agent Rules

## Estrutura e Escopo
- Defina o escopo de arquivos no início da tarefa. Precisa mexer fora do combinado? Pergunte antes.
- Mudanças pequenas: limite de ~400 linhas alteradas por entrega. Maior que isso, exija divisão.
- Projetos Novos: Entregue estrutura de pastas, README, dependências, `.env.example`, suite de testes inicial, lint e CI/CD.

## Decisões Técnicas (ADR)
- Qualquer decisão técnica estrutural (arquitetura, libs, formato) deve gerar um arquivo em `docs/adr/NNNN-titulo.md` contendo: contexto, decisão, alternativas e consequências.

## Banco de Dados e Migrations
- Nunca execute `migrations`, modifique `schema.sql`, ou rode `DROP/TRUNCATE/DELETE sem WHERE` sem autorização.
- Modelagem de Deleção: `ON DELETE CASCADE` nunca é padrão. Use apenas quando o registro filho for inútil sem o pai. Para vínculos ou categorias, exija `RESTRICT` ou `SET NULL`. Justifique cada FK.
- Toda migration deve ter um rollback (`down`) correspondente e testado.
- Exija parâmetros (prepared statements) em todas as consultas SQL sugeridas.
