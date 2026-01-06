# Token Efficiency: A Critical Evaluation Metric

**Date:** 2025-12-22
**Source:** [Linearis blog post](https://zottmann.org/2025/09/03/linearis-my-linear-cli-built.html)

## The Insight

Carlo Zottmann's [blog post about building Linearis](https://zottmann.org/2025/09/03/linearis-my-linear-cli-built.html) reveals a critical consideration often overlooked when comparing MCP servers to CLI tools:

> "The official MCP server consumed roughly **13,000 tokens** just by connecting"

For context:
- Claude's context window is 100k-200k tokens
- 13k tokens = 6.5% to 13% of available context just for tool schema
- This overhead exists for EVERY conversation, before any work begins

## Why This Matters

### MCP Server Token Overhead

MCP servers expose tools dynamically. Each tool requires:
1. Tool name and description
2. Input schema (parameters, types, descriptions)
3. Output schema
4. Examples (sometimes)

For a comprehensive server with 20+ tools, this adds up quickly.

### CLI Tool Token Overhead

CLI tools invoked via shell have minimal overhead:
1. Command itself (few tokens)
2. Output parsing (user-controlled)
3. Documentation only when needed (`--help`)

## Evaluation Criteria Update

Based on this insight, add these metrics to project evaluation:

### New Fields for spec.yaml

```yaml
token-efficiency:
  connection-overhead: "number of tokens to initialize"
  per-call-overhead: "tokens per tool invocation"
  tool-count: "number of tools exposed"

agent-optimization:
  json-output: true/false
  single-command-docs: true/false
  predictable-flags: true/false
```

### Comparison Matrix

| Tool Type | Connection Tokens | Per-call Tokens | When Preferred |
|-----------|-------------------|-----------------|----------------|
| MCP Server (full) | ~13k | Medium | Exploration, full API access |
| MCP Server (lite) | ~2-5k | Medium | Balanced approach |
| CLI (JSON) | 0 | Low | Focused operations, scripts |
| CLI (text) | 0 | Medium | Human use, simple queries |

## Recommendation

For agent-focused use cases:

1. **Evaluate token cost** as first-class metric
2. **Prefer focused tools** over comprehensive ones
3. **Consider hybrid approach**: CLI for common ops, MCP for discovery
4. **Document token overhead** in project YAML files

## Implementation

Add to subagent analysis:
- Count tools exposed by each MCP server
- Estimate token overhead (tools × avg schema size)
- Compare focused vs comprehensive tools
- Note which tools are "agent-optimized"

## Quote to Remember

> "I am only using maybe three or four tools out of the 20+ that the Linear MCP server offers."

This is the key insight: most users need a subset of features. Token-efficient alternatives that cover the common 80% use case are valuable.
