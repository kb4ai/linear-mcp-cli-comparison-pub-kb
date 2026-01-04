# Linear API Coverage Overview


*Generated from 56 project files on 2026-01-04*


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

**Tools with `api-coverage` data:** 20/56


## Key API Coverage Gaps


### Issue Relationships (Blocking/Blocked-by)


> **No CLI tool currently supports issue relationships.**


The Linear GraphQL API provides `issueRelationCreate` with these types:

- `blocks` - Issue A blocks Issue B

- `duplicate` - Mark as duplicate

- `related` - Related issues


This is a significant gap for dependency tracking workflows.


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
| [linearator](https://github.com/AdiKsOnDev/linear-cli) | cli-client | 88% | - |
| [linctl](https://github.com/dorkitude/linctl) | ai-agent-tool | 76% | ⭐ 78 |
| [linearis](https://github.com/czottmann/linearis) | cli-client | 76% | - |
| [linear-mcp-server](https://github.com/jerhadf/linear-mcp-server) | linear-mcp-server | 68% | ⭐ 339 |
| [linear-streamable-mcp-server](https://github.com/iceener/linear-streamable-mcp-server) | linear-mcp-server | 68% | ⭐ 45 |
| [linear-cli](https://github.com/rubyists/linear-cli) | cli-client | 68% | ⭐ 7 |
| [Linear Official MCP Server](https://mcp.linear.app) | linear-mcp-server | 68% | - |
| [linear-mcp](https://github.com/cline/linear-mcp) | linear-mcp-server | 48% | ⭐ 121 |
| [linear-mcp-go](https://github.com/geropl/linear-mcp-go) | linear-mcp-server | 48% | ⭐ 11 |
| [linear-mcp-server](https://github.com/cpropster/linear-mcp-server) | linear-mcp-server | 40% | ⭐ 2 |
