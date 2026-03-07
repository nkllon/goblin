#!/usr/bin/env python3
"""Generate guidance-governance ontology and SHACL module files via RDFLib."""

from __future__ import annotations

import argparse
from pathlib import Path

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import OWL, RDF, RDFS, SH, XSD


REPO_ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY_PATH = REPO_ROOT / "goblin-guidance-ontology.ttl"
SHAPES_PATH = REPO_ROOT / "goblin-guidance-shapes.ttl"

UI = Namespace("https://nkllon.com/ui#")
UISH = Namespace("https://nkllon.com/ui/shapes#goblin#")


def _ontology_graph() -> Graph:
    g = Graph()
    g.bind("ui", UI)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    g.add((UI.GuidanceRequirement, RDF.type, OWL.Class))
    g.add((UI.GuidanceRequirement, RDFS.label, Literal("Guidance Requirement")))
    g.add(
        (
            UI.GuidanceRequirement,
            RDFS.comment,
            Literal("Normalized governance requirement extracted from guidance artifacts."),
        )
    )

    g.add((UI.GuidanceTopic, RDF.type, OWL.Class))
    g.add((UI.GuidanceTopic, RDFS.label, Literal("Guidance Topic")))
    g.add((UI.GuidanceTopic, RDFS.comment, Literal("Normalized topic for cross-artifact drift checks.")))

    g.add((UI.NormativeModality, RDF.type, OWL.Class))
    g.add((UI.NormativeModality, RDFS.label, Literal("Normative Modality")))

    for iri, label in (
        (UI.Must, "must"),
        (UI.MustNot, "must_not"),
        (UI.Should, "should"),
        (UI.ShouldNot, "should_not"),
        (UI.Policy, "policy"),
    ):
        g.add((iri, RDF.type, UI.NormativeModality))
        g.add((iri, RDFS.label, Literal(label)))

    for iri, label in (
        (UI.Topic_GitHubAuth, "github.auth"),
        (UI.Topic_OntologyGovernance, "ontology.governance"),
        (UI.Topic_QueuePrioritization, "queue.prioritization"),
        (UI.Topic_Branching, "branching"),
    ):
        g.add((iri, RDF.type, UI.GuidanceTopic))
        g.add((iri, RDFS.label, Literal(label)))

    g.add((UI.hasGuidanceTopic, RDF.type, OWL.ObjectProperty))
    g.add((UI.hasGuidanceTopic, RDFS.label, Literal("has guidance topic")))
    g.add((UI.hasGuidanceTopic, RDFS.domain, UI.GuidanceRequirement))
    g.add((UI.hasGuidanceTopic, RDFS.range, UI.GuidanceTopic))

    g.add((UI.hasModality, RDF.type, OWL.ObjectProperty))
    g.add((UI.hasModality, RDFS.label, Literal("has modality")))
    g.add((UI.hasModality, RDFS.domain, UI.GuidanceRequirement))
    g.add((UI.hasModality, RDFS.range, UI.NormativeModality))

    g.add((UI.sourceArtifact, RDF.type, OWL.DatatypeProperty))
    g.add((UI.sourceArtifact, RDFS.label, Literal("source artifact")))
    g.add((UI.sourceArtifact, RDFS.domain, UI.GuidanceRequirement))
    g.add((UI.sourceArtifact, RDFS.range, XSD.string))

    g.add((UI.sourceLine, RDF.type, OWL.DatatypeProperty))
    g.add((UI.sourceLine, RDFS.label, Literal("source line")))
    g.add((UI.sourceLine, RDFS.domain, UI.GuidanceRequirement))
    g.add((UI.sourceLine, RDFS.range, XSD.integer))

    g.add((UI.enforcementLevel, RDF.type, OWL.DatatypeProperty))
    g.add((UI.enforcementLevel, RDFS.label, Literal("enforcement level")))
    g.add((UI.enforcementLevel, RDFS.domain, UI.GuidanceRequirement))
    g.add((UI.enforcementLevel, RDFS.range, XSD.string))

    return g


def _shapes_graph() -> Graph:
    g = Graph()
    g.bind("ui", UI)
    g.bind("sh", SH)
    g.bind("xsd", XSD)
    g.bind("uiSh", UISH)

    shape = UISH.GuidanceRequirementShape
    g.add((shape, RDF.type, SH.NodeShape))
    g.add((shape, SH.targetClass, UI.GuidanceRequirement))

    def _property(path, min_count=1, datatype=None, in_values=None, msg=None):
        node = UISH[f"Prop_{path.split('#')[-1]}"]
        g.add((shape, SH.property, node))
        g.add((node, SH.path, path))
        g.add((node, SH.minCount, Literal(min_count, datatype=XSD.integer)))
        if datatype is not None:
            g.add((node, SH.datatype, datatype))
        if in_values is not None:
            collection = UISH[f"In_{path.split('#')[-1]}"]
            g.add((node, SH["in"], collection))
            # Build rdf list manually
            head = collection
            for index, value in enumerate(in_values):
                nxt = UISH[f"In_{path.split('#')[-1]}_{index}"]
                g.add((head, RDF.first, value))
                if index == len(in_values) - 1:
                    g.add((head, RDF.rest, RDF.nil))
                else:
                    g.add((head, RDF.rest, nxt))
                head = nxt
        if msg:
            g.add((node, SH.message, Literal(msg)))

    _property(
        UI.hasGuidanceTopic,
        msg="GuidanceRequirement MUST define hasGuidanceTopic.",
    )
    _property(
        UI.hasModality,
        in_values=(UI.Must, UI.MustNot, UI.Should, UI.ShouldNot, UI.Policy),
        msg="GuidanceRequirement MUST define hasModality.",
    )
    _property(
        UI.sourceArtifact,
        datatype=XSD.string,
        msg="GuidanceRequirement MUST define sourceArtifact.",
    )
    _property(
        UI.sourceLine,
        datatype=XSD.integer,
        msg="GuidanceRequirement MUST define sourceLine.",
    )
    _property(
        UI.enforcementLevel,
        datatype=XSD.string,
        msg="GuidanceRequirement MUST define enforcementLevel.",
    )

    return g


def _serialize(g: Graph) -> str:
    text = g.serialize(format="turtle")
    assert isinstance(text, str)
    return text


def _write(path: Path, content: str, check: bool) -> int:
    if check:
        if not path.exists():
            return 1
        return 0 if path.read_text(encoding="utf-8") == content else 1
    path.write_text(content, encoding="utf-8")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    ontology = _serialize(_ontology_graph())
    shapes = _serialize(_shapes_graph())

    rc = 0
    rc |= _write(ONTOLOGY_PATH, ontology, args.check)
    rc |= _write(SHAPES_PATH, shapes, args.check)

    if args.check and rc != 0:
        print("FAIL: guidance governance module files are out of date.")
        print("Run: python3 tools/generate_guidance_governance_module.py")
        return 1

    if not args.check:
        print(f"Wrote {ONTOLOGY_PATH.name}")
        print(f"Wrote {SHAPES_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
