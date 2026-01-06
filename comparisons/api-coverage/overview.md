# Linear API Coverage Overview


*Generated from 56 project files on 2026-01-07*


## Summary Statistics


### Tools by Category


| Category | Count |
|----------|-------|
| Linear Mcp Server | 12 |
| Proxy Bridge | 11 |
| Mcp Cli Auth | 9 |
| Cli Client | 9 |
| Linear Cli | 8 |
| Ai Agent Tool | 2 |
| Git Workflow | 2 |
| Cross Team | 1 |
| Importer Exporter | 1 |
| Tui Client | 1 |

**Tools with `api-coverage` data:** 36/56


## Key API Coverage Gaps


### Issue Relationships (Blocking/Blocked-by)


> **[linearis](https://github.com/czottmann/linearis)** is the only CLI with issue relation support (via [workaround script](https://gist.github.com/g-click-trade/3d73f0492abd2e5c75baa863053867dc)).


The Linear GraphQL API provides `issueRelationCreate` with these types:

- `blocks` - Issue A blocks Issue B

- `duplicate` - Mark as duplicate

- `related` - Related issues


Most tools lack this feature - consider linearis + workaround for dependency workflows.


## Resource Coverage Tables


- [Issue Operations](issues.md)
- [Issue Field Support](issue-fields.md)
- [Issue Relationship Operations](relations.md) ⚠️
- [Comment Operations](comments.md)
- [Label Operations](labels.md)
- [Team Operations](teams.md)

## Top Tools by Overall Feature Coverage


| Tool | Category | Coverage | Stars |
|------|----------|----------|-------|
| [linearator](https://github.com/AdiKsOnDev/linear-cli) | cli-client | 86% | - |
| [linearis](https://github.com/czottmann/linearis) | cli-client | 80% | - |
| [linctl](https://github.com/dorkitude/linctl) | ai-agent-tool | 72% | ⭐ 78 |
| [linear-mcp-server](https://github.com/jerhadf/linear-mcp-server) | linear-mcp-server | 36% | ⭐ 339 |
| [linear-streamable-mcp-server](https://github.com/iceener/linear-streamable-mcp-server) | linear-mcp-server | 36% | ⭐ 45 |
| [linear-cli](https://github.com/rubyists/linear-cli) | cli-client | 36% | ⭐ 7 |
| [Linear Official MCP Server](https://mcp.linear.app) | linear-mcp-server | 36% | - |
| [mcp-linear](https://github.com/tacticlaunch/mcp-linear) | linear-mcp-server | 32% | ⭐ 121 |
| [linear-mcp](https://github.com/cline/linear-mcp) | linear-mcp-server | 16% | ⭐ 121 |
| [linear-mcp-go](https://github.com/geropl/linear-mcp-go) | linear-mcp-server | 16% | ⭐ 11 |
