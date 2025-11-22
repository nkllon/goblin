
# Goblin: Systemic Closure Illusion Gradient

Repo target: `nkllon/goblin`

This bundle contains:

- `goblin-ontology.ttl` — OWL ontology defining Goblin score (SCIG), problem classes, dimensions, and example domains.
- `goblin-shapes.ttl` — SHACL shapes constraining Goblin score usage.
- `goblin-map.dot` — Graphviz DOT file for a "Goblin map" of common domains.
- `goblin-agent-lim42.md` — lim42-ready agent spec for computing Goblin scores.
- `goblin-energy-gradient.md` — energy gradient interpretation with simple flow equations.

## Quick links

- Goblin map (rendered): see `docs/goblin-map.svg` and `docs/goblin-map.png`
- Ontology visualization (WebVOWL): open `docs/kg.html`

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

## CI parity (local)

You can reproduce GitHub Actions locally in two ways:

1) Docker Compose (dev-friendly)

- Build/run the same steps as CI:

```
make ci-docker
```

- Or individual steps:

```
docker compose run --rm python-validate
docker compose run --rm python-export
docker compose run --rm dot-check
docker compose run --rm js-package
docker compose run --rm web-build
```

2) act (exact workflow runner)

- Install: `brew install act` (macOS)
- Run specific jobs matching `.github/workflows/*.yml`:

```
act pull_request -j validate-and-build
act pull_request -j js
act pull_request -j python-validate
act pull_request -j dot-check
act pull_request -j docs-link
```

## Pre-commit (mirrors CI)

Install pre-commit and enable hooks:

```
python3 -m pip install --user pre-commit
pre-commit install
pre-commit install --hook-type pre-push
```

Run all hooks (heavy, uses Docker to ensure parity):

```
pre-commit run --all-files --show-diff-on-failure
pre-commit run --all-files --hook-stage push --show-diff-on-failure
```

