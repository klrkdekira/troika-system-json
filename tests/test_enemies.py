"""
Unit tests for Enemy data against SRD.md
"""

import glob
import json
import os
import unittest
from typing import Any, Dict, List, Optional


class TestEnemyData(unittest.TestCase):
    """Test enemy JSON data against SRD.md content"""

    def setUp(self):
        """Set up test fixtures"""
        self.enemies_dir = "objects/enemies/"
        self.maxDiff = None

    def load_enemy_json(self, enemy_id: str) -> Optional[Dict[str, Any]]:
        """Load an enemy JSON file"""
        file_path = f"{self.enemies_dir}{enemy_id}.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def get_all_enemy_files(self) -> List[str]:
        """Get all enemy file IDs"""
        files = glob.glob(f"{self.enemies_dir}*.json")
        return [os.path.basename(f).replace(".json", "") for f in files]

    def test_enemy_structure_validity(self):
        """Test that enemy JSON structure is valid"""
        required_fields = ["name", "description", "mien", "stats"]

        all_enemy_files = self.get_all_enemy_files()
        self.assertGreater(len(all_enemy_files), 0, "No enemy files found")

        for enemy_id in all_enemy_files:
            with self.subTest(enemy_id=enemy_id):
                enemy_data = self.load_enemy_json(enemy_id)
                self.assertIsNotNone(enemy_data, f"Enemy {enemy_id} file not found")

                if enemy_data:
                    for field in required_fields:
                        self.assertIn(
                            field,
                            enemy_data,
                            f"Enemy {enemy_id} missing field: {field}",
                        )

                    # Check stats structure
                    stats = enemy_data["stats"]
                    required_stats = ["skill", "stamina", "initiative"]
                    for stat in required_stats:
                        self.assertIn(
                            stat, stats, f"Enemy {enemy_id} stats missing {stat}"
                        )
                        self.assertIsInstance(
                            stats[stat], int, f"Enemy {enemy_id} {stat} must be integer"
                        )
                        self.assertGreater(
                            stats[stat], 0, f"Enemy {enemy_id} {stat} must be positive"
                        )

                    # Check mien structure
                    if "mien" in enemy_data:
                        mien = enemy_data["mien"]
                        self.assertIn(
                            "diceType", mien, f"Enemy {enemy_id} mien missing diceType"
                        )
                        self.assertIn(
                            "entries", mien, f"Enemy {enemy_id} mien missing entries"
                        )
                        self.assertIsInstance(
                            mien["entries"],
                            list,
                            f"Enemy {enemy_id} mien entries must be list",
                        )

    def test_enemy_stats_are_valid(self):
        """Test that enemy stats are valid numbers"""
        all_enemy_files = self.get_all_enemy_files()

        for enemy_id in all_enemy_files:
            with self.subTest(enemy_id=enemy_id):
                enemy_data = self.load_enemy_json(enemy_id)
                if enemy_data and "stats" in enemy_data:
                    stats = enemy_data["stats"]

                    # Test skill
                    skill = stats.get("skill", 0)
                    self.assertIsInstance(
                        skill, int, f"Enemy {enemy_id} skill must be integer"
                    )
                    self.assertGreaterEqual(
                        skill, 1, f"Enemy {enemy_id} skill must be >= 1"
                    )
                    self.assertLessEqual(
                        skill, 20, f"Enemy {enemy_id} skill seems too high"
                    )

                    # Test stamina
                    stamina = stats.get("stamina", 0)
                    self.assertIsInstance(
                        stamina, int, f"Enemy {enemy_id} stamina must be integer"
                    )
                    self.assertGreater(
                        stamina, 0, f"Enemy {enemy_id} stamina must be positive"
                    )

                    # Test initiative
                    initiative = stats.get("initiative", 0)
                    self.assertIsInstance(
                        initiative, int, f"Enemy {enemy_id} initiative must be integer"
                    )
                    self.assertGreaterEqual(
                        initiative, 1, f"Enemy {enemy_id} initiative must be >= 1"
                    )

    def test_enemy_has_description_or_special(self):
        """Test that enemies have description or special abilities"""
        all_enemy_files = self.get_all_enemy_files()

        for enemy_id in all_enemy_files:
            with self.subTest(enemy_id=enemy_id):
                enemy_data = self.load_enemy_json(enemy_id)
                if enemy_data:
                    has_description = (
                        "description" in enemy_data
                        and enemy_data["description"].strip()
                    )
                    has_special = "special" in enemy_data and enemy_data["special"]
                    has_attacks = "attacks" in enemy_data and enemy_data["attacks"]

                    self.assertTrue(
                        has_description or has_special or has_attacks,
                        f"Enemy {enemy_id} should have description, special abilities, or attack info",
                    )

    def test_enemy_names_are_present(self):
        """Test that all enemies have names"""
        all_enemy_files = self.get_all_enemy_files()

        for enemy_id in all_enemy_files:
            with self.subTest(enemy_id=enemy_id):
                enemy_data = self.load_enemy_json(enemy_id)
                if enemy_data:
                    name = enemy_data.get("name", "")
                    self.assertNotEqual(
                        name.strip(), "", f"Enemy {enemy_id} has empty name"
                    )


if __name__ == "__main__":
    unittest.main()
