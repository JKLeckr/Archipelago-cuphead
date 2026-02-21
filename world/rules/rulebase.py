### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from collections.abc import Iterable

from BaseClasses import CollectionRule, Entrance, Location, Region
from rule_builder.rules import (
    And,
    CanReachEntrance,
    CanReachLocation,
    CanReachRegion,
    False_,
    Has,
    HasAll,
    HasAllCounts,
    HasAny,
    HasAnyCount,
    HasFromList,
    HasFromListUnique,
    HasGroup,
    HasGroupUnique,
    Or,
    Rule,
    True_,
)

if typing.TYPE_CHECKING:
    from ... import CupheadWorld

RuleReg = dict[Location | Entrance, list[CollectionRule]]


# Base Rule functions

def rule_and(*rules: Rule) -> Rule:
    return And(*rules)
def rule_or(*rules: Rule) -> Rule:
    return Or(*rules)

def rule_none() -> Rule:
    return rule_true()
def rule_true() -> Rule:
    return True_()
def rule_false() -> Rule:
    return False_()

def rule_has(item: str, count: int = 1) -> Rule:
    return Has(item, count)
def rule_has_all(items: Iterable[str]) -> Rule:
    return HasAll(*items)
def rule_has_all_counts(item_counts: dict[str, int]) -> Rule:
    return HasAllCounts(item_counts)
def rule_has_any(items: Iterable[str]) -> Rule:
    return HasAny(*items)
def rule_has_any_count(item_counts: dict[str, int]) -> Rule:
    return HasAnyCount(item_counts)
def rule_has_from_list(items: Iterable[str], count: int = 1) -> Rule:
    return HasFromList(*items, count=count)
def rule_has_from_list_unique(items: Iterable[str], count: int = 1) -> Rule:
    return HasFromListUnique(*items, count=count)
def rule_has_group(item_group: str, count: int = 1) -> Rule:
    return HasGroup(item_group, count)
def rule_has_group_unique(item_group: str, count: int = 1) -> Rule:
    return HasGroupUnique(item_group, count)

def rule_can_reach(location: str) -> Rule:
    return CanReachLocation(location)
def rule_can_reach_region(region: str) -> Rule:
    return CanReachRegion(region)
def rule_can_reach_all_regions(regions: Iterable[str]) -> Rule:
    return And(*[rule_can_reach_region(r) for r in regions])
def rule_can_reach_any_region(regions: Iterable[str]) -> Rule:
    return Or(*[rule_can_reach_region(r) for r in regions])
def rule_can_reach_entrance(entrance: str) -> Rule:
    return CanReachEntrance(entrance)
def rule_can_reach_all_entrances(entrances: Iterable[str]) -> Rule:
    return And(*[rule_can_reach_entrance(e) for e in entrances])
def rule_can_reach_any_entrance(entrances: Iterable[str]) -> Rule:
    return Or(*[rule_can_reach_entrance(e) for e in entrances])


# Rule helper functions

def get_entrance(world: CupheadWorld, exit: str, entrance: str) -> Entrance:
    return world.multiworld.get_entrance(f"({exit})->({entrance})", world.player)
def get_location(world: CupheadWorld, location: str) -> Location:
    return world.multiworld.get_location(location, world.player)
def get_region(world: CupheadWorld, region: str) -> Region:
    return world.multiworld.get_region(region, world.player)
def set_item_rule(world: CupheadWorld, loc: str, item: str, count: int = 1) -> None:
    set_loc_rule(world, loc, rule_has(world, item, count))
def add_item_rule(world: CupheadWorld, loc: str, item: str, count: int = 1, combine_and: bool = True) -> None:
    add_loc_rule(world, loc, rule_has(world, item, count), combine_and)
def set_loc_rule(world: CupheadWorld, loc: str, rule: Rule) -> None:
    set_rule(get_location(world, loc), rule)
def add_loc_rule(world: CupheadWorld, loc: str, rule: Rule, combine_and: bool = True) -> None:
    add_rule(get_location(world, loc), rule, "and" if combine_and else "or")
def set_region_rules(world: CupheadWorld, region_name: str, rule: Rule):
    region = get_region(world, region_name)
    for entrance in region.entrances:
        set_rule(entrance, rule)
def set_region_exit_rules(world: CupheadWorld, region_name: str, rule: Rule):
    region = get_region(world, region_name)
    for entrance in region.exits:
        set_rule(entrance, rule)
def add_region_rule(world: CupheadWorld, region_name: str, rule: Rule, combine_and: bool = True):
    region = get_region(world, region_name)
    for entrance in region.entrances:
        add_rule(entrance, rule, "and" if combine_and else "or")
def add_region_exit_rule(world: CupheadWorld, region_name: str, rule: Rule, combine_and: bool = True):
    region = get_region(world, region_name)
    for entrance in region.exits:
        add_rule(entrance, rule, "and" if combine_and else "or")
