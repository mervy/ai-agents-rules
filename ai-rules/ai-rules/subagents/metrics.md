# Subagent: metrics

## Token metrics per session (all agents)

- **Before starting work**, ensure `$METRICS_DIR` exists and create the session file:
  `YYYYMMDD-HHMM-<work-folder>.md`, where `<work-folder>` is the **literal** name of
  the project folder, including a leading `_` if present — e.g. `20260923-0856-_my-project.md`.
  Because date/time always changes, sessions for the same folder never collide.
  Non-Claude-Code agents append their own name: `20260923-0856-_my-project-codex.md`.
- First line of the file is the date and time (`YYYY-MM-DD HH:MM`), nothing else.
  Second line states the agent and model (e.g. `Copilot + DeepSeek V4 Pro`).
- Annotate tokens spent per step in a table throughout the session.
- **At the end of the session, show the total tokens spent** and write it to the file.
- Numbers always come from the tool's real usage record, **never from estimates**.
  If the tool does not expose usage, write "no usage data" and tell the user.

### Claude Code
- Numbers come from the `usage` block of the JSONL transcript
  (`~/.claude/projects/<cwd-slug>/<session-id>.jsonl`).
  Use `$METRICS_SCRIPT [transcript]`.
- Trap: each assistant response occupies **multiple lines** in the JSONL
  (thinking, text, tool_use) repeating the same `usage`. Deduplicate by
  `message.id` — raw sum inflates the total by ~2.5×.
- `usage` appears only after the response is written, so intermediate notes
  reflect the state up to the previous response; the final total is exact.

### Other agents (Codex, Copilot, etc.)
- Create **your own script** in `$METRICS_DIR/ai-metrics-<agent>.sh`
  (e.g. `ai-metrics-codex.sh`), in the same spirit as `$METRICS_SCRIPT`:
  receives the session (or picks the most recent) and prints input, cache,
  output and total.
- Before writing, discover where the tool records usage (session log, API response,
  provider dashboard) and check the format on a real file.
  Example: Codex stores sessions in `~/.codex/sessions/`.
- Watch the same traps: repeated lines for the same response and cumulative
  totals versus per-response values.
- If the script already exists, use it; adjust only if the tool's format changed.

### Session too expensive → continue in another
- Trigger: context of the last response (`input + cache_creation + cache_read`) above
  **150 k tokens**, or session total above **5 M**.
- When reached: stop at a stable point and create
  `$METRICS_DIR/YYYYMMDD-HHMM-<work-folder>-continue.md` with:
  goal, what was done, what remains (ordered), decisions taken and why,
  touched files, useful commands and the exact next step.
- Write the token total to the metrics file and **suggest opening a new session**
  that starts by reading the `-continue.md`.
