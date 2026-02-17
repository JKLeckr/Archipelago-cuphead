### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from typing import Any, ClassVar

from .... import data
from ....names import namemap
from ...dep.deps import DEPS
from ..levelruleselectors import LRSELECTORS
from . import levelrulejsonbase as lrb
from .levelrulejsonbase import (
    InheritMode,
    ItemRule,
    ItemRuleHas,
    ItemRuleHasFromList,
    ItemRuleHasGroup,
    ItemRuleHasSelection,
    LevelDef,
    LevelRules,
    LocationDef,
    RuleBool,
    RuleContainer,
    RuleDep,
    RuleExpr,
    RuleFragment,
    RuleRef,
)


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
    def _check_item_names(fnames: list[str], src: str):
        for fname in fnames:
            if not namemap.item_name_exists(fname):
                raise ValueError(f"For {src}: item '{fname}' is unknown!")

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
            __class__._check_item_names(has_list, src=f"{src}.has")
            return ItemRuleHas(src, has_list, has_any, has_count)
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
            __class__._check_item_names(has_from_list, src=f"{src}.has_from_list")
            return ItemRuleHasFromList(src, has_from_list, has_count, unique)
        if "has_group" in json_obj:
            has_group = json_obj["has_group"]
            has_count = json_obj.get("count", 1)
            unique = bool(json_obj.get("unique", False))
            __class__._check_item_entries(
                    f"{src}.has_group", s = has_group, i = has_count, i_str = " count"
                )
            return ItemRuleHasGroup(src, has_group, has_count, unique)

        raise ValueError(f"{src} is an invalid rule expression")

    @staticmethod
    def _compile_rule_ref(ref: str, ref_data: dict[str, RuleContainer], *, src: str) -> RuleFragment:
        __class__._check_item_entries(src, s = ref)

        if ref not in ref_data:
            raise KeyError(
                f"From {src}: Rule Reference '{ref}' does not exist!"
            )

        rule_ref = ref_data[ref]
        return RuleFragment(
            f"{src}[{ref}]",
            [],
            RuleRef(f"{src}[{ref}].requires", rule_ref, ref)
        )

    @classmethod
    def _compile_preset_ref(cls, preset: str, *, src: str) -> RuleRef:
        __class__._check_item_entries(f"{src}.preset", s = preset)

        if preset not in cls._preset_reg:
            raise KeyError(
                f"From {src}: Preset Reference '{preset}' does not exist or is not resolved!",
                f"Make sure you add '{preset}' to 'requires_presets' for preset '{src.split('.', 2)[1]}'."
            )

        preset_ref = cls._preset_reg[preset]
        return RuleRef(f"{src}.preset[{preset}]", preset_ref, preset)

    @staticmethod
    def _compile_rule_expr(json_obj: dict[str, dict[str, Any] | bool], *, src: str) -> RuleExpr:
        if "preset" in json_obj:
            _preset = json_obj["preset"]
            if isinstance(_preset, str):
                return __class__._compile_preset_ref(_preset, src=src)
            raise ValueError(f"{src}.preset is an invalid type")
        if "rule" in json_obj:
            _rule = json_obj["rule"]
            if isinstance(_rule, dict):
                return __class__._compile_itemrule(_rule, src=f"{src}.rule")
            raise ValueError(f"{src}.rule is an invalid type")
        if "and" in json_obj or "or" in json_obj:
            return __class__._compile_rule_combo(json_obj, src=src)
        if "not" in json_obj:
            _not = json_obj["not"]
            if isinstance(_not, dict):
                return lrb.Not(src, __class__._compile_rule_expr(_not, src=f"{src}.not"))
            raise ValueError(f"{src}.not is an invalid type")

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
        requires_json: dict[str, Any] | bool | None = json_obj.get("requires")

        if requires_json is None:
            raise ValueError(f"{src}.requires is required!")
        __class__._check_item_entries(f"{src}.when", ls = when_json)

        when = [
            __class__._compile_ruledep(dep, src=f"{src}.when")
            for dep in when_json
        ]

        if isinstance(requires_json, bool):
            if requires_json:
                raise SyntaxWarning(f"{src}.true is discouraged! Disable rule instead.")
            _res_str = "false" if not requires_json else "true"
            requires = RuleBool(f"{src}.{_res_str}", requires_json)
        elif isinstance(requires_json, dict): # type: ignore
            requires = __class__._compile_rule_expr(
                requires_json,
                src=f"{src}.requires"
            )
        else:
            raise ValueError(f"{src}.preset is an invalid type")

        return RuleFragment(src, when, requires)

    @staticmethod
    def _build_rules(
        json_obj: dict[str, Any], *,
        src: str,
        rule_defs: dict[str, RuleContainer] | None = None
    ) -> list[RuleFragment]:
        rules_json: list[dict[str, Any]] = json_obj.get("rules", [])
        __class__._check_item_entries(f"{src}.rules", ls = rules_json)

        res: list[RuleFragment] = []

        for i, rule_json in enumerate(rules_json):
            if "from" in rule_json:
                rdsrc = f"{src}.rules[{i}].from"
                if rule_defs is None:
                    raise ValueError(f"{rdsrc} cannot be used outside of locations!")
                ruledef_ref: str = rule_json["from"]
                if not isinstance(ruledef_ref, str): # type: ignore
                    raise ValueError(f"{rdsrc} must be a string!")
                if ruledef_ref not in rule_defs:
                    raise KeyError(f"{rdsrc}: {ruledef_ref} does not exist in rule_defs!")
                res.append(
                    __class__._compile_rule_ref(ruledef_ref, rule_defs, src=rdsrc)
                )
            else:
                res.append(
                    __class__._compile_rule_fragment(rule_json, src=f"{src}.rules[{i}]")
                )

        return res

    @staticmethod
    def _compile_rule_container(
        json_obj: dict[str, Any],
        *,
        src: str,
        rule_defs: dict[str, RuleContainer] | None = None
    ) -> RuleContainer:
        rules = __class__._build_rules(json_obj, src=src, rule_defs=rule_defs)
        return RuleContainer(src, rules)

    @staticmethod
    def _parse_inherit_mode(inherit_raw: str, *, src: str) -> InheritMode:
        match inherit_raw:
            case "and":
                return InheritMode.AND
            case "or":
                return InheritMode.OR
            case "none":
                return InheritMode.NONE
            case _:
                raise ValueError(f"{src} needs to be one of: [and,or,none]")

    @staticmethod
    def _compile_lloc(
        json_obj: dict[str, Any], *,
        src: str,
        inherit_default: InheritMode = InheritMode.NONE,
        rule_defs: dict[str, RuleContainer] | None = None
    ) -> LocationDef:
        rules = __class__._build_rules(json_obj, src=src, rule_defs=rule_defs)

        inherit_raw = json_obj.get("inherit")
        if inherit_raw is not None:
            if not isinstance(inherit_raw, str):
                raise ValueError(f"{src}.inherit is not a valid string!")
            inherit = __class__._parse_inherit_mode(inherit_raw, src=f"{src}.inherit")
        else:
            inherit = inherit_default

        return LocationDef(src, rules, inherit)

    @staticmethod
    def _populate_ruledefs(json_obj: dict[str, Any], *, src: str) -> dict[str, RuleContainer]:
        ruledefs_json: dict[str, Any] = json_obj.get("rule_defs", {})

        if not isinstance(ruledefs_json, dict): # type: ignore
            raise ValueError(f"{src}.rule_defs is an invalid json object!")

        return {
            rdname: __class__._compile_rule_container(ruledef, src=f"{src}.rule_defs[{rdname}]")
            for rdname, ruledef in ruledefs_json.items()
        }

    @staticmethod
    def _compile_level(json_obj: dict[str, Any], *, src: str) -> LevelDef:
        rule_defs = (
            __class__._populate_ruledefs(json_obj, src=src)
            if "rule_defs" in json_obj
            else None
        )

        access = (
            __class__._compile_rule_container(
                json_obj["access"], src=f"{src}.access", rule_defs=rule_defs
            )
            if "access" in json_obj
            else None
        )

        base = (
            __class__._compile_rule_container(
                json_obj["base"], src=f"{src}.base", rule_defs=rule_defs
            )
            if "base" in json_obj
            else None
        )

        inherit_default = __class__._parse_inherit_mode(
            json_obj.get("inherit_default", "and"), # and is the default
            src=f"{src}.inherit_default"
        )

        locations: dict[str, LocationDef] = {}
        locs_json: dict[str, Any] = json_obj.get("locations", {})
        if not isinstance(locs_json, dict): # type: ignore
            raise ValueError(f"{src}.locations is an invalid json object!")
        for name, loc_json in locs_json.items():
            if not namemap.location_name_exists(name):
                raise ValueError(f"For {src}.locations: location '{name}' is unknown!")
            locations[name] = (
                __class__._compile_lloc(
                    loc_json,
                    src=f"{src}.locations.{name}",
                    rule_defs=rule_defs,
                    inherit_default=inherit_default
                )
            )

        exit_location: str | None = json_obj.get("exit_location")
        if exit_location and exit_location not in locations:
            raise ValueError(
                f"For {src}.exit_location: '{exit_location}' is not a location in this level!"
            )

        return LevelDef(src, access, exit_location, base, locations)

    @classmethod
    def _compile_preset(cls, json_obj: dict[str, Any], *, name: str, src: str) -> RuleContainer:
        res = __class__._compile_rule_container(json_obj, src=src)
        if name in cls._preset_reg:
            raise KeyError(f"From {src}: '{name}' already is registered!")
        cls._preset_reg[name] = res
        return res

    @staticmethod
    def _toposort_reqs(graph: dict[str, set[str]]) -> list[str]:
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

        comp_order: list[str] = __class__._toposort_reqs(preset_req_graph)

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
    def load_data(cls, *, debug: bool = False):
        if cls._data:
            raise Warning("levelrule data is already loaded. Reloading.")
        if debug:
            print("Loading levelrule data...")
        cls._load_levelrule_data()
        if debug:
            print("levelrule data loaded")

    @classmethod
    def get_data(cls, *, debug: bool = False) -> LevelRules:
        if not cls._data:
            if debug:
                print("Loading levelrule data...")
            cls._load_levelrule_data()
            if debug:
                print("levelrule data loaded")
        if cls._data is not None:
            return cls._data
        raise ValueError("Could not load levelrule data")

#LevelRuleData.load_data()
