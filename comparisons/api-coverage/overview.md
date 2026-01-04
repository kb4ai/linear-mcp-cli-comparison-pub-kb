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

**Tools with `api-coverage` data:** 4/56


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
| [linear-cli](https://github.com/rubyists/linear-cli) | cli-client | 8% | ⭐ 7 |
| [linear-cli](https://github.com/carlosflorencio/linear-cli) | cli-client | 8% | - |
| [@digitalstories/linear-cli](https://www.npmjs.com/package/@digitalstories/linear-cli) | cli-client | 8% | - |
| [linear_cli](https://github.com/eriksandfort/linear_cli) | cli-client | 8% | - |
| [pylinear](https://github.com/hxghhhh/pylinear) | cli-client | 8% | - |
| [linear-app-cli](https://www.piwheels.org/project/linear-app-cli/) | cli-client | 8% | - |
| [linear-cli](https://github.com/max-muoto/linear-cli) | cli-client | 8% | - |
