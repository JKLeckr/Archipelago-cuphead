### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from dataclasses import dataclass
from enum import IntEnum
from typing import NamedTuple

from rule_builder.rules import And, Or, Rule

from . import rulebase as rb

if typing.TYPE_CHECKING:
    from ... import CupheadWorld

class SpotType(IntEnum):
    LOCATION = 0
    ENTRANCE = 1

class Spot(NamedTuple):
    name: str
    type: SpotType

class RuleData(NamedTuple):
    rule: Rule
    combine_and: bool = True

@dataclass(init=False)
class RuleReg:
    _reg: dict[Spot, list[RuleData]]
    _world: CupheadWorld

    def __init__(self, world: CupheadWorld):
        self._reg = {}
        self._world = world

    def set_rule(self, spot_name: str, spot_type: SpotType, rule: Rule):
        spot = Spot(spot_name, spot_type)
        self._reg[spot] = [RuleData(rule)]
        if spot in self._reg:
            raise ValueError(f"Cannot add rule '{rule}': Rule for {spot_name} already exists")

    def add_rule(self, spot_name: str, spot_type: SpotType, rule: Rule, combine_and: bool):
        spot = Spot(spot_name, spot_type)
        if spot not in self._reg:
            self._reg[spot] = [RuleData(rule)]
        else:
            self._reg[spot].append(RuleData(rule, combine_and))

    def set_item_rule(self, loc: str, item: str, count: int = 1) -> None:
        self.set_loc_rule(loc, rb.rule_has(item, count))
    def add_item_rule(self, loc: str, item: str, count: int = 1, combine_and: bool = True) -> None:
        self.add_loc_rule(loc, rb.rule_has(item, count), combine_and)
    def set_loc_rule(self, loc: str, rule: Rule) -> None:
        self.set_rule(loc, SpotType.LOCATION, rule)
    def add_loc_rule(self, loc: str, rule: Rule, combine_and: bool = True) -> None:
        self.add_rule(loc, SpotType.LOCATION, rule, combine_and)
    def set_region_rules(self, region_name: str, rule: Rule):
        region = rb.get_region(self._world, region_name)
        for entrance in region.entrances:
            self.set_rule(entrance.name, SpotType.ENTRANCE, rule)
    def add_region_rule(self, region_name: str, rule: Rule, combine_and: bool = True):
        region = rb.get_region(self._world, region_name)
        for entrance in region.entrances:
            self.add_rule(entrance.name, SpotType.ENTRANCE, rule, combine_and)
    def set_region_exit_rules(self, region_name: str, rule: Rule):
        region = rb.get_region(self._world, region_name)
        for entrance in region.exits:
            self.set_rule(entrance.name, SpotType.ENTRANCE, rule)
    def add_region_exit_rule(self, region_name: str, rule: Rule, combine_and: bool = True):
        region = rb.get_region(self._world, region_name)
        for entrance in region.exits:
            self.add_rule(entrance.name, SpotType.ENTRANCE, rule, combine_and)

    def compile_rules(self):
        # This will iterate through the rules for each type and set the rule for
        # that spot (location or entrance) using self._world.set_rules(). It is done this way
        # because rule_builder Rules cannot be appended to exising world rules.
        # So this will stitch together all the rule_builder rules before setting them.
        for (spot_name, spot_type), rules in self._reg.items():
            if len(rules) < 1:
                print(f"{spot_name} rules is empty")
                continue

            if spot_type == SpotType.ENTRANCE:
                spot = rb.get_entrance_by_name(self._world, spot_name)
            else:
                spot = rb.get_location(self._world, spot_name)

            if len(rules) == 1:
                self._world.set_rule(spot, rules[0].rule)
                continue

            _col: list[Rule] = []
            _and = True
            for rule in rules:
                if rule.combine_and != _and:
                    _rule = And(*_col) if _and else Or(*_col)
                    _col = [_rule]
                    _and = rule.combine_and
                _col.append(rule.rule)

            _res = And(*_col) if _and else Or(*_col)
            self._world.set_rule(spot, _res)
