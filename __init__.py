from __future__ import annotations
from typing import TextIO, Any
from typing_extensions import override
from BaseClasses import Item, Tutorial, ItemClassification, CollectionState
from worlds.AutoWorld import World, WebWorld
from .rules import rules
from .names import ItemNames, LocationNames
from .options import presets
from .options import CupheadOptions
from .options.optionsanitizer import OptionSanitizer
from .wconf import WorldConfig
from .settings import CupheadSettings
from .items import itemgroups, itemdefs as idef
from .items.itembase import ItemData
from .locations import locationdefs as ld
from .locations.locationbase import LocationData
from .levels.levelids import level_ids
from .levels.levelbase import LevelData
from .shop import ShopData
from . import options, locations, levels, regions, items, shop
#from . import debug as dbg

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

class CupheadWorld(World):
    """
    A classic run and gun action game heavily focused on boss battles
    """

    GAME_NAME: str = "Cuphead"
    APWORLD_VERSION: str = "alpha02a"

    SLOT_DATA_VERSION: int = 4

    game: str = GAME_NAME # type: ignore
    web = CupheadWebWorld()
    options_dataclass = CupheadOptions
    options: CupheadOptions # type: ignore
    version = APWORLD_VERSION

    required_client_version = (0, 6, 0)
    required_server_version = (0, 6, 0)

    item_name_to_id = idef.name_to_id
    location_name_to_id = ld.name_to_id

    item_name_groups = itemgroups.item_groups

    item_names = set(idef.items_all.keys())
    location_names = set(ld.locations_all.keys())

    settings: CupheadSettings # type: ignore

    wconfig: WorldConfig

    active_items: dict[str, ItemData]
    active_locations: dict[str, LocationData]

    level_map: dict[int, int] = {}

    def resolve_random_options(self) -> None:
        _options = self.options

        # Resolve Random
        if _options.mode.value==-1:
            _options.mode.value = self.random.randint(0,6 if _options.use_dlc else 2)
        if _options.start_weapon.value==-1:
            _options.start_weapon.value = self.random.randint(0,8 if _options.use_dlc else 5)
        if _options.boss_grade_checks.value==-1:
            _options.boss_grade_checks.value = self.random.randint(0,4 if _options.use_dlc else 3)
        if _options.level_shuffle_seed.value=="":
            _options.level_shuffle_seed.value = str(self.random.getrandbits(16))

    def solo_setup(self) -> None:
        # Put items in early to prevent fill errors. FIXME: Make this more elegant.
        if self.wconfig.randomize_abilities:
            self.multiworld.early_items[self.player][ItemNames.item_ability_parry] = 1
            self.multiworld.early_items[self.player][ItemNames.item_ability_dash] = 1

    @override
    def generate_early(self) -> None:
        self.options.version.value = self.version

        self.option_sanitizer = OptionSanitizer(self.player, self.options, self.random)

        self.resolve_random_options()
        self.option_sanitizer.sanitize_options()

        # World Config (See wconfig.py)
        self.wconfig = WorldConfig(self.options)

        self.topology_present = not self.wconfig.freemove_isles

        self.use_dlc = self.wconfig.use_dlc
        self.start_weapon = self.wconfig.start_weapon
        self.level_shuffle = self.wconfig.level_shuffle

        coin_amounts = self.wconfig.coin_amounts
        self.total_coins = coin_amounts[0] + (coin_amounts[1]*2) + (coin_amounts[2]*3)

        self.active_items: dict[str,ItemData] = items.setup_items(self.wconfig)
        self.active_locations: dict[str,LocationData] = locations.setup_locations(self.wconfig)
        self.active_levels: dict[str,LevelData] = levels.setup_levels(self.wconfig,self.active_locations)

        if len(self.level_map) < 1:
            self.level_map = levels.setup_level_map(self.wconfig)

        self.shop: ShopData = shop.setup_shop_data(self.wconfig)

        self.contract_requirements: tuple[int,int,int] = self.wconfig.contract_requirements
        self.dlc_ingredient_requirements: int = self.wconfig.dlc_ingredient_requirements

        # Filler items and weights
        filler_items = list(idef.item_filler.keys())
        filler_item_weights = self.wconfig.filler_item_weights
        self.filler_item_weights = [
            (trap, weight) for trap, weight in zip(filler_items, filler_item_weights, strict=True) if weight > 0
        ]

        # Solo World Setup (for loners)
        if self.multiworld.players<2:
            self.solo_setup()

    @override
    def fill_slot_data(self) -> dict[str, Any]:
        slot_data: dict[str, Any] = {
            "version": CupheadWorld.SLOT_DATA_VERSION,
            "world_version": self.version,
            "level_map": self.level_map,
            "shop_map": self.shop.shop_map,
            "contract_requirements": self.contract_requirements,
            "dlc_ingredient_requirements": self.dlc_ingredient_requirements,
        }
        slot_data_options: list[str] = [
            "use_dlc",
            "mode",
            "expert_mode",
            "start_weapon",
            "weapon_mode",
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

    @override
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if len(self.option_sanitizer.option_overrides)>0:
            spoiler_handle.write(f"\n{self.player_name} Option Changes:\n\n")
            spoiler_handle.write('\n'.join([x for x in self.option_sanitizer.option_overrides]) + '\n')
        if self.level_shuffle and len(self.level_map)>0:
            spoiler_handle.write(f"\n{self.player_name} Level Shuffle Map:\n\n")
            spoiler_handle.write(
                '\n'.join([f"{level_ids[x]} -> {level_ids[y]}" for x, y in self.level_map.items()]) + '\n'
            )

        def _gen_shop_list(y: list[str]) -> str:
            return "\n".join([f" {z}" for z in y])

        spoiler_handle.write(f"\n{self.player_name} Shop Items:\n\n")
        spoiler_handle.write("\n".join([
            f"{x}:\n{_gen_shop_list(y)}" for x, y in self.shop.shop_locations.items() \
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
    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        hint_dict: dict[int, str] = {}
        if self.level_shuffle:
            for level, map in self.level_map.items():
                if level_ids[level] in self.active_locations.keys() and level != map:
                    for loc in self.active_levels[level_ids[level]].locations:
                        hint_dict[self.location_name_to_id[loc]] = \
                            f"{level_ids[self.level_map[level]]} at {level_ids[level]}"
        for shopl, locs in self.shop.shop_locations.items():
            if shopl != LocationNames.shop_set4 or self.use_dlc:
                for loc in locs:
                    hint_dict[self.location_name_to_id[loc]] = shopl
        hint_data.update({self.player: hint_dict})

    @override
    def set_rules(self) -> None:
        rules.set_rules(self)

    @override
    def post_fill(self) -> None:
        #debug.print_locations(self)
        #dbg.debug_visualize_regions(self)
        return super().post_fill()

    # For Universal Tracker
    def interpret_slot_data(self, slot_data: dict[str, Any]) -> None:
        if "version" not in slot_data:
            raise KeyError("\"version\" is missing from slot data!")
        if "world_version" not in slot_data:
            raise KeyError("\"world_version\" is missing from slot data!\nIncompatible APWorld!")
        _version = slot_data["version"]
        if _version != CupheadWorld.SLOT_DATA_VERSION:
            raise ValueError(f"Slot data version mismatch. {_version}!={CupheadWorld.SLOT_DATA_VERSION}")

        print(f"SlotData version: {_version}")
        print(f"Server APWorld Version: {slot_data["world_version"]}")
        print(f"This APWorld Version: {CupheadWorld.APWORLD_VERSION}")

        if "level_map" in slot_data:
            self.level_map = slot_data["level_map"]
