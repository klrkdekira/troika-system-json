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

## License & Attribution

<p align="center">
  <img src="fortle.svg" alt="Fortle Logo" width="120" height="120">
</p>

*Troika! System JSON* (the code, schemas, and data structure) is an independent production by [Chee Leong](https://cheeleong.dev) under the MIT License. Original Troika! game content remains copyright of the Melsonian Arts Council; this project is not affiliated with the Melsonian Arts Council.

Based on the official [Troika! System Reference Document (SRD)](https://troika-srd.netlify.app/) ([repository](https://github.com/dialectrical/troika-srd)). *Troika!* is a trademark of the Melsonian Arts Council.
