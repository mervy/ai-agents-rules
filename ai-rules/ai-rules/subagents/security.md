# Subagent: security

- **OWASP checklist** on every change that touches external input:
  - validate and normalise every input (type, size, format) on the server;
  - injection protection: SQL with prepared statements and NoSQL without building
    filters from user objects (e.g. MongoDB `$` operators);
  - escape output in templates (XSS); never disable default escaping without reason;
  - uploads with size limit, allow-list of types and server-generated name;
  - authentication/authorization checked on the server for every protected route;
  - CSRF on session forms; security headers; rate limit on login.
- **Least privilege**: the agent never receives or uses production credentials,
  only development ones. Application DB user without DDL permission in production.
