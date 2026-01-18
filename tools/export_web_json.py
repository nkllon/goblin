#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_TTL = REPO_ROOT / "goblin-ontology.ttl"
OUT_DIR = REPO_ROOT / "docs"
JSON_PATH = OUT_DIR / "goblin.json"

UI = Namespace("https://nkllon.com/ui#")
STAKE = Namespace("https://nkllon.com/stake#")


def load_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(str(path), format="turtle")
    return g


def get_label(g: Graph, node: URIRef) -> str:
    label = g.value(node, RDFS.label)
    return str(label) if isinstance(label, Literal) else node.split("#")[-1]


def get_float(g: Graph, node: URIRef, prop: URIRef) -> Optional[float]:
    val = g.value(node, prop)
    if isinstance(val, Literal):
        try:
            return float(val)
        except Exception:
            return None
    return None


def collect(g: Graph) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    dimensions: List[Dict[str, Any]] = []
    weights: List[Dict[str, Any]] = []
    stakeholders: List[Dict[str, Any]] = []

    # Problem classes (nodes)
    problem_classes = set(g.subjects(RDF.type, UI.ProblemClass))
    for subclass in g.subjects(RDFS.subClassOf, UI.ProblemClass):
        for inst in g.subjects(RDF.type, subclass):
            problem_classes.add(inst)

    for n in sorted(problem_classes, key=lambda x: str(x)):
        nid = str(n)
        nodes.append({
            "id": nid,
            "label": get_label(g, n),
            "score": get_float(g, n, UI.goblinScore),
            "tier": str(g.value(n, UI.hasTier)) if g.value(n, UI.hasTier) else None,
            "type": "ProblemClass",
        })

    # Relations (edges)
    for s in sorted(list(problem_classes), key=lambda x: str(x)):
        for prop, kind in ((UI.influences, "influences"), (UI.overlapsWith, "overlapsWith"), (UI.dependsOn, "dependsOn")):
            for o in g.objects(s, prop):
                if (str(s) in {n["id"] for n in nodes}) and (str(o) in {n["id"] for n in nodes}):
                    edges.append({"source": str(s), "target": str(o), "type": kind})

    # Dimensions
    for d in sorted(g.subjects(RDF.type, UI.Dimension), key=lambda x: str(x)):
        did = str(d)
        dimensions.append({
            "id": did,
            "label": get_label(g, d),
            "index": get_float(g, d, UI.dimensionIndex),
            "energyRelevance": get_float(g, d, UI.energyRelevanceScore),
        })

    # Weights
    for w in sorted(g.subjects(RDF.type, UI.WeightAssignment), key=lambda x: str(x)):
        for dim in sorted(g.objects(w, UI.forDimension), key=lambda x: str(x)):
            weight_val = get_float(g, w, UI.hasWeight)
            if weight_val is not None:
                weights.append({
                    "dimension": str(dim),
                    "weight": weight_val,
                    "assignment": str(w),
                })

    # Stakeholders
    for role in sorted(g.subjects(RDF.type, STAKE.StakeholderRole), key=lambda x: str(x)):
        cares = sorted([str(d) for d in g.objects(role, STAKE.caresAbout)])
        stakeholders.append({
            "id": str(role),
            "label": get_label(g, role),
            "caresAbout": cares,
        })

    # Deterministic ordering for all lists
    nodes.sort(key=lambda n: (n["label"], n["id"]))
    edges.sort(key=lambda e: (e["source"], e["target"], e["type"]))
    dimensions.sort(key=lambda d: (d["label"], d["id"]))
    weights.sort(key=lambda w: (w["dimension"], w["assignment"], w["weight"]))
    stakeholders.sort(key=lambda s: (s["label"], s["id"]))

    return {
        "nodes": nodes,
        "edges": edges,
        "dimensions": dimensions,
        "weights": weights,
        "stakeholders": stakeholders,
    }


def main() -> int:
    g = load_graph(DATA_TTL)
    data = collect(g)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Ensure trailing newline for stable EOF fixer behavior
    JSON_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote JSON: {JSON_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
