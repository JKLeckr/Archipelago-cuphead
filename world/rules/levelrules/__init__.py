### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing

from . import levelrulecomp as lrc

if typing.TYPE_CHECKING:
    from .... import CupheadWorld

def set_levelrules(world: CupheadWorld) -> None:
    lrc.compile_levelrules(world)
