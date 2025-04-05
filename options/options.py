from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Range, Choice, FreeText, PerGameCommonOptions, OptionGroup, Visibility
from .optionbase import ChoiceEx, Weight

class Version(FreeText):
    """
    Internal. Set during generation.
    The version of the APWorld
    """
    name = "version"
    display_name = name
    visibility = Visibility.spoiler
    default = "MISSINGVER"

class DeliciousLastCourse(Toggle):
    """
    ---WORKS, WIP---
    Set whether or not to use Delicious Last Course content (Requires owning the DLC).
    """
    display_name = "DLC"

class GameMode(ChoiceEx):
    """
    Set the mode of the randomizer which includes goal.
    NOTE: If DLC is not enabled, picking DLC modes will pick a random mode from the base game instead.
    """
    display_name = "Mode"
    option_beat_devil = 0
    option_collect_contracts = 1
    option_buy_out_shop = 2
    option_dlc_beat_saltbaker = 3
    option_dlc_beat_both = 4
    option_dlc_collect_ingredients = 5
    option_dlc_collect_both = 6
    #option_dlc_beat_devil_no_isle4 = 7
    #option_dlc_beat_saltbaker_isle4_only = 8
    default = 0

class HardLogic(Toggle):
    """
    -PARTIALLY WORKS, NOT STABLE-
    Use more difficult logic that may require doing unconventional things that make the randomizer more difficult.
    Examples include requiring jumping into pits to get across gaps and requiring avoiding King Dice bosses that
    requires certain abilities to beat King Dice in logic.
    """
    display_name = "Hard Logic"

class ExpertMode(Toggle):
    """
    Set the boss difficulty to expert.
    """
    display_name = "Expert Mode"

class StartWeapon(ChoiceEx):
    """
    Choose weapon to start with.
    NOTE: If DLC is not enabled, picking DLC weapons will pick a random base game weapon instead.
    """
    display_name = "Start Weapon"
    option_peashooter = 0
    option_spread = 1
    option_chaser = 2
    option_lobber = 3
    option_charge = 4
    option_roundabout = 5
    option_dlc_crackshot = 6
    option_dlc_converge = 7
    option_dlc_twistup = 8
    default = "random"

class RandomizeWeaponEx(Choice):
    """
    Randomize the weapon EX ability also.
    Your weapons will be progressive weapons.
    """
    display_name = "Randomize Weapon EX"
    option_disabled = 0
    option_enabled = 1
    option_all_but_start = 2
    default = 0

class ContractRequirements(Range):
    """
    Set the amount of contracts needed to confront Kingdice and, ultimately, the devil.
    The required contracts for the die houses are evenly distributed.
    """
    display_name = "Contract Requirements"
    range_start = 3
    range_end = 17
    default = 17

class DlcIngredientRequirements(Range):
    """
    -DLC ONLY-
    Set the amount of ingredients needed to confront Saltbaker.
    """
    display_name = "[DLC] Ingredient Requirements"
    range_start = 1
    range_end = 5
    default = 5

class ContractGoalRequirements(Range):
    """
    Set the amount of contracts needed for goal.
    Note: Cannot be lower than Contract Requirements
    """
    display_name = "Contract Goal Requirements"
    range_start = 3
    range_end = 17
    default = 17

class DlcIngredientGoalRequirements(Range):
    """
    -DLC ONLY-
    Set the amount of ingredients needed for goal.
    Note: Cannot be lower than Ingredient Requirements
    """
    display_name = "[DLC] Ingredient Goal Requirements"
    range_start = 1
    range_end = 5
    default = 5

class LevelShuffle(Choice):
    """
    --NOT YET IMPLEMENTED--
    Shuffle the Boss and Run n' Gun levels.
    Bosses and Run n' Guns are shuffled within their own group.
    """
    display_name = "Level Shuffle"
    visibility = Visibility.template | Visibility.spoiler
    option_disabled = 0
    option_all_levels = 1
    option_plane_levels_separate = 2
    alias_false = 0
    alias_true = 1
    default = 0

class FreeMoveIsles(Toggle):
    """
    Allow all the levels on each island to be freely accessible without completing a previous level first.
    """
    display_name = "Free Move Isles"

class WeaponGate(Toggle):
    """
    --NOT YET IMPLEMENTED--
    Add a weapon gate which only allows specific weapons for each fight.
    """
    display_name = "Weapon Gate"
    visibility = Visibility.none

class RandomizeAbilities(DefaultOnToggle):
    """
    Randomize essential abilities like Duck, Parry, Dash, etc.
    """
    display_name = "Randomize Abilities"

class RandomizeAimAbilities(Toggle):
    """
    --NOT IMPLEMENTED--
    Randomize aiming abilities.
    You will start with only top-right.
    """
    display_name = "Randomize Aim Abilities"
    visibility = Visibility.none

class BossSecretChecks(Toggle):
    """
    Also include beating the secret phases of the three bosses as checks.
    The three boss levels include: Botanic Panic, Pyramid Peril, and Dramatic Fanatic.
    The secret phases are more difficult than the normal fight.
    """
    display_name = "Boss Secret Checks"

class BossGradeChecks(ChoiceEx):
    """
    Enable grade checks for Boss Levels.
    NOTE: S Grade option will be treated as A+ Grade if Expert Mode is disabled.
    """
    display_name = "Boss Grade Checks"
    option_disabled = 0
    option_a_minus_grade = 1
    option_a_grade = 2
    option_a_plus_grade = 3
    option_s_grade = 4
    default = 1

class RunGunGradeChecks(Choice):
    """
    Enable grade checks for Run n' Gun levels.
    Pacifist: Beat the level without killing any monsters (not easy).
    """
    display_name = "Run n' Gun Grade Checks"
    option_disabled = 0
    option_a_minus_grade = 1
    option_a_grade = 2
    option_a_plus_grade = 3
    option_p_grade = 5
    alias_pacifist = 5
    default = 1

class DlcBossChaliceChecks(Toggle):
    """
    --NOT YET IMPLEMENTED--
    -DLC ONLY-
    -REQUIRES CHALICE-
    Enable checks for defeating each boss as Ms. Chalice.
    """
    display_name = "[DLC] Boss Chalice Checks"
    visibility = Visibility.template | Visibility.spoiler

class DlcRunGunChaliceChecks(Toggle):
    """
    --NOT YET IMPLEMENTED--
    -DLC ONLY-
    -REQUIRES CHALICE-
    Enable checks for completing each Run N Gun as Ms. Chalice.
    """
    display_name = "[DLC] Boss Chalice Checks"
    visibility = Visibility.template | Visibility.spoiler

class DlcDicePalaceChaliceChecks(Toggle):
    """
    --NOT YET IMPLEMENTED--
    -DLC ONLY-
    -REQUIRES CHALICE-
    -REQUIRES KINGDICE BOSSSANITY-
    Enable checks for completing Kingdice Bossanity checks as Ms. Chalice.
    """
    display_name = "[DLC] Kingdice Chalice Checks"
    visibility = Visibility.template | Visibility.spoiler

class DlcChessChaliceChecks(Toggle):
    """
    --NOT YET IMPLEMENTED--
    -DLC ONLY-
    -REQUIRES CHALICE-
    -REQUIRES THE KING'S LEAP-
    Enable checks for completing The King's Leap checks as Ms. Chalice.
    """
    display_name = "[DLC] Chess Chalice Checks"
    visibility = Visibility.template | Visibility.spoiler

class SilverworthQuest(DefaultOnToggle):
    """
    Enable the Silverworth Quest check.
    This means that you will have to beat 15 levels with at least an A- Grade in order to get this check.
    """
    display_name = "Silverworth Quest"

class PacifistQuest(Toggle):
    """
    Enable the Pacifist Quest check.
    This means that you will have to beat all 6 Run n' Gun levels without beating any enemies (not easy).
    """
    display_name = "Pacifist Quest"

class DicePalaceBossSanity(Toggle):
    """
    ---NOT YET IMPLEMENTED---
    Enable checks for beating the Kingdice mini-bosses.
    There is an indicator for which mini-bosses you defeated.
    """
    display_name = "Kingdice BossSanity"
    visibility = Visibility.template | Visibility.spoiler

class TrapLoadoutAnyWeapon(Toggle):
    """
    For Loadout Mixup Trap:
    Allow Loadout Mixup to use any item including ones you do not currently have.
    """
    display_name = "Loadout Mixup Any Item"
    visibility = Visibility.spoiler

class DlcChaliceEnabled(Choice):
    """
    ---NOT YET IMPLEMENTED---
    -DLC ONLY-
    Enable Ms. Chalice and the Astral Cookie.
    Options:
    - Disabled: The cookie is disabled and cannot be obtained (Ms. Chalice is disabled).
    - Vanilla: The cookie is obtained at the start of the DLC (Vanilla Behavior).
    - Randomized: The cookie is in the item pool. Starting the DLC is a check.
    """
    display_name = "[DLC] Ms. Chalice"
    visibility = Visibility.template | Visibility.spoiler
    option_disabled = 0
    option_vanilla = 1
    option_randomized = 2
    default = 0

class DlcChaliceItemsSeparate(Choice):
    """
    ---NOT YET IMPLEMENTED---
    -DLC ONLY-
    Make certain items seperate for when playing as Ms. Chalice.
    Options:
    - Core Items: Core items like plane and supers.
    - Abilities: Abilities including parry.

    With parry for Ms. Chalice, the Parry item is replaced with Progressive Dash.
    Progressive Dash has two levels: 1. Dash only, 2. Dash with Parry.
    """
    display_name = "[DLC] Chalice Items Separate"
    visibility = Visibility.spoiler
    option_none = 0
    option_core_items = 3
    option_abilities = 4
    #option_core_and_abilities = 7
    #option_aim_abilities = 8
    #option_core_and_aim = 11
    #option_abilities_and_aim = 12
    option_all = 255
    default = 0

class DlcChessCastle(Choice):
    """
    -DLC ONLY-
    Choose how to handle the locations of The King's Leap.
    Gauntlet is the run where you have to defeat all the King's Leap bosses in succession.
    """
    display_name = "[DLC] The King's Leap"
    option_exclude = 0
    option_exclude_gauntlet = 1
    option_include_all = 3
    default = 1

class DlcCactusGirlQuest(Toggle):
    """
    ---NOT YET IMPLEMENTED---
    -DLC ONLY-
    -REQUIRES CHALICE-
    Enable the Cactus Girl Quest (aka Ms. Chalice Quest) check.
    This means that you will have to beat EVERY boss as Ms. Chalice (tedious) for a single check.
    You can talk to the Cactus Girl to know which bosses you need to defeat still.
    """
    display_name = "[DLC] Cactus Girl Quest"
    visibility = Visibility.template | Visibility.spoiler

class DlcCurseMode(Choice):
    """
    -DLC ONLY-
    Set how the cursed and devine relic is handled.

    Modes:
    - Off: Broken Relic is removed from the game
    - Normal: Broken Relic is in pool. The graveyard and getting the devine relic is excluded from logic.
    """
    display_name = "[DLC] Curse Mode"
    option_off = 0
    option_normal = 1
    #option_reverse = 2
    #option_always_on = 3
    #option_always_on_r = 4
    #option_always_on_1 = 5
    #option_always_on_2 = 6
    #option_always_on_3 = 7
    #option_always_on_4 = 8
    default = 0

class ExtraCoins(Range):
    """
    Set extra coins in the item pool.
    """
    display_name = "Extra Coins"
    range_start = 0
    range_end = 10
    default = 0

class StartMaxHealth(Range):
    """
    Set starting max health.
    NOTE: Health cannot be any higher than 9, so health charms would be less useful at higher health amounts.
    """
    display_name = "Starting Max Health"
    range_start = 1
    range_end = 4
    default = 3

class MaxHealthUpgrades(Range):
    """
    Set number of max health upgrades in the pool.
    NOTE: Health cannot be any higher than 9, so health charms would be less useful at higher health amounts.
    """
    display_name = "Max Health Upgrades"
    range_start = 0
    range_end = 3
    default = 0

class MinimumFillerItems(Range):
    """
    Set the minimum amount of filler items that should exist in this world.
    NOTE: If there are not enough locations, some coins will be compressed into packs of 2 or 3 to make space.
    """
    display_name = "Minimum Filler Items"
    range_start = 0
    range_end = 10
    default = 0

class FillerWeightExtraHealth(Weight):
    """
    Set Extra Health weight. Higher weight means it will more likely appear compared to other filler items.
    Set to 0 to disable this item.
    """
    display_name = "Extra Health Weight"
    default = 3
class FillerWeightSuperRecharge(Weight):
    """
    Set Super Recharge weight. Higher weight means it will more likely appear compared to other filler items.
    Set to 0 to disable this item.
    """
    display_name = "Super Recharge Weight"
    default = 3
class FillerWeightFastFire(Weight):
    """
    Set Fast Fire weight. Higher weight means it will more likely appear compared to other filler items.
    Set to 0 to disable this item.
    """
    display_name = "Fast Fire Weight"
    visibility = Visibility.none
    default = 0

class Traps(Range):
    """
    ---NOT YET IMPLEMENTED ON CLIENT---
    Set Trap percentage for filler items.
    """
    display_name = "Traps"
    visibility = Visibility.template | Visibility.spoiler
    range_start = 0
    range_end = 100
    default = 0
class TrapWeightFingerJam(Weight):
    """
    Set Finger Jam Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    display_name = "Finger Jam Trap Weight"
    visibility = Visibility.none
    default = 5
class TrapWeightSlowFire(Weight):
    """
    Set Slow Fire Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    display_name = "Slow Fire Trap Weight"
    visibility = Visibility.none
    default = 5
class TrapWeightSuperDrain(Weight):
    """
    Set Super Drain Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    display_name = "Super Drain Trap Weight"
    visibility = Visibility.none
    default = 5
class TrapWeightLoadout(Weight):
    """
    Set Loadout Mixup Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    display_name = "Loadout Mixup Trap Weight"
    visibility = Visibility.none
    default = 5
class TrapWeightScreen(Weight):
    """
    Set Screen Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    display_name = "Screen Trap Weight"
    visibility = Visibility.none
    default = 3

class MusicShuffle(Choice):
    """
    ---NOT YET IMPLEMENTED ON CLIENT---
    Enable Shuffling Music.
    NOTE: This option will do nothing until the client is updated
    """
    display_name = "Music Rando"
    visibility = Visibility.none
    option_disabled = 0
    option_level_music = 1
    option_map_music = 2
    option_level_and_map_music = 3
    #option_all_music = 255
    default = 0

class DeathLink(Toggle):
    """
    Enable Deathlink. When you die, everyone dies. Of course the reverse is true too.
    In Cuphead, this only applies while you are in a level.
    """
    display_name = "Death Link"

@dataclass
class CupheadOptions(PerGameCommonOptions):
    version: Version
    use_dlc: DeliciousLastCourse
    mode: GameMode
    expert_mode: ExpertMode
    start_weapon: StartWeapon
    randomize_weapon_ex: RandomizeWeaponEx
    start_maxhealth: StartMaxHealth
    contract_requirements: ContractRequirements
    dlc_ingredient_requirements: DlcIngredientRequirements
    contract_goal_requirements: ContractGoalRequirements
    dlc_ingredient_goal_requirements: DlcIngredientGoalRequirements
    level_shuffle: LevelShuffle
    freemove_isles: FreeMoveIsles
    deathlink: DeathLink
    #weapon_gate: WeaponGate
    randomize_abilities: RandomizeAbilities
    #randomize_abilities_aim: RandomizeAimAbilities
    boss_secret_checks: BossSecretChecks
    boss_grade_checks: BossGradeChecks
    rungun_grade_checks: RunGunGradeChecks
    kingdice_bosssanity: DicePalaceBossSanity
    dlc_boss_chalice_checks: DlcBossChaliceChecks
    dlc_rungun_chalice_checks: DlcRunGunChaliceChecks
    dlc_kingdice_chalice_checks: DlcDicePalaceChaliceChecks
    dlc_chess_chalice_checks: DlcChessChaliceChecks
    silverworth_quest: SilverworthQuest
    pacifist_quest: PacifistQuest
    dlc_chalice: DlcChaliceEnabled
    #dlc_chalice_items_separate: DlcChaliceItemsSeparate
    dlc_kingsleap: DlcChessCastle
    dlc_cactusgirl_quest: DlcCactusGirlQuest
    dlc_curse_mode: DlcCurseMode
    extra_coins: ExtraCoins
    maxhealth_upgrades: MaxHealthUpgrades
    minimum_filler: MinimumFillerItems
    traps: Traps
    filler_weight_extrahealth: FillerWeightExtraHealth
    filler_weight_superrecharge: FillerWeightSuperRecharge
    filler_weight_fastfire: FillerWeightFastFire
    trap_loadout_anyweapon: TrapLoadoutAnyWeapon
    trap_weight_fingerjam: TrapWeightFingerJam
    trap_weight_slowfire: TrapWeightSlowFire
    trap_weight_superdrain: TrapWeightSuperDrain
    trap_weight_loadout: TrapWeightLoadout
    music_shuffle: MusicShuffle

cuphead_option_groups = [
    OptionGroup("Main", [
        DeliciousLastCourse,
        GameMode,
        ExpertMode,
        StartWeapon,
        RandomizeWeaponEx,
        StartMaxHealth,
        FreeMoveIsles,
        #WeaponGate,
        RandomizeAbilities,
        #RandomizeAimAbilities,
        DeathLink,
    ]),
    OptionGroup("DLC Main", [
        DlcIngredientRequirements,
        DlcChaliceEnabled,
        DlcCurseMode,
    ]),
    OptionGroup("Checks", [
        BossSecretChecks,
        BossGradeChecks,
        RunGunGradeChecks,
        SilverworthQuest,
        PacifistQuest,
        DicePalaceBossSanity,
    ]),
    OptionGroup("DLC Checks", [
        DlcChessCastle,
        DlcBossChaliceChecks,
        DlcRunGunChaliceChecks,
        DlcDicePalaceChaliceChecks,
        DlcChessChaliceChecks,
        DlcCactusGirlQuest,
    ]),
    OptionGroup("Items", [
        ExtraCoins,
        MaxHealthUpgrades,
        MinimumFillerItems,
        Traps,
        DlcChaliceItemsSeparate,
    ]),
    #OptionGroup("Misc", [
    #    TrapLoadoutAnyWeapon,
    #    MusicShuffle,
    #]),
    OptionGroup("Item Weights", [
        FillerWeightExtraHealth,
        FillerWeightSuperRecharge,
        FillerWeightFastFire,
        TrapWeightFingerJam,
        TrapWeightSlowFire,
        TrapWeightSuperDrain,
        TrapWeightLoadout,
    ], True),
]
