### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import dataclasses
from collections.abc import Callable
from typing import Any

from typing_extensions import override

from rule_builder.options import OptionFilter

from ..enums import ChaliceCheckMode, ChaliceMode, WeaponMode
from ..wconf import WorldConfig


@dataclasses.dataclass(frozen=True, init=False)
class Dep(OptionFilter):
    fn: Callable[[WorldConfig], bool]
    __name__: str

    def __init__(self, fn: Callable[[WorldConfig], bool]):
        super().__init__(None, None)  # type: ignore
        object.__setattr__(self, "fn", fn)
        object.__setattr__(self, "__name__", fn.__name__ if hasattr(fn, "__name__") else "anonymous_dep")

    def __call__(self, c: WorldConfig) -> bool:
        return self.fn(c)

    @override
    def check(self, options: Any) -> bool:
        if isinstance(options.wconfig, WorldConfig):
            return self.fn(options.wconfig)
        raise ValueError("options.wconfig cannot be none!")

    def __and__(self, other: Dep) -> Dep:
        return dep_and(self, other)

    def __or__(self, other: Dep) -> Dep:
        return dep_or(self, other)

    def __invert__(self) -> Dep:
        return dep_not(self)


DEPS: dict[str, Dep] = {}
def dep(fn: Callable[[WorldConfig], bool]) -> Dep:
    wrapped = Dep(fn)
    _name = wrapped.__name__.removeprefix("dep_")
    DEPS[_name] = wrapped
    return wrapped

# Deps define a dependency with specific configurations.
def dep_and(*deps: Dep) -> Dep:
    return Dep(lambda c: all(d(c) for d in deps))
def dep_or(*deps: Dep) -> Dep:
    return Dep(lambda c: any(d(c) for d in deps))
def dep_not(d: Dep) -> Dep:
    return Dep(lambda c: not d(c))

def _dep_none(c: WorldConfig) -> bool:
    return True
dep_none = Dep(_dep_none)

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
def dep_weapon_ex_rando(c: WorldConfig) -> bool:
    return c.weapon_mode & (WeaponMode.PROGRESSIVE | WeaponMode.EX_SEPARATE) > 0
@dep
def dep_dlc_chalice(c: WorldConfig) -> bool:
    return c.use_dlc and c.dlc_chalice > 0
@dep
def dep_dlc_chalice_only(c: WorldConfig) -> bool:
    return c.use_dlc and c.dlc_chalice == ChaliceMode.CHALICE_ONLY
@dep
def dep_dlc_cookie(c: WorldConfig) -> bool:
    return c.use_dlc and (c.dlc_chalice == ChaliceMode.VANILLA or c.dlc_chalice == ChaliceMode.RANDOMIZED)
@dep
def dep_dlc_chaliced_grade_required(c: WorldConfig) -> bool:
    return c.use_dlc and (c.dlc_boss_chalice_checks & ChaliceCheckMode.GRADE_REQUIRED) > 0
@dep
def dep_dlc_rungun_chaliced_grade_required(c: WorldConfig) -> bool:
    return c.use_dlc and (c.dlc_rungun_chalice_checks & ChaliceCheckMode.GRADE_REQUIRED) > 0
@dep
def dep_dlc_boatitem(c: WorldConfig) -> bool:
    return c.use_dlc and c.dlc_randomize_boat
@dep
def dep_dlc_boat_mausoleum(c: WorldConfig) -> bool:
    return c.use_dlc and c.dlc_requires_mausoleum
@dep
def dep_dlc_cactusgirl_quest(c: WorldConfig) -> bool:
    return c.use_dlc and c.dlc_cactusgirl_quest
