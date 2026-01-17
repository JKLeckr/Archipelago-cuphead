### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import IntEnum

from ..deps import Dep
from ..rulebase import RegionRule # TODO: Remove

if typing.TYPE_CHECKING:
    from ...wconf import WorldConfig

LevelRule = Callable[["WorldConfig"], RegionRule] # TODO: Remove
LRSelector = Callable[["WorldConfig"], Mapping[str, int]]

### Base intermediary representation data classes

## Rule Expressions

@dataclass(frozen=True)
class RuleExpr:
    source_path: str

@dataclass(frozen=True)
class PresetRef(RuleExpr):
    item: RuleContainer | None
    name: str

@dataclass(frozen=True)
class And(RuleExpr):
    items: list[RuleExpr]

@dataclass(frozen=True)
class Or(RuleExpr):
    items: list[RuleExpr]

@dataclass(frozen=True)
class Not(RuleExpr):
    item: RuleExpr


## Item Rules

@dataclass(frozen=True)
class ItemRule(RuleExpr): ...

@dataclass(frozen=True)
class ItemRuleHas(ItemRule):
    items: list[str]
    has_any: bool
    count: int

@dataclass(frozen=True)
class ItemRuleHasSelection(ItemRule):
    selector: LRSelector
    selector_name: str
    has_any: bool

@dataclass(frozen=True)
class ItemRuleHasFromList(ItemRule):
    items: list[str]
    count: int
    unique: bool

@dataclass(frozen=True)
class ItemRuleHasGroup(ItemRule):
    group: str
    count: int
    unique: bool

## Deps

@dataclass(frozen=True)
class RuleDep:
    source_path: str
    ref: Dep
    negated: bool
    name: str

    def eval(self, wconf: WorldConfig) -> bool:
        res = self.ref(wconf)
        return not res if self.negated else res


## Rule Containers

@dataclass(frozen=True)
class RuleFragment:
    source_path: str
    when: list[RuleDep]
    requires: RuleExpr


@dataclass(frozen=True)
class RuleContainer:
    source_path: str
    rules: list[RuleFragment]


## Data Structure

class InheritMode(IntEnum):
    NONE = 0
    AND = 1
    OR = 2

@dataclass(frozen=True)
class LocationDef(RuleContainer):
    inherit: InheritMode

@dataclass(frozen=True)
class LevelDef:
    source_path: str
    access: RuleContainer | None
    base: RuleContainer | None
    locations: dict[str, LocationDef]

@dataclass(frozen=True)
class LevelRules:
    levels: dict[str, LevelDef]
    presets: dict[str, RuleContainer]
