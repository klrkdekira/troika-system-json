"""
Unit tests for Character data in objects/characters/
"""

import glob
import json
import os
import unittest
from typing import Any


class TestCharacterData(unittest.TestCase):
    """Test character JSON data structures and requirements"""

    def setUp(self):
        """Set up test fixtures"""
        self.characters_dir = "objects/characters/"
        self.maxDiff = None

    def load_character_json(self, char_id: str) -> dict[str, Any] | None:
        """Load a character JSON file"""
        file_path = f"{self.characters_dir}{char_id}.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def get_all_character_files(self) -> list[str]:
        """Get all character file IDs"""
        files = glob.glob(f"{self.characters_dir}*.json")
        return [os.path.basename(f).replace(".json", "") for f in files]

    def test_character_files_exist(self):
        """Test that sample character files exist"""
        all_char_files = self.get_all_character_files()
        self.assertGreater(len(all_char_files), 0, "No character JSON files found")

    def test_character_structure_validity(self):
        """Test that character JSON structure meets required fields"""
        required_fields = [
            "name",
            "background",
            "attributes",
            "advancedSkills",
            "inventory",
        ]

        all_char_files = self.get_all_character_files()
        for char_id in all_char_files:
            with self.subTest(char_id=char_id):
                char_data = self.load_character_json(char_id)
                self.assertIsNotNone(char_data, f"Character {char_id} file not found")

                if char_data:
                    for field in required_fields:
                        self.assertIn(
                            field,
                            char_data,
                            f"Character {char_id} missing required field: {field}",
                        )

                    # Check attributes
                    attrs = char_data["attributes"]
                    self.assertIn("skill", attrs)
                    self.assertIn("stamina", attrs)
                    self.assertIn("luck", attrs)

                    self.assertIsInstance(attrs["skill"], int)
                    self.assertGreaterEqual(attrs["skill"], 4)
                    self.assertLessEqual(attrs["skill"], 6)

                    stamina = attrs["stamina"]
                    self.assertIn("current", stamina)
                    self.assertIn("maximum", stamina)
                    self.assertGreaterEqual(stamina["maximum"], 14)
                    self.assertLessEqual(stamina["maximum"], 24)

                    luck = attrs["luck"]
                    self.assertIn("current", luck)
                    self.assertIn("maximum", luck)
                    self.assertGreaterEqual(luck["maximum"], 7)
                    self.assertLessEqual(luck["maximum"], 12)

                    # Check inventory
                    inventory = char_data["inventory"]
                    self.assertIsInstance(inventory, list)
                    self.assertLessEqual(len(inventory), 18)


if __name__ == "__main__":
    unittest.main()
