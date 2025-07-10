#!/usr/bin/env python3
"""
Script to find all "X_silver" values in JSON files and convert them to integer values.

This script will:
1. Recursively search through the objects/ directory for JSON files
2. Find all "value" fields containing patterns like "2_silver", "25_silver", etc.
3. Convert these string values to integer values (e.g., "2_silver" -> 2)
4. Update the JSON files with the converted values
5. Provide a summary of all changes made
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple


def find_json_files(directory: str) -> List[Path]:
    """Find all JSON files in the given directory and subdirectories."""
    directory_path = Path(directory)
    return list(directory_path.rglob("*.json"))


def convert_silver_value(value: Any) -> Tuple[Any, bool]:
    """
    Convert a value if it matches the X_silver pattern.

    Args:
        value: The value to potentially convert

    Returns:
        Tuple of (converted_value, was_changed)
    """
    if isinstance(value, str):
        # Look for pattern like "2_silver", "25_silver", etc.
        match = re.match(r"^(\d+)_silver$", value)
        if match:
            return int(match.group(1)), True
    return value, False


def process_json_object(obj: Any, path: str = "") -> Tuple[Any, List[str]]:
    """
    Recursively process a JSON object to find and convert silver values.

    Args:
        obj: The JSON object to process
        path: Current path in the object (for logging)

    Returns:
        Tuple of (processed_object, list_of_changes)
    """
    changes = []

    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key

            if key == "value":
                # Check if this is a value field that needs conversion
                new_value, was_changed = convert_silver_value(value)
                if was_changed:
                    changes.append(f"{current_path}: '{value}' -> {new_value}")
                new_obj[key] = new_value
            else:
                # Recursively process other fields
                new_obj[key], nested_changes = process_json_object(value, current_path)
                changes.extend(nested_changes)
        return new_obj, changes

    elif isinstance(obj, list):
        new_list = []
        for i, item in enumerate(obj):
            current_path = f"{path}[{i}]"
            new_item, nested_changes = process_json_object(item, current_path)
            new_list.append(new_item)
            changes.extend(nested_changes)
        return new_list, changes

    else:
        # For primitive values, just return as-is
        return obj, []


def process_json_file(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Process a single JSON file to convert silver values.

    Args:
        file_path: Path to the JSON file

    Returns:
        Tuple of (file_was_modified, list_of_changes)
    """
    try:
        # Read the file
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Process the data
        new_data, changes = process_json_object(data)

        # Write back if there were changes
        if changes:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(new_data, f, indent=2, ensure_ascii=False)
            return True, changes

        return False, []

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, []


def main():
    """Main function to run the conversion script."""
    print("Silver Value Converter")
    print("=" * 50)
    print("Looking for JSON files with 'X_silver' value patterns...")
    print()

    # Find all JSON files in the objects directory
    json_files = find_json_files("objects")
    print(f"Found {len(json_files)} JSON files to process")
    print()

    total_files_modified = 0
    total_changes = 0
    all_changes = {}

    # Process each file
    for file_path in json_files:
        file_modified, changes = process_json_file(file_path)

        if file_modified:
            total_files_modified += 1
            total_changes += len(changes)
            all_changes[str(file_path)] = changes

            print(f"✅ Modified: {file_path}")
            for change in changes:
                print(f"   {change}")
            print()

    # Summary
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Files processed: {len(json_files)}")
    print(f"Files modified: {total_files_modified}")
    print(f"Total conversions: {total_changes}")
    print()

    if all_changes:
        print("All changes made:")
        for file_path, changes in all_changes.items():
            print(f"\n{file_path}:")
            for change in changes:
                print(f"  - {change}")
    else:
        print("No files needed modification.")


if __name__ == "__main__":
    main()
