# Initial Research: Linear CLI Tools

**Date:** 2025-12-23
**Source:** Perplexity AI search for "linux unix CLI tools for linear.app"

## Research Query

Searched for comprehensive overview of command-line tools for interacting with Linear.app from terminal environments.

## Key Findings

### Featured Tools Identified

1. **linctl** (Go) - Agent-friendly, built for AI assistants
2. **schpet/linear-cli** (TypeScript/Deno) - Git-aware, best GitHub integration
3. **linearator** (Python) - AUR support, comprehensive
4. **@anoncam/linear-cli** (Node.js) - Cross-team reporting, kanban view
5. **lt** (Rust) - Beautiful TUI for issue browsing
6. **@minupalaniappan/linear** (Node.js) - Branch-aware commands

### Language Distribution

* **Go:** linctl, carlosflorencio/linear-cli, filipjaj/linear-cli
* **TypeScript/Deno:** schpet/linear-cli
* **Python:** linearator, pylinear, linear-app-cli
* **Node.js:** @anoncam/linear-cli, @minupalaniappan/linear, @digitalstories/linear-cli
* **Rust:** lt, eriksandfort/linear_cli, max-muoto/linear-cli, linear-issue-importer
* **Ruby:** rubyists/linear-cli

### Unique Differentiators

| Tool | Unique Value |
|------|--------------|
| linctl | Purpose-built for AI agents, image downloads |
| schpet/linear-cli | Git branch detection, `gh pr create` integration |
| lt | TUI with view switcher, clipboard support |
| @anoncam/linear-cli | Kanban board, cross-team queries, Claude AI labels |
| linearator | Arch Linux AUR package |
| linear-issue-importer | JSON/CSV bulk operations |

### MCP Integration

Linear provides official MCP (Model Context Protocol) server:

```bash
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

This enables natural language Linear interactions from Claude Code and other AI assistants.

## Installation Patterns

Most common:

* **npm:** 4 tools
* **cargo:** 4 tools
* **go install:** 3 tools
* **pip:** 3 tools
* **brew:** 2 tools (schpet/linear-cli, lt)
* **aur:** 1 tool (linearator)
* **deno:** 1 tool (schpet/linear-cli)

## Authentication Pattern

Nearly all tools use `LINEAR_API_KEY` environment variable:

```bash
export LINEAR_API_KEY="lin_api_..."
```

Some tools (linctl) offer additional options: system keyring, encrypted files.

## Source References

* GitHub repositories
* npm packages
* crates.io
* PyPI
* AUR
* Reddit r/Linear discussions

## Next Steps

1. Clone repositories for deeper analysis
2. Verify star counts from GitHub API
3. Test installation methods
4. Document security considerations
5. Create detailed comparison matrices
