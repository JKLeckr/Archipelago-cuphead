from typing import Iterable, Any

def count_in_list(e: Any, ls: list[Any]):
    count = 0
    for el in ls:
        if el == e:
            count += 1
    return count

def format_list(ls: list[Any]) -> str:
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

def scrub_list(a: list[Any], b: Iterable[Any]) -> list[Any]:
    newlist: list[Any] = []
    for item in a:
        if item in b:
            newlist.append(item)
    return newlist
