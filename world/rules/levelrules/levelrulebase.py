### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ..deps import Dep
from .levelrules import LevelRule

### Base intermediary representation data classes

## Rule Expressions

class RuleExpr: ...

@dataclass(frozen=True)
class LRule(RuleExpr):
    rule: LevelRule
    name: str

@dataclass(frozen=True)
class PresetRef(RuleExpr):
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


## Deps

@dataclass(frozen=True)
class RuleDep:
    ref: Dep
    negated: bool
    name: str


## Rule Containers

@dataclass(frozen=True)
class RuleFragment:
    when: list[RuleDep]
    requires: RuleExpr
    source_path: str


@dataclass(frozen=True)
class RuleContainer:
    rules: list[RuleFragment]
    source_path: str


## Data Structure

@dataclass(frozen=True)
class LocationDef:
    rule: RuleContainer | None
    inherit: Literal["and", "or", "none"]

@dataclass(frozen=True)
class LevelDef:
    access: RuleContainer | None
    base: RuleContainer | None
    locations: dict[str, LocationDef]

@dataclass(frozen=True)
class LevelRules:
    levels: dict[str, LevelDef]
    presets: dict[str, RuleContainer]
