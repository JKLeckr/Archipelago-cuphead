### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0
"""
import typing
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import IntEnum

from worlds.cuphead.world.wconf import WorldConfig

from ..deps import Dep

from rule_builder.rules import And, Has, Rule

from .levelrulebase import RuleData

from ...names import itemnames as i
from ...names import locationnames as l
from ...names import regionnames as r
"""
