from __future__ import annotations
from collections.abc import Callable
from ..wconf import WorldConfig

Dep = Callable[[WorldConfig], bool]

# Deps define a dependency with specific configurations.
def dep_and(*deps: Dep) -> Dep:
    return lambda c: all(dep(c) for dep in deps)
def dep_or(*deps: Dep) -> Dep:
    return lambda c: any(dep(c) for dep in deps)
def dep_not(dep: Dep) -> Dep:
    return lambda c: not dep(c)
def dep_none(c: WorldConfig) -> bool:
    return True

def dep_dlc(c: WorldConfig) -> bool:
    return c.use_dlc
def dep_freemove(c: WorldConfig) -> bool:
    return c.freemove_isles
def dep_shortcuts(c: WorldConfig) -> bool:
    return c.require_secret_shortcuts
def dep_agrade_quest(c: WorldConfig) -> bool:
    return c.silverworth_quest
def dep_pacifist_quest(c: WorldConfig) -> bool:
    return c.pacifist_quest
def dep_lucien_quest(c: WorldConfig) -> bool:
    return c.lucien_quest
def dep_music_quest(c: WorldConfig) -> bool:
    return c.music_quest
def dep_dicepalace(c: WorldConfig) -> bool:
    return c.kingdice_bosssanity
def dep_dlc_boatitem(c: WorldConfig) -> bool:
    return c.use_dlc and c.dlc_randomize_boat
def dep_dlc_boat_mausoleum(c: WorldConfig) -> bool:
    return c.use_dlc and c.dlc_requires_mausoleum
def dep_dlc_chalice(c: WorldConfig) -> bool:
    return c.dlc_chalice > 0
def dep_dlc_cactusgirl_quest(c: WorldConfig) -> bool:
    return c.use_dlc and c.dlc_cactusgirl_quest
