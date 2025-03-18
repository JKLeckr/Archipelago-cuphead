#!/usr/bin/env python3

import sys
from .items import items_all
from .locations import locations_all

def print_items():
    print("-- Items --")
    for item, data in items_all.items():
        print(f"{item}: {data.id} | {data.item_type}")
    print("")
def print_locations():
    print("-- Locations --")
    for item, data in locations_all.items():
        print(f"{item}: {data.id} | {data.progress_type}")
    print("")

def print(mode: str):
    if (mode == "items".lower() or mode == "all".lower()):
        print_items()
    if (mode == "locations".lower() or mode == "all".lower()):
        print_locations()

if __name__ == "__main__":
    if len(sys.argv) >= 1:
        arg = sys.argv[1]
    else:
        arg = "all"
    print(arg)
