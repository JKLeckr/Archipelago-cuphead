### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from random import Random

from ..enums import LevelShuffleMode
from ..names import regionnames
from . import leveldefs as ldef
from . import levelids as lmap


def get_level_shuffle_lists(
        use_dlc: bool,
        mode: LevelShuffleMode,
        shuffle_kingdice: bool
    ) -> list[tuple[list[str],list[str]]]:
    enabled = mode > 0
    separate_plane = mode == LevelShuffleMode.PLANE_SEPARATE

    level_lists: list[tuple[list[str],list[str]]] = []
    if enabled:
        if separate_plane:
            level_lists += [
                (list(ldef.level_boss_regular.keys()), [regionnames.level_boss_kingdice]),
                (list(ldef.level_boss_plane.keys()), []),
                (list(ldef.level_rungun.keys()), []),
            ]
        else:
            level_lists += [
                (list(ldef.level_boss.keys()), [regionnames.level_boss_kingdice]),
                (list(ldef.level_rungun.keys()), []),
            ]

    if shuffle_kingdice:
        level_lists.append((list(ldef.level_dicepalace_boss.keys()), []))

    if enabled and use_dlc:
        level_lists[0][0].extend(ldef.level_dlc_boss_regular.keys() if separate_plane else ldef.level_dlc_boss.keys())
        if separate_plane:
            level_lists[1][0].extend(ldef.level_dlc_boss_plane.keys())
        #level_lists.append((list(ldef.level_dlc_chesscastle_boss.keys()), [regionnames.level_dlc_chesscastle_run]))

    return level_lists

def shuffle_levels(
    rand: Random,
    level_list: list[str],
    level_exclude_list: list[str],
    level_placements: dict[str, str] | None = None
) -> dict[int, int]:
    res: dict[int, int] = {}
    _levels = [lmap.level_to_id[x] for x in level_list if (x not in level_exclude_list)]
    _excluded_levels = [lmap.level_to_id[x] for x in level_list if (x in level_exclude_list)]

    placed_levels: dict[int, int] = {}
    used_placed_tgts: set[int] = set()

    if level_placements:
        _level_set = set(_levels)
        for src_name, tgt_name in level_placements.items():
            sindex = lmap.level_to_id[src_name]
            tindex = lmap.level_to_id[tgt_name]
            _src_in_set = sindex in _level_set
            _tgt_in_set = tindex in _level_set
            if not _src_in_set and not _tgt_in_set:
                continue
            if not _src_in_set or not _tgt_in_set:
                raise ValueError(
                    "Level placement has invalid placement: "
                    f"'{src_name} -> {tgt_name}'. "
                    f"Valid levels: {_levels}"
                )
            if tindex in used_placed_tgts:
                raise ValueError(f"Level placement duplicate target mapping: {tgt_name}")
            placed_levels[sindex] = tindex
            used_placed_tgts.add(tindex)

    rem_levels = [x for x in _levels if x not in placed_levels]
    levels_shuffled = [x for x in _levels if x not in used_placed_tgts]
    if len(rem_levels) != len(levels_shuffled):
        raise ValueError("Level placement map is invalid.")

    rand.shuffle(levels_shuffled)

    res.update(placed_levels)
    for i in range(len(rem_levels)):
        res[rem_levels[i]] = levels_shuffled[i]
    if _excluded_levels:
        res.update({x: x for x in _excluded_levels})

    return res

def get_level_shuffle_map(
    rand: Random,
    use_dlc: bool,
    mode: LevelShuffleMode,
    shuffle_kingdice: bool,
    level_placements: dict[str, str] | None = None
) -> dict[int,int]:
    level_shuffle_map: dict[int,int] = {}

    # level_lists format: (level_list, exclude_list)
    level_lists = get_level_shuffle_lists(use_dlc, mode, shuffle_kingdice)

    for level_list in level_lists:
        _shuffled_levels = shuffle_levels(rand, level_list[0], level_list[1], level_placements)
        level_shuffle_map.update(_shuffled_levels)

    return level_shuffle_map
