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

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


def validate_date(value: str) -> bool:
    """Validate YYYY-MM-DD format."""
    if not isinstance(value, str):
        return False
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", value))


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
        if not validate_date(data["last-update"]):
            messages.append(f"ERROR: last-update must be YYYY-MM-DD format, got: {data['last-update']}")
            is_valid = False

    # Validate repo-url format
    if "repo-url" in data:
        if not validate_url(data["repo-url"]):
            messages.append(f"ERROR: repo-url must be a valid URL, got: {data['repo-url']}")
            is_valid = False

    # Validate last-commit format (if present)
    if "last-commit" in data and data["last-commit"]:
        if not validate_date(str(data["last-commit"])):
            messages.append(f"WARN: last-commit should be YYYY-MM-DD format")
            if strict:
                is_valid = False

    # Validate stars is numeric (if present)
    if "stars" in data and data["stars"] is not None:
        if not isinstance(data["stars"], int):
            messages.append(f"ERROR: stars must be an integer, got: {type(data['stars']).__name__}")
            is_valid = False

    # Validate boolean fields
    bool_fields = ["reputable-source"]
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
