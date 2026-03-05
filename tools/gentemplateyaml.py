#!/usr/bin/env python3

### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

"""
gentemplateyaml.py - generate the Player.yaml file.
"""

import argparse
import ast
from pathlib import Path
import textwrap
import typing
from collections.abc import Iterable

# --- CONFIG ---
INCLUDE_VISIBILITIES: set[str] = set()
VISIBILITY_SKIP_KEYWORDS: set[str] = {"spoiler", "template", "none", "complex_ui"}
EXCLUDE_OPTION_TYPE: set[str] = {"Version"}
DEFAULT_OUTPUT_FILE: str = "Player.yaml"
DEFAULT_HEADER: str = "Template YAML generated with gentemplateyaml"


def parse_valid_option_classes(init_path: str, dataclass_name: str = "GameOptions") -> list[str]:
    """
    Parse the __init__.py file and return the set of option class names
    """
    with open(init_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=init_path)
    res: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == dataclass_name:
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                    annotation = stmt.annotation
                    # odefs.Version
                    if isinstance(annotation, ast.Attribute):
                        res.append(annotation.attr)
                    # Version (unlikely but safe)
                    elif isinstance(annotation, ast.Name):
                        res.append(annotation.id)
    return res

def parse_optiondefs(path: str) -> list[ast.ClassDef]:
    """Parse optiondefs.py into a list of class definitions."""
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)
    return [node for node in tree.body if isinstance(node, ast.ClassDef)]

def format_apworld_version(sem_ver: tuple[int, int, int, int]) -> str:
    """Format APWORLD_SEM_VERSION into the APWORLD_VERSION display string."""
    if sem_ver[0] == 0:
        branch = {
            1: "preview",
            2: "alpha",
            3: "beta",
            4: "rc",
        }.get(sem_ver[1], "unknown")
    else:
        branch = "v"

    baseline = sem_ver[2] + 1
    revision = sem_ver[3]
    if revision < 0:
        raise ValueError("revision must be non-negative")

    res: list[str] = []
    while revision >= 0:
        revision, rem = divmod(revision, 26)
        res.append(chr(rem + ord("a")))
        revision -= 1

    revision_letter = "".join(res)
    return f"{branch}{baseline:02d}{revision_letter}"

def parse_apworld_version(world_init_path: str, world_class_name: str = "CupheadWorld") -> str | None:
    """Read APWORLD_SEM_VERSION from world __init__.py and format it to APWORLD_VERSION."""
    with open(world_init_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=world_init_path)

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == world_class_name:
            for stmt in node.body:
                if not isinstance(stmt, ast.AnnAssign):
                    continue
                if not isinstance(stmt.target, ast.Name) or stmt.target.id != "APWORLD_SEM_VERSION":
                    continue
                if not isinstance(stmt.value, ast.Tuple) or len(stmt.value.elts) != 4:
                    return None
                values: list[int] = []
                for elt in stmt.value.elts:
                    if isinstance(elt, ast.Constant) and isinstance(elt.value, int):
                        values.append(elt.value)
                    else:
                        return None
                return format_apworld_version(tuple(values))  # pyright: ignore[reportArgumentType]
    return None


def get_docstring(node: ast.ClassDef) -> str:
    """Return the class docstring."""
    return ast.get_docstring(node) or ""


def get_class_attrs(node: ast.ClassDef) -> dict[str, typing.Any]:
    """Extract top-level assignments from the class body."""
    attrs: dict[str, typing.Any] = {}
    for stmt in node.body:
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            target = stmt.targets[0]
            if isinstance(target, ast.Name):
                name = target.id
                value_node = stmt.value
                value = None
                if isinstance(value_node, ast.Constant):
                    value = value_node.value
                elif isinstance(value_node, ast.Name):
                    value = value_node.id
                elif isinstance(value_node, ast.BinOp):
                    # For things like Visibility.spoiler | Visibility.template
                    value = ast.unparse(value_node)
                elif isinstance(value_node, ast.Attribute):
                    value = ast.unparse(value_node)
                attrs[name] = value
    return attrs

def get_option_fields(node: ast.ClassDef) -> dict[str, int]:
    """Find all options: class-level constants named option_* and return their keys."""
    opt_val_to_name: dict[str, int] = {}
    for stmt in node.body:
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            target = stmt.targets[0]
            if isinstance(target, ast.Name) and target.id.startswith("option_"):
                opt_name = target.id[len("option_"):]
                val_node = stmt.value
                if isinstance(val_node, ast.Constant) and isinstance(val_node.value, int):
                    opt_val_to_name[opt_name] = val_node.value
    return dict(sorted(opt_val_to_name.items(), key=lambda item: item[1]))

def get_option_range(
        attrs: dict[str, typing.Any],
        base_names: list[str]
    ) -> tuple[int, int, int, int] | tuple[int, int] | None:
    """Get the range of the range-type option"""
    # LaxRange provides defaults that some concrete options inherit without overriding.
    if "LaxRange" in base_names:
        hard_min = attrs.get("hard_min", 0)
        hard_max = attrs.get("hard_max", 100)
        rec_min = attrs.get("range_start", 0)
        rec_max = attrs.get("range_end", 10)
        return (hard_min, hard_max, rec_min, rec_max)

    range_start = attrs.get("range_start", None)
    range_end = attrs.get("range_end", None)
    if range_start is not None and range_end is not None:
        return (range_start, range_end)
    return None

def get_doc_lines(option_dname: str, doc: str) -> list[str]:
    doc_lines: list[str] = []
    if option_dname:
        doc_lines.extend([f"## {option_dname}", "#"])
    doc_lines.extend([f"# {line}".rstrip() for line in doc.strip().splitlines()])
    return doc_lines

def generate_comments(  # noqa: C901
        node: ast.ClassDef,
        attrs: dict[str, typing.Any],
        base_names: list[str],
        option_names: Iterable[str],
        default: typing.Any
    ) -> list[str]:
    lines: list[str] = []

    doc = get_docstring(node)
    ranges = get_option_range(attrs, base_names)

    option_dname = attrs.get("display_name", "")

    if doc and isinstance(option_dname, str):
        lines.extend(get_doc_lines(option_dname, doc))

    if "BDefaultOnToggle" in base_names or "DefaultOnToggle" in base_names:
        _option_names: list[str] = ["true", "false"]  # pyright: ignore[reportRedeclaration]
        _default = "true" if default else "false"
    elif "BToggle" in base_names or "Toggle" in base_names:
        _option_names: list[str] = ["false", "true"]  # pyright: ignore[reportRedeclaration]
        _default = "true" if default else "false"
    else:
        _option_names: list[str] = list(option_names) if option_names else []
        _default = default

    _spaced = False
    if _option_names:
        if lines:
            lines.append("#")
            _spaced = True
        lines.append(f"# Values: {', '.join(_option_names)}")
    if ranges:
        if lines and not _spaced:
            lines.append("#")
            _spaced = True
        lines.append(f"# Range: {ranges[0]}-{ranges[1]}")
        if len(ranges) > 3:
            lines.append(f"# Recommended Range: {ranges[2]}-{ranges[3]}")
    if _default is not None:
        if lines and not _spaced:
            lines.append("#")
            _spaced = True
        lines.append(f"# Default: {_default}")

    return lines

def get_default_option(attrs: dict[str, typing.Any], base_names: list[str], options: dict[str, int]) -> typing.Any:
    default = attrs.get("default", None)
    if default is None:
        if "BDefaultOnToggle" in base_names or "DefaultOnToggle" in base_names:
            return True
        if "BToggle" in base_names or "Toggle" in base_names:
            return False
        if "NumericOption" in base_names or "Range" in base_names:
            default = 0
        else:
            return ""
    if "Choice" in base_names or "ChoiceEx" in base_names:
        if isinstance(default, int):
            return str(next((k for k, v in options.items() if v == default), default))
    return default

def should_skip_visibility(visibility_value: str):
    """Return True if visibility attribute includes disallowed flags."""
    if not visibility_value:
        return False
    vis_str = str(visibility_value).lower()
    return any(flag in vis_str for flag in VISIBILITY_SKIP_KEYWORDS)


def generate_yaml_data(classes: Iterable[ast.ClassDef], allowed_classes: list[str]) -> dict[str, typing.Any]:
    """Build structured data for YAML output."""
    yaml_data: dict[str, typing.Any] = {
        "name": "Player",
        "game": "Cuphead",
        "Cuphead": {},
    }

    by_name: dict[str, ast.ClassDef] = {node.name: node for node in classes}

    for cls_name in allowed_classes:
        node = by_name.get(cls_name)
        # Only include option classes explicitly listed in CupheadOptions and defined in options.py
        if node is None:
            continue

        attrs = get_class_attrs(node)
        name = attrs.get("name", node.name)
        if name in EXCLUDE_OPTION_TYPE:
            continue

        visibility = attrs.get("visibility", "")
        if should_skip_visibility(visibility):
            continue

        base_names = [base.id for base in node.bases if isinstance(base, ast.Name)]
        options = get_option_fields(node)
        default = get_default_option(attrs, base_names, options)

        # --- Format comments ---
        lines: list[str] = generate_comments(node, attrs, base_names, options.keys(), default)

        # Append formatted comments before the entry
        if lines:
            comment_block = textwrap.indent("\n".join(lines), "  ")
            yaml_data["Cuphead"][f"__comment_{name}"] = comment_block

        yaml_data["Cuphead"][name] = default

    return yaml_data

def get_value_string(value: typing.Any) -> str:
    if isinstance(value, str):
        return value if value else "''"
    if isinstance(value, bool):
        return "'true'" if value else "'false'"
    return f"'{value!s}'"

def main():
    parser = argparse.ArgumentParser(description="generate the Player.yaml file")
    parser.add_argument("world_init", help="Path to world __init__ py")
    parser.add_argument("-O", "--options", default="", help="Path to the options __init__ py")
    parser.add_argument("-D", "--odefs", help="Path to the options definitions py")
    parser.add_argument("-o", "--output", default="", help="Output file")
    parser.add_argument("-c", "--comment", default=DEFAULT_HEADER, help="Add comment to header")

    args = parser.parse_args()

    world_root = Path(args.world_init).resolve().parent
    odefs = args.odefs or str(world_root / "world" / "options" / "options.py")
    options_init_path = args.options or str(world_root / "world" / "options" / "__init__.py")

    valid_option_classes = parse_valid_option_classes(options_init_path, "CupheadOptions")
    classes = parse_optiondefs(odefs)
    yaml_dict = generate_yaml_data(classes, valid_option_classes)
    apworld_version = parse_apworld_version(args.world_init)

    header = args.comment if args.comment else DEFAULT_HEADER

    # --- Generate formatted YAML ---
    lines: list[str] = [f"# {header}"] if header else []
    if apworld_version:
        lines.append(f"# {apworld_version}")
    if lines:
        lines.append("")
    lines.extend([
        f"name: {yaml_dict['name']}",
        f"game: {yaml_dict['game']}",
        "Cuphead:",
        "  progression_balancing: '50'",
        "  accessibility: items",
        "  start_inventory: {}",
        "",
    ])

    for key, val in yaml_dict["Cuphead"].items():
        if key.startswith("__comment_"):
            lines.append(val)
        else:
            lines.append(f"  {key}: {get_value_string(val)}")
            lines.append("")

    # Trim end
    if not lines[-1]:
        lines.pop()

    if args.output:
        with open(args.output, "w") as f:
            [f.write(line + "\n") for line in lines]
    else:
        [print(line) for line in lines]

if __name__ == "__main__":
    main()
