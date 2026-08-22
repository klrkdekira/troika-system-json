# Troika! System JSON

<p align="center">
  <img src="fortle.svg" alt="Fortle Logo" width="120" height="120">
</p>

<p align="center">
  <strong>A machine-readable JSON-LD 1.1 corpus, JSON Schema specification, and interactive explorer for the Troika! tabletop RPG System Reference Document (SRD).</strong>
</p>

<p align="center">
  <a href="https://cheeleong.dev/troika-system-json/"><img src="https://img.shields.io/badge/Live%20Explorer-cheeleong.dev-blue?style=flat-square" alt="Live Explorer"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square" alt="Version 0.1.0"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT%20%2B%20Troika!%20SRD-green?style=flat-square" alt="License"></a>
  <a href="CITATION.cff"><img src="https://img.shields.io/badge/Citation-CITATION.cff-blueviolet?style=flat-square" alt="Citation"></a>
  <br>
  <a href="systems/context.jsonld"><img src="https://img.shields.io/badge/Linked%20Data-JSON--LD%201.1-purple?style=flat-square" alt="JSON-LD 1.1"></a>
  <a href="systems/"><img src="https://img.shields.io/badge/JSON%20Schema-Draft--07%20%2F%202020--12-blue?style=flat-square" alt="JSON Schema"></a>
  <a href="datapackage.json"><img src="https://img.shields.io/badge/Data%20Package-Frictionless-orange?style=flat-square" alt="Data Package"></a>
  <a href="objects/troika-system-data.json"><img src="https://img.shields.io/badge/Corpus-225%20Entities-success?style=flat-square" alt="Corpus 225 Entities"></a>
  <a href="llms.txt"><img src="https://img.shields.io/badge/AI%2FLLM-llms.txt-teal?style=flat-square" alt="llms.txt"></a>
  <br>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.12+"></a>
  <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/badge/uv-Astral-261230?style=flat-square&logo=astral&logoColor=white" alt="uv package manager"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/Code%20Style-Ruff-000000?style=flat-square&logo=ruff&logoColor=white" alt="Ruff code style"></a>
  <a href="tests/"><img src="https://img.shields.io/badge/Tests-45%20Passing-success?style=flat-square" alt="Tests"></a>
  <a href="main.py"><img src="https://img.shields.io/badge/Schema%20Validation-Passing-brightgreen?style=flat-square" alt="Schema Validation"></a>
</p>

---

## Overview

**Troika! System JSON** turns the official [Troika! System Reference Document (SRD)](https://troika-srd.netlify.app/) into structured, schema-validated, and linked JSON data.

Every background, spell, skill, enemy, item, and roll table is represented as:
1. **Granular JSON-LD objects** with explicit semantic `@context`, `@id`, and `@type` fields.
2. **Deterministic single-file bundles** for zero-dependency client integration.
3. **AI/LLM-ready text projections** (`llms.txt`, `llms-full.txt`) for agents, crawlers, and retrieval pipelines.
4. **Precomputed static indexes** (`search-index.json`, `collection-index.json`) for instant client-side search without a backend.

Explore the dataset live at **[cheeleong.dev/troika-system-json](https://cheeleong.dev/troika-system-json/)**.

---

## Dataset Summary

The corpus contains **225 structured entities** across 7 core collections:

| Collection | Path | Count | Description |
| :--- | :--- | :---: | :--- |
| **Backgrounds** | [`objects/backgrounds/`](objects/backgrounds/) | 36 | Complete d66 character backgrounds with skills, possessions, and special abilities |
| **Enemies** | [`objects/enemies/`](objects/enemies/) | 25 | Bestiary entries with initiative (Miên), stamina, armor ratings, and attacks |
| **Items** | [`objects/items/`](objects/items/) | 50 | Weapons, armor, gear, and provisions with silver values, inventory slots, and damage rows |
| **Skills** | [`objects/skills/`](objects/skills/) | 22 | Advanced skills definitions, prerequisites, and descriptions |
| **Spells** | [`objects/spells/`](objects/spells/) | 74 | Magic spells with stamina costs, casting requirements, and rules |
| **Tables** | [`objects/tables/`](objects/tables/) | 5 | Core matrices: Melee, Ranged, and Beastly damage tables, Oops table, and Random Spell table |
| **Characters** | [`objects/characters/`](objects/characters/) | 3 | Sample pre-generated character records |

---

## Repository Structure

```
troika-system-json/
├── objects/                              # Game data collections (JSON & JSON-LD 1.1)
│   ├── troika-system-data.json           # Master manifest linking entities via $ref
│   ├── troika-system-data.bundled.json   # Single-file bundled corpus (all $refs inlined)
│   ├── search-index.json                 # Precomputed static inverted search index
│   ├── collection-index.json             # Lightweight collection metadata index
│   ├── backgrounds/                      # 36 character background files
│   ├── characters/                       # Sample character sheets
│   ├── enemies/                          # 25 bestiary records
│   ├── items/                            # 50 equipment and item entries
│   ├── skills/                           # 22 advanced skill files
│   ├── spells/                           # 74 spell records
│   └── tables/                           # 5 core system tables & damage matrices
├── systems/                              # JSON Schemas (Draft 7 / Draft 2020-12)
│   ├── context.jsonld                    # Shared JSON-LD vocabulary and context
│   ├── background.schema.json            # Schema for character backgrounds
│   ├── character.schema.json             # Schema for character sheets
│   ├── enemy.schema.json                 # Schema for enemies
│   ├── item.schema.json                  # Schema for items and weapons
│   ├── skill.schema.json                 # Schema for advanced skills
│   ├── spell.schema.json                 # Schema for spells
│   ├── table.schema.json                 # Schema for damage and roll tables
│   └── troika-system.schema.json         # Schema for the top-level manifest and bundle
├── scripts/                              # Publishing and index generation tools
│   ├── publishlib.py                     # Shared corpus traversal utilities
│   ├── build_llms.py                     # Generates llms.txt
│   ├── build_llms_full.py                # Generates llms-full.txt
│   ├── build_search_index.py             # Generates objects/search-index.json
│   ├── build_collection_index.py         # Generates objects/collection-index.json
│   ├── build_sitemap.py                  # Generates sitemap.xml
│   └── generate_indexes.py               # Compiles inlined bundle & root context
├── tests/                                # Test suite (45 unit tests)
├── datapackage.json                      # Frictionless Data Package metadata
├── CITATION.cff                          # Citation File Format metadata
├── llms.txt                              # Concise agent and crawler corpus guide
├── llms-full.txt                         # Full-text context projection of all records
├── index.html                            # Interactive single-page web explorer
├── Makefile                              # Build, test, validate, and publishing tasks
└── pyproject.toml                        # Python package configuration
```

---

## Machine-Readable Publishing & AI/LLM Access

This repository implements standardized discovery formats for AI agents, search engines, and data pipelines:

- **[`llms.txt`](llms.txt)**: A concise index following the `/llms.txt` standard with collection summaries, counts, and canonical URLs.
- **[`llms-full.txt`](llms-full.txt)**: A complete, deterministic markdown projection of all 225 records designed for direct context-window ingestion.
- **[`objects/search-index.json`](objects/search-index.json)**: Static inverted index spanning ~3,880 searchable tokens for zero-backend client search.
- **[`objects/collection-index.json`](objects/collection-index.json)**: Lightweight metadata summaries for rapidly browsing collections.
- **[`datapackage.json`](datapackage.json)**: [Frictionless Data Package](https://datapackage.org/) descriptor defining all resources and licenses.
- **[`sitemap.xml`](sitemap.xml)** & **[`robots.txt`](robots.txt)**: Search engine crawler manifests and canonical URLs.

---

## Quick Start & Consumption

### 1. Inlined Single-File Bundle
For apps, web clients, or bots that need all data in a single HTTP request:
```bash
curl -O https://cheeleong.dev/troika-system-json/objects/troika-system-data.bundled.json
```

### 2. Individual Entities via JSON-LD
Each entity is addressable directly by its `@id`:
```bash
# Fetch the 'Epopt' background
curl -O https://cheeleong.dev/troika-system-json/objects/backgrounds/04-epopt.json

# Fetch the 'Fire Bolt' spell
curl -O https://cheeleong.dev/troika-system-json/objects/spells/fire-bolt.json
```

### 3. Python Integration
```python
import json
from urllib.request import urlopen

# Load bundled corpus
url = "https://cheeleong.dev/troika-system-json/objects/troika-system-data.bundled.json"
with urlopen(url) as response:
    corpus = json.loads(response.read().decode())

# Access backgrounds and spells
print(f"Loaded {len(corpus['backgrounds'])} backgrounds and {len(corpus['spells'])} spells.")
```

---

## Development, Validation & Testing

### Prerequisites
- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) (recommended) or standard `pip`

Install dependencies:
```bash
uv sync
```

### Makefile Commands

| Command | Description |
| :--- | :--- |
| `make check` | Full pipeline: rebuilds all publishing artifacts, validates all schemas, and runs test suite |
| `make publish` | Regenerates all publishing artifacts (`bundle`, `llms.txt`, `llms-full.txt`, indexes, sitemap) |
| `make validate` | Validates all JSON files against their schemas and verifies cross-references |
| `make test` | Runs the test suite via `unittest` |
| `make bundle` | Compiles `troika-system-data.bundled.json` and syncs `context.jsonld` |
| `make search-index` | Regenerates `objects/search-index.json` |
| `make collection-index` | Regenerates `objects/collection-index.json` |
| `make llms` | Regenerates `llms.txt` |
| `make llms-full` | Regenerates `llms-full.txt` |
| `make sitemap` | Regenerates `sitemap.xml` |

### CLI Validation

Validate all files or specific directories:
```bash
# Validate entire dataset with Rich formatted output
uv run python main.py

# Validate and cross-check all cross-references ($ref, item IDs, spell names)
uv run python main.py objects --check-references

# Validate a single file against its schema
uv run python main.py objects/backgrounds/01-arphaestian-unfettered.json
```

### Running Tests
```bash
uv run python -m unittest discover -s tests -v
```

---

## Citation

If you use or reference this dataset in research, tools, or applications, please cite it using the metadata from [`CITATION.cff`](CITATION.cff):

```bibtex
@dataset{chow_troika_system_json_2026,
  author    = {Chow, Chee Leong},
  title     = {Troika! System JSON},
  year      = {2026},
  url       = {https://cheeleong.dev/troika-system-json/},
  version   = {0.1.0},
  note      = {Machine-readable JSON-LD 1.1 corpus and JSON Schemas for the Troika! SRD}
}
```

---

## License & Attribution

<p align="center">
  <img src="fortle.svg" alt="Fortle Logo" width="100" height="100">
</p>

- **Repository Code, Schemas, Architecture & UI**: Licensed under the [MIT License](LICENSE) &copy; 2026 [Chee Leong](https://cheeleong.dev).
- **Troika! Game Content**: Content from the *Troika! System Reference Document* remains &copy; [Melsonian Arts Council](https://www.troika-rpg.com/) and is used under the terms of the official [Troika! SRD](https://troika-srd.netlify.app/) ([dialectrical/troika-srd](https://github.com/dialectrical/troika-srd)).
- *Troika!* is a trademark of the Melsonian Arts Council. *Troika! System JSON* is an independent production and is not affiliated with the Melsonian Arts Council.
