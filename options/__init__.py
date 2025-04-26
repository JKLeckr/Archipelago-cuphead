from dataclasses import dataclass
from Options import PerGameCommonOptions, OptionGroup
from . import optiondefs as odefs

@dataclass
class CupheadOptions(PerGameCommonOptions):
    version: odefs.Version
    use_dlc: odefs.DeliciousLastCourse
    mode: odefs.GameMode
    expert_mode: odefs.ExpertMode
    start_weapon: odefs.StartWeapon
    weapon_mode: odefs.WeaponMode
    start_maxhealth: odefs.StartMaxHealth
    contract_requirements: odefs.ContractRequirements
    dlc_ingredient_requirements: odefs.DlcIngredientRequirements
    contract_goal_requirements: odefs.ContractGoalRequirements
    dlc_ingredient_goal_requirements: odefs.DlcIngredientGoalRequirements
    level_shuffle: odefs.LevelShuffle
    freemove_isles: odefs.FreeMoveIsles
    deathlink: odefs.DeathLink
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
    dlc_chalice: odefs.DlcChaliceEnabled
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
        odefs.LevelShuffle,
        odefs.FreeMoveIsles,
        #odefs.WeaponGate,
        odefs.RandomizeAbilities,
        #odefs.RandomizeAimAbilities,
        odefs.DeathLink,
    ]),
    OptionGroup("DLC Main", [
        odefs.DlcIngredientRequirements,
        odefs.DlcIngredientGoalRequirements,
        odefs.DlcChaliceEnabled,
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
    #OptionGroup("Misc", [
    #    odefs.TrapLoadoutAnyWeapon,
    #    odefs.MusicShuffle,
    #]),
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
