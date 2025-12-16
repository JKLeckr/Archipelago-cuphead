### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from typing import Any

if typing.TYPE_CHECKING:
     from ... import CupheadWorld
     from ..wconf import WorldConfig

def _get_feature_bits(wconf: WorldConfig) -> int:
    return 0

_slot_data_options: list[str] = [
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
    "dlc_kingsleap",
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

def get_slot_data_options() -> frozenset[str]:
    return frozenset(_slot_data_options)

def fill_slot_data(world: CupheadWorld) -> dict[str, Any]:
    slot_data: dict[str, Any] = {
        "version": world.SLOT_DATA_VERSION,
        "world_version": world.APWORLD_VERSION,
        "feature_bit_reqs": _get_feature_bits(world.wconfig),
        "gen_bits": world.gen_bits,
        "level_map": world.level_map,
        "shop_mode": world.wconfig.shop_mode,
        "shop_map": world.shop.shop_map,
        "contract_requirements": world.contract_requirements,
        "dlc_ingredient_requirements": world.dlc_ingredient_requirements,
    }
    for option in _slot_data_options:
        slot_data.update(world.options.as_dict(option))
    return slot_data
