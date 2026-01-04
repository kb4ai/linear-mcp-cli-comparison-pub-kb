# Issue Field Support Coverage

*Which issue fields can be set via create/update*

*Generated from 56 project files on 2026-01-04*


## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Full support |
| ⚠️ | Partial support |
| 👁️ | Read-only |
| ❌ | Not supported |
| ❓ | Unknown / Not tested |


---

## Cli Client


| Tool | parentId (sub-issues) | estimate | dueDate | priority | stateId (status) | assigneeId | cycleId | projectId | Coverage |
|------|----|----|----|----|----|----|----|----|----------|
| [linearator](https://github.com/AdiKsOnDev/linear-cli) | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 93% |
| [linearis](https://github.com/czottmann/linearis) | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | 75% |

## Tui Client


| Tool | parentId (sub-issues) | estimate | dueDate | priority | stateId (status) | assigneeId | cycleId | projectId | Coverage |
|------|----|----|----|----|----|----|----|----|----------|
| [lt](https://github.com/markmarkoh/lt) | 👁️ | 👁️ | 👁️ | 👁️ | 👁️ | 👁️ | 👁️ | 👁️ | 50% |

## Git Workflow


| Tool | parentId (sub-issues) | estimate | dueDate | priority | stateId (status) | assigneeId | cycleId | projectId | Coverage |
|------|----|----|----|----|----|----|----|----|----------|
| [linear-cli](https://github.com/schpet/linear-cli) | ❌ | 👁️ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | 68% |
| [@minupalaniappan/linear](https://github.com/minupalaniappan/linear-cli) | ⚠️ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | 18% |

## Ai Agent Tool


| Tool | parentId (sub-issues) | estimate | dueDate | priority | stateId (status) | assigneeId | cycleId | projectId | Coverage |
|------|----|----|----|----|----|----|----|----|----------|
| [linctl](https://github.com/dorkitude/linctl) | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 87% |

## Cross Team


| Tool | parentId (sub-issues) | estimate | dueDate | priority | stateId (status) | assigneeId | cycleId | projectId | Coverage |
|------|----|----|----|----|----|----|----|----|----------|
| [@anoncam/linear-cli](https://www.npmjs.com/package/@anoncam/linear-cli) | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | 50% |

## Importer Exporter


| Tool | parentId (sub-issues) | estimate | dueDate | priority | stateId (status) | assigneeId | cycleId | projectId | Coverage |
|------|----|----|----|----|----|----|----|----|----------|
| [linear-issue-importer](https://crates.io/crates/linear-issue-importer) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |

---


## Gap Analysis


### Best Coverage


1. [linear-issue-importer](https://crates.io/crates/linear-issue-importer) - 100%
2. [linearator](https://github.com/AdiKsOnDev/linear-cli) - 93%
3. [linctl](https://github.com/dorkitude/linctl) - 87%
4. [linearis](https://github.com/czottmann/linearis) - 75%
5. [linear-cli](https://github.com/schpet/linear-cli) - 68%