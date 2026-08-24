"""
Unit tests for JSON-LD semantic linking and context completeness
"""

import json
import unittest
from pathlib import Path


class TestJsonLdData(unittest.TestCase):
    """Test JSON-LD context, @id URIs, and @type declarations across objects"""

    def setUp(self):
        """Set up test fixtures"""
        self.objects_dir = Path("objects")
        self.context_file = Path("systems/context.jsonld")
        self.base_uri = "https://cheeleong.dev/troika-system-json"
        self.maxDiff = None

        self.expected_types = {
            "backgrounds": "Background",
            "characters": "Character",
            "enemies": "Enemy",
            "items": "Item",
            "skills": "Skill",
            "spells": "Spell",
            "tables": "Table",
        }

    def test_context_file_exists_and_valid(self):
        """Test that systems/context.jsonld exists and defines @context"""
        self.assertTrue(self.context_file.exists(), "Context file missing")
        with open(self.context_file, "r", encoding="utf-8") as f:
            context_data = json.load(f)

        self.assertIn("@context", context_data)
        ctx = context_data["@context"]
        self.assertIn("@vocab", ctx)
        self.assertIn("Background", ctx)
        self.assertIn("Enemy", ctx)
        self.assertIn("Item", ctx)
        self.assertIn("Skill", ctx)
        self.assertIn("Spell", ctx)
        self.assertIn("Table", ctx)
        self.assertIn("Character", ctx)
        self.assertIn("TroikaSystemData", ctx)
        self.assertIn("CollectionIndex", ctx)
        self.assertIn("SearchIndex", ctx)

    def test_all_objects_have_jsonld_fields(self):
        """Test that every data object in objects/ contains @context, @id, and @type"""
        json_files = list(self.objects_dir.glob("**/*.json"))
        self.assertGreater(len(json_files), 0, "No JSON object files found")

        for json_file in json_files:
            rel_path = str(json_file)
            with self.subTest(file=rel_path):
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                self.assertIn("@context", data, f"Missing @context in {rel_path}")
                self.assertIn("@id", data, f"Missing @id in {rel_path}")
                self.assertIn("@type", data, f"Missing @type in {rel_path}")

                self.assertTrue(
                    data["@context"].endswith("context.jsonld"),
                    f"Invalid @context URL in {rel_path}",
                )
                self.assertTrue(
                    data["@id"].startswith(self.base_uri),
                    f"Invalid @id URI prefix in {rel_path}",
                )

    def test_all_object_ids_map_to_filesystem(self):
        """Test that all @id URIs map to existing JSON files on disk"""
        json_files = list(self.objects_dir.glob("**/*.json"))
        for json_file in json_files:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            uri = data.get("@id", "")
            if uri.startswith(self.base_uri + "/objects/"):
                rel_part = uri.removeprefix(self.base_uri + "/objects/")
                expected_file = self.objects_dir / rel_part
                self.assertTrue(
                    expected_file.exists(),
                    f"@id '{uri}' in {json_file} does not resolve to {expected_file}",
                )

    def test_index_html_embedded_jsonld(self):
        """Test that index.html contains valid Schema.org Dataset metadata"""
        import re

        index_file = Path("index.html")
        self.assertTrue(index_file.exists(), "index.html missing")
        content = index_file.read_text(encoding="utf-8")
        match = re.search(
            r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
            content,
            re.DOTALL,
        )
        self.assertIsNotNone(match, "No application/ld+json script in index.html")
        meta = json.loads(match.group(1))
        self.assertEqual(meta.get("@context"), "https://schema.org")
        self.assertEqual(meta.get("@type"), "Dataset")
        self.assertEqual(meta.get("name"), "Troika! System JSON")
        self.assertIn("distribution", meta)
        self.assertGreaterEqual(len(meta["distribution"]), 3)

    def test_object_jsonld_types_match_categories(self):
        """Test that @type matches the directory category"""
        for category, expected_type in self.expected_types.items():
            cat_dir = self.objects_dir / category
            if not cat_dir.exists():
                continue

            for json_file in cat_dir.glob("*.json"):
                rel_path = str(json_file)
                with self.subTest(file=rel_path):
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    self.assertEqual(
                        data.get("@type"),
                        expected_type,
                        f"Type mismatch in {rel_path}",
                    )


if __name__ == "__main__":
    unittest.main()
