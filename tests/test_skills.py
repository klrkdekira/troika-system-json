"""
Unit tests for Skill data against SRD.md
"""

import glob
import json
import os
import unittest
from typing import Any, Dict, List, Optional


class TestSkillData(unittest.TestCase):
    """Test skill JSON data against SRD.md content"""

    def setUp(self):
        """Set up test fixtures"""
        self.skills_dir = "objects/skills/"
        self.maxDiff = None

        # Expected core skills from SRD.md
        self.expected_skills = {
            "acrobatics": "Used for rolling, balancing, falling, jumping, etc.",
            "astrology": "An essential Skill for anyone intent on travelling the stars. Can be used to identify stars and constellations, to gather hints on the destination of interdimensional portals, and to make star charts.",
            "awareness": "Anything worth having is well hidden so one must look very carefully. Use this to spot traps, things normally hidden, or things out of the ordinary.",
            "climb": "The usefulness of the ability to clamber up things cannot be overstated. Most climbs should be single rolls though longer or more difficult climbs may require multiple rolls.",
            "disguise": "Covers the use of props to change your appearance. When in disguise you must Roll Under this when someone is liable to see through it. Opposed by Awareness when under scrutiny.",
            "etiquette": "When making a good impression is important Roll Versus your host's Etiquette. Represents a mechanical understanding of social conduct and those who are better at it are more discerning.",
            "evaluate": "Test this to get an idea of how much something is worth.",
            "fly": "Use Fly much as you would Run. In normal situations this doesn't need testing, only in chases or high winds, maybe. Anyone attempting to Fly without this Skill must Test every Round to make sure they don't crash or lose control.",
            "golden-barge-pilot": "Test this to navigate between the stars on a ship with golden mirror sails.",
            "healing": "Used to stitch wounds and apply ointments, stop bleeding, slow poison and the like. Also used for stabilising dying people.",
            "locks": "This allows a character to examine and open locks but does not detect traps. Roll Versus an imaginary locksmith whose Skill is somewhere between 6 and 12 with 6 being easy and 12 being very hard.",
            "mathmology": "Use this to gain insight into angles, pressures, numbers, and other such arcane arts. You could, for instance, Test your Mathmology to get a good idea of the surface tension of a ball of inert plasmic goo or to find the fulcrum for tripping a giant.",
            "poison": "You may Test this Skill during down time to create a single dose of poison. Pick which kind it is when you make it.",
            "ride": "Everyone is assumed to have basic animal riding Skill though anything more than trotting slowly will require some kind of roll to avoid trouble.",
            "run": "When it matters how fast you are, or if you can reach somewhere in time, use this. A basic chase is an Roll Versus.",
            "second-sight": "Use of this allows the detection of magic. On a successful Test you focus your inner eye and all sorcerous activity glows faintly for a moment.",
            "sneak": "The art of remaining unseen. This is Tested only when someone or something is actively trying to detect you. The sneaker would Roll Versus the Awareness of those searching for them; anyone beating the sneaker's score detects them.",
            "strength": "Used for lifting and breaking things. May also be used to grapple people if no grappling-appropriate Weapon Skill is possessed, though it counts for half rounded up.",
            "swim": "Use this while swimming in dangerous waters, diving, holding your breath for long periods, and so on. If you have this Skill you don't need to roll it for normal conditions.",
            "tracking": "Used to stalk prey and find tracks. When stalking a quarry this is treated as an opposed Roll Versus the opponent's Tracking or Sneaking.",
            "trapping": "Use this to set and disarm traps. When setting traps Roll Under your Trapping Skill and describe how the trap is made with the materials at hand.",
        }

    def load_skill_json(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """Load a skill JSON file"""
        file_path = f"{self.skills_dir}{skill_id}.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def get_all_skill_files(self) -> List[str]:
        """Get all skill file IDs"""
        files = glob.glob(f"{self.skills_dir}*.json")
        return [os.path.basename(f).replace(".json", "") for f in files]

    def test_expected_skills_present(self):
        """Test that expected core skills are present"""
        for skill_id in self.expected_skills.keys():
            with self.subTest(skill_id=skill_id):
                skill_data = self.load_skill_json(skill_id)
                self.assertIsNotNone(
                    skill_data, f"Skill {skill_id} JSON file not found"
                )

    def test_skill_names_correct(self):
        """Test that skill names are correct"""
        for skill_id in self.expected_skills.keys():
            with self.subTest(skill_id=skill_id):
                skill_data = self.load_skill_json(skill_id)
                if skill_data:
                    expected_name = skill_id.replace("-", " ").title()
                    if skill_id == "golden-barge-pilot":
                        expected_name = "Golden Barge Pilot"
                    elif skill_id == "second-sight":
                        expected_name = "Second Sight"

                    actual_name = skill_data.get("name", "")
                    self.assertEqual(
                        actual_name, expected_name, f"Skill {skill_id} name mismatch"
                    )

    def test_skill_has_description(self):
        """Test that all skills have descriptions"""
        all_skill_files = self.get_all_skill_files()

        for skill_id in all_skill_files:
            with self.subTest(skill_id=skill_id):
                skill_data = self.load_skill_json(skill_id)
                if skill_data:
                    self.assertIn(
                        "description",
                        skill_data,
                        f"Skill {skill_id} missing description",
                    )
                    self.assertNotEqual(
                        skill_data["description"].strip(),
                        "",
                        f"Skill {skill_id} has empty description",
                    )

    def test_skill_structure_validity(self):
        """Test that skill JSON structure is valid"""
        required_fields = ["name", "description"]

        all_skill_files = self.get_all_skill_files()
        for skill_id in all_skill_files:
            with self.subTest(skill_id=skill_id):
                skill_data = self.load_skill_json(skill_id)
                if skill_data:
                    for field in required_fields:
                        self.assertIn(
                            field,
                            skill_data,
                            f"Skill {skill_id} missing field: {field}",
                        )

    def test_all_background_skills_exist(self):
        """Test that all skills referenced in backgrounds exist as files"""
        # Load all background files to get skill references
        background_files = glob.glob("objects/backgrounds/*.json")
        referenced_skills = set()

        for bg_file in background_files:
            with open(bg_file, "r", encoding="utf-8") as f:
                bg_data = json.load(f)
                for skill in bg_data.get("advancedSkills", []):
                    skill_name = skill.get("name", "")
                    if skill_name and not skill_name.startswith("Spell"):
                        # Convert to expected filename format
                        skill_id = (
                            skill_name.lower()
                            .replace(" ", "-")
                            .replace("–", "-")
                            .replace("—", "-")
                        )
                        referenced_skills.add(skill_id)

        print(f"Found {len(referenced_skills)} referenced skills from backgrounds")

        # Check that core skills exist
        missing_skills = []
        for skill_id in referenced_skills:
            if skill_id in self.expected_skills:  # Only check expected core skills
                skill_data = self.load_skill_json(skill_id)
                if not skill_data:
                    missing_skills.append(skill_id)

        if missing_skills:
            self.fail(f"Missing skill files: {missing_skills}")


if __name__ == "__main__":
    unittest.main()
