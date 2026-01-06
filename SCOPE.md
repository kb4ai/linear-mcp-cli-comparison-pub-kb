# Research Scope Definition

## Research Title

**Title:** Linear CLI and MCP Tools Comparison

## Research Question

* What CLI tools exist for interacting with Linear (issue tracking)?
* What MCP servers provide Linear integration?
* Which MCP CLI tools support authenticated HTTP endpoints (needed for Linear's MCP server)?
* What proxy/bridge solutions enable tools like mcptools to work with authenticated MCP servers?

## Why This Research Matters

> **The official Linear MCP server uses [~13,000 tokens just to connect](https://zottmann.org/2025/09/03/linearis-my-linear-cli-built.html).**

That's 6.5% to 13% of your available context (100k-200k tokens) consumed before any actual work begins. Every conversation. Every time.

This research compares alternatives that are more efficient for agent workflows.

### The Bigger Picture: CLI Tools Enable Custom Automation

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

# Pretty terminal tables via CSV
linearis issues list | jq -r '.[] | [.identifier, .title, .state] | @csv' | csview
```

**Key tools:** [jq](https://github.com/jqlang/jq) (JSON processing), [csview](https://github.com/wfxr/csview)/[xsv](https://github.com/BurntSushi/xsv) (CSV tables), [csvlens](https://github.com/YS-L/csvlens) (interactive CSV viewer).

**The pattern:**

1. LLM generates a script once (using jq, python, whatever)
2. Script runs instantly, forever, without LLM involvement
3. Customize for YOUR projects, teams, workflows
4. Build personal dashboards, alerts, reports

MCP servers can't do this. They require the LLM for every interaction.

See [JSON CLI Workflows](ramblings/2026-01-07--json-cli-workflows.md) for detailed examples.

## Motivation

Linear provides an MCP server at `https://mcp.linear.app/mcp` that requires authentication. Initial investigation revealed that popular tools like `mcptools` don't support passing authorization headers for direct HTTP MCP use. This research aims to:

1. Catalog all available Linear CLI/MCP tools
2. Identify which tools support authenticated HTTP MCP endpoints
3. Document proxy/bridge solutions that enable auth-less tools to work
4. Provide recommendations for different use cases

## Scope Definition

### In Scope

* [x] CLI tools for Linear (official and third-party)
* [x] MCP servers for Linear
* [x] MCP CLI tools that support HTTP authentication
* [x] Proxy/bridge solutions (stdio↔HTTP with auth)
* [x] Direct API approaches (curl/JSON-RPC)

### Out of Scope

* [ ] Linear web UI analysis
* [ ] IDE plugins (unless they provide CLI)
* [ ] Abandoned projects (no commits in 2+ years)
* [ ] Non-open-source tools (unless official)

## Target Platform/Service

**Primary:** Linear (issue tracking / project management)
**Official API Docs:** https://developers.linear.app/docs
**Official MCP Docs:** https://linear.app/docs/mcp
**MCP Endpoint:** https://mcp.linear.app/mcp

## Categories

### Linear CLI Categories

| Category ID | Description |
|-------------|-------------|
| `cli-client` | Standard CLI for Linear operations |
| `tui-client` | Terminal User Interface (interactive) |
| `ai-agent-tool` | Designed for AI agent integration |
| `importer-exporter` | Bulk import/export operations |
| `git-workflow` | Focused on git/GitHub integration |
| `cross-team` | Multi-team reporting and analysis |

### MCP & Proxy Categories

| Category ID | Description |
|-------------|-------------|
| `linear-mcp-server` | MCP servers exposing Linear functionality |
| `mcp-cli-auth` | MCP CLI tools with HTTP auth support |
| `proxy-bridge` | stdio↔HTTP bridges with auth support |

## Data Points to Collect

### Required Fields

- [x] `repo-url` - Repository URL
- [x] `last-update` - Date of last analysis
- [x] `name` - Project name
- [x] `description` - Brief description
- [x] `category` - Project category

### Standard Fields

- [x] `stars` - GitHub stars
- [x] `language` - Primary programming language
- [x] `license` - License type
- [x] `last-commit` - Date of last commit
- [x] `reputable-source` - From known organization?
- [x] `features` - List of features
- [x] `installation` - Installation methods

### Domain-Specific Fields

| Field | Type | Description |
|-------|------|-------------|
| `transports.stdio` | boolean | Supports stdio transport |
| `transports.http` | boolean | Supports HTTP transport |
| `transports.sse` | boolean | Supports SSE transport |
| `auth.api-key` | boolean | Supports API key auth |
| `auth.oauth` | boolean | Supports OAuth |
| `auth.bearer-header` | boolean | Supports passing Bearer header |
| `linear-api-coverage` | string | full/partial/minimal |
| `tested-with-linear` | boolean | Verified working with Linear MCP |

## Search Strategy

### GitHub Searches

```bash
# Linear CLI tools
"linear cli" language:typescript
"linear cli" language:python
"linear cli" language:go
"linctl" OR "linear-cli"

# Linear MCP servers
"linear mcp server"
"mcp server" + "linear.app"
topic:mcp topic:linear

# MCP CLI tools with auth
"mcp cli" + "authorization" OR "bearer"
"mcp client" + "http" + "auth"
"mcp" + "--header"

# Proxy solutions
"mcp proxy" + "bearer" OR "auth"
"stdio http" + "mcp" + "bridge"
"mcp-proxy"
```

### Other Sources

* [x] Official Linear integrations: https://linear.app/integrations
* [x] Linear MCP docs: https://linear.app/docs/mcp
* [x] mcpservers.org: Search for Linear
* [x] npm: @modelcontextprotocol packages
* [x] PyPI: mcp-proxy, mcp packages
* [x] Reference: ../mcp-as-cli-tools-comparison (sibling repo)

## Success Criteria

* [x] Found all major Linear CLI tools (target: 5+ projects)
* [x] Found Linear MCP server options (target: 3+ projects)
* [x] Identified MCP CLI tools with auth support (target: 5+ projects)
* [x] Documented working proxy solutions (target: 3+ solutions)
* [ ] Validated top 5 solutions practically
* [ ] Generated comparison tables
* [ ] Wrote recommendations for different use cases

## Subagent Analysis Strategy

Research will be split into 5 parallel agents:

1. **Agent 1:** Linear CLI Tools discovery
2. **Agent 2:** Linear MCP Servers discovery
3. **Agent 3:** MCP CLI tools with auth support
4. **Agent 4:** Proxy/bridge solutions
5. **Agent 5:** Solution validation (sequential, after 1-4)

See `ramblings/2025-12-22--subagent-analysis-plan.md` for detailed plan.

## Prior Research

Initial investigation documented in:

* `ramblings/2025-12-22--mcptools-linear-auth-investigation.md` - Failed attempts with mcptools
* `ramblings/2025-12-22--mcp-auth-solutions-research.md` - Perplexity research on solutions

Key findings:
- mcptools does NOT support HTTP auth headers for direct use
- MCP Inspector CLI mode works with `--header` flag
- Proxy solutions available: mcp-proxy, mcp-stdio-to-streamable-http-adapter
- Linear supports both OAuth and direct API key auth

---

**Scope defined:** 2025-12-22
**Status:** Ready for discovery phase
