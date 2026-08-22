#!/usr/bin/env python3
"""Generate sitemap.xml for top-level artifacts and individual records."""

from __future__ import annotations

import argparse
from pathlib import Path
from xml.sax.saxutils import escape

from publishlib import BASE, iter_object_files, load_json


def build(root: Path) -> None:
    urls = [
        BASE,
        BASE + "README.md",
        BASE + "CITATION.cff",
        BASE + "LICENSE",
        BASE + "datapackage.json",
        BASE + "llms.txt",
        BASE + "llms-full.txt",
        BASE + "objects/troika-system-data.json",
        BASE + "objects/troika-system-data.bundled.json",
        BASE + "objects/search-index.json",
        BASE + "objects/collection-index.json",
        BASE + "systems/context.jsonld",
    ]
    urls.extend(
        load_json(path).get("@id", BASE + path.relative_to(root).as_posix())
        for _, path in iter_object_files(root)
    )
    body = "\n".join(
        f"  <url><loc>{escape(url)}</loc></url>" for url in dict.fromkeys(urls)
    )
    (root / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>\n",
        encoding="utf-8",
    )
    print(f"sitemap: {len(dict.fromkeys(urls))} URLs")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    build(Path(args.root).resolve())


if __name__ == "__main__":
    main()
