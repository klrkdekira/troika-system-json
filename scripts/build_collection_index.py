#!/usr/bin/env python3
"""Generate compact display metadata for every collection."""

from __future__ import annotations

import argparse
from pathlib import Path

from publishlib import BASE, COLLECTIONS, dump_json, iter_object_files, load_json


def build(root: Path) -> None:
    collections = {name: [] for name in COLLECTIONS}
    for collection, path in iter_object_files(root):
        record = load_json(path)
        entry = {
            "slug": path.stem,
            "name": record.get("name", path.stem),
            "type": record.get("@type", ""),
        }
        if record.get("description"):
            entry["description"] = record["description"][:240]
        collections[collection].append(entry)
    for entries in collections.values():
        entries.sort(key=lambda entry: (entry["name"].casefold(), entry["slug"]))
    dump_json(
        root / "objects" / "collection-index.json",
        {
            "@context": BASE + "systems/context.jsonld",
            "@id": BASE + "objects/collection-index.json",
            "@type": "CollectionIndex",
            "collections": collections,
        },
    )
    print(f"collection-index: {sum(map(len, collections.values()))} entries")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    build(Path(args.root).resolve())


if __name__ == "__main__":
    main()
