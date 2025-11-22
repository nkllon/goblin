# Contributing to Goblin (SCIG)

Thank you for helping improve the Goblin ontology and visualizations.

## Authoring rules
- Problem instances MUST use `ui:ProblemClass` (or a subclass) and SHOULD have a `ui:goblinScore` in [0,1].
- UI-closure problems MUST include `ui:goblinScore` (enforced by SHACL).
- Dimensions SHOULD include `ui:dimensionIndex` and `ui:energyRelevanceScore`.
- Use `ui:hasScoreComponent` to attach per-dimension components (`ui:ScoreComponent`) with `ui:componentValue` in [0,1].
- Use `ui:WeightAssignment` with `ui:forDimension` and `ui:hasWeight` for weight vectors. Prefer one canonical assignment (e.g. `ui:DefaultWeights`).
- Optional relations between problem classes:
  - `ui:influences` (directed)
  - `ui:overlapsWith` (symmetric)
  - `ui:dependsOn` (directed, transitive)
- Qualitative tiering is optional via `ui:hasTier` with values `ui:High`, `ui:Medium`, `ui:Low`.

## Validation
All changes are checked in CI via SHACL (pySHACL). Pushes/PRs must pass.

## Visualization outputs
The pipeline generates:
- `docs/ttl-graph.svg|png` — TTL-derived static graph (score-colored)
- `docs/goblin.json` — JSON for the interactive graph
- `docs/index.html` — interactive graph (bundled TS/D3)
- `docs/kg.html` — KG viewer (WebVOWL)

## Contribution workflow
1. Fork and branch from `main`.
2. Update `goblin-ontology.ttl` (and `goblin-shapes.ttl` if adding constraints).
3. Run local checks if possible (`tools/validate_shapes.py`).
4. Open a PR with a summary of ontology changes.

## Versioning
We tag semantic versions for ontology releases and maintain a `CHANGELOG.md`.
