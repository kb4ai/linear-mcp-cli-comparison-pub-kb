#!/usr/bin/env python3
"""
Validate YAML files in projects/ against the schema defined in spec.yaml.

Usage:
    ./scripts/check-yaml.py [OPTIONS] [FILES...]

Options:
    --strict    Fail on warnings (optional fields become required)
    --help      Show this help

If no files specified, validates all projects/*.yaml files.
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

# Valid categories from spec.yaml
VALID_CATEGORIES = [
    "linear-cli",
    "linear-mcp-server",
    "mcp-cli-auth",
    "proxy-bridge",
    "official",
    "uncategorized",
]


def validate_date(value: str) -> tuple[bool, str]:
    """Validate YYYY-MM-DD format and actual date validity."""
    if not isinstance(value, str):
        return False, "not a string"
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return False, "not YYYY-MM-DD format"
    # Actually parse to catch invalid dates like 2024-02-30
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True, ""
    except ValueError as e:
        return False, str(e)


def validate_url(value: str) -> bool:
    """Validate URL format."""
    if not isinstance(value, str):
        return False
    return value.startswith("http://") or value.startswith("https://")


def validate_yaml_file(filepath: Path, strict: bool = False) -> tuple[bool, list[str]]:
    """
    Validate a single YAML file.

    Returns: (is_valid, list_of_messages)
    """
    messages = []
    is_valid = True

    try:
        with open(filepath) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return False, [f"YAML parse error: {e}"]
    except Exception as e:
        return False, [f"File read error: {e}"]

    if data is None:
        return False, ["File is empty"]

    if not isinstance(data, dict):
        return False, ["Root must be a mapping/dictionary"]

    # Required fields
    required = ["last-update", "repo-url"]
    for field in required:
        if field not in data:
            messages.append(f"ERROR: Missing required field: {field}")
            is_valid = False

    # Validate last-update format
    if "last-update" in data:
        valid, err = validate_date(data["last-update"])
        if not valid:
            messages.append(f"ERROR: last-update invalid: {err}, got: {data['last-update']}")
            is_valid = False

    # Validate repo-url format
    if "repo-url" in data:
        if not validate_url(data["repo-url"]):
            messages.append(f"ERROR: repo-url must be a valid URL, got: {data['repo-url']}")
            is_valid = False

    # Validate last-commit format (if present)
    if "last-commit" in data and data["last-commit"]:
        valid, err = validate_date(str(data["last-commit"]))
        if not valid:
            messages.append(f"WARN: last-commit invalid: {err}")
            if strict:
                is_valid = False

    # Validate category enum (if present)
    if "category" in data and data["category"]:
        if data["category"] not in VALID_CATEGORIES:
            messages.append(f"WARN: unknown category '{data['category']}', valid: {VALID_CATEGORIES}")
            if strict:
                is_valid = False

    # Validate numeric fields
    numeric_fields = ["stars", "forks", "watchers", "contributors"]
    for field in numeric_fields:
        if field in data and data[field] is not None:
            if not isinstance(data[field], int):
                messages.append(f"ERROR: {field} must be an integer, got: {type(data[field]).__name__}")
                is_valid = False

    # Validate boolean fields
    bool_fields = ["reputable-source", "tested-with-linear", "agent-optimized", "mcptools-compatible"]
    for field in bool_fields:
        if field in data and data[field] is not None:
            if not isinstance(data[field], bool):
                messages.append(f"WARN: {field} should be boolean")
                if strict:
                    is_valid = False

    # Validate nested structures
    if "transports" in data and data["transports"]:
        if not isinstance(data["transports"], dict):
            messages.append(f"ERROR: transports must be a mapping")
            is_valid = False
        else:
            # Validate each transport is boolean
            for key, val in data["transports"].items():
                if val is not None and not isinstance(val, bool):
                    messages.append(f"WARN: transports.{key} should be boolean")
                    if strict:
                        is_valid = False

    if "auth" in data and data["auth"]:
        if not isinstance(data["auth"], dict):
            messages.append(f"ERROR: auth must be a mapping")
            is_valid = False

    if "features" in data and data["features"]:
        if not isinstance(data["features"], list):
            messages.append(f"ERROR: features must be a list")
            is_valid = False

    if "security" in data and data["security"]:
        if not isinstance(data["security"], dict):
            messages.append(f"ERROR: security must be a mapping")
            is_valid = False

    return is_valid, messages


def main():
    args = sys.argv[1:]
    strict = "--strict" in args
    args = [a for a in args if not a.startswith("--")]

    if "--help" in sys.argv:
        print(__doc__)
        sys.exit(0)

    # Find project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    projects_dir = project_root / "projects"

    # Determine files to validate
    if args:
        files = [Path(f) for f in args]
    else:
        files = sorted(projects_dir.glob("*.yaml"))

    if not files:
        print("No YAML files to validate")
        sys.exit(0)

    # Validate each file
    total = 0
    valid = 0
    invalid = 0

    for filepath in files:
        if not filepath.exists():
            print(f"SKIP: {filepath} (not found)")
            continue

        total += 1
        is_valid, messages = validate_yaml_file(filepath, strict)

        if is_valid:
            valid += 1
            status = "OK"
        else:
            invalid += 1
            status = "FAIL"

        # Print results
        rel_path = filepath.name if filepath.parent.name == "projects" else filepath
        print(f"[{status}] {rel_path}")

        for msg in messages:
            print(f"      {msg}")

    # Summary
    print()
    print(f"Validated {total} files: {valid} valid, {invalid} invalid")

    if invalid > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
