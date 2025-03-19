from __future__ import annotations
from typing import Callable
from .wsettings import WorldSettings

Dep = Callable[[WorldSettings], bool]

# Deps determine if a region or target is enabled
def dep_and(a: Dep, b: Dep) -> Dep:
    return lambda s: a(s) and b(s)
def dep_not(a: Dep) -> Dep:
    return lambda s: not a(s)
def dep_or(a: Dep, b: Dep) -> Dep:
    return lambda s: a(s) or b(s)
def dep_none(s: WorldSettings) -> bool:
    return True
def dep_dlc(s: WorldSettings) -> bool:
    return s.use_dlc
def dep_freemove(s: WorldSettings) -> bool:
    return s.freemove_isles
def dep_shortcuts(s: WorldSettings) -> bool:
    return s.require_secret_shortcuts
def dep_agrade_quest(s: WorldSettings) -> bool:
    return s.silverworth_quest
def dep_pacifist_quest(s: WorldSettings) -> bool:
    return s.pacifist_quest
def dep_lucien_quest(s: WorldSettings) -> bool:
    return s.lucien_quest
def dep_music_quest(s: WorldSettings) -> bool:
    return s.music_quest
def dep_dicepalace(s: WorldSettings) -> bool:
    return s.kingdice_bosssanity
def dep_dlc_boatitem(s: WorldSettings) -> bool:
    return s.use_dlc and s.dlc_randomize_boat
def dep_dlc_boat_mausoleum(s: WorldSettings) -> bool:
    return s.use_dlc and s.dlc_requires_mausoleum
def dep_dlc_chalice(s: WorldSettings) -> bool:
    return s.dlc_chalice > 0
def dep_dlc_chesscastle_run(s: WorldSettings) -> bool:
    return s.dlc_chesscastle_fullrun
def dep_dlc_cactusgirl_quest(s: WorldSettings) -> bool:
    return s.use_dlc and s.dlc_cactusgirl_quest
