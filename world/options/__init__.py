### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions

from .. import enums as e
from ..names import locationnames
from . import constantoptions as codefs
from . import internaloptions as iodefs
from . import options as odefs


@dataclass
class CupheadOptions(PerGameCommonOptions):
    # Options
    version: iodefs.Version
    use_dlc: odefs.DeliciousLastCourse
    mode: odefs.GameMode
    expert_mode: odefs.ExpertMode
    start_weapon: odefs.StartWeapon
    weapon_mode: odefs.WeaponMode
    start_maxhealth: odefs.StartMaxHealth
    start_maxhealth_p2: odefs.StartMaxHealthP2
    contract_requirements: odefs.ContractRequirements
    dlc_ingredient_requirements: odefs.DlcIngredientRequirements
    contract_goal_requirements: odefs.ContractGoalRequirements
    dlc_ingredient_goal_requirements: odefs.DlcIngredientGoalRequirements
    level_shuffle: odefs.LevelShuffle
    level_shuffle_kingdice: odefs.LevelShuffleDicePalace
    level_shuffle_seed: odefs.LevelShuffleSeed
    level_placements: odefs.LevelPlacements
    freemove_isles: odefs.FreeMoveIsles
    #shop_mode: odefs.ShopMode
    deathlink: odefs.DeathLink
    deathlink_grace_count: odefs.DeathLinkGraceCount
    #weapon_gate: odefs.WeaponGate
    randomize_abilities: odefs.RandomizeAbilities
    #randomize_abilities_aim: odefs.RandomizeAimAbilities
    boss_secret_checks: odefs.BossSecretChecks
    boss_grade_checks: odefs.BossGradeChecks
    rungun_grade_checks: odefs.RunGunGradeChecks
    kingdice_bosssanity: odefs.DicePalaceBossSanity
    dlc_boss_chalice_checks: odefs.DlcBossChaliceChecks
    dlc_rungun_chalice_checks: odefs.DlcRunGunChaliceChecks
    dlc_kingdice_chalice_checks: odefs.DlcDicePalaceChaliceChecks
    dlc_chess_chalice_checks: odefs.DlcChessChaliceChecks
    silverworth_quest: odefs.SilverworthQuest
    pacifist_quest: odefs.PacifistQuest
    dlc_chalice: odefs.DlcChaliceMode
    dlc_chalice_items_separate: odefs.DlcChaliceItemsSeparate
    dlc_kingsleap: odefs.DlcChessCastle
    dlc_cactusgirl_quest: odefs.DlcCactusGirlQuest
    dlc_curse_mode: odefs.DlcCurseMode
    extra_coins: odefs.ExtraCoins
    maxhealth_upgrades: odefs.MaxHealthUpgrades
    minimum_filler: odefs.MinimumFillerItems
    traps: odefs.Traps
    filler_weight_extrahealth: odefs.FillerWeightExtraHealth
    filler_weight_supercharge: odefs.FillerWeightSuperRecharge
    filler_weight_fastfire: odefs.FillerWeightFastFire
    trap_loadout_anyweapon: odefs.TrapLoadoutAnyWeapon
    trap_weight_fingerjam: odefs.TrapWeightFingerJam
    trap_weight_slowfire: odefs.TrapWeightSlowFire
    trap_weight_superdrain: odefs.TrapWeightSuperDrain
    trap_weight_loadout: odefs.TrapWeightLoadout
    music_shuffle: odefs.MusicShuffle
    ducklock_platdrop: odefs.DuckLockPlatDrop

    # Internally set options
    coin_amounts: iodefs.CoinAmounts
    contract_requirements_isle2 = iodefs.ContractRequirementsIsle2
    contract_requirements_isle3 = iodefs.ContractRequirementsIsle3

    # Constants (never change)
    buster_quest: codefs.BusterQuest
    randomize_boat: codefs.DlcRandomizeBoat
    dlc_requires_mausoleum: codefs.DlcRequiresMausoleum

    def is_dlc_chalice_items_separate(self, item_group: e.ItemGroups) -> bool:
        return (self.dlc_chalice_items_separate.enum_value & item_group) > 0

    def is_goal_used(self, goal: str) -> bool:
        if goal == locationnames.loc_event_goal_devil:
            return (
                self.mode == e.GameMode.BEAT_DEVIL or
                self.mode == e.GameMode.DLC_BEAT_BOTH or
                self.mode == e.GameMode.DLC_BEAT_DEVIL_NO_ISLE4
            )
        if goal == locationnames.loc_event_dlc_goal_saltbaker:
            return (
                self.mode == e.GameMode.DLC_BEAT_SALTBAKER or
                self.mode == e.GameMode.DLC_BEAT_BOTH or
                self.mode == e.GameMode.DLC_BEAT_SALTBAKER_ISLE4_ONLY
            )
        return False

cuphead_option_groups = [
    OptionGroup("Main", [
        odefs.DeliciousLastCourse,
        odefs.GameMode,
        odefs.ExpertMode,
        odefs.StartWeapon,
        odefs.WeaponMode,
        odefs.ContractRequirements,
        odefs.ContractGoalRequirements,
        odefs.StartMaxHealth,
        odefs.StartMaxHealthP2,
        odefs.LevelShuffle,
        odefs.LevelShuffleDicePalace,
        odefs.LevelShuffleSeed,
        odefs.LevelPlacements,
        odefs.FreeMoveIsles,
        #odefs.ShopMode,
        #odefs.WeaponGate,
        odefs.RandomizeAbilities,
        #odefs.RandomizeAimAbilities,
        odefs.DeathLink,
        odefs.DeathLinkGraceCount,
    ]),
    OptionGroup("DLC Main", [
        odefs.DlcIngredientRequirements,
        odefs.DlcIngredientGoalRequirements,
        odefs.DlcChaliceMode,
        odefs.DlcCurseMode,
    ]),
    OptionGroup("Checks", [
        odefs.BossSecretChecks,
        odefs.BossGradeChecks,
        odefs.RunGunGradeChecks,
        odefs.SilverworthQuest,
        odefs.PacifistQuest,
        odefs.DicePalaceBossSanity,
    ]),
    OptionGroup("DLC Checks", [
        odefs.DlcChessCastle,
        odefs.DlcBossChaliceChecks,
        odefs.DlcRunGunChaliceChecks,
        odefs.DlcDicePalaceChaliceChecks,
        odefs.DlcChessChaliceChecks,
        odefs.DlcCactusGirlQuest,
    ]),
    OptionGroup("Items", [
        odefs.ExtraCoins,
        odefs.MaxHealthUpgrades,
        odefs.MinimumFillerItems,
        odefs.Traps,
        odefs.DlcChaliceItemsSeparate,
    ]),
    OptionGroup("Misc", [
        odefs.DuckLockPlatDrop,
        #odefs.TrapLoadoutAnyWeapon,
        #odefs.MusicShuffle,
    ]),
    OptionGroup("Item Weights", [
        odefs.FillerWeightExtraHealth,
        odefs.FillerWeightSuperRecharge,
        odefs.FillerWeightFastFire,
        odefs.TrapWeightFingerJam,
        odefs.TrapWeightSlowFire,
        odefs.TrapWeightSuperDrain,
        odefs.TrapWeightLoadout,
    ], True),
]
