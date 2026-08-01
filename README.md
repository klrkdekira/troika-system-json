# Troika! System JSON

The Troika! tabletop RPG as structured JSON. Backgrounds, enemies, items, skills, spells and tables each live in their own file, with JSON Schemas to validate against. If you'd rather fetch than clone, everything is served at [troika-system-json.cheeleong.dev](https://troika-system-json.cheeleong.dev).

## What's in here

```
troika-system-json/
├── objects/                    # Game data
│   ├── troika-system-data.json # Aggregates everything via JSON references
│   ├── backgrounds/            # 36 character backgrounds (the d66 table)
│   ├── enemies/                # 36 bestiary entries
│   ├── items/                  # 50 pieces of equipment
│   ├── skills/                 # 22 advanced skills
│   ├── spells/                 # 74 spells
│   └── tables/                 # 5 random tables
└── systems/                    # JSON Schemas, one per data type
    ├── troika-system.schema.json
    ├── background.schema.json
    ├── character.schema.json
    ├── enemy.schema.json
    ├── item.schema.json
    ├── skill.schema.json
    ├── spell.schema.json
    └── table.schema.json
```

## Usage

Start with `objects/troika-system-data.json` if you want the whole system in one go. It stitches the individual files together with JSON references. If you only need part of it, grab files straight from the relevant directory; every background, enemy, item and so on is self-contained and follows the schema for its type in `systems/`.

All the data from the Troika! SRD is covered.

## Licence & Attribution

<p align="center">
  <img src="fortle.svg" alt="Fortle Logo" width="200" height="200">
</p>

This project is based on the **Troika!** tabletop RPG system by the **Melsonian Arts Council**, sourced from the official [Troika! System Reference Document (SRD)](https://troika-srd.netlify.app/) and its open source repository [`dialectrical/troika-srd`](https://github.com/dialectrical/troika-srd).

### Third Party Compatibility

This is an independent production and is not affiliated with the Melsonian Arts Council. It is published under the terms outlined in the [Troika! System Reference Document (SRD)](https://troika-srd.netlify.app/).

**Troika! System JSON is an independent production by [Chee Leong](https://cheeleong.dev) and is not affiliated with the Melsonian Arts Council.**

### Attribution & Sources

* **Troika! SRD Web**: [https://troika-srd.netlify.app/](https://troika-srd.netlify.app/)
* **Troika! SRD Repository**: [https://github.com/dialectrical/troika-srd](https://github.com/dialectrical/troika-srd)

### Terms of Use

- The mechanics and concepts of "Troika!" are used under the terms of the SRD
- This data structure may be used freely for compatible projects
- Original game content remains copyright of the Melsonian Arts Council
- See the [SRD](https://troika-srd.netlify.app/) and [`dialectrical/troika-srd`](https://github.com/dialectrical/troika-srd) for complete licensing terms

### Original Work

"Troika!" is a trademark of the Melsonian Arts Council. This project provides a data structure for the system but does not include the complete game text. Please support the original creators by buying the official Troika! rulebook.
