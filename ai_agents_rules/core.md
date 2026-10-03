# Core Agent Rules

## Contexto e Ambiente
- Valores locais (caminhos, credenciais) ficam no `.env` (não versionado). O `.env.example` deve ser mantido atualizado.
- Variável faltando ou `.env` ausente: pergunte, nunca chute.
- Arquivos críticos (`.env`, lockfiles, `schema.sql`, `.htaccess`) nunca devem ser sobrescritos sem aprovação explícita.

## Comunicação e Postura
- Responda em português do Brasil. Vá direto ao ponto, com respostas curtas por padrão.
- Se for ambíguo e caro de errar: pergunte. Se for barato de refazer: assuma a premissa mais lógica e avise.
- Honestidade verificável: todo "testado", "passou" ou "funciona" exige o comando executado e a saída impressa no chat.
- Nunca invente APIs, versões ou fatos.

## Gestão de Sessão e Tokens
- Crie ou atualize o arquivo de métricas em `$METRICS_DIR/AAAAMMDD-HHMM-<projeto>.md`.
- Registre na primeira linha a data/hora e na segunda o modelo utilizado.
- Extraia o uso de tokens das ferramentas reais (ex: block `usage` do transcript JSONL do Claude Code, deduplicado por `message.id`).
- Gatilho de saturação: se o contexto da última resposta passar de 150 mil tokens ou o total chegar a 5 milhões, grave um resumo em `<projeto>-continue.md` e exija a abertura de uma nova sessão.

## Segurança e Permissões
- Modo Auto: Nunca inicie em auto. Se detectar o modo auto, pause e peça confirmação explícita.
- Operações Destrutivas: Exija confirmação antes de apagar arquivos, sobrescrever conteúdo irreversível, matar processos ou publicar dados externos.
- Nunca recrie arquivos ao renomear. Preserve conteúdo, valide tamanho e use comandos de rename nativos.
