#!/usr/bin/env python3
"""Generate llms-full.txt as a single-file LLM ingestion context."""

from __future__ import annotations

import argparse
from pathlib import Path

from publishlib import (
    BASE,
    COLLECTIONS,
    iter_object_files,
    iter_text_fragments,
    load_json,
)


def format_record(record: dict) -> str:
    lines = [
        f"### {record.get('name', 'Unnamed record')}",
        f"id: {record.get('@id', '')}",
    ]
    for fragment in iter_text_fragments(record):
        if fragment["path"] == "name":
            continue
        lines.extend(("", f"[{fragment['path']}]", fragment["text"]))
    return "\n".join(lines)


def build(root: Path) -> None:
    out = [
        "# Troika! System JSON — full corpus context",
        "",
        "Machine-readable JSON and JSON-LD reference corpus for the Troika! SRD.",
        f"Base IRI: {BASE}",
        f"Manifest: {BASE}objects/troika-system-data.json",
        "",
        "Attribution: Based on the Troika! SRD by Melsonian Arts Council and dialectrical. Troika! System JSON is an independent production by Chee Leong and is not affiliated with the Melsonian Arts Council.",
        "",
    ]
    files = list(iter_object_files(root))
    for collection in COLLECTIONS:
        records = [
            load_json(path)
            for item_collection, path in files
            if item_collection == collection
        ]
        out.extend((f"## Collection: {collection} ({len(records)} records)", ""))
        for record in records:
            out.extend((format_record(record), ""))
    output = "\n".join(out) + "\n"
    (root / "llms-full.txt").write_text(output, encoding="utf-8")
    print(f"llms-full.txt: {len(files)} records, {len(output.splitlines())} lines")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    build(Path(args.root).resolve())


if __name__ == "__main__":
    main()
