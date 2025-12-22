# Quick Start

Get up and running with this repository in under 5 minutes.

## Prerequisites

* **Python 3.8+**
* **yq** (YAML processor for shell scripts)
* **git**

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install yq

```bash
# macOS
brew install yq

# Arch Linux
pacman -S yq

# Debian/Ubuntu
apt install yq

# pip (alternative)
pip install yq
```

### 3. Verify Installation

```bash
# Run the setup script to check everything
./scripts/setup.sh
```

## First Run

### Validate Existing Data

```bash
# Check all YAML files are valid
./scripts/check-yaml.py

# Strict mode (warnings become errors)
./scripts/check-yaml.py --strict
```

### Generate Comparison Tables

```bash
# Generate all tables
./scripts/generate-tables.py > comparisons/auto-generated.md

# With category grouping
./scripts/generate-tables.py --by-category > comparisons/auto-generated.md

# With transport matrix
./scripts/generate-tables.py --by-transport

# JSON output
./scripts/generate-tables.py --json
```

### Clone Tracked Repositories

```bash
# Clone all tracked repos to tmp/
./scripts/clone-all.sh

# Shallow clone (faster)
./scripts/clone-all.sh --shallow

# Update existing clones
./scripts/clone-all.sh --update
```

## Adding a New Project

1. Create a YAML file in `projects/`:

```bash
# Naming convention: {owner}--{repo}.yaml
touch projects/owner--repo-name.yaml
```

2. Add required fields (see [spec.yaml](spec.yaml)):

```yaml
last-update: "2024-12-22"
repo-url: "https://github.com/owner/repo"
name: "repo-name"
description: "One-line description"
language: "TypeScript"
category: "linear-cli"  # or linear-mcp-server, mcp-cli-auth, proxy-bridge
```

3. Validate:

```bash
./scripts/check-yaml.py projects/owner--repo-name.yaml
```

4. Regenerate tables:

```bash
./scripts/generate-tables.py > comparisons/auto-generated.md
```

## Directory Structure

```
.
├── projects/           # YAML files for each tool (45 files)
├── comparisons/        # Generated comparison tables
├── reports/            # Research reports
├── archive/            # Archived web research
├── ramblings/          # Research notes
├── scripts/            # Utility scripts
│   ├── check-yaml.py   # YAML validation
│   ├── generate-tables.py  # Table generation
│   └── clone-all.sh    # Repository cloning
├── spec.yaml           # YAML schema definition
└── requirements.txt    # Python dependencies
```

## Common Tasks

| Task | Command |
|------|---------|
| Validate all YAML | `./scripts/check-yaml.py` |
| Generate tables | `./scripts/generate-tables.py > comparisons/auto-generated.md` |
| Clone all repos | `./scripts/clone-all.sh --shallow` |
| Check single file | `./scripts/check-yaml.py projects/file.yaml` |
| JSON output | `./scripts/generate-tables.py --json` |

## Next Steps

* Read [SCOPE.md](SCOPE.md) to understand research goals
* Review [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
* Check [comparisons/auto-generated.md](comparisons/auto-generated.md) for current data
