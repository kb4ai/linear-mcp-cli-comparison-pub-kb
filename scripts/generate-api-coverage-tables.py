#!/usr/bin/env python3
"""
Generate Linear GraphQL API coverage comparison tables.

This script compares CLI/MCP tools against the Linear GraphQL API
to show which operations each tool supports.

Features:
- Resource grouping: Issues, Comments, Relations, etc.
- Read vs Write distinction
- Intelligent filtering: Only shows tools with coverage
- Category grouping: CLI tools vs MCP servers
- Percentage coverage display
- Gap analysis

Usage:
    python generate-api-coverage-tables.py
    python generate-api-coverage-tables.py --resource issues
    python generate-api-coverage-tables.py --overview-only

Outputs to: comparisons/api-coverage/
"""

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

try:
    import yaml
except ImportError:
    print("Error: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# CONSTANTS - Linear GraphQL Operations by Resource
# =============================================================================

# Maps YAML feature keys to supported operations
FEATURE_OPERATION_MAP = {
    # Basic issue operations
    "issue-creation": ["issueCreate"],
    "issue-update": ["issueUpdate"],
    "issue-view": ["issue"],
    "issue-search": ["issues", "issueSearch"],
    "bulk-operations": ["issueBatchCreate", "issueBatchUpdate"],

    # Issue field support (implies create/update with that field)
    "sub-issues": ["issueCreate:parentId"],
    "estimates": ["issueCreate:estimate"],
    "due-dates": ["issueCreate:dueDate"],
    "priority": ["issueCreate:priority", "issueUpdate:priority"],
    "status": ["issueCreate:stateId", "issueUpdate:stateId"],
    "assignee": ["issueCreate:assigneeId", "issueUpdate:assigneeId"],
    "cycles": ["issueCreate:cycleId", "issueUpdate:cycleId"],
    "projects": ["issueCreate:projectId", "issueUpdate:projectId"],

    # Issue relationships
    "blocking-blocked-by": ["issueRelationCreate:blocks"],
    "related-issues": ["issueRelationCreate:related"],
    "duplicate-marking": ["issueRelationCreate:duplicate"],

    # Labels
    "labels": ["issueAddLabel", "issueRemoveLabel"],
    "label-management": ["issueLabelCreate", "issueLabelUpdate"],

    # Comments
    "comments": ["commentCreate", "comments"],

    # Teams
    "team-management": ["team", "teams"],

    # Attachments
    "attachments": ["attachmentCreate"],
}

# Comparison group definitions
RESOURCE_GROUPS = {
    "issues": {
        "title": "Issue Operations",
        "description": "Core issue CRUD and batch operations",
        "operations": [
            ("issueCreate", "issue-creation"),
            ("issueUpdate", "issue-update"),
            ("issue", "issue-view"),
            ("issues", "issue-search"),
            ("issueSearch", "issue-search"),
            ("issueBatchCreate", "bulk-operations"),
            ("issueBatchUpdate", "bulk-operations"),
        ],
        "include-categories": [
            "cli-client", "tui-client", "ai-agent-tool",
            "git-workflow", "cross-team", "importer-exporter",
            "linear-mcp-server",
        ],
    },
    "issue-fields": {
        "title": "Issue Field Support",
        "description": "Which issue fields can be set via create/update",
        "operations": [
            ("parentId (sub-issues)", "sub-issues"),
            ("estimate", "estimates"),
            ("dueDate", "due-dates"),
            ("priority", "priority"),
            ("stateId (status)", "status"),
            ("assigneeId", "assignee"),
            ("cycleId", "cycles"),
            ("projectId", "projects"),
        ],
        "include-categories": [
            "cli-client", "tui-client", "ai-agent-tool",
            "git-workflow", "importer-exporter", "linear-mcp-server",
        ],
    },
    "relations": {
        "title": "Issue Relationship Operations",
        "description": "Blocking, duplicates, and related issue links",
        "operations": [
            ("blocks/blocked-by", "blocking-blocked-by"),
            ("related", "related-issues"),
            ("duplicate", "duplicate-marking"),
        ],
        "include-categories": [
            "cli-client", "ai-agent-tool", "linear-mcp-server",
        ],
        "highlight": True,
        "note": "**KEY GAP**: No CLI tool currently supports issue relations via the GraphQL API",
    },
    "comments": {
        "title": "Comment Operations",
        "description": "Creating and managing comments on issues",
        "operations": [
            ("commentCreate", "comments"),
            ("comments (read)", "comments"),
        ],
        "include-categories": [
            "cli-client", "ai-agent-tool", "linear-mcp-server",
        ],
    },
    "labels": {
        "title": "Label Operations",
        "description": "Label management and issue tagging",
        "operations": [
            ("issueAddLabel", "labels"),
            ("issueRemoveLabel", "labels"),
            ("issueLabelCreate", "label-management"),
        ],
        "include-categories": [
            "cli-client", "ai-agent-tool", "linear-mcp-server",
        ],
    },
    "teams": {
        "title": "Team Operations",
        "description": "Team listing and management",
        "operations": [
            ("team (read)", "team-management"),
            ("teams (list)", "team-management"),
        ],
        "include-categories": [
            "cli-client", "cross-team", "linear-mcp-server",
        ],
    },
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Project:
    """Parsed project data."""
    name: str
    repo_url: str
    category: str
    secondary_categories: List[str] = field(default_factory=list)
    features: Dict = field(default_factory=dict)
    api_coverage: Dict = field(default_factory=dict)
    stars: int = 0
    filename: str = ""

    def get_operation_support(self, feature_key: Optional[str]) -> str:
        """
        Get support status for a feature.

        Returns: "✅", "⚠️", "👁️", "❌", or "❓"
        """
        if feature_key is None:
            return "❌"

        # Check api-coverage first (more specific)
        if self.api_coverage:
            queries = self.api_coverage.get("queries-supported", [])
            mutations = self.api_coverage.get("mutations-supported", [])
            # Handle both dict and string formats for operations-partial
            partial_list = self.api_coverage.get("operations-partial", [])
            partial = []
            for p in partial_list:
                if isinstance(p, dict):
                    partial.append(p.get("operation", ""))
                elif isinstance(p, str):
                    partial.append(p)

            # Map feature to operations
            ops = FEATURE_OPERATION_MAP.get(feature_key, [])
            for op in ops:
                # For field-specific operations (e.g., "issueCreate:parentId"),
                # we can't determine support from just having the base operation.
                # Fall through to features dict for these.
                if ":" in op:
                    continue  # Skip field-specific ops, use features dict instead

                if op in mutations or op in queries:
                    return "✅"
                if op in partial:
                    return "⚠️"

        # Fall back to features dict
        if not isinstance(self.features, dict):
            return "❓"

        value = self.features.get(feature_key)

        if value is True:
            return "✅"
        elif value is False:
            return "❌"
        elif value == "partial":
            return "⚠️"
        elif value == "read-only":
            return "👁️"
        elif isinstance(value, str) and "partial" in value.lower():
            return "⚠️"
        elif isinstance(value, str) and "read" in value.lower():
            return "👁️"
        elif value is None:
            return "❓"
        else:
            return "❓"


# =============================================================================
# LOADING FUNCTIONS
# =============================================================================

def load_projects(projects_dir: Path) -> List[Project]:
    """Load all project YAML files."""
    projects = []
    for yaml_file in sorted(projects_dir.glob("*.yaml")):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data:
                    projects.append(Project(
                        name=data.get('name', yaml_file.stem),
                        repo_url=data.get('repo-url', ''),
                        category=data.get('category', 'unknown'),
                        secondary_categories=data.get('secondary-categories', []),
                        features=data.get('features', {}),
                        api_coverage=data.get('api-coverage', {}),
                        stars=data.get('stars', 0) or 0,
                        filename=yaml_file.name,
                    ))
        except yaml.YAMLError as e:
            print(f"Warning: Failed to parse {yaml_file}: {e}", file=sys.stderr)
    return projects


def filter_projects_by_resource(
    projects: List[Project],
    resource: str
) -> Tuple[List[Project], List[Project]]:
    """
    Filter projects to only those relevant for a resource category.

    Returns: (included_projects, excluded_projects)
    """
    resource_group = RESOURCE_GROUPS.get(resource, {})
    allowed_categories = resource_group.get('include-categories', [])
    operations = resource_group.get('operations', [])

    included = []
    excluded = []

    for project in projects:
        # Check if category is allowed
        cat_match = (
            project.category in allowed_categories or
            any(cat in allowed_categories for cat in project.secondary_categories)
        )

        if not cat_match:
            excluded.append(project)
            continue

        # Check if project has ANY coverage for this resource
        has_any_coverage = False
        for op_name, feature_key in operations:
            status = project.get_operation_support(feature_key)
            if status in ("✅", "⚠️", "👁️"):
                has_any_coverage = True
                break

        if has_any_coverage:
            included.append(project)
        else:
            excluded.append(project)

    return included, excluded


def calculate_coverage_percentage(
    project: Project,
    operations: List[Tuple[str, Optional[str]]]
) -> int:
    """Calculate coverage percentage for a set of operations."""
    if not operations:
        return 0

    supported = 0
    partial = 0
    total = len(operations)

    for op_name, feature_key in operations:
        status = project.get_operation_support(feature_key)
        if status == "✅":
            supported += 1
        elif status in ("⚠️", "👁️"):
            partial += 0.5

    return int(((supported + partial) / total) * 100)


# =============================================================================
# TABLE GENERATION
# =============================================================================

def generate_legend() -> str:
    """Generate legend for symbols."""
    return """## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Full support |
| ⚠️ | Partial support |
| 👁️ | Read-only |
| ❌ | Not supported |
| ❓ | Unknown / Not tested |
"""


def generate_table_for_projects(
    projects: List[Project],
    operations: List[Tuple[str, Optional[str]]]
) -> str:
    """Generate a markdown table for a list of projects."""
    if not projects:
        return "*No tools with coverage in this category.*\n"

    # Header
    op_names = [op[0] for op in operations]
    header = "| Tool | " + " | ".join(op_names) + " | Coverage |"
    separator = "|------|" + "|".join(["----"] * len(op_names)) + "|----------|"

    lines = [header, separator]

    # Sort by coverage descending, then by stars
    projects_with_coverage = [
        (p, calculate_coverage_percentage(p, operations))
        for p in projects
    ]
    projects_with_coverage.sort(key=lambda x: (-x[1], -(x[0].stars or 0), x[0].name.lower()))

    for project, coverage in projects_with_coverage:
        name_link = f"[{project.name}]({project.repo_url})" if project.repo_url else project.name
        cells = [name_link]

        for op_name, feature_key in operations:
            status = project.get_operation_support(feature_key)
            cells.append(status)

        cells.append(f"{coverage}%")
        lines.append("| " + " | ".join(cells) + " |")

    return '\n'.join(lines)


def generate_resource_table(
    projects: List[Project],
    resource: str
) -> str:
    """Generate markdown table for a resource type."""
    resource_group = RESOURCE_GROUPS[resource]
    operations = resource_group['operations']
    title = resource_group['title']
    description = resource_group.get('description', '')
    note = resource_group.get('note', '')

    lines = [
        f"# {title} Coverage\n",
        f"*{description}*\n",
        f"*Generated from {len(projects)} project files on {date.today().isoformat()}*\n",
        "",
        generate_legend(),
        "",
        "---",
        "",
    ]

    if note:
        lines.append(f"> {note}\n")
        lines.append("")

    # Filter to only relevant projects
    included, excluded = filter_projects_by_resource(projects, resource)

    if not included:
        lines.append("*No tools found with coverage for this resource.*\n")
        lines.append("")
        lines.append("## Tools Without Coverage\n")
        lines.append("")
        for p in sorted(excluded, key=lambda x: x.name.lower()):
            if p.category in resource_group.get('include-categories', []):
                lines.append(f"- [{p.name}]({p.repo_url}) ({p.category})")
        return '\n'.join(lines)

    # Group projects by category
    categories: Dict[str, List[Project]] = {}
    for p in included:
        cat = p.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)

    # Category display order
    category_order = [
        "cli-client", "tui-client", "git-workflow", "ai-agent-tool",
        "cross-team", "importer-exporter", "linear-mcp-server",
    ]

    for cat in category_order:
        if cat not in categories:
            continue
        cat_title = cat.replace('-', ' ').title()
        lines.append(f"## {cat_title}\n")
        lines.append("")
        lines.append(generate_table_for_projects(categories[cat], operations))
        lines.append("")

    # Gap analysis
    lines.append("---\n")
    lines.append("")
    lines.append(generate_gap_analysis(included, operations))

    return '\n'.join(lines)


def generate_gap_analysis(
    projects: List[Project],
    operations: List[Tuple[str, Optional[str]]]
) -> str:
    """Generate gap analysis section."""
    lines = ["## Gap Analysis\n", ""]

    # Find operations with zero support
    unsupported = []
    for op_name, feature_key in operations:
        support_count = sum(
            1 for p in projects
            if p.get_operation_support(feature_key) in ("✅", "⚠️", "👁️")
        )
        if support_count == 0:
            unsupported.append(op_name)

    if unsupported:
        lines.append("### Unsupported by All Tools\n")
        lines.append("")
        for op in unsupported:
            lines.append(f"- `{op}` - No tool supports this operation")
        lines.append("")

    # Find best tools
    lines.append("### Best Coverage\n")
    lines.append("")
    projects_ranked = sorted(
        [(p, calculate_coverage_percentage(p, operations)) for p in projects],
        key=lambda x: (-x[1], x[0].name.lower())
    )[:5]

    if projects_ranked:
        for i, (project, coverage) in enumerate(projects_ranked, 1):
            lines.append(f"{i}. [{project.name}]({project.repo_url}) - {coverage}%")
    else:
        lines.append("*No tools with coverage data.*")

    return '\n'.join(lines)


# =============================================================================
# OVERVIEW GENERATION
# =============================================================================

def generate_overview(projects: List[Project]) -> str:
    """Generate overview.md with summary statistics."""
    lines = [
        "# Linear API Coverage Overview\n",
        "",
        f"*Generated from {len(projects)} project files on {date.today().isoformat()}*\n",
        "",
        "## Summary Statistics\n",
        "",
    ]

    # Count by category
    categories: Dict[str, int] = {}
    for p in projects:
        cat = p.category
        categories[cat] = categories.get(cat, 0) + 1

    lines.append("### Tools by Category\n")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|----------|-------|")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        cat_title = cat.replace('-', ' ').title()
        lines.append(f"| {cat_title} | {count} |")
    lines.append("")

    # Count tools with api-coverage data
    with_coverage = sum(1 for p in projects if p.api_coverage)
    lines.append(f"**Tools with `api-coverage` data:** {with_coverage}/{len(projects)}\n")
    lines.append("")

    # Overall gap analysis
    lines.append("## Key API Coverage Gaps\n")
    lines.append("")

    # Check issue relations specifically
    lines.append("### Issue Relationships (Blocking/Blocked-by)\n")
    lines.append("")
    lines.append("> **No CLI tool currently supports issue relationships.**\n")
    lines.append("")
    lines.append("The Linear GraphQL API provides `issueRelationCreate` with these types:\n")
    lines.append("- `blocks` - Issue A blocks Issue B\n")
    lines.append("- `duplicate` - Mark as duplicate\n")
    lines.append("- `related` - Related issues\n")
    lines.append("")
    lines.append("This is a significant gap for dependency tracking workflows.\n")
    lines.append("")

    # Resource coverage summary
    lines.append("## Resource Coverage Tables\n")
    lines.append("")
    for resource, group in RESOURCE_GROUPS.items():
        note = " ⚠️" if group.get('highlight') else ""
        lines.append(f"- [{group['title']}]({resource}.md){note}")
    lines.append("")

    # Tools with highest overall coverage
    lines.append("## Top Tools by Overall Feature Coverage\n")
    lines.append("")

    all_operations = []
    for group in RESOURCE_GROUPS.values():
        all_operations.extend(group['operations'])

    projects_ranked = sorted(
        [(p, calculate_coverage_percentage(p, all_operations)) for p in projects if p.category in ['cli-client', 'ai-agent-tool', 'linear-mcp-server']],
        key=lambda x: (-x[1], -(x[0].stars or 0))
    )[:10]

    lines.append("| Tool | Category | Coverage | Stars |")
    lines.append("|------|----------|----------|-------|")
    for project, coverage in projects_ranked:
        name = f"[{project.name}]({project.repo_url})" if project.repo_url else project.name
        stars = f"⭐ {project.stars}" if project.stars else "-"
        lines.append(f"| {name} | {project.category} | {coverage}% | {stars} |")
    lines.append("")

    return '\n'.join(lines)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Generate Linear API coverage tables')
    parser.add_argument('--resource', type=str, help='Generate only this resource table')
    parser.add_argument('--overview-only', action='store_true', help='Generate only overview')
    parser.add_argument('--output-dir', type=str, default='comparisons/api-coverage')
    parser.add_argument('--projects-dir', type=str, default='projects')

    args = parser.parse_args()

    # Find paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    projects_dir = repo_root / args.projects_dir
    output_dir = repo_root / args.output_dir

    if not projects_dir.exists():
        print(f"Error: Projects directory not found at {projects_dir}", file=sys.stderr)
        return 1

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    projects = load_projects(projects_dir)
    print(f"Loaded {len(projects)} projects", file=sys.stderr)

    # Generate overview
    if args.overview_only or not args.resource:
        overview_file = output_dir / "overview.md"
        overview_file.write_text(generate_overview(projects))
        print(f"Generated {overview_file}", file=sys.stderr)

    if args.overview_only:
        return 0

    # Generate per-resource tables
    resources_to_generate = [args.resource] if args.resource else list(RESOURCE_GROUPS.keys())

    for resource in resources_to_generate:
        if resource not in RESOURCE_GROUPS:
            print(f"Warning: Unknown resource '{resource}', skipping", file=sys.stderr)
            continue

        output_file = output_dir / f"{resource}.md"
        content = generate_resource_table(projects, resource)
        output_file.write_text(content)
        print(f"Generated {output_file}", file=sys.stderr)

    print(f"\nDone! Output files in {output_dir}", file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
