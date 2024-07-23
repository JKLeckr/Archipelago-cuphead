from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Range, Choice, Option, DeathLink, PerGameCommonOptions

class DeliciousLastCourse(Toggle):
    """
    Whether or not to use Delicious Last Course content (Requires owning the DLC)
    """
    display_name = "DLC"

class ExpertMode(Toggle):
    """Sets the boss difficulty to expert"""
    display_name = "Expert Mode"

class StartWeapon(Choice):
    """
    Weapon to start with
    NOTE: If DLC is not enabled, picking DLC weapons will pick a random weapon instead
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
    """Shuffles the Boss and Run n' Gun levels"""
    display_name = "Level Shuffle"

class FreeMoveIsles(Toggle):
    """Allows all the bosses on each island to be freely accessible without completing a previous level first"""
    display_name = "Free Move Islands"

class WeaponGate(Toggle):
    """
    --NOT YET IMPLEMENTED--
    Adds a weapon gate which only allows specific weapons for each fight
    """
    display_name = "Weapon Gate"

class RandomizeAbilities(DefaultOnToggle):
    """Randomize essential abilities like Duck, Perry, Dash, etc."""
    display_name = "Randomize Abilities"

class RandomizeAimAbilities(Toggle):
    """
    --NOT YET IMPLEMENTED--
    Randomize aiming abilities. You will start with only top-right
    """
    display_name = "Randomize Aim Abilities"

class BossGradeChecks(Choice):
    """
    Enable grade checks for Boss Levels
    NOTE: S Grade option will be treated as A+ Grade if Expert Mode is disabled
    """
    display_name = "Boss Grade Checks"
    option_disabled = 0
    option_a_grade = 1
    option_aplus_grade = 2
    option_s_grade = 3
    default = 0

class RunGunGradeChecks(Choice):
    """
    Enable grade checks for Run n' Gun levels
    Pacifist: Beat the level without killing any monsters (not easy)
    """
    display_name = "Run n' Gun Grade Checks"
    option_disabled = 0
    option_a_grade = 1
    option_aplus_grade = 2
    option_pacifist = 4
    alias_p_grade = 4
    default = 0

class DlcBossChaliceChecks(Toggle):
    """
    -DLC ONLY-
    Enable checks for defeating each boss as Ms. Chalice
    """
    display_name = "[DLC] Boss Chalice Checks"

class AGradeQuest(DefaultOnToggle):
    """
    Enable the 15 A-Grade Quest check
    This means that you will have to beat 15 levels with at least an A-Grade in order to get this check
    """
    display_name = "15 A-Grade Quest"

class PacifistQuest(Toggle):
    """
    Enable the Pacifist Quest check
    This means that you will have to beat all 6 Run n' Gun levels without killing any monsters in order to get this check (not easy)
    """
    display_name = "Pacifist Quest"

class DlcCactusGirlQuest(Toggle):
    """
    -DLC ONLY-
    Enable the Cactus Girl Quest (aka Ms. Chalice Quest) check
    This means that you will have to beat EVERY boss as Ms. Chalice (tedious) for a single check
    You can talk to the Cactus Girl to know which bosses you need to defeat still
    """
    display_name = "[DLC] Cactus Girl Quest"

class Traps(Range):
    """
    Set Trap percentage for filler items.
    """
    display_name = "Traps"
    range_start = 0
    range_end = 100
    default = 0

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
    boss_grade_checks: BossGradeChecks
    rungun_grade_checks: RunGunGradeChecks
    #dlc_boss_chalice_checks: DlcBossChaliceChecks
    agrade_quest: AGradeQuest
    pacifist_quest: PacifistQuest
    #dlc_cactusgirl_quest: DlcCactusGirlQuest
    traps: Traps
    deathlink: DeathLink
