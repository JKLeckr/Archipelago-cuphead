### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing

from ...enums import WeaponMode
from ...items import weapons
from ...names import itemnames
from .levelrulebase import LRSelector

if typing.TYPE_CHECKING:
    from ...options import CupheadOptions

LRSELECTORS: dict[str, LRSelector] = {}
def selector(fn: LRSelector) -> LRSelector:
    _name = fn.__name__.removeprefix("lrs_")
    LRSELECTORS[_name] = fn
    return fn

@selector
def lrs_all_weapon_ex(options: CupheadOptions) -> dict[str, int]:
    if (options.weapon_mode.evalue & WeaponMode.PROGRESSIVE) > 0:
        return dict.fromkeys(weapons.weapon_p_dict.values(), 2)
    return dict.fromkeys(weapons.weapon_ex_dict.values(), 1)

@selector
def lrs_contract_req(options: CupheadOptions) -> dict[str, int]:
    return {itemnames.item_contract: options.contract_requirements.value}

@selector
def lrs_dlc_ingredient_req(options: CupheadOptions) -> dict[str, int]:
    return {itemnames.item_dlc_ingredient: options.dlc_ingredient_requirements.value}
