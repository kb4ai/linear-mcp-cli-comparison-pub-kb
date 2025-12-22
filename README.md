# Linear CLI and MCP Tools Comparison

## Why This Research Matters

> **The official Linear MCP server uses ~13,000 tokens just to connect.**

That's 6.5% to 13% of your available context (100k-200k tokens) consumed before any actual work begins. Every conversation. Every time.

This research compares alternatives that are more efficient for agent workflows.

## The Bigger Picture: CLI Tools Enable Custom Automation

MCP servers are convenient for discovery, but **CLI tools with JSON output unlock something more powerful**:

```bash
# Once you have a CLI tool like linearis, you can ask an LLM to generate:

# Custom issue views for YOUR workflow
linearis search "team:engineering status:in-progress" | jq '.[] | {id, title, assignee}'

# Daily standup reports
linearis my-issues --since yesterday | python generate_standup.py

# Project dashboards (HTML on localhost!)
linearis project ABC | python -c "import json,sys; ..." > dashboard.html && python -m http.server 8080

# Slack/Discord notifications
linearis search "priority:urgent updated:today" | jq -r '.[] | "🔥 \(.title)"' | notify-send
```

**The pattern:**
1. LLM generates a script once (using jq, python, whatever)
2. Script runs instantly, forever, without LLM involvement
3. Customize for YOUR projects, teams, workflows
4. Build personal dashboards, alerts, reports

MCP servers can't do this. They require the LLM for every interaction.

## Research Goals

* Find CLI tools for Linear (beyond the official MCP server)
* Identify MCP CLI tools that support authenticated HTTP endpoints
* Document proxy solutions for tools that don't support auth headers
* Compare token efficiency vs feature completeness
* Recommend tools for different use cases

## Quick Stats

| Metric | Status |
|--------|--------|
| Research scope | Defined |
| Projects tracked | 1 (discovery in progress) |
| Token efficiency documented | Yes |

## Key Finding So Far

[**Linearis**](https://github.com/czottmann/linearis) - A Linear CLI built specifically for agent use:
- JSON output, works with jq
- Focused feature set (not 20+ tools you don't need)
- Near-zero token overhead
- [Blog post explaining the motivation](https://zottmann.org/2025/09/03/linearis-my-linear-cli-built.html)

## Research Approach

We're using parallel subagents to investigate:

1. **Linear CLI Tools** - Direct CLI tools for Linear API
2. **Linear MCP Servers** - MCP servers exposing Linear
3. **MCP CLI Tools with Auth** - Tools supporting HTTP + Bearer tokens
4. **Proxy/Bridge Solutions** - stdio↔HTTP bridges with auth

See [ramblings/2025-12-22--subagent-analysis-plan.md](ramblings/2025-12-22--subagent-analysis-plan.md) for details.

## Repository Structure

```
.
├── README.md                    # This file
├── SCOPE.md                     # Research scope definition
├── archive/                     # Archived web research
├── projects/                    # YAML files for each tool
├── reports/                     # Subagent analysis reports
├── ramblings/                   # Research notes and insights
├── comparisons/                 # Generated comparison tables
└── scripts/                     # Utility scripts
```

## Documentation

| Document | Purpose |
|----------|---------|
| [SCOPE.md](SCOPE.md) | What we're researching and why |
| [PROCESS.md](PROCESS.md) | Research methodology |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to add findings |
| [spec.yaml](spec.yaml) | YAML schema for projects |

## Key Insights

* [Token Efficiency](ramblings/2025-12-22--token-efficiency-insight.md) - Why this matters for agents
* [MCP Auth Investigation](ramblings/2025-12-22--mcptools-linear-auth-investigation.md) - Why mcptools doesn't work with Linear
* [Auth Solutions](ramblings/2025-12-22--mcp-auth-solutions-research.md) - Working alternatives

## The Token Efficiency Trade-off

| Approach | Connection Tokens | Automation Potential | Best For |
|----------|-------------------|----------------------|----------|
| Official MCP Server | ~13,000 | Low (requires LLM) | Exploration, full API |
| Focused MCP Server | ~2,000-5,000 | Low | Balanced |
| CLI + JSON (linearis) | ~0 | **High** (scripts!) | Daily workflows |
| Direct API (curl) | ~0 | **High** | Automation, CI/CD |

## Contributing

Found a Linear CLI tool or MCP solution? See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
# Quick start
./scripts/clone-all.sh          # Clone tracked repos
./scripts/check-yaml.py         # Validate YAML
./scripts/generate-tables.py    # Generate tables
```

## Prior Art

This research builds on [mcp-as-cli-tools-comparison](../mcp-as-cli-tools-comparison/) which cataloged 27 MCP wrapper tools with security analysis.
