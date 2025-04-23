from __future__ import annotations
from random import Random
from collections.abc import Iterable
from Options import NumericOption, OptionSet
from ..auxiliary import format_list
from .options import CupheadOptions

class OptionSanitizer:
    option_overrides: list[str] = []

    def __init__(self, player: int, options: CupheadOptions, random: Random, log_overrides: bool):
        self.option_overrides = []
        self.player = player
        self.options = options
        self.random = random
        self.log_overrides: bool = log_overrides

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
        option.value.difference_update(values)

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
        if ABILITIES_VAL in _options.dlc_chalice_items_separate.value and not _options.randomize_abilities:
            self.override_option_set(
                _options.dlc_chalice_items_separate,
                {ABILITIES_VAL},
                False,
                "Randomize Abilities Off",
                quiet
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

    def sanitize_options(self) -> None:
        _options = self.options

        CONTRACT_GOAL_REASON = "Contract Goal cannot be less than requirements"

        # Sanitize settings
        if _options.contract_goal_requirements.value < _options.contract_requirements.value:
            self.override_num_option(
                _options.contract_goal_requirements,
                _options.contract_requirements.value,
                CONTRACT_GOAL_REASON
            )
        if (_options.use_dlc and \
            _options.dlc_ingredient_goal_requirements.value < _options.dlc_ingredient_requirements.value):
            self.override_num_option(
                _options.dlc_ingredient_goal_requirements,
                _options.dlc_ingredient_requirements.value,
                CONTRACT_GOAL_REASON
            )
        self._sanitize_dlc_options()
        # Sanitize grade checks
        if not _options.expert_mode and _options.boss_grade_checks.value>3:
            self.override_num_option(_options.boss_grade_checks, 3, "Expert Off")
