### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from random import Random

from .. import enums as e
from ..names import itemnames
from . import options as odefs

if typing.TYPE_CHECKING:
    from . import CupheadOptions

def _get_coin_amounts(options: CupheadOptions | None) -> tuple[int, int, int]:
    use_dlc = options.use_dlc.value if options else odefs.DeliciousLastCourse.default
    extra_coins = options.extra_coins.value if options else odefs.ExtraCoins.default
    total_single_coins = (40 if use_dlc else 37) + extra_coins
    total_double_coins = 5 if use_dlc else 0
    total_triple_coins = 2 if use_dlc else 1

    return (total_single_coins, total_double_coins, total_triple_coins)


def _get_contract_requirements(options: CupheadOptions | None) -> tuple[int, int, int]:
    max_contracts = (5, 10, 17)
    total_req = options.contract_requirements.value if options else odefs.ContractRequirements.default
    die1 = min(total_req // 3, max_contracts[0])
    die2 = min((die1 + total_req) // 2, max_contracts[1])

    return (die1, die2, total_req)


def _get_filler_item_weights(options: CupheadOptions | None) -> list[tuple[str, int]]:
    filler_items: list[str] = [
        itemnames.item_level_extrahealth,
        itemnames.item_level_supercharge,
        itemnames.item_level_fastfire,
    ]
    filler_item_weights: list[int] = [
        options.filler_weight_extrahealth.value,
        options.filler_weight_supercharge.value,
        options.filler_weight_fastfire.value,
    ] if options else [
        odefs.FillerWeightExtraHealth.default,
        odefs.FillerWeightSuperRecharge.default,
        odefs.FillerWeightFastFire.default,
    ]
    return [
        (item, weight) for item, weight in zip(filler_items, filler_item_weights, strict=True) if weight > 0
    ]


def _get_trap_item_weights(options: CupheadOptions | None) -> list[tuple[str, int]]:
    trap_items: list[str] = [
        itemnames.item_level_trap_fingerjam,
        itemnames.item_level_trap_slowfire,
        itemnames.item_level_trap_superdrain,
        itemnames.item_level_trap_loadout,
        itemnames.item_level_trap_screen,
    ]
    trap_item_weights: list[int] = [
        options.trap_weight_fingerjam.value,
        options.trap_weight_slowfire.value,
        options.trap_weight_superdrain.value,
        options.trap_weight_loadout.value,
        0,
    ] if options else [
        odefs.TrapWeightFingerJam.default,
        odefs.TrapWeightSlowFire.default,
        odefs.TrapWeightSuperDrain.default,
        odefs.TrapWeightLoadout.default,
        0,
    ]
    return [
        (trap, weight) for trap, weight in zip(trap_items, trap_item_weights, strict=True) if weight > 0
    ]

def _get_separate_items_mode(options: CupheadOptions | None) -> e.ItemGroups:
    _set = (
        options.dlc_chalice_items_separate.value if options else odefs.DlcChaliceItemsSeparate.default
    )
    _val = e.ItemGroups.NONE

    def _get_bit(opt: str, item_group: e.ItemGroups) -> int:
        return item_group if opt in _set else e.ItemGroups.NONE

    _val |= _get_bit("core_items", e.ItemGroups.CORE_ITEMS)
    _val |= _get_bit("weapon_ex", e.ItemGroups.WEAPON_EX)
    _val |= _get_bit("abilities", e.ItemGroups.ABILITIES)

    # TODO: Change this when this is implemented
    return e.ItemGroups.NONE

# Shop Map (shop_index(weapons, charms)) # TODO: Maybe shuffle the amounts later
def _get_shop_map(options: CupheadOptions | None) -> list[tuple[int, int]]:
        dlc = options.use_dlc.value if options else odefs.DeliciousLastCourse.default
        return [(2,2), (2,2), (1,2), (3,2)] if not dlc else [(2,2), (2,2), (2,2), (2,2)]

def resolve_dependent_options(options: CupheadOptions) -> None:
    if options.start_maxhealth_p2.value == 0:
        options.start_maxhealth_p2.value = options.start_maxhealth.value

def resolve_random_options(options: CupheadOptions, rand: Random) -> None:
    # Resolve Random
    if options.mode.value == -1:
        # TODO: Once modes can be combined, remove this and use randint
        _mode_choices = [1, 2, 4] + ([8, 9, 16, 18] if options.use_dlc else [])
        options.mode.value = rand.choice(_mode_choices)
    if options.start_weapon.value == -1:
        options.start_weapon.value = rand.randint(0,8 if options.use_dlc else 5)
    if options.boss_grade_checks.value == -1:
        options.boss_grade_checks.value = rand.randint(0,4 if options.use_dlc else 3)
    if options.level_shuffle_seed.value == "":
        options.level_shuffle_seed.value = "".join(rand.choices("0123456789", k=16))
