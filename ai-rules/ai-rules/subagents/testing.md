# Subagent: testing

The agent's code is not read line by line: confidence comes from the constraints it
must pass. These rules are therefore **blocking**.

## Rules
- **Never delete test files** (`tests/`) without authorization.
- Before modifying code that already has tests, run the suite and confirm it is green.
- When removing a class/method, check whether tests cover it before deleting.
- **Do not deliver code without tests.** Bug fixes start with a test that reproduces the bug.
- **Forbidden to skip or weaken tests** to make the suite pass: no `skip`/`ignore`/`only`,
  deleting assertions, loosening comparisons, increasing tolerance or mocking the
  code under test itself. Wrong test? Explain and ask before changing.

## Test types
- **Unit** for every business rule and function with logic.
- **Gherkin/BDD** (`Given / When / Then`) for user-visible behaviour,
  written from the requirements (Cucumber, Behat, behave or equivalent).
- **Integration** for database, queues, external APIs and file system;
  **end-to-end** for the main flows.
- **Property-based** for pure functions with wide input
  (parsers, slug, calculations): proptest, fast-check, Hypothesis, jqwik.
- **Mutation**: run the language's tool (Stryker, Infection, cargo-mutants,
  mutmut, PIT or equivalent) on the changed code. Surviving mutant = missing test:
  eliminate it or justify in the report.
- **Contract**: APIs with a contract (OpenAPI or JSON Schema as source of truth)
  have tests that validate requests and responses against it.
- **Architecture**: limits such as "controller does not access the DB directly"
  verified by test (dependency-cruiser, deptrac, ArchUnit or equivalent) when the
  project defines layers.

## Metrics
- **Minimum 80% coverage** of lines and branches, and existing coverage **never drops**.
- Lint, formatting and type checking with zero warnings.

## QA procedure (fixed order; any failure blocks delivery)
1. Formatting
2. Lint and type checking
3. Unit and property tests
4. Integration, contract, architecture and Gherkin tests
5. End-to-end tests
6. Coverage (≥ 80%, no drop)
7. Mutation tests on the changed code
8. Dependency audit (`npm audit`, `composer audit`, `cargo audit`,
   `pip-audit`, `govulncheck` or equivalent)
9. Secret scanning (e.g. `gitleaks`)

At the end, report each step: command, result and what could not be executed (and why).
A step that does not apply to the project is marked "not applicable", never omitted.

## CI
- The pipeline runs the same procedure and **blocks the merge** if any step fails.
