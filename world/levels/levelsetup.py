### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from random import Random

from ..auxiliary import scrub_list
from ..locations.locationbase import LocationData
from ..names import regionnames
from ..wconf import WorldConfig
from . import leveldefs as ldef
from . import levelids, levelshuffle
from .levelbase import LevelData

if typing.TYPE_CHECKING:
    from ..settings import CupheadSettings

def setup_levels(
        settings: CupheadSettings,
        wconf: WorldConfig,
        active_locations: dict[str,LocationData]
    ) -> dict[str,LevelData]:
    use_dlc = wconf.use_dlc
    levels: dict[str,LevelData] = {}

    _debug_scrub = settings.is_debug_bit_on(32)

    levels[regionnames.level_tutorial] = ldef.level_special[regionnames.level_tutorial]
    for lev,data in {**ldef.level_boss, **ldef.level_boss_final, **ldef.level_rungun}.items():
        levels[lev] = LevelData(
            data.world_location,
            scrub_list(data.locations, active_locations.keys(), _debug_scrub),
        )
    levels.update(ldef.level_mausoleum)

    if use_dlc:
        for lev,data in {**ldef.level_dlc_boss, **ldef.level_dlc_boss_final}.items():
            levels[lev] = LevelData(
                data.world_location,
                scrub_list(data.locations, active_locations.keys(), _debug_scrub),
            )
        levels.update(ldef.level_dlc_chesscastle_boss)
        levels.update(ldef.level_dlc_special)

    return levels

def setup_level_map(wconf: WorldConfig) -> dict[int,int]:
    rand = Random(wconf.level_shuffle_seed)
    level_map: dict[int,int] = {}

    level_map.update(
        levelshuffle.get_level_shuffle_map(rand, wconf.use_dlc, wconf.level_shuffle, wconf.level_shuffle_kingdice)
    )

    for k,v in wconf.level_placements.items():
        level_map[levelids.level_to_id[k]] = levelids.level_to_id[v]

    return level_map
