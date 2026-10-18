# Refrain

Snapshot-keyed data gateway for AI agents: the data plane between agents and the warehouse.

@.specify/memory/constitution.md

## Layout

- `.specify/memory/constitution.md` — the constitution: rules that override everything else. Only the project owner edits it.
- `specs/` — one directory per spec (`specs/NNN-name/`: `spec.md`, `plan.md`, `tasks.md`, `vectors.json`, plus whatever `speckit-plan` adds). `specs/000-prd.md` is the private PRD (gitignored); `specs/README.md` is the index. Every other spec is public.
- `.specify/` — GitHub Spec Kit (constitution, scripts, templates, workflow). Refrain's templates live in `.specify/templates/overrides/`.
- `tests/` — tests derived from specs.
- `src/` — implementation (Python 3.12+, uv).
- `docs/`, `examples/`, `.github/` — docs and site, integration examples, CI/CD.

## Workflow

Spec Kit (`/speckit-*` skills) drives the steps; each step runs inside the agent that owns its files. Each agent can only write its own paths, enforced by `.claude/hooks/scope.py`. Don't run `/speckit-implement` in the main session: it would write tests and code together.

0. `product-owner` turns a need into requirements in the PRD and an index row. The project owner approves.
1. `spec-writer` runs `speckit-specify` → `speckit-clarify` → `speckit-plan` → `speckit-tasks` → `speckit-analyze`, producing `spec.md`, `plan.md`, `tasks.md` and `vectors.json`. The project owner approves it (status APPROVED).
2. `test-author` does the test tasks in `tasks.md`: failing tests from the spec, without reading `src/`.
3. `implementer` runs `speckit-implement` on the remaining tasks and makes the tests pass, without touching `tests/` or `specs/` (except checking off `tasks.md`).
4. `spec-reviewer` (includes `speckit-analyze`); open work goes back to `spec-writer`, which runs `speckit-converge` to append it to `tasks.md`. Plus `security-reviewer` for anything touching keys, storage, principals, handles, policy or sensitive data.

A conflict goes to the owner of the higher document (constitution → PRD → spec → tests → code), never patched in place.

`/speckit-constitution` is the project owner's alone. No agent's scope includes `.specify/memory/`.

Alongside, not in sequence:

- `release-engineer` owns `.github/`, packaging, container, registry config and `examples/`.
- `docs-writer` owns `docs/`, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`; it cannot read the private PRD.

| Agent | Writes | Ponytail |
|-------|--------|----------|
| product-owner | `specs/000-prd.md`, `specs/README.md` | — |
| spec-writer | `specs/` except PRD and index; `.specify/feature.json` | — |
| test-author | `tests/`, `specs/*/tasks.md` (reads only `specs/`, `tests/`) | overridden: every vector is required |
| implementer | `src/`, `pyproject.toml`, `uv.lock`, `specs/*/tasks.md` | preloads `ponytail:ponytail` |
| spec-reviewer | nothing | preloads `ponytail:ponytail-review` |
| security-reviewer | nothing | overridden: never trims security |
| release-engineer | `.github/`, `Dockerfile`, packaging, `CHANGELOG.md`, `server.json`, `examples/` | preloads `ponytail:ponytail` |
| docs-writer | `docs/`, `README.md`, `CONTRIBUTING.md`, `SECURITY.md` | — |

The ponytail plugin is enabled for the project in `.claude/settings.json`; its SubagentStart hook reaches every agent. Constitution, specs, fail-closed and security rules beat ponytail minimalism (Article XI).
