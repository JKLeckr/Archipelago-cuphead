#!/usr/bin/env python3

### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

import argparse
import importlib.util
import json
import os
import sys
from typing import Any

import jsonschema

THIS_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(THIS_DIR, "..", "..", ".."))

WORLD_MOD = "world"
RULES_MOD = ".rules"
RULES_MOD_PATH = f"{WORLD_MOD}{RULES_MOD}"
DEP_MOD = ".deps"
DEP_MOD_PATH = f"{RULES_MOD_PATH}{DEP_MOD}"
LEVELRULES_MOD = ".levelrules"
LEVELRULES_MOD_PATH = f"{RULES_MOD_PATH}{LEVELRULES_MOD}"
LEVELRULES_SELECTORS_MOD = ".levelruleselectors"
LEVELRULES_SELECTORS_MOD_PATH = f"{LEVELRULES_MOD_PATH}{LEVELRULES_SELECTORS_MOD}"

WORLD_MOD_PATH = os.path.join(WORLD_MOD, "__init__.py")


def validate_schema(data: Any, schema: Any):
    try:
        jsonschema.validate(data, schema) # type: ignore
    except jsonschema.ValidationError as e:
        print(f"JSON Schema validation error: {e.message}")
        print("Errors occured during schema validation.")
        sys.exit(2)

def walk_rule_expr(expr: Any, used_rules: set[str], used_presets: set[str]):
    if "rule" in expr:
        # TODO: Analyze has rules with items
        pass
    elif "preset" in expr:
        used_presets.add(expr["preset"])
    elif "and" in expr:
        for sub in expr["and"]:
            walk_rule_expr(sub, used_rules, used_presets)
    elif "or" in expr:
        for sub in expr["or"]:
            walk_rule_expr(sub, used_rules, used_presets)
    elif "not" in expr:
        walk_rule_expr(expr["not"], used_rules, used_presets)

def lint_rule_container(
        container: Any,
        known_presets: set[str],
        known_selectors: set[str],
        known_deps: set[str],
        context: str
    ):
    used_rules: set[str] = set()
    used_presets: set[str] = set()

    for frag in container.get("rules", []):
        for dep in frag.get("when", []):
            name = dep[1:] if dep.startswith("!") else dep
            if name not in known_deps:
                raise ValueError(f"{context}: unknown dep '{dep}'")

        walk_rule_expr(frag["requires"], used_rules, used_presets)

    for r in used_rules:
        if r not in known_selectors:
            raise ValueError(f"{context}: unknown rule '{r}'")

    for p in used_presets:
        if p not in known_presets:
            raise ValueError(f"{context}: unknown preset '{p}'")

def build_preset_graph(presets: Any) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {name: set() for name in presets}

    for name, container in presets.items():
        used_rules: set[str] = set()
        used_presets: set[str] = set()

        for frag in container.get("rules", []):
            walk_rule_expr(frag["requires"], used_rules, used_presets)

        graph[name] = used_presets

    return graph

def detect_cycles(graph: dict[str, set[str]]):
    visiting: set[str] = set()
    visited: set[str] = set()

    def _visit(node: str):
        if node in visiting:
            raise ValueError(f"Preset cycle detected at '{node}'")
        if node in visited:
            return

        visiting.add(node)
        for dep in graph[node]:
            _visit(dep)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        _visit(node)

def lint(data: Any, known_selectors: set[str], known_deps: set[str]):
    known_presets: set[Any] = set(data.get("presets", {}))

    # Presets
    for name, preset in data.get("presets", {}).items():
        lint_rule_container(
            preset,
            known_presets,
            known_selectors,
            known_deps,
            context=f"preset '{name}'"
        )

    # Preset cycles
    detect_cycles(build_preset_graph(data.get("presets", {})))

    # Levels
    for lname, level in data["levels"].items():
        if "access" in level:
            lint_rule_container(level["access"], known_selectors, known_presets, known_deps, f"level '{lname}' access")
        if "base" in level:
            lint_rule_container(level["base"], known_selectors, known_presets, known_deps, f"level '{lname}' base")

        for loc, locdef in level.get("locations", {}).items():
            if "rule" in locdef:
                lint_rule_container(
                    locdef["rule"],
                    known_selectors,
                    known_presets,
                    known_deps,
                    f"location '{loc}'"
                )

def fix_ref_str(schema: Any) -> None:
    prefix = "levelrules.generated.schema.json"
    pcomment = schema["properties"]["$comment"]
    ppresetscomment = schema["$defs"]["preset"]["properties"]["$comment"]
    ppresetsrules = schema["$defs"]["preset"]["properties"]["rules"]
    cref = str(pcomment["$ref"])
    pcref = str(ppresetscomment["$ref"])
    prref = str(ppresetsrules["$ref"])
    pcomment["$ref"] = cref.removeprefix(prefix)
    ppresetscomment["$ref"] = pcref.removeprefix(prefix)
    ppresetsrules["$ref"] = prref.removeprefix(prefix)

def main():
    _fate_desc = (f"that files will be read from '{ROOT_DIR}'."
        " This directory must be the Archipelago root directory!"
    )

    parser = argparse.ArgumentParser(description="Check levelrules json")
    parser.add_argument("file", help="File of the levelrules json to check")
    parser.add_argument("presets_file", help="File of the levelrulepresets json to check")
    parser.add_argument("schema", help="Rules Schema file to validate against")
    parser.add_argument("presets_schema", help="Presets Schema file to validate against")
    parser.add_argument(
        "--yes",
        help=f"Accept {_fate_desc}",
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

    _lrsspec = importlib.util.find_spec(LEVELRULES_SELECTORS_MOD, package=LEVELRULES_MOD_PATH)
    _levelruleselectors = (
        _lrsspec.loader.load_module(LEVELRULES_SELECTORS_MOD_PATH) if _lrsspec and _lrsspec.loader else None
    )

    if not _deps or not _levelruleselectors:
        raise ImportError("Could not import necessary modules.")

    deps = _deps
    levelruleselectors = _levelruleselectors

    known_lrselectors: set[str] = set(levelruleselectors.LRSELECTORS)
    known_deps: set[str] = set(deps.DEPS)

    if not os.path.isfile(args.file):
        print(f"File '{args.file}' does not exist!")
        exit(1)

    if not os.path.isfile(args.presets_file):
        print(f"Schema file '{args.schema}' does not exist!")
        exit(1)

    if not os.path.isfile(args.schema):
        print(f"File '{args.file}' does not exist!")
        exit(1)

    if not os.path.isfile(args.presets_schema):
        print(f"Schema file '{args.schema}' does not exist!")
        exit(1)

    lrjson = json.load(open(args.file, "r", encoding="utf-8"))
    lrpjson = json.load(open(args.presets_file, "r", encoding="utf-8"))
    schema = json.load(open(args.schema, "r", encoding="utf-8"))
    pschema = json.load(open(args.presets_schema, "r", encoding="utf-8"))

    # Mash
    schema["properties"]["presets"] = pschema["properties"]["presets"]
    schema["$defs"]["preset"] = pschema["$defs"]["preset"]
    fix_ref_str(schema)

    lrjson["presets"] = lrpjson["presets"]

    validate_schema(lrjson, schema)

    lint(lrjson, known_lrselectors, known_deps) # TODO: Fix

if __name__ == "__main__":
    main()
