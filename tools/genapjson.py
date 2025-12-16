#!/usr/bin/env python3

### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

"""
genapjson.py - generate the archipelago.json file.
"""

import argparse
import ast
import importlib.util
import json
from collections import OrderedDict
from collections.abc import Generator
from os import path
from typing import Any

from typing_extensions import override

APWORLD_ROOT_FILE: str = "__init__.py"
APWORLD_FVER_MOD: str = "fver"
APWORLD_CLASS: str = "CupheadWorld"
OUTPUT_FILE: str = "archipelago.json"

APWORLD_FIELDS: dict[str, str] = {
    "GAME_NAME": "game",
    "required_server_version": "minimum_ap_version",
    "AUTHORS": "authors",
    "APWORLD_SEM_VERSION": "world_version",
}

FieldTypes = str | int | None
FieldTypeTuple = (str , int)

class InlineListEncoder(json.JSONEncoder):
    @override
    def iterencode(self, o: Any, _one_shot: bool=False):
        if self.indent is None or isinstance(self.indent, str): # type: ignore
            indent = self.indent
        else:
            indent = " " * self.indent

        def _iterencode(obj: Any, level: int) -> Generator[str]:
            if isinstance(obj, list):
                # Inline list regardless of nesting
                yield "["
                first = True
                for item in obj: # type: ignore
                    if not first:
                        yield ", "
                    first = False
                    yield json.dumps(item)
                yield "]"
            elif isinstance(obj, dict):
                yield "{"
                first = True
                for k, v in obj.items(): # type: ignore
                    if not first:
                        yield ","
                    first = False
                    yield f"\n{indent * (level + 1)}"
                    yield json.dumps(k) + ": "
                    yield from _iterencode(v, level + 1)
                yield f"\n{(indent * level)}}}"
            else:
                yield json.dumps(obj)

        return _iterencode(o, 0)

def _sem_version_to_tuple_version(version: tuple[int, int, int, int]) -> tuple[int, int, int]:
    _format = 1
    _pofx = 0
    if version[0] > 0:
        raise NotImplementedError("Version tuple parser not implemented for full versions!")
    return (
        version[0],
        version[1],
        (
            ((_format & 0xFF) << 24) |
            ((version[2] & 0xFF) << 16) |
            ((version[3] & 0xFF) << 8) |
            (_pofx & 0xFF)
        )
    )

def _get_class_def(tree: ast.Module, class_name: str) -> ast.ClassDef | None:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    return None

def _add_field_value(res_ref: dict[str, FieldTypes], key: str, value: FieldTypes) -> None:
    if isinstance(value, tuple) and all(isinstance(x, int) for x in value): # type: ignore
        if key == "APWORLD_SEM_VERSION" and len(value) == 4:
            res_ref["_apworld_sem_version"] = value
            _value = _sem_version_to_tuple_version(value) # type: ignore
        else:
            _value = value
        res_ref[key] = ".".join(map(str, _value))
    elif isinstance(value, list):
        res_ref[key] = value
    elif isinstance(value, FieldTypeTuple):
        res_ref[key] = value
    else:
        raise TypeError(f"Unsupported value type for '{key}': {type(value)}")

def get_apworld_fields(
        dirpath: str,
        class_name: str,
    ) -> dict[str, FieldTypes] | None:
    _class_file_path = path.join(dirpath, APWORLD_ROOT_FILE)
    with open(_class_file_path, "r") as f:
        tree: ast.Module = ast.parse(f.read(), filename=APWORLD_ROOT_FILE)

    class_def: ast.ClassDef | None = _get_class_def(tree, class_name)

    if class_def is None:
        raise ValueError(f"Class '{class_name}' not found in '{_class_file_path}'.")

    res: dict[str, FieldTypes] = {}

    for node in class_def.body:
        if isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name):
                key: str = target.id
                if key in APWORLD_FIELDS:
                    try:
                        value = ast.literal_eval(node.value) # type: ignore
                    except Exception as e:
                        raise ValueError(f"Failed to evaluate value for '{key}': {e}") from e

                    _add_field_value(res, key, value)

    return res

def main():
    parser = argparse.ArgumentParser(description="Generate archipelago.json from file")
    parser.add_argument("dir", help="Directory where the Python script containing the APWorld class is")
    parser.add_argument("-c", "--classname", default=APWORLD_CLASS, help="Name of the APWorld class")
    parser.add_argument("-o", "--output", default=None, help="Output file")
    parser.add_argument("-m", "--matchversion", default=None, help="Version parsed must match this version")

    args = parser.parse_args()

    filename = f"{APWORLD_FVER_MOD}.py"
    file_path = path.join(args.dir, filename)

    spec = importlib.util.spec_from_file_location(APWORLD_FVER_MOD, file_path)
    module = importlib.util.module_from_spec(spec) if spec else None

    if spec and module:
        spec.loader.exec_module(module) # type: ignore
    else:
        raise ImportError("Could not import the fver module.")

    _values = get_apworld_fields(args.dir, args.classname)
    if not _values:
        print("Failed.")
        exit(1)

    world_fver_field = "world_friendly_version"

    njson: OrderedDict[str, FieldTypes] = OrderedDict([
        ("version", 7),
        ("compatible_version", 7),
    ])
    for k, v in _values.items():
        if k.startswith("_"):
            continue

        #print(f"{APWORLD_FIELDS[k]}: {v}")
        field = APWORLD_FIELDS[k]
        njson[field] = v
        if field == "world_version":
            njson[world_fver_field] = str(module.FVersion.from_int_tuple(_values["_apworld_sem_version"]))

    if args.matchversion and njson[world_fver_field] != args.match_version:
        print(f"Version mismatch: {njson[world_fver_field]} != {args.match_version}")
        exit(2)

    res = json.dumps(njson, indent=2, cls=InlineListEncoder)

    print(res)

    if args.output:
        with open(args.output, "w") as f:
            f.write(res)
        print(f"Wrote {len(njson)} variables to {args.output}")

if __name__ == "__main__":
    main()
