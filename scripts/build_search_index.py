#!/usr/bin/env python3
"""Generate a deterministic, static full-text token index."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from publishlib import (
    BASE,
    dump_json,
    iter_object_files,
    iter_text_fragments,
    load_json,
)

TOKEN_RE = re.compile(r"[a-z0-9']+")
STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "of",
    "to",
    "in",
    "on",
    "is",
    "it",
    "that",
    "this",
    "as",
    "for",
    "with",
    "by",
    "at",
    "be",
    "are",
    "can",
    "if",
}


def build(root: Path) -> None:
    documents: list[dict] = []
    postings: dict[str, list[dict]] = {}
    for collection, path in iter_object_files(root):
        record = load_json(path)
        fragments = list(iter_text_fragments(record))
        document = len(documents)
        documents.append(
            {
                "id": record.get(
                    "@id", BASE + path.relative_to(root).as_posix()
                ).removeprefix(BASE),
                "type": record.get("@type", ""),
                "name": record.get("name", path.stem),
                "collection": collection,
                "excerpt": next(
                    (f["text"][:160] for f in fragments if f["path"] == "description"),
                    "",
                ),
            }
        )
        found: dict[str, str] = {}
        for fragment in fragments:
            value = fragment["text"]
            for match in TOKEN_RE.finditer(value.lower()):
                token = match.group()
                if len(token) < 3 or token in STOPWORDS or token in found:
                    continue
                start, end = (
                    max(0, match.start() - 55),
                    min(len(value), match.end() + 105),
                )
                found[token] = re.sub(r"\s+", " ", value[start:end]).strip()
        for token, excerpt in found.items():
            postings.setdefault(token, []).append(
                {"document": document, "excerpt": excerpt}
            )
    dump_json(
        root / "objects" / "search-index.json",
        {
            "@context": BASE + "systems/context.jsonld",
            "@id": BASE + "objects/search-index.json",
            "@type": "SearchIndex",
            "base": BASE,
            "documents": documents,
            "tokens": {token: postings[token] for token in sorted(postings)},
        },
    )
    print(f"search-index: {len(documents)} documents, {len(postings)} tokens")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    build(Path(args.root).resolve())


if __name__ == "__main__":
    main()
