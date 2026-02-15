### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from typing import Any, ClassVar, Generic, TypeVar

from typing_extensions import override

from Options import NumericOption, Option, Visibility

T = TypeVar("T")

class NonUserOption(Option[Any], Generic[T]):
    value: T
    default: ClassVar[Any]
    visibility = Visibility.none

    def __init__(self):
        self.value = self.default

    @classmethod
    @override
    def from_any(cls, data: Any) -> NonUserOption[T]:
        return NonUserOption[T]()

class NonUserNumericOption(NumericOption):
    value: int
    visibility = Visibility.none

    def __init__(self):
        self.value = self.default

    @classmethod
    @override
    def from_any(cls, data: Any) -> NonUserNumericOption:
        return NonUserNumericOption()
