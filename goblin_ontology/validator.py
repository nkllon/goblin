from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from rdflib import Graph
from pyshacl import validate as shacl_validate


@dataclass(frozen=True)
class ValidationResult:
    conforms: bool
    report_text: str
    report_graph: Graph


def _guess_format_from_suffix(path: Path) -> Optional[str]:
    name = path.name.lower()
    if name.endswith(".ttl"):
        return "turtle"
    if name.endswith(".nt"):
        return "nt"
    if name.endswith(".nq"):
        return "nquads"
    if name.endswith(".trig"):
        return "trig"
    if name.endswith(".json") or name.endswith(".jsonld") or name.endswith(".json-ld"):
        return "json-ld"
    if name.endswith(".rdf") or name.endswith(".xml"):
        return "xml"
    return None


def load_graph(source_path: Path, rdf_format: Optional[str] = None) -> Graph:
    graph = Graph()
    fmt = rdf_format or _guess_format_from_suffix(source_path)
    graph.parse(source=str(source_path), format=fmt)
    return graph


def validate(
    data_graph_path: Path | str,
    shapes_graph_path: Path | str,
    data_format: Optional[str] = None,
    shapes_format: Optional[str] = None,
    inference: str = "rdfs",
    advanced: bool = True,
) -> ValidationResult:
    """
    Validate an RDF data graph against SHACL shapes.
    """
    data_path = Path(data_graph_path)
    shapes_path = Path(shapes_graph_path)

    data_graph = load_graph(data_path, data_format)
    shapes_graph = load_graph(shapes_path, shapes_format)

    conforms, report_graph, report_text = shacl_validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        inference=inference,
        advanced=advanced,
        serialize_report_graph=False,
    )

    return ValidationResult(
        conforms=bool(conforms), report_text=str(report_text), report_graph=report_graph
    )
