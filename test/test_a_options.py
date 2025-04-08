from typing import Any
from dataclasses import fields
from Options import PerGameCommonOptions
from ..options import options
from . import CupheadTestBase

class TestOptionNames(CupheadTestBase):
    def test_option_names(self):
        common_fieldnames = {f for f in fields(PerGameCommonOptions)}
        option_fields = [f for f in fields(options.CupheadOptions) if f not in common_fieldnames]

        for field in option_fields:
            with self.subTest(field.name):
                assert field.name == field.type.name, f"{field.name} != {field.type.name}" # type: ignore

# Borrowed from Hammerwatch (thx @Parcosmic)
class TestOptions(CupheadTestBase):
    option_dict: dict[str, dict[str, Any]] = {
        "Freemove": {
            "freemove_isles": True,
        },
        "DLC": {
            "use_dlc": True,
            "mode": "dlc_beat_both",
        },
        "No Ability Rando": {
            "randomize_abilities": False,
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
        "DLC Devil Goal": {
            "use_dlc": True,
            "mode": "beat_devil"
        },
        "DLC Devil Goal No Abilities": {
            "use_dlc": True,
            "mode": "beat_devil",
            "randomize_abilities": False,
        },
    }

    def test_default_options(self):
        option_set_name = "Default Options"
        test_world = TestOptions()
        test_world.world_setup()
        test_world._check_all_locations_are_active(option_set_name)
        print(f"Seed of \"{option_set_name}\": {test_world.multiworld.seed}")
        test_world.test_fill()

    def test_options(self):
        for option_set, opts in self.option_dict.items():
            with self.subTest(option_set):
                test_world = TestOptions()
                test_world.options = opts
                test_world.world_setup()
                test_world._check_all_locations_are_active(option_set)
                print(f"Seed of \"{option_set}\": {test_world.multiworld.seed}")
                test_world.test_fill()
                test_world.world_setup()
                test_world.test_empty_state_can_reach_something()
                test_world.world_setup()
                test_world.test_all_state_can_reach_everything()

    def _check_all_locations_are_active(self, option_set_name: str):
        for player in self.multiworld.get_game_players(self.game):
            remaining_locs = {x for x,y in self.multiworld.worlds[player].active_locations.items() if y.id is not None}
            for region in self.multiworld.get_regions(player):
                for loc in region.locations:
                    if not loc.is_event:
                        assert loc.name in remaining_locs, \
                            f"{option_set_name}: '{loc.name}' exists even though it isn't an active location."
                        remaining_locs.remove(loc.name)
            assert len(remaining_locs) == 0, \
                f"{option_set_name}: The following locations are active but have not been created: {remaining_locs}"
