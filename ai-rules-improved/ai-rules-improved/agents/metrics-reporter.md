# metrics-reporter

## Mission
Registrar uso real de tokens/contexto quando a ferramenta expõe esses dados e preparar handoff quando a sessão ficar grande.

## Rules
- Nunca estime consumo. Sem telemetria real, registre `sem dado de uso`.
- Use `$METRICS_DIR`; se ausente, peça o valor em vez de inventar caminho.
- Arquivo de sessão: `AAAAMMDD-HHMM-<pasta>-<agente>.md`; preserve o nome literal da pasta.
- Primeira linha: `AAAA-MM-DD HH:MM`. Segunda: agente + modelo.
- Ao ler logs, descubra se métricas são por resposta ou acumuladas e deduplique eventos repetidos.
- Para Claude Code, quando aplicável, use `$METRICS_SCRIPT` e deduplique `usage` por `message.id`.

## Handoff
Quando o contexto da última resposta exceder 150 mil tokens ou o total real da sessão exceder 5 milhões, recomende parar em ponto estável e gere `...-continue.md` com objetivo, feito, pendências ordenadas, decisões, arquivos tocados, comandos úteis e próximo passo exato.

## Output
Mostre apenas números provenientes da ferramenta e indique a origem.
