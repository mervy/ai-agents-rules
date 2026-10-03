# Subagent: operations

- **Standardised logs and errors**: single format in the project (preferably structured),
  with level and context, **no sensitive data** (password, token, document, card).
  Error shown to the user is generic; detail stays in the log.
- **Fail early on startup**: validate all required environment variables on boot
  and abort with a clear message if any is missing.
- **Health check**: web service exposes a simple route (e.g. `/health`) for deploy.
- **Performance budget**: each project defines limits in the README (max response time,
  max image/page size) and the change must not exceed them.
