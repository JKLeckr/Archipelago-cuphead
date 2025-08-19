from __future__ import annotations
import typing
from collections.abc import Callable, Iterable, Mapping
from BaseClasses import CollectionState
from ..debug import p
if typing.TYPE_CHECKING:
    from .. import CupheadWorld

Rule = Callable[[CollectionState], bool]
RegionRule = Callable[[CollectionState, int], bool]

def rule_and(*rules: Rule) -> Rule:
    return lambda state: all(rule(state) for rule in rules)
def rule_or(*rules: Rule) -> Rule:
    return lambda state: any(rule(state) for rule in rules)
def rule_not(rule: Rule) -> Rule:
    return lambda state: not rule(state)

def rule_none() -> Rule:
    return lambda state: True
def rule_false() -> Rule:
    return lambda state: False

def rule_has(world: "CupheadWorld", item: str, count: int = 1) -> Rule:
    return lambda state, player=world.player: state.has(item, player, count)
def rule_has_all(world: "CupheadWorld", items: Iterable[str]) -> Rule:
    return lambda state, player=world.player: state.has_all(items, player)
def rule_has_all_counts(world: "CupheadWorld", item_counts: Mapping[str, int]) -> Rule:
    return lambda state, player=world.player: state.has_all_counts(item_counts, player)
def rule_has_any(world: "CupheadWorld", items: Iterable[str]) -> Rule:
    return lambda state, player=world.player: state.has_any(items, player)
def rule_has_any_count(world: "CupheadWorld", item_counts: Mapping[str, int]) -> Rule:
    return lambda state, player=world.player: state.has_any_count(item_counts, player)
def rule_has_group(world: "CupheadWorld", item_group: str, count: int = 1) -> Rule:
    return lambda state, player=world.player: state.has_group(item_group, player, count)
def rule_has_group_unique(world: "CupheadWorld", item_group: str, count: int = 1) -> Rule:
    return lambda state, player=world.player: state.has_group_unique(item_group, player, count)

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

def rrule_to_rule(rrule: RegionRule, player: int) -> Rule:
    return lambda state, plr=player: rrule(state, plr)

def rrule_and(*rules: RegionRule) -> RegionRule:
    return lambda state, player: all(p(p(rule)(state, player)) for rule in rules)
def rrule_or(*rules: RegionRule) -> RegionRule:
    return lambda state, player: any(p(p(rule)(state, player)) for rule in rules)
def rrule_not(rule: RegionRule) -> RegionRule:
    return lambda state, player: not rule(state, player)

def rrule_none() -> RegionRule:
    return lambda state, player: True
def rrule_false() -> RegionRule:
    return lambda state, player: False

def rrule_has(item: str, count: int = 1) -> RegionRule:
    return lambda state, player: state.has(item, player, count)
def rrule_has_all(items: Iterable[str]) -> RegionRule:
    return lambda state, player: state.has_all(items, player)
def rrule_has_all_counts(item_counts: Mapping[str, int]) -> RegionRule:
    return lambda state, player: state.has_all_counts(item_counts, player)
def rrule_has_any(items: Iterable[str]) -> RegionRule:
    return lambda state, player: state.has_any(items, player)
def rrule_has_any_count(item_counts: Mapping[str, int]) -> RegionRule:
    return lambda state, player: state.has_any_count(item_counts, player)
def rrule_has_group(item_group: str, count: int = 1) -> RegionRule:
    return lambda state, player: state.has_group(item_group, player, count)
def rrule_has_group_unique(item_group: str, count: int = 1) -> RegionRule:
    return lambda state, player: state.has_group_unique(item_group, player, count)
