### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from rule_builder.rules import Has, HasAny

from ...names import itemnames as i
from ..dep import deps
from ..dep.depfilter import DepFilter
from .levelrulebase import RBRule, RuleContainer, RulePreset, lrpreset


@lrpreset
def lrp_plane() -> RuleContainer:
    return RuleContainer([
        RBRule(
            Has(i.item_plane_gun, options=[DepFilter(deps.dep_hard_logic, False)])
        ),
        RBRule(
            HasAny(i.item_plane_gun, i.item_plane_bombs, options=[DepFilter(deps.dep_hard_logic, False)])
        )
    ])
