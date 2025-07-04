# Troika! System JSON

<p align="center">
  <strong>🚧 WORK IN PROGRESS 🚧</strong><br>
  <em>This project is actively being developed and data may be incomplete or subject to change.</em>
</p>

A comprehensive JSON data structure for the Troika! tabletop RPG system, providing structured access to all game content including backgrounds, enemies, items, skills, spells, and tables.

## 📁 Directory Structure

```
troika-system-json/
├── README.md                    # This file
├── pyproject.toml              # Python project configuration
├── main.py                     # Main application entry point
├── LICENSE                     # Project license
├── fortle.svg                  # Project logo
├── srd.md                      # System Reference Document
├── analysis.md                 # Project analysis documentation
├── srd-*.md                    # SRD mapping and progress reports
├── COMPLETION-REPORT.md        # Project completion status
├── objects/                    # Game data JSON files
│   ├── troika-system-data.json # Main data aggregation file
│   ├── backgrounds/            # Character backgrounds (36 files)
│   │   ├── 11-ardent-giant-of-corda.json
│   │   ├── 12-befouler-of-ponds.json
│   │   ├── 13-burglar.json
│   │   └── ... (33 more backgrounds)
│   ├── enemies/                # Bestiary entries (36 files)
│   │   ├── alzabo.json
│   │   ├── boggart.json
│   │   ├── dragon.json
│   │   └── ... (33 more enemies)
│   ├── items/                  # Equipment and items (50 files)
│   │   ├── astrological-equipment.json
│   │   ├── axe.json
│   │   ├── bale-hook.json
│   │   └── ... (47 more items)
│   ├── skills/                 # Character skills (18 files)
│   │   └── ... (various skill definitions)
│   ├── spells/                 # Magic spells (74 files)
│   │   ├── cockroach.json
│   │   ├── jolt.json
│   │   ├── languages.json
│   │   └── ... (71 more spells)
│   └── tables/                 # Random tables (5 files)
│       └── ... (various game tables)
└── systems/                    # JSON schemas
    ├── troika-system.schema.json
    ├── background.schema.json
    ├── character.schema.json
    ├── enemy.schema.json
    ├── item.schema.json
    ├── skill.schema.json
    ├── spell.schema.json
    └── table.schema.json
```

## 📊 Data Summary

- **Total JSON Files**: 220+ game data files
- **Backgrounds**: 36 unique character backgrounds (d66 table)
- **Enemies**: 36 creature entries for the bestiary
- **Items**: 50 equipment and artifact entries
- **Skills**: 18 advanced skill definitions
- **Spells**: 74 magical spells and effects
- **Tables**: 5 random generation tables
- **Schemas**: 8 JSON schema files for validation

## 🎯 Features

- **Structured Data**: All Troika! content organized in machine-readable JSON format
- **JSON Schema Validation**: Complete schema definitions for all data types
- **Modular Design**: Individual files for each game element
- **Reference System**: Main data file uses JSON references for organization
- **Standards Compliant**: Follows JSON standards for maximum compatibility

## 🚀 Usage

### Main Data File

The primary entry point is `objects/troika-system-data.json`, which aggregates all game content using JSON references:

```json
{
    "metadata": {
        "version": "1.0",
        "name": "Troika!",
        "description": "Science Fantasy RPG System Data",
        "publisher": "Melsonian Arts Council",
        "license": "Third Party Compatible - see Terms in SRD"
    },
    "characterCreation": {
        "skillGeneration": "1d3+3",
        "staminaGeneration": "2d6+12",
        "luckGeneration": "1d6+6",
        "baselinePossessions": [...]
    },
    "backgrounds": [...],
    "enemies": [...],
    "items": [...],
    "skills": [...],
    "spells": [...],
    "tables": [...]
}
```

### Individual Components

Each game element is stored in its own JSON file with a consistent structure:

- **Backgrounds**: Character creation options with skills and possessions
- **Enemies**: Bestiary entries with stats and special abilities
- **Items**: Equipment with mechanical effects and descriptions
- **Skills**: Advanced skills with test mechanics
- **Spells**: Magic with costs and effects
- **Tables**: Random generation content

## 🏗️ Development Status

This project is actively being developed with the following progress:

- ✅ Core data structure defined
- ✅ JSON schemas created
- ✅ Background data (36/36 complete)
- ✅ Enemy data (36/36 complete)
- ✅ Item data (50/50 complete)
- ✅ Spell data (74/74 complete)
- ✅ Basic skill data (18/18 complete)
- ✅ Table data (5/5 complete)
- 🔄 Data validation and testing
- 🔄 API development
- 🔄 Documentation completion

## 📜 License & Attribution

<p align="center">
  <img src="fortle.svg" alt="Fortle Logo" width="200" height="200">
</p>

This project is based on the **Troika!** tabletop RPG system by the **Melsonian Arts Council**.

### Third Party Compatibility

This is an independent production and is not affiliated with the Melsonian Arts Council. It is published under the terms outlined in the Troika! System Reference Document (SRD).

**Troika! System JSON is an independent production by Chee Leong and is not affiliated with the Melsonian Arts Council.**

### Terms of Use

- The mechanics and concepts of "Troika!" are used under the terms of the SRD
- This data structure may be used freely for compatible projects
- Original game content remains copyright of the Melsonian Arts Council
- See `srd.md` for complete licensing terms

### Original Work

"Troika!" is a trademark of the Melsonian Arts Council. This project provides a data structure for the system but does not include the complete game text. Please support the original creators by purchasing the official Troika! rulebook.

## 🤝 Contributing

This project is under active development. Contributions are welcome for:

- Data validation and error correction
- Schema improvements
- Documentation enhancements
- Tool development for data consumption
