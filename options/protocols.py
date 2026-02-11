### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import Protocol

class CupheadOption(Protocol):
    name: str
    @property
    def current_key(self) -> str:
        return ""

class CupheadNumericOption(CupheadOption, Protocol):
    value: int

class CupheadOptionSet(CupheadOption, Protocol):
    value: set[str]
