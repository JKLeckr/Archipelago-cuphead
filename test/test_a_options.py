from typing import Dict, Any
from . import CupheadTestBase

# Borrowed from Hammerwatch (thx @Parcosmic)
class TestOptions(CupheadTestBase):
    option_dict: Dict[str, Dict[str, Any]] = {
        "Default options": {},
        "Freemove": {
            "freemove_isles": True,
        },
        "DLC": {
            "use_dlc": True,
            "mode": "dlc_beat_both",
        },
        "Ability Rando": {
            "randomize_abilities": True,
        },
        "Boss Secrets": {
            "boss_secret_checks": True,
        },
        "DLC Freemove": {
            "use_dlc": True,
            "mode": "dlc_beat_both",
            "freemove_isles": True,
        },
        "MacGuffin": {
            "mode": "collect_contracts",
        },
        "DLC MacGuffin": {
            "use_dlc": True,
            "mode": "dlc_collect_ingredients",
        },
        "DLC Collect Both": {
            "use_dlc": True,
            "mode": "dlc_collect_both",
        },
        "No Grade Checks": {
            "boss_grade_checks": "disabled",
            "rungun_grade_checks": "disabled",
        },
        "DLC No Grade Checks": {
            "use_dlc": True,
            "boss_grade_checks": "disabled",
            "rungun_grade_checks": "disabled",
        },
    }

    def test_options(self):
        for option_set, opts in self.option_dict.items():
            with self.subTest(option_set):
                test_world = TestOptions()
                test_world.options = opts
                test_world.world_setup()
                test_world._check_all_locations_are_active(option_set)

    def _check_all_locations_are_active(self, option_set_name: str):
        for player in self.multiworld.get_game_players(self.game):
            remaining_locs = {x for x,y in self.multiworld.worlds[player].active_locations.items() if y.id is not None}
            for region in self.multiworld.get_regions(player):
                for loc in region.locations:
                    if not loc.is_event:
                        assert loc.name in remaining_locs, f"{option_set_name}: '{loc.name}' exists even though it isn't an active location. "
                        remaining_locs.remove(loc.name)
            assert len(remaining_locs) == 0, f"{option_set_name}: The following locations are active but have not been created: {remaining_locs}"
