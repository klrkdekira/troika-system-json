"""
Unit tests for Table data in objects/tables/
"""

import glob
import json
import os
import unittest
from typing import Any


class TestTableData(unittest.TestCase):
    """Test table JSON data structures and requirements"""

    def setUp(self):
        """Set up test fixtures"""
        self.tables_dir = "objects/tables/"
        self.maxDiff = None

        self.expected_tables = [
            "beastly-damage-table",
            "melee-damage-table",
            "oops-table",
            "random-spell-table",
            "ranged-damage-table",
        ]

    def load_table_json(self, table_id: str) -> dict[str, Any] | None:
        """Load a table JSON file"""
        file_path = f"{self.tables_dir}{table_id}.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def get_all_table_files(self) -> list[str]:
        """Get all table file IDs"""
        files = glob.glob(f"{self.tables_dir}*.json")
        return [os.path.basename(f).replace(".json", "") for f in files]

    def test_expected_tables_present(self):
        """Test that all expected table files exist"""
        for table_id in self.expected_tables:
            with self.subTest(table_id=table_id):
                table_data = self.load_table_json(table_id)
                self.assertIsNotNone(
                    table_data, f"Table {table_id} JSON file not found"
                )

    def test_table_structure_validity(self):
        """Test that table JSON structure is valid"""
        required_fields = ["name", "type"]

        all_table_files = self.get_all_table_files()
        self.assertEqual(
            len(all_table_files),
            len(self.expected_tables),
            "Table file count mismatch",
        )

        for table_id in all_table_files:
            with self.subTest(table_id=table_id):
                table_data = self.load_table_json(table_id)
                self.assertIsNotNone(table_data, f"Table {table_id} file not found")

                if table_data:
                    for field in required_fields:
                        self.assertIn(
                            field,
                            table_data,
                            f"Table {table_id} missing required field: {field}",
                        )

                    table_type = table_data["type"]
                    self.assertIn(
                        table_type,
                        [
                            "damage",
                            "random",
                            "lookup",
                            "roll",
                            "oops",
                            "background",
                            "mien",
                            "success",
                        ],
                        f"Table {table_id} has invalid type: {table_type}",
                    )

    def test_damage_tables_matrix_structure(self):
        """Test damage table matrix structure"""
        damage_tables = [
            "beastly-damage-table",
            "melee-damage-table",
            "ranged-damage-table",
        ]

        for table_id in damage_tables:
            with self.subTest(table_id=table_id):
                table_data = self.load_table_json(table_id)
                if table_data:
                    self.assertEqual(table_data["type"], "damage")
                    self.assertIn("damageMatrix", table_data)

                    matrix_data = table_data["damageMatrix"]
                    self.assertIn("weapons", matrix_data)
                    self.assertIn("rollColumns", matrix_data)
                    self.assertIn("matrix", matrix_data)

                    weapons = matrix_data["weapons"]
                    matrix = matrix_data["matrix"]

                    for weapon in weapons:
                        self.assertIn(
                            weapon,
                            matrix,
                            f"Weapon {weapon} listed in weapons but missing in matrix for {table_id}",
                        )
                        for col in matrix_data["rollColumns"]:
                            self.assertIn(
                                col,
                                matrix[weapon],
                                f"Missing roll column {col} for weapon {weapon} in {table_id}",
                            )

    def test_roll_tables_entries_structure(self):
        """Test roll tables entry structure"""
        roll_tables = ["oops-table", "random-spell-table"]

        for table_id in roll_tables:
            with self.subTest(table_id=table_id):
                table_data = self.load_table_json(table_id)
                if table_data:
                    self.assertIn("entries", table_data)
                    entries = table_data["entries"]
                    self.assertIsInstance(entries, list)
                    self.assertGreater(len(entries), 0)

                    for entry in entries:
                        self.assertIn("roll", entry)
                        self.assertIn("result", entry)


if __name__ == "__main__":
    unittest.main()
