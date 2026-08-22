# Troika! System JSON

Structured JSON and JSON Schemas for the [Troika!](https://www.troika-rpg.com/) tabletop RPG System Reference Document (SRD).

Available online at [cheeleong.dev/troika-system-json](https://cheeleong.dev/troika-system-json/).

## Structure

```
troika-system-json/
├── objects/                    # Game data (JSON & JSON-LD)
│   ├── troika-system-data.json # Aggregated data bundle
│   ├── backgrounds/            # 36 character backgrounds (d66 table)
│   ├── characters/             # Sample characters
│   ├── enemies/                # Bestiary entries
│   ├── items/                  # Equipment & items
│   ├── skills/                 # Advanced skills
│   ├── spells/                 # Spells
│   └── tables/                 # Random tables
└── systems/                    # JSON Schemas & JSON-LD Context
    ├── context.jsonld          # Shared JSON-LD context
    └── *.schema.json           # Schemas for validation
```

## Quick Start

- **Full Data Bundle:** Use [`objects/troika-system-data.json`](objects/troika-system-data.json) for all data stitched via JSON references.
- **Individual Entities:** Fetch individual JSON files from `objects/<category>/`.
- **Validation & Testing:** Validate entities against schemas in [`systems/`](systems/). Run tests with `python -m unittest`.

## Machine-readable publishing

- [`llms.txt`](llms.txt) provides a concise corpus guide for agents and crawlers.
- [`llms-full.txt`](llms-full.txt) contains a complete text projection of every record.
- [`objects/search-index.json`](objects/search-index.json) and [`objects/collection-index.json`](objects/collection-index.json) support static search and browsing.
- [`datapackage.json`](datapackage.json), [`sitemap.xml`](sitemap.xml), and [`robots.txt`](robots.txt) describe the published package.

Run `make publish` to rebuild all generated publishing artifacts, or `make check` to rebuild, validate, and test the repository.

## Citation

Preferred citation metadata is available in [`CITATION.cff`](CITATION.cff). If you use or redistribute the dataset, retain the Troika! SRD attribution and follow the content terms described in [`LICENSE`](LICENSE).

## License & Attribution

<p align="center">
  <img src="fortle.svg" alt="Fortle Logo" width="120" height="120">
</p>

*Troika! System JSON* (the code, schemas, and data structure) is an independent production by [Chee Leong](https://cheeleong.dev) under the MIT License. Original Troika! game content remains copyright of the Melsonian Arts Council; this project is not affiliated with the Melsonian Arts Council.

Based on the official [Troika! System Reference Document (SRD)](https://troika-srd.netlify.app/) ([repository](https://github.com/dialectrical/troika-srd)). *Troika!* is a trademark of the Melsonian Arts Council.
