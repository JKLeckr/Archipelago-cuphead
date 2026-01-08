### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from dataclasses import dataclass
from typing import Literal

from ..deps import DEPS, Dep

if typing.TYPE_CHECKING:
    from ...wconf import WorldConfig

### Base intermediary representation data classes

## Rule Expressions

class RuleExpr: ...

@dataclass(frozen=True)
class RuleRef(RuleExpr):
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
    _expr: Dep
    _expr_name: str

    @classmethod
    def from_str(cls, dep: str) -> RuleDep:
        try:
            _expr = DEPS[dep]
        except KeyError as e:
            raise KeyError(f"'{dep}' is not a valid dep!") from e
        return cls(_expr, dep)

    def eval(self, wconf: WorldConfig) -> bool:
        return self._expr(wconf)


## Rule Containers

@dataclass(frozen=True)
class RuleFragment:
    when: tuple[Dep, ...]
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
