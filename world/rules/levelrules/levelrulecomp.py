### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from collections.abc import Callable, Iterable

from .. import deps, rulebase as rb
from ..rulebase import RegionRule
from . import levelrulebase as lrb
from . import levelrules
from .levelruledata import LevelRuleData

if typing.TYPE_CHECKING:
    from .... import CupheadWorld
    from ...wconf import WorldConfig

def compile_rule_exprs(wconf: WorldConfig, rule_expr: lrb.RuleExpr) -> RegionRule:
    match rule_expr:
        case lrb.LRule:
            return rule_expr.rule(wconf)
        case lrb.PresetRef:
            if rule_expr.item:
                return compile_rule_container(wconf, rule_expr.item)
            return rb.rrule_none()
        case lrb.And:
            rules = [compile_rule_exprs(wconf, i) for i in rule_expr.items]
            return rb.rrule_and(*rules)
        case lrb.Or:
            rules = [compile_rule_exprs(wconf, i) for i in rule_expr.items]
            return rb.rrule_or(*rules)
        case lrb.Not:
            return rb.rrule_not(compile_rule_exprs(wconf, rule_expr.item))
        case _:
            raise NotImplementedError(f"{type(rule_expr)} is not a supported rule expression type")

def compile_rule_container(wconf: WorldConfig, rulec: lrb.RuleContainer) -> RegionRule:
    active_rules: list[lrb.RuleExpr] = []

    root_src = rulec.source_path
    for rulef in rulec.rules:
        if all(dep.eval(wconf) for dep in rulef.when):
            active_rules.append(rulef.requires)

    if not active_rules:
        return rb.rrule_none()

    return compile_rule_exprs(wconf, lrb.And(root_src, active_rules))

def compile_location(world: CupheadWorld, base_rule: lrb.RuleContainer) -> None:
    pass

def compile_levelrules(world: CupheadWorld) -> None:
    levelrule_data = LevelRuleData.get_data()

    # TODO: Level location inherit

    for lname, ldef in levelrule_data.levels.items():
        pass
