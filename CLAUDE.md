# Refrain

Snapshot-keyed data gateway for AI agents: the data plane between agents and the warehouse.

@CONSTITUTION.md

## Layout

- `CONSTITUTION.md` — rules that override everything else. Only the project owner edits it.
- `specs/` — specs and test vectors. `specs/000-prd.md` is the private PRD (gitignored); `specs/README.md` is the index. Every other spec is public.
- `tests/` — tests derived from specs.
- `src/` — implementation (Python 3.12+, uv).
- `docs/`, `examples/`, `.github/` — docs and site, integration examples, CI/CD.

## Workflow

Each agent can only write its own paths, enforced by `.claude/hooks/scope.py`.

0. `product-owner` turns a need into requirements in the PRD and an index row. The project owner approves.
1. `spec-writer` writes `specs/NNN-*.md` and its `.vectors.json`. The project owner approves it (status APPROVED).
2. `test-author` writes failing tests from the spec, without reading `src/`.
3. `implementer` makes them pass, without touching `tests/` or `specs/`.
4. `spec-reviewer`, plus `security-reviewer` for anything touching keys, storage, principals, handles, policy or sensitive data.

A conflict goes to the owner of the higher document (constitution → PRD → spec → tests → code), never patched in place.

Alongside, not in sequence:

- `release-engineer` owns `.github/`, packaging, container, registry config and `examples/`.
- `docs-writer` owns `docs/`, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`; it cannot read the private PRD.

| Agent | Writes | Ponytail |
|-------|--------|----------|
| product-owner | `specs/000-prd.md`, `specs/README.md` | — |
| spec-writer | `specs/` except PRD and index | — |
| test-author | `tests/` (reads only `specs/`, `tests/`) | overridden: every vector is required |
| implementer | `src/`, `pyproject.toml`, `uv.lock` | preloads `ponytail:ponytail` |
| spec-reviewer | nothing | preloads `ponytail:ponytail-review` |
| security-reviewer | nothing | overridden: never trims security |
| release-engineer | `.github/`, `Dockerfile`, packaging, `CHANGELOG.md`, `server.json`, `examples/` | preloads `ponytail:ponytail` |
| docs-writer | `docs/`, `README.md`, `CONTRIBUTING.md`, `SECURITY.md` | — |

The ponytail plugin is enabled for the project in `.claude/settings.json`; its SubagentStart hook reaches every agent. Constitution, specs, fail-closed and security rules beat ponytail minimalism (Article XI).
