#!/usr/bin/env python3
"""Report mixed-modality conflicts for guidance requirements."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS


UI = Namespace("https://nkllon.com/ui#")
POSITIVE = {str(UI.Must), str(UI.Should)}
NEGATIVE = {str(UI.MustNot), str(UI.ShouldNot)}


def _topic_label(g: Graph, iri) -> str:
    label = g.value(iri, RDFS.label)
    return str(label) if label else str(iri)


def _collect(data_path: Path, ontology_path: Path | None = None) -> dict[str, set[str]]:
    g = Graph()
    if ontology_path and ontology_path.exists():
        g.parse(ontology_path, format="turtle")
    g.parse(data_path, format="turtle")
    by_topic: dict[str, set[str]] = {}

    for req in g.subjects(RDF.type, UI.GuidanceRequirement):
        topic = g.value(req, UI.hasGuidanceTopic)
        modality = g.value(req, UI.hasModality)
        if topic is None or modality is None:
            continue
        topic_name = _topic_label(g, topic)
        by_topic.setdefault(topic_name, set()).add(str(modality))

    return by_topic


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--base-data", type=Path)
    parser.add_argument("--ontology", type=Path)
    parser.add_argument("--key-topic", action="append", default=["github.auth", "ontology.governance"])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    current = _collect(args.data, args.ontology)
    current_conflicts = []
    for topic, modalities in sorted(current.items()):
        if modalities.intersection(POSITIVE) and modalities.intersection(NEGATIVE):
            current_conflicts.append(topic)

    base_conflicts: list[str] = []
    if args.base_data and args.base_data.exists():
        base = _collect(args.base_data, args.ontology)
        for topic, modalities in sorted(base.items()):
            if modalities.intersection(POSITIVE) and modalities.intersection(NEGATIVE):
                base_conflicts.append(topic)

    payload = {
        "current_conflicts": current_conflicts,
        "base_conflicts": base_conflicts,
        "current_count": len(current_conflicts),
        "base_count": len(base_conflicts),
        "key_topic_conflicts": sorted(set(args.key_topic).intersection(current_conflicts)),
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("Current conflicts:", payload["current_count"])
        if current_conflicts:
            print("Topics:", ", ".join(current_conflicts))
        if args.base_data:
            print("Base conflicts:", payload["base_count"])
        if payload["key_topic_conflicts"]:
            print("Key-topic conflicts:", ", ".join(payload["key_topic_conflicts"]))

    if payload["key_topic_conflicts"]:
        return 1
    if args.base_data and payload["current_count"] > payload["base_count"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
