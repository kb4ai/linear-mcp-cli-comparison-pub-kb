#!/usr/bin/env python3
"""
Validate project YAML files against the spec.

Usage:
    ./scripts/check-yaml.py                    # Check all projects
    ./scripts/check-yaml.py projects/foo.yaml  # Check specific file
    ./scripts/check-yaml.py --strict           # Treat warnings as errors
"""

import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# Required fields
REQUIRED_FIELDS = ['last-update', 'repo-url', 'name', 'description', 'language', 'category']

# Valid categories
VALID_CATEGORIES = [
    'cli-client',
    'tui-client',
    'ai-agent-tool',
    'importer-exporter',
    'git-workflow',
    'cross-team',
]

# Valid languages
VALID_LANGUAGES = [
    'TypeScript', 'JavaScript', 'Python', 'Rust', 'Go', 'Ruby', 'Deno',
]

# Date pattern
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')

# URL pattern
URL_PATTERN = re.compile(r'^https?://')


def validate_file(filepath: Path, strict: bool = False) -> tuple[list[str], list[str]]:
    """Validate a single YAML file. Returns (errors, warnings)."""
    errors = []
    warnings = []

    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"], []
    except Exception as e:
        return [f"File read error: {e}"], []

    if not data:
        return ["Empty or null YAML content"], []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif data[field] is None:
            errors.append(f"Required field is null: {field}")

    # Validate date format
    if 'last-update' in data and data['last-update']:
        if not DATE_PATTERN.match(str(data['last-update'])):
            errors.append(f"Invalid date format for last-update: {data['last-update']} (expected YYYY-MM-DD)")

    if 'last-commit' in data and data['last-commit']:
        if not DATE_PATTERN.match(str(data['last-commit'])):
            errors.append(f"Invalid date format for last-commit: {data['last-commit']} (expected YYYY-MM-DD)")

    # Validate URL format
    if 'repo-url' in data and data['repo-url']:
        if not URL_PATTERN.match(str(data['repo-url'])):
            errors.append(f"Invalid URL format for repo-url: {data['repo-url']}")

    # Validate category
    if 'category' in data and data['category']:
        if data['category'] not in VALID_CATEGORIES:
            warnings.append(f"Unknown category: {data['category']} (valid: {', '.join(VALID_CATEGORIES)})")

    # Validate language
    if 'language' in data and data['language']:
        if data['language'] not in VALID_LANGUAGES:
            warnings.append(f"Unknown language: {data['language']} (valid: {', '.join(VALID_LANGUAGES)})")

    # Validate stars is a number
    if 'stars' in data and data['stars'] is not None:
        if not isinstance(data['stars'], int):
            errors.append(f"stars should be an integer, got: {type(data['stars']).__name__}")

    # Validate features is a dict
    if 'features' in data and data['features'] is not None:
        if not isinstance(data['features'], dict):
            errors.append(f"features should be a dictionary, got: {type(data['features']).__name__}")

    # Validate installation is a dict
    if 'installation' in data and data['installation'] is not None:
        if not isinstance(data['installation'], dict):
            errors.append(f"installation should be a dictionary, got: {type(data['installation']).__name__}")

    return errors, warnings


def main():
    strict = '--strict' in sys.argv
    args = [a for a in sys.argv[1:] if a != '--strict']

    # Find projects directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    projects_dir = repo_root / 'projects'

    # Determine which files to check
    if args:
        files = [Path(a) for a in args]
    else:
        if not projects_dir.exists():
            print(f"Error: Projects directory not found: {projects_dir}", file=sys.stderr)
            sys.exit(1)
        files = sorted(projects_dir.glob("*.yaml"))

    if not files:
        print("No YAML files to check")
        sys.exit(0)

    total_errors = 0
    total_warnings = 0

    for filepath in files:
        if not filepath.exists():
            print(f"❌ {filepath}: File not found")
            total_errors += 1
            continue

        errors, warnings = validate_file(filepath, strict)

        if errors or warnings:
            status = '❌' if errors else '⚠️'
            print(f"{status} {filepath.name}")

            for error in errors:
                print(f"   ERROR: {error}")
            for warning in warnings:
                print(f"   WARNING: {warning}")

            total_errors += len(errors)
            total_warnings += len(warnings)
        else:
            print(f"✅ {filepath.name}")

    print()
    print(f"Checked {len(files)} files: {total_errors} errors, {total_warnings} warnings")

    if total_errors > 0 or (strict and total_warnings > 0):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
