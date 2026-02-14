### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field

from rule_builder.rules import And, Filtered, Rule, True_

from ..dep.depfilter import DepFilter, depf_none

if typing.TYPE_CHECKING:
    from ...wconf import WorldConfig

LRSelector = Callable[["WorldConfig"], Mapping[str, int]]

@dataclass(frozen=True)
class RuleUnit:
    rule: Rule
    when: DepFilter = depf_none

@dataclass(frozen=True)
class RuleData:
    rules: list[RuleUnit] = field(default_factory=list[RuleUnit])

    def compile_rules(self, wconf: WorldConfig) -> Rule:
        """
        Compiles the rules into a single Rule using
        rule_builder's native filtering (via Dep as OptionFilter).
        Resolves to True_() if there are no rules.
        """
        rulelist: list[Rule] = []
        for unit in self.rules:
            if unit.when is depf_none:
                rulelist.append(unit.rule)
            else:
                rulelist.append(Filtered(unit.rule, options=(unit.when,)))
        rllen = len(rulelist)
        if rllen == 0:
            return True_()
        if rllen == 1:
            return rulelist[0]
        return And(*rulelist)

def when(rule: Rule, depf: DepFilter) -> Rule:
    """Wraps a rule with a dep filter condition, resolving to False if the condition is not met."""
    return Filtered(rule, options=(depf,))
