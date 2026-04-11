### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from typing_extensions import override

from rule_builder import rules as rb
from rule_builder.rules import Rule, WrapperRule

from ...consts import GAME_NAME as GAME

if TYPE_CHECKING:
    from .... import CupheadWorld

@dataclass(init=False)
class Has(rb.Has, game=GAME):
    filtered_resolution: bool = field(default=True, kw_only=True)

@dataclass(init=False)
class HasAll(rb.HasAll, game=GAME):
    filtered_resolution: bool = field(default=True, kw_only=True)

@dataclass(init=False)
class HasAny(rb.HasAny, game=GAME):
    filtered_resolution: bool = field(default=True, kw_only=True)

@dataclass(init=False)
class HasGroup(rb.HasGroup, game=GAME):
    filtered_resolution: bool = field(default=True, kw_only=True)

@dataclass
class Filtered(WrapperRule["CupheadWorld"], game=GAME):
    filtered_resolution: bool = field(default=True, kw_only=True)

    @override
    def _instantiate(self, world: "CupheadWorld") -> Rule.Resolved:
        return self.child.resolve(world)
