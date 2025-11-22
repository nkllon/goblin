
# Goblin: Systemic Closure Illusion Gradient

Repo target: `nkllon/goblin`

This bundle contains:

- `goblin-ontology.ttl` — OWL ontology defining Goblin score (SCIG), problem classes, dimensions, and example domains.
- `goblin-shapes.ttl` — SHACL shapes constraining Goblin score usage.
- `goblin-map.dot` — Graphviz DOT file for a "Goblin map" of common domains.
- `goblin-agent-lim42.md` — lim42-ready agent spec for computing Goblin scores.
- `goblin-energy-gradient.md` — energy gradient interpretation with simple flow equations.

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
- Render `goblin-map.dot` with Graphviz to produce a PNG/SVG for documentation.
