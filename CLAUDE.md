# Refrain

Snapshot-keyed data gateway for AI agents. Spec-driven: specs change first, then tests, then code.

## Layout

- `specs/` — specs and test vectors. `specs/000-prd.md` is the private PRD (gitignored); every other spec is public.
- `tests/` — tests derived from specs.
- `src/` — implementation (Python 3.12+, uv).

## Workflow

For each spec, delegate in order. Each agent is limited to its own directories by `.claude/hooks/scope.py`.

1. `spec-writer` drafts or revises `specs/NNN-*.md` and its `.vectors.json`. The user approves it.
2. `test-author` writes failing tests from the spec, without reading `src/`.
3. `implementer` makes them pass, without touching `tests/` or `specs/`.
4. `spec-reviewer`, plus `security-reviewer` for anything touching keys, storage, principals or handles.

A disagreement between spec, test and code goes back to step 1, never patched in place.

## Rules

- Ponytail: `implementer` preloads `ponytail:ponytail`; `spec-reviewer` preloads `ponytail:ponytail-review`. The plugin is enabled for the project in `.claude/settings.json`; its SubagentStart hook also reaches every other agent, so `test-author` and `security-reviewer` carry explicit overrides. Spec, fail-closed and security rules beat ponytail minimalism.

- Fail closed: a wrong cached answer is worse than a miss.
- Requirement IDs (G-, FR-, CR-, NFR-) come from the PRD; cite them in specs and tests.
