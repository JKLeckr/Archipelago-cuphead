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

def region_rule_none() -> RegionRule:
    return lambda state, player: True
def region_rule_has(item: str, count: int = 1) -> RegionRule:
    return lambda state, player: state.has(item, player, count)
def region_rule_has_all(items: Iterable[str]) -> RegionRule:
    return lambda state, player: state.has_all(items, player)
def region_rule_has_any(items: Iterable[str]) -> RegionRule:
    return lambda state, player: state.has_any(items, player)
