### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from typing import NamedTuple


class LevelData(NamedTuple):
    world_location: str | None
    locations: list[str]
