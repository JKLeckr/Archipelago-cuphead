from __future__ import annotations
from typing import Iterable, TypeVar

T = TypeVar("T")

def count_in_list(e: T, ls: Iterable[T]):
    count = 0
    for el in ls:
        if el == e:
            count += 1
    return count

def format_list(ls: Iterable[T]) -> str:
    res = "["
    first = True
    if ls:
        for item in ls:
            if not first:
                res += ","
            else:
                first = False
            res += str(item)
    res += "]"
    return res

def scrub_list(a: list[T], b: Iterable[T]) -> list[T]:
    newlist: list[T] = []
    for item in a:
        if item in b:
            newlist.append(item)
    return newlist
