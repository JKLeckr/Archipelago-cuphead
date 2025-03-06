from __future__ import annotations
import Utils
from typing import Any, Iterable
from worlds.AutoWorld import World
from BaseClasses import Region
from .auxiliary import format_list

def test_duplicates(ls: Iterable[Any]) -> int:
    seen: set[Any] = set()
    dups: list[Any] = []
    for x in ls:
        if x in seen:
            dups.append(x)
        else:
            seen.add(x)
    print("Duplicates: "+str(dups))
    print("Total Duplicates: "+str(len(dups)))
    return len(dups)

def print_list_each_line(ls: Iterable[Any]) -> None:
    for item in ls:
        print(item)

def print_list(ls: Iterable[Any]) -> None:
    print(format_list(ls))

def print_locations(world: World) -> None:
    locations = world.multiworld.get_locations(world.player)
    for loc in locations:
        print(f"{loc.name}: {loc.access_rule}")

def visualize_regions(root_region: Region, file_name: str) -> None:
    Utils.visualize_regions(root_region, file_name, show_entrance_names=True, show_locations=True, show_other_regions=True, linetype_ortho=True)
