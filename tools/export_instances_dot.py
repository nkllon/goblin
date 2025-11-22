#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import Dict, Tuple, Optional

from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef

try:
    import graphviz  # type: ignore
except Exception:
    graphviz = None  # Rendering optional; we'll still emit DOT


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_TTL = REPO_ROOT / "goblin-ontology.ttl"
OUT_DIR = REPO_ROOT / "docs"
DOT_PATH = OUT_DIR / "ttl-graph.dot"
SVG_PATH = OUT_DIR / "ttl-graph.svg"
PNG_PATH = OUT_DIR / "ttl-graph.png"

UI = Namespace("https://nkllon.com/ui#")


def score_to_color(score: Optional[float]) -> str:
    """Map 0..1 to green->yellow->red gradient hex color; None -> lightgray."""
    if score is None:
        return "#d3d3d3"
    s = max(0.0, min(1.0, float(score)))
    # simple red-green interpolation via HSV-ish bands
    # 0 -> green, 0.5 -> yellow, 1 -> red
    if s < 0.5:
        # green (0, 200) to yellow (255, 255)
        r = int(2 * s * 255)
        g = 255
        b = 0
    else:
        # yellow (255,255) to red (255,0)
        r = 255
        g = int((1 - 2 * (s - 0.5)) * 255)
        b = 0
    return f"#{r:02x}{g:02x}{b:02x}"


def load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(str(path), format="turtle")
    return g


def get_label(g: Graph, node: URIRef) -> str:
    label = g.value(node, RDFS.label)
    return str(label) if isinstance(label, Literal) else node.split("#")[-1]


def get_score(g: Graph, node: URIRef) -> Optional[float]:
    for prop in (UI.goblinScore, UI.SCIG_Score):
        val = g.value(node, prop)
        if isinstance(val, Literal):
            try:
                return float(val)
            except Exception:
                continue
    return None


def collect_nodes_and_edges(g: Graph) -> Tuple[Dict[str, Dict], Dict[Tuple[str, str], str]]:
    nodes: Dict[str, Dict] = {}
    edges: Dict[Tuple[str, str], str] = {}

    # Any subject that is a ui:ProblemClass or subclass instance
    problem_classes = set(g.subjects(RDF.type, UI.ProblemClass))
    # Include known subclasses instances
    for subclass in g.subjects(RDFS.subClassOf, UI.ProblemClass):
        for inst in g.subjects(RDF.type, subclass):
            problem_classes.add(inst)

    for n in problem_classes:
        nid = str(n)
        label = get_label(g, n)
        score = get_score(g, n)
        color = score_to_color(score)
        nodes[nid] = {
            "id": nid,
            "label": f"{label}\\nGoblin ~ {score:.2f}" if score is not None else label,
            "fillcolor": color,
        }

    # Edges based on optional properties
    edge_defs = {
        UI.influences: "influences",
        UI.overlapsWith: "overlaps",
        UI.dependsOn: "depends",
    }
    for subj in list(problem_classes):
        for prop, kind in edge_defs.items():
            for obj in g.objects(subj, prop):
                if str(subj) in nodes and str(obj) in nodes:
                    edges[(str(subj), str(obj))] = kind

    return nodes, edges


def emit_dot(nodes: Dict[str, Dict], edges: Dict[Tuple[str, str], str]) -> str:
    lines = []
    lines.append("digraph GoblinTTL {")
    lines.append("  rankdir=LR;")
    lines.append("  node [shape=box, style=rounded, fontname=\"Helvetica\"];")
    # Deterministic ordering: sort nodes by label then id
    for nid, meta in sorted(nodes.items(), key=lambda item: (item[1].get("label", ""), item[0])):
        label = meta["label"].replace("\"", "\\\"")
        color = meta["fillcolor"]
        lines.append(f"  \"{nid}\" [label=\"{label}\", style=\"filled,rounded\", fillcolor=\"{color}\"];")
    # Deterministic ordering: sort edges by (u, v, kind)
    for (u, v), kind in sorted(edges.items(), key=lambda item: (item[0][0], item[0][1], item[1])):
        style = "solid"
        if kind == "overlaps":
            style = "dashed"
        elif kind == "depends":
            style = "dotted"
        lines.append(f"  \"{u}\" -> \"{v}\" [label=\"{kind}\", style=\"{style}\"];")
    lines.append("}")
    return "\n".join(lines) + "\n"


def write_outputs(dot_text: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DOT_PATH.write_text(dot_text, encoding="utf-8")
    if graphviz is not None:
        try:
            src = graphviz.Source(dot_text, format="svg")
            src.render(filename=SVG_PATH.stem, directory=str(OUT_DIR), cleanup=True)
            src = graphviz.Source(dot_text, format="png")
            src.render(filename=PNG_PATH.stem, directory=str(OUT_DIR), cleanup=True)
        except Exception as e:
            sys.stderr.write(f"Graphviz render failed: {e}\n")


def main() -> int:
    if not DATA_TTL.exists():
        sys.stderr.write(f"Data TTL not found: {DATA_TTL}\n")
        return 2
    g = load_graph(DATA_TTL)
    nodes, edges = collect_nodes_and_edges(g)
    dot_text = emit_dot(nodes, edges)
    write_outputs(dot_text)
    sys.stdout.write(f"Wrote DOT: {DOT_PATH}\n")
    if SVG_PATH.exists():
        sys.stdout.write(f"Wrote SVG: {SVG_PATH}\n")
    if PNG_PATH.exists():
        sys.stdout.write(f"Wrote PNG: {PNG_PATH}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
