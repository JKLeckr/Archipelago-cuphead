from __future__ import annotations
from enum import IntEnum
from .names import LocationNames
from .options import CupheadOptions

class GameMode(IntEnum):
    beat_devil = 0
    collect_contracts = 1
    buy_out_shop = 2
    dlc_beat_saltbaker = 3
    dlc_beat_both = 4
    dlc_collect_ingredients = 5
    dlc_collect_both = 6
    dlc_beat_devil_no_isle4 = 7
    dlc_beat_saltbaker_isle4_only = 8
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
    level_shuffle_plane_separate: bool
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
    kingdice_bosssanity: bool
    dlc_boss_chalice_checks: bool
    fourparries_quest: bool
    ginger_quest: bool
    fourmel_quest: bool
    lucien_quest: bool
    silverworth_quest: bool
    pacifist_quest: bool
    music_quest: bool
    dlc_cactusgirl_quest: bool
    coin_amounts: tuple[int, int, int]
    contract_requirements: tuple[int, int, int]
    dlc_ingredient_requirements: int
    contract_goal_requirements: int
    dlc_ingredient_goal_requirements: int
    require_secret_shortcuts: bool
    dlc_randomize_boat: bool
    dlc_requires_mausoleum: bool
    dlc_chalice_items_separate: bool
    dlc_chesscastle_fullrun: bool
    minimum_filler: int
    trap_loadout_anyweapon: bool

    def __init__(self, options: CupheadOptions) -> None:
        self.use_dlc = bool(options.use_dlc.value)
        self.mode = GameMode(options.mode.value)
        self.hard_logic = False #bool(options.hard_logic.value)
        self.expert_mode = bool(options.expert_mode.value)
        self.start_weapon = int(options.start_weapon.value)
        self.start_maxhealth = options.start_maxhealth.value
        self.level_shuffle = bool(options.level_shuffle.value)
        self.level_shuffle_plane_separate = bool(options.level_shuffle_plane_separate)
        #self.shop_shuffle = bool(options.shop_shuffle.value)
        self.freemove_isles = bool(options.freemove_isles.value)
        self.weapon_gate = False #bool(options.weapon_gate.value)
        self.randomize_abilities = bool(options.randomize_abilities.value)
        self.boss_grade_checks = GradeCheckMode(options.boss_grade_checks.value)
        self.rungun_grade_checks = GradeCheckMode(options.rungun_grade_checks.value)
        self.boss_secret_checks = bool(options.boss_secret_checks.value)
        self.kingdice_bosssanity = bool(options.kingdice_bosssanity.value)
        self.dlc_boss_chalice_checks = bool(options.dlc_boss_chalice_checks.value)
        self.fourparries_quest = True
        self.ginger_quest = True
        self.fourmel_quest = True
        self.lucien_quest = False
        self.silverworth_quest = bool(options.silverworth_quest.value)
        self.pacifist_quest = bool(options.pacifist_quest.value)
        self.music_quest = False
        self.dlc_cactusgirl_quest = bool(options.dlc_cactusgirl_quest.value)
        self.maxhealth_upgrades = options.maxhealth_upgrades.value
        self.traps = options.traps.value
        self.trap_weights = self._get_trap_weights(options)
        self.filler_item_weights = self._get_filler_item_weights(options)
        self.coin_amounts = self._get_coin_amounts(options)
        self.contract_requirements = self._get_contract_requirements(options)
        self.dlc_ingredient_requirements = options.dlc_ingredient_requirements.value
        self.contract_goal_requirements = options.contract_goal_requirements.value
        self.dlc_ingredient_goal_requirements = options.dlc_ingredient_goal_requirements.value
        self.require_secret_shortcuts = True
        self.dlc_randomize_boat = True
        self.dlc_requires_mausoleum = True
        self.dlc_chalice_items_separate = False
        self.dlc_chesscastle_fullrun = True
        self.minimum_filler = options.minimum_filler.value
        self.trap_loadout_anyweapon = bool(options.trap_loadout_anyweapon.value)

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
            options.trap_weight_fingerjam.value,
            options.trap_weight_slowfire.value,
            options.trap_weight_superdrain.value,
            options.trap_weight_loadout.value,
            0,
        ]

    def is_goal_used(self, goal: str) -> bool:
        if goal == LocationNames.loc_event_goal_devil:
            return (
                self.mode == GameMode.beat_devil or
                self.mode == GameMode.dlc_beat_both or
                self.mode == GameMode.dlc_beat_devil_no_isle4
            )
        elif goal == LocationNames.loc_event_dlc_goal_saltbaker:
            return (
                self.mode == GameMode.dlc_beat_saltbaker or
                self.mode == GameMode.dlc_beat_both or
                self.mode == GameMode.dlc_beat_saltbaker_isle4_only
            )
        return False
