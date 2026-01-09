### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from typing import Any, ClassVar

from ... import data
from ..deps import DEPS
from .levelrulebase import LevelDef, LevelRules, LocationDef, RuleContainer, RuleDep, RuleExpr, RuleFragment, LRule
from .levelrules import LRULES


class LevelRuleData:
    _data: ClassVar[LevelRules | None] = None

    @staticmethod
    def _compile_levelrule(lrule: str, *, src: str) -> LRule:
        try:
            _expr = LRULES[lrule]
        except KeyError as e:
            raise KeyError(f"From {src}: '{lrule}' is not a valid level rule!") from e
        return LRule(_expr, lrule)

    @staticmethod
    def _compile_rule_expr(json_obj: dict[str, Any], *, src: str) -> RuleExpr:
        switch json_obj

    @staticmethod
    def _compile_ruledeps(depname: str, *, src: str) -> RuleDep:
        negated = depname.startswith("!")
        dname = depname[1:] if negated else depname

        try:
            dep = DEPS[dname]
        except KeyError as e:
            raise KeyError(f"From {src}: '{depname}' is not a valid dep!") from e

        return RuleDep(dep, negated, depname)

    @staticmethod
    def _compile_rule_fragment(json_obj: dict[str, Any], *, src: str) -> RuleFragment:
        when_json: list[str] = json_obj.get("when", [])
        requires_json: dict[str, Any] | None = json_obj.get("requires")

        if not requires_json:
            raise ValueError(f"{src}.requires is required")
        if not isinstance(when_json, list): # type: ignore
            raise ValueError(f"{src}.when must be a list")

        when = [
            __class__._compile_ruledeps(dep, src=f"{src}.when")
            for dep in when_json
        ]

        requires = __class__._compile_rule_expr(
            requires_json,
            src=f"${src}.requires"
        )

        return RuleFragment(when, requires, src)

    @staticmethod
    def _compile_rule_container(json_obj: dict[str, Any], *, src: str) -> RuleContainer:
        rules_json: list[dict[str, Any]] = json_obj.get("rules", [])
        if not isinstance(rules_json, list): # type: ignore
            raise ValueError(f"{src}.rules must be a list")

        rules = [
            __class__._compile_rule_fragment(rule_json, src=f"{src}.rules['{i}']")
            for i, rule_json in enumerate(rules_json)
        ]

        return RuleContainer(rules, src)

    @staticmethod
    def _compile_loc(json_obj: dict[str, Any], *, src: str) -> LocationDef:
        pass

    @staticmethod
    def _compile_level(json_obj: dict[str, Any], *, src: str) -> LevelDef:
        pass

    @staticmethod
    def _compile_levelruledata(levelrules_json: dict[str, Any], presets_json: dict[str, Any]) -> LevelRules:
        levelrule_presets: dict[str, RuleContainer] = {}
        levelrules: dict[str, LevelDef] = {}

        _proot = presets_json.get("presets", {})
        for pname, preset_json in _proot.items():
            levelrule_presets[pname] = __class__._compile_rule_container(
                preset_json,
                src=f"presets.{pname}"
            ) # TODO: Resolve presets to the actual rule containers instead of simply string references.

        _lrroot = levelrules_json.get("levels", {})
        for lname, level_json in _lrroot.items():
            levelrules[lname] = __class__._compile_level(
                level_json,
                src=f"levels.{lname}"
            )

        return LevelRules(levelrules, levelrule_presets)

    @classmethod
    def _load_levelrule_data(cls):
        data.load_data("levelrulepresets")
        data.load_data("levelruledefs")

        _json_data = data.get_json_data("levelruledefs")
        _json_presets_data = data.get_json_data("levelrulepresets")

        if not isinstance(_json_data, dict):
            raise ValueError("Level rules JSON must be an object")
        if not isinstance(_json_presets_data, dict):
            raise ValueError("Preset rules JSON must be an object")

        cls._data = cls._compile_levelruledata(_json_data, _json_presets_data) # pyright: ignore[reportUnknownArgumentType]

        data.unload_data("levelrulepresets")
        data.unload_data("levelruledefs")

    @classmethod
    def get_data(cls) -> LevelRules:
        if not cls._data:
            cls._load_levelrule_data()
        if cls._data:
            return cls._data
        raise ValueError("Could not load levelrule data")
