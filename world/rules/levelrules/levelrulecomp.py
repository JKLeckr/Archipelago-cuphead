### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing

from ...names import namemap
from .. import rulebase as rb
from ..rulebase import RegionRule
from . import levelrulebase as lrb

if typing.TYPE_CHECKING:
    from .... import CupheadWorld
    from ...options import CupheadOptions

class LevelRuleComp:
    _world: CupheadWorld
    _options: CupheadOptions

    def _debug_on(self) -> bool:
        return self._world.settings.is_debug_bit_on(128)

    @classmethod
    def _combine_rules(cls, *rules: lrb.RuleExpr | None) -> list[lrb.RuleExpr] | None:
        _res = [rule for rule in rules if rule]
        if _res:
            return _res
        return None

    def _compile_rb_rule(self, rbrule: lrb.RBRule) -> RegionRule:
        return rb.rrule_none() # TODO: Finish

    def compile_rule_expr(self, rule_expr: lrb.RuleExpr) -> RegionRule:
        match rule_expr:
            case lrb.RuleRef():
                return self.compile_rule_container(rule_expr.item)
            case lrb.RuleBool():
                return rb.rrule_false() if not rule_expr.value else rb.rrule_none()
            case lrb.RBRule():
                return self._compile_rb_rule(rule_expr)
            case lrb.And():
                rules = [self.compile_rule_expr(i) for i in rule_expr.items]
                return rb.rrule_and(*rules)
            case lrb.Or():
                rules = [self.compile_rule_expr(i) for i in rule_expr.items]
                return rb.rrule_or(*rules)
            case _:
                raise NotImplementedError(
                    f"{rule_expr.source_path}: '{type(rule_expr).__name__}' is not a supported rule expression type"
                )

    def construct_rule_expr(self, rulec: lrb.RuleContainer) -> lrb.RuleExpr | None:
        root_src = rulec.source_path
        active_rules: list[lrb.RuleExpr] = [
            rulef.requires for rulef in rulec.rules if all(dep.eval(self._options) for dep in rulef.when)
        ]

        if not active_rules:
            return None

        if len(active_rules) == 1:
            return active_rules[0]

        return lrb.And(root_src, active_rules)

    def compile_rule_container(self, rulec: lrb.RuleContainer) -> RegionRule:
        _rule_expr = self.construct_rule_expr(rulec)
        if _rule_expr:
            return self.compile_rule_expr(_rule_expr)
        return rb.rrule_none()

    def compile_location(
        self,
        level: lrb.LevelDef,
        loc: lrb.LocationDef
        ) -> RegionRule:
        root_src = loc.source_path
        loc_rule = self.construct_rule_expr(loc) if loc else None

        if level.base:
            match loc.inherit:
                case lrb.InheritMode.AND:
                    _rules = self._combine_rules(self.construct_rule_expr(level.base), loc_rule)
                    if _rules:
                        return self.compile_rule_expr(lrb.And(f"{root_src}.and", _rules))
                case lrb.InheritMode.OR:
                    _rules = self._combine_rules(self.construct_rule_expr(level.base), loc_rule)
                    if _rules:
                        return self.compile_rule_expr(lrb.Or(f"{root_src}.or", _rules))
                case lrb.InheritMode.NONE:
                    if loc_rule:
                        return self.compile_rule_expr(loc_rule)
                    return rb.rrule_none()
        return self.compile_rule_expr(loc_rule) if loc_rule else rb.rrule_none()

    def _compile_level_loc(self, rlname: str, ldef: lrb.LevelDef, locname: str, loc: lrb.LocationDef) -> None:
        player = self._world.player
        active_locations = self._world.active_locations

        rlocname = namemap.get_location_name(locname)
        if rlocname in active_locations:
            _rule = rb.rrule_to_rule(self.compile_location(ldef, loc), player)
            rb.add_loc_rule(
                self._world,
                rlocname,
                _rule
            )
            if locname == ldef.exit_location:
                rb.add_region_exit_rule(
                    self._world,
                    rlname,
                    _rule
                )
        else:
            if self._debug_on():
                print(f"Skipping rules for {loc.source_path}")
            if rlocname == ldef.exit_location:
                raise Warning(
                    f"{ldef.source_path}.exit_location: '{ldef.exit_location}' is skipped because location is inactive."
                )

    def compile_levelrules(self) -> None:
        active_levels = self._world.active_levels
        player = self._world.player

        levelrule_data = LevelRuleData.get_data(debug=self._world.settings.is_debug_bit_on(64))

        for lname, ldef in levelrule_data.levels.items():
            if self._debug_on():
                print(lname)
            rlname = namemap.get_region_name(lname)
            #print(active_levels)
            if rlname in active_levels:
                if ldef.exit_location and ldef.exit_location not in ldef.locations:
                    raise ValueError(f"{ldef.source_path}.exit_location: '{ldef.exit_location}' is unknown.")
                if ldef.access:
                    rb.add_region_rule(
                        self._world,
                        rlname,
                        rb.rrule_to_rule(self.compile_rule_container(ldef.access), player)
                    )
                for locname, loc in ldef.locations.items():
                    self._compile_level_loc(rlname, ldef, locname, loc)
            elif self._debug_on():
                print(f"Skipping rules for {ldef.source_path}")

    def __init__(self, world: CupheadWorld):
        self._world = world
        self._options = world.options
