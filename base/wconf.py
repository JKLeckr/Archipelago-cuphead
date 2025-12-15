### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

# RUF009 suppressed because create_field returns a field.
# This issue seems to be a problem only when used with non-primative types.
# ruff: noqa RUF009

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, fields
from typing import Any

from ..base import enums as e
from ..names import ItemNames, LocationNames
from ..options import CupheadOptions
from ..options import options as odefs
from ..options.field import create_field


_bitifiable_fields: list[str] = [
    "boss_secret_checks",
    "buster_quest",
    "dlc_cactusgirl_quest",
    "dlc_requires_mausoleum",
    "dlc_randomize_boat",
    "fourmel_quest",
    "freemove_isles",
    "ginger_quest",
    "hard_logic",
    "kingdice_bosssanity",
    "music_quest",
    "pacifist_quest",
    "require_secret_shortcuts",
    "silverworth_quest",
]

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
        ItemNames.item_level_extrahealth,
        ItemNames.item_level_supercharge,
        ItemNames.item_level_fastfire,
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
        ItemNames.item_level_trap_fingerjam,
        ItemNames.item_level_trap_slowfire,
        ItemNames.item_level_trap_superdrain,
        ItemNames.item_level_trap_loadout,
        ItemNames.item_level_trap_screen,
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

# These are settings stored and accessed by other classes
@dataclass
class WorldConfig:
    boss_grade_checks: e.GradeCheckMode = create_field(e.GradeCheckMode, odefs.BossGradeChecks)
    boss_secret_checks: bool = create_field(bool, odefs.BossSecretChecks)
    buster_quest: bool = True
    coin_amounts: tuple[int, int, int] = _get_coin_amounts(None)
    contract_goal_requirements: int = create_field(int, odefs.ContractGoalRequirements)
    contract_requirements: tuple[int, int, int] = _get_contract_requirements(None)
    dlc_boss_chalice_checks: e.ChaliceCheckMode = create_field(e.ChaliceCheckMode, odefs.DlcBossChaliceChecks)
    dlc_cactusgirl_quest: bool = create_field(bool, odefs.DlcCactusGirlQuest)
    dlc_chalice_items_separate: e.ItemGroups = odefs.DlcChaliceItemsSeparate.default
    dlc_chalice: e.ChaliceMode = create_field(e.ChaliceMode, odefs.DlcChaliceMode)
    dlc_chess_chalice_checks: e.ChaliceCheckMode = create_field(e.ChaliceCheckMode, odefs.DlcChessChaliceChecks)
    dlc_curse_mode: e.CurseMode = e.CurseMode.VANILLA #create_field(e.CurseMode, odefs.DlcCurseMode)
    dlc_ingredient_goal_requirements: int = create_field(int, odefs.DlcIngredientGoalRequirements)
    dlc_ingredient_requirements: int = create_field(int, odefs.DlcIngredientRequirements)
    dlc_kingdice_chalice_checks: e.ChaliceCheckMode = create_field(e.ChaliceCheckMode, odefs.DlcDicePalaceChaliceChecks)
    dlc_kingsleap: e.ChessCastleMode = create_field(e.ChessCastleMode, odefs.DlcChessCastle)
    dlc_randomize_boat: bool = True
    dlc_requires_mausoleum: bool = True
    dlc_rungun_chalice_checks: e.ChaliceCheckMode = create_field(e.ChaliceCheckMode, odefs.DlcRunGunChaliceChecks)
    expert_mode: bool = create_field(bool, odefs.ExpertMode)
    filler_item_weights: list[tuple[str, int]] = field(default_factory=list[tuple[str, int]])
    fourmel_quest: bool = True
    freemove_isles: bool = create_field(bool, odefs.FreeMoveIsles)
    ginger_quest: bool = True
    hard_logic: bool = create_field(bool, odefs.HardLogic)
    kingdice_bosssanity: bool = create_field(bool, odefs.DicePalaceBossSanity)
    level_placements: dict[str, str] = create_field(dict[str, str], odefs.LevelPlacements)
    level_shuffle_kingdice: bool = create_field(bool, odefs.LevelShuffleDicePalace)
    level_shuffle_seed: str = create_field(str, odefs.LevelShuffleSeed)
    level_shuffle: e.LevelShuffleMode = create_field(e.LevelShuffleMode, odefs.LevelShuffle)
    lucien_quest: bool = False
    maxhealth_upgrades: int = create_field(int, odefs.MaxHealthUpgrades)
    minimum_filler: int = create_field(int, odefs.MinimumFillerItems)
    mode: e.GameMode = create_field(e.GameMode, odefs.GameMode)
    music_quest: bool = False
    pacifist_quest: bool = create_field(bool, odefs.PacifistQuest)
    randomize_abilities_aim: bool = False #create_field(bool, odefs.RandomizeAimAbilities)
    randomize_abilities: bool = create_field(bool, odefs.RandomizeAbilities)
    require_secret_shortcuts: bool = True
    rungun_grade_checks: e.GradeCheckMode = create_field(e.GradeCheckMode, odefs.RunGunGradeChecks)
    shop_mode: e.ShopMode = e.ShopMode.TIERS #create_field(e.ShopMode, odefs.ShopMode)
    silverworth_quest: bool = create_field(bool, odefs.SilverworthQuest)
    start_weapon: int = create_field(int, odefs.StartWeapon, 0)
    trap_item_weights: list[tuple[str, int]] = field(default_factory=list[tuple[str, int]])
    trap_loadout_anyweapon: bool = create_field(bool, odefs.TrapLoadoutAnyWeapon)
    traps: int = create_field(int, odefs.Traps)
    use_dlc: bool = create_field(bool, odefs.DeliciousLastCourse)
    weapon_gate: bool = False #create_field(bool, odefs.WeaponGate)
    weapon_mode: e.WeaponMode = create_field(e.WeaponMode, odefs.WeaponMode)

    def __init__(self, options: CupheadOptions | None = None, debug_bit: int = 0) -> None:
        for f in fields(self):
            try:
                default = (
                    f.default_factory() if callable(f.default_factory) else f.default
                )
            except ValueError as err:
                raise ValueError(f"For field {f.name}: {err}") from err
            setattr(self, f.name, default)

        if options:
            self._apply_options(options)

        self.filler_item_weights = _get_filler_item_weights(options)
        self.trap_item_weights = _get_trap_item_weights(options)
        self.coin_amounts = _get_coin_amounts(options)
        self.contract_requirements = _get_contract_requirements(options)
        self.dlc_chalice_items_separate = _get_separate_items_mode(options)

    def _apply_options(self, options: CupheadOptions) -> None:
        for f in fields(self):
            meta = f.metadata
            if meta and "conv" in meta and "oname" in meta:
                oname = meta.get("oname") or f.name
                if hasattr(options, oname):
                    value = getattr(options, oname).value
                    conv: Callable[[Any], Any] | None = meta.get("conv") or None
                    setattr(self, f.name, conv(value) if conv else value)

    def bitify(self) -> int:
        res = 0

        shift = 0
        for bit in _bitifiable_fields:
            if (hasattr(self, bit)):
                _field = getattr(self, bit)
                res |= ((1 if _field else 0) << shift) & 1
            else:
                raise KeyError(f"{bit} is not in wconf!")
            shift += 1

        return res
    
    def debitify(self, bits: int) -> None:
        shift = 0
        for bit in _bitifiable_fields:
            if (hasattr(self, bit)):
                res = (bits << shift) & 1
                setattr(self, bit, bool(res))
            else:
                raise KeyError(f"{bit} is not in wconf!")
            shift += 1

    def is_dlc_chalice_items_separate(self, item_group: e.ItemGroups) -> bool:
        return (self.dlc_chalice_items_separate & item_group) > 0

    def is_goal_used(self, goal: str) -> bool:
        if goal == LocationNames.loc_event_goal_devil:
            return (
                self.mode == e.GameMode.BEAT_DEVIL or
                self.mode == e.GameMode.DLC_BEAT_BOTH or
                self.mode == e.GameMode.DLC_BEAT_DEVIL_NO_ISLE4
            )
        if goal == LocationNames.loc_event_dlc_goal_saltbaker:
            return (
                self.mode == e.GameMode.DLC_BEAT_SALTBAKER or
                self.mode == e.GameMode.DLC_BEAT_BOTH or
                self.mode == e.GameMode.DLC_BEAT_SALTBAKER_ISLE4_ONLY
            )
        return False
