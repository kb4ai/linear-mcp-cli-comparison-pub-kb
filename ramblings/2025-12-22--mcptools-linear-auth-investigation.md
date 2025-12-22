# Issues with mcptools and Linear MCP Server Authentication

## Context

Trying to use [mcptools](https://github.com/f/mcptools) CLI to connect to Linear's MCP server (`https://mcp.linear.app/mcp`) using OAuth credentials stored by Claude CLI.

## Working Setup (Claude CLI)

Claude CLI connects successfully to Linear MCP via:
```bash
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

After OAuth authentication, credentials are stored in `~/.claude/.credentials.json`:
```json
{
  "mcpOAuth": {
    "linear-server|ABCDEF0123456789": {
      "serverName": "linear-server",
      "serverUrl": "https://mcp.linear.app/mcp",
      "clientId": "aBcDeFgH-XyZ012",
      "accessToken": "ABCDEF01-...:FAKE0TOKEN0HERE:xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX",
      "expiresAt": 1767039278431,
      "refreshToken": "...",
      "scope": ""
    }
  }
}
```

## Attempts with mcptools

### Attempt 1: Direct URL with Bearer token
```bash
mcptools tools https://mcp.linear.app/mcp --headers "Authorization=Bearer <token>"
```
**Result:** Error - `--headers` flag not recognized for `tools` command. The command tries to execute the URL as a stdio command.

### Attempt 2: Using alias with URL
```bash
mcptools alias add linear https://mcp.linear.app/mcp
```
Modified `~/.mcpt/aliases.json` to add headers:
```json
{
  "linear": {
    "command": "https://mcp.linear.app/mcp",
    "headers": {
      "Authorization": "Bearer <token>"
    }
  }
}
```
```bash
mcptools tools linear
```
**Result:** `401 Unauthorized` - headers in aliases.json are not being sent

### Attempt 3: Config file approach
Created `~/.mcpt/mcp-config.json`:
```json
{
  "mcpServers": {
    "linear": {
      "url": "https://mcp.linear.app/mcp",
      "headers": {
        "Authorization": "Bearer <token>"
      }
    }
  }
}
```
Then:
```bash
mcptools configs alias mcp-linear ~/.mcpt/mcp-config.json '$.mcpServers'
mcptools configs view mcp-linear
```
**Result:** Config shows correctly with headers, but no clear way to use it with `tools` command.

### Attempt 4: Environment variable
```bash
MCP_HTTP_HEADERS="Authorization=Bearer <token>" mcptools tools https://mcp.linear.app/mcp
```
**Result:** `401 Unauthorized` - env var not working

### Attempt 5: configs set command
According to docs, should work:
```bash
mcp configs set cursor my-api https://api.example.com/mcp --headers "Authorization=Bearer token"
```
But `configs set` requires a config file alias (like "cursor", "vscode", etc.) that doesn't exist on Linux/CLI-only setup.

## Key Issues

1. **`--headers` flag only available in `configs set`**, not in direct `tools`/`call` commands
2. **Headers in aliases.json not being read** when using aliased servers
3. **Config file alias system** seems designed for IDE configs (Cursor, VSCode, etc.), not standalone CLI use
4. **No documented way** to pass Authorization headers when using mcptools directly with HTTP MCP servers

## Linear MCP Server Requirements

Linear MCP server accepts:
- `Authorization: Bearer <token>` header
- Both HTTP and SSE transports
- OAuth 2.1 with dynamic client registration (what Claude CLI uses)

Reference: https://linear.app/docs/mcp

### Attempt 6: configs set with explicit config file
```bash
mcptools configs set mcp-linear linear https://mcp.linear.app/mcp \
  --config ~/.mcpt/mcp-config.json \
  --headers "Authorization=Bearer <token>"
```
**Result:** Successfully stores the config with headers visible in `configs view`:
```
mcp-linear
  linear (sse):
    https://mcp.linear.app/mcp
      Authorization: Bearer <token>
```
BUT trying to use it:
- `mcptools tools mcp-linear:linear` → `executable file not found in $PATH`
- `mcptools shell mcp-linear:linear` → same error

## Root Cause Analysis

**The mcptools `configs` subsystem is designed to:**
1. Read/write config files used by other MCP-aware applications (IDEs)
2. Sync configs between different IDE installations
3. **NOT** to provide a way to use those servers directly in mcptools CLI

**For direct server usage, mcptools expects:**
- `mcp tools <command>` where `<command>` is a stdio-based MCP server
- HTTP URLs are auto-detected, but **no mechanism to pass headers** with them
- The alias system stores a "command" field but ignores "headers" field

## Questions for Alternative Solutions

1. Does mcptools have an undocumented way to pass headers for direct HTTP server use?
2. Are there other MCP CLI tools that support HTTP authentication?
   - `cli-mcp` by zueai?
   - Official MCP inspector?
   - `mcp-cli` (npm)?
3. Can mcptools read Claude CLI's OAuth credentials natively?
4. Is there a proxy approach - run a local stdio server that forwards to HTTP with auth?
5. Should this be filed as a feature request on mcptools GitHub?

## Environment

- OS: Linux (Arch)
- mcptools: installed via `go install` at `~/go/bin/mcptools`
- Claude CLI: v2.0.74+
- Linear MCP endpoint: `https://mcp.linear.app/mcp`
