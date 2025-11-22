#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import Tuple

from rdflib import Graph

try:
    from pyshacl import validate
except ImportError as e:
    sys.stderr.write("pyshacl is required. Install with: pip install pyshacl rdflib\n")
    raise


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_TTL = REPO_ROOT / "goblin-ontology.ttl"
SHAPES_TTL = REPO_ROOT / "goblin-shapes.ttl"


def load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(str(path), format="turtle")
    return g


def run_validation(data_graph: Graph, shacl_graph: Graph) -> Tuple[bool, Graph, str]:
    conforms, results_graph, results_text = validate(
        data_graph=data_graph,
        shacl_graph=shacl_graph,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        inference="rdfs",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
    )
    return bool(conforms), results_graph, results_text


def main() -> int:
    if not DATA_TTL.exists():
        sys.stderr.write(f"Data TTL not found: {DATA_TTL}\n")
        return 2
    if not SHAPES_TTL.exists():
        sys.stderr.write(f"Shapes TTL not found: {SHAPES_TTL}\n")
        return 2

    data_graph = load_graph(DATA_TTL)
    shapes_graph = load_graph(SHAPES_TTL)
    conforms, _, results_text = run_validation(data_graph, shapes_graph)

    if not conforms:
        sys.stderr.write("SHACL validation failed:\n")
        sys.stderr.write(results_text)
        return 1
    else:
        sys.stdout.write("SHACL validation passed.\n")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
