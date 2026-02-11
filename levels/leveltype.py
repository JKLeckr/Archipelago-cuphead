### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations
from . import leveldefs as ldefs

def get_level_type(level: str) -> str:
    if (level in ldefs.level_boss):
        return "boss"
    elif (level in ldefs.level_rungun):
        return "rungun"
    else:
        return "none"
