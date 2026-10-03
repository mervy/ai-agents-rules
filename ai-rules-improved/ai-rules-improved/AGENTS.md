# Regras globais para assistentes de IA

Este arquivo contém apenas regras invariantes. Regras especializadas ficam em `agents/` e são acionadas conforme a tarefa.

## 1. Prioridades

1. Segurança e preservação de dados.
2. Instrução explícita do usuário.
3. Escopo combinado para a tarefa.
4. Regras específicas do projeto (`README`, `AGENTS.md`, documentação local).
5. Estas regras globais.

Se houver conflito que não possa ser resolvido por essa ordem, pare e pergunte.

## 2. Portabilidade e configuração

- Este arquivo pode ser público: nunca inclua segredos, dados pessoais, nomes privados de projetos ou caminhos específicos da máquina.
- Valores locais ficam em `.env`, não versionado, e aparecem aqui como `$NOME`.
- `.env.example` deve listar todas as variáveis com placeholders seguros.
- Se uma variável necessária estiver ausente, pergunte; nunca invente caminho ou valor.

## 3. Comunicação

- Responda em português do Brasil; identificadores de código permanecem em inglês.
- Seja direto e curto por padrão; aprofunde quando necessário ou solicitado.
- Ambiguidade cara de errar: pergunte antes. Barata de refazer: assuma a interpretação mais razoável e declare a suposição.
- Nunca invente fatos, APIs, versões, funções, resultados de comandos ou testes.
- Não amplie o escopo silenciosamente; sugira trabalho extra em vez de executá-lo.
- Diferencie claramente: **verificado**, **inferido** e **não verificado**.
- Só diga “testado”, “passou” ou “funciona” quando houver comando executado e evidência observável.
- Ao usar pesquisa externa, cite a fonte.

## 4. Escopo e fluxo de trabalho

- Antes de editar, determine os arquivos/pastas dentro do escopo. Se precisar sair dele, peça autorização.
- Prefira mudanças pequenas, coesas e reversíveis. Um PR deve ter uma responsabilidade principal.
- Para bugs e lógica nova, use TDD quando tecnicamente aplicável: teste falhando → implementação mínima → refatoração com testes verdes.
- Decisão arquitetural relevante deve gerar ADR curto em `docs/adr/NNNN-titulo.md`.
- Mudança não trivial deve receber revisão independente; o revisor recebe requisitos e diff, não a conversa de implementação.
- Não recrie um arquivo para renomeá-lo: faça move/rename real e valide integridade quando houver risco de perda.

## 5. Operações que sempre exigem confirmação

Nunca execute sem autorização explícita:

- `git push`, force-push, `git reset --hard`, exclusão de branch ou alteração destrutiva do histórico;
- deploy, publicação externa, gist, post ou envio a serviço externo;
- migrations ou alteração de schema em banco;
- `DROP TABLE`, `TRUNCATE`, `DELETE` sem `WHERE` ou outra operação destrutiva de dados;
- exclusão de arquivos, sobrescrita irreversível, encerramento de processos ou mudança ampla de permissões;
- atualização ampla de dependências (`composer update`, `npm update`, `cargo update` e equivalentes);
- sobrescrita de `.env`, lockfiles, `schema.sql`, migrations já aplicadas ou outros arquivos críticos do projeto.

Antes de pedir confirmação, explique exatamente o efeito esperado.

## 6. Git

- Conventional Commits; descrição em português.
- Branch curta por tarefa: `feature/...`, `fix/...` ou `chore/...`.
- Mudanças entram por PR com: o que mudou, por quê e como testar.
- Tags são anotadas.
- Não adicione trailers de coautoria nem assinatura de ferramenta.
- Nunca faça amend de commit já publicado sem autorização explícita.

## 7. Dependências e segredos

- Não adicione dependência sem necessidade; justifique cada nova dependência.
- Aplicações versionam lockfile; não use `*` ou `latest`.
- Antes de commit, verifique o diff por senhas, chaves, tokens, connection strings e dados pessoais.
- Se um segredo foi versionado, informe que removê-lo do arquivo não basta: a credencial precisa ser rotacionada e o histórico pode precisar de limpeza autorizada.
- Nunca copie valores reais de `.env` para documentação, exemplos ou arquivos versionados.

## 8. Banco de dados

- SQL sempre parametrizado; nunca concatene entrada do usuário.
- `ON DELETE CASCADE` só quando a vida do filho depende integralmente do pai; caso contrário prefira `RESTRICT` ou `SET NULL` conforme o domínio.
- Ao propor schema, liste e justifique cada FK com `CASCADE`.
- Migration deve ser versionada e reversível, ou documentar por que rollback seguro não existe.
- Apresente SQL proposto antes de qualquer execução destrutiva.

## 9. Código

- KISS e YAGNI. SOLID com pragmatismo.
- Código completo: sem `...`, stubs ocultos ou “implemente aqui”.
- Nomes claros; funções pequenas; uma responsabilidade; sem código morto.
- Identificadores em inglês; comentários em português e apenas para explicar o **porquê** não óbvio.
- Trate erros explicitamente; nunca engula exceções.
- Toda I/O de rede deve ter timeout.
- UTF-8 em tudo; considere corretamente acentos em busca, ordenação e slug.
- Configuração varia por ambiente; código não.

## 10. Segurança e operação

Em qualquer mudança que processe entrada externa, verifique: validação e limites; injeção; XSS/escape; upload seguro; autenticação e autorização; CSRF quando aplicável; headers de segurança; rate limiting em endpoints sensíveis.

- Princípio do menor privilégio; não use credenciais de produção no desenvolvimento.
- Logs estruturados quando possível, sem segredos ou dados sensíveis.
- Mensagem ao usuário deve ser segura; detalhe técnico fica no log.
- Valide variáveis obrigatórias na inicialização e falhe cedo com mensagem clara.
- Serviços web devem ter health check quando isso fizer sentido operacionalmente.

## 11. Definição de pronto

Uma entrega só está pronta quando houver evidência para os itens aplicáveis:

- [ ] requisito atendido dentro do escopo;
- [ ] testes novos/alterados cobrem comportamento, erros e bordas relevantes;
- [ ] QA aplicável executado e reportado;
- [ ] imports, pacotes e dependências conferidos;
- [ ] diff sem segredos;
- [ ] README, ADR e `.env.example` atualizados quando necessário;
- [ ] relatório final informa o que mudou, como testar, o que foi verificado e o que não foi.

## 12. Sub-agentes

Use sub-agentes por **responsabilidade**, não por linguagem. O agente principal mantém contexto, escopo e decisão final.

- `agents/qa-engineer.md`: testes, cobertura, lint, tipos, mutation e CI.
- `agents/security-reviewer.md`: segurança, segredos, autorização e riscos destrutivos.
- `agents/code-reviewer.md`: revisão independente de diff e requisitos.
- `agents/database-reviewer.md`: schema, migrations, SQL, integridade e rollback.
- `agents/docs-writer.md`: README, ADR, documentação e instruções operacionais.
- `agents/metrics-reporter.md`: métricas de sessão e handoff de contexto.

Não delegue a sub-agente a autorização de operação destrutiva. Ele pode detectar e recomendar; a confirmação continua entre agente principal e usuário.

## 13. Regras específicas por linguagem

As convenções abaixo são defaults e cedem às convenções explícitas do projeto.

- **JavaScript/Node:** ES Modules; funções/módulos antes de classes; recursos nativos do Node antes de dependências equivalentes; timeout em rede.
- **PHP:** Composer + PSR-4, namespaces, `strict_types`, PDO parametrizado e escape de saída.
- **Go:** stdlib primeiro, `gofmt`, `go vet`, erros com contexto e `context.Context` em I/O.
- **C:** C17, warnings rigorosos, sanitizers em debug, retornos checados e memória com ownership claro.
- **C++:** C++20, CMake, RAII, smart pointers e STL antes de implementação própria.
- **C#:** .NET LTS, nullable habilitado, async de ponta a ponta.
- **Rust:** stable, `cargo fmt`, `clippy -D warnings`, evitar `unwrap`/`expect` em produção.
- **Python:** 3.12+, `pyproject.toml`, type hints, Ruff, `pathlib`, exceções específicas e timeout HTTP.
- **Java:** LTS, um build tool por projeto, `try-with-resources`, exceções não engolidas.
- **Front-end:** HTML semântico e acessível; não misture frameworks CSS; evite CSS inline quando o projeto usa stylesheet/framework.

## 14. Projetos novos

Ao criar projeto novo, entregue estrutura, README, dependências/configuração, `.env.example`, comandos de instalar/rodar/testar, testes, lint e CI mínimos. Siga a convenção da linguagem e do ecossistema para lockfiles e arquivos gerados.
