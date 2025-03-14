from __future__ import annotations
from typing import Optional, TextIO, Dict, Any
from typing_extensions import override
from BaseClasses import Item, Tutorial, ItemClassification, CollectionState
from Options import NumericOption
from worlds.AutoWorld import World, WebWorld
from .names import ItemNames, LocationNames
from .options import CupheadOptions, cuphead_option_groups
from .settings import WorldSettings
from .items import ItemData
from .locations import LocationData
from .levels import LevelData, level_map
from . import items, itembase, levels, locations, regions, rules, debug # type: ignore  # noqa: F401

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
    option_groups = cuphead_option_groups

class CupheadWorld(World):
    """
    A classic run and gun action game heavily focused on boss battles
    """

    GAME_NAME: str = "Cuphead"
    APWORLD_VERSION: str = "0.1.2-preview03a"

    game: str = GAME_NAME # type: ignore
    web = CupheadWebWorld()
    options_dataclass = CupheadOptions
    options: CupheadOptions # type: ignore
    version = APWORLD_VERSION

    required_client_version = (0, 5, 1)
    required_server_version = (0, 5, 1)

    item_name_to_id = items.name_to_id
    location_name_to_id = locations.name_to_id

    item_name_groups = items.get_item_groups()

    item_names = set(items.items_all.keys())
    location_names = set(locations.locations_all.keys())

    wsettings: WorldSettings

    active_locations: dict[str,LocationData]

    level_shuffle_map: dict[int,int] = {}

    option_overrides: list[str] = []

    def override_option(self, option: NumericOption, value: int, reason: Optional[str] = None):
        string = f"{option.current_option_name}: \"{option.value}\" -> \"{value}\"."
        if reason:
            string += " Reason: {reason}"
        self.option_overrides.append(string)
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

        CONTRACT_GOAL_REASON = "Contract Goal cannot be less than requirements."
        DLC_REASON = "DLC Off"

        # Sanitize settings
        if _options.contract_goal_requirements.value < _options.contract_requirements.value:
            self.override_option(_options.contract_goal_requirements, _options.contract_requirements.value, CONTRACT_GOAL_REASON)
        if _options.use_dlc and _options.dlc_ingredient_goal_requirements.value < _options.dlc_ingredient_requirements.value:
            self.override_option(_options.dlc_ingredient_goal_requirements, _options.dlc_ingredient_requirements.value, CONTRACT_GOAL_REASON)
        if not _options.use_dlc.value:
            # Sanitize mode
            if _options.mode.value>2:
                self.override_option(_options.mode, self.random.randint(0,2), DLC_REASON)
            # Sanitize start_weapon
            if _options.start_weapon.value>5:
                self.override_option(_options.start_weapon, self.random.randint(0,5), DLC_REASON)
        if _options.dlc_chalice.value >= 0:
            if _options.dlc_boss_chalice_checks.value:
                self.override_option(_options.mode, False, "Chalice Off")
        # Sanitize grade checks
        if not _options.expert_mode and _options.boss_grade_checks.value>3:
            self.override_option(_options.boss_grade_checks, 3, "Expert Off")

    def solo_setup(self) -> None:
        # Put items in early to prevent fill errors. FIXME: Make this more elegant.
        if self.wsettings.randomize_abilities:
            self.multiworld.early_items[self.player][ItemNames.item_ability_dash] = 1
            if not self.wsettings.freemove_isles:
                self.multiworld.early_items[self.player][ItemNames.item_ability_parry] = 1

    @override
    def generate_early(self) -> None:
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

        # Shop Map (shop_index(weapons, charms)) # TODO: Maybe shuffle the amounts later
        self.shop_map: list[tuple[int, int]] = self.get_shop_map()
        self.shop_locations: dict[str,list[str]] = self.get_shop_locations()

        self.contract_requirements: tuple[int,int,int] = self.wsettings.contract_requirements
        self.dlc_ingredient_requirements: int = self.wsettings.dlc_ingredient_requirements

        # Filler items and weights
        filler_items = list(items.item_filler.keys())
        filler_item_weights = self.wsettings.filler_item_weights
        self.filler_item_weights = [(trap, weight) for trap, weight in zip(filler_items, filler_item_weights, strict=True) if weight > 0]

        # Solo World Setup (for loners)
        if self.multiworld.players<2:
            self.solo_setup()

    @override
    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: dict[str, Any] = {
            "version": 2,
            "world_version": self.version,
            "level_shuffle_map": self.level_shuffle_map,
            "shop_map": self.shop_map,
            "contract_requirements": self.contract_requirements,
            "dlc_ingredient_requirements": self.dlc_ingredient_requirements,
        }
        slot_data_options: list[str] = [
            "use_dlc",
            "mode",
            "expert_mode",
            "start_weapon",
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

    def get_shop_map(self) -> list[tuple[int, int]]:
        return [(2,2), (2,2), (1,2), (3,2)] if not self.use_dlc else [(2,2), (2,2), (2,2), (2,2)]

    def get_shop_locations(self) -> dict[str,list[str]]:
        _shop_weapons = [
            LocationNames.loc_shop_weapon1,
            LocationNames.loc_shop_weapon2,
            LocationNames.loc_shop_weapon3,
            LocationNames.loc_shop_weapon4,
            LocationNames.loc_shop_weapon5,
            LocationNames.loc_shop_dlc_weapon6,
            LocationNames.loc_shop_dlc_weapon7,
            LocationNames.loc_shop_dlc_weapon8
        ]
        _shop_charms = [
            LocationNames.loc_shop_charm1,
            LocationNames.loc_shop_charm2,
            LocationNames.loc_shop_charm3,
            LocationNames.loc_shop_charm4,
            LocationNames.loc_shop_charm5,
            LocationNames.loc_shop_charm6,
            LocationNames.loc_shop_dlc_charm7,
            LocationNames.loc_shop_dlc_charm8
        ]

        shop_locations: dict[str,list[str]] = {}
        weapon_index = 0
        charm_index = 0
        for i in range(4):
            shop_region: list[str] = []
            if (i == 3):
                shop_region += _shop_weapons[weapon_index:]+_shop_charms[charm_index:]
            else:
                wcount = min(self.shop_map[i][0], len(_shop_weapons)-weapon_index)
                ccount = min(self.shop_map[i][1], len(_shop_charms)-charm_index)
                shop_region += _shop_weapons[weapon_index:(weapon_index+wcount)]
                shop_region += _shop_charms[charm_index:(charm_index+ccount)]
                weapon_index+=wcount
                charm_index+=ccount
            shop_locations[LocationNames.level_shops[i]] = shop_region ## TODO: Rename to shop sets
        return shop_locations

    @override
    def create_regions(self) -> None:
        regions.create_regions(self)
        #print(self.multiworld.get_locations(self.player))
        #print(regions.list_multiworld_regions_names(self.multiworld))
        #print(self.multiworld.get_region(LocationNames.level_mausoleum_ii, self.player).locations)

    @override
    def create_item(self, name: str, force_classification: Optional[ItemClassification] = None) -> Item:
        return itembase.create_item(name, self.player, force_classification)

    @override
    def create_items(self) -> None:
        itembase.create_items(self)

    @override
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if len(self.option_overrides)>0:
            spoiler_handle.write(f"\n{self.player} Option Changes:\n\n")
            spoiler_handle.write('\n'.join([x for x in self.option_overrides]) + '\n')
        if self.level_shuffle and len(self.level_shuffle_map)>0:
            spoiler_handle.write(f"\n{self.player} Level Shuffle Map:\n\n")
            spoiler_handle.write('\n'.join([f"{level_map[x]} -> {level_map[y]}" for x, y in self.level_shuffle_map.items()]) + '\n')
        spoiler_handle.write(f"\n{self.player} Shop Items:\n\n")
        spoiler_handle.write('\n'.join([
            (x + ':\n' + '\n'.join([f" {z}" for z in y])) for x, y in self.shop_locations.items() if (x != LocationNames.level_dlc_shop4 or self.use_dlc)
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
    def get_filler_item_name(self) -> str:
        return itembase.get_filler_item_name(self)

    @override
    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        hint_dict: Dict[int, str] = {}
        if self.level_shuffle:
            for level, map in self.level_shuffle_map.items():
                if level_map[level] in self.active_locations.keys() and level != map:
                    for loc in self.active_levels[level_map[level]].locations:
                        hint_dict[self.location_name_to_id[loc]] = level_map[self.level_shuffle_map[level]] + " at " + level_map[level]
        for shop, locs in self.shop_locations.items():
            if shop != LocationNames.level_dlc_shop4 or self.use_dlc:
                for loc in locs:
                    hint_dict[self.location_name_to_id[loc]] = shop ## TODO: Use Shop Sets
        hint_data.update({self.player: hint_dict})

    @override
    def set_rules(self) -> None:
        rules.set_rules(self)
        #debug.print_locations(self)
        #debug.visualize_regions(self.multiworld.get_region("Menu", self.player), "./output/regionmap.puml")
