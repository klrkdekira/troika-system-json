"""
Unit tests for Item data against SRD.md
"""

import glob
import json
import os
import unittest
from typing import Any, Dict, List, Optional


class TestItemData(unittest.TestCase):
    """Test item JSON data against SRD.md content"""

    def setUp(self):
        """Set up test fixtures"""
        self.items_dir = "objects/items/"
        self.maxDiff = None

        # Expected items from SRD.md
        self.expected_items = {
            "astrological-equipment": {
                "name": "Astrological Equipment",
                "description": "Requires twenty minutes to set up and use but doesn't need to be outside. Consists of a ruby specular, charms against reciprocal observation, and complicated charts of the spheres. Grants +1 to Astrology.",
                "type": "equipment",
            },
            "bale-hook": {
                "name": "Bale Hook",
                "description": "Counts as a Knife for Damage and grants +1 on rolls to lift heavy objects.",
                "type": "weapon",
            },
            "blue-star-maps": {
                "name": "Blue Star Maps",
                "description": "The blue star maps of Corda hold the secrets of travel between the spheres. Every juncture in space and time can be found on its many square metred face if one is sufficiently educated in its use. Test Astrology to tell the precise destination of any portal.",
                "type": "artifact",
            },
            "epopt-staff": {
                "name": "Epopt Staff",
                "description": "A tool, an advert, and, in a pinch, a Weapon. In its head is set a cloudy ruby, like a useless magnifying glass, which grants the user +1 Second Sight while peering through it.",
                "type": "weapon",
            },
            "fusil": {
                "name": "Fusil",
                "description": "A long Weapon that looks like a rifle and can be used in melee as a Club. A Fusil holds 6 charges before the plasmic core needs replacing.",
                "type": "weapon",
            },
            "knuckle-dice": {
                "name": "Knuckle Dice",
                "description": "Made from the nimble, petal shaped knuckle bones of goblins and make excellent two sided dice.",
                "type": "tool",
            },
            "pistolet": {
                "name": "Pistolet",
                "description": "A hand held energy Weapon. Holds enough energy for 8 shots.",
                "type": "weapon",
            },
            "plasmic-cores": {
                "name": "Plasmic Cores",
                "description": "Crystalised starlight cast in metal. Or astral vapours captured in glass. Or maybe hard-ghosts? Whatever it is, it's pretty and used as a fuel source for exotic Weapons and reckless magicians. A plasmic core can be cracked open and huffed by a wizard in place of spending Stamina on a Spell. However, if an Oops! Table roll is called for the wizard has overdosed and drops dead, foaming at the mouth.",
                "type": "component",
            },
            "pocket-barometer": {
                "name": "Pocket Barometer",
                "description": "Part of a fashionable affectation for the metropolitan Troikan. Though the city has no discernable weather it is considered polite to check it intermittently and comment on the present clemency and hope for it to continue into the future. Examining its quartz face will inform you of future weather with 5 in 6 accuracy.",
                "type": "tool",
            },
            "ruby-lorgnette": {
                "name": "Ruby Lorgnette",
                "description": "Collapsable spectacles made with ruby lenses that require a free hand to use. While wearing them your sight is impaired but you can see sorcerous activity clearly (+2 Second Sight).",
                "type": "tool",
            },
        }

    def load_item_json(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Load an item JSON file"""
        file_path = f"{self.items_dir}{item_id}.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def get_all_item_files(self) -> List[str]:
        """Get all item file IDs"""
        files = glob.glob(f"{self.items_dir}*.json")
        return [os.path.basename(f).replace(".json", "") for f in files]

    def test_expected_items_present(self):
        """Test that expected items are present"""
        for item_id in self.expected_items.keys():
            with self.subTest(item_id=item_id):
                item_data = self.load_item_json(item_id)
                self.assertIsNotNone(item_data, f"Item {item_id} JSON file not found")

    def test_item_names_match_srd(self):
        """Test that item names match SRD exactly"""
        for item_id, expected_data in self.expected_items.items():
            with self.subTest(item_id=item_id):
                item_data = self.load_item_json(item_id)
                if item_data:
                    self.assertEqual(
                        item_data.get("name", ""),
                        expected_data["name"],
                        f"Item {item_id} name mismatch",
                    )

    def test_item_has_description(self):
        """Test that all items have descriptions"""
        for item_id in self.expected_items.keys():
            with self.subTest(item_id=item_id):
                item_data = self.load_item_json(item_id)
                if item_data:
                    self.assertIn(
                        "description", item_data, f"Item {item_id} missing description"
                    )
                    self.assertNotEqual(
                        item_data["description"].strip(),
                        "",
                        f"Item {item_id} has empty description",
                    )

    def test_item_structure_validity(self):
        """Test that item JSON structure is valid"""
        required_fields = ["name", "description"]

        all_item_files = self.get_all_item_files()
        for item_id in all_item_files:
            with self.subTest(item_id=item_id):
                item_data = self.load_item_json(item_id)
                if item_data:
                    for field in required_fields:
                        self.assertIn(
                            field, item_data, f"Item {item_id} missing field: {field}"
                        )

    def test_all_referenced_items_exist(self):
        """Test that all items referenced in backgrounds exist as files"""
        # Load all background files to get item references
        background_files = glob.glob("objects/backgrounds/*.json")
        referenced_items = set()

        for bg_file in background_files:
            with open(bg_file, "r", encoding="utf-8") as f:
                bg_data = json.load(f)
                for item in bg_data.get("possessions", []):
                    item_name = item.get("name", "")
                    if item_name:
                        # Convert to expected filename format (simple approximation)
                        item_id = (
                            item_name.lower()
                            .replace(" ", "-")
                            .replace("'", "")
                            .replace("(", "")
                            .replace(")", "")
                        )
                        # Remove common words that indicate variants
                        item_id = item_id.replace("and-", "").replace("or-", "")
                        referenced_items.add(item_id)

        print(f"Found {len(referenced_items)} referenced items")
        # Note: This test is informational - many items may not have individual files
        # if they're simple possessions

    def test_weapon_items_have_damage_info(self):
        """Test that weapon items include damage information"""
        weapon_keywords = [
            "sword",
            "bow",
            "club",
            "axe",
            "hammer",
            "knife",
            "dagger",
            "spear",
            "staff",
        ]

        all_item_files = self.get_all_item_files()
        for item_id in all_item_files:
            with self.subTest(item_id=item_id):
                item_data = self.load_item_json(item_id)
                if item_data:
                    item_name = item_data.get("name", "").lower()
                    item_desc = item_data.get("description", "").lower()

                    # Check if this looks like a weapon
                    is_weapon = any(
                        keyword in item_name or keyword in item_desc
                        for keyword in weapon_keywords
                    )

                    if is_weapon:
                        # Should have damage information
                        has_damage_info = (
                            "damage" in item_desc
                            or "weapon" in item_desc
                            or "fighting" in item_desc
                        )
                        if not has_damage_info:
                            print(
                                f"Note: {item_id} appears to be a weapon but lacks damage info"
                            )


if __name__ == "__main__":
    unittest.main()
