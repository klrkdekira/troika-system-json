"""Shared deterministic helpers for Troika! publishing artifacts."""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

BASE = "https://cheeleong.dev/troika-system-json/"
COLLECTIONS = [
    "backgrounds",
    "skills",
    "spells",
    "items",
    "enemies",
    "tables",
    "characters",
]

IGNORED_TEXT_KEYS = {"@context", "@id", "@type", "$ref"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, value) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def iter_object_files(root: Path) -> Iterator[tuple[str, Path]]:
    for collection in COLLECTIONS:
        directory = root / "objects" / collection
        if directory.is_dir():
            for path in sorted(directory.glob("*.json")):
                yield collection, path


def iter_text_fragments(value, path: str = "") -> Iterator[dict[str, str]]:
    """Yield human-meaningful scalar values with their structural paths."""
    if isinstance(value, dict):
        for key, child in value.items():
            if key in IGNORED_TEXT_KEYS:
                continue
            child_path = f"{path}.{key}" if path else key
            yield from iter_text_fragments(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_text_fragments(child, f"{path}[{index}]")
    elif isinstance(value, (str, int, float, bool)):
        text = str(value)
        if text:
            yield {"path": path, "text": text}
