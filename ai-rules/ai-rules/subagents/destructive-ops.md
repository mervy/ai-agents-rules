# Subagent: destructive-ops

Any operation that:
- Deletes files (`rm`, `unlink`, `rmdir -r`)
- Overwrites existing content irreversibly
- Terminates processes (`kill`, `pkill`)
- Changes permissions broadly (`chmod 777`, `chown -R`)
- Publishes something externally (deploy, gist, post, send to external service)

…requires explicit user confirmation before execution.
