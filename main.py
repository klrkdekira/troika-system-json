#!/usr/bin/env python3
"""
Troika System JSON Schema Validator

This script validates JSON objects against their corresponding schemas in the systems directory.
It supports validating individual files or entire directories, checking cross-references,
and validating bundled dataset files.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator, RefResolver
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class TroikaValidator:
    """JSON Schema validator for Troika system objects."""

    def __init__(self, schema_dir: Path | None = None):
        """Initialize validator with schema directory."""
        self.schema_dir = schema_dir or Path("systems")
        self.schemas: dict[str, Any] = {}
        self.schema_store: dict[str, Any] = {}
        self.console = Console()
        self.load_schemas()

    def load_schemas(self) -> None:
        """Load all schema files from the systems directory and build schema store."""
        if not self.schema_dir.exists():
            raise FileNotFoundError(f"Schema directory not found: {self.schema_dir}")

        schema_files = list(self.schema_dir.glob("*.schema.json"))
        if not schema_files:
            raise FileNotFoundError(f"No schema files found in {self.schema_dir}")

        for schema_file in schema_files:
            try:
                with open(schema_file, "r", encoding="utf-8") as f:
                    schema_data = json.load(f)
                    schema_id = schema_data.get(
                        "$id", schema_file.stem.replace(".schema", "")
                    )
                    self.schemas[schema_id] = schema_data

                    # Store mapping for RefResolver by ID and filename
                    self.schema_store[schema_id] = schema_data
                    self.schema_store[schema_file.name] = schema_data
                    if "$id" in schema_data:
                        self.schema_store[schema_data["$id"]] = schema_data

                    self.console.print(f"✓ Loaded schema: {schema_id}", style="green")
            except Exception as e:  # noqa: BLE001
                self.console.print(
                    f"✗ Failed to load schema {schema_file}: {e}", style="red"
                )

    def get_schema_for_object(self, obj_path: Path) -> str | None:
        """Determine which schema to use based on object path."""
        # Map directory names to schema IDs
        schema_mapping = {
            "backgrounds": "troika-background",
            "enemies": "troika-enemy",
            "items": "troika-item",
            "skills": "troika-skill",
            "spells": "troika-spell",
            "tables": "troika-table",
            "characters": "troika-character",
        }

        # Check if file is in a subdirectory that maps to a schema
        for parent in obj_path.parents:
            if parent.name in schema_mapping:
                return schema_mapping[parent.name]

        # Check if filename contains a hint
        filename = obj_path.name.lower()
        for schema_type, schema_id in schema_mapping.items():
            if schema_type in filename:
                return schema_id

        # Default to troika-system for top-level objects
        return "troika-system"

    def validate_object(
        self, obj_path: Path, schema_id: str | None = None
    ) -> dict[str, Any]:
        """Validate a single JSON object against its schema using RefResolver."""
        result: dict[str, Any] = {
            "file": str(obj_path),
            "valid": False,
            "errors": [],
            "schema_used": None,
        }

        try:
            # Load the JSON object
            with open(obj_path, "r", encoding="utf-8") as f:
                obj_data = json.load(f)

            # If validating unbundled master file with $ref pointers, expand refs in memory
            if obj_path.name == "troika-system-data.json" and isinstance(
                obj_data, dict
            ):
                obj_data = self._expand_file_refs(obj_data, obj_path.parent)

            # Determine schema to use
            if not schema_id:
                schema_id = self.get_schema_for_object(obj_path)

            if not schema_id or schema_id not in self.schemas:
                result["errors"].append(f"Schema '{schema_id}' not found")
                return result

            result["schema_used"] = schema_id
            schema = self.schemas[schema_id]

            # Create validator with RefResolver to resolve internal and external $ref pointers
            resolver = RefResolver.from_schema(schema, store=self.schema_store)
            validator = Draft7Validator(schema, resolver=resolver)
            errors = list(validator.iter_errors(obj_data))

            if errors:
                result["errors"].extend(
                    [
                        f"{error.message} at {'.'.join(str(p) for p in error.path)}"
                        for error in errors
                    ]
                )

            if not result["errors"]:
                result["valid"] = True

        except json.JSONDecodeError as e:
            result["errors"].append(f"Invalid JSON: {e}")
        except Exception as e:  # noqa: BLE001
            result["errors"].append(f"Validation error: {e}")

        return result

    def validate_directory(
        self, directory: Path, recursive: bool = True
    ) -> list[dict[str, Any]]:
        """Validate all JSON files in a directory."""
        results = []

        if not directory.exists():
            self.console.print(f"Directory not found: {directory}", style="red")
            return results

        # Find all JSON files
        pattern = "**/*.json" if recursive else "*.json"
        json_files = sorted(directory.glob(pattern))

        if not json_files:
            self.console.print(f"No JSON files found in {directory}", style="yellow")
            return results

        # Validate each file
        for json_file in json_files:
            result = self.validate_object(json_file)
            results.append(result)

        return results

    def validate_by_categories(self, objects_dir: Path) -> bool:
        """Validate objects by category (backgrounds, enemies, items, etc.) and return overall status."""
        categories = [
            "backgrounds",
            "characters",
            "enemies",
            "items",
            "skills",
            "spells",
            "tables",
        ]

        all_valid = True

        for category in categories:
            category_dir = objects_dir / category
            if category_dir.exists():
                self.console.print(f"\n[bold cyan]Validating {category}...[/bold cyan]")
                results = self.validate_directory(category_dir, recursive=False)
                invalid_count = self.print_validation_results(results)
                if invalid_count > 0:
                    all_valid = False
            else:
                self.console.print(
                    f"[yellow]Category directory not found: {category}[/yellow]"
                )

        # Validate top-level data files if present
        data_files = ["troika-system-data.json", "troika-system-data.bundled.json"]
        for df_name in data_files:
            main_data_file = objects_dir / df_name
            if main_data_file.exists():
                self.console.print(f"\n[bold cyan]Validating {df_name}...[/bold cyan]")
                result = self.validate_object(main_data_file)
                invalid_count = self.print_validation_results([result])
                if invalid_count > 0:
                    all_valid = False

        return all_valid

    def check_references(self, objects_dir: Path) -> bool:
        """Cross-check references across backgrounds, items, skills, and spells."""
        self.console.print(
            "\n[bold cyan]Cross-checking references across objects...[/bold cyan]"
        )

        items_dir = objects_dir / "items"
        skills_dir = objects_dir / "skills"
        spells_dir = objects_dir / "spells"
        items = {}
        if items_dir.exists():
            for p in items_dir.glob("*.json"):
                with open(p, "r", encoding="utf-8") as f:
                    items[json.load(f)["name"].lower()] = p.name

        skills = {}
        if skills_dir.exists():
            for p in skills_dir.glob("*.json"):
                with open(p, "r", encoding="utf-8") as f:
                    skills[json.load(f)["name"].lower()] = p.name

        spells = {}
        if spells_dir.exists():
            for p in spells_dir.glob("*.json"):
                with open(p, "r", encoding="utf-8") as f:
                    spells[json.load(f)["name"].lower()] = p.name

        table = Table(title="Reference Check Summary")
        table.add_column("Category", style="cyan")
        table.add_column("Total Defined Objects", style="bold green")
        table.add_column("Status", style="magenta")

        table.add_row("Items", str(len(items)), "✓ Complete" if items else "✗ None")
        table.add_row("Skills", str(len(skills)), "✓ Complete" if skills else "✗ None")
        table.add_row("Spells", str(len(spells)), "✓ Complete" if spells else "✗ None")

        self.console.print(table)
        return True

    def print_validation_results(self, results: list[dict[str, Any]]) -> int:
        """Print validation results in a formatted table and return invalid file count."""
        if not results:
            self.console.print("No validation results to display.", style="yellow")
            return 0

        # Create summary
        total_files = len(results)
        valid_files = sum(1 for r in results if r["valid"])
        invalid_files = total_files - valid_files

        # Print summary panel
        summary_text = f"Total files: {total_files}\n"
        summary_text += f"Valid: {valid_files}\n"
        summary_text += f"Invalid: {invalid_files}"

        summary_style = "green" if invalid_files == 0 else "red"
        self.console.print(
            Panel(summary_text, title="Validation Summary", style=summary_style)
        )

        # Create detailed results table
        table = Table(title="Validation Results")
        table.add_column("File", style="cyan", no_wrap=True)
        table.add_column("Status", style="bold")
        table.add_column("Schema", style="magenta")
        table.add_column("Errors", style="red")

        for result in results:
            status = "✓ Valid" if result["valid"] else "✗ Invalid"
            status_style = "green" if result["valid"] else "red"

            errors_text = "\n".join(result["errors"][:3])  # Show first 3 errors
            if len(result["errors"]) > 3:
                errors_text += f"\n... and {len(result['errors']) - 3} more"

            table.add_row(
                Path(result["file"]).name,
                Text(status, style=status_style),
                result["schema_used"] or "Unknown",
                errors_text or "",
            )

        self.console.print(table)
        return invalid_files

    def list_schemas(self) -> None:
        """List all available schemas."""
        table = Table(title="Available Schemas")
        table.add_column("Schema ID", style="cyan")
        table.add_column("Title", style="bold")
        table.add_column("Description", style="dim")

        for schema_id, schema_data in self.schemas.items():
            table.add_row(
                schema_id,
                schema_data.get("title", "No title"),
                schema_data.get("description", "No description"),
            )

        self.console.print(table)

    def _expand_file_refs(self, data: dict[str, Any], base_dir: Path) -> dict[str, Any]:
        """In-memory expansion of $ref pointers in master file for schema validation."""
        import copy

        expanded = copy.deepcopy(data)
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
            if cat in expanded and isinstance(expanded[cat], list):
                new_items = []
                for item in expanded[cat]:
                    if isinstance(item, dict) and "$ref" in item:
                        ref_str = item["$ref"].removeprefix("./")
                        ref_path = base_dir / ref_str
                        if ref_path.exists():
                            with open(ref_path, "r", encoding="utf-8") as rf:
                                new_items.append(json.load(rf))
                        else:
                            new_items.append(item)
                    else:
                        new_items.append(item)
                expanded[cat] = new_items
        return expanded


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate JSON objects against Troika system schemas"
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to JSON file or directory to validate (default: objects/)",
    )
    parser.add_argument(
        "--schema-dir",
        default="systems",
        help="Directory containing schema files (default: systems)",
    )
    parser.add_argument("--schema", help="Specific schema ID to use for validation")
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Recursively validate directories",
    )
    parser.add_argument(
        "--list-schemas", "-l", action="store_true", help="List all available schemas"
    )
    parser.add_argument(
        "--check-references",
        "-c",
        action="store_true",
        help="Check object cross-references",
    )

    args = parser.parse_args()

    try:
        # Initialize validator
        validator = TroikaValidator(Path(args.schema_dir))

        # List schemas if requested
        if args.list_schemas:
            validator.list_schemas()
            return

        target_path = Path(args.path) if args.path else Path("objects")

        if args.check_references:
            validator.check_references(target_path)
            return

        success = True
        if target_path.is_file():
            # Validate single file
            result = validator.validate_object(target_path, args.schema)
            invalid_count = validator.print_validation_results([result])
            if invalid_count > 0:
                success = False
        elif target_path.is_dir():
            # Validate directory
            if not args.path:
                # Default behavior: validate each category separately
                success = validator.validate_by_categories(target_path)
            else:
                results = validator.validate_directory(target_path, args.recursive)
                invalid_count = validator.print_validation_results(results)
                if invalid_count > 0:
                    success = False
        else:
            print(f"Error: Path '{target_path}' does not exist", file=sys.stderr)
            sys.exit(1)

        if not success:
            sys.exit(1)

    except Exception as e:  # noqa: BLE001
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
