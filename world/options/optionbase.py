### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Generic, TypeVar

from typing_extensions import override

from Options import Choice, NumericOption, Option, OptionDict, OptionError, Range, Toggle, Visibility

from . import _levelset

T = TypeVar("T")

class BToggle(Toggle):
    @property
    def bvalue(self) -> bool:
        return bool(self.value)

class BDefaultOnToggle(BToggle):
    default = 1

class ChoiceEx(Choice):
    random_value: int = -1

    @override
    @classmethod
    def from_text(cls, text: str) -> Choice:
        text = text.lower()
        if text == "random":
            return cls(cls.random_value)
        return super().from_text(text)

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

class LevelDict(OptionDict):
    valid_keys: Iterable[str] = frozenset(_levelset.levels)
    valid_values: Iterable[str] = valid_keys

    def __init__(self, value: dict[str, Any]):
        res: dict[str, str] = {}
        for x, y in value.items():
            if x in self.valid_keys and y in self.valid_values:
                res[x] = y
            else:
                raise OptionError(f"Option {self.__class__.__name__} contains invalid levels. '{x}: {y}' is invalid")
        super().__init__(res)

class Weight(Range):
    range_start = 0
    range_end = 10
    weight_max = 100

    def __init__(self, value: int):
        if value < 0:
            raise OptionError(f"Option {self.__class__.__name__} cannot be negative!")
        if value > self.weight_max:
            raise OptionError(f"Option {self.__class__.__name__} cannot be larger than {self.weight_max}!")
        self.value = value
