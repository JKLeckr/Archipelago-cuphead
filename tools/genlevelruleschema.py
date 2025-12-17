#!/usr/bin/env python3

### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

import argparse
import importlib.util
import json
import os
import sys

THIS_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(THIS_DIR, "..", "..", ".."))

WORLD_MOD = "world"
RULES_MOD = ".rules"
RULES_MOD_PATH = f"{WORLD_MOD}{RULES_MOD}"
DEP_MOD = ".deps"
DEP_MOD_PATH = f"{RULES_MOD_PATH}{DEP_MOD}"
LEVELS_MOD = ".levels"
LEVELS_MOD_PATH = f"{WORLD_MOD}{LEVELS_MOD}"
LEVELRULES_MOD = ".levelrules"
LEVELRULES_MOD_PATH = f"{RULES_MOD_PATH}{LEVELRULES_MOD}"
NAMES_MOD = ".names"
NAMES_MOD_PATH = f"{WORLD_MOD}{NAMES_MOD}"

WORLD_MOD_PATH = os.path.join(WORLD_MOD, "__init__.py")
BASE_SCHEMA_PATH = os.path.join(THIS_DIR, "schemas", "levelrules.schema.json")

DEST_DIR = os.path.join("schemas", "levelrules.generated.schema.json")


def main():  # noqa: C901
    _fate_desc = (f"that files will be read from '{ROOT_DIR}'."
        " This directory must be the Archipelago root directory!"
        f" Files will be written to '{DEST_DIR}'."
    )

    parser = argparse.ArgumentParser(description="Generate levelrules schema from apworld rules")
    parser.add_argument(
        "--yes",
        help=f"Accept {_fate_desc}",
        action="store_true"
    )
    parser.add_argument(
        "-L",
        "--include-lnames",
        help="Include level and location names in the schema",
        action="store_true"
    )

    args = parser.parse_args()

    if not args.yes:
        print(f"Use --yes to accept {_fate_desc}")
        exit(0)

    sys.path.insert(0, ROOT_DIR)

    _wspec = importlib.util.spec_from_file_location(WORLD_MOD, WORLD_MOD_PATH)
    _world = _wspec.loader.load_module(WORLD_MOD) if _wspec and _wspec.loader else None

    _rspec = importlib.util.find_spec(RULES_MOD, package=WORLD_MOD)
    _rules = _rspec.loader.load_module(RULES_MOD_PATH) if _rspec and _rspec.loader else None

    _dspec = importlib.util.find_spec(DEP_MOD, package=RULES_MOD_PATH)
    _deps = _dspec.loader.load_module(DEP_MOD_PATH) if _dspec and _dspec.loader else None

    _lrspec = importlib.util.find_spec(LEVELRULES_MOD, package=RULES_MOD_PATH)
    _levelrules = _lrspec.loader.load_module(LEVELRULES_MOD_PATH) if _lrspec and _lrspec.loader else None

    if not _deps or not _levelrules:
        raise ImportError("Could not import necessary modules.")

    deps = _deps
    levelrules = _levelrules

    if args.include_lnames:
        _nspec = importlib.util.find_spec(NAMES_MOD, package=WORLD_MOD)
        _names = _nspec.loader.load_module(NAMES_MOD_PATH) if _nspec and _nspec.loader else None
        if not _names:
            raise ImportError("Could not import names module.")
        names = _names
    else:
        names = None

    base = json.load(open(BASE_SCHEMA_PATH))

    lrule_names = sorted(levelrules.LRULES)
    dep_names = sorted(deps.DEPS)

    # Patch enums
    for variant in base["$defs"]["ruleExpr"]["oneOf"]:
        if "rule" in variant.get("properties", {}):
            variant["properties"]["rule"]["enum"] = lrule_names

    base["$defs"]["depSelector"]["enum"] = (
        dep_names + ["!" + d for d in dep_names]
    )

    if names:
        level_names: list[str] = []
        location_names: list[str] = []

        for name in sorted(vars(names.LocationNames).keys()): # type: ignore
            if not isinstance(name, str):
                print(f"WARNING: Skipping non-str name: {name}")
                continue
            if name.startswith("loc_level_"):
                location_names.append(name)
            elif name.startswith("level_"):
                level_names.append(name)

        base["properties"]["levels"]["propertyNames"]["enum"] = level_names
        base["$defs"]["level"]["properties"]["locations"]["propertyNames"]["enum"] = location_names

    if not os.path.isdir("schemas"):
        os.mkdir("schemas", mode=0o755)

    json.dump(
        base,
        open(DEST_DIR, "w"),
        indent=2
    )

if __name__ == "__main__":
    main()
