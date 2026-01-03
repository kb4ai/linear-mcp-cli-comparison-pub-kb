# Subagent Analysis Plan for Linear CLI & MCP Tools Research

**Date:** 2025-12-22
**Context:** Based on initial research into MCP authentication issues with Linear, we need systematic analysis of the tool ecosystem.

## Research Questions

1. What CLI tools exist for interacting with Linear?
2. What MCP servers exist for Linear integration?
3. Which MCP CLI tools support authenticated HTTP endpoints?
4. What proxy/bridge solutions enable mcptools (and similar) to work with authenticated MCP servers?
5. What are the practical workflows for using Linear via CLI/MCP?

## Subagent Strategy

Split research into 5 parallel agents, each producing a structured report. After collection, synthesize findings for decision-making.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PARALLEL ANALYSIS PHASE                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│  │  Agent 1    │  │  Agent 2    │  │  Agent 3    │                │
│  │ Linear CLI  │  │ Linear MCP  │  │ MCP CLI     │                │
│  │   Tools     │  │  Servers    │  │ Auth Tools  │                │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                │
│         │                │                │                        │
│  ┌──────┴──────┐  ┌──────┴──────┐                                 │
│  │  Agent 4    │  │  Agent 5    │                                 │
│  │ Proxy/Bridge│  │ Solution    │                                 │
│  │  Solutions  │  │ Validation  │                                 │
│  └─────────────┘  └─────────────┘                                 │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                     SYNTHESIS PHASE                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Synthesis Agent                           │   │
│  │  * Merge findings from all 5 agents                         │   │
│  │  * Create unified comparison tables                         │   │
│  │  * Produce decision matrix                                  │   │
│  │  * Write recommendations                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Agent Definitions

### Agent 1: Linear CLI Tools

**Purpose:** Find all CLI tools for Linear (official and third-party)

**Search Strategy:**
```
GitHub: "linear cli" OR "linear command line"
GitHub: "linctl" OR "linear-cli"
npm: linear cli
PyPI: linear cli
```

**Data to Collect:**
- Tool name, repo URL, language
- Features (issues, projects, cycles, teams)
- Authentication method (API key, OAuth)
- Installation method
- Activity (stars, last commit)

**Output:** `reports/agent1-linear-cli-tools.md`

### Agent 2: Linear MCP Servers

**Purpose:** Find MCP servers that provide Linear integration

**Search Strategy:**
```
GitHub: "linear mcp server"
GitHub: "mcp server" + "linear.app"
mcpservers.org: Linear
Official: linear.app/docs/mcp
```

**Data to Collect:**
- Server name, repo URL
- Transport support (stdio, HTTP, SSE)
- Authentication (API key, OAuth)
- Tools/capabilities exposed
- Official vs community

**Output:** `reports/agent2-linear-mcp-servers.md`

### Agent 3: MCP CLI Tools with Auth Support

**Purpose:** Find MCP CLI tools that support authenticated HTTP endpoints

**Search Strategy:**
```
GitHub: "mcp cli" + "authorization" OR "bearer"
GitHub: "mcp client" + "http" + "auth"
npm: @modelcontextprotocol
Reference: mcp-as-cli-tools-comparison repo
```

**Data to Collect:**
- Tool name, repo URL
- HTTP/SSE transport support
- Auth header support (how to pass)
- Tested with Linear? (yes/no/unknown)

**Output:** `reports/agent3-mcp-cli-auth-tools.md`

### Agent 4: Proxy/Bridge Solutions

**Purpose:** Find stdio↔HTTP bridges that support authentication

**Search Strategy:**
```
GitHub: "mcp proxy" + "bearer" OR "auth"
GitHub: "stdio http" + "mcp"
npm: mcp-proxy, mcp-bridge
PyPI: mcp-proxy
```

**Data to Collect:**
- Proxy name, repo URL
- Direction: stdio→HTTP, HTTP→stdio, bidirectional
- Auth support: bearer token, OAuth, API key
- Compatibility with mcptools
- Setup complexity

**Output:** `reports/agent4-proxy-bridge-solutions.md`

### Agent 5: Solution Validation

**Purpose:** Practically test top solutions from other agents

**Test Cases:**
1. MCP Inspector CLI with Linear API key
2. mcp-stdio-to-streamable-http-adapter + mcptools
3. mcp-proxy (Python) + mcptools
4. chrishayuk/mcp-cli with Linear
5. Direct curl JSON-RPC

**Data to Collect:**
- Works? (yes/no/partial)
- Setup steps required
- Error messages if failed
- Performance notes
- Recommendation

**Output:** `reports/agent5-solution-validation.md`

## Synthesis Phase

After all agents complete, run synthesis:

1. **Merge YAML data** into projects/ directory
2. **Generate comparison tables** with generate-tables.py
3. **Create decision matrix** based on:
   - Ease of setup
   - Feature completeness
   - Active maintenance
   - Auth support quality
4. **Write recommendations** for different use cases:
   - Quick testing
   - Daily CLI usage
   - Automation/scripting
   - Integration with existing tools

## Execution Commands

```bash
# Run all discovery agents in parallel (background)
claude --task "Agent 1: Linear CLI Tools" --background
claude --task "Agent 2: Linear MCP Servers" --background
claude --task "Agent 3: MCP CLI Auth Tools" --background
claude --task "Agent 4: Proxy/Bridge Solutions" --background

# Wait for reports, then run validation
claude --task "Agent 5: Solution Validation"

# Synthesis
claude --task "Synthesize all agent reports into comparison"
```

## Expected Deliverables

1. `reports/agent1-linear-cli-tools.md`
2. `reports/agent2-linear-mcp-servers.md`
3. `reports/agent3-mcp-cli-auth-tools.md`
4. `reports/agent4-proxy-bridge-solutions.md`
5. `reports/agent5-solution-validation.md`
6. `projects/*.yaml` - YAML files for each discovered tool
7. `comparisons/auto-generated.md` - Generated comparison tables
8. `comparisons/decision-matrix.md` - Recommendations

## Key Insights from Prior Research

From the initial investigation (see other ramblings):

1. **mcptools limitation:** No HTTP auth header support for direct use
2. **Working solutions identified:**
   - MCP Inspector CLI mode
   - mcp-stdio-to-streamable-http-adapter
   - mcp-proxy (Python)
   - Direct API key with Linear
3. **Linear specifics:** Supports both OAuth and API key auth

## Timeline

- **Phase 1 (Parallel):** Agents 1-4 run simultaneously
- **Phase 2 (Sequential):** Agent 5 validates top findings
- **Phase 3 (Synthesis):** Merge and generate outputs
