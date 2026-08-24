# Troika! System JSON

<p align="center">
  <img src="fortle.svg" alt="Fortle logo" width="120" height="120">
</p>

<p align="center">
  <strong>A machine-readable JSON-LD corpus, JSON Schema specification, and interactive explorer for the Troika! tabletop RPG System Reference Document.</strong>
</p>

<p align="center">
  <a href="https://cheeleong.dev/troika-system-json/"><img src="https://img.shields.io/badge/Explorer-Live-4f46e5?style=flat-square" alt="Live explorer"></a>
  <a href="systems/context.jsonld"><img src="https://img.shields.io/badge/JSON--LD-1.1-7b1fa2?style=flat-square" alt="JSON-LD 1.1"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT%20%2B%20Troika!%20SRD-059669?style=flat-square" alt="MIT and Troika! SRD license"></a>
</p>

## Overview

Troika! System JSON turns the official [Troika! System Reference Document](https://troika-srd.netlify.app/) into structured, schema-validated, linked data. Browse it in the [live explorer](https://cheeleong.dev/troika-system-json/) or use the published files directly in applications, tools, and retrieval pipelines.

The repository provides:

- Granular JSON-LD records with explicit `@context`, `@id`, and `@type` fields.
- JSON Schemas for backgrounds, characters, enemies, items, skills, spells, and tables.
- A deterministic, single-file bundle for zero-dependency client integration.
- AI-friendly text projections and precomputed indexes for static search and retrieval.

## Use the dataset

Choose the artifact that best fits your use case:

| Artifact | Best for |
| :--- | :--- |
| [Live explorer](https://cheeleong.dev/troika-system-json/) | Browsing and searching the corpus |
| [`troika-system-data.bundled.json`](objects/troika-system-data.bundled.json) | Loading the complete corpus in one request |
| [`troika-system-data.json`](objects/troika-system-data.json) | Traversing the corpus as a manifest of `$ref` links |
| [`llms.txt`](llms.txt) | Discovering collections and canonical URLs |
| [`llms-full.txt`](llms-full.txt) | Ingesting a deterministic full-text projection |
| [`datapackage.json`](datapackage.json) | Using the corpus as a Frictionless Data Package |

### Download the complete corpus

```bash
curl -O https://cheeleong.dev/troika-system-json/objects/troika-system-data.bundled.json
```

### Fetch individual records

Each record is available at a stable URL:

```bash
# Epopt background
curl -O https://cheeleong.dev/troika-system-json/objects/backgrounds/23-epopt.json

# Fire Bolt spell
curl -O https://cheeleong.dev/troika-system-json/objects/spells/fire-bolt.json
```

### Load the bundle with Python

```python
import json
from urllib.request import urlopen

url = "https://cheeleong.dev/troika-system-json/objects/troika-system-data.bundled.json"

with urlopen(url) as response:
    corpus = json.load(response)

print(
    f"Loaded {len(corpus['backgrounds'])} backgrounds "
    f"and {len(corpus['spells'])} spells."
)
```

## Collections

The corpus contains **225 records** across seven collections:

| Collection | Records | Description |
| :--- | :---: | :--- |
| [Backgrounds](objects/backgrounds/) | 36 | d66 character backgrounds with skills, possessions, and special abilities |
| [Characters](objects/characters/) | 2 | Sample pre-generated character records |
| [Enemies](objects/enemies/) | 36 | Bestiary entries with initiative (Miên), stamina, armor ratings, and attacks |
| [Items](objects/items/) | 50 | Weapons, armor, gear, and provisions with values, inventory slots, and damage rows |
| [Skills](objects/skills/) | 22 | Advanced skill definitions, prerequisites, and descriptions |
| [Spells](objects/spells/) | 74 | Spells with stamina costs, casting requirements, and rules |
| [Tables](objects/tables/) | 5 | Damage matrices and core random tables |

The publishing pipeline also produces [`objects/search-index.json`](objects/search-index.json), [`objects/collection-index.json`](objects/collection-index.json), [`sitemap.xml`](sitemap.xml), and [`robots.txt`](robots.txt) for static discovery and search.

## Repository structure

```text
troika-system-json/
├── objects/                    # JSON-LD records, manifests, bundle, and indexes
│   ├── backgrounds/
│   ├── characters/
│   ├── enemies/
│   ├── items/
│   ├── skills/
│   ├── spells/
│   └── tables/
├── systems/                    # JSON Schemas and the shared JSON-LD context
├── scripts/                    # Publishing and index-generation tools
├── tests/                      # Unit test suite
├── datapackage.json            # Frictionless Data Package metadata
├── llms.txt                    # Concise agent and crawler guide
├── llms-full.txt               # Full-text corpus projection
├── index.html                  # Interactive web explorer
├── Makefile                    # Build, validation, and test tasks
└── pyproject.toml              # Python project configuration
```

## Development

### Requirements

- Python 3.12.10 or newer
- [`uv`](https://github.com/astral-sh/uv)

Install the dependencies and run the complete verification pipeline:

```bash
uv sync
make check
```

### Common commands

| Command | Description |
| :--- | :--- |
| `make check` | Rebuild all artifacts, validate the corpus and references, and run the tests |
| `make publish` | Regenerate the bundle, text projections, indexes, and sitemap |
| `make validate` | Validate JSON files against their schemas and check cross-references |
| `make test` | Run the unit test suite |
| `make bundle` | Rebuild the single-file corpus and synchronize the JSON-LD context |
| `make search-index` | Regenerate the static search index |
| `make collection-index` | Regenerate the collection metadata index |
| `make llms` | Regenerate `llms.txt` |
| `make llms-full` | Regenerate `llms-full.txt` |
| `make sitemap` | Regenerate `sitemap.xml` |

### Validate specific data

```bash
# Validate the complete dataset
uv run python main.py

# Validate the dataset and all cross-references
uv run python main.py objects --check-references

# Validate one record
uv run python main.py objects/backgrounds/23-epopt.json
```

## Citation

If you use this dataset in research, tools, or applications, cite the metadata in [`CITATION.cff`](CITATION.cff):

```bibtex
@dataset{chow_troika_system_json_2026,
  author  = {Chow, Chee Leong},
  title   = {Troika! System JSON},
  year    = {2026},
  url     = {https://cheeleong.dev/troika-system-json/},
  version = {0.1.0},
  note    = {Machine-readable JSON-LD corpus and JSON Schemas for the Troika! SRD}
}
```

## License and attribution

- Repository code, schemas, architecture, and interface: [MIT License](LICENSE), copyright 2026 [Chee Leong](https://cheeleong.dev).
- Troika! game content: copyright [Melsonian Arts Council](https://www.troika-rpg.com/), used under the terms of the official [Troika! SRD](https://troika-srd.netlify.app/).
- Troika! is a trademark of the Melsonian Arts Council. Troika! System JSON is an independent production and is not affiliated with the Melsonian Arts Council.
