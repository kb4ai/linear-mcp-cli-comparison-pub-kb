# Linear CLI Tools - By Language

## Overview

Linear CLI tools are available in multiple programming languages. This document groups them by language for developers who prefer tools in their ecosystem.

---

## TypeScript / JavaScript / Deno

### schpet/linear-cli

* **Runtime:** Deno
* **Install:** `brew install schpet/tap/linear` or `deno install jsr:@schpet/linear-cli`
* **Focus:** Git workflow integration
* **Highlights:** Best git/GitHub integration, PR creation, branch management

### @anoncam/linear-cli

* **Runtime:** Node.js
* **Install:** `npm i -g @anoncam/linear-cli`
* **Focus:** Cross-team reporting
* **Highlights:** Kanban view, AI labels, GraphQL integration

### @minupalaniappan/linear

* **Runtime:** Node.js
* **Install:** `npm i -g @minupalaniappan/linear`
* **Focus:** Branch-aware commands
* **Highlights:** Simple, branch-context commands

### @digitalstories/linear-cli

* **Runtime:** Node.js
* **Install:** `npm i -g @digitalstories/linear-cli`
* **Focus:** Basic CLI
* **Highlights:** French language support

### linearis

* **Runtime:** Deno
* **Install:** `deno install jsr:@czottmann/linearis`
* **Focus:** LLM-optimized CLI
* **Highlights:** Minimal token output for AI agents, JSON-first, [workaround scripts](https://gist.github.com/g-click-trade/3d73f0492abd2e5c75baa863053867dc) for estimates/relations
* **Blog:** [Token efficiency analysis](https://zottmann.org/2025/09/03/linearis-my-linear-cli-built.html)

---

## Go

### linctl

* **Install:** `go install github.com/dorkitude/linctl@latest`
* **Focus:** AI agent integration
* **Highlights:** Purpose-built for AI agents, flexible auth, image download

### carlosflorencio/linear-cli

* **Install:** `go install github.com/carlosflorencio/linear-cli@latest`
* **Focus:** Basic CLI
* **Highlights:** Simple and lightweight

### filipjaj/linear-cli

* **Install:** `go install github.com/filipjaj/linear-cli@latest`
* **Focus:** AI-powered
* **Highlights:** Gemini AI for issue creation

---

## Python

### linearator

* **Install:** `pip install linearator` or AUR `linear-cli`
* **Focus:** Comprehensive CLI
* **Highlights:** Available on AUR, bulk operations

### pylinear

* **Install:** `pip install pylinear`
* **Focus:** Basic CLI
* **Highlights:** Built with Click framework

### linear-app-cli

* **Install:** `pip install linear-app-cli`
* **Focus:** Basic CLI
* **Highlights:** Simple Linear API wrapper

---

## Rust

### lt

* **Install:** `brew tap markmarkoh/lt && brew install lt` or `cargo install lt`
* **Focus:** Terminal UI
* **Highlights:** Beautiful TUI, view switcher, clipboard integration

### linear-issue-importer

* **Install:** `cargo install linear-issue-importer`
* **Focus:** Bulk operations
* **Highlights:** JSON/CSV import/export

### eriksandfort/linear_cli

* **Install:** `cargo install linear_cli`
* **Focus:** Basic CLI
* **Highlights:** Rust implementation

### max-muoto/linear-cli

* **Install:** `cargo install linear-cli`
* **Focus:** Basic CLI
* **Highlights:** Rust implementation

---

## Ruby

### rubyists/linear-cli

* **Install:** Binary release
* **Focus:** Basic CLI
* **Highlights:** For Ruby developers

---

## Language Statistics

| Language | Count | Notable Tools |
|----------|-------|---------------|
| JavaScript/TypeScript | 5 | schpet/linear-cli, @anoncam/linear-cli, linearis |
| Rust | 4 | lt, linear-issue-importer |
| Go | 3 | linctl |
| Python | 3 | linearator |
| Ruby | 1 | rubyists/linear-cli |

---

## Recommendations by Ecosystem

| Your Stack | Recommended Tool | Why |
|------------|------------------|-----|
| TypeScript/Deno | schpet/linear-cli | Native ecosystem, great git integration |
| Node.js | @anoncam/linear-cli | Rich features, kanban view |
| Go | linctl | AI-friendly, comprehensive |
| Python | linearator | AUR support, comprehensive |
| Rust | lt | Beautiful TUI |
| Any (binary) | linctl | Pre-built binaries available |
