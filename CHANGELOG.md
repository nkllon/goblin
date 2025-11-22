# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-11-22
### Added
- CI with SHACL validation and artifact publishing to GitHub Pages.
- TTL-derived DOT/SVG/PNG export and interactive TS/D3 graph (docs/).
- `CONTRIBUTING.md` with authoring rules.
- Initial KG viewer page (`docs/kg.html`).

### Ontology
- Core ontology defining Goblin score and example domains (existing).

### Notes
- Semantic versioning will track ontology schema changes going forward.

## Unreleased
### Fixed
- SHACL failures due to `ui:forDimension` declaring a dual `rdfs:domain` of both `ui:ScoreComponent` and `ui:WeightAssignment`, which inferred nodes into both classes. Removed the domain to avoid unintended inference; SHACL now passes.
- Regenerated `docs/goblin-map.svg` and `docs/goblin-map.png` from `goblin-map.dot` to match CI dot-check.
### JS
- Corrected `rdf-validate-shacl` dependency to `^0.6.5` and adjusted TS config/imports to pass typecheck and build under Node 20.
