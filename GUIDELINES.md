# Linear CLI Tools Comparison - Guidelines

## Purpose

This repository catalogs and compares command-line tools for Linear.app, helping developers choose the right tool for their workflow.

## Comparison Dimensions

### 1. Reputation & Trust

* GitHub stars, forks, contributors
* Maintenance status (last commit, open issues)
* Author/organization reputation
* License (open source friendly)

### 2. Feature Comparison

* Core Linear operations (issue CRUD, team/project management)
* Git integration (branch detection, PR creation)
* AI integration (agent compatibility, AI-assisted features)
* Output formats (JSON, table, markdown)
* Interactive vs. scriptable

### 3. Installation & Platform

* Package managers (npm, pip, brew, cargo, go, deno, aur)
* Platform support (Linux, macOS, Windows)
* Binary availability

### 4. Authentication

* Environment variable support
* Configuration file
* Keyring integration
* Setup wizard

### 5. Use Case Fit

* Developer workflow (git-centric)
* AI agent integration
* Team reporting
* Bulk operations

## Data Quality Standards

### Required Fields

Every project YAML must include:

* `last-update` - Date of last update (YYYY-MM-DD)
* `repo-url` - Repository URL
* `name` - Project name
* `description` - Brief description
* `language` - Primary language
* `category` - Primary category

### Recommended Fields

* `stars` - GitHub stars (update monthly)
* `last-commit` - Recent activity indicator
* `installation` - At least one install method
* `features` - Key features boolean map

### Categories

* `cli-client` - Standard CLI for Linear operations
* `tui-client` - Terminal User Interface
* `ai-agent-tool` - Designed for AI integration
* `importer-exporter` - Bulk operations
* `git-workflow` - Git/GitHub focused
* `cross-team` - Multi-team reporting

## File Naming Convention

Project files: `projects/{owner}--{repo}.yaml`

Examples:

* `projects/schpet--linear-cli.yaml`
* `projects/dorkitude--linctl.yaml`
* `projects/markmarkoh--lt.yaml`

For npm-scoped packages: `projects/{scope}--{package}.yaml`

* `projects/anoncam--linear-cli.yaml`
* `projects/minupalaniappan--linear.yaml`

## Updating Data

1. Clone repos periodically: `./scripts/clone-all.sh`
2. Update star counts monthly
3. Regenerate tables: `./scripts/generate-tables.py`
4. Validate: `./scripts/check-yaml.py`

## Comparison Documents

* `comparisons/auto-generated.md` - Script-generated from YAML
* `comparisons/features.md` - Curated feature analysis
* `comparisons/by-language.md` - Grouped by language
* `comparisons/git-integration.md` - Git workflow comparison
