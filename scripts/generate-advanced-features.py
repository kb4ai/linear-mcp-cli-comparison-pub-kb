#!/usr/bin/env python3
"""
Generate advanced Linear features comparison table from project YAML files.

This script focuses on the features that matter most for workflows:
- Sub-issues (parent-child relationships)
- Estimates/Story Points
- Blocking/Blocked-by dependencies
- Due dates
- Related issues

Usage:
    ./scripts/generate-advanced-features.py > comparisons/advanced-features.md
"""

import os
import sys
from pathlib import Path
from datetime import date

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


def format_support(value, with_links: bool = False, feature: str = None) -> str:
    """Format feature support as emoji indicator."""
    if value is True:
        return '✅'
    elif value is False:
        return '❌'
    elif value == 'partial':
        return '⚠️'
    elif value == 'read-only':
        return '👁️'
    elif value == 'unknown':
        return '❓'
    elif value == 'workaround':
        if with_links:
            # Map features to their tracking issues
            issue_map = {
                'estimates': '#26',
                'blocking-blocked-by': '#27',
                'related-issues': '#27',
                'duplicate-marking': '#27',
                'due-dates': '#29',
            }
            issue = issue_map.get(feature, '')
            if issue:
                return f'[🔧](https://github.com/czottmann/linearis/issues/{issue[1:]})'
            return '🔧'
        return '🔧'
    elif isinstance(value, str):
        # Handle string values like "partial", "read-only", "workaround"
        if 'workaround' in value.lower():
            return '🔧'
        if 'partial' in value.lower():
            return '⚠️'
        if 'read' in value.lower():
            return '👁️'
        return value
    return '❓'


def get_advanced_feature(project: dict, feature: str):
    """Get advanced feature value from project."""
    features = project.get('features', {})
    # Handle both dict and list formats for features
    if isinstance(features, dict):
        return features.get(feature, None)
    elif isinstance(features, list):
        # For list-style features, we can't check specific feature flags
        return None
    return None


def generate_priority_features_table(projects: list[dict]) -> str:
    """Generate the HIGH PRIORITY features table (what the user wants most)."""
    lines = [
        "## High Priority Features",
        "",
        "These are the most requested features for agile/sprint workflows.",
        "",
        "| Tool | Language | Sub-Issues | Estimates | Blocking |",
        "|------|----------|------------|-----------|----------|",
    ]

    sorted_projects = sorted(projects, key=lambda p: p.get('name', '').lower())

    for p in sorted_projects:
        name = p.get('name', 'Unknown')
        repo_url = p.get('repo-url', '')
        language = p.get('language', 'Unknown')

        sub_issues = format_support(get_advanced_feature(p, 'sub-issues'))
        estimates = format_support(get_advanced_feature(p, 'estimates'))
        blocking = format_support(get_advanced_feature(p, 'blocking-blocked-by'))

        if repo_url:
            name_link = f"[{name}]({repo_url})"
        else:
            name_link = name

        lines.append(f"| {name_link} | {language} | {sub_issues} | {estimates} | {blocking} |")

    return '\n'.join(lines)


def generate_full_advanced_table(projects: list[dict]) -> str:
    """Generate comprehensive advanced features table."""
    lines = [
        "## Complete Advanced Features Matrix",
        "",
        "| Tool | Sub-Issues | Estimates | Blocking | Due Dates | Related | Labels | Status | Priority |",
        "|------|------------|-----------|----------|-----------|---------|--------|--------|----------|",
    ]

    sorted_projects = sorted(projects, key=lambda p: p.get('name', '').lower())

    for p in sorted_projects:
        name = p.get('name', 'Unknown')

        sub_issues = format_support(get_advanced_feature(p, 'sub-issues'))
        estimates = format_support(get_advanced_feature(p, 'estimates'))
        blocking = format_support(get_advanced_feature(p, 'blocking-blocked-by'))
        due_dates = format_support(get_advanced_feature(p, 'due-dates'))
        related = format_support(get_advanced_feature(p, 'related-issues'))
        labels = format_support(get_advanced_feature(p, 'labels'))
        status = format_support(get_advanced_feature(p, 'status'))
        priority = format_support(get_advanced_feature(p, 'priority'))

        lines.append(
            f"| {name} | {sub_issues} | {estimates} | {blocking} | "
            f"{due_dates} | {related} | {labels} | {status} | {priority} |"
        )

    return '\n'.join(lines)


def generate_best_for_workflow(projects: list[dict]) -> str:
    """Generate recommendations based on feature needs."""
    lines = [
        "## Best Tools for Specific Workflows",
        "",
    ]

    # Score projects for different workflows
    agile_scores = []
    dependency_scores = []
    comprehensive_scores = []

    for p in projects:
        name = p.get('name', 'Unknown')
        repo_url = p.get('repo-url', '')
        features = p.get('features', {})

        def safe_get_feature(feat_dict, key):
            """Safely get feature from dict or return None for lists."""
            if isinstance(feat_dict, dict):
                return feat_dict.get(key)
            return None

        def score_feature(val):
            if val is True:
                return 2
            elif val in ['partial', 'read-only']:
                return 1
            elif isinstance(val, str) and ('partial' in val.lower() or 'read' in val.lower()):
                return 1
            return 0

        # Agile workflow: estimates + sub-issues + cycles
        agile = (
            score_feature(safe_get_feature(features, 'estimates')) * 3 +  # Weighted heavily
            score_feature(safe_get_feature(features, 'sub-issues')) * 2 +
            score_feature(safe_get_feature(features, 'cycles'))
        )
        agile_scores.append((agile, name, repo_url))

        # Dependency tracking: blocking + related + sub-issues
        deps = (
            score_feature(safe_get_feature(features, 'blocking-blocked-by')) * 3 +
            score_feature(safe_get_feature(features, 'related-issues')) * 2 +
            score_feature(safe_get_feature(features, 'sub-issues'))
        )
        dependency_scores.append((deps, name, repo_url))

        # Comprehensive: all advanced features
        comp = (
            score_feature(safe_get_feature(features, 'sub-issues')) +
            score_feature(safe_get_feature(features, 'estimates')) +
            score_feature(safe_get_feature(features, 'blocking-blocked-by')) +
            score_feature(safe_get_feature(features, 'due-dates')) +
            score_feature(safe_get_feature(features, 'related-issues'))
        )
        comprehensive_scores.append((comp, name, repo_url))

    # Agile/Sprint Planning
    lines.append("### Agile/Sprint Planning (Estimates + Sub-issues)")
    lines.append("")
    lines.append("| Rank | Tool | Score |")
    lines.append("|------|------|-------|")
    for i, (score, name, url) in enumerate(sorted(agile_scores, reverse=True)[:5], 1):
        link = f"[{name}]({url})" if url else name
        lines.append(f"| {i} | {link} | {score} |")
    lines.append("")

    # Dependency Tracking
    lines.append("### Dependency Tracking (Blocking/Related)")
    lines.append("")
    lines.append("| Rank | Tool | Score |")
    lines.append("|------|------|-------|")
    for i, (score, name, url) in enumerate(sorted(dependency_scores, reverse=True)[:5], 1):
        link = f"[{name}]({url})" if url else name
        lines.append(f"| {i} | {link} | {score} |")
    lines.append("")

    # Most Comprehensive
    lines.append("### Most Comprehensive (All Advanced Features)")
    lines.append("")
    lines.append("| Rank | Tool | Score |")
    lines.append("|------|------|-------|")
    for i, (score, name, url) in enumerate(sorted(comprehensive_scores, reverse=True)[:5], 1):
        link = f"[{name}]({url})" if url else name
        lines.append(f"| {i} | {link} | {score} |")

    return '\n'.join(lines)


def generate_legend() -> str:
    """Generate legend for feature support indicators."""
    return """## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Full support (read and write) |
| ⚠️ | Partial support |
| 🔧 | Workaround available ([script](https://gist.github.com/g-click-trade/3d73f0492abd2e5c75baa863053867dc)) |
| 👁️ | Read-only (can view but not modify) |
| ❌ | Not supported |
| ❓ | Unknown / Not tested |
"""


def generate_key_findings() -> str:
    """Generate key findings section."""
    return """## Key Findings (2025-12-23)

### Blocking/Blocked-by Support

**No CLI tool natively supports blocking/blocked-by relationships!**

All tools would need to implement the `IssueRelation` GraphQL mutations:

* `issueRelationCreate(type: "blocks", issueId, relatedIssueId)`
* `issueRelationCreate(type: "blocked", issueId, relatedIssueId)`

**Workaround:** [Python GraphQL scripts](https://gist.github.com/g-click-trade/3d73f0492abd2e5c75baa863053867dc) for estimates, assignees, and blocking relations.

### Estimates Support

Only 2 tools support setting estimates:

* **linear-issue-importer** (Rust) - via `estimate` field in JSON/CSV
* **linearator** (Python) - partial support via API fields

**Workaround:** [Python scripts](https://gist.github.com/g-click-trade/3d73f0492abd2e5c75baa863053867dc) provide `get_issue_estimate()` and `set_issue_estimate()` functions.

### Sub-Issues Support

Best support for sub-issues (parent-child):

* **linearis** (TypeScript) - full CRUD support
* **linctl** (Go) - read/write via `--parent` flag
* **linearator** (Python) - GraphQL parent/children queries
* **linear-issue-importer** (Rust) - via `parentId` field
"""


def generate_recommendations() -> str:
    """Generate tool recommendations by use case."""
    return """## Tool Recommendations by Use Case

### For AI Agent Workflows
**Recommended: [linctl](https://github.com/dorkitude/linctl)** (Go)

* Purpose-built for AI agents (Claude Code, Cursor, Gemini)
* `--json` flag for structured output
* Authenticated image downloads (unique feature)
* Sub-issues + due dates support

### For Git-Integrated Workflows
**Recommended: [schpet/linear-cli](https://github.com/schpet/linear-cli)** (TypeScript/Deno)

* Auto-detects issue IDs from git branch names
* GitHub PR creation via `gh pr create`
* Branch management

### For LLM-Optimized Token Efficiency
**Recommended: [linearis](https://github.com/czottmann/linearis)** (TypeScript/Deno)

* Minimal token output (~0 tokens vs ~13k for MCP servers)
* JSON-first design for piping to `jq`
* [Workaround scripts](https://gist.github.com/g-click-trade/3d73f0492abd2e5c75baa863053867dc) for estimates/relations
* Feature requests tracked: [#26 estimates](https://github.com/czottmann/linearis/issues/26), [#27 blocking](https://github.com/czottmann/linearis/issues/27), [#29 due dates](https://github.com/czottmann/linearis/issues/29)
* See: [Token efficiency analysis](https://zottmann.org/2025/09/03/linearis-my-linear-cli-built.html)

### For Cross-Platform / Python Users
**Recommended: [linearator](https://github.com/AdiKsOnDev/linear-cli)** (Python)

* PyPI: `pip install linearator`
* AUR: `paru -S linear-cli`
* Windows support
* Note: GitHub repo is "linear-cli", PyPI package is "linearator"

### For Bulk Import/Export with Estimates
**Recommended: [linear-issue-importer](https://crates.io/crates/linear-issue-importer)** (Rust)

* Only tool with full estimate write support
* Sub-issues + due dates
* JSON/CSV batch operations

---

## Workaround Scripts for Missing Features

For **linearis** and other tools missing estimates/blocking support:

**Gist:** https://gist.github.com/g-click-trade/3d73f0492abd2e5c75baa863053867dc

```python
# Estimates
get_issue_estimate(identifier)      # Returns float or None
set_issue_estimate(identifier, 5.0) # Set to 5 points

# Blocking relations
add_issue_relation('TES-123', 'TES-456', 'blocks')
remove_issue_relation('TES-123', 'TES-456', 'blocks')
```

Requires: `LINEAR_API_KEY` environment variable
"""


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
        "# Linear CLI Tools - Advanced Features Comparison",
        "",
        f"*Generated on {date.today().isoformat()} from {len(projects)} project files*",
        "",
        "This comparison focuses on advanced Linear features important for agile workflows:",
        "",
        "* **Sub-issues** - Parent-child issue relationships",
        "* **Estimates** - Story points / complexity estimates",
        "* **Blocking/Blocked-by** - Issue dependency tracking",
        "* **Due dates** - Target completion dates",
        "* **Related issues** - Non-blocking issue links",
        "",
        "---",
        "",
        generate_legend(),
        "",
        "---",
        "",
        generate_priority_features_table(projects),
        "",
        "---",
        "",
        generate_full_advanced_table(projects),
        "",
        "---",
        "",
        generate_best_for_workflow(projects),
        "",
        "---",
        "",
        generate_key_findings(),
        "",
        generate_recommendations(),
    ]

    print('\n'.join(output))


if __name__ == '__main__':
    main()
