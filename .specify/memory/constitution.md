# Refrain Constitution

The rules every spec, test, line of code, doc and agent in this repo must follow. Specs decide *what* Refrain does; this document decides what it may never do.

## Precedence

Constitution → product requirements → specs → tests → code. When two disagree, the higher one wins and the lower one is fixed through its owner. Nothing is patched in place to make a conflict go away.

## Core Principles

### I. Spec first

Behavior changes start in a spec with test vectors. Tests are written from the spec, code is written to the tests. Code without a spec is a prototype and is not merged.

### II. Fail closed

A wrong answer is worse than a miss. Whatever Refrain cannot verify — an unparseable query, an unknown function, an unreadable policy, an unreachable catalog, an audit store that won't write — becomes an error, or an uncached pass-through when running it is provably safe. Never a guess.

### III. Never wrong, never vague

Every response carries exactly one named status. Empty, partial, stale, withheld and failed results say so explicitly. A bare "ok" that hides any of them is a bug.

### IV. Stateless

All durable state lives in the customer's bucket. Configuration is files, environment or a versioned object in that bucket. Refrain never requires a database, scheduler or any other service that holds state; any instance can serve any request and scaling to zero loses nothing.

### V. The customer's data stays in the customer's cloud

No result data, SQL, sampled values or identities leave it. No telemetry or usage reporting is on by default. Logs, traces and metrics never contain data values unless the operator opts in.

### VI. No model in the key or the answer path

Cache keys and served answers are computed deterministically. Models may rank hints, suggest labels or analyze logs offline, where a mistake costs a miss or a turn, never a wrong answer.

### VII. Least privilege, defense in depth

Refrain runs with read-only credentials and enforces read-only itself. Its policy adds to warehouse and catalog permissions; it never replaces them and is never described as if it did. Sensitive values stay out of an agent's context unless policy explicitly allows them.

### VIII. Every action is audited

Each request, denial, erasure and policy change produces an immutable audit record. If the record cannot be written, the action does not happen.

### IX. Neutral and open

Refrain works with any MCP client, behind any AI gateway or none, and its storage formats are published specs with test vectors that other tools can implement. Integrations are adapters, never dependencies.

### X. A data plane, not an LLM gateway

Refrain decides what data work runs, what is reused and what it cost. LLM routing, model keys, prompt caching and LLM guardrails belong to other tools, which Refrain integrates with rather than rebuilds.

### XI. Reuse before build; simplest correct thing

Prefer an existing library, standard library or platform feature over new code, and the smallest change that meets the spec. Simplicity never removes validation, fail-closed handling, auditing or security.

### XII. Open core with a clear line

The MIT core is complete for one team running Refrain on its own. Paid features are about many teams and hosted operation (shared cache policy, SSO and roles, compliance exports, managed control plane), never about making the core safe or correct.

### XIII. Evidence over assertion

Performance, savings and accuracy claims are measured, and the measurement is reproducible. Proposals and estimates are labeled as such until measured.

## Governance

- This file lives at `.specify/memory/constitution.md`, where GitHub Spec Kit reads it. Amend it with `/speckit-constitution`.
- Only the project owner amends this document. Agents may propose amendments in their reports; no agent can write this file.
- An amendment states the article changed, the reason, and the specs and code it affects.
- Versioning is semantic. MAJOR: an article removed or redefined incompatibly. MINOR: an article added or materially expanded. PATCH: wording, clarification or formatting with no change in meaning.
- Every review checks changes against these articles and cites the article number for any violation.

**Version**: 1.0.0 | **Ratified**: 2026-10-18 | **Last Amended**: 2026-10-18
