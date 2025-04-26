from __future__ import annotations
from .names import LocationNames
from .options import CupheadOptions
from . import enums as e

# These are settings stored and accessed by other classes
class WorldConfig:
    use_dlc: bool
    mode: e.GameMode
    hard_logic: bool
    expert_mode: bool
    start_weapon: int
    randomize_weapon_ex: e.WeaponExMode
    start_maxhealth: int
    level_shuffle: e.LevelShuffleMode
    freemove_isles: bool
    weapon_gate: bool
    randomize_abilities: bool
    randomize_abilities_aim: bool
    maxhealth_upgrades: int
    traps: int
    filler_item_weights: list[int]
    trap_weights: list[int]
    boss_grade_checks: e.GradeCheckMode
    rungun_grade_checks: e.GradeCheckMode
    boss_secret_checks: bool
    kingdice_bosssanity: bool
    dlc_boss_chalice_checks: bool
    dlc_rungun_chalice_checks: bool
    dlc_kingdice_chalice_checks: bool
    dlc_chess_chalice_checks: bool
    fourparries_quest: bool
    ginger_quest: bool
    fourmel_quest: bool
    lucien_quest: bool
    silverworth_quest: bool
    pacifist_quest: bool
    dlc_chalice: e.ChaliceMode
    music_quest: bool
    dlc_kingsleap: e.ChessCastleMode
    dlc_cactusgirl_quest: bool
    coin_amounts: tuple[int, int, int]
    contract_requirements: tuple[int, int, int]
    dlc_ingredient_requirements: int
    contract_goal_requirements: int
    dlc_ingredient_goal_requirements: int
    require_secret_shortcuts: bool
    dlc_randomize_boat: bool
    dlc_requires_mausoleum: bool
    dlc_chalice_items_separate: e.ItemGroups
    dlc_curse_mode: e.CurseMode
    minimum_filler: int
    trap_loadout_anyweapon: bool

    def __init__(self, options: CupheadOptions) -> None:
        self.use_dlc = bool(options.use_dlc.value)
        self.mode = e.GameMode(options.mode.value)
        self.hard_logic = False #bool(options.hard_logic.value)
        self.expert_mode = bool(options.expert_mode.value)
        self.start_weapon = int(options.start_weapon.value)
        self.randomize_weapon_ex = e.WeaponExMode(options.randomize_weapon_ex.value)
        self.start_maxhealth = options.start_maxhealth.value
        self.level_shuffle = e.LevelShuffleMode(options.level_shuffle.value)
        self.freemove_isles = bool(options.freemove_isles.value)
        self.weapon_gate = False #bool(options.weapon_gate.value)
        self.randomize_abilities = bool(options.randomize_abilities.value)
        self.randomize_abilities_aim = False #bool(options.randomize_abilities_aim.value)
        self.boss_grade_checks = e.GradeCheckMode(options.boss_grade_checks.value)
        self.rungun_grade_checks = e.GradeCheckMode(options.rungun_grade_checks.value)
        self.boss_secret_checks = bool(options.boss_secret_checks.value)
        self.kingdice_bosssanity = bool(options.kingdice_bosssanity.value)
        self.dlc_boss_chalice_checks = bool(options.dlc_boss_chalice_checks.value)
        self.dlc_rungun_chalice_checks = bool(options.dlc_rungun_chalice_checks.value)
        self.dlc_kingdice_chalice_checks = bool(options.dlc_kingdice_chalice_checks.value)
        self.dlc_chess_chalice_checks = bool(options.dlc_chess_chalice_checks.value)
        self.fourparries_quest = True
        self.ginger_quest = True
        self.fourmel_quest = True
        self.lucien_quest = False
        self.silverworth_quest = bool(options.silverworth_quest.value)
        self.pacifist_quest = bool(options.pacifist_quest.value)
        self.music_quest = False
        self.dlc_chalice = e.ChaliceMode(options.dlc_chalice.value)
        self.dlc_kingsleap = e.ChessCastleMode(options.dlc_kingsleap.value)
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
        self.dlc_chalice_items_separate = self._get_separate_items_mode(options)
        self.dlc_curse_mode = e.CurseMode.VANILLA
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
            options.filler_weight_supercharge.value,
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

    def _get_separate_items_mode(self, options: CupheadOptions) -> e.ItemGroups:
        _set = options.dlc_chalice_items_separate.value
        _val = e.ItemGroups.NONE

        def _get_bit(opt: str, item_group: e.ItemGroups) -> int:
            return item_group if opt in _set else e.ItemGroups.NONE

        _val |= _get_bit("core_items", e.ItemGroups.CORE_ITEMS) # TODO: Finish
        _val |= _get_bit("weapon_ex", e.ItemGroups.WEAPON_EX)
        _val |= _get_bit("abilities", e.ItemGroups.ABILITIES)

        return e.ItemGroups.NONE

    def is_dlc_chalice_items_separate(self, item_group: e.ItemGroups) -> bool:
        return (self.dlc_chalice_items_separate & item_group) > 0

    def is_goal_used(self, goal: str) -> bool:
        if goal == LocationNames.loc_event_goal_devil:
            return (
                self.mode == e.GameMode.BEAT_DEVIL or
                self.mode == e.GameMode.DLC_BEAT_BOTH or
                self.mode == e.GameMode.DLC_BEAT_DEVIL_NO_ISLE4
            )
        elif goal == LocationNames.loc_event_dlc_goal_saltbaker:
            return (
                self.mode == e.GameMode.DLC_BEAT_SALTBAKER or
                self.mode == e.GameMode.DLC_BEAT_BOTH or
                self.mode == e.GameMode.DLC_BEAT_SALTBAKER_ISLE4_ONLY
            )
        return False
