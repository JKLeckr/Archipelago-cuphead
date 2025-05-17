from __future__ import annotations
from random import Random
from ..names import LocationNames
from ..locations.locationbase import LocationData
from ..wconf import WorldConfig
from ..auxiliary import scrub_list
from .levelbase import LevelData
from . import levelshuffle, leveldefs as ldef

def setup_levels(wconf: WorldConfig, active_locations: dict[str,LocationData]) -> dict[str,LevelData]:
    use_dlc = wconf.use_dlc
    levels: dict[str,LevelData] = {}

    levels[LocationNames.level_tutorial] = ldef.level_special[LocationNames.level_tutorial]
    for lev,data in {**ldef.level_boss, **ldef.level_boss_final, **ldef.level_rungun}.items():
        levels[lev] = LevelData(data.world_location, scrub_list(data.locations, active_locations.keys()), data.rule)
    levels.update(ldef.level_mausoleum)

    if use_dlc:
        for lev,data in {**ldef.level_dlc_boss, **ldef.level_dlc_boss_final}.items():
            levels[lev] = LevelData(data.world_location, scrub_list(data.locations, active_locations.keys()), data.rule)
        levels.update(ldef.level_dlc_chesscastle_boss)
        levels.update(ldef.level_dlc_special)

    return levels

def setup_level_shuffle_map(rand: Random, wconf: WorldConfig) -> dict[int,int]:
    return levelshuffle.setup_level_shuffle_map(rand, wconf)
