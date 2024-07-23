from enum import IntEnum
from BaseClasses import MultiWorld

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

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        self.use_dlc = multiworld.use_dlc[player]
        self.start_weapon = int(multiworld.start_weapon[player])
        self.level_shuffle = multiworld.level_shuffle[player]
        #self.shop_shuffle = multiworld.shop_shuffle[player]
        self.freemove_isles = multiworld.freemove_isles[player]
        self.weapon_gate = False #multiworld.weapon_gate[player]
        self.randomize_abilities = multiworld.randomize_abilities[player]
        self._boss_grade_checks = int(multiworld.boss_grade_checks[player])
        self._rungun_grade_checks = int(multiworld.rungun_grade_checks[player])
        self.dlc_boss_chalice_checks = False #multiworld.dlc_boss_chalice_checks[player]
        self.fourparries_quest = True
        self.ginger_quest = True
        self.fourmel_quest = True
        self.lucien_quest = True
        self.agrade_quest = multiworld.agrade_quest[player]
        self.pacifist_quest = multiworld.pacifist_quest[player]
        self.ludwig_quest = True
        self.wolfgang_quest = True
        self.dlc_cactusgirl_quest = False #multiworld.dlc_cactusgirl_quest[player]
        self.traps = multiworld.traps[player]
        self.contract_requirements = (5,10,17)
        self.dlc_ingredient_requirements = 5
        self.require_secret_shortcuts = True
        self.filler_item_buffer = 0
    def get_boss_grade_checks(self) -> GradeCheckMode:
        return GradeCheckMode(self._boss_grade_checks)
    def get_rungun_grade_checks(self) -> GradeCheckMode:
        return GradeCheckMode(self._rungun_grade_checks)
