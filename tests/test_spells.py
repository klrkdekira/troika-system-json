"""
Unit tests for Spell data against SRD.md
"""

import glob
import json
import os
import unittest
from typing import Any, Dict, List, Optional


class TestSpellData(unittest.TestCase):
    """Test spell JSON data against SRD.md content"""

    def setUp(self):
        """Set up test fixtures"""
        self.spells_dir = "objects/spells/"
        self.maxDiff = None

        # Expected spells from SRD.md (partial list for testing)
        self.expected_spells = {
            "affix": {
                "name": "Affix",
                "cost": 3,
                "description": "Cause a subject to be fixed in place. While they are so held they do not move, breathe, fall, perspire, acquire, or otherwise change. They are totally immune to harm, in fact. Lasts for 3 minutes.",
            },
            "amity": {
                "name": "Amity",
                "cost": 4,
                "description": "The College of Friends always sends out its Factotums on nights after Amity classes. Clearing out the bars and brothels of their drunken apprentices is tiring work. Use of this Spell causes the target to Test their Luck (or Skill for Enemies) or become very friendly towards the wizard, as though they were an old friend. They will not act irrationally, though, and if they were already a bit of a boor this might not change much.",
            },
            "animate": {
                "name": "Animate",
                "cost": 2,
                "description": "Cause inanimate objects to question their place. One object up to the size of a human baby may be caused to hop around and do whatever else the wizard wishes.",
            },
            "assassins-dagger": {
                "name": "Assassin's Dagger",
                "cost": 3,
                "description": "Evocatively named but actually quite mundane. The wizard whispers to an object and that object then seeks out and vigorously and repeatedly bumps into the desired target. Obviously if you whisper to a poisoned dagger the result is one thing while doing it to a letter is another. Travels any distance and always arrives (eventually).",
            },
            "assume-shape": {
                "name": "Assume Shape",
                "cost": 4,
                "description": "The wizard undergoes a distressing transformation into an inanimate object no larger than a piano and no smaller than a cup. Lasts until ended.",
            },
            "astral-reach": {
                "name": "Astral Reach",
                "cost": 1,
                "description": "The Sorcerers of the Academy of Doors are most famous for this one Spell. With it they may reach through any portal and into another known receptacle. For example they might use it to reach through to a safe in their manse via their purse. This Spell only allows partial translocation— the wizard cannot fully or permanently enter.",
            },
            "babble": {
                "name": "Babble",
                "cost": 2,
                "description": "The wizard speaks nonsense while watching the intended target, causing their words to trip and confuse. This may be done under their breath and relatively subtly.",
            },
            "banish-spirit": {
                "name": "Banish Spirit",
                "cost": 6,
                "description": "The wizard explains, clearly, sternly, why it is impossible that the spirit could be here at this time. The spirit must Test its Luck (or Skill for Enemies) or be sent to somewhere less improbable.",
            },
            "befuddle": {
                "name": "Befuddle",
                "cost": 1,
                "description": "A wizard's touch can shake up someone's mind like a snow globe. The target makes all rolls at a -1 penalty until their head clears. Lasts for 3 minutes.",
            },
            "blood-shroud": {
                "name": "Blood Shroud",
                "cost": 4,
                "description": "Smear a small amount of a demon's blood on yourself to become completely invisible to them, even if you attack or speak to them, for 6 hours.",
            },
        }

    def load_spell_json(self, spell_id: str) -> Optional[Dict[str, Any]]:
        """Load a spell JSON file"""
        file_path = f"{self.spells_dir}{spell_id}.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def get_all_spell_files(self) -> List[str]:
        """Get all spell file IDs"""
        files = glob.glob(f"{self.spells_dir}*.json")
        return [os.path.basename(f).replace(".json", "") for f in files]

    def test_expected_spells_present(self):
        """Test that expected spells are present"""
        for spell_id in self.expected_spells.keys():
            with self.subTest(spell_id=spell_id):
                spell_data = self.load_spell_json(spell_id)
                self.assertIsNotNone(
                    spell_data, f"Spell {spell_id} JSON file not found"
                )

    def test_spell_names_match_srd(self):
        """Test that spell names match SRD exactly"""
        for spell_id, expected_data in self.expected_spells.items():
            with self.subTest(spell_id=spell_id):
                spell_data = self.load_spell_json(spell_id)
                if spell_data:
                    self.assertEqual(
                        spell_data.get("name", ""),
                        expected_data["name"],
                        f"Spell {spell_id} name mismatch",
                    )

    def test_spell_costs_match_srd(self):
        """Test that spell costs match SRD exactly"""
        for spell_id, expected_data in self.expected_spells.items():
            with self.subTest(spell_id=spell_id):
                spell_data = self.load_spell_json(spell_id)
                if spell_data:
                    self.assertEqual(
                        spell_data.get("cost", 0),
                        expected_data["cost"],
                        f"Spell {spell_id} cost mismatch",
                    )

    def test_spell_has_description(self):
        """Test that all spells have descriptions"""
        for spell_id in self.expected_spells.keys():
            with self.subTest(spell_id=spell_id):
                spell_data = self.load_spell_json(spell_id)
                if spell_data:
                    self.assertIn(
                        "description",
                        spell_data,
                        f"Spell {spell_id} missing description",
                    )
                    self.assertNotEqual(
                        spell_data["description"].strip(),
                        "",
                        f"Spell {spell_id} has empty description",
                    )

    def test_spell_structure_validity(self):
        """Test that spell JSON structure is valid"""
        required_fields = ["name", "cost", "description"]

        all_spell_files = self.get_all_spell_files()
        for spell_id in all_spell_files:
            with self.subTest(spell_id=spell_id):
                spell_data = self.load_spell_json(spell_id)
                if spell_data:
                    for field in required_fields:
                        self.assertIn(
                            field,
                            spell_data,
                            f"Spell {spell_id} missing field: {field}",
                        )

    def test_spell_cost_is_positive_integer(self):
        """Test that spell costs are positive integers"""
        all_spell_files = self.get_all_spell_files()
        # Special cases with non-integer costs
        special_cost_spells = {"undo", "zed"}

        for spell_id in all_spell_files:
            with self.subTest(spell_id=spell_id):
                spell_data = self.load_spell_json(spell_id)
                if spell_data:
                    cost = spell_data.get("cost", 0)

                    if spell_id in special_cost_spells:
                        # Special spells can have non-integer costs
                        self.assertIsInstance(
                            cost,
                            (int, str),
                            f"Spell {spell_id} cost must be integer or string",
                        )
                        if isinstance(cost, str):
                            self.assertGreater(
                                len(cost),
                                0,
                                f"Spell {spell_id} cost string cannot be empty",
                            )
                    else:
                        # Regular spells must have integer costs
                        self.assertIsInstance(
                            cost, int, f"Spell {spell_id} cost must be integer"
                        )
                        self.assertGreater(
                            cost, 0, f"Spell {spell_id} cost must be positive"
                        )

    def test_all_referenced_spells_exist(self):
        """Test that all spells referenced in backgrounds exist as files"""
        # Load all background files to get spell references
        background_files = glob.glob("objects/backgrounds/*.json")
        referenced_spells = set()

        for bg_file in background_files:
            with open(bg_file, "r", encoding="utf-8") as f:
                bg_data = json.load(f)
                for spell in bg_data.get("spells", []):
                    spell_name = spell.get("name", "")
                    if spell_name and spell_name != "Random":
                        # Convert to expected filename format
                        spell_id = spell_name.lower().replace(" ", "-").replace("'", "")
                        referenced_spells.add(spell_id)

        # Check that all referenced spells have files
        for spell_id in referenced_spells:
            with self.subTest(spell_id=spell_id):
                spell_data = self.load_spell_json(spell_id)
                self.assertIsNotNone(
                    spell_data, f"Referenced spell {spell_id} has no JSON file"
                )


if __name__ == "__main__":
    unittest.main()
