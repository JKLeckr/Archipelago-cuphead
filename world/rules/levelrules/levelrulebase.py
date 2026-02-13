### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from collections.abc import Callable, Mapping
from dataclasses import dataclass

from typing_extensions import override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.rules import And, False_, Has, HasAll, HasAllCounts, NestedRule, Rule, True_, TWorld

from ..deps import Dep, dep_none

if typing.TYPE_CHECKING:
    from ...wconf import WorldConfig

LRSelector = Callable[["WorldConfig"], Mapping[str, int]]

@dataclass(frozen=True)
class RuleUnit:
    rule: Rule
    when: Dep

@dataclass(frozen=True)
class RuleData:
    rules: list[RuleUnit]

    def compile_rules(self, wconf: WorldConfig) -> Rule | None:
        rulelist: list[Rule] = []
        for rule in self.rules:
            if rule.when(wconf):
                rulelist.append(rule.rule)
        rllen = len(rulelist)
        if rllen == 1:
            return rulelist[0]
        if rllen > 1:
            return And(*rulelist)
        return True_()
