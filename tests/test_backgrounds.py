"""
Unit tests for Background data against SRD.md
"""

import glob
import json
import unittest
from typing import Any, Dict, Optional


class TestBackgroundData(unittest.TestCase):
    """Test background JSON data against SRD.md content"""

    def setUp(self):
        """Set up test fixtures"""
        self.backgrounds_dir = "objects/backgrounds/"
        self.maxDiff = None

        # Expected backgrounds from SRD.md
        self.expected_backgrounds = {
            11: {
                "name": "Ardent Giant of Corda",
                "skills": [("Strength", 4), ("Astrology", 3), ("Run", 2), ("Climb", 2)],
                "spells": [],
                "possessions": ["Artefact of Lost Corda"],
                "special": [],
            },
            12: {
                "name": "Befouler of Ponds",
                "skills": [("Swim", 3), ("Sneak", 1), ("Second Sight", 1)],
                "spells": [
                    ("Drown", 3),
                    ("Tongue Twister", 2),
                    ("Undo", 2),
                    ("Web", 1),
                ],
                "possessions": ["Sackcloth Robes", "Large, Worn Wooden Ladle"],
                "special": [
                    "You never contract disease as a result of drinking stagnant liquids."
                ],
            },
            13: {
                "name": "Burglar",
                "skills": [
                    ("Sneak", 2),
                    ("Locks", 2),
                    ("Awareness", 1),
                    ("Climb", 1),
                    ("Trapping", 1),
                    ("Knife Fighting", 1),
                    ("Crossbow Fighting", 1),
                ],
                "spells": [],
                "possessions": [
                    "Crossbow and 18 Bolts",
                    "Roll of Lock Picks",
                    "Grappling Hook",
                ],
                "special": [
                    "You may Test your Luck to find and get in with the local criminal underbelly if one exists."
                ],
            },
            14: {
                "name": "Cacogen",
                "skills": [
                    ("Fusil Fighting", 2),
                    ("Astrology", 2),
                    ("Second Sight", 2),
                    ("Golden Barge Pilot", 2),
                    ("Sword Fighting", 1),
                ],
                "spells": [("Random", 2), ("Random", 2), ("Random", 1)],
                "possessions": ["Fusil", "2d6 Plasmic Cores", "Sword", "Velare"],
                "special": [],
            },
            15: {
                "name": "Chaos Champion",
                "skills": [
                    ("Language – Kurgan", 6),
                    ("Maul Fighting", 3),
                    ("Secret Signs – Chaos Patron", 3),
                    ("Second Sight", 1),
                ],
                "spells": [("Random", 1)],
                "possessions": [
                    "Ritual Scars",
                    "Huge Maul",
                    "Assortment of Ragged Armour",
                    "Dream Journal",
                ],
                "special": [
                    "Name your patron. You may call upon your patron for aid once per day. To do so roll three 6s on 3d6. The GM interprets their intervention."
                ],
            },
            16: {
                "name": "Claviger",
                "skills": [
                    ("Locks", 4),
                    ("Strength", 3),
                    ("Trapping", 3),
                    ("Maul Fighting", 1),
                ],
                "spells": [("Open", 2), ("See Through", 1), ("Lock", 1)],
                "possessions": [
                    "Festooned with Keys",
                    "Distinguished Sledgehammer",
                    "Lock Picking Tools",
                ],
                "special": [],
            },
            21: {
                "name": "Demon Stalker",
                "skills": [
                    ("Language – Abyssal", 5),
                    ("Second Sight", 2),
                    ("Sword Fighting", 2),
                    ("Bow Fighting", 2),
                    ("Tracking", 1),
                    ("Sneak", 1),
                ],
                "spells": [("Blood Shroud", 3)],
                "possessions": [
                    "Silver Sword",
                    "16 Silver Arrows and Bow",
                    "Pouch of Salt",
                    "Vial of Demon Blood",
                ],
                "special": [],
            },
            22: {
                "name": "Dwarf",
                "skills": [
                    ("Awareness", 3),
                    ("Sculpting", 2),
                    ("Painting", 2),
                    ("Metalworking", 2),
                    ("Construction", 2),
                    ("Strength", 2),
                    ("Fist Fighting", 2),
                    ("Wrestling", 2),
                    ("Hammer Fighting", 1),
                ],
                "spells": [],
                "possessions": ["Masonry Hammer", "Roll of Artist's Supplies"],
                "special": [
                    "Dwarfs may eat gems and rare metals as food replacements. You, in fact, vastly prefer the taste of rare minerals to mundane food."
                ],
            },
            23: {
                "name": "Epopt",
                "skills": [
                    ("Awareness", 2),
                    ("Evaluate", 2),
                    ("Second Sight", 1),
                    ("Etiquette", 1),
                    ("Fist Fighting", 1),
                    ("Run", 1),
                ],
                "spells": [],
                "possessions": [
                    "Yellow Epopt Outfit",
                    "Epopt Staff",
                    "Collapsible Tent",
                ],
                "special": [
                    "Epopts may Test their Luck to get a yes or no answer to a question about mundane matters. The GM should make this Test in private, not informing the Epopt if their visions are accurate."
                ],
            },
            24: {
                "name": "Exographer",
                "skills": [
                    ("Exography", 4),
                    ("Golden Barge Pilot", 3),
                    ("Astrology", 2),
                    ("Pistolet Fighting", 2),
                ],
                "spells": [],
                "possessions": [
                    "Hermetically Sealed Rubber Suit",
                    "Exographical Surveyors Box",
                    "Spring-Loaded Measuring Tape",
                    "Pistolet",
                    "1d6 Plasmic Cores",
                ],
                "special": [],
            },
            25: {
                "name": "The Fellowship of Knidos",
                "skills": [("Mathmology", 3), ("Astrology", 2)],
                "spells": [("Find", 2)],
                "possessions": [
                    "Large Astrolabe",
                    "Abacus",
                    "Lots of Scrolls and Writing Equipment",
                ],
                "special": [],
            },
            26: {
                "name": "Fellow of the Peerage of Porters & Basin Fillers",
                "skills": [
                    ("Strength", 4),
                    ("Fist Fighting", 2),
                    ("Run", 2),
                    ("Hook Fighting", 1),
                    ("Sneak", 1),
                    ("Awareness", 1),
                ],
                "spells": [],
                "possessions": [
                    "Wooden Yoke",
                    "Brown Overcoat and Soft Doffing Cap",
                    "Bale Hook",
                    "Length of Rope",
                ],
                "special": [],
            },
            31: {
                "name": "Gremlin Catcher",
                "skills": [
                    ("Tunnel Fighting", 4),
                    ("Trapping", 4),
                    ("Sneak", 2),
                    ("Awareness", 2),
                    ("Club Fighting", 2),
                    ("Tracking", 2),
                    ("Swim", 1),
                ],
                "spells": [],
                "possessions": [
                    "Small but Vicious Dog",
                    "Flat Cap",
                    "A Club",
                    "A Sack",
                    "1d6 Empty Gremlin Jars",
                    "A Jar with a Pissed-off Gremlin Inside",
                ],
                "special": [],
            },
            32: {
                "name": "Journeyman of the Guild of Sharp Corners",
                "skills": [
                    ("Poison", 1),
                    ("Sneak", 1),
                    ("Locks", 1),
                    ("Knife Fighting", 1),
                    ("Climb", 1),
                    ("Awareness", 1),
                    ("Crossbow Fighting", 1),
                    ("Swim", 1),
                    ("Disguise", 1),
                ],
                "spells": [],
                "possessions": [
                    "Black Clothes of the Apprentice",
                    "Garrotte",
                    "Curved Sword",
                    "3 Vials of Poison",
                    "Crossbow and 6 Bolts",
                ],
                "special": [],
            },
            33: {
                "name": "Lansquenet",
                "skills": [
                    ("Greatsword Fighting", 2),
                    ("Pistolet Fighting", 2),
                    ("Run", 1),
                    ("Fist Fighting", 1),
                    ("Astrology", 1),
                ],
                "spells": [],
                "possessions": [
                    "Exquisite Pistolet",
                    "Bandolier containing 18 Plasmic Cores",
                    "Greatsword",
                    "Brightly Coloured Clothing",
                ],
                "special": [],
            },
            34: {
                "name": "Lonesome Monarch",
                "skills": [("Etiquette", 3), ("Tracking", 1), ("Ride", 3)],
                "spells": [],
                "possessions": ["Nice Weapon of your choice", "Crown", "Tired Horse"],
                "special": [],
            },
            35: {
                "name": "Member of Miss Kinsey's Dining Club",
                "skills": [
                    ("Etiquette", 3),
                    ("Strength", 1),
                    ("Tracking", 1),
                    ("Trapping", 1),
                    ("Gastrology", 1),
                ],
                "spells": [],
                "possessions": ["Sharp metal dentures", "Embroidered napkin"],
                "special": [
                    "Eaters are immune to mundane ingested poisons. They may also identify any object if eaten, gaining knowledge of its material, its origin (if plausibly familiar), and its magical properties on a successful Test of Gastrology though the object must be thoroughly masticated, not merely swallowed and passed. This does not grant special immunity to any effects the object may possess."
                ],
            },
            36: {
                "name": "Monkeymonger",
                "skills": [
                    ("Climb", 4),
                    ("Trapping", 2),
                    ("Club Fighting", 1),
                    ("Knife Fighting", 1),
                ],
                "spells": [],
                "possessions": [
                    "Monkey Club",
                    "Butcher's Knife",
                    "1d6 Small Monkeys",
                    "A Pocket Full of Monkey Treats",
                ],
                "special": [
                    "The GM may choose to roll on this table anytime the Mien of monkeys must be determined: 1 Playful, 2 Stalking, 3 Hungry, 4 Tired, 5 Austere, 6 Aggressive"
                ],
            },
            41: {
                "name": "Necromancer",
                "skills": [
                    ("Healing", 2),
                    ("Mortuary Science", 2),
                    ("Relationship Counseling", 2),
                    ("Sneak", 1),
                ],
                "spells": [
                    ("Posthumous Vitality", 1),
                    ("Skeletal Counsel", 1),
                    ("Torpor", 1),
                ],
                "possessions": [
                    "Dusty Robes",
                    "Skull of your Master or Zombie Servant or Ghost",
                ],
                "special": [],
            },
            42: {
                "name": "Parchment Witch",
                "skills": [("Disguise", 2), ("Second Sight", 2), ("Healing", 1)],
                "spells": [
                    ("Protection From Rain", 2),
                    ("Callous Strike", 2),
                    ("Quench", 2),
                    ("True Seeing", 2),
                    ("Undo", 1),
                    ("Random", 1),
                ],
                "possessions": [
                    "d6 Rolls of Parchment",
                    "Vials of Pigments and Powders",
                    "Collection of Brushes",
                    "Sword Cane",
                ],
                "special": [
                    "You are undead and so do not need to breathe or circulate blood. You take double Damage from Silver Weapons and regain Stamina half as effectively from all sources. You must Test your Luck if outside in the rain, are made wet, are close to open flames, or suffer generally grievous wounds. A failure will see your skin ruined. If your skin is compromised you are very obviously a walking corpse."
                ],
            },
            43: {
                "name": "Derivative Dwarf",
                "skills": [
                    ("Fist Fighting", 3),
                    ("Awareness", 3),
                    ("Strength", 2),
                    ("Wrestling", 2),
                    ("Axe Fighting", 2),
                ],
                "spells": [],
                "possessions": ["Woodsman's Axe", "Empty Firkin"],
                "special": [
                    "As 22 Dwarf but additionally:",
                    "To non-Dwarfy eyes you look like any other Dwarf. Only Dwarfs can see the derivative or uninspired parts of your creation. Other Dwarfs will completely ignore you since you remind them of their fading novelty. You have +4 Sneak versus Dwarfs.",
                ],
            },
            44: {
                "name": "Questing Knight",
                "skills": [
                    ("Jousting", 3),
                    ("Sword Fighting", 2),
                    ("Spear Fighting", 2),
                    ("Shield Fighting", 1),
                    ("Awareness", 1),
                ],
                "spells": [],
                "possessions": [
                    "Heavy Armour",
                    "Horse",
                    "Lance",
                    "Sword",
                    "Shield",
                    "Quixotic Undertaking",
                ],
                "special": [],
            },
            45: {
                "name": "Red Priest",
                "skills": [("Great Axe Fighting", 2), ("Second Sight", 1)],
                "spells": [
                    ("Ember", 2),
                    ("Fire Bolt", 2),
                    ("Flash", 2),
                    ("Exorcism", 1),
                ],
                "possessions": [
                    "Red Robes",
                    "Traditional Faceless Metal Helmet of your order",
                    "Symbolic (but fully sized and fully functional) Single Headed Greataxe, to help batter down the door to sin",
                ],
                "special": [],
            },
            46: {
                "name": "Rhino-Man",
                "skills": [
                    ("Spear Fighting", 3),
                    ("Run", 2),
                    ("Strength", 2),
                    ("Gambling", 1),
                ],
                "spells": [],
                "possessions": [
                    "Horn",
                    "Thick Skin",
                    "Undersized Spear",
                    "Tiny, Useless Helmet",
                    "Knuckle Dice",
                    "Half Full Firkin of Rhino-beer",
                ],
                "special": [],
            },
            51: {
                "name": "Sceptical Lamassu",
                "skills": [("Fly", 3), ("Claw Fighting", 2), ("Hoof Fighting", 1)],
                "spells": [("Random", 3), ("Random", 3), ("Random", 3)],
                "possessions": [
                    "Incidental Sacred Jewellery",
                    "Pillbox Hat",
                    "Claws",
                    "Hooves",
                    "Wings",
                ],
                "special": [],
            },
            52: {
                "name": "Sorcerer of the Academy of Doors",
                "skills": [("Astrology", 3), ("Second Sight", 2)],
                "spells": [
                    ("Astral Reach", 2),
                    ("Teleport", 1),
                    ("Web", 1),
                    ("Random", 1),
                    ("Random", 1),
                    ("Random", 1),
                ],
                "possessions": ["Small Functional Door", "Flashy Robes"],
                "special": [],
            },
            53: {
                "name": "Sorcerer of the College of Friends",
                "skills": [
                    ("Secret Signs – Witching Words", 4),
                    ("Run", 2),
                    ("Climb", 1),
                    ("Sleight of Hand", 1),
                    ("Swim", 1),
                    ("Sneak", 1),
                    ("Second Sight", 1),
                ],
                "spells": [
                    ("Jolt", 1),
                    ("Amity", 1),
                    ("Mirror Selves", 1),
                    ("Protection from Rain", 1),
                    ("Helping Hands", 1),
                    ("Purple Lens", 1),
                    ("Random", 1),
                ],
                "possessions": [
                    "Pointed Wizard Hat",
                    "Pocket Full of Wizard Biscuits",
                    "Wand",
                ],
                "special": [],
            },
            54: {
                "name": "Fellow of The Sublime Society of Beef Steaks",
                "skills": [
                    ("Wrestling", 2),
                    ("Swim", 2),
                    ("Climb", 2),
                    ("Run", 2),
                    ("Fist Fighting", 2),
                    ("Grilling", 1),
                ],
                "spells": [],
                "possessions": [
                    "Weapon of your choice",
                    "Small Gridiron",
                    "2kg of Premium Meat Cuts",
                    "Waistcoat",
                    "Bottle of Strong but Fancy Wine",
                ],
                "special": [],
            },
            55: {
                "name": "Temple Knight of Telak the Swordbringer",
                "skills": [
                    ("Awareness", 3),
                    ("Blacksmithing", 2),
                    ("Sword Fighting", 1),
                    ("Greatsword Fighting", 1),
                ],
                "spells": [],
                "possessions": ["Blessing of Telak", "6 Swords of your choice"],
                "special": [
                    "The blessing of Telak awards you Armour equal to half (rounded down) the number of Swords you carry. If you carried 6 Swords your Armour would be 3 while if you carried 9 it would be 4. You must be overtly armed at all times or else Telak will take this blessing away until you forge and donate to the unarmed a brand new Sword."
                ],
            },
            56: {
                "name": "Thaumaturge",
                "skills": [("Second Sight", 1), ("Astrology", 1)],
                "spells": [
                    ("Undo", 3),
                    ("Assume Shape", 2),
                    ("Thunder", 2),
                    ("Random", 2),
                    ("Brittle Twigs", 1),
                    ("Random", 1),
                ],
                "possessions": [
                    "Thaumaturgic Fez",
                    "Staff",
                    "Curled Shoes",
                    "Voluminous Robes",
                ],
                "special": [
                    "You may Test your Luck to just so happen to have exactly the (common) mystic tchotchke, bauble, or gewgaw the situation requires."
                ],
            },
            61: {
                "name": "Thinking Engine",
                "skills": [
                    ("Golden Barge Pilot", 3),
                    ("Astrology", 2),
                    ("Pistolet Fighting", 2),
                    ("Healing", 2),
                    ("Run", 1),
                    ("Strength", 1),
                    ("Cooking", 1),
                ],
                "spells": [],
                "possessions": [
                    "Soldering iron",
                    "Detachable autonomous hands or centaur body (+4 Run) or inbuilt particle detector (+4 Second Sight) or one random Spell at rank 3",
                ],
                "special": [
                    "You don't recover Stamina by resting in the usual manner — instead you must spend a full rest period with a hot iron welding your skin back together like putty. For each hour of rest with access to the right tools you regain 3 Stamina.",
                    "You may recharge plasmic machines by hooking your fluids to them and spending Stamina at a rate of 1 Stamina and 6 minutes per charge.",
                    "You always count as being at least Lightly Armoured.",
                ],
            },
            62: {
                "name": "Vengeful Child",
                "skills": [
                    ("Longsword Fighting", 3),
                    ("Awareness", 1),
                    ("Climb", 1),
                    ("Bow Fighting", 1),
                    ("Run", 1),
                    ("Swim", 1),
                    ("Vengeance", 1),
                ],
                "spells": [],
                "possessions": ["Too-Large Sword", "Old Hunting Bow and 12 Arrows"],
                "special": [],
            },
            63: {
                "name": "Venturesome Academic",
                "skills": [
                    ("Evaluate", 2),
                    ("Astrology", 2),
                    ("Healing", 1),
                    ("Sword Fighting", 1),
                    ("Sleight of Hand", 1),
                ],
                "spells": [("Random", 1)],
                "possessions": [
                    "Reading Glasses",
                    "Small Sword",
                    "Bundle of Candles and Matches",
                    "Writing materials",
                    "Journal",
                ],
                "special": [
                    "You may Test your Luck to recall facts that you might reasonably be expected to have encountered relating to the natural sciences and humanities."
                ],
            },
            64: {
                "name": "Wizard Hunter",
                "skills": [
                    ("Tracking", 2),
                    ("Disguise", 2),
                    ("Crossbow Fighting", 2),
                    ("Sword Fighting", 1),
                    ("Sneak", 1),
                    ("Locks", 1),
                    ("Etiquette", 1),
                ],
                "spells": [],
                "possessions": [
                    "Large Sack",
                    "Witch-hair Rope",
                    "Crossbow and 12 Bolts",
                    "Sword",
                    "1d6 Pocket Gods",
                    "Ruby Lorgnette",
                ],
                "special": [],
            },
            65: {
                "name": "Yongardy Lawyer",
                "skills": [("Etiquette", 2), ("Healing", 1)],
                "spells": [],
                "possessions": [
                    "Rapier (Damage as Sword) and Puffy Shirt or Sjambok (Damage as Club) and Lots of Scars or Longsword and Heavy Armour or Hammer and Gargantuan Shield",
                    "Manual on Yongardy Law",
                    "Barrister's Wig",
                ],
                "special": [
                    "Choose weapon combination when creating character - gain 4 points in that Fighting skill"
                ],
            },
            66: {
                "name": "Zoanthrop",
                "skills": [
                    ("Climb", 3),
                    ("Run", 3),
                    ("Strength", 2),
                    ("Fist Fighting", 2),
                    ("Club Fighting", 2),
                    ("Wrestling", 2),
                ],
                "spells": [],
                "possessions": [],
                "special": [
                    "You are immune to all mind altering effects. You are able to speak but usually choose not to. When making Advancement Checks for Skills related to abstract thought, such as Spells or Astrology, you must roll twice and succeed on both to improve them."
                ],
            },
        }

    def load_background_json(self, background_id: int) -> Optional[Dict[str, Any]]:
        """Load a background JSON file"""
        file_pattern = f"{self.backgrounds_dir}{background_id}-*.json"
        files = glob.glob(file_pattern)
        if not files:
            return None

        with open(files[0], "r", encoding="utf-8") as f:
            return json.load(f)

    def test_all_backgrounds_present(self):
        """Test that all 36 backgrounds are present"""
        for bg_id in self.expected_backgrounds.keys():
            with self.subTest(background_id=bg_id):
                bg_data = self.load_background_json(bg_id)
                self.assertIsNotNone(bg_data, f"Background {bg_id} JSON file not found")

    def test_background_names_match_srd(self):
        """Test that background names match SRD exactly"""
        for bg_id, expected_data in self.expected_backgrounds.items():
            with self.subTest(background_id=bg_id):
                bg_data = self.load_background_json(bg_id)
                if bg_data:
                    self.assertEqual(
                        bg_data.get("name", ""),
                        expected_data["name"],
                        f"Background {bg_id} name mismatch",
                    )

    def test_background_skills_match_srd(self):
        """Test that background skills match SRD exactly"""
        for bg_id, expected_data in self.expected_backgrounds.items():
            with self.subTest(background_id=bg_id):
                bg_data = self.load_background_json(bg_id)
                if bg_data:
                    # Extract skills from JSON
                    actual_skills = {
                        skill["name"]: skill["rank"]
                        for skill in bg_data.get("advancedSkills", [])
                    }
                    expected_skills = {
                        skill[0]: skill[1] for skill in expected_data["skills"]
                    }

                    # Check each expected skill
                    for skill_name, expected_rank in expected_skills.items():
                        self.assertIn(
                            skill_name,
                            actual_skills,
                            f"Background {bg_id} missing skill: {skill_name}",
                        )
                        self.assertEqual(
                            actual_skills[skill_name],
                            expected_rank,
                            f"Background {bg_id} skill {skill_name} rank mismatch",
                        )

    def test_background_spells_match_srd(self):
        """Test that background spells match SRD exactly"""
        for bg_id, expected_data in self.expected_backgrounds.items():
            with self.subTest(background_id=bg_id):
                bg_data = self.load_background_json(bg_id)
                if bg_data:
                    # Extract spells from JSON
                    actual_spells = {
                        spell["name"]: spell["rank"]
                        for spell in bg_data.get("spells", [])
                    }
                    expected_spells = {
                        spell[0]: spell[1] for spell in expected_data["spells"]
                    }

                    # Check each expected spell
                    for spell_name, expected_rank in expected_spells.items():
                        self.assertIn(
                            spell_name,
                            actual_spells,
                            f"Background {bg_id} missing spell: {spell_name}",
                        )
                        self.assertEqual(
                            actual_spells[spell_name],
                            expected_rank,
                            f"Background {bg_id} spell {spell_name} rank mismatch",
                        )

    def test_background_possessions_present(self):
        """Test that background possessions are present"""
        for bg_id, expected_data in self.expected_backgrounds.items():
            with self.subTest(background_id=bg_id):
                bg_data = self.load_background_json(bg_id)
                if bg_data:
                    actual_possessions = [
                        item["name"] for item in bg_data.get("possessions", [])
                    ]
                    expected_possessions = expected_data["possessions"]

                    self.assertEqual(
                        len(actual_possessions),
                        len(expected_possessions),
                        f"Background {bg_id} possession count mismatch",
                    )

                    # Check that expected possessions are present (allowing for variations in naming)
                    for expected_item in expected_possessions:
                        found = any(
                            expected_item.lower() in actual_item.lower()
                            or actual_item.lower() in expected_item.lower()
                            for actual_item in actual_possessions
                        )
                        self.assertTrue(
                            found,
                            f"Background {bg_id} missing possession: {expected_item}",
                        )

    def test_background_special_abilities_present(self):
        """Test that background special abilities are present"""
        for bg_id, expected_data in self.expected_backgrounds.items():
            with self.subTest(background_id=bg_id):
                bg_data = self.load_background_json(bg_id)
                if bg_data:
                    actual_special = bg_data.get("special", [])
                    expected_special = expected_data["special"]

                    self.assertEqual(
                        len(actual_special),
                        len(expected_special),
                        f"Background {bg_id} special abilities count mismatch",
                    )

    def test_background_has_description(self):
        """Test that all backgrounds have descriptions"""
        for bg_id in self.expected_backgrounds.keys():
            with self.subTest(background_id=bg_id):
                bg_data = self.load_background_json(bg_id)
                if bg_data:
                    self.assertIn(
                        "description",
                        bg_data,
                        f"Background {bg_id} missing description",
                    )
                    self.assertNotEqual(
                        bg_data["description"].strip(),
                        "",
                        f"Background {bg_id} has empty description",
                    )

    def test_background_structure_validity(self):
        """Test that background JSON structure is valid"""
        required_fields = [
            "id",
            "name",
            "description",
            "possessions",
            "advancedSkills",
            "spells",
            "special",
        ]

        for bg_id in self.expected_backgrounds.keys():
            with self.subTest(background_id=bg_id):
                bg_data = self.load_background_json(bg_id)
                if bg_data:
                    for field in required_fields:
                        self.assertIn(
                            field, bg_data, f"Background {bg_id} missing field: {field}"
                        )

                    # Check that ID matches filename
                    self.assertEqual(
                        bg_data["id"], bg_id, f"Background {bg_id} ID mismatch"
                    )


if __name__ == "__main__":
    unittest.main()
