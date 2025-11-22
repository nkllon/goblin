from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .validator import ValidationResult, validate


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="goblin-validate",
        description="Validate a Goblin score RDF/JSON-LD document against SHACL shapes.",
    )
    parser.add_argument(
        "data",
        help="Path to data graph (JSON-LD, TTL, RDF/XML, etc.).",
    )
    parser.add_argument(
        "--shapes",
        required=True,
        help="Path to SHACL shapes TTL.",
    )
    parser.add_argument(
        "--data-format",
        default=None,
        help="Optional explicit RDF format for data (e.g., json-ld, turtle).",
    )
    parser.add_argument(
        "--shapes-format",
        default="turtle",
        help="Optional explicit RDF format for shapes (default: turtle).",
    )
    parser.add_argument(
        "--inference",
        default="rdfs",
        choices=["none", "rdfs", "owlrl"],
        help="Inference mode during validation (default: rdfs).",
    )
    parser.add_argument(
        "--no-advanced",
        action="store_true",
        help="Disable advanced SHACL features.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    result: ValidationResult = validate(
        data_graph_path=Path(args.data),
        shapes_graph_path=Path(args.shapes),
        data_format=args.data_format,
        shapes_format=args.shapes_format,
        inference=args.inference,
        advanced=not args.no_advanced,
    )

    print(result.report_text.strip())
    return 0 if result.conforms else 1


if __name__ == "__main__":
    raise SystemExit(main())
