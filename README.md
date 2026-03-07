
# Goblin: Systemic Closure Illusion Gradient

Repo target: `nkllon/goblin`

This bundle contains:

- `goblin-ontology.ttl` — OWL ontology defining Goblin score (SCIG), problem classes, dimensions, and example domains.
- `goblin-shapes.ttl` — SHACL shapes constraining Goblin score usage.
- `goblin-guidance-ontology.ttl` — OWL module for normalized guidance requirements (topics/modality/provenance).
- `goblin-guidance-shapes.ttl` — SHACL module constraining guidance requirement instances.
- `goblin-map.dot` — Graphviz DOT file for a "Goblin map" of common domains.
- `goblin-agent-lim42.md` — lim42-ready agent spec for computing Goblin scores.
- `goblin-energy-gradient.md` — energy gradient interpretation with simple flow equations.
- Rendered `docs/goblin-map.svg` — quick visual of the Goblin map without requiring Graphviz (generate PNG locally with `dot -Tpng goblin-map.dot -o docs/goblin-map.png` if you prefer).

You can `pip install .` (or `pip install -e .` for development) to get the ontology, SHACL shapes, and validation helpers as a tiny Python package (`goblin-score`).
Then validate data against the bundled shapes (after installation):

```bash
python -m goblin.validate --data samples/goblin-sample.ttl
```

Guidance-governance module:

```bash
python tools/generate_guidance_governance_module.py
python -m goblin.validate --data samples/guidance-governance-sample.ttl --shapes goblin-guidance-shapes.ttl
python tools/report_guidance_conflicts.py --data samples/guidance-governance-sample.ttl --ontology goblin-guidance-ontology.ttl
```

## Meme / Usage

Because "SCIG" is overloaded in Google (subcutaneous immunoglobulin), we use the meme name:

> **Goblin score**

Example phrases:

- "What is the goblin score for that model?"
- "That architecture looks like a goblin, what do you think?"
- "Can you compute the goblin score for this solution?"

The Goblin score is defined in the ontology as `ui:goblinScore` and is an alias of `ui:SCIG_Score`.

## Next Steps

- Push this bundle into `nkllon/goblin` as initial commit.
- Wire `goblin-agent-lim42.md` into lim42 as a reusable agent profile.
- Render `goblin-map.dot` with Graphviz to produce a PNG/SVG for documentation. ✅

## Scoring workflow (lim42 example)

Use the existing lim42 agent prompt (`goblin-agent-lim42.md`) and weights to go from a system description to a JSON score.

**Example prompt input** (shortened):

> "A multi-tenant SaaS with asynchronous provisioning, eventual consistency across regions, and teams expecting deterministic dashboards. Observability is partial; on-call engineers rely on retries and manual overrides."

**Expected JSON output shape** (weights baked into the agent):

```json
{
  "goblin_score": 0.82,
  "dimensions": {
    "illusion_closure": 0.90,
    "distributed_state": 0.85,
    "async_nondeterminism": 0.80,
    "stakeholder_demand_for_determinism": 0.70,
    "observability_deficit": 0.60,
    "energy_gradient_misalignment": 0.95
  },
  "commentary": "Async provisioning and partial observability create large closure illusions; teams expect deterministic dashboards."
}
```

## Goblin map preview

- [SVG](docs/goblin-map.svg) — scalable version from the DOT source (`goblin-map.dot`).
- To produce a PNG locally (not checked into the repo), run `dot -Tpng goblin-map.dot -o docs/goblin-map.png`.
