from dataclasses import dataclass
from Options import Toggle, Range, Choice, PerGameCommonOptions

class Weight(Range):
    range_start = 0
    range_end = 10
    weight_max = 100

    def __init__(self, value: int):
        if value < 0:
            raise Exception(f"Option {self.__class__.__name__} cannot be negative!")
        elif value > self.weight_max:
            raise Exception(f"Option {self.__class__.__name__} cannot be larger than {self.weight_max}!")
        self.value = value

class DeliciousLastCourse(Toggle):
    """
    --DLC NOT FULLY IMPLEMENTED!--
    Set whether or not to use Delicious Last Course content (Requires owning the DLC).
    """
    display_name = "DLC"

class Mode(Choice):
    """
    --ONLY DEFAULT CHOICE WORKS--
    Set the mode of the randomizer which includes goal.
    NOTE: Setting dlc
    """
    display_name = "Mode"
    option_beat_devil = 0
    option_dlc_beat_devil = 1
    option_dlc_beat_saltbaker = 2
    option_dlc_beat_both = 3
    option_dlc_beat_saltbaker_isle4_only = 4
    default = 0

class HardLogic(Toggle):
    """
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

class StartWeapon(Choice):
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
    default = 0

class LevelShuffle(Toggle):
    """
    --NOT YET IMPLEMENTED--
    Shuffle the Boss and Run n' Gun levels.
    """
    display_name = "Level Shuffle"

class FreeMoveIsles(Toggle):
    """
    Allow all the levels on each island to be freely accessible without completing a previous level first.
    """
    display_name = "Free Move Islands"

class WeaponGate(Toggle):
    """
    --NOT YET IMPLEMENTED--
    Add a weapon gate which only allows specific weapons for each fight.
    """
    display_name = "Weapon Gate"

class RandomizeAbilities(Toggle):
    """
    Randomize essential abilities like Duck, Perry, Dash, etc.
    """
    display_name = "Randomize Abilities"

class RandomizeAimAbilities(Toggle):
    """
    --NOT YET IMPLEMENTED--
    Randomize aiming abilities.
    You will start with only top-right.
    """
    display_name = "Randomize Aim Abilities"

class BossSecretChecks(Toggle):
    """
    Also include beating the secret phases of the three bosses as checks.
    The three boss levels include: Botanic Panic, Pyramid Peril, and Dramatic Fanatic.
    The secret phases are more difficult than the normal fight.
    """
    display_name = "Boss Secret Checks"

class BossGradeChecks(Choice):
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
    default = 0

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
    default = 0

class DlcBossChaliceChecks(Toggle):
    """
    -DLC ONLY-
    Enable checks for defeating each boss as Ms. Chalice.
    """
    display_name = "[DLC] Boss Chalice Checks"

class AGradeQuest(Toggle): # TODO: Maybe make this on by default later.
    """
    Enable the 15 A-Grade Quest check.
    This means that you will have to beat 15 levels with at least an A-Grade in order to get this check.
    """
    display_name = "15 A-Grade Quest"

class PacifistQuest(Toggle):
    """
    Enable the Pacifist Quest check.
    This means that you will have to beat all 6 Run n' Gun levels without killing any monsters in order to get this check (not easy).
    """
    display_name = "Pacifist Quest"

class DlcCactusGirlQuest(Toggle):
    """
    -DLC ONLY-
    Enable the Cactus Girl Quest (aka Ms. Chalice Quest) check.
    This means that you will have to beat EVERY boss as Ms. Chalice (tedious) for a single check.
    You can talk to the Cactus Girl to know which bosses you need to defeat still.
    """
    display_name = "[DLC] Cactus Girl Quest"

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
    range_end = 5
    default = 0

class Traps(Range):
    """
    Set Trap percentage for filler items.
    """
    display_name = "Traps"
    range_start = 0
    range_end = 100
    default = 0
class TrapWeightFingerJam(Weight):
    """
    Set Finger Jam Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    display_name = "Finger Jam Trap Weight"
    default = 3
class TrapWeightSlowFire(Weight):
    """
    Set Slow Fire Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    display_name = "Slow Fire Trap Weight"
    default = 3
class TrapWeightSuperDrain(Weight):
    """
    Set Super Drain Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    display_name = "Super Drain Trap Weight"
    default = 3
class TrapWeightReversal(Weight):
    """
    Set Reversal Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    display_name = "Reversal Trap Weight"
    default = 3
class TrapWeightEnviro(Weight):
    """
    Set Envirotrap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    display_name = "Envirotrap Weight"
    default = 0

class DeathLink(Toggle):
    """
    When you die, everyone dies. Of course the reverse is true too.
    In Cuphead, this only applies while you are in a level.
    """
    display_name = "Death Link"

@dataclass
class CupheadOptions(PerGameCommonOptions):
    use_dlc: DeliciousLastCourse
    expert_mode: ExpertMode
    start_weapon: StartWeapon
    level_shuffle: LevelShuffle
    freemove_isles: FreeMoveIsles
    #weapon_gate: WeaponGate
    randomize_abilities: RandomizeAbilities
    #randomize_abilities_aim: RandomizeAimAbilities
    boss_secret_checks: BossSecretChecks
    boss_grade_checks: BossGradeChecks
    rungun_grade_checks: RunGunGradeChecks
    #dlc_boss_chalice_checks: DlcBossChaliceChecks
    agrade_quest: AGradeQuest
    pacifist_quest: PacifistQuest
    #dlc_cactusgirl_quest: DlcCactusGirlQuest
    traps: Traps
    trap_weight_fingerjam: TrapWeightFingerJam
    trap_weight_slowfire: TrapWeightSlowFire
    trap_weight_superdrain: TrapWeightSuperDrain
    trap_weight_reversal: TrapWeightReversal
    #trap_weight_enviro: TrapWeightEnviro
    deathlink: DeathLink
