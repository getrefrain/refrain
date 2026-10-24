# NNN — [FEATURE NAME]

Status: DRAFT · Spec version: `[short id, e.g. k1]` · Implements: [PRD IDs: FR-, CR-, NFR-, G-] · Vectors: [`vectors.json`](vectors.json)

**Feature Branch**: `[###-feature-name]` · **Created**: [DATE] · **Input**: "$ARGUMENTS"

<!--
  Refrain spec template (overrides Spec Kit's default). Rules:
  - This file says WHAT and WHY. Language, libraries, module layout and bindings go in plan.md.
  - Requirement IDs come from the PRD (.specify/memory/prd.md, private). Never copy business strategy here; specs are public.
  - Fail closed (Constitution Article II): when a rule is uncertain, pick the behavior that causes a miss or an error.
  - Mark unresolved points with [NEEDS CLARIFICATION: question] and list them under Open questions.
-->

## Purpose

[What this does, for whom, and the one-sentence correctness guarantee.]

## Safety rule

[The asymmetry that resolves ambiguity, e.g. "a false hit is a wrong answer; a miss is only a miss". Delete if none.]

## User Scenarios & Testing *(mandatory)*

<!--
  Prioritized journeys (P1 first), each independently testable, with Given/When/Then scenarios.
  For a pure-function contract, each scenario can name the vector category that covers it.
-->

### Scenario 1 - [Brief title] (Priority: P1)

[Plain-language journey.]

**Acceptance**:

1. **Given** [state], **When** [action], **Then** [outcome] — vectors: `[category]`

### Edge Cases

- [Boundary or error condition and the fail-closed outcome]

### Testing *(mandatory)*

TDD is requested for this spec (Constitution Article I). Every vector in `vectors.json` becomes a test, written by `test-author` before implementation, and must fail first. Vectors marked `must` fail the build; informational vectors record outcomes only.

## Interface

[Language-neutral contract: inputs, outputs, result variants. Bindings for a specific language go in plan.md.]

## Outcomes

[Every result status and reason code, and what the caller receives for each (Constitution Article III: exactly one named status).]

## Rules

[Normative behavior, numbered so tests and reviews can cite them.]

## Success Criteria *(mandatory)*

- **SC-001**: [Measurable, technology-agnostic outcome. Performance or savings claims say how they are measured (Article XIII).]

## Test vectors

[`vectors.json`](vectors.json) contains: [vector kinds, their strictness, and how a test consumes each].

## Out of scope

- [What this spec deliberately does not cover, and which spec does]

## Open questions

- [Questions that need the project owner's decision. Do not decide product questions in the spec.]
