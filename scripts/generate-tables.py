#!/usr/bin/env python3
"""
Generate comparison tables from projects/*.yaml files.

Usage:
    ./scripts/generate-tables.py [OPTIONS]

Options:
    --by-category       Group projects by category
    --by-transport      Show transport support matrix
    --by-stars          Sort by star count
    --reputable-only    Only show reputable sources
    --json              Output as JSON instead of markdown
    --help              Show this help

Output is written to stdout. Redirect to file:
    ./scripts/generate-tables.py > comparisons/auto-generated.md
"""

import sys
import os
import json
from pathlib import Path
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def load_projects(projects_dir: Path) -> list[dict]:
    """Load all project YAML files."""
    projects = []

    for yaml_file in sorted(projects_dir.glob("*.yaml")):
        try:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data and isinstance(data, dict):
                    data["_filename"] = yaml_file.name
                    projects.append(data)
        except Exception as e:
            print(f"WARN: Could not load {yaml_file}: {e}", file=sys.stderr)

    return projects


def format_stars(stars) -> str:
    """Format star count for display."""
    if stars is None:
        return "?"
    if isinstance(stars, int):
        return str(stars)
    return str(stars)


def generate_summary(projects: list[dict]) -> str:
    """Generate summary statistics."""
    lines = ["## Summary Statistics", ""]

    total = len(projects)
    reputable = sum(1 for p in projects if p.get("reputable-source"))

    # Calculate combined stars
    stars_data = [p.get("stars", 0) for p in projects if isinstance(p.get("stars"), int)]
    combined_stars = sum(stars_data)
    projects_with_stars = len(stars_data)

    lines.append(f"- **Total projects:** {total}")
    lines.append(f"- **Reputable sources:** {reputable}")
    if projects_with_stars > 0:
        lines.append(f"- **Combined stars:** {combined_stars:,} (from {projects_with_stars} projects with star data)")
    lines.append("")

    # By category
    categories = defaultdict(int)
    for p in projects:
        cat = p.get("category", "uncategorized")
        categories[cat] += 1

    if categories:
        lines.append("### By Category")
        lines.append("")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            lines.append(f"- {cat}: {count}")
        lines.append("")

    # By language
    languages = defaultdict(int)
    for p in projects:
        lang = p.get("language", "unknown")
        languages[lang] += 1

    if languages:
        lines.append("### By Language")
        lines.append("")
        for lang, count in sorted(languages.items(), key=lambda x: -x[1]):
            lines.append(f"- {lang}: {count}")
        lines.append("")

    return "\n".join(lines)


def generate_overview_table(projects: list[dict]) -> str:
    """Generate main overview table sorted by stars."""
    lines = ["## Overview: All Projects by Stars", ""]

    # Sort by stars (descending), None/unknown at end
    def star_sort_key(p):
        stars = p.get("stars")
        if isinstance(stars, int):
            return (0, -stars)
        return (1, 0)

    sorted_projects = sorted(projects, key=star_sort_key)

    lines.append("| Project | Stars | Language | Category | Description |")
    lines.append("|---------|------:|----------|----------|-------------|")

    for p in sorted_projects:
        name = p.get("name", "unknown")
        url = p.get("repo-url", "")
        stars = format_stars(p.get("stars"))
        lang = p.get("language", "")
        cat = p.get("category", "")
        desc = p.get("description", "")[:60]
        if len(p.get("description", "")) > 60:
            desc += "..."

        if url:
            name_cell = f"[{name}]({url})"
        else:
            name_cell = name

        lines.append(f"| {name_cell} | {stars} | {lang} | {cat} | {desc} |")

    lines.append("")
    return "\n".join(lines)


def generate_reputable_table(projects: list[dict]) -> str:
    """Generate table of reputable/official sources."""
    reputable = [p for p in projects if p.get("reputable-source")]

    if not reputable:
        return ""

    lines = ["## Reputable/Official Sources", ""]
    lines.append("| Project | Organization | Category | Description |")
    lines.append("|---------|--------------|----------|-------------|")

    for p in sorted(reputable, key=lambda x: x.get("organization", "")):
        name = p.get("name", "unknown")
        url = p.get("repo-url", "")
        org = p.get("organization", "")
        cat = p.get("category", "")
        desc = p.get("description", "")[:50]
        if len(p.get("description", "")) > 50:
            desc += "..."

        if url:
            name_cell = f"[{name}]({url})"
        else:
            name_cell = name

        lines.append(f"| {name_cell} | {org} | {cat} | {desc} |")

    lines.append("")
    return "\n".join(lines)


def generate_transport_matrix(projects: list[dict]) -> str:
    """Generate transport support matrix."""
    lines = ["## Transport Support Matrix", ""]

    # Define transports to check
    transports = ["stdio", "http", "sse", "websocket"]

    # Header
    header = "| Project | " + " | ".join(t.upper() for t in transports) + " |"
    separator = "|---------|" + "|".join(":---:" for _ in transports) + "|"

    lines.append(header)
    lines.append(separator)

    # Sort by stars
    def star_sort_key(p):
        stars = p.get("stars")
        if isinstance(stars, int):
            return (0, -stars)
        return (1, 0)

    for p in sorted(projects, key=star_sort_key):
        name = p.get("name", "unknown")
        url = p.get("repo-url", "")

        if url:
            name_cell = f"[{name}]({url})"
        else:
            name_cell = name

        # Get transport support
        transport_data = p.get("transports", {}) or {}
        cells = []
        for t in transports:
            if transport_data.get(t):
                cells.append("✓")
            else:
                cells.append("")

        lines.append(f"| {name_cell} | " + " | ".join(cells) + " |")

    lines.append("")
    return "\n".join(lines)


def generate_by_category(projects: list[dict]) -> str:
    """Generate tables grouped by category."""
    categories = defaultdict(list)
    for p in projects:
        cat = p.get("category", "uncategorized")
        categories[cat].append(p)

    lines = ["## Projects by Category", ""]

    for cat in sorted(categories.keys()):
        cat_projects = categories[cat]
        cat_title = cat.replace("-", " ").title()

        lines.append(f"### {cat_title}")
        lines.append("")
        lines.append("| Project | Stars | Language | Description |")
        lines.append("|---------|------:|----------|-------------|")

        # Sort by stars within category
        def star_sort_key(p):
            stars = p.get("stars")
            if isinstance(stars, int):
                return (0, -stars)
            return (1, 0)

        for p in sorted(cat_projects, key=star_sort_key):
            name = p.get("name", "unknown")
            url = p.get("repo-url", "")
            stars = format_stars(p.get("stars"))
            lang = p.get("language", "")
            desc = p.get("description", "")[:60]
            if len(p.get("description", "")) > 60:
                desc += "..."

            if url:
                name_cell = f"[{name}]({url})"
            else:
                name_cell = name

            lines.append(f"| {name_cell} | {stars} | {lang} | {desc} |")

        lines.append("")

    return "\n".join(lines)


def main():
    args = set(sys.argv[1:])

    if "--help" in args:
        print(__doc__)
        sys.exit(0)

    # Find project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    projects_dir = project_root / "projects"

    if not projects_dir.exists():
        print("ERROR: projects/ directory not found", file=sys.stderr)
        sys.exit(1)

    projects = load_projects(projects_dir)

    if not projects:
        print("No projects found in projects/", file=sys.stderr)
        sys.exit(0)

    # Filter if needed
    if "--reputable-only" in args:
        projects = [p for p in projects if p.get("reputable-source")]

    # Generate output
    if "--json" in args:
        # JSON output
        output = json.dumps(projects, indent=2, default=str)
    else:
        # Markdown output
        parts = []
        parts.append(generate_summary(projects))
        parts.append(generate_overview_table(projects))
        parts.append(generate_reputable_table(projects))

        if "--by-category" in args:
            parts.append(generate_by_category(projects))

        if "--by-transport" in args:
            parts.append(generate_transport_matrix(projects))

        output = "\n".join(parts)

    print(output)


if __name__ == "__main__":
    main()
