### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing

from .. import rulebase as rb
from ..rulebase import RegionRule
from . import levelrulebase as lrb
from .levelruledata import LevelRuleData

if typing.TYPE_CHECKING:
    from .... import CupheadWorld
    from ...wconf import WorldConfig

def _combine_rules(*rules: lrb.RuleExpr | None) -> list[lrb.RuleExpr]:
    _res = [rule for rule in rules if rule]
    if _res:
        return _res
    raise ValueError("All rules are None!")

def _compile_item_rule(wconf: WorldConfig, irule: type[lrb.ItemRule]) -> RegionRule:  # noqa: C901
    match irule:
        case lrb.ItemRuleHas:
            if len(irule.items) < 1:
                raise ValueError(f"{irule.source_path}: cannot be empty")
            if len(irule.items) == 1:
                return rb.rrule_has(irule.items[0])
            count = irule.count if irule.count else 1
            if irule.has_any:
                return rb.rrule_has_any_count(dict.fromkeys(irule.items, count))
            return rb.rrule_has_all_counts(dict.fromkeys(irule.items, count))
        case lrb.ItemRuleHasSelection:
            selection = irule.selector(wconf)
            if irule.has_any:
                return rb.rrule_has_any_count(selection)
            return rb.rrule_has_all_counts(selection)
        case lrb.ItemRuleHasFromList:
            if len(irule.items) < 1:
                raise ValueError(f"{irule.source_path}: cannot be empty")
            count = irule.count if irule.count else 1
            if irule.unique:
                return rb.rrule_has_from_list_unique(irule.items, count)
            return rb.rrule_has_from_list(irule.items, count)
        case lrb.ItemRuleHasGroup:
            count = irule.count if irule.count else 1
            if irule.unique:
                return rb.rrule_has_group_unique(irule.group, count)
            return rb.rrule_has_group(irule.group, count)
        case _:
            raise NotImplementedError(f"{type(irule)} is not a supported item rule type")

def compile_rule_expr(wconf: WorldConfig, rule_expr: lrb.RuleExpr) -> RegionRule:
    match rule_expr:
        case lrb.ItemRule:
            return _compile_item_rule(wconf, rule_expr)
        case lrb.PresetRef:
            if rule_expr.item:
                return compile_rule_container(wconf, rule_expr.item)
            return rb.rrule_none()
        case lrb.And:
            rules = [compile_rule_expr(wconf, i) for i in rule_expr.items]
            return rb.rrule_and(*rules)
        case lrb.Or:
            rules = [compile_rule_expr(wconf, i) for i in rule_expr.items]
            return rb.rrule_or(*rules)
        case lrb.Not:
            return rb.rrule_not(compile_rule_expr(wconf, rule_expr.item))
        case _:
            raise NotImplementedError(f"{type(rule_expr)} is not a supported rule expression type")

def construct_rule_expr(wconf: WorldConfig, rulec: lrb.RuleContainer) -> lrb.RuleExpr | None:
    root_src = rulec.source_path
    active_rules: list[lrb.RuleExpr] = [
        rulef.requires for rulef in rulec.rules if all(dep.eval(wconf) for dep in rulef.when)
    ]

    if not active_rules:
        return None

    if len(active_rules) == 1:
        return active_rules[0]

    return lrb.And(root_src, active_rules)

def compile_rule_container(wconf: WorldConfig, rulec: lrb.RuleContainer) -> RegionRule:
    _rule_expr = construct_rule_expr(wconf, rulec)
    if _rule_expr:
        return compile_rule_expr(wconf, _rule_expr)
    return rb.rrule_none()

def compile_location(
    wconf: WorldConfig,
    level: lrb.LevelDef,
    loc: lrb.LocationDef
    ) -> RegionRule:
    root_src = loc.source_path
    loc_rule = construct_rule_expr(wconf, loc.rule) if loc.rule else None

    if level.base:
        match loc.inherit:
            case lrb.InheritMode.AND:
                _rules = _combine_rules(construct_rule_expr(wconf, level.base), loc_rule)
                return compile_rule_expr(wconf, lrb.And(f"{root_src}.and", _rules))
            case lrb.InheritMode.OR:
                _rules = _combine_rules(construct_rule_expr(wconf, level.base), loc_rule)
                return compile_rule_expr(wconf, lrb.Or(f"{root_src}.or", _rules))
            case lrb.InheritMode.NONE:
                if loc_rule:
                    return compile_rule_expr(wconf, loc_rule)
                return rb.rrule_none()
    return compile_rule_expr(wconf, loc_rule) if loc_rule else rb.rrule_none()

def compile_levelrules(world: CupheadWorld) -> None:
    wconf = world.wconfig
    player = world.player
    levelrule_data = LevelRuleData.get_data()

    for lname, ldef in levelrule_data.levels.items():
        if ldef.access:
            rb.add_region_rule(
                world,
                lname,
                rb.rrule_to_rule(compile_rule_container(wconf, ldef.access), player)
            )
        for locname, loc in ldef.locations.items():
            rb.add_loc_rule(
                world,
                locname,
                rb.rrule_to_rule(compile_location(wconf, ldef, loc), player)
            )
