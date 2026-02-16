### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from typing import Any, ClassVar, TextIO

from typing_extensions import override

from BaseClasses import CollectionState, Item, ItemClassification, Tutorial
from Options import Option, PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World

from . import debug as dbg
from .fver import FVersion
from .world import items, levels, locations, options, regions, slotdata
from .world.enums import WeaponMode
from .world.items import itemcreate, itemgroups, weapons
from .world.items import itemdefs as idef
from .world.items.itembase import ItemData
from .world.levels.levelbase import LevelData
from .world.levels.levelids import level_ids
from .world.locations import locationdefs as ld
from .world.locations.locationbase import LocationData
from .world.names import itemnames, regionnames
from .world.options import CupheadOptions, presets
from .world.options import optionbits as obits
from .world.options import optionresolver as oresolver
from .world.options.optionsanitizer import OptionSanitizer
from .world.rules import rules
from .world.settings import CupheadSettings
from .world.shop import ShopData


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
    tutorials = [setup_en]  # noqa: RUF012
    option_groups = options.cuphead_option_groups
    options_presets = presets.option_presets

class CupheadWorld(World):
    """
    A classic run and gun action game heavily focused on boss battles
    """

    GAME_NAME: ClassVar[str] = "Cuphead"

    APWORLD_SEM_VERSION: ClassVar[tuple[int, int, int, int]] = (0, 2, 2, 0)
    APWORLD_VERSION: ClassVar[str] = str(FVersion.from_int_tuple(APWORLD_SEM_VERSION))

    AUTHORS: ClassVar[list[str]] = ["JKLeckr"]

    SLOT_DATA_VERSION: ClassVar[int] = 5

    game: ClassVar[str] = GAME_NAME # type: ignore
    web: ClassVar[WebWorld] = CupheadWebWorld()
    options_dataclass: ClassVar[type[PerGameCommonOptions]] = CupheadOptions
    options: CupheadOptions # type: ignore
    origin_region_name: str = "Start"

    required_client_version: tuple[int, int, int] = (0, 6, 7)
    required_server_version: tuple[int, int, int] = (0, 6, 7)

    item_name_to_id: ClassVar[dict[str, int]] = idef.name_to_id
    location_name_to_id: ClassVar[dict[str, int]] = ld.name_to_id

    item_name_groups: ClassVar[dict[str, set[str]]] = itemgroups.item_groups

    item_names: ClassVar[set[str]] = set(idef.items_all.keys())
    location_names: ClassVar[set[str]] = set(ld.locations_all.keys())

    settings: CupheadSettings # type: ignore

    active_items: dict[str, ItemData]
    active_locations: dict[str, LocationData]
    active_levels: dict[str, LevelData]

    level_map: dict[int, int]

    fake_gen: bool = False
    ut_can_gen_without_yaml: ClassVar[bool] = True

    def solo_setup(self) -> None:
        # Put items in early to prevent fill errors. TODO: Make this more elegant.
        if self.options.randomize_abilities.value:
            self.multiworld.early_items[self.player][itemnames.item_ability_parry] = 1
            self.multiworld.early_items[self.player][itemnames.item_ability_dash] = 1
        if (self.options.weapon_mode.value & WeaponMode.PROGRESSIVE) > 0:
            _start_weapon = weapons.weapon_p_dict[self.options.start_weapon.value]
            self.multiworld.early_items[self.player][_start_weapon] = 1
        if (self.options.weapon_mode.value & WeaponMode.EX_SEPARATE) > 0:
            _weapon = self.random.choice(weapons.weapon_ex_dict)
            self.multiworld.early_items[self.player][_weapon] = 1

    def re_gen_setup(self) -> None:
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            _slot_data_options = slotdata.get_slot_data_options()
            for okey in _slot_data_options:
                opt: Option[Any] | None = getattr(self.options, okey, None)
                if opt is not None:
                    opt.value = opt.from_any(slot_data[okey])
                else:
                    print(f"re_gen_setup: WARNING: {okey} is not registered!")

            bits: int = slot_data["gen_bits"]

            self.options.shop_mode.value = slot_data["shop_mode"] # TODO: Finish
            self.options.contract_requirements.value = slot_data["contract_requirements"]
            self.options.dlc_ingredient_requirements.value = slot_data["dlc_ingredient_requirements"]

            obits.debitify(self.options, bits) # TODO: TEST

            self.level_map = slot_data["level_map"]
            self.shop = ShopData(slot_data["shop_map"])


    @override
    def generate_early(self) -> None:
        self.fake_gen = getattr(self.multiworld, "generation_is_fake", False)

        self.options.version.value = self.APWORLD_VERSION

        oresolver.resolve_dependent_options(self.options)
        oresolver.resolve_random_options(self.options, self.random)

        self.option_sanitizer = OptionSanitizer(self.player, self.options, self.random)

        self.option_sanitizer.sanitize_options()

        if self.fake_gen:
            self.re_gen_setup()
        else:
            #print(self.level_map)
            self.level_map = levels.setup_level_map(self.options)
            self.shop = ShopData.create_from_options(self.options)

        self.gen_bits = obits.bitify(self.options)

        self.topology_present = not self.options.freemove_isles.value

        self.use_dlc = self.options.use_dlc.value
        self.start_weapon = self.options.start_weapon.value

        coin_amounts = self.options.coin_amounts.value
        self.total_coins = coin_amounts[0] + (coin_amounts[1]*2) + (coin_amounts[2]*3)

        self.active_items = items.setup_items(self.options)
        self.active_locations = locations.setup_locations(self.options)
        self.active_levels = levels.setup_levels(self.settings, self.options, self.active_locations)

        # Solo World Setup (for loners)
        if self.multiworld.players<2:
            self.solo_setup()

    @override
    def fill_slot_data(self) -> dict[str, Any]:
        return slotdata.fill_slot_data(self)

    @override
    def create_regions(self) -> None:
        regions.create_regions(self)
        #print(self.multiworld.get_locations(self.player))
        #print(regions.list_multiworld_regions_names(self.multiworld))
        #print(self.multiworld.get_region(regionnames.level_mausoleum_ii, self.player).locations)

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
            spoiler_handle.write("\n".join(list(self.option_sanitizer.option_overrides)) + "\n")
        if len(self.level_map)>0:
            spoiler_handle.write(f"\n{self.player_name} Level Shuffle Map:\n\n")
            spoiler_handle.write(
                "\n".join([f"{level_ids[x]} -> {level_ids[y]}" for x, y in self.level_map.items()]) + "\n"
            )

        def _gen_shop_list(y: list[str]) -> str:
            return "\n".join([f" {z}" for z in y])

        spoiler_handle.write(f"\n{self.player_name} Shop Items:\n\n")
        spoiler_handle.write("\n".join([
            f"{x}:\n{_gen_shop_list(y)}" for x, y in self.shop.shop_locations.items() \
                if (x != regionnames.shop_set4 or self.use_dlc)
        ]))

    @override
    def collect(self, state: CollectionState, item: Item) -> bool:
        #print(item.name)
        if item.name in (itemnames.item_coin2, itemnames.item_coin3):
            amount = 3 if item.name == itemnames.item_coin3 else 2
            _name = self.collect_item(
                state,
                itemcreate.create_item(itemnames.item_coin, self.player)
            )
            if _name:
                state.add_item(_name, self.player, amount)
                return True
            return False
        if (self.options.weapon_mode.value & WeaponMode.PROGRESSIVE) > 0 and item.name in weapons.weapon_dict.values():
            _name = self.collect_item(
                state,
                itemcreate.create_active_item(self, weapons.weapon_p_dict[weapons.weapon_to_index[item.name]]),
            )
            if _name:
                state.add_item(_name, self.player, 2)
                return True
            return False
        return super().collect(state, item)

    @override
    def remove(self, state: CollectionState, item: Item) -> bool:
        if item.name in (itemnames.item_coin2, itemnames.item_coin3):
            amount = 3 if item.name == itemnames.item_coin3 else 2
            _name = self.collect_item(
                state,
                itemcreate.create_item(itemnames.item_coin, self.player),
                True
            )
            if _name:
                state.remove_item(_name, self.player, amount)
                return True
            return False
        if (self.options.weapon_mode.value & WeaponMode.PROGRESSIVE) > 0 and item.name in weapons.weapon_dict.values():
            _name = self.collect_item(
                state,
                itemcreate.create_active_item(self, weapons.weapon_p_dict[weapons.weapon_to_index[item.name]]),
                True
            )
            if _name:
                state.remove_item(_name, self.player, 2)
                return True
            return False
        return super().remove(state, item)

    @override
    def get_filler_item_name(self) -> str:
        return items.get_filler_item_name(self)

    @override
    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        hint_dict: dict[int, str] = {}
        if self.level_map:
            for level, lmap in self.level_map.items():
                if (
                    level_ids[level] in self.active_levels and
                    level_ids[lmap] in self.active_levels and
                    level != lmap
                ):
                    for loc in self.active_levels[level_ids[lmap]].locations:
                        if loc in self.active_locations and loc in self.location_name_to_id:
                            hint_dict[self.location_name_to_id[loc]] = level_ids[level]
                            if self.settings.is_debug_bit_on(16):
                                print(f"Hint: {loc} -> {level_ids[level]}")
                        #else:
                        #    print(f"{loc} not valid for shuffle hint.")
        for shopl, locs in self.shop.shop_locations.items():
            if shopl != regionnames.shop_set4 or self.use_dlc:
                for loc in locs:
                    hint_dict[self.location_name_to_id[loc]] = shopl
        hint_data.update({self.player: hint_dict})

    @override
    def set_rules(self) -> None:
        rules.set_rules(self)

    @override
    def post_fill(self) -> None:
        #debug.print_locations(self)
        if self.settings.is_debug_bit_on(4):
            dbg.debug_visualize_regions(self, self.settings.is_debug_bit_on(8))
        if self.fake_gen and self.settings.is_debug_bit_on(256):
            #dbg.debug_print_regions(self)
            dbg.debug_visualize_regions(self, True, "UT")

        return super().post_fill()

    def get_start_locations(self) -> list[str]:
        _region = self.multiworld.get_region("Start", self.player)
        return [s.name for s in _region.locations]

    # For Universal Tracker
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        if "version" not in slot_data:
            raise KeyError("'version' is missing from slot data!")
        if "world_version" not in slot_data:
            raise KeyError("'world_version' is missing from slot data!\nIncompatible APWorld!")
        _version = slot_data["version"]
        if _version != CupheadWorld.SLOT_DATA_VERSION:
            raise ValueError(f"Slot data version mismatch. {_version}!={CupheadWorld.SLOT_DATA_VERSION}")

        _world_version = slot_data["world_version"]

        # FIXME: Add option to enable/disable logging
        print(f"SlotData version: {_version}")
        print(f"Server APWorld Version: {_world_version}")
        print(f"This APWorld Version: {CupheadWorld.APWORLD_VERSION}")

        return slot_data
