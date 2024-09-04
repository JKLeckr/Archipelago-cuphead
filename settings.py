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
    level_shuffle: bool
    #shop_shuffle: bool
    freemove_isles: bool
    weapon_gate: bool
    randomize_abilities: bool
    traps: int
    filler_item_weights: list[int, int]
    trap_weights: list[int, int, int, int, int]
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
    filler_item_buffer: int

    def __init__(self, options: CupheadOptions) -> None:
        self.use_dlc = options.use_dlc
        self.mode = GameMode(options.mode)
        self.hard_logic = False #options.hard_logic
        self.expert_mode = options.expert_mode
        self.start_weapon = int(options.start_weapon)
        self.level_shuffle = options.level_shuffle
        #self.shop_shuffle = options.shop_shuffle
        self.freemove_isles = options.freemove_isles
        self.weapon_gate = False #options.weapon_gate
        self.randomize_abilities = options.randomize_abilities
        self.boss_grade_checks = GradeCheckMode(options.boss_grade_checks)
        self.rungun_grade_checks = GradeCheckMode(options.rungun_grade_checks)
        self.boss_secret_checks = options.boss_secret_checks
        self.dlc_boss_chalice_checks = False #options.dlc_boss_chalice_checks
        self.fourparries_quest = True
        self.ginger_quest = True
        self.fourmel_quest = True
        self.lucien_quest = False
        self.agrade_quest = options.agrade_quest
        self.pacifist_quest = options.pacifist_quest
        self.music_quest = False
        self.dlc_cactusgirl_quest = False #options.dlc_cactusgirl_quest
        self.traps = options.traps
        self.trap_weights = self._get_trap_weights(options)
        self.filler_item_weights = self._get_filler_item_weights(options)
        self.coin_amounts = self._get_coin_amounts(options)
        self.contract_requirements = (5,10,17)
        self.dlc_ingredient_requirements = 5
        self.require_secret_shortcuts = True
        self.filler_item_buffer = 0

    def _get_coin_amounts(self, options: CupheadOptions) -> tuple[int]:
        total_single_coins = 40 if self.use_dlc else 37
        total_double_coins = 5 if self.use_dlc else 0
        total_triple_coins = 2 if self.use_dlc else 1

        return (total_single_coins, total_double_coins, total_triple_coins)

    def _get_filler_item_weights(self, options: CupheadOptions) -> list[int]:
        return [
            options.filler_weight_extrahealth,
            options.filler_weight_superrecharge,
        ]

    def _get_trap_weights(self, options: CupheadOptions) -> list[int]:
        return [
            options.trap_weight_fingerjam,
            options.trap_weight_slowfire,
            options.trap_weight_superdrain,
            options.trap_weight_reversal,
            0, #options.trap_weight_enviro
        ]
