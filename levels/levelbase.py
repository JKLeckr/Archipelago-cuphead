from __future__ import annotations
from typing import NamedTuple
from .levelrules import LevelRule
from . import levelrules as lr

class LevelData(NamedTuple):
    world_location: str | None
    locations: list[str]
    rule: LevelRule = lr.level_rule_none
