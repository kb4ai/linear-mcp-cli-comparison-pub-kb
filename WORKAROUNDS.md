# Linear CLI Tools - Workarounds and Limitations

This document tracks known limitations in Linear CLI tools and workarounds for missing features.

## Linearis (czottmann/linearis)

### Missing Features (Tested 2025-12-23)

| Feature | Status | Workaround |
|---------|--------|------------|
| Estimates (story points) | Not supported | Python/GraphQL script |
| Blocking/Blocked-by relations | Not supported | Python/GraphQL script |
| Related issues linking | Not supported | Python/GraphQL script |
| Due dates | Not supported | Python/GraphQL script |
| Attachments | Not supported | Direct API |
| Duplicate marking | Not supported | Direct API |

### Python Workaround Scripts

A community-maintained gist provides Python scripts for missing features:

**Gist:** https://gist.github.com/g-click-trade/3d73f0492abd2e5c75baa863053867dc

Features covered:

* Get/set estimates (story points)
* Get/set assignee
* Add/remove issue relations (blocking, blocked_by, related, duplicate)

### Feature Request Issues

Track progress on official support:

* [#26 - Estimates support](https://github.com/czottmann/linearis/issues/26)
* [#27 - Blocking/blocked-by relations](https://github.com/czottmann/linearis/issues/27)
* [#28 - Attachments](https://github.com/czottmann/linearis/issues/28)
* [#29 - Due dates](https://github.com/czottmann/linearis/issues/29)
* [#30 - Assignee read](https://github.com/czottmann/linearis/issues/30)
* [#31 - Raw GraphQL support](https://github.com/czottmann/linearis/issues/31)

---

## schpet/linear-cli

### Limitations

| Feature | Status | Notes |
|---------|--------|-------|
| Estimates | Read-only | Displayed in queries, cannot set |
| Sub-issues | Partial | `--parent` flag exists, reads parent info |
| Blocking relations | Not supported | [Feature request #26](https://github.com/schpet/linear-cli/issues/26) |
| Due dates | Not supported | - |
| Related issues | Not supported | - |

---

## linctl (dorkitude/linctl)

### Supported Advanced Features

| Feature | Status | Notes |
|---------|--------|-------|
| Sub-issues | Full support | `--parent` flag (PR #24) |
| Due dates | Supported | `--due-date YYYY-MM-DD` |
| Estimates | Not exposed | - |
| Blocking relations | Not supported | - |

---

## General Workaround: Direct GraphQL API

For features not supported by CLI tools, you can use the Linear GraphQL API directly:

```bash
# Example: Set estimate on an issue
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { issueUpdate(id: \"ISSUE_ID\", input: { estimate: 3 }) { success } }"
  }'
```

See Linear API docs: https://developers.linear.app/docs/graphql/working-with-the-graphql-api

---

## Contributing Workarounds

If you have scripts or workarounds for CLI tool limitations:

1. Add them to this document
2. Link to gists or external resources
3. Document which tool version was tested
