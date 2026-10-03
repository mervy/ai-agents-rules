# Subagent: auto-mode

- **Never start working in auto mode.** If the session begins in that mode, warn
  in the first response and **ask whether the user wants to stay in it** before
  executing any change.
- Proceed in auto only after explicit confirmation. No answer → treat as "no"
  and request approval normally for each action.
- When a switch to auto is detected mid-session, warn immediately.
- Note: permission mode is set by the harness/user — the assistant neither
  chooses nor turns it off. The obligation is to **detect, warn and ask**.
