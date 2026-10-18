# Specs

Specs change first, then tests, then code. See `CLAUDE.md` for the agent workflow.

## Lifecycle

| Status | Meaning | Who moves it |
|--------|---------|--------------|
| DRAFT | Being written or revised | spec-writer |
| APPROVED | Frozen for implementation; tests may be written | Project owner |
| IMPLEMENTED | Tests pass in CI and reviews are clean | Project owner, after spec-reviewer |
| SUPERSEDED | Replaced by a newer version; kept for history | spec-writer |

Changing an APPROVED or IMPLEMENTED spec bumps its version and sends it back to DRAFT.

## Index

| Spec | Version | Status | Requirements | Tests |
|------|---------|--------|--------------|-------|
| 000 Product requirements | — | Private (not in repo) | Defines G-, FR-, CR-, NFR- | — |
| [001 Canonical key](001-canonical-key.md) | k1 | DRAFT | FR-2, FR-5, CR-6 | — |
| 002 Outcome contract | — | Planned | CR-1 to CR-9, FR-8 | — |
| 003 Replay and report | — | Planned | FR-1, FR-7 | — |
| 004 Freshness | — | Planned | FR-3, CR-1, CR-7 | — |
| 005 Bucket layout | — | Planned | FR-4, NFR-2, NFR-5 | — |
| 006 MCP tools | — | Planned | FR-6, FR-10 | — |
