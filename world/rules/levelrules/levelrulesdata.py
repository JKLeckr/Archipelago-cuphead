### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from typing import Any, ClassVar

from ... import data
from . import levelrulebase as lrb
from .levelrulebase import LevelDef, LevelRules, RuleContainer


class LevelRuleData:
    _data: ClassVar[LevelRules | None] = None

    @staticmethod
    def _compile_levelruledata(levelrules_json: dict[str, Any], presets_json: dict[str, Any]) -> LevelRules:
        levelrule_presets: dict[str, RuleContainer] = {}
        levelrules: dict[str, LevelDef] = {}

        _proot = presets_json.get("presets", {})
        for name, preset in _proot.items():
            pass

        return lrb.LevelRules(levelrules, levelrule_presets)

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
    def get_data(cls):
        if not cls._data:
            cls._load_levelrule_data()
        return cls._data
