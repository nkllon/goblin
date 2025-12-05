from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pyshacl import validate as shacl_validate
from rdflib import Graph

from .resources import resource_path


@dataclass
class ValidationResult:
    conforms: bool
    results_text: str
    data_source: Path
    shapes_source: Path


def _load_graph(path: Path) -> Graph:
    graph = Graph()
    graph.parse(str(path), format="turtle")
    return graph


def validate_graph(
    data_path: Optional[Path] = None,
    shapes_path: Optional[Path] = None,
) -> ValidationResult:
    """Run SHACL validation against the Goblin shapes."""

    if data_path is None:
        with resource_path("goblin-ontology.ttl") as default_data:
            data_graph = _load_graph(default_data)
            data_source = default_data
    else:
        data_graph = _load_graph(data_path)
        data_source = data_path

    if shapes_path is None:
        with resource_path("goblin-shapes.ttl") as default_shapes:
            shapes_graph = _load_graph(default_shapes)
            shapes_source = default_shapes
    else:
        shapes_graph = _load_graph(shapes_path)
        shapes_source = shapes_path

    conforms, _, results_text = shacl_validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        inference="rdfs",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
    )

    return ValidationResult(bool(conforms), results_text, Path(data_source), Path(shapes_source))


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Validate Goblin ontology data with SHACL shapes.")
    parser.add_argument("--data", type=Path, help="Path to a Turtle data file to validate.")
    parser.add_argument("--shapes", type=Path, help="Path to a Turtle SHACL shapes file.")
    args = parser.parse_args()

    result = validate_graph(args.data, args.shapes)

    print(result.results_text.strip() or "SHACL validation produced no messages.")
    return 0 if result.conforms else 1


if __name__ == "__main__":
    raise SystemExit(main())
