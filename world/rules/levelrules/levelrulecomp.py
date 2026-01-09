### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import typing
from collections.abc import Callable, Iterable

from .. import deps
from . import levelrulebase as lrb
from . import levelrules

if typing.TYPE_CHECKING:
    from .... import CupheadWorld

def compile_levelrules(world: CupheadWorld) -> None:
    pass
