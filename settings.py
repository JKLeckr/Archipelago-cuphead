from __future__ import annotations
from enum import IntEnum
from .options import CupheadOptions

class GameMode(IntEnum):
    beat_devil = 0
    contracts = 1
    dlc_beat_devil = 2
    dlc_beat_saltbaker = 3
    dlc_beat_both = 4
    dlc_beat_saltbaker_isle4_only = 5
    dlc_ingradients = 6
class GradeCheckMode(IntEnum):
    disabled = 0
    a_minus_grade = 1
    a_grade = 2
    a_plus_grade = 3
    s_grade = 4
    pacifist = 5

# These are settings stored and accessed by other classes
class WorldSettings:
    use_dlc: bool
    mode: GameMode
    hard_logic: bool
    expert_mode: bool
    start_weapon: int
    start_maxhealth: int
    level_shuffle: bool
    #shop_shuffle: bool
    freemove_isles: bool
    weapon_gate: bool
    randomize_abilities: bool
    maxhealth_upgrades: int
    traps: int
    filler_item_weights: list[int]
    trap_weights: list[int]
    boss_grade_checks: GradeCheckMode
    rungun_grade_checks: GradeCheckMode
    boss_secret_checks: bool
    dlc_boss_chalice_checks: bool
    fourparries_quest: bool
    ginger_quest: bool
    fourmel_quest: bool
    lucien_quest: bool
    agrade_quest: bool
    pacifist_quest: bool
    music_quest: bool
    dlc_cactusgirl_quest: bool
    coin_amounts: tuple[int, int, int]
    contract_requirements: tuple[int, int, int]
    dlc_ingredient_requirements: int
    require_secret_shortcuts: bool
    minimum_filler: int

    def __init__(self, options: CupheadOptions) -> None:
        self.use_dlc = options.use_dlc.value
        self.mode = GameMode(options.mode.value)
        self.hard_logic = False #options.hard_logic.value
        self.expert_mode = options.expert_mode.value
        self.start_weapon = int(options.start_weapon.value)
        self.start_maxhealth = options.start_maxhealth.value
        self.level_shuffle = options.level_shuffle.value
        #self.shop_shuffle = options.shop_shuffle.value
        self.freemove_isles = options.freemove_isles.value
        self.weapon_gate = False #options.weapon_gate.value
        self.randomize_abilities = options.randomize_abilities.value
        self.boss_grade_checks = GradeCheckMode(options.boss_grade_checks.value)
        self.rungun_grade_checks = GradeCheckMode(options.rungun_grade_checks.value)
        self.boss_secret_checks = options.boss_secret_checks.value
        self.dlc_boss_chalice_checks = False #options.dlc_boss_chalice_checks.value
        self.fourparries_quest = True
        self.ginger_quest = True
        self.fourmel_quest = True
        self.lucien_quest = False
        self.agrade_quest = options.silverworth_quest.value
        self.pacifist_quest = options.pacifist_quest.value
        self.music_quest = False
        self.dlc_cactusgirl_quest = False #options.dlc_cactusgirl_quest
        self.maxhealth_upgrades = options.maxhealth_upgrades.value
        self.traps = options.traps.value
        self.trap_weights = self._get_trap_weights(options)
        self.filler_item_weights = self._get_filler_item_weights(options)
        self.coin_amounts = self._get_coin_amounts(options)
        self.contract_requirements = self._get_contract_requirements(options)
        self.dlc_ingredient_requirements = options.ingredient_requirements.value
        self.require_secret_shortcuts = True
        self.minimum_filler = options.minimum_filler.value

    def _get_coin_amounts(self, options: CupheadOptions) -> tuple[int, int, int]:
        total_single_coins = (40 if self.use_dlc else 37) + options.extra_coins.value
        total_double_coins = 5 if self.use_dlc else 0
        total_triple_coins = 2 if self.use_dlc else 1

        return (total_single_coins, total_double_coins, total_triple_coins)

    def _get_contract_requirements(self, options: CupheadOptions) -> tuple[int, int, int]:
        max_contracts = (5, 10, 17)
        total_req = options.contract_requirements.value
        distrib = total_req // 3
        die1 = min(distrib, max_contracts[0])
        die2 = die1 + min(distrib, max_contracts[1])

        return (die1, die2, total_req)

    def _get_filler_item_weights(self, options: CupheadOptions) -> list[int]:
        return [
            options.filler_weight_extrahealth.value,
            options.filler_weight_superrecharge.value,
            options.filler_weight_fastfire.value,
        ]

    def _get_trap_weights(self, options: CupheadOptions) -> list[int]:
        return [
            0, #options.trap_weight_fingerjam.value,
            0, #options.trap_weight_slowfire.value,
            3, #options.trap_weight_superdrain.value,
            0, #options.trap_weight_reverse.value,
            0, #options.trap_weight_screen.value,
        ]
