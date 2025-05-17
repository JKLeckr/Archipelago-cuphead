from __future__ import annotations
import typing
from .levelbase import LevelData
from . import levelsetup, levelmap
if typing.TYPE_CHECKING:
    from .. import CupheadWorld

setup_levels = levelsetup.setup_levels

setup_level_shuffle_map = levelsetup.setup_level_shuffle_map

def get_mapped_level_name(world: CupheadWorld, level: str) -> str:
    if world.level_shuffle:
        level_shuffle_map = world.level_shuffle_map
        if level in levelmap.level_id_map:
            level_map_id = levelmap.level_id_map[level]
            if level_map_id in level_shuffle_map:
                return levelmap.level_map[level_shuffle_map[level_map_id]]
    return level

def get_level(world: CupheadWorld, level: str, map: bool = True) -> LevelData:
    levels = world.active_levels
    if level not in levels:
        print("WARNING: For \""+level+"\": level is invalid!")
        return LevelData(None, [])
    if not map:
        return levels[level]
    return levels[get_mapped_level_name(world, level)]

def level_query(levels: dict[str,LevelData], world_location: str | None) -> dict[str,LevelData]:
    return {
        level: data for level,data in levels.items() if (not world_location or data.world_location == world_location)
    }
