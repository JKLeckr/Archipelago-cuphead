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

def get_entrance_name(exit: str, entrance: str) -> str:
    return f"({exit})->({entrance})"
def get_entrance_by_name(world: CupheadWorld, entrance_name: str) -> Entrance:
    return world.multiworld.get_entrance(entrance_name, world.player)
def get_entrance(world: CupheadWorld, exit: str, entrance: str) -> Entrance:
    return get_entrance_by_name(world, get_entrance_name(exit, entrance))
def get_location(world: CupheadWorld, location: str) -> Location:
    return world.multiworld.get_location(location, world.player)
def get_region(world: CupheadWorld, region: str) -> Region:
    return world.multiworld.get_region(region, world.player)
