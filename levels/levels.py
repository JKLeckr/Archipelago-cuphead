from __future__ import annotations
import typing
from random import Random
from ..names import LocationNames
from ..locations.locations import LocationData
from ..wsettings import WorldSettings, LevelShuffleMode
from ..auxiliary import scrub_list
from .levelbase import LevelData
from . import leveldefs as ldef
if typing.TYPE_CHECKING:
    from .. import CupheadWorld

def setup_levels(settings: WorldSettings, active_locations: dict[str,LocationData]) -> dict[str,LevelData]:
    use_dlc = settings.use_dlc
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

def setup_level_shuffle_map(rand: Random, settings: WorldSettings) -> dict[int,int]:
    use_dlc = settings.use_dlc
    separate_plane = settings.level_shuffle == LevelShuffleMode.PLANE_LEVELS_SEPARATE
    level_shuffle_map: dict[int,int] = {}

    # level_lists format: (level_list, exclude_list)
    level_lists: list[tuple[list[str],list[str]]]
    if separate_plane:
        level_lists: list[tuple[list[str],list[str]]] = [
            (list(ldef.level_boss_regular.keys()), [LocationNames.level_boss_kingdice]),
            (list(ldef.level_boss_plane.keys()), []),
            (list(ldef.level_rungun.keys()), []),
        ]
    else:
        level_lists: list[tuple[list[str],list[str]]] = [
            (list(ldef.level_boss.keys()), [LocationNames.level_boss_kingdice]),
            (list(ldef.level_rungun.keys()), []),
        ]
    if use_dlc:
        level_lists[0][0].extend(ldef.level_dlc_boss_regular.keys() if separate_plane else ldef.level_dlc_boss.keys())
        if separate_plane:
            level_lists[1][0].extend(ldef.level_dlc_boss_plane.keys())
        level_lists.append((list(ldef.level_dlc_chesscastle_boss.keys()), [LocationNames.level_dlc_chesscastle_run]))

    for level_list in level_lists:
        _shuffled_levels = shuffle_levels(rand, level_list[0], level_list[1])
        level_shuffle_map.update(_shuffled_levels)

    return level_shuffle_map

def shuffle_levels(rand: Random, level_list: list[str], level_exclude_list: list[str]) -> dict[int, int]:
    res: dict[int, int] = {}
    _levels = [ldef.level_id_map[x] for x in level_list if (x not in level_exclude_list)]
    _excluded_levels = [ldef.level_id_map[x] for x in level_list if (x in level_exclude_list)]

    levels_shuffled = list(_levels)
    rand.shuffle(levels_shuffled)

    for i in range(len(_levels)):
        res[_levels[i]] = levels_shuffled[i]
    for x in _excluded_levels:
        res[x] = x

    return res

def level_query(levels: dict[str,LevelData], world_location: str | None) -> dict[str,LevelData]:
    return {
        level: data for level,data in levels.items() if (not world_location or data.world_location == world_location)
    }

def get_mapped_level_name(world: CupheadWorld, level: str) -> str:
    if world.level_shuffle:
        level_shuffle_map = world.level_shuffle_map
        if level in ldef.level_id_map:
            level_map_id = ldef.level_id_map[level]
            if level_map_id in level_shuffle_map:
                return ldef.level_map[level_shuffle_map[level_map_id]]
    return level
def get_level(world: CupheadWorld, level: str, map: bool = True) -> LevelData:
    levels = world.active_levels
    if level not in levels:
        print("WARNING: For \""+level+"\": level is invalid!")
        return LevelData(None, [])
    if not map:
        return levels[level]
    return levels[get_mapped_level_name(world, level)]
