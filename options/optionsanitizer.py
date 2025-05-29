from __future__ import annotations
from random import Random
from collections.abc import Iterable
from Options import NumericOption, OptionSet
from ..auxiliary import format_list
from ..enums import ChaliceMode, LevelShuffleMode
from ..levels import levelshuffle, leveltype
from . import CupheadOptions

class OptionSanitizer:
    option_overrides: list[str] = []

    def __init__(
            self, player: int,
            options: CupheadOptions,
            random: Random,
            log_overrides: bool = True,
            sanitize_goal_options: bool = False
        ):
        self.option_overrides = []
        self.player = player
        self.options = options
        self.random = random
        self.log_overrides = log_overrides
        self.strict_goal_options = sanitize_goal_options

    def override_num_option(
            self,
            option: NumericOption,
            value: int,
            reason: str | None = None,
            quiet: bool = False
        ):
        string = f"{option.current_option_name}: \"{option.value}\" -> \"{value}\"."
        if reason:
            string += " Reason: {reason}"
        self.option_overrides.append(string)
        if self.log_overrides and not quiet:
            msg = f"Option \"{option.current_option_name}\" was overridden from \"{option.value}\" to \"{value}\"."
            msg_reason = f"Reason: {reason}."
            print(f"Warning: For player {self.player}: {msg} {msg_reason}")
        option.value = value

    def override_option_set(
            self,
            option: OptionSet,
            values: Iterable[str],
            add_mode: bool = False,
            reason: str | None = None,
            quiet: bool = False
        ):
        values_str = format_list(values, enc_start="\"", enc_end="\"")
        mode_str = "added to" if add_mode else "removed from"
        string = f"{option.current_option_name}: \"{values_str}\" {mode_str} set."
        if reason:
            string += " Reason: {reason}"
        self.option_overrides.append(string)
        if self.log_overrides and not quiet:
            msg = f"Option \"{option.current_option_name}\" was overridden with \"{values_str}\" {mode_str} set."
            msg_reason = f"Reason: {reason}."
            print(f"Warning: For player {self.player}: {msg} {msg_reason}")
        if add_mode:
            option.value.update(values)
        else:
            option.value.difference_update(values)

    def override_option_set_clear(
            self,
            option: OptionSet,
            reason: str | None = None,
            quiet: bool = False
        ):
        string = f"{option.current_option_name}: Set cleared."
        if reason:
            string += " Reason: {reason}"
        self.option_overrides.append(string)
        if self.log_overrides and not quiet:
            msg = f"Option \"{option.current_option_name}\" was overridden with set cleared."
            msg_reason = f"Reason: {reason}."
            print(f"Warning: For player {self.player}: {msg} {msg_reason}")
        option.value.clear()

    def _sanitize_dlc_chalice_options(self, quiet: bool = False) -> None:
        _options = self.options
        if _options.dlc_chalice.value == 0:
            CHALICE_REASON = "Chalice Off"
            if _options.dlc_boss_chalice_checks.value:
                self.override_num_option(_options.dlc_boss_chalice_checks, False, CHALICE_REASON, True)
            if _options.dlc_rungun_chalice_checks.value:
                self.override_num_option(_options.dlc_rungun_chalice_checks, False, CHALICE_REASON, True)
            if _options.dlc_kingdice_chalice_checks.value:
                self.override_num_option(_options.dlc_kingdice_chalice_checks, False, CHALICE_REASON, True)
            if _options.dlc_chess_chalice_checks.value:
                self.override_num_option(_options.dlc_chess_chalice_checks, False, CHALICE_REASON, True)
            if _options.dlc_cactusgirl_quest.value:
                self.override_num_option(_options.dlc_cactusgirl_quest, False, CHALICE_REASON, quiet)
        ABILITIES_VAL = "abilities"
        if len(_options.dlc_chalice_items_separate.value) > 0:
            if ABILITIES_VAL in _options.dlc_chalice_items_separate.value and not _options.randomize_abilities:
                self.override_option_set(
                    _options.dlc_chalice_items_separate,
                    {ABILITIES_VAL},
                    False,
                    "Randomize Abilities Off",
                    quiet
                )
            if not _options.dlc_chalice.value == int(ChaliceMode.CHALICE_ONLY):
                self.override_option_set_clear(
                    _options.dlc_chalice_items_separate,
                    "Chalice Mode is Chalice Only",
                    True
                )

    def _sanitize_dlc_options(self) -> None:
        _options = self.options
        use_dlc = _options.use_dlc.value
        if not use_dlc:
            DLC_REASON = "DLC Off"
            # Sanitize mode
            if _options.mode.value>2:
                self.override_num_option(_options.mode, self.random.randint(0,2), DLC_REASON)
            # Sanitize start_weapon
            if _options.start_weapon.value>5:
                self.override_num_option(_options.start_weapon, self.random.randint(0,5), DLC_REASON)
        self._sanitize_dlc_chalice_options(not use_dlc)

    def _sanitize_goal_requirements(self) -> None:
        _options = self.options

        _GOAL_REASON = "Goal cannot be less than requirements"

        # Sanitize settings
        if _options.contract_goal_requirements.value < _options.contract_requirements.value:
            self.override_num_option(
                _options.contract_goal_requirements,
                _options.contract_requirements.value,
                f"Contract {_GOAL_REASON}"
            )
        if (_options.use_dlc and \
            _options.dlc_ingredient_goal_requirements.value < _options.dlc_ingredient_requirements.value):
            self.override_num_option(
                _options.dlc_ingredient_goal_requirements,
                _options.dlc_ingredient_requirements.value,
                f"Ingredient {_GOAL_REASON}"
            )

    def _sanitize_level_placement(self) -> None:
        _options = self.options
        _value = _options.level_placements.value

        if len(_value) < 1:
            return

        valid_levels = {
            x
            for y in
                levelshuffle.get_level_shuffle_lists(
                        bool(_options.use_dlc),
                        LevelShuffleMode(_options.mode)
                )
            for x in y[0] if x not in y[1]
        }

        INVALID_LEVEL_REASON = "Invalid level"
        INVALID_LEVEL_COMBO_REASON = "Invalid level combination"

        for k,v in _value.items():
            drop = False
            drop_reason = ""
            if k in valid_levels and v in valid_levels:
                drop = True
                drop_reason = INVALID_LEVEL_REASON
            elif leveltype.get_level_type(k) != leveltype.get_level_type(v):
                drop = True
                drop_reason = INVALID_LEVEL_COMBO_REASON
            if drop:
                string = f"level_placements: \"{k}: {v}\" removed from dict. Reason: {drop_reason}."
                self.option_overrides.append(string)
                if self.log_overrides:
                    msg = f"Option \"level_placements\" was overridden with \"{k}: {v}\" removed from dict."
                    msg_reason = f"Reason: {drop_reason}."
                    print(f"Warning: For player {self.player}: {msg} {msg_reason}")
                _value.pop(k)

    def sanitize_options(self) -> None:
        _options = self.options

        if self.strict_goal_options:
            self._sanitize_goal_requirements()

        self._sanitize_dlc_options()

        self._sanitize_level_placement()

        # Sanitize grade checks
        if not _options.expert_mode and _options.boss_grade_checks.value>3:
            self.override_num_option(_options.boss_grade_checks, 3, "Expert Off")
