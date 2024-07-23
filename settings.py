from enum import IntEnum
from Options import PerGameCommonOptions

class GradeCheckMode(IntEnum):
    disabled = 0
    a_grade = 1
    aplus_grade = 2
    s_grade = 3
    pacifist = 4

# These are settings stored and accessed by other classes
class WorldSettings:
    use_dlc: bool
    start_weapon: int
    level_shuffle: bool
    #shop_shuffle: bool
    freemove_isles: bool
    weapon_gate: bool
    randomize_abilities: bool
    traps: int
    _boss_grade_checks: int
    _rungun_grade_checks: int
    boss_secret_checks: bool
    dlc_boss_chalice_checks: bool
    fourparries_quest: bool
    ginger_quest: bool
    fourmel_quest: bool
    lucien_quest: bool
    agrade_quest: bool
    pacifist_quest: bool
    ludwig_quest: bool
    wolfgang_quest: bool
    dlc_cactusgirl_quest: bool
    contract_requirements: tuple[int,int,int]
    dlc_ingredient_requirements: int
    require_secret_shortcuts: bool
    filler_item_buffer: int

    def __init__(self, options: PerGameCommonOptions) -> None:
        self.use_dlc = options.use_dlc
        self.start_weapon = int(options.start_weapon)
        self.level_shuffle = options.level_shuffle
        #self.shop_shuffle = options.shop_shuffle
        self.freemove_isles = options.freemove_isles
        self.weapon_gate = False #options.weapon_gate
        self.randomize_abilities = options.randomize_abilities
        self._boss_grade_checks = int(options.boss_grade_checks)
        self._rungun_grade_checks = int(options.rungun_grade_checks)
        self.boss_secret_checks = False
        self.dlc_boss_chalice_checks = False #options.dlc_boss_chalice_checks
        self.fourparries_quest = True
        self.ginger_quest = True
        self.fourmel_quest = True
        self.lucien_quest = True
        self.agrade_quest = options.agrade_quest
        self.pacifist_quest = options.pacifist_quest
        self.ludwig_quest = True
        self.wolfgang_quest = True
        self.dlc_cactusgirl_quest = False #options.dlc_cactusgirl_quest
        self.traps = options.traps
        self.contract_requirements = (5,10,17)
        self.dlc_ingredient_requirements = 5
        self.require_secret_shortcuts = True
        self.filler_item_buffer = 0
    def get_boss_grade_checks(self) -> GradeCheckMode:
        return GradeCheckMode(self._boss_grade_checks)
    def get_rungun_grade_checks(self) -> GradeCheckMode:
        return GradeCheckMode(self._rungun_grade_checks)
