### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import And as RBAnd
from rule_builder.rules import HasAllCounts, HasAnyCount, Rule, True_
from rule_builder.rules import Or as RBOr

from . import levelrulebase as lrb
from .levelruledefs import levelrules

if TYPE_CHECKING:
    from .... import CupheadWorld
    from ...options import CupheadOptions


@dataclass(slots=True)
class _RuleEvalCtx:
    level_name: str
    options: CupheadOptions
    ruledefs: dict[str, lrb.RuleList]
    compiled_ruledefs: dict[str, Rule] = field(default_factory=dict[str, Rule])


class LevelRuleComp:
    _world: CupheadWorld
    _options: CupheadOptions

    def _debug_on(self) -> bool:
        return self._world.settings.is_debug_bit_on(128)

    def _check_filters(self, filters: Iterable[OptionFilter]) -> bool:
        return all(opt.check(self._options) for opt in filters)

    def _contains_rule_ref(self, rule: lrb.RuleExpr) -> bool:
        match rule:
            case lrb.RuleRef():
                return True
            case lrb.And() | lrb.Or():
                return any(self._contains_rule_ref(item) for item in rule.items)
            case lrb.RulePreset():
                return any(self._contains_rule_ref(item) for item in rule.rules)
            case _:
                return False

    def _eval_rule_ref(self, ref: lrb.RuleRef, ctx: _RuleEvalCtx, filtered_resolution: bool):
        cached = ctx.compiled_ruledefs.get(ref.ref_name)
        if cached is not None:
            return cached

        ruledef = ctx.ruledefs.get(ref.ref_name)
        if ruledef is None:
            raise ValueError(f"Unknown RuleRef '{ref.ref_name}' in level '{ctx.level_name}'.")

        compiled = self._eval_rule_list(ruledef, ctx)
        ctx.compiled_ruledefs[ref.ref_name] = compiled
        return compiled

    def _eval_filtered_resolution(self, fr_orig: bool, fr_override: bool | None, fr_auto: bool) -> bool:
        return (
            fr_override
            if fr_override is not None and fr_auto else
            fr_orig
        )

    def _eval_rule_expr(
        self,
        expr: lrb.RuleExpr,
        ctx: _RuleEvalCtx,
        fr_override: bool | None
    ) -> Rule:
        match expr:
            case lrb.RBRule():
                if expr.auto_filter_resolution:
                    expr.rule.filtered_resolution = (
                        fr_override if fr_override is not None else lrb.FR_DEFAULT
                    )
                return expr.rule
            case lrb.SelectRule():
                filtered_resolution = (
                    self._eval_filtered_resolution(expr.filtered_resolution, fr_override, expr.fr_auto)
                )
                selected = expr.select(self._options)
                return (
                    HasAnyCount(
                        selected,
                        options=expr.options,
                        filtered_resolution=filtered_resolution
                    )
                    if expr.any else
                    HasAllCounts(
                        selected,
                        options=expr.options,
                        filtered_resolution=filtered_resolution
                    )
                )
            case lrb.RulePreset():
                filtered_resolution = (
                    self._eval_filtered_resolution(expr.filtered_resolution, fr_override, expr.fr_auto)
                )
                return self._eval_rule_list(
                    expr.rules,
                    ctx,
                    True,
                    expr.options,
                    filtered_resolution
                )
            case lrb.And():
                filtered_resolution = (
                    self._eval_filtered_resolution(expr.filtered_resolution, fr_override, expr.fr_auto)
                )
                return self._eval_rule_list(
                    expr.items,
                    ctx,
                    True,
                    expr.options,
                    filtered_resolution
                )
            case lrb.Or():
                filtered_resolution = (
                    self._eval_filtered_resolution(expr.filtered_resolution, fr_override, expr.fr_auto)
                )
                return self._eval_rule_list(
                    expr.items,
                    ctx,
                    False,
                    expr.options,
                    filtered_resolution
                )
            case lrb.RuleRef():
                filtered_resolution = (
                    self._eval_filtered_resolution(expr.filtered_resolution, fr_override, expr.fr_auto)
                )
                return self._eval_rule_ref(expr, ctx, filtered_resolution)
            case _:
                raise TypeError(f"Unsupported rule expression type: {type(expr)!r}")

    def _eval_rule_list(
        self,
        rule_list: Iterable[lrb.RuleExpr] | None,
        ctx: _RuleEvalCtx,
        op_and: bool = True,
        filters: Iterable[OptionFilter] = (),
        filtered_resolution: bool = True
    ) -> Rule:
        if not rule_list:
            return True_(options=filters, filtered_resolution=filtered_resolution)

        fr_override = False if not op_and else None
        rules = [self._eval_rule_expr(rule, ctx, fr_override) for rule in rule_list]
        if len(rules) == 1:
            return rules[0]
        return (
            RBAnd(*rules, options=filters, filtered_resolution=filtered_resolution)
            if op_and else
            RBOr(*rules, options=filters, filtered_resolution=filtered_resolution)
        )

    def _validate_ruledefs(self, ctx: _RuleEvalCtx) -> None:
        for def_name, rule_list in ctx.ruledefs.items():
            if any(self._contains_rule_ref(rule) for rule in rule_list):
                raise ValueError(
                    f"Level '{ctx.level_name}' ruledef '{def_name}' cannot contain RuleRef."
                )

    def _compile_location_rule(
        self,
        level: lrb.LevelDef,
        loc: lrb.LocationDef,
        ctx: _RuleEvalCtx
    ) -> Rule:
        loc_rule = self._eval_rule_list(loc.rules, ctx)
        if not level.base:
            return loc_rule

        base_rule = self._eval_rule_list(level.base, ctx)
        match loc.inherit:
            case lrb.InheritMode.AND:
                return RBAnd(base_rule, loc_rule)
            case lrb.InheritMode.OR:
                return RBOr(base_rule, loc_rule)
            case lrb.InheritMode.NONE:
                return loc_rule

    def _compile_level_loc(
        self,
        rlname: str,
        ldef: lrb.LevelDef,
        locname: str,
        loc: lrb.LocationDef,
        ctx: _RuleEvalCtx
    ) -> None:
        if locname in self._world.active_locations:
            _rule = self._compile_location_rule(ldef, loc, ctx)
            self._world.rulereg.add_loc_rule(locname, _rule)
            if locname == ldef.exit_location:
                self._world.rulereg.add_region_exit_rule(rlname, _rule)
        else:
            if self._debug_on():
                print(f"Skipping rules for location '{locname}'")
            if locname == ldef.exit_location:
                raise ValueError(
                    f"level '{rlname}' exit_location '{ldef.exit_location}' is an inactive location."
                )

    def compile_levelrules(self) -> None:
        active_levels = self._world.active_levels

        for lname, ldef in levelrules.levels.items():
            if self._debug_on():
                print(lname)

            if lname in active_levels:
                if ldef.exit_location and ldef.exit_location not in ldef.locations:
                    raise ValueError(f"'{lname}'.exit_location: '{ldef.exit_location}' is unknown.")
                ctx = _RuleEvalCtx(lname, self._options, ldef.ruledefs)
                self._validate_ruledefs(ctx)

                if ldef.access:
                    self._world.rulereg.add_region_rule(lname, self._eval_rule_list(ldef.access, ctx))

                for locname, loc in ldef.locations.items():
                    self._compile_level_loc(lname, ldef, locname, loc, ctx)
            elif self._debug_on():
                print(f"Skipping rules for level '{lname}'")

    def __init__(self, world: CupheadWorld):
        self._world = world
        self._options = world.options
