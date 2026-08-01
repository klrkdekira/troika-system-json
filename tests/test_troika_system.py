"""
Unit tests for master troika-system-data.json manifest and $ref resolutions
"""

import json
import unittest
from pathlib import Path


class TestTroikaSystemData(unittest.TestCase):
    """Test troika-system-data.json structure and JSON reference resolution"""

    def setUp(self):
        """Set up test fixtures"""
        self.objects_dir = Path("objects")
        self.master_file = self.objects_dir / "troika-system-data.json"
        self.maxDiff = None

    def test_master_file_exists(self):
        """Test that objects/troika-system-data.json exists"""
        self.assertTrue(
            self.master_file.exists(),
            f"Master data file missing: {self.master_file}",
        )

    def test_master_file_valid_json(self):
        """Test that master file is valid JSON with required top-level metadata"""
        with open(self.master_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("version", data)
        self.assertIn("metadata", data)
        self.assertIn("title", data["metadata"])
        self.assertIn("rules", data)

    def test_all_ref_links_resolve(self):
        """Test that all $ref pointers resolve to existing files on disk"""
        with open(self.master_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        categories = ["backgrounds", "skills", "spells", "items", "enemies", "tables"]

        for category in categories:
            with self.subTest(category=category):
                self.assertIn(
                    category, data, f"Master data missing category: {category}"
                )
                items = data[category]
                self.assertIsInstance(items, list, f"{category} must be a list")
                self.assertGreater(len(items), 0, f"{category} array is empty")

                for index, item in enumerate(items):
                    self.assertIn(
                        "$ref",
                        item,
                        f"Item at index {index} in {category} missing '$ref'",
                    )
                    ref_path = item["$ref"]
                    target_file = (self.objects_dir / ref_path).resolve()
                    self.assertTrue(
                        target_file.exists(),
                        f"$ref pointer '{ref_path}' in {category}[{index}] points to non-existent file: {target_file}",
                    )

    def test_rules_structure(self):
        """Test top-level rules structure in master data"""
        with open(self.master_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        rules = data.get("rules", {})
        expected_rule_keys = [
            "coreRules",
            "initiative",
            "combat",
            "advancement",
            "encumbrance",
        ]

        for key in expected_rule_keys:
            with self.subTest(rule_key=key):
                self.assertIn(key, rules, f"Rules block missing '{key}'")

    def test_bundled_file_valid_and_inlined(self):
        """Test that objects/troika-system-data.bundled.json exists and has inlined objects"""
        bundled_file = self.objects_dir / "troika-system-data.bundled.json"
        self.assertTrue(
            bundled_file.exists(),
            f"Bundled data file missing: {bundled_file}",
        )
        with open(bundled_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("version", data)
        self.assertIn("metadata", data)

        categories = ["backgrounds", "skills", "spells", "items", "enemies", "tables", "characters"]
        for category in categories:
            with self.subTest(category=category):
                self.assertIn(category, data)
                items = data[category]
                self.assertIsInstance(items, list)
                self.assertGreater(len(items), 0)
                for index, item in enumerate(items):
                    self.assertNotIn(
                        "$ref",
                        item,
                        f"Bundled item at {category}[{index}] still contains '$ref'",
                    )
                    self.assertIn(
                        "name",
                        item,
                        f"Inlined item at {category}[{index}] missing 'name' field",
                    )


if __name__ == "__main__":
    unittest.main()

