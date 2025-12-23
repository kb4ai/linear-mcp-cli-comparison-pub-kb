# Linear CLI Tools Comparison

A comprehensive comparison of command-line tools for [Linear.app](https://linear.app), the modern issue tracking platform.

## Quick Navigation

| I want to... | Recommended Tool | Why |
|--------------|------------------|-----|
| Use a git-aware CLI with PR integration | [schpet/linear-cli](#git-workflow-tools) | Best git/GitHub integration |
| Use Linear from AI agents (Claude, Cursor) | [linctl](#ai-agent-tools) | Purpose-built for agents |
| View issues in a terminal UI | [lt](#tui-clients) | Beautiful Rust TUI |
| Do cross-team reporting | [@anoncam/linear-cli](#cross-team-tools) | Multi-team queries, kanban |
| Bulk import/export issues | [linear-issue-importer](#importerexporter) | JSON/CSV batch operations |
| Use on Arch Linux (AUR) | [linearator](#cli-clients) | Available in AUR |

## Ecosystem Overview

**Total Tools Tracked:** 15+

| Category | Count | Description |
|----------|-------|-------------|
| CLI Clients | 8 | Standard command-line interfaces |
| TUI Clients | 1 | Terminal User Interface (interactive) |
| AI Agent Tools | 2 | Designed for AI integration |
| Git Workflow | 3 | Git/GitHub focused |
| Cross-Team | 1 | Multi-team reporting |
| Importer/Exporter | 1 | Bulk operations |

**Languages:** TypeScript/Deno, Python, Rust, Go, Node.js, Ruby

---

## CLI Clients

Standard command-line interfaces for Linear operations.

| Tool | Language | Stars | Key Features | Install |
|------|----------|-------|--------------|---------|
| [schpet/linear-cli](https://github.com/schpet/linear-cli) | TypeScript/Deno | - | Git-aware, PR creation, branch management | `brew install schpet/tap/linear` |
| [linearator](https://github.com/linearator/linearator) | Python | - | PyPI + AUR, comprehensive | `pip install linearator` |
| [@minupalaniappan/linear](https://github.com/minupalaniappan/linear-cli) | Node.js | - | Branch-aware, simple | `npm i -g @minupalaniappan/linear` |
| [@digitalstories/linear-cli](https://www.npmjs.com/package/@digitalstories/linear-cli) | Node.js | - | French language support | `npm i -g @digitalstories/linear-cli` |
| [carlosflorencio/linear-cli](https://github.com/carlosflorencio/linear-cli) | Go | - | Go-based, simple | `go install` |
| [pylinear](https://github.com/hxghhhh/pylinear) | Python | - | Click framework | `pip install` |

---

## TUI Clients

Terminal User Interface applications with interactive displays.

| Tool | Language | Stars | Key Features | Install |
|------|----------|-------|--------------|---------|
| [lt](https://github.com/markmarkoh/lt) | Rust | - | Read-only TUI, issue browser, clipboard integration | `brew tap markmarkoh/lt && brew install lt` |

**lt Features:**

* View "My Issues" with full details
* Press `y` to copy git branch name to clipboard
* Press `o` to open issue in Linear
* View switcher with `/` + Tab
* Optimized for modern terminals (kitty, Ghostty, iTerm2)

---

## AI Agent Tools

Tools designed for integration with AI coding assistants.

| Tool | Language | Stars | Key Features | Install |
|------|----------|-------|--------------|---------|
| [linctl](https://github.com/dorkitude/linctl) | Go | - | Agent-friendly, image download, flexible auth | `go install github.com/dorkitude/linctl@latest` |
| [filipjaj/linear-cli](https://github.com/filipjaj/linear-cli) | Go | - | AI-powered issue creation (Gemini) | `go install` |

**linctl** is purpose-built for AI agents (Claude Code, Cursor, Amp) while remaining human-friendly:

* Authenticated image downloads
* Flexible credential storage (env vars, keyring, encrypted files, JSON)
* Structured output for agent parsing

---

## Git Workflow Tools

Tools focused on git integration and GitHub workflows.

| Tool | Language | Stars | Key Features | Install |
|------|----------|-------|--------------|---------|
| [schpet/linear-cli](https://github.com/schpet/linear-cli) | TypeScript/Deno | - | Auto-detect issue from branch, PR creation | `brew install schpet/tap/linear` |
| [@minupalaniappan/linear](https://github.com/minupalaniappan/linear-cli) | Node.js | - | Branch-aware commands | `npm i -g @minupalaniappan/linear` |

**schpet/linear-cli** Workflow:

```bash
linear issue start ABC-123    # Create branch, mark issue started
# ... make changes ...
linear issue pr               # Create PR with Linear issue details
```

---

## Cross-Team Tools

Tools for multi-team reporting and analysis.

| Tool | Language | Stars | Key Features | Install |
|------|----------|-------|--------------|---------|
| [@anoncam/linear-cli](https://www.npmjs.com/package/@anoncam/linear-cli) | Node.js | - | Cross-team queries, kanban view, AI labels | `npm i -g @anoncam/linear-cli` |

**Features:**

* Cross-team queries and analysis
* Interactive terminal kanban board (`-k` flag)
* AI-assisted label management with Claude
* Report generation in markdown
* Direct GraphQL API integration

---

## Importer/Exporter

Bulk import and export tools.

| Tool | Language | Stars | Key Features | Install |
|------|----------|-------|--------------|---------|
| [linear-issue-importer](https://crates.io/crates/linear-issue-importer) | Rust | - | JSON/CSV batch create/update | `cargo install linear-issue-importer` |

---

## Rust Alternatives

Additional Rust-based tools:

| Tool | Description |
|------|-------------|
| [eriksandfort/linear_cli](https://github.com/eriksandfort/linear_cli) | Rust CLI |
| [max-muoto/linear-cli](https://github.com/max-muoto/linear-cli) | Another Rust CLI |

---

## Ruby Alternatives

| Tool | Description |
|------|-------------|
| [rubyists/linear-cli](https://github.com/rubyists/linear-cli) | Ruby-based Linear CLI |

---

## Authentication Setup

Most tools use the `LINEAR_API_KEY` environment variable:

1. Generate API key: **Linear Settings → Account → Security & Access → Personal API Keys → "New API Key"**

2. Set environment variable:

```bash
# Bash/Zsh
export LINEAR_API_KEY="lin_api_..."

# Fish
set -Ux LINEAR_API_KEY "lin_api_..."
```

---

## MCP Server Integration

Linear also provides an official [MCP (Model Context Protocol) server](https://linear.app/docs/mcp) for AI coding assistants:

```bash
# Configure for Claude Code
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

This enables natural language interactions with Linear from development environments.

---

## Detailed Comparisons

* [Feature Comparison](comparisons/features.md) - Side-by-side feature matrix
* [By Language](comparisons/by-language.md) - Grouped by programming language
* [Git Integration](comparisons/git-integration.md) - Git workflow capabilities
* [Auto-Generated Tables](comparisons/auto-generated.md) - Full data tables

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add or update tools.

## Data Sources

Project data is stored in YAML format in `projects/` directory. See [spec.yaml](spec.yaml) for schema.
