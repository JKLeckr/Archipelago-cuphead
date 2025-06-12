import ast
import json
import argparse
from collections import OrderedDict
#import os
#from pathlib import Path

APWORLD_ROOT_FILE: str = "__init__.py"
APWORLD_CLASS: str = "CupheadWorld"
OUTPUT_FILE: str = "archipelago.json"

APWORLD_FIELDS: dict[str, str] = {
    "GAME_NAME": "game",
    "required_server_version": "minimum_ap_version",
    "APWORLD_VERSION": "world_version",
}

FieldTypes = str | int | None
FieldTypeTuple = (str , int)

def _get_class_def(tree: ast.Module, class_name: str) -> ast.ClassDef | None:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node

def _add_field_value(res_ref: dict[str, FieldTypes], key: str, value: FieldTypes) -> None:
    # Convert version tuples to strings
    if isinstance(value, tuple) and all(isinstance(x, int) for x in value): # type: ignore
        res_ref[key] = '.'.join(map(str, value)) # type: ignore
    elif isinstance(value, FieldTypeTuple):
        res_ref[key] = value
    else:
        raise TypeError(f"Unsupported value type for \"{key}\": {type(value)}") # type: ignore

def get_apworld_fields(
        filepath: str,
        class_name: str,
        match_version: str | None = None
    ) -> dict[str, FieldTypes] | None:
    with open(filepath, "r") as f:
        tree: ast.Module = ast.parse(f.read(), filename=filepath)

    class_def: ast.ClassDef | None = _get_class_def(tree, class_name)

    if class_def is None:
        raise ValueError(f"Class '{class_name}' not found in '{filepath}'.")

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
                        raise ValueError(f"Failed to evaluate value for \"{key}\": {e}") from e

                    if match_version and key == "APWORLD_VERSION" and value != match_version:
                        print(f"Version mismatch: {value} != {match_version}")
                        return None

                    _add_field_value(res, key, value)

    return res

def main():
    parser = argparse.ArgumentParser(description="Generate archipelago.json from file")
    parser.add_argument("file", help="Path to the Python script containing the APWorld class")
    parser.add_argument("-c", "--classname", default=APWORLD_CLASS, help="Name of the APWorld class")
    parser.add_argument("-o", "--output", default=OUTPUT_FILE, help="Output file")
    parser.add_argument("-m", "--matchversion", default=None, help="Version parsed must match this version")

    args = parser.parse_args()

    _values = get_apworld_fields(args.file, args.classname, args.matchversion)
    if not _values:
        print("Failed.")
        exit(1)

    njson: OrderedDict[str, FieldTypes] = OrderedDict([
        ("version", 6),
        ("compatible_version", 5),
    ])
    for k, v in _values.items():
        njson[APWORLD_FIELDS[k]] = v

    with open(args.output, "w") as f:
        json.dump(njson, f, indent=2)

    print(f"Wrote {len(njson)} variables to {args.output}")

if __name__ == "__main__":
    main()
