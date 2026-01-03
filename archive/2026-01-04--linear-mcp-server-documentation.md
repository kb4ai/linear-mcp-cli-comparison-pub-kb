# Linear MCP Server Documentation

**Source URL:** https://linear.app/docs/mcp
**Archive Date:** 2026-01-04
**Summary:** Complete documentation for Linear's Model Context Protocol (MCP) server implementation, including setup instructions for various platforms and authentication methods.

---

## Overview

The Model Context Protocol (MCP) server provides a standardized interface allowing compatible AI models and agents to access Linear data securely and simply. It operates as a centrally hosted, managed service following the authenticated remote MCP specification.

## Setup Instructions

### General Information

Linear's MCP server supports both Server-Sent Events (SSE) and Streamable HTTP transports using OAuth 2.1 with dynamic client registration:

* **HTTP endpoint:** `https://mcp.linear.app/mcp`
* **SSE endpoint:** `https://mcp.linear.app/sse`

The streamable HTTP endpoint is recommended for increased reliability where supported.

### Claude Setup

**Team/Enterprise (Claude.ai):**

1. Navigate to Settings → Integrations → Add more
2. Enter integration name: `Linear`
3. Enter URL: `https://mcp.linear.app/mcp`
4. Enable tools in new chats

**Free/Pro (Claude Desktop):**

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.linear.app/mcp"]
    }
  }
}
```

**Claude Code:**

```bash
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

Then run `/mcp` in a session to authenticate.

### Cursor Setup

Install via [direct link](cursor://anysphere.cursor-deeplink/mcp/install?name=Linear&config=eyJ1cmwiOiJodHRwczovL21jcC5saW5lYXIuYXBwL3NzZSJ9) or search Linear in MCP tools.

### Visual Studio Code

1. Press CTRL/CMD P, search "MCP: Add Server"
2. Select "Command (stdio)"
3. Enter: `npx mcp-remote https://mcp.linear.app/mcp`
4. Name it "Linear"
5. Activate via "MCP: List Servers"

### Codex Setup

**CLI method:**

```bash
codex mcp add linear --url https://mcp.linear.app/mcp
codex mcp login linear
```

**Configuration (add to `~/.codex/config.toml`):**

```toml
[features]
experimental_use_rmcp_client = true

[mcp_servers.linear]
url = "https://mcp.linear.app/mcp"
```

### Other Platforms

* **v0 by Vercel:** Install from connections page
* **Windsurf/Zed:** Similar configuration using `mcp-remote`
* **Generic tools:** Use command `npx` with arguments `-y mcp-remote https://mcp.linear.app/mcp`

## Capabilities

The MCP server provides tools for discovering, creating, and updating Linear objects including issues, projects, and comments, with additional functionality planned.

## Authentication

The server supports two authentication approaches:

1. **Interactive OAuth flow** (default)
2. **Direct token authentication:** Pass OAuth tokens or API keys via `Authorization: Bearer <token>` header for app users, restricted API key access, or existing Linear OAuth applications

## Troubleshooting

**Internal server errors:** Clear saved auth with `rm -rf ~/.mcp-auth` and retry. Update Node.js if needed.

**WSL on Windows:** Use SSE transport instead:

```json
{"mcpServers": {"linear": {"command": "wsl", "args": ["npx", "-y", "mcp-remote", "https://mcp.linear.app/sse", "--transport", "sse-only"]}}}
```

**Streamable HTTP support:** Yes, available at the standard HTTP endpoint.

---

**Related Resources:**

* MCP Protocol Specification: https://modelcontextprotocol.io/
* Linear GraphQL API: https://linear.app/developers/graphql
* Linear API Documentation: https://linear.app/developers
