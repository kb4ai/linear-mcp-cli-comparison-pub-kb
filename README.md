# Linear CLI and MCP Tools Comparison

A comprehensive comparison of command-line tools for [Linear.app](https://linear.app), including CLI clients, MCP servers, and proxy solutions.

## Quick Navigation

| I want to... | Go to |
|--------------|-------|
| Find the right CLI tool for my workflow | [Tool Recommendations](#tool-recommendations) |
| See all CLI tools compared | [CLI Clients](#cli-clients) |
| Use Linear with AI agents | [AI Agent Tools](#ai-agent-tools) |
| Understand the MCP token problem | [SCOPE.md](SCOPE.md#why-this-research-matters) |
| See MCP servers and proxies | [MCP Tools](#mcp-servers-and-proxies) |
| View feature comparison matrices | [Detailed Comparisons](#detailed-comparisons) |
| **See API coverage by resource** | [API Coverage](comparisons/api-coverage/overview.md) |
| Find workarounds for missing features | [WORKAROUNDS.md](WORKAROUNDS.md) |
| Contribute to this research | [CONTRIBUTING.md](CONTRIBUTING.md) |

---

## Tool Recommendations

| I want to... | Recommended Tool | Why |
|--------------|------------------|-----|
| Use a git-aware CLI with PR integration | [schpet/linear-cli](https://github.com/schpet/linear-cli) | Best git/GitHub integration |
| Use Linear from AI agents (Claude, Cursor) | [linctl](https://github.com/dorkitude/linctl) | Purpose-built for agents |
| Minimize token overhead for agents | [linearis](https://github.com/czottmann/linearis) | JSON output, focused feature set |
| View issues in a terminal UI | [lt](https://github.com/markmarkoh/lt) | Beautiful Rust TUI |
| Do cross-team reporting | [@anoncam/linear-cli](https://www.npmjs.com/package/@anoncam/linear-cli) | Multi-team queries, kanban |
| Bulk import/export issues | [linear-issue-importer](https://crates.io/crates/linear-issue-importer) | JSON/CSV batch operations |
| Use on Arch Linux (AUR) | [linearator](https://github.com/linearator/linearator) | Available in AUR |

---

## Quick Stats

| Category | Count |
|----------|-------|
| Total projects tracked | 55+ |
| Linear CLI tools | 13 |
| Linear MCP servers | 12 |
| MCP CLI auth tools | 9 |
| Proxy/bridge solutions | 11 |

**Languages:** TypeScript, Python, Rust, Go, Swift, Node.js, Ruby

---

## CLI Clients

| Tool | Language | Key Features | Install |
|------|----------|--------------|---------|
| [schpet/linear-cli](https://github.com/schpet/linear-cli) | TypeScript/Deno | Git-aware, PR creation, branch management | `brew install schpet/tap/linear` |
| [linearis](https://github.com/czottmann/linearis) | TypeScript | Comprehensive CLI, document management | `brew install czottmann/tap/linearis` |
| [linctl](https://github.com/dorkitude/linctl) | Go | AI agent-friendly, flexible auth | `go install github.com/dorkitude/linctl@latest` |
| [linearator](https://github.com/linearator/linearator) | Python | PyPI + AUR, comprehensive | `pip install linearator` |
| [lt](https://github.com/markmarkoh/lt) | Rust | Read-only TUI, issue browser | `brew tap markmarkoh/lt && brew install lt` |
| [@anoncam/linear-cli](https://www.npmjs.com/package/@anoncam/linear-cli) | Node.js | Cross-team, kanban, AI labels | `npm i -g @anoncam/linear-cli` |

[View full CLI comparison →](comparisons/auto-generated.md)

---

## AI Agent Tools

Tools optimized for LLM agent integration with minimal token overhead:

| Tool | Focus | Token Efficiency |
|------|-------|------------------|
| [linearis](https://github.com/czottmann/linearis) | JSON output, focused features | ~0 tokens (CLI, no schema) |
| [linctl](https://github.com/dorkitude/linctl) | Agent-friendly, structured output | ~0 tokens (CLI, no schema) |
| Official MCP Server | Full Linear API | ~13,000 tokens on connect |

See [SCOPE.md](SCOPE.md#why-this-research-matters) for the token efficiency analysis.

---

## MCP Servers and Proxies

For users who need MCP integration:

| Category | Examples | Description |
|----------|----------|-------------|
| Linear MCP Servers | linear-mcp, dvcrn/mcp-server-linear | MCP servers for Linear |
| Auth Proxies | mcp-proxy, mcp-auth-proxy | Add auth to MCP tools |
| Bridges | mcp-bridge, mcp-gateway | stdio↔HTTP bridging |

[View full MCP comparison →](comparisons/auto-generated.md)

---

## Detailed Comparisons

| Document | Description |
|----------|-------------|
| [Feature Matrix](comparisons/features.md) | Side-by-side feature comparison |
| [Advanced Features](comparisons/advanced-features.md) | Sub-issues, estimates, blocking |
| [**API Coverage**](comparisons/api-coverage/overview.md) | GraphQL operations by resource |
| [Git Integration](comparisons/git-integration.md) | Git workflow capabilities |
| [By Language](comparisons/by-language.md) | Grouped by programming language |
| [Auto-Generated Tables](comparisons/auto-generated.md) | Full data from all projects |

---

## Authentication Setup

Most tools use `LINEAR_API_KEY`:

1. **Generate key:** Linear Settings → Account → Security & Access → Personal API Keys
2. **Set environment variable:**

```bash
export LINEAR_API_KEY="lin_api_..."
```

---

## Research Methodology

This repository follows a structured research approach:

| Document | Purpose |
|----------|---------|
| [SCOPE.md](SCOPE.md) | Research goals, motivation, token efficiency analysis |
| [PROCESS.md](PROCESS.md) | Discovery and analysis methodology |
| [GUIDELINES.md](GUIDELINES.md) | Data collection standards |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to add/update tools |
| [QUICKSTART.md](QUICKSTART.md) | Setup and usage guide |

---

## Project Data

* **YAML files:** `projects/*.yaml` - One file per tool
* **Schema:** [spec.yaml](spec.yaml) - Field definitions
* **Validation:** `./scripts/check-yaml.py`
* **Table generation:** `./scripts/generate-tables.py`

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for step-by-step instructions on adding or updating tools.
