# Guidance Model Pathology Note (2026-03-07)

## Context

Observed while tightening agent-governance gates in `eudorus`, but applicable to Goblin-style guidance systems.

## Pathology

A recurrent failure mode appears when guidance is partly model-driven and partly hand-maintained prose:

1. Policy clauses are duplicated across multiple artifacts.
2. Semantic coupling is implicit (inferred from wording), not explicit in a canonical model.
3. Projection/generation covers only a subset of guidance surfaces.
4. CI validates syntax/format but not cross-artifact semantic overlap.

This yields "goblin-class" drift:
- overlapping or contradictory norms,
- frequent merge conflicts in high-churn policy files,
- partial refactors leaving dead or inconsistent logic paths,
- policy intent ambiguity during enforcement.

## Triggering Example

- Introduced stricter ontology-exemption governance and typo-only semantics.
- Concurrent branch evolution changed adjacent exemption/authenticity policy text.
- A code path introduced richer change-status parsing but still used synthetic status in enforcement.
- Result: merge conflict + semantic ambiguity + inconsistent enforcement intent.

## Hypothesis

The root issue is under-modeled guidance dimensions, not just bad merge hygiene.

Missing/weak dimensions usually include:
- topic (normalized policy domain),
- modality (`must`, `must_not`, `should`, `should_not`),
- scope/target surface,
- precedence/authority,
- enforcement level,
- provenance and ownership.

## Recommended Controls

1. Maintain a canonical normalized requirement model for guidance artifacts.
2. Project host-specific guidance from model where possible.
3. Add drift gates:
   - fail on conflict-risk growth relative to base,
   - fail on mixed-modality drift for key topics.
4. Require explicit concept IDs for policy clauses to reduce inferred coupling.

## Follow-up Work for Goblin

- Add a first-class guidance ontology/schema for policy dimensions.
- Add deterministic extraction from markdown/yaml guidance into that schema.
- Add CI checks for topic-level modality conflicts and precedence violations.
- Build a dashboard/report for conflict hotspots by topic and source file.
