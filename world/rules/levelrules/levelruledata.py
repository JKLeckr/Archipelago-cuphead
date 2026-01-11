### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from typing import Any, ClassVar

from ... import data
from ..deps import DEPS
from . import levelrulebase as lrb
from .levelrulebase import (
    InheritMode,
    LevelDef,
    LevelRules,
    LocationDef,
    LRule,
    PresetRef,
    RuleContainer,
    RuleDep,
    RuleExpr,
    RuleFragment,
)
from .levelrules import LRULES


class LevelRuleData:
    _data: ClassVar[LevelRules | None] = None
    _preset_reg: ClassVar[dict[str, RuleContainer]] = {}

    @staticmethod
    def _compile_rule_combo(json_obj: dict[str, Any], *, src: str) -> RuleExpr:
        condition = "and" if "and" in json_obj else "or"
        children_json: list[dict[str, Any]] = json_obj[condition]
        if not isinstance(children_json, list): # type: ignore
            raise ValueError(f"{src}.{condition} must be a list")
        children = [
            __class__._compile_rule_expr(child, src=f"{src}.{condition}[{i}]")
            for i, child in enumerate(children_json)
        ]
        return lrb.And(src, children) if condition == "and" else lrb.Or(src, children)

    @staticmethod
    def _compile_levelrule(lrule: str, *, src: str) -> LRule:
        try:
            _expr = LRULES[lrule]
        except KeyError as e:
            raise KeyError(f"From {src}: '{lrule}' is not a valid level rule!") from e
        return LRule(src, _expr, lrule)

    @classmethod
    def _compile_preset_ref(cls, preset: str, *, src: str) -> PresetRef:
        if not isinstance(preset, str): # type: ignore
            raise ValueError(f"{src}.preset is not a valid string")

        if preset not in cls._preset_reg:
            raise KeyError(
                f"From {src}: Preset Reference '{preset}' does not exist or is not resolved!",
                f"Make sure you add '{preset}' to 'requires_presets' for preset '{src.split('.', 2)[1]}'."
            )

        preset_ref = cls._preset_reg[preset]
        return PresetRef(f"{src}.preset[{preset}]", preset_ref, preset)

    @staticmethod
    def _compile_rule_expr(json_obj: dict[str, Any], *, src: str) -> RuleExpr:
        if "rule" in json_obj:
            return __class__._compile_levelrule(json_obj["rule"], src=src)
        if "preset" in json_obj:
            return __class__._compile_preset_ref(json_obj["preset"], src=src)
        if "and" in json_obj or "or" in json_obj:
            return __class__._compile_rule_combo(json_obj, src=src)
        if "not" in json_obj:
            return lrb.Not(src, __class__._compile_rule_expr(json_obj["not"], src=f"{src}.not"))

        raise ValueError(f"{src} is an invalid rule expression")

    @staticmethod
    def _compile_ruledep(depname: str, *, src: str) -> RuleDep:
        negated = depname.startswith("!")
        dname = depname[1:] if negated else depname

        try:
            dep = DEPS[dname]
        except KeyError as e:
            raise KeyError(f"From {src}: '{depname}' is not a valid dep!") from e

        return RuleDep(src, dep, negated, depname)

    @staticmethod
    def _compile_rule_fragment(json_obj: dict[str, Any], *, src: str) -> RuleFragment:
        when_json: list[str] = json_obj.get("when", [])
        requires_json: dict[str, Any] | None = json_obj.get("requires")

        if not requires_json:
            raise ValueError(f"{src}.requires is required!")
        if not isinstance(when_json, list): # type: ignore
            raise ValueError(f"{src}.when must be a list!")

        when = [
            __class__._compile_ruledep(dep, src=f"{src}.when")
            for dep in when_json
        ]

        requires = __class__._compile_rule_expr(
            requires_json,
            src=f"${src}.requires"
        )

        return RuleFragment(src, when, requires)

    @staticmethod
    def _compile_rule_container(json_obj: dict[str, Any], *, src: str) -> RuleContainer:
        rules_json: list[dict[str, Any]] = json_obj.get("rules", [])
        if not isinstance(rules_json, list): # type: ignore
            raise ValueError(f"{src}.rules must be a list")

        rules = [
            __class__._compile_rule_fragment(rule_json, src=f"{src}.rules['{i}']")
            for i, rule_json in enumerate(rules_json)
        ]

        return RuleContainer(src, rules)

    @staticmethod
    def _compile_lloc(json_obj: dict[str, Any], *, src: str) -> LocationDef:
        rule = (
            __class__._compile_rule_container(json_obj["rule"], src=f"{src}.rule")
            if "rule" in json_obj
            else None
        )

        inherit_raw = json_obj.get("inherit", "none")
        if not isinstance(inherit_raw, str):
            raise ValueError(f"{src}.inherit is not a valid string!")
        match inherit_raw:
            case "and":
                inherit = InheritMode.AND
            case "or":
                inherit = InheritMode.OR
            case "none":
                inherit = InheritMode.NONE
            case _:
                raise ValueError(f"{src}.inherit needs to be one of: [and,or,none]")

        return LocationDef(src, rule, inherit)

    @staticmethod
    def _compile_level(json_obj: dict[str, Any], *, src: str) -> LevelDef:
        access = (
            __class__._compile_rule_container(json_obj["access"], src=f"{src}.access")
            if "access" in json_obj
            else None
        )

        base = (
            __class__._compile_rule_container(json_obj["base"], src=f"{src}.base")
            if "base" in json_obj
            else None
        )

        locations: dict[str, LocationDef] = {}
        locs_json: dict[str, Any] = json_obj.get("locations", {})
        if not isinstance(locs_json, dict): # type: ignore
            raise ValueError(f"{src}.locations is an invalid json object!")
        for name, loc_json in locs_json.items():
            locations[name] = __class__._compile_lloc(loc_json, src=f"{src}.locations.{name}")

        return LevelDef(src, access, base, locations)

    @classmethod
    def _compile_preset(cls, json_obj: dict[str, Any], *, name: str, src: str) -> RuleContainer:
        res = __class__._compile_rule_container(json_obj, src=src)
        if name in cls._preset_reg:
            raise KeyError(f"From {src}: '{name}' already is registered!")
        cls._preset_reg[name] = res
        return res

    @staticmethod
    def _toposort_presets(graph: dict[str, set[str]]) -> list[str]:
        res: list[str] = []
        visiting: set[str] = set()
        visited: set[str] = set()

        def dfs(node: str):
            if node in visiting:
                raise ValueError(f"Preset cycle with '{node}'")
            if node in visited:
                return

            visiting.add(node)
            for dep in graph[node]:
                if dep not in graph:
                    raise ValueError(f"Preset '{node}' depends on unknown preset '{dep}'")
                dfs(dep)
            visiting.remove(node)

            visited.add(node)
            res.append(node)

        for name in graph:
            if name not in visited:
                dfs(name)

        return res

    @staticmethod
    def _compile_presets(presets_json: dict[str, Any], *, src: str) -> dict[str, RuleContainer]:
        preset_req_graph: dict[str, set[str]] = {name: set() for name in presets_json}

        for pname, preset_json in presets_json.items():
            preset_reqs: list[str] = preset_json["requires_presets"]
            if isinstance(preset_reqs, list): # type: ignore
                preset_req_graph[pname] = set(preset_reqs)
            else:
                raise ValueError(f"{src}.{pname} has malformed 'requires_presets' entry")

        comp_order: list[str] = __class__._toposort_presets(preset_req_graph)

        res: dict[str, RuleContainer] = {}

        for pname in comp_order:
            res[pname] = __class__._compile_preset(
                presets_json[pname],
                name=pname,
                src=f"{src}.{pname}"
            )

        return res

    @staticmethod
    def _compile_levelruledata(levelrules_json: dict[str, Any], presets_json: dict[str, Any]) -> LevelRules:
        levelrule_presets: dict[str, RuleContainer] = {}
        levelrules: dict[str, LevelDef] = {}

        _proot = presets_json.get("presets", {})
        levelrule_presets = __class__._compile_presets(_proot, src="presets")

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
            raise ValueError("Level rules JSON must be an object!")
        if not isinstance(_json_presets_data, dict):
            raise ValueError("Preset rules JSON must be an object!")

        cls._preset_reg = {}
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
