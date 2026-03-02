### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import dataclasses
from typing import Any, Self

from typing_extensions import override

from Options import CommonOptions
from rule_builder.options import OptionFilter

from ...options import CupheadOptions
from .depbase import DEPS, Dep

# DepFilters integrate Deps into rule_builder.

@dataclasses.dataclass(frozen=True, init=False)
class DepFilter(OptionFilter):
    fn: Dep
    value: bool
    _fn_name: str

    def __init__(self, fn: Dep, value: bool = True):
        super().__init__(None, None)  # pyright: ignore[reportArgumentType]
        object.__setattr__(self, "fn", fn)
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "_fn_name", fn.__name__)

    def __call__(self, c: CupheadOptions) -> bool:
        return self.fn(c)

    @override
    def to_dict(self) -> dict[str, Any]:
        """Returns a JSON compatible dict representation of this Dep"""
        return {
            "when": self._fn_name,
            "condition": self.value
        }

    @override
    def check(self, options: CommonOptions) -> bool:
        """Tests the given options dataclass to see if it passes this Dep"""
        if isinstance(options, CupheadOptions):
            return self.fn(options) == self.value
        raise ValueError("options is invalid!")

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:  # type: ignore
        """Returns a new Dep instance from a dict representation"""
        expr = data.get("when")
        if not isinstance(expr, str) or not expr.strip():
            raise ValueError("Dep dict must contain a non-empty string 'when' value")

        value = data.get("condition", True)

        if expr in DEPS:
            return cls(fn=DEPS[expr], value=value)
        raise ValueError(f"Unknown dep name '{expr}'")

    @override
    def __str__(self) -> str:
        prefix = "!" if not self.value else ""
        return f"{prefix}{self._fn_name}"
