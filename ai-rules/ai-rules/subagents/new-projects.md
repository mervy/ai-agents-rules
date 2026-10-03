# Subagent: new-projects

- Deliver folder structure, README, dependency/config file,
  `.env.example` and instructions to install, run and test.
- Born with the test suite, lint and CI pipeline (see `testing` subagent).
- Separate local and production configuration only by environment variables,
  ready for deploy when requested.
- Follow the language convention (e.g. `Cargo.lock` versioned in binaries,
  not in libraries).
