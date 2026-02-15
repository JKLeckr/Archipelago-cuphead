### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from typing import Any, ClassVar, Generic, TypeVar

from typing_extensions import override

from Options import NumericOption, Option, Visibility

T = TypeVar("T")

class ConstOption(Option[Any], Generic[T]):
    value: T
    default: ClassVar[Any] = 0
    visibility = Visibility.none

    def __init__(self):
        pass

    @classmethod
    @override
    def from_any(cls, data: Any) -> ConstOption[T]:
        return ConstOption[T]()

class ConstNumericOption(NumericOption):
    value: int
    visibility = Visibility.none

    def __init__(self):
        pass

    @classmethod
    @override
    def from_any(cls, data: Any) -> ConstNumericOption:
        return ConstNumericOption()
