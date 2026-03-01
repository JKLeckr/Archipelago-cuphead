### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from enum import IntEnum
from typing import ClassVar

from typing_extensions import override

from rule_builder.options import OptionFilter
from rule_builder.rules import And as RBAnd
from rule_builder.rules import HasAllCounts, HasAnyCount, Rule, True_
from rule_builder.rules import Or as RBOr

from ...options import CupheadOptions

LRPreset = Callable[[], "RuleList"]

LRPRESETS: dict[str, LRPreset] = {}
def lrpreset(fn: LRPreset) -> LRPreset:
    _name = fn.__name__.removeprefix("lrp_")
    LRPRESETS[_name] = fn
    return fn

LRSelector = Callable[["CupheadOptions"], dict[str, int]]

### Base intermediary representation data classes

def compile_rule_list(
    rules: Iterable[RuleExpr],
    options: CupheadOptions,
    op_and: bool = True, # or if false
    filters: Iterable[OptionFilter] = ()
) -> Rule:
    def _check_filter(opt: OptionFilter) -> bool:
        res = opt.check(options)
        # DepFilter stores negation in `value`.
        value = getattr(opt, "value", True)
        return res if value else not res

    # If the parent expression options fail, this expression is inactive.
    if not all(_check_filter(opt) for opt in filters):
        return True_()

    _rules = [rule.eval(options) for rule in rules]
    if not _rules:
        return True_()
    if len(_rules) == 1:
        return _rules[0]
    return RBAnd(*_rules) if op_and else RBOr(*_rules)

## Rule Expressions

@dataclass(frozen=True)
class Evaluable(ABC):
    @abstractmethod
    def eval(self, options: CupheadOptions) -> Rule: ...

@dataclass(frozen=True)
class RuleExpr(Evaluable, ABC): ...

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

@dataclass(frozen=True)
class RuleRef(RuleExpr):
    ref_name: str
    options: Iterable[OptionFilter]

    def __init__(self, ref: str, options: Iterable[OptionFilter] = ()):
        object.__setattr__(self, "ref_name", ref)
        object.__setattr__(self, "options", options)

    @override
    def eval(self, options: CupheadOptions) -> Rule:
        raise NotImplementedError("RuleRefs cannot be evaled directly")

@dataclass(frozen=True, init=False)
class RulePreset(RuleExpr):
    rules: RuleList
    options: Iterable[OptionFilter]
    _ref_name: str
    __cache: ClassVar[dict[tuple[str, tuple[str, ...]], Rule]] = {}

    @property
    def preset_name(self) -> str:
        return self._ref_name

    def __init__(self, preset: LRPreset, options: Iterable[OptionFilter] = ()):
        object.__setattr__(self, "_ref_name", preset.__name__)
        object.__setattr__(self, "rules", preset())
        object.__setattr__(self, "options", options)

    @override
    def eval(self, options: CupheadOptions) -> Rule:
        opt_key = tuple(str(opt) for opt in self.options)
        cache_key = (self._ref_name, opt_key)
        res = self.__class__.__cache.get(cache_key)
        if res is None:
            res = compile_rule_list(self.rules, options, True, self.options)
            self.__class__.__cache[cache_key] = res
        return res

@dataclass(frozen=True)
class And(RuleExpr):
    items: Iterable[RuleExpr]
    options: Iterable[OptionFilter] = ()

    def __init__(self, *items: RuleExpr, options: Iterable[OptionFilter] = ()):
        object.__setattr__(self, "items", items)
        object.__setattr__(self, "options", options)

    @override
    def eval(self, options: CupheadOptions) -> Rule:
        return compile_rule_list(self.items, options, True, self.options)

@dataclass(frozen=True)
class Or(RuleExpr):
    items: Iterable[RuleExpr]
    options: Iterable[OptionFilter]

    def __init__(self, *items: RuleExpr, options: Iterable[OptionFilter] = ()):
        object.__setattr__(self, "items", items)
        object.__setattr__(self, "options", options)

    @override
    def eval(self, options: CupheadOptions) -> Rule:
        return compile_rule_list(self.items, options, False, self.options)


## Rule Containers

RuleList = list[RuleExpr]

## Data Structure

class InheritMode(IntEnum):
    NONE = 0
    AND = 1
    OR = 2

@dataclass(frozen=True)
class LocationDef(RuleList):
    rules: RuleList = field(default_factory=RuleList)
    inherit: InheritMode = InheritMode.AND

@dataclass(frozen=True)
class LevelDef:
    locations: dict[str, LocationDef]
    exit_location: str
    access: RuleList = field(default_factory=RuleList)
    base: RuleList = field(default_factory=RuleList)
    ruledefs: dict[str, RuleList] = field(default_factory=dict[str, RuleList])

    def __init__(
        self,
        locations: dict[str, LocationDef],
        exit_location: str | None = None,
        access: RuleList | None = None,
        base: RuleList | None = None,
        ruledefs: dict[str, RuleList] | None = None
    ):
        object.__setattr__(self, "locations", locations)
        object.__setattr__(self, "exit_location", exit_location if exit_location else "")
        object.__setattr__(self, "access", access if access else [])
        object.__setattr__(self, "base", base if base else [])
        object.__setattr__(self, "ruledefs", ruledefs if ruledefs else {})

@dataclass(frozen=True)
class LevelRules:
    levels: dict[str, LevelDef]
