### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from typing import Any, Generic, TypeVar

from typing_extensions import override

from Options import NumericOption, Option, Visibility

T = TypeVar("T")

class ConstOption(Option[Any], Generic[T]):
    value: T
    default: Any = 0
    visibility = Visibility.none

    def __init__(self):
        if not self.value:
            raise ValueError(f"{self.__class__.__name__} value is not set.")
        self.default = self.value

    @classmethod
    @override
    def from_any(cls, data: Any) -> ConstOption[T]:
        return ConstOption[T]()

class ConstNumericOption(NumericOption):
    value: int
    default: int = 0
    visibility = Visibility.none

    def __init__(self):
        if not self.value:
            self.value = self.default
            raise Warning(f"{self.__class__.__name__} value is not set. Using default value of {self.default}")
        self.default = self.value

    @classmethod
    @override
    def from_any(cls, data: Any) -> ConstNumericOption:
        return ConstNumericOption()
