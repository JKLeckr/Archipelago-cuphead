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
LEVELRULES_RULES_MOD = ".levelrules"
LEVELRULES_RULES_MOD_PATH = f"{LEVELRULES_MOD_PATH}{LEVELRULES_RULES_MOD}"
NAMES_MOD = ".names"
NAMES_MOD_PATH = f"{WORLD_MOD}{NAMES_MOD}"

DATA_PATH = os.path.join("world", "data")
PRESET_DEFS_PATH = os.path.join(DATA_PATH, "levelrulepresets.json")

WORLD_MOD_PATH = os.path.join(WORLD_MOD, "__init__.py")
BASE_SCHEMAS_DIR = os.path.join(THIS_DIR, "schemas")
BASE_RULES_SCHEMA_PATH = os.path.join(BASE_SCHEMAS_DIR, "levelrules.schema.json")
BASE_PRESETS_SCHEMA_PATH = os.path.join(BASE_SCHEMAS_DIR, "levelrulepresets.schema.json")

GEN_RULES_SCHEMA_NAME = "levelrules.generated.schema.json"
GEN_RULES_SCHEMA_DEST = os.path.join("schemas", GEN_RULES_SCHEMA_NAME)
GEN_PRESETS_SCHEMA_NAME = "levelrulepresets.generated.schema.json"
GEN_PRESETS_SCHEMA_DEST = os.path.join("schemas", GEN_PRESETS_SCHEMA_NAME)


def main():  # noqa: C901
    _fate_desc = (f"that files will be read from '{ROOT_DIR}'."
        " This directory must be the Archipelago root directory!"
        f" Files will be written to '{GEN_RULES_SCHEMA_DEST}'."
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

    _lrrspec = importlib.util.find_spec(LEVELRULES_RULES_MOD, package=LEVELRULES_MOD_PATH)
    _levelrulesrules = _lrrspec.loader.load_module(LEVELRULES_RULES_MOD_PATH) if _lrrspec and _lrrspec.loader else None

    if not _deps or not _levelrulesrules:
        raise ImportError("Could not import necessary modules.")

    deps = _deps
    levelrules = _levelrulesrules

    if args.include_lnames:
        _nspec = importlib.util.find_spec(NAMES_MOD, package=WORLD_MOD)
        _names = _nspec.loader.load_module(NAMES_MOD_PATH) if _nspec and _nspec.loader else None
        if not _names:
            raise ImportError("Could not import names module.")
        names = _names
    else:
        names = None

    base = json.load(open(BASE_RULES_SCHEMA_PATH))
    presets_base = json.load(open(BASE_PRESETS_SCHEMA_PATH))
    presets_data = json.load(open(PRESET_DEFS_PATH))

    lrule_names = sorted(levelrules.LRULES)
    dep_names = sorted(deps.DEPS)

    preset_names = sorted(presets_data["presets"].keys())

    # Patch enums
    for variant in base["$defs"]["ruleExpr"]["oneOf"]:
        if "rule" in variant.get("properties", {}):
            variant["properties"]["rule"]["enum"] = lrule_names
        if "preset" in variant.get("properties", {}):
            variant["properties"]["preset"]["enum"] = preset_names

    base["$defs"]["ruleDep"]["enum"] = (
        dep_names + ["!" + d for d in dep_names]
    )

    if names:
        level_names: list[str] = []
        location_names: list[str] = []

        for name in sorted(vars(names.LocationNames).keys()): # type: ignore
            if not isinstance(name, str):
                print(f"WARNING: Skipping non-str name: {name}")
                continue
            if name.startswith("loc_level_") or (name.startswith("loc_event_") and "goal" in name):
                location_names.append(name)
            elif name.startswith("level_"):
                level_names.append(name)

        base["properties"]["levels"]["propertyNames"]["enum"] = level_names
        base["$defs"]["level"]["properties"]["locations"]["propertyNames"]["enum"] = location_names

    presets_base["properties"]["$comment"]["$ref"] = f"{GEN_RULES_SCHEMA_NAME}#/$defs/comment"
    presets_base["$defs"]["preset"]["properties"]["$comment"]["$ref"] = (
        f"{GEN_RULES_SCHEMA_NAME}#/$defs/comment"
    )
    presets_base["$defs"]["preset"]["properties"]["rules"]["$ref"] = (
        f"{GEN_RULES_SCHEMA_NAME}#/$defs/ruleList"
    )

    if not os.path.isdir("schemas"):
        os.mkdir("schemas", mode=0o755)

    json.dump(
        base,
        open(GEN_RULES_SCHEMA_DEST, "w"),
        indent=2
    )
    json.dump(
        presets_base,
        open(GEN_PRESETS_SCHEMA_DEST, "w"),
        indent=2
    )

if __name__ == "__main__":
    main()
