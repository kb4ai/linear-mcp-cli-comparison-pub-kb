# Linearis CLI Limitations - Hands-On Testing Results

**Date:** 2025-12-23
**Tool:** linearis
**Repository:** https://github.com/czottmann/linearis
**Commit:** `3b3ccd18299cfd70c427482aacadf0a65b43e4c4` (2025-12-11)
**Release:** 2025.12.03

## Summary

Based on hands-on testing of the linearis CLI, here are the supported features and current limitations.

## Feature Support Matrix

| Feature                    | Supported | Workaround       |
|----------------------------|-----------|------------------|
| **Issues**                 |           |                  |
| Create/read/update issues  | ✅ Yes    | -                |
| Sub-issues (parent-ticket) | ✅ Yes    | -                |
| Labels                     | ✅ Yes    | -                |
| Status                     | ✅ Yes    | -                |
| Priority                   | ✅ Yes    | -                |
| Assignee                   | ✅ Yes    | -                |
| Projects                   | ✅ Yes    | -                |
| Cycles                     | ✅ Yes    | -                |
| Project milestones         | ✅ Yes    | -                |
| Comments                   | ✅ Yes    | -                |
| **Missing Features**       |           |                  |
| Estimates (story points)   | ❌ No     | WebUI or GraphQL |
| Blocking/blocked by        | ❌ No     | WebUI or GraphQL |
| Related issues             | ❌ No     | WebUI or GraphQL |
| Duplicate marking          | ❌ No     | WebUI or GraphQL |
| Linked GitHub commits      | ❌ No     | WebUI only       |
| Linked GitHub PRs          | ❌ No     | WebUI only       |
| Attachments                | ❌ No     | WebUI or GraphQL |
| Due dates                  | ❌ No     | WebUI or GraphQL |

## Key Observations

### Strengths

* Excellent sub-issue support (parent-ticket relationship)
* Full CRUD for issues with all basic fields
* Good cycle and milestone integration
* Comment support works well

### Critical Missing Features (for our workflows)

1. **Estimates/Story Points** - Cannot set or read story point estimates via CLI
2. **Blocking/Blocked By** - No way to establish issue dependencies
3. **Related Issues** - Cannot link related issues together
4. **Due Dates** - No due date field support

### Workarounds

For missing features, options include:

* **WebUI** - Use Linear's web interface for these operations
* **GraphQL API** - Direct API calls using Linear's GraphQL endpoint
* **Complementary tool** - Use another CLI tool that supports these features

## Impact on AI-Assisted Workflows

When using linearis with AI coding assistants (Claude, Cursor, etc.):

* AI cannot programmatically set estimates when creating issues
* Dependency chains (blocking/blocked-by) must be managed manually
* Sprint planning with story points requires WebUI intervention

## Recommendations

1. For basic issue management: linearis works well
2. For agile workflows with estimates: need WebUI or custom GraphQL scripts
3. For dependency tracking: must use WebUI or find alternative tool
