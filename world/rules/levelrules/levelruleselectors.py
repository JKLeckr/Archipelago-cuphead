### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from collections.abc import Mapping

from ...items import weapons
from .levelrulebase import LRSelector

if typing.TYPE_CHECKING:
    from ...wconf import WorldConfig

LRSELECTORS: dict[str, LRSelector] = {}
def selector(fn: LRSelector) -> LRSelector:
    _name = fn.__name__.removeprefix("lrs_")
    LRSELECTORS[_name] = fn
    return fn

@selector
def lrs_all_p_weapons_full(wconf: WorldConfig) -> Mapping[str, int]:
    return dict.fromkeys(weapons.weapon_p_dict.values(), 2)

@selector
def lrs_all_weapon_ex(wconf: WorldConfig) -> Mapping[str, int]:
    return dict.fromkeys(weapons.weapon_ex_dict.values(), 1)
