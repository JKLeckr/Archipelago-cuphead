from __future__ import annotations
from random import Random
from ..names import LocationNames
from ..wconf import WorldConfig
from ..enums import LevelShuffleMode
from . import leveldefs as ldef
from . import levelmap as lmap

def setup_level_shuffle_map(rand: Random, wconf: WorldConfig) -> dict[int,int]:
    use_dlc = wconf.use_dlc
    separate_plane = wconf.level_shuffle == LevelShuffleMode.PLANE_SEPARATE
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
    _levels = [lmap.level_id_map[x] for x in level_list if (x not in level_exclude_list)]
    _excluded_levels = [lmap.level_id_map[x] for x in level_list if (x in level_exclude_list)]

    levels_shuffled = list(_levels)
    rand.shuffle(levels_shuffled)

    for i in range(len(_levels)):
        res[_levels[i]] = levels_shuffled[i]
    for x in _excluded_levels:
        res[x] = x

    return res
