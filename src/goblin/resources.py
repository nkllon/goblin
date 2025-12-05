from contextlib import contextmanager
from importlib import resources
from pathlib import Path
from typing import Generator, Iterable, Iterator, Sequence

RESOURCE_PACKAGE = "goblin.data"
RESOURCE_FILES = (
    "goblin-ontology.ttl",
    "goblin-shapes.ttl",
    "goblin-map.dot",
    "goblin-sample.ttl",
)


def available_resources() -> Iterable[str]:
    """Return the names of packaged Goblin resource files."""

    return RESOURCE_FILES


def _candidate_paths(name: str) -> Iterator[Path]:
    """Yield possible on-disk paths for a resource.

    When running from a wheel/sdist we expect resources inside ``goblin.data``.
    When running from a source checkout (``python -m goblin.validate`` without
    installation) we also try repo-root fallbacks.
    """

    package_target = resources.files(RESOURCE_PACKAGE) / name
    if package_target.exists():
        yield package_target

    repo_root = Path(__file__).resolve().parents[2]
    fallback_locations: Sequence[Path] = (
        Path(__file__).resolve().parent / "data" / name,
        repo_root / name,
        repo_root / "samples" / name,
    )

    for candidate in fallback_locations:
        if candidate.exists():
            yield candidate


@contextmanager
def resource_path(name: str) -> Generator[Path, None, None]:
    """Yield a concrete filesystem path for a packaged resource."""

    if name not in RESOURCE_FILES:
        raise FileNotFoundError(f"Unknown Goblin resource: {name}")

    for candidate in _candidate_paths(name):
        # If the path lives inside the package, convert any importlib.resources
        # handle into a real filesystem path. For plain files (source checkout),
        # just yield the path directly.
        if RESOURCE_PACKAGE in candidate.parts:
            with resources.as_file(candidate) as path:
                yield path
        else:
            yield candidate
        return

    raise FileNotFoundError(f"Packaged resource not found: {name}")


@contextmanager
def resource_stream(name: str):
    """Yield a binary stream for a packaged resource."""

    with resource_path(name) as path:
        with path.open("rb") as handle:
            yield handle
