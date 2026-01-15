### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing

from . import levelrulebase as lrb
from . import levelrulecomp as lrc

if typing.TYPE_CHECKING:
    from .... import CupheadWorld

LevelRule = lrb.LevelRule

def set_levelrules(world: CupheadWorld) -> None:
    lrc.compile_levelrules(world)
