### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from enum import IntEnum

from rule_builder.options import OptionFilter
from rule_builder.rules import Rule

from ...options import CupheadOptions

LRPreset = Callable[[], "RuleList"]

LRPRESETS: dict[str, LRPreset] = {}
def lrpreset(fn: LRPreset) -> LRPreset:
    _name = fn.__name__.removeprefix("lrp_")
    LRPRESETS[_name] = fn
    return fn

LRSelector = Callable[["CupheadOptions"], dict[str, int]]

### Base intermediary representation data classes

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


@dataclass(frozen=True)
class RuleRef(RuleExpr):
    ref_name: str
    options: Iterable[OptionFilter]

    def __init__(self, ref: str, options: Iterable[OptionFilter] = ()):
        object.__setattr__(self, "ref_name", ref)
        object.__setattr__(self, "options", options)


@dataclass(frozen=True, init=False)
class RulePreset(RuleExpr):
    rules: RuleList
    options: Iterable[OptionFilter]
    _ref_name: str

    @property
    def preset_name(self) -> str:
        return self._ref_name

    def __init__(self, preset: LRPreset, options: Iterable[OptionFilter] = ()):
        object.__setattr__(self, "_ref_name", preset.__name__)
        object.__setattr__(self, "rules", preset())
        object.__setattr__(self, "options", options)


@dataclass(frozen=True)
class And(RuleExpr):
    items: Iterable[RuleExpr]
    options: Iterable[OptionFilter] = ()

    def __init__(self, *items: RuleExpr, options: Iterable[OptionFilter] = ()):
        object.__setattr__(self, "items", items)
        object.__setattr__(self, "options", options)


@dataclass(frozen=True)
class Or(RuleExpr):
    items: Iterable[RuleExpr]
    options: Iterable[OptionFilter]

    def __init__(self, *items: RuleExpr, options: Iterable[OptionFilter] = ()):
        object.__setattr__(self, "items", items)
        object.__setattr__(self, "options", options)


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
