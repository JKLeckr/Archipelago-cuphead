### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from collections.abc import Callable

from ..enums import ChaliceMode
from ..wconf import WorldConfig

Dep = Callable[[WorldConfig], bool]

DEPS: dict[str, Dep] = {}
def dep(fn: Dep) -> Dep:
    _name = fn.__name__.removeprefix("dep_")
    DEPS[_name] = fn
    return fn

# Deps define a dependency with specific configurations.
def dep_and(*deps: Dep) -> Dep:
    return lambda c: all(dep(c) for dep in deps)
def dep_or(*deps: Dep) -> Dep:
    return lambda c: any(dep(c) for dep in deps)
def dep_not(dep: Dep) -> Dep:
    return lambda c: not dep(c)
def dep_none(c: WorldConfig) -> bool:
    return True

@dep
def dep_dlc(c: WorldConfig) -> bool:
    return c.use_dlc
@dep
def dep_freemove(c: WorldConfig) -> bool:
    return c.freemove_isles
@dep
def dep_shortcuts(c: WorldConfig) -> bool:
    return c.require_secret_shortcuts
@dep
def dep_agrade_quest(c: WorldConfig) -> bool:
    return c.silverworth_quest
@dep
def dep_pacifist_quest(c: WorldConfig) -> bool:
    return c.pacifist_quest
@dep
def dep_lucien_quest(c: WorldConfig) -> bool:
    return c.lucien_quest
@dep
def dep_music_quest(c: WorldConfig) -> bool:
    return c.music_quest
@dep
def dep_dicepalace_sanity(c: WorldConfig) -> bool:
    return c.kingdice_bosssanity
@dep
def dep_hard_logic(c: WorldConfig) -> bool:
    return c.hard_logic
@dep
def dep_rando_abilities(c: WorldConfig) -> bool:
    return c.randomize_abilities
@dep
def dep_dlc_cookie(c: WorldConfig) -> bool:
    return c.dlc_chalice == ChaliceMode.VANILLA or c.dlc_chalice == ChaliceMode.RANDOMIZED
@dep
def dep_dlc_boatitem(c: WorldConfig) -> bool:
    return c.use_dlc and c.dlc_randomize_boat
@dep
def dep_dlc_boat_mausoleum(c: WorldConfig) -> bool:
    return c.use_dlc and c.dlc_requires_mausoleum
@dep
def dep_dlc_chalice(c: WorldConfig) -> bool:
    return c.dlc_chalice > 0
@dep
def dep_dlc_cactusgirl_quest(c: WorldConfig) -> bool:
    return c.use_dlc and c.dlc_cactusgirl_quest
