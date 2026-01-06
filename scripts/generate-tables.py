#!/usr/bin/env python3
"""
Generate markdown comparison tables from project YAML files.

Usage:
    ./scripts/generate-tables.py > comparisons/auto-generated.md
"""

import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def load_projects(projects_dir: Path) -> list[dict]:
    """Load all project YAML files."""
    projects = []
    for yaml_file in sorted(projects_dir.glob("*.yaml")):
        with open(yaml_file, 'r') as f:
            try:
                data = yaml.safe_load(f)
                if data:
                    data['_filename'] = yaml_file.name
                    projects.append(data)
            except yaml.YAMLError as e:
                print(f"Warning: Failed to parse {yaml_file}: {e}", file=sys.stderr)
    return projects


def get_stars(project: dict) -> int:
    """Get star count, defaulting to 0."""
    return project.get('stars', 0) or 0


def get_category(project: dict) -> str:
    """Get primary category."""
    return project.get('category', 'unknown')


def get_language(project: dict) -> str:
    """Get primary language."""
    return project.get('language', 'Unknown')


def format_install(project: dict) -> str:
    """Format installation method."""
    install = project.get('installation', {})
    if not install:
        return '-'

    # Handle list format
    if isinstance(install, list):
        return ', '.join(str(i) for i in install[:2]) if install else '-'

    methods = []
    if install.get('brew'):
        methods.append(f"`brew install {install['brew']}`")
    if install.get('npm'):
        methods.append(f"`npm i -g {install['npm']}`")
    if install.get('pip'):
        methods.append(f"`pip install {install['pip']}`")
    if install.get('cargo'):
        methods.append(f"`cargo install {install['cargo']}`")
    if install.get('go-install'):
        methods.append("`go install`")
    if install.get('deno'):
        methods.append("`deno install`")
    if install.get('aur'):
        methods.append(f"AUR: `{install['aur']}`")

    return ', '.join(methods) if methods else '-'


def format_features(project: dict) -> str:
    """Format key features as bullet points."""
    features = project.get('features', {})
    if not features:
        return '-'

    # Handle list format (some YAMLs use list of strings)
    if isinstance(features, list):
        return ', '.join(features[:3]) if features else '-'

    feature_list = []
    if features.get('git-integration'):
        feature_list.append('Git integration')
    if features.get('github-pr-creation'):
        feature_list.append('PR creation')
    if features.get('kanban-view'):
        feature_list.append('Kanban view')
    if features.get('ai-integration'):
        provider = features.get('ai-provider', '')
        feature_list.append(f'AI ({provider})' if provider else 'AI')
    if features.get('cross-team-queries'):
        feature_list.append('Cross-team')
    if features.get('bulk-operations'):
        feature_list.append('Bulk ops')
    if features.get('interactive-mode'):
        feature_list.append('Interactive')

    return ', '.join(feature_list) if feature_list else '-'


def generate_overview_table(projects: list[dict]) -> str:
    """Generate main overview table sorted by stars."""
    lines = [
        "## All Tools by Stars",
        "",
        "| Tool | Language | Category | Stars | Key Features | Install |",
        "|------|----------|----------|-------|--------------|---------|",
    ]

    sorted_projects = sorted(projects, key=get_stars, reverse=True)

    for p in sorted_projects:
        name = p.get('name', 'Unknown')
        repo_url = p.get('repo-url', '')
        language = get_language(p)
        category = get_category(p).replace('-', ' ').title()
        stars = get_stars(p) or '-'
        features = format_features(p)
        install = format_install(p)

        if repo_url:
            name_link = f"[{name}]({repo_url})"
        else:
            name_link = name

        lines.append(f"| {name_link} | {language} | {category} | {stars} | {features} | {install} |")

    return '\n'.join(lines)


def generate_by_category(projects: list[dict]) -> str:
    """Generate tables grouped by category."""
    categories = {}
    for p in projects:
        cat = get_category(p)
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)

    lines = ["## By Category", ""]

    for cat in sorted(categories.keys()):
        cat_title = cat.replace('-', ' ').title()
        lines.append(f"### {cat_title}")
        lines.append("")
        lines.append("| Tool | Language | Stars | Key Features |")
        lines.append("|------|----------|-------|--------------|")

        for p in sorted(categories[cat], key=get_stars, reverse=True):
            name = p.get('name', 'Unknown')
            repo_url = p.get('repo-url', '')
            language = get_language(p)
            stars = get_stars(p) or '-'
            features = format_features(p)

            if repo_url:
                name_link = f"[{name}]({repo_url})"
            else:
                name_link = name

            lines.append(f"| {name_link} | {language} | {stars} | {features} |")

        lines.append("")

    return '\n'.join(lines)


def generate_by_language(projects: list[dict]) -> str:
    """Generate tables grouped by language."""
    languages = {}
    for p in projects:
        lang = get_language(p)
        if lang not in languages:
            languages[lang] = []
        languages[lang].append(p)

    lines = ["## By Language", ""]

    for lang in sorted(languages.keys()):
        lines.append(f"### {lang}")
        lines.append("")
        lines.append("| Tool | Category | Stars | Install |")
        lines.append("|------|----------|-------|---------|")

        for p in sorted(languages[lang], key=get_stars, reverse=True):
            name = p.get('name', 'Unknown')
            repo_url = p.get('repo-url', '')
            category = get_category(p).replace('-', ' ').title()
            stars = get_stars(p) or '-'
            install = format_install(p)

            if repo_url:
                name_link = f"[{name}]({repo_url})"
            else:
                name_link = name

            lines.append(f"| {name_link} | {category} | {stars} | {install} |")

        lines.append("")

    return '\n'.join(lines)


def generate_feature_matrix(projects: list[dict]) -> str:
    """Generate feature comparison matrix."""
    lines = [
        "## Feature Matrix",
        "",
        "| Tool | Git | PR | Kanban | AI | Cross-team | Bulk | Interactive |",
        "|------|-----|-----|--------|-----|------------|------|-------------|",
    ]

    sorted_projects = sorted(projects, key=get_stars, reverse=True)

    for p in sorted_projects:
        name = p.get('name', 'Unknown')
        features = p.get('features', {})

        def check(key):
            if isinstance(features, list):
                return '✅' if key in features else '❌'
            return '✅' if features.get(key) else '❌'

        lines.append(
            f"| {name} | {check('git-integration')} | {check('github-pr-creation')} | "
            f"{check('kanban-view')} | {check('ai-integration')} | {check('cross-team-queries')} | "
            f"{check('bulk-operations')} | {check('interactive-mode')} |"
        )

    return '\n'.join(lines)


def generate_stats(projects: list[dict]) -> str:
    """Generate summary statistics."""
    total = len(projects)

    # Count by category
    categories = {}
    for p in projects:
        cat = get_category(p)
        categories[cat] = categories.get(cat, 0) + 1

    # Count by language
    languages = {}
    for p in projects:
        lang = get_language(p)
        languages[lang] = languages.get(lang, 0) + 1

    lines = [
        "## Statistics",
        "",
        f"**Total Tools:** {total}",
        "",
        "### By Category",
        "",
        "| Category | Count |",
        "|----------|-------|",
    ]

    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        cat_title = cat.replace('-', ' ').title()
        lines.append(f"| {cat_title} | {count} |")

    lines.extend([
        "",
        "### By Language",
        "",
        "| Language | Count |",
        "|----------|-------|",
    ])

    for lang, count in sorted(languages.items(), key=lambda x: -x[1]):
        lines.append(f"| {lang} | {count} |")

    return '\n'.join(lines)


def main():
    # Find projects directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    projects_dir = repo_root / 'projects'

    if not projects_dir.exists():
        print(f"Error: Projects directory not found: {projects_dir}", file=sys.stderr)
        sys.exit(1)

    projects = load_projects(projects_dir)

    if not projects:
        print("Error: No project YAML files found", file=sys.stderr)
        sys.exit(1)

    # Generate output
    output = [
        "# Linear CLI Tools - Auto-Generated Comparison",
        "",
        f"*Generated from {len(projects)} project files*",
        "",
        "---",
        "",
        generate_stats(projects),
        "",
        "---",
        "",
        generate_overview_table(projects),
        "",
        "---",
        "",
        generate_feature_matrix(projects),
        "",
        "---",
        "",
        generate_by_category(projects),
        "",
        "---",
        "",
        generate_by_language(projects),
    ]

    print('\n'.join(output))


if __name__ == '__main__':
    main()
