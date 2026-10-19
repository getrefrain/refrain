# Specs

Specs change first, then tests, then code. See the [constitution](../.specify/memory/constitution.md) for the rules every spec must follow and `CLAUDE.md` for the agent workflow. This index is maintained by the `product-owner` agent; only the project owner moves a spec to APPROVED or IMPLEMENTED.

## Lifecycle

| Status | Meaning | Who moves it |
|--------|---------|--------------|
| DRAFT | Being written or revised | spec-writer (index row kept by product-owner) |
| APPROVED | Frozen for implementation; tests may be written | Project owner |
| IMPLEMENTED | Tests pass in CI and reviews are clean | Project owner, after spec-reviewer |
| SUPERSEDED | Replaced by a newer version; kept for history | spec-writer |

Changing an APPROVED or IMPLEMENTED spec bumps its version and sends it back to DRAFT.

## Index

| Spec | Version | Status | Requirements | Tests |
|------|---------|--------|--------------|-------|
| Product requirements (`.specify/memory/prd.md`) | — | Private (not in repo) | Defines G-, FR-, CR-, NFR- | — |
| [001 Canonical key](001-canonical-key/spec.md) | k1 | DRAFT | FR-2, FR-5, CR-6, CR-11, FR-12 (read-only part) | — |
| 002 Outcome contract | — | Planned | CR-1 to CR-9, FR-8 | — |
| 003 Replay and report | — | Planned | FR-1, FR-7 | — |
| 004 Freshness | — | Planned | FR-3, CR-1, CR-7 | — |
| 005 Bucket layout and lifecycle | — | Planned | FR-4, FR-13, NFR-2, NFR-5 | — |
| 006 MCP tools and gateway adapters | — | Planned | FR-6, FR-10, NFR-8 (LiteLLM adapter), FR-20 (schema tools) | — |
| 007 Query policy and sensitive data | — | Planned | FR-12, FR-18, CR-10, CR-11, CR-13, FR-20 (policy filtering) | — |
| 008 Observability and audit | — | Planned | FR-14, FR-15, FR-16 | — |
| 009 Release and distribution | — | Planned | REL-1 to REL-10, FR-11 (`examples/litellm/`) | — |
| 010 Execution backends | — | Planned | FR-17, CR-12 | — |
| 011 Console and versioned policy | — | Planned (v0.2) | FR-19 | — |
| 012 Recipes and task suite | — | Planned | FR-9, CR-2 | — |
