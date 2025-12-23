# Linear CLI Tools - Git Integration Comparison

## Overview

Many developers use Linear with git-based workflows. This document compares how different CLI tools integrate with git and GitHub.

---

## Git Integration Matrix

| Tool | Branch Detection | Branch Creation | PR Creation | Open in Linear | Clipboard |
|------|------------------|-----------------|-------------|----------------|-----------|
| **schpet/linear-cli** | ✅ Auto from branch name | ✅ `issue start` | ✅ `issue pr` | ✅ `issue view` | ❌ |
| **@minupalaniappan/linear** | ✅ `linear branch` | ❌ | ❌ | ✅ `linear open` | ❌ |
| **lt** | ❌ | ❌ | ❌ | ✅ `o` key | ✅ `y` key |
| **linctl** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Others** | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## Detailed Comparison

### schpet/linear-cli (Best Git Integration)

**Branch Detection:**

```bash
# On branch feat/ABC-123-add-feature
linear issue view  # Automatically shows ABC-123
```

**Branch Creation + Status Update:**

```bash
# Interactive: select issue, create branch, mark as started
linear issue start

# Direct: specify issue ID
linear issue start ABC-123
# Creates branch: abc-123-issue-title
# Sets issue status to "In Progress"
```

**GitHub PR Creation:**

```bash
linear issue pr
# Runs: gh pr create
# Pre-fills title and body from Linear issue
```

**Workflow Example:**

```bash
linear issue list              # See your issues
linear issue start ABC-123     # Create branch, mark started
# ... make changes ...
git add . && git commit -m "feat: implement feature"
linear issue pr                # Create PR with Linear details
```

### @minupalaniappan/linear (Branch-Aware)

**Branch Context Commands:**

```bash
# On branch feat/ABC-123-add-feature
linear branch    # Show ticket info for current branch
linear team      # Show team info for current branch's ticket
linear open      # Open current branch's ticket in Linear
linear new       # Create sub-issue from current branch
```

**Setup:**

```bash
linear key      # Set API key
linear me       # Verify account
```

### lt (TUI with Clipboard)

**Keyboard Shortcuts:**

* `y` - Copy git branch name to clipboard
* `o` - Open issue in Linear (desktop/web)
* `/` - Search issues
* `/` + Tab - Switch views

**Branch Name Format:**
Copies branch name suitable for git checkout.

---

## Branch Naming Conventions

Tools expect Linear issue IDs in branch names:

| Pattern | Example |
|---------|---------|
| `{ID}-{description}` | `ABC-123-add-feature` |
| `feat/{ID}-{description}` | `feat/ABC-123-add-feature` |
| `{type}/{ID}-{description}` | `fix/ABC-123-bug-fix` |

---

## Workflow Recommendations

### For Solo Developers

```bash
# Use schpet/linear-cli for complete workflow
linear issue start ABC-123
# code...
linear issue pr
```

### For Teams with Existing Conventions

```bash
# Use @minupalaniappan/linear for branch-aware queries
linear branch   # Check current ticket
linear open     # Quick access to Linear
```

### For Quick Issue Viewing

```bash
# Use lt for beautiful TUI browsing
lt
# y to copy branch name
# o to open in browser
```

---

## GitHub CLI Integration

**schpet/linear-cli** integrates with GitHub CLI (`gh`):

```bash
# Prerequisites
brew install gh
gh auth login

# Then use
linear issue pr  # Calls gh pr create internally
```

---

## Comparison Summary

| Need | Best Tool |
|------|-----------|
| Full git workflow (branch + PR) | schpet/linear-cli |
| Branch-aware commands | @minupalaniappan/linear |
| Copy branch name quickly | lt |
| View issues without git context | Any tool |
