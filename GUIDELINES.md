# Research Guidelines

This document establishes standards for data collection and project comparison.

> **Prerequisites**: Complete [SCOPE.md](SCOPE.md) before beginning research.

## Repository Structure

```
.
├── README.md                    # Overview and quick start
├── SCOPE.md                     # Research scope definition
├── GUIDELINES.md                # This file - standards
├── PROCESS.md                   # Research methodology
├── CONTRIBUTING.md              # Step-by-step workflows
├── spec.yaml                    # YAML schema
├── projects/                    # Project YAML files
│   └── {owner}--{repo}.yaml
├── scripts/                     # Utility scripts
├── comparisons/                 # Generated tables
└── ramblings/                   # Research notes
```

## Data Collection Standards

### YAML File Requirements

1. **File naming**: `projects/{repo-owner}--{repo-name}.yaml`
   * Use double-dash to separate owner from repo name
   * Example: `linear--linear.yaml`, `acme--linear-cli.yaml`

2. **Required fields** (must be first):
   * `last-update`: YYYY-MM-DD format (when you analyzed it)
   * `repo-url`: Full GitHub/GitLab URL

3. **Optional fields**: Defined in your `spec.yaml`

4. **Field ordering**: Tracking fields first, then grouped by category

### Example YAML Structure

```yaml
last-update: "2025-12-16"
repo-commit: "abc123def"
repo-url: "https://github.com/owner/repo"

name: "Project Name"
description: "What it does"
language: "TypeScript"
stars: 1234
license: "MIT"

category: "cli-client"
reputable-source: false

features:
  - "Feature 1"
  - "Feature 2"

# Add custom fields based on your SCOPE.md
```

## Comparison Dimensions

### 1. Reputation & Trust

* GitHub stars, forks, contributors
* Organization/author reputation
* Maintenance status (last commit, open issues)
* Whether from official source

### 2. Feature Comparison

* Core functionality coverage
* Platform support
* API coverage
* Documentation quality

### 3. Security Properties (if applicable)

* Code execution patterns (eval, exec)
* Network isolation
* Input validation
* Subprocess handling

## Script Conventions

1. Scripts in `scripts/` should be executable:
   ```python
   #!/usr/bin/env python3
   ```

2. Scripts should work with the `projects/*.yaml` structure

3. Output should be markdown-compatible

## Git Commit Practices

* Small, focused commits with clear messages
* Present tense imperative mood
* Include attribution footer for AI-assisted work

Example:
```
Add owner/repo to comparison

* Category: cli-client
* Stars: 500
* Key features: interactive mode, batch operations
```

## Updating Information

1. Update `last-update` field when modifying a project YAML
2. Update `repo-commit` if analysis was based on specific commit
3. Document findings in `ramblings/`
4. Re-run `check-yaml.py` after changes
5. Regenerate tables: `./scripts/generate-tables.py > comparisons/auto-generated.md`

## Related Documents

* [SCOPE.md](SCOPE.md) - Your research scope definition
* [CONTRIBUTING.md](CONTRIBUTING.md) - Step-by-step contribution workflows
* [PROCESS.md](PROCESS.md) - Research methodology
* [spec.yaml](spec.yaml) - Full YAML schema specification
