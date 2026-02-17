### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import dataclasses
from typing import Any, Self

from typing_extensions import override

from rule_builder.options import OptionFilter

from ...options import CupheadOptions
from . import deps
from .depbase import DEPS, Dep

# DepFilters integrate Deps into rule_builder.

@dataclasses.dataclass(frozen=True, init=False)
class DepFilter(OptionFilter):
    fn: Dep
    __name__: str

    def __init__(self, fn: Dep):
        super().__init__(None, None)  # pyright: ignore[reportArgumentType]
        object.__setattr__(self, "fn", fn)
        object.__setattr__(self, "__name__", fn.__name__ if hasattr(fn, "__name__") else "anonymous_dep")

    def __call__(self, c: CupheadOptions) -> bool:
        return self.fn(c)

    @override
    def to_dict(self) -> dict[str, Any]:
        """Returns a JSON compatible dict representation of this Dep"""
        return {
            "when": _dep_to_expr(self)
        }

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:  # type: ignore
        """Returns a new Dep instance from a dict representation"""
        expr = data.get("when")
        if not isinstance(expr, str) or not expr.strip():
            raise ValueError("Dep dict must contain a non-empty string 'when' value")
        return _parse_dep_expr(expr)  # type: ignore[return-value]

    @override
    def check(self, options: Any) -> bool:
        """Tests the given options dataclass to see if it passes this Dep"""
        if isinstance(options, CupheadOptions):
            return self.fn(options)
        raise ValueError("options is invalid!")

    def __and__(self, other: DepFilter) -> DepFilter:
        return depf_and(self, other)

    def __or__(self, other: DepFilter) -> DepFilter:
        return depf_or(self, other)

    def __invert__(self) -> DepFilter:
        return depf_not(self)

def depf_and(*deps: DepFilter) -> DepFilter:
    expr = f"and[{', '.join(_dep_to_expr(d) for d in deps)}]"
    return _make_composite(lambda c: all(d(c) for d in deps), expr)
def depf_or(*deps: DepFilter) -> DepFilter:
    expr = f"or[{', '.join(_dep_to_expr(d) for d in deps)}]"
    return _make_composite(lambda c: any(d(c) for d in deps), expr)
def depf_not(d: DepFilter) -> DepFilter:
    expr = f"not[{_dep_to_expr(d)}]"
    return _make_composite(lambda c: not d(c), expr)

depf_none = DepFilter(deps.dep_none)

def _make_composite(fn: Dep, expr: str) -> DepFilter:
    wrapped = DepFilter(fn)
    object.__setattr__(wrapped, "__name__", expr)
    return wrapped

def _dep_to_expr(d: DepFilter) -> str:
    name = d.__name__.strip()
    if (
        name.startswith("and[")
        or name.startswith("or[")
        or name.startswith("not[")
    ):
        return name
    if name == "_dep_none":
        return "none"
    return name.removeprefix("dep_")

def _split_args(body: str) -> list[str]:
    args: list[str] = []
    depth = 0
    start = 0
    for i, ch in enumerate(body):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth < 0:
                raise ValueError("Unbalanced brackets in dep expression")
        elif ch == "," and depth == 0:
            args.append(body[start:i].strip())
            start = i + 1
    if depth != 0:
        raise ValueError("Unbalanced brackets in dep expression")
    tail = body[start:].strip()
    if tail:
        args.append(tail)
    return args

def _parse_dep_expr(expr: str) -> DepFilter:
    text = expr.strip()
    if text.startswith("and[") and text.endswith("]"):
        args = _split_args(text[4:-1])
        if not args:
            raise ValueError("and[...] requires at least one argument")
        return depf_and(*(_parse_dep_expr(arg) for arg in args))
    if text.startswith("or[") and text.endswith("]"):
        args = _split_args(text[3:-1])
        if not args:
            raise ValueError("or[...] requires at least one argument")
        return depf_or(*(_parse_dep_expr(arg) for arg in args))
    if text.startswith("not[") and text.endswith("]"):
        args = _split_args(text[4:-1])
        if len(args) != 1:
            raise ValueError("not[...] requires exactly one argument")
        return depf_not(_parse_dep_expr(args[0]))
    if text == "none":
        return depf_none
    if text in DEPS:
        return DepFilter(DEPS[text])
    if text.startswith("dep_") and text.removeprefix("dep_") in DEPS:
        return DepFilter(DEPS[text.removeprefix("dep_")])
    raise ValueError(f"Unknown dep name '{text}'")
