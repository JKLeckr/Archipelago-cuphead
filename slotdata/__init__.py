from __future__ import annotations
import typing
from typing import Any
from .. import regions, rules
if typing.TYPE_CHECKING:
     from .. import CupheadWorld

def fill_slot_data(world: CupheadWorld) -> dict[str, Any]:
    slot_data: dict[str, Any] = {
        "version": world.SLOT_DATA_VERSION,
        "world_version": world.version,
        "level_map": world.level_map,
        "shop_map": world.shop.shop_map,
        "contract_requirements": world.contract_requirements,
        "dlc_ingredient_requirements": world.dlc_ingredient_requirements,
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
        "start_maxhealth_p2",
        "dlc_chalice",
        "dlc_boss_chalice_checks",
        "dlc_rungun_chalice_checks",
        "dlc_curse_mode",
        "trap_loadout_anyweapon",
        "music_shuffle",
        "ducklock_platdrop",
        "deathlink",
        "deathlink_grace_count",
    ]
    for option in slot_data_options:
        slot_data.update(world.options.as_dict(option))
    return slot_data

def _parse_level_map(raw_level_map: dict[str, Any]) -> dict[int, int]:
    return {int(x): int(y) for x, y in raw_level_map.items()}

def interpret_slot_data(world: CupheadWorld, slot_data: dict[str, Any]) -> None:
    if "version" not in slot_data:
        raise KeyError("\"version\" is missing from slot data!")
    if "world_version" not in slot_data:
        raise KeyError("\"world_version\" is missing from slot data!\nIncompatible APWorld!")
    _version = slot_data["version"]
    if _version != world.SLOT_DATA_VERSION:
        raise ValueError(f"Slot data version mismatch. {_version}!={world.SLOT_DATA_VERSION}")

    _world_version = slot_data["world_version"]

    print(f"SlotData version: {_version}")
    print(f"Server APWorld Version: {_world_version}")
    print(f"This APWorld Version: {world.APWORLD_VERSION}")

    if "level_map" in slot_data:
        world.level_map = _parse_level_map(slot_data["level_map"])

    world.multiworld.regions.region_cache[world.player] = {}
    world.multiworld.regions.entrance_cache[world.player] = {}
    world.multiworld.regions.location_cache[world.player] = {}

    #print(world.wconfig.level_shuffle)
    #print(world.level_map)

    regions.create_regions(world)
    rules.set_rules(world)
