from __future__ import annotations
import typing
from typing import NamedTuple
if typing.TYPE_CHECKING:
    from .levelrules import LevelRule

class LevelData(NamedTuple):
    world_location: str | None
    locations: list[str]
    rule: LevelRule | None = None
