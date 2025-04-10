from __future__ import annotations
from typing import Union # type: ignore
from typing import TextIO, Any
from typing_extensions import override
from BaseClasses import Item, Tutorial, ItemClassification, CollectionState
from Options import NumericOption
from worlds.AutoWorld import World, WebWorld
from .rules import rules
from .regions import regions
from .names import ItemNames, LocationNames
from .options import options, presets
from .options.options import CupheadOptions
from .wsettings import WorldSettings
from .items import items, itemdefs as idef
from .items.itembase import ItemData
from .locations import locations, locationdefs as ld
from .locations.locationbase import LocationData
from .levels import levels
from .levels.leveldefs import level_map
from .levels.levelbase import LevelData
from .shop import ShopData
from . import shop
from . import debug # type: ignore
import settings

class CupheadWebWorld(WebWorld):
    theme = "grass"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Cuphead Archipelago randomizer on your machine",
        "English",
        "setup_en.md",
        "setup/en",
        ["JKLeckr"]
    )
    tutorials = [setup_en]
    option_groups = options.cuphead_option_groups
    options_presets = presets.option_presets

class CupheadSettings(settings.Group):
    class LogOptionOverrides(settings.Bool):
        """Log options that are overridden from incompatible combinations to console."""

    class WriteOverridesToSpoiler(settings.Bool):
        """Write options that are overridden from incompatible combinations to spoiler."""

    class Verbose(settings.Bool):
        """Log extra information to the console."""

    log_option_overrides: Union[LogOptionOverrides, bool] = True # type: ignore
    write_overrides_to_spoiler: Union[WriteOverridesToSpoiler, bool] = True # type: ignore
    verbose: Union[LogOptionOverrides, bool] = False # type: ignore

class CupheadWorld(World):
    """
    A classic run and gun action game heavily focused on boss battles
    """

    GAME_NAME: str = "Cuphead"
    APWORLD_VERSION: str = "alpha01a"

    game: str = GAME_NAME # type: ignore
    web = CupheadWebWorld()
    options_dataclass = CupheadOptions
    options: CupheadOptions # type: ignore
    version = APWORLD_VERSION

    required_client_version = (0, 6, 0)
    required_server_version = (0, 6, 0)

    item_name_to_id = idef.name_to_id
    location_name_to_id = ld.name_to_id

    item_name_groups = idef.item_groups

    item_names = set(idef.items_all.keys())
    location_names = set(ld.locations_all.keys())

    settings: CupheadSettings # type: ignore

    wsettings: WorldSettings

    active_locations: dict[str,LocationData]

    level_shuffle_map: dict[int,int] = {}

    option_overrides: list[str] = []

    def override_option(self, option: NumericOption, value: int, reason: str | None = None, quiet: bool = False):
        string = f"{option.current_option_name}: \"{option.value}\" -> \"{value}\"."
        if reason:
            string += " Reason: {reason}"
        self.option_overrides.append(string)
        if self.settings.log_option_overrides and not quiet:
            msg = f"Option \"{option.current_option_name}\" was overridden from \"{option.value}\" to \"{value}\"."
            msg_reason = f"Reason: {reason}."
            print(f"Warning: For player {self.player}: {msg} {msg_reason}")
        option.value = value

    def resolve_random_options(self) -> None:
        _options = self.options

        # Resolve Random
        if _options.mode.value==-1:
            _options.mode.value = self.random.randint(0,6 if _options.use_dlc else 2)
        if _options.start_weapon.value==-1:
            _options.start_weapon.value = self.random.randint(0,8 if _options.use_dlc else 5)
        if _options.boss_grade_checks.value==-1:
            _options.boss_grade_checks.value = self.random.randint(0,4 if _options.use_dlc else 3)

    def sanitize_options(self) -> None:
        _options = self.options

        CONTRACT_GOAL_REASON = "Contract Goal cannot be less than requirements"

        # Sanitize settings
        if _options.contract_goal_requirements.value < _options.contract_requirements.value:
            self.override_option(
                _options.contract_goal_requirements,
                _options.contract_requirements.value,
                CONTRACT_GOAL_REASON
            )
        if (_options.use_dlc and \
            _options.dlc_ingredient_goal_requirements.value < _options.dlc_ingredient_requirements.value):
            self.override_option(
                _options.dlc_ingredient_goal_requirements,
                _options.dlc_ingredient_requirements.value,
                CONTRACT_GOAL_REASON
            )
        self.sanitize_dlc_options()
        # Sanitize grade checks
        if not _options.expert_mode and _options.boss_grade_checks.value>3:
            self.override_option(_options.boss_grade_checks, 3, "Expert Off")

    def sanitize_dlc_chalice_options(self) -> None:
        _options = self.options
        if _options.dlc_chalice.value == 0:
            CHALICE_REASON = "Chalice Off"
            if _options.dlc_boss_chalice_checks.value:
                self.override_option(_options.dlc_boss_chalice_checks, False, CHALICE_REASON, True)
            if _options.dlc_rungun_chalice_checks.value:
                self.override_option(_options.dlc_rungun_chalice_checks, False, CHALICE_REASON, True)
            if _options.dlc_kingdice_chalice_checks.value:
                self.override_option(_options.dlc_kingdice_chalice_checks, False, CHALICE_REASON, True)
            if _options.dlc_chess_chalice_checks.value:
                self.override_option(_options.dlc_chess_chalice_checks, False, CHALICE_REASON, True)
            if _options.dlc_cactusgirl_quest.value:
                self.override_option(_options.dlc_cactusgirl_quest, False, CHALICE_REASON)
        CI_SEPARATE_ABILITIES_B = 4
        if (_options.dlc_chalice_items_separate.value & CI_SEPARATE_ABILITIES_B)>0 and not _options.randomize_abilities:
            _new_value = _options.dlc_chalice_items_separate.value & ~CI_SEPARATE_ABILITIES_B
            self.override_option(_options.dlc_chalice_items_separate, _new_value, "Randomize Abilities Off")

    def sanitize_dlc_options(self) -> None:
        _options = self.options
        if not _options.use_dlc.value:
            DLC_REASON = "DLC Off"
            # Sanitize mode
            if _options.mode.value>2:
                self.override_option(_options.mode, self.random.randint(0,2), DLC_REASON)
            # Sanitize start_weapon
            if _options.start_weapon.value>5:
                self.override_option(_options.start_weapon, self.random.randint(0,5), DLC_REASON)
        self.sanitize_dlc_chalice_options()

    def solo_setup(self) -> None:
        # Put items in early to prevent fill errors. FIXME: Make this more elegant.
        if self.wsettings.randomize_abilities:
            self.multiworld.early_items[self.player][ItemNames.item_ability_parry] = 1
            self.multiworld.early_items[self.player][ItemNames.item_ability_dash] = 1

    @override
    def generate_early(self) -> None:
        self.options.version.value = self.version

        self.resolve_random_options()
        self.sanitize_options()

        # Settings (See Settings.py)
        self.wsettings = WorldSettings(self.options)

        self.topology_present = not self.wsettings.freemove_isles

        self.use_dlc = self.wsettings.use_dlc
        self.start_weapon = self.wsettings.start_weapon
        self.level_shuffle = self.wsettings.level_shuffle

        coin_amounts = self.wsettings.coin_amounts
        self.total_coins = coin_amounts[0] + (coin_amounts[1]*2) + (coin_amounts[2]*3)

        self.active_items: dict[str,ItemData] = items.setup_items(self.wsettings)
        self.active_locations: dict[str,LocationData] = locations.setup_locations(self.wsettings)
        #Tests.test_duplicates(self.active_locations)
        self.active_levels: dict[str,LevelData] = levels.setup_levels(self.wsettings,self.active_locations)
        if self.level_shuffle:
            self.level_shuffle_map: dict[int,int] = levels.setup_level_shuffle_map(self.random, self.wsettings)

        self.shop: ShopData = shop.setup_shop_data(self.wsettings)

        self.contract_requirements: tuple[int,int,int] = self.wsettings.contract_requirements
        self.dlc_ingredient_requirements: int = self.wsettings.dlc_ingredient_requirements

        # Filler items and weights
        filler_items = list(idef.item_filler.keys())
        filler_item_weights = self.wsettings.filler_item_weights
        self.filler_item_weights = [
            (trap, weight) for trap, weight in zip(filler_items, filler_item_weights, strict=True) if weight > 0
        ]

        # Solo World Setup (for loners)
        if self.multiworld.players<2:
            self.solo_setup()

    @override
    def fill_slot_data(self) -> dict[str, Any]:
        slot_data: dict[str, Any] = {
            "version": 2,
            "world_version": self.version,
            "level_shuffle_map": self.level_shuffle_map,
            "shop_map": self.shop.shop_map,
            "contract_requirements": self.contract_requirements,
            "dlc_ingredient_requirements": self.dlc_ingredient_requirements,
        }
        slot_data_options: list[str] = [
            "use_dlc",
            "mode",
            "expert_mode",
            "start_weapon",
            "randomize_weapon_ex",
            "contract_goal_requirements",
            "dlc_ingredient_goal_requirements",
            "freemove_isles",
            "randomize_abilities",
            "boss_grade_checks",
            "rungun_grade_checks",
            "start_maxhealth",
            "dlc_chalice",
            "dlc_curse_mode",
            "trap_loadout_anyweapon",
            "music_shuffle",
            "deathlink",
        ]
        for option in slot_data_options:
            slot_data.update(self.options.as_dict(option))
        return slot_data

    @override
    def create_regions(self) -> None:
        regions.create_regions(self)
        #print(self.multiworld.get_locations(self.player))
        #print(regions.list_multiworld_regions_names(self.multiworld))
        #print(self.multiworld.get_region(LocationNames.level_mausoleum_ii, self.player).locations)

    @override
    def create_item(self, name: str, force_classification: ItemClassification | None = None) -> Item:
        return items.create_item(name, self.player, force_classification)

    @override
    def create_items(self) -> None:
        items.create_items(self)

    def _gen_shop_list(self, y: list[str]) -> str:
        return "\n".join([f" {z}" for z in y])

    @override
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.settings.write_overrides_to_spoiler and len(self.option_overrides)>0:
            spoiler_handle.write(f"\n{self.player_name} Option Changes:\n\n")
            spoiler_handle.write('\n'.join([x for x in self.option_overrides]) + '\n')
        if self.level_shuffle and len(self.level_shuffle_map)>0:
            spoiler_handle.write(f"\n{self.player_name} Level Shuffle Map:\n\n")
            spoiler_handle.write(
                '\n'.join([f"{level_map[x]} -> {level_map[y]}" for x, y in self.level_shuffle_map.items()]) + '\n'
            )
        spoiler_handle.write(f"\n{self.player_name} Shop Items:\n\n")
        _nl = "\n"
        spoiler_handle.write("\n".join([
            f"{x}:\n{self._gen_shop_list(y)}" for x, y in self.shop.shop_locations.items() \
                if (x != LocationNames.shop_set4 or self.use_dlc)
        ]))

    @override
    def collect(self, state: CollectionState, item: Item) -> bool:
        if item.name in {ItemNames.item_coin2, ItemNames.item_coin3}:
            amount = 3 if item.name == ItemNames.item_coin3 else 2
            state.prog_items[self.player][ItemNames.item_coin] += amount
            return True
        else:
            return super().collect(state, item)

    @override
    def remove(self, state: CollectionState, item: Item) -> bool:
        if item.name in {ItemNames.item_coin2, ItemNames.item_coin3}:
            amount = 3 if item.name == ItemNames.item_coin3 else 2
            state.prog_items[self.player][ItemNames.item_coin] -= amount
            return True
        else:
            return super().remove(state, item)

    @override
    def get_filler_item_name(self) -> str:
        return items.get_filler_item_name(self)

    @override
    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        hint_dict: dict[int, str] = {}
        if self.level_shuffle:
            for level, map in self.level_shuffle_map.items():
                if level_map[level] in self.active_locations.keys() and level != map:
                    for loc in self.active_levels[level_map[level]].locations:
                        hint_dict[self.location_name_to_id[loc]] = \
                            f"{level_map[self.level_shuffle_map[level]]} at {level_map[level]}"
        for shopl, locs in self.shop.shop_locations.items():
            if shopl != LocationNames.shop_set4 or self.use_dlc:
                for loc in locs:
                    hint_dict[self.location_name_to_id[loc]] = shopl
        hint_data.update({self.player: hint_dict})

    @override
    def set_rules(self) -> None:
        rules.set_rules(self)
        #debug.print_locations(self)
        #debug.visualize_regions(self.multiworld.get_region("Menu", self.player), "./output/regionmap.puml")
