# Linear CLI Tools - Feature Comparison

## Overview

This document provides a curated analysis of features across Linear CLI tools.

## Quick Feature Matrix

| Tool | Git Integration | PR Creation | TUI/Kanban | AI Integration | Cross-Team | Bulk Ops |
|------|-----------------|-------------|------------|----------------|------------|----------|
| schpet/linear-cli | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| linctl | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| lt | ✅* | ❌ | ✅ | ❌ | ❌ | ❌ |
| @anoncam/linear-cli | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| linearator | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| linear-issue-importer | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

*lt copies branch name to clipboard, read-only TUI

---

## Feature Categories

### Git Workflow Integration

Tools that integrate with git for developer workflows:

| Tool | Branch Detection | Branch Creation | PR Creation | Open in Linear |
|------|------------------|-----------------|-------------|----------------|
| **schpet/linear-cli** | ✅ Auto-detects issue from branch | ✅ Creates issue branches | ✅ `gh pr create` integration | ✅ |
| **@minupalaniappan/linear** | ✅ Branch-aware commands | ❌ | ❌ | ✅ |
| **lt** | Copy branch name (`y` key) | ❌ | ❌ | ✅ (`o` key) |

**Best for git workflows:** schpet/linear-cli

### AI Integration

Tools designed for AI agent usage:

| Tool | Agent-Friendly | AI Provider | Features |
|------|----------------|-------------|----------|
| **linctl** | ✅ Purpose-built | - | Structured output, image download, flexible auth |
| **filipjaj/linear-cli** | ❌ | Gemini | AI-powered issue creation |
| **@anoncam/linear-cli** | ❌ | Claude | AI-assisted label management |

**Best for AI agents:** linctl

### Terminal UI

Tools with rich terminal interfaces:

| Tool | Type | Features |
|------|------|----------|
| **lt** | TUI (read-only) | Issue browser, view switcher, search, clipboard integration |
| **@anoncam/linear-cli** | Kanban view | `-k` flag for kanban board visualization |

**Best for TUI:** lt (for viewing), @anoncam/linear-cli (for kanban)

### Bulk Operations

Tools for batch import/export:

| Tool | Import | Export | Formats |
|------|--------|--------|---------|
| **linear-issue-importer** | ✅ | ✅ | JSON, CSV |
| **linearator** | ✅ | ✅ | Various |

**Best for bulk ops:** linear-issue-importer

### Cross-Team Analysis

| Tool | Multi-Team Queries | Reports |
|------|-------------------|---------|
| **@anoncam/linear-cli** | ✅ | Markdown reports |

**Best for cross-team:** @anoncam/linear-cli

---

## Unique Capabilities

### schpet/linear-cli

* `linear issue start ABC-123` - Creates branch, marks issue as started
* `linear issue pr` - Creates GitHub PR with Linear issue details pre-filled
* Context-aware: opens right Linear view based on current branch

### linctl

* Purpose-built for AI agents (Claude Code, Cursor, Amp)
* Authenticated image downloads from issues
* Multiple credential storage options (keyring, encrypted file, JSON)

### lt

* Beautiful Rust TUI optimized for modern terminals
* View switcher for custom Linear views
* Press `y` to copy branch name, `o` to open in Linear
* Requires Nerdfont and modern terminal (kitty, Ghostty, iTerm2)

### @anoncam/linear-cli

* Terminal kanban board visualization (`-k` flag)
* Cross-team queries and filtering
* AI-assisted label management with Claude
* Direct GraphQL API integration

---

## Decision Guide

| Use Case | Recommended Tool |
|----------|------------------|
| Git-centric development workflow | schpet/linear-cli |
| AI agent integration | linctl |
| Viewing issues in terminal | lt |
| Cross-team reporting | @anoncam/linear-cli |
| Bulk import/export | linear-issue-importer |
| Arch Linux user | linearator (AUR) |
| Python ecosystem | linearator or pylinear |
| Rust ecosystem | lt or linear-issue-importer |
| Go ecosystem | linctl |
