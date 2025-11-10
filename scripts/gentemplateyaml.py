#!/usr/bin/env python3
"""
gentemplateyaml.py - generate the Player.yaml file.
"""

import argparse
import ast
import textwrap
import typing
from collections.abc import Iterable

# --- CONFIG ---
INCLUDE_VISIBILITIES: set[str] = set()
VISIBILITY_SKIP_KEYWORDS: set[str] = {"spoiler", "template", "none", "complex_ui"}
EXCLUDE_OPTION_TYPE: set[str] = {"Version"}
DEFAULT_OUTPUT_FILE: str = "Player.yaml"
DEFAULT_HEADER: str = "Template YAML generated with gentemplateyaml"


def parse_optiondefs(path: str) -> list[ast.ClassDef]:
    """Parse optiondefs.py into a list of class definitions."""
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)
    return [node for node in tree.body if isinstance(node, ast.ClassDef)]


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
    """Find all class-level constants named option_* and return their keys."""
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

def get_option_range(attrs: dict[str, typing.Any]) -> tuple[int, int] | None:
    """Get the range of the range-type option"""
    if "weight_max" in attrs:
        return None
    range_start = attrs.get("range_start", None)
    range_end = attrs.get("range_end", None)
    if range_start is not None and range_end is not None:
        return (range_start, range_end)
    return None

def generate_comments(
        node: ast.ClassDef,
        attrs: dict[str, typing.Any],
        base_names: list[str],
        option_names: Iterable[str],
        default: typing.Any
    ) -> list[str]:
    lines: list[str] = []

    doc = get_docstring(node)
    ranges = get_option_range(attrs)

    if doc:
        doc_lines = [f"# {line}" for line in doc.strip().splitlines()]
        lines.extend(doc_lines)

    if "Toggle" in base_names:
        _option_names: list[str] = ["false", "true"]
    elif "DefaultOnToggle" in base_names:
        _option_names: list[str] = ["true", "false"]
    else:
        _option_names: list[str] = list(option_names) if option_names else []

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
    if default is not None:
        if lines and not _spaced:
            lines.append("#")
            _spaced = True
        lines.append(f"# Default: {default}")

    return lines

def get_default_option(attrs: dict[str, typing.Any], base_names: list[str], options: dict[str, int]) -> typing.Any:
    default = attrs.get("default", None)
    if default is None:
        if "DefaultOnToggle" in base_names:
            return True
        if "Toggle" in base_names:
            return False
        if "NumericOption" in base_names:
            default = 0
        else:
            return ""
    if "Choice" in base_names:
        if isinstance(default, int):
            return str(next((k for k, v in options.items() if v == default), default))
    return default

def should_skip_visibility(visibility_value: str):
    """Return True if visibility attribute includes disallowed flags."""
    if not visibility_value:
        return False
    vis_str = str(visibility_value).lower()
    return any(flag in vis_str for flag in VISIBILITY_SKIP_KEYWORDS)


def generate_yaml_data(classes: Iterable[ast.ClassDef]) -> dict[str, typing.Any]:
    """Build structured data for YAML output."""
    yaml_data: dict[str, typing.Any] = {
        "name": "Player",
        "game": "Cuphead",
        "Cuphead": {},
    }

    for node in classes:
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
    parser.add_argument("file", help="Path to the optiondefs py")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT_FILE, help="Output file")
    parser.add_argument("-c", "--comment", default=DEFAULT_HEADER, help="Add comment to header")

    args = parser.parse_args()

    classes = parse_optiondefs(args.file)
    yaml_dict = generate_yaml_data(classes)

    header = args.comment if args.comment else DEFAULT_HEADER

    # --- Generate formatted YAML ---
    lines: list[str] = [f"# {header}", ""] if header else []
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

    if args.output:
        with open(args.output, "w") as f:
            [f.write(line + "\n") for line in lines]
    else:
        [print(line) for line in lines]

if __name__ == "__main__":
    main()

