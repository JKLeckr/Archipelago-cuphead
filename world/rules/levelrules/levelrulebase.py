### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import IntEnum
from typing import ClassVar, Literal

from typing_extensions import override

from rule_builder.options import OptionFilter
from rule_builder.rules import HasAllCounts, HasAnyCount, Rule, True_

from ...options import CupheadOptions
from ..dep import Dep

LRPreset = Callable[[], "RuleList"]

LRPRESETS: dict[str, LRPreset] = {}
def lrpreset(fn: LRPreset) -> LRPreset:
    _name = fn.__name__.removeprefix("lrp_")
    LRPRESETS[_name] = fn
    return fn

LRSelector = Callable[["CupheadOptions"], dict[str, int]]

### Base intermediary representation data classes

def compile_rule_list(
    rules: list[RuleExpr],
    op: Literal["and", "or"],
    options: Iterable[OptionFilter] = ()
) -> Rule:
    return True_() # TODO Finish

## Rule Expressions

@dataclass(frozen=True)
class RuleExpr(ABC):
    @abstractmethod
    def eval(self, options: CupheadOptions) -> Rule: ...

@dataclass(frozen=True)
class RBRule(RuleExpr):
    rule: Rule

    @override
    def eval(self, options: CupheadOptions) -> Rule:
        return self.rule

@dataclass(frozen=True)
class SelectRule(RuleExpr):
    select: LRSelector
    any: bool
    options: Iterable[OptionFilter] = ()

    @override
    def eval(self, options: CupheadOptions) -> Rule:
        select = self.select(options)
        return HasAnyCount(select) if self.any else HasAllCounts(select)

@dataclass(frozen=True, init=False)
class RulePreset(RuleExpr):
    rule: RuleList
    options: Iterable[OptionFilter]
    _preset_name: str
    _cache: ClassVar[dict[str, Rule]] = {}

    @property
    def preset_name(self) -> str:
        return self._preset_name

    def __init__(self, preset: LRPreset, options: Iterable[OptionFilter] = ()):
        object.__setattr__(self, "_preset_name", preset.__name__)
        object.__setattr__(self, "rule", preset())
        object.__setattr__(self, "options", options)

    @override
    def eval(self, options: CupheadOptions) -> Rule:
        res = self.__class__._cache.get(self._preset_name)
        if res is None:
            res = compile_rule_list(self.rule.rules, "and", self.options)
            self.__class__._cache[self._preset_name] = res
        return res

@dataclass(frozen=True)
class And(RuleExpr):
    items: list[RuleExpr]
    options: Iterable[OptionFilter] = ()

    @override
    def eval(self, options: CupheadOptions) -> Rule:
        return compile_rule_list(self.items, "and", self.options)

@dataclass(frozen=True)
class Or(RuleExpr):
    items: list[RuleExpr]
    options: Iterable[OptionFilter] = ()

    @override
    def eval(self, options: CupheadOptions) -> Rule:
        return compile_rule_list(self.items, "or", self.options)

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
    access: RuleList | None
    exit_location: str | None
    base: RuleList | None
    locations: dict[str, LocationDef]

@dataclass(frozen=True)
class LevelRules:
    levels: dict[str, LevelDef]
    presets: dict[str, RuleList]
