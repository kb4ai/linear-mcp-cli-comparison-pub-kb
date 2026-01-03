# Archive: Linearis - A Linear CLI Built for Agents

**Source:** https://zottmann.org/2025/09/03/linearis-my-linear-cli-built.html
**Author:** Carlo Zottmann
**Archived:** 2025-12-22
**Original Date:** 2025-09-03

## Summary

Carlo Zottmann built Linearis, a lightweight Linear CLI tool optimized for LLM agent usage. The key motivation was token efficiency - the official Linear MCP server consumes ~13,000 tokens just to connect, which is significant overhead when working with 100k-200k token context limits.

## Key Insights for Research

### 1. Token Efficiency Problem

> "The official MCP server consumed roughly 13,000 tokens just by connecting"

This is a critical insight for evaluating MCP servers vs CLI tools:

- MCP servers expose many tools, each requiring schema description
- Claude must understand all 20+ tools even if only 3-4 are used
- Token overhead reduces available context for actual work

### 2. CLI vs MCP Trade-offs

| Aspect | MCP Server | Lean CLI (Linearis) |
|--------|------------|---------------------|
| Token overhead | ~13k tokens | Minimal |
| Tool discovery | Automatic | Manual/documentation |
| Shell scriptable | No | Yes (JSON output) |
| Feature scope | Comprehensive (20+ tools) | Focused (core features) |
| Agent integration | Native | Via shell commands |

### 3. Design Principles for Agent-Friendly CLIs

From the author's approach:

1. **JSON output** - Machine-parseable, works with jq
2. **Smart ID resolution** - Accept "ABC-123" format (human-friendly)
3. **Consistent flag structure** - Predictable for agents
4. **Single-command documentation** - `linearis usage` provides context
5. **Focused feature set** - Only what's actually needed

### 4. Author's Workflow

Uses multiple agent tools:
- Claude Code
- sst/opencode
- charmbracelet/crush

This suggests a market for CLI tools optimized for agent use rather than human-first design.

## Tool Details

**Repository:** https://github.com/czottmann/linearis
**Language:** Node.js / TypeScript
**Installation:** npm
**Output:** JSON

### Features

- Create and update tickets
- Add comments and labels
- Search and filter issues
- Manage ticket relationships

### Example Usage

```bash
# Get issue details
linearis issue ABC-123

# Create issue
linearis create --title "Bug fix" --team "Engineering"

# Search
linearis search "authentication"
```

## Implications for Research

1. **Add evaluation metric**: Token overhead per tool/connection
2. **Compare**: CLI token cost vs MCP server token cost
3. **Consider**: Hybrid approaches (CLI for common ops, MCP for discovery)
4. **Document**: Which tools are optimized for agent use

## Quotes

> "I am only using maybe three or four tools out of the 20+ that the Linear MCP server offers."

> "The official MCP server consumed roughly 13,000 tokens just by connecting, representing a significant overhead when working with 100k-200k token context limits"

## Related Projects Mentioned

- Linear MCP Server (official)
- Claude Code
- sst/opencode
- charmbracelet/crush (agent framework)
