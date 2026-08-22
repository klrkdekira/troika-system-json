#!/usr/bin/env python3
"""Generate the concise llms.txt discovery document."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from publishlib import BASE, COLLECTIONS, iter_object_files


def build(root: Path) -> None:
    counts = Counter(collection for collection, _ in iter_object_files(root))
    total = sum(counts.values())
    labels = {
        "backgrounds": "Backgrounds",
        "skills": "Advanced skills",
        "spells": "Spells",
        "items": "Items",
        "enemies": "Enemies",
        "tables": "Tables",
        "characters": "Sample characters",
    }
    lines = [
        "# Troika! System JSON",
        "",
        f"> Machine-readable JSON and JSON-LD reference corpus for the Troika! SRD. {total} records with JSON Schema validation.",
        "",
        "Attribution: Based on the Troika! SRD by Melsonian Arts Council and dialectrical. Troika! System JSON is an independent production by Chee Leong and is not affiliated with the Melsonian Arts Council.",
        "",
        "## Entry points",
        "",
        f"- [Full corpus context]({BASE}llms-full.txt): complete text projection of every record",
        f"- [Reference manifest]({BASE}objects/troika-system-data.json): collection lists using JSON References",
        f"- [Single-file bundle]({BASE}objects/troika-system-data.bundled.json): every record in one document",
        f"- [Search index]({BASE}objects/search-index.json): static inverted token index",
        f"- [Collection index]({BASE}objects/collection-index.json): compact browse metadata",
        f"- [JSON-LD context]({BASE}systems/context.jsonld)",
        "",
        "## Collections",
        "",
    ]
    for collection in COLLECTIONS:
        lines.append(
            f"- {labels[collection]}: {counts[collection]} records under `objects/{collection}/`"
        )
    lines.extend(
        [
            "",
            "## Documentation",
            "",
            f"- [README]({BASE}README.md)",
            f"- [Citation metadata]({BASE}CITATION.cff)",
            f"- [License and attribution]({BASE}LICENSE)",
            "- [Official Troika! SRD](https://troika-srd.netlify.app/)",
            "",
        ]
    )
    (root / "llms.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"llms.txt: {total} records")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    build(Path(args.root).resolve())


if __name__ == "__main__":
    main()
