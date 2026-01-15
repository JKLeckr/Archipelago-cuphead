### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from typing import NamedTuple

if typing.TYPE_CHECKING:
    from ..rules.levelrules.levelrulebase import LevelRule

class LevelData(NamedTuple):
    world_location: str | None
    locations: list[str]
    rule: LevelRule | None = None
