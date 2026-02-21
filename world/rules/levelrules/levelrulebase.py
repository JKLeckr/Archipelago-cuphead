### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import IntEnum

from rule_builder.options import OptionFilter
from rule_builder.rules import HasAllCounts, HasAnyCount, Rule

from ...options import CupheadOptions
from ..dep import Dep

LRPreset = Callable[[], "RuleContainer"]

LRPRESETS: dict[str, LRPreset] = {}
def lrpreset(fn: LRPreset) -> LRPreset:
    _name = fn.__name__.removeprefix("lrp_")
    LRPRESETS[_name] = fn
    return fn

LRSelector = Callable[["CupheadOptions"], dict[str, int]]

### Base intermediary representation data classes

## Rule Expressions

@dataclass(frozen=True)
class RuleExpr: ...

@dataclass(frozen=True)
class RBRule(RuleExpr):
    rule: Rule

@dataclass(frozen=True)
class SelectRule(RuleExpr):
    select: LRSelector
    any: bool
    options: Iterable[OptionFilter] = ()

    def eval(self, options: CupheadOptions) -> Rule:
        select = self.select(options)
        return HasAnyCount(select) if self.any else HasAllCounts(select)

@dataclass(frozen=True, init=False)
class RulePreset(RuleExpr):
    rule: RuleContainer
    _preset_name: str

    @property
    def preset_name(self) -> str:
        return self._preset_name

    def __init__(self, preset: LRPreset):
        object.__setattr__(self, "_preset_name", preset.__name__)
        object.__setattr__(self, "rule", preset())

@dataclass(frozen=True)
class And(RuleExpr):
    items: list[RuleExpr]

@dataclass(frozen=True)
class Or(RuleExpr):
    items: list[RuleExpr]

## Deps

@dataclass(frozen=True)
class RuleDep:
    ref: Dep
    negated: bool
    name: str

    def eval(self, options: CupheadOptions) -> bool:
        res = self.ref(options)
        return not res if self.negated else res


## Rule Containers

@dataclass(frozen=True)
class RuleList:
    rules: list[RuleExpr]

@dataclass(frozen=True)
class RuleContainer(RuleList):
    rules: list[RuleExpr]
    options: Iterable[OptionFilter] = ()


## Data Structure

class InheritMode(IntEnum):
    NONE = 0
    AND = 1
    OR = 2

@dataclass(frozen=True)
class LocationDef(RuleList):
    inherit: InheritMode

@dataclass(frozen=True)
class LevelDef:
    access: RuleContainer | None
    exit_location: str | None
    base: RuleContainer | None
    locations: dict[str, LocationDef]

@dataclass(frozen=True)
class LevelRules:
    levels: dict[str, LevelDef]
    presets: dict[str, RuleContainer]
