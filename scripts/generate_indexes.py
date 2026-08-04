#!/usr/bin/env python3
"""Build bundled dataset and sync context.jsonld.

Run from anywhere: python3 scripts/generate_indexes.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OBJECTS = ROOT / "objects"
SYSTEMS = ROOT / "systems"


def generate_bundled_data():
    master_file = OBJECTS / "troika-system-data.json"
    with open(master_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = [
        "backgrounds",
        "skills",
        "spells",
        "items",
        "enemies",
        "tables",
        "characters",
    ]
    for cat in categories:
        if cat in data and isinstance(data[cat], list):
            new_items = []
            for item in data[cat]:
                if isinstance(item, dict) and "$ref" in item:
                    ref_str = item["$ref"].removeprefix("./")
                    ref_path = OBJECTS / ref_str
                    with open(ref_path, "r", encoding="utf-8") as rf:
                        new_items.append(json.load(rf))
                else:
                    new_items.append(item)
            data[cat] = new_items

    bundled_file = OBJECTS / "troika-system-data.bundled.json"
    with open(bundled_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote objects/troika-system-data.bundled.json")


def sync_root_context():
    context_src = SYSTEMS / "context.jsonld"
    context_dst = ROOT / "context.jsonld"
    if context_src.exists():
        context_dst.write_bytes(context_src.read_bytes())
        print("synced context.jsonld to root")


def main():
    generate_bundled_data()
    sync_root_context()


if __name__ == "__main__":
    main()
