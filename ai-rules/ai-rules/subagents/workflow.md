# Subagent: workflow

## Scope control
- At the start of a task, define (or ask for) the closed list of files and folders
  that may be changed. Need to touch something outside? Ask first.
- If a requirement conflicts with a global rule, stop and ask instead of deciding alone.

## TDD
- Write the failing test first, confirm the failure, implement until it passes,
  then refactor with a green suite.

## Small changes
- One PR = one responsibility, ideally ≤ ~400 changed lines (excluding lockfiles
  and generated files). Larger → split.

## ADRs
- Relevant technical decisions (library, architecture, data format, approach change)
  become a short record in `docs/adr/NNNN-title.md`:
  context, decision, discarded alternatives, consequences.

## Second-agent review
- For non-trivial changes, request review from a different agent (another session
  or tool) that receives **only the diff and the requirements**, not the conversation
  that produced the code.

## Definition of done
A delivery is ready only when the agent can check, with evidence, every item:
- [ ] Requirement met, inside the agreed scope
- [ ] New tests covering the change (including error and edge cases)
- [ ] Full QA procedure executed end-to-end with no failures
- [ ] Imports, declared dependencies, package names and versions checked
- [ ] No secrets in the diff
- [ ] README / ADR / `.env.example` updated when the change requires it
- [ ] Final report: what changed, how to test, what was and was **not** verified
