#!/usr/bin/env python3
from pathlib import Path

from goblin.validate import validate_graph


REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    data_ttl = REPO_ROOT / "samples" / "goblin-sample.ttl"
    shapes_ttl = REPO_ROOT / "goblin-shapes.ttl"

    result = validate_graph(data_ttl, shapes_ttl)
    print(result.results_text.strip() or "SHACL validation produced no messages.")
    return 0 if result.conforms else 1


if __name__ == "__main__":
    raise SystemExit(main())
