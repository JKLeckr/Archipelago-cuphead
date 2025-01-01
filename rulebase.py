from __future__ import annotations
import typing
from typing import Callable, Iterable
from BaseClasses import CollectionState
if typing.TYPE_CHECKING:
    from . import CupheadWorld

Rule = Callable[[CollectionState], bool]
RegionRule = Callable[[CollectionState, int], bool]

def rule_and(a: Rule, b: Rule) -> Rule:
    return lambda state: a(state) and b(state)
def rule_not(a: Rule) -> Rule:
    return lambda state: not a(state)
def rule_or(a: Rule, b: Rule) -> Rule:
    return lambda state: a(state) or b(state)
def rule_none() -> Rule:
    return lambda state: True
def rule_has(world: "CupheadWorld", item: str, count: int = 1) -> Rule:
    return lambda state, player=world.player: state.has(item, player, count)
def rule_has_all(world: "CupheadWorld", items: Iterable[str]) -> Rule:
    return lambda state, player=world.player: state.has_all(items, player)
def rule_has_any(world: "CupheadWorld", items: Iterable[str]) -> Rule:
    return lambda state, player=world.player: state.has_any(items, player)

def _can_reach_all_regions(state: CollectionState, player: int, regions: Iterable[str]) -> bool:
    for region in regions:
        if not state.can_reach_region(region, player):
            return False
    return True
def _can_reach_any_region(state: CollectionState, player: int, regions: Iterable[str]) -> bool:
    for region in regions:
        if state.can_reach_region(region, player):
            return True
    return False

def rule_can_reach(world: "CupheadWorld", location: str) -> Rule:
    return lambda state, player=world.player: state.can_reach_location(location, player)
def rule_can_reach_region(world: "CupheadWorld", region: str) -> Rule:
    return lambda state, player=world.player: state.can_reach_region(region, player)
def rule_can_reach_all_regions(world: "CupheadWorld", regions: Iterable[str]) -> Rule:
    return lambda state, player=world.player: _can_reach_all_regions(state, player, regions)
def rule_can_reach_any_region(world: "CupheadWorld", regions: Iterable[str]) -> Rule:
    return lambda state, player=world.player: _can_reach_any_region(state, player, regions)

def region_rule_to_rule(rrule: RegionRule, player: int) -> Rule:
    return lambda state, p=player: rrule(state, p)

def region_rule_and(a: RegionRule, b: RegionRule) -> RegionRule:
    return lambda state, player: a(state, player) and b(state, player)
def region_rule_none() -> RegionRule:
    return lambda state, player: True
def region_rule_has(item: str, count: int = 1) -> RegionRule:
    return lambda state, player: state.has(item, player, count)
def region_rule_has_all(items: Iterable[str]) -> RegionRule:
    return lambda state, player: state.has_all(items, player)
def region_rule_has_any(items: Iterable[str]) -> RegionRule:
    return lambda state, player: state.has_any(items, player)
