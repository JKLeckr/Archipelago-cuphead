### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing

from . import levelids, levelsetup
from .levelbase import LevelData

if typing.TYPE_CHECKING:
    from .. import CupheadWorld

setup_levels = levelsetup.setup_levels

setup_level_map = levelsetup.setup_level_map

def get_mapped_level_name(world: CupheadWorld, level: str) -> str:
    if world.level_map:
        level_map = world.level_map
        if level in levelids.level_to_id:
            level_map_id = levelids.level_to_id[level]
            if level_map_id in level_map:
                return levelids.level_ids[level_map[level_map_id]]
    return level

def get_level(world: CupheadWorld, level: str, map: bool = True) -> LevelData:
    levels = world.active_levels
    if level not in levels:
        print(f"WARNING: For '{level}': level is invalid!")
        return LevelData(None, [])
    if not map:
        return levels[level]
    return levels[get_mapped_level_name(world, level)]

def level_query(levels: dict[str, LevelData], world_location: str | None) -> dict[str,LevelData]:
    return {
        level: data for level,data in levels.items() if (not world_location or data.world_location == world_location)
    }
