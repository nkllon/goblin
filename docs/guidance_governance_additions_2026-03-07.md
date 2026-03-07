# Guidance Governance Additions (2026-03-07)

Based on real failures encountered in cross-repo agent guidance work, Goblin now includes baseline support for guidance-governance modeling and drift checks:

1. RDFLib-generated ontology module: `goblin-guidance-ontology.ttl`
2. RDFLib-generated SHACL module: `goblin-guidance-shapes.ttl`
3. Sample governed data: `samples/guidance-governance-sample.ttl`
4. Conflict drift report tool: `tools/report_guidance_conflicts.py`
5. CI enforcement for generation, SHACL validation, and conflict gate.

## Why this was added

- We observed policy drift when guidance was split across model-driven and hand-maintained sources.
- We observed semantic overlap and conflicting clauses hidden by prose.
- We observed conflict-prone merges in high-churn policy files.

## Immediate next candidates

- Add explicit precedence/authority modeling (for conflict resolution beyond polarity checks).
- Add owner metadata for each requirement topic and enforcement policy.
- Add baseline-vs-head conflict growth checks against repository history for real guidance datasets.
