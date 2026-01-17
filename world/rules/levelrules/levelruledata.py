### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from typing import Any, ClassVar

from ... import data
from ...names import itemnames, locationnames
from ..deps import DEPS
from . import levelrulebase as lrb
from .levelrulebase import (
    InheritMode,
    ItemRule,
    ItemRuleHas,
    ItemRuleHasFromList,
    ItemRuleHasGroup,
    ItemRuleHasSelection,
    LevelDef,
    LevelRules,
    LocationDef,
    PresetRef,
    RuleContainer,
    RuleDep,
    RuleExpr,
    RuleFragment,
)
from .levelruleselectors import LRSELECTORS


class LevelRuleData:
    _data: ClassVar[LevelRules | None] = None
    _preset_reg: ClassVar[dict[str, RuleContainer]] = {}

    @staticmethod
    def _check_item_entries(
        src: str,
        ls_str: str = "",
        ls: list[Any] | None = None,
        s_str: str = "",
        s: str | None = None,
        i_str: str = "",
        i: int | None = None
    ) -> None:
        if ls:
            if not isinstance(ls, list): # type: ignore
                raise ValueError(f"{src}{ls_str} must be a list!")
        if s:
            if not isinstance(s, str): # type: ignore
                raise ValueError(f"{src}{s_str} must be a valid string!")
        if i:
            if not isinstance(i, int): # type: ignore
                raise ValueError(f"{src}{i_str} must be an integer!")

    @staticmethod
    def _parse_item_names(fnames: list[str], src: str) -> list[str]:
        res: list[str] = []
        for fname in fnames:
            iname = getattr(itemnames, fname)
            if not iname or not isinstance(res, str):
                raise ValueError(f"For {src}: {fname} is an unknown item")
            res.append(iname)
        return res

    @staticmethod
    def _parse_location_names(fname: str, src: str) -> str:
        res = getattr(locationnames, fname)
        if res and isinstance(res, str):
            return res
        raise ValueError(f"For {src}: {fname} is an unknown location")

    @staticmethod
    def _compile_rule_combo(json_obj: dict[str, Any], *, src: str) -> RuleExpr:
        condition = "and" if "and" in json_obj else "or"
        children_json: list[dict[str, Any]] = json_obj[condition]
        __class__._check_item_entries(f"{src}.{condition}", ls = children_json)
        children = [
            __class__._compile_rule_expr(child, src=f"{src}.{condition}[{i}]")
            for i, child in enumerate(children_json)
        ]
        return lrb.And(src, children) if condition == "and" else lrb.Or(src, children)

    @staticmethod
    def _compile_itemrule_selector(lrselector: str, *, src: str, has_any: bool = False) -> ItemRule:
        try:
            _sel = LRSELECTORS[lrselector]
        except KeyError as e:
            raise KeyError(f"From {src}: '{lrselector}' is not a valid level rule!") from e
        return ItemRuleHasSelection(src, _sel, lrselector, has_any)

    @staticmethod
    def _compile_itemrule(json_obj: dict[str, Any], *, src: str) -> ItemRule:
        if "has" in json_obj:
            has_list: list[str] = json_obj["has"]
            has_any = bool(json_obj.get("has_any", False))
            has_count = json_obj.get("count", 1)
            __class__._check_item_entries(
                f"{src}.has", ls = has_list, i = has_count, i_str = " count"
            )
            item_list = __class__._parse_item_names(has_list, src=f"{src}.has")
            return ItemRuleHas(src, item_list, has_any, has_count)
        if "has_selection" in json_obj:
            has_any = bool(json_obj.get("has_any", False))
            return __class__._compile_itemrule_selector(
                json_obj["has_selection"],
                src=f"{src}.has_selection",
                has_any=has_any
            )
        if "has_from_list" in json_obj:
            has_from_list: list[str] = json_obj["has_from_list"]
            has_count = json_obj.get("count", 1)
            unique = bool(json_obj.get("unique", False))
            __class__._check_item_entries(
                f"{src}.has_from_list", ls = has_from_list, i = has_count, i_str = " count"
            )
            item_hlist = __class__._parse_item_names(has_from_list, src=f"{src}.has_from_list")
            return ItemRuleHasFromList(src, item_hlist, has_count, unique)
        if "has_group" in json_obj:
            has_group = json_obj["has_group"]
            has_count = json_obj.get("count", 1)
            unique = bool(json_obj.get("unique", False))
            __class__._check_item_entries(
                    f"{src}.has_group", s = has_group, i = has_count, i_str = " count"
                )
            return ItemRuleHasGroup(src, has_group, has_count, unique)

        raise ValueError(f"{src} is an invalid rule expression")

    @classmethod
    def _compile_preset_ref(cls, preset: str, *, src: str) -> PresetRef:
        __class__._check_item_entries(f"{src}.preset", s = preset)

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
            return __class__._compile_itemrule(json_obj["rule"], src=f"{src}.rule")
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
        __class__._check_item_entries(f"{src}.when", ls = when_json)

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
        __class__._check_item_entries(f"{src}.rules", ls = rules_json)

        rules = [
            __class__._compile_rule_fragment(rule_json, src=f"{src}.rules['{i}']")
            for i, rule_json in enumerate(rules_json)
        ]

        return RuleContainer(src, rules)

    @staticmethod
    def _compile_lloc(json_obj: dict[str, Any], *, src: str) -> LocationDef:
        rules = __class__._compile_rule_container(json_obj, src=src).rules

        inherit_raw = json_obj.get("inherit", "and") # and is the default
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

        return LocationDef(src, rules, inherit)

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
            locations[__class__._parse_location_names(name, src=f"{src}.locations")] = (
                __class__._compile_lloc(loc_json, src=f"{src}.locations.{name}")
            )

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
            preset_reqs: list[str] = preset_json.get("requires_presets", [])
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
