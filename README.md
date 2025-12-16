# Research Comparison Repository

A structured approach to researching and comparing software tools/projects.

## Getting Started

This repository provides a template for conducting systematic research comparisons of software tools. Before beginning research:

1. **Define your scope** by filling out `SCOPE.md.template` and renaming to `SCOPE.md`
2. **Customize the schema** by updating `spec.yaml` with your fields
3. **Commit your scope** to mark the beginning of your research

## Quick Start

```bash
# 1. Define what you're researching
cp SCOPE.md.template SCOPE.md
# Edit SCOPE.md with your research parameters

# 2. Commit and tag your scope
git add SCOPE.md
git commit -m "Define research scope: [your title]"
git tag -a scope-defined -m "Research scope defined"

# 3. Begin discovery (see PROCESS.md)
```

## Repository Structure

```
.
├── README.md                    # This file
├── SCOPE.md.template            # Template to define research scope
├── SCOPE.md                     # Your filled-in scope (after setup)
├── GUIDELINES.md                # Data collection standards
├── PROCESS.md                   # Research methodology
├── CONTRIBUTING.md              # Step-by-step contribution guide
├── spec.yaml                    # YAML schema for project data
├── .gitignore
├── projects/                    # YAML files for each discovered project
│   └── {owner}--{repo}.yaml
├── scripts/
│   ├── clone-all.sh             # Clone all repos to tmp/
│   ├── check-yaml.py            # Validate YAML against schema
│   └── generate-tables.py       # Generate comparison tables
├── comparisons/                 # Generated comparison documents
│   └── auto-generated.md
├── ramblings/                   # Research notes and discoveries
│   └── YYYY-MM-DD--{topic}.md
└── tmp/                         # Cloned repositories (gitignored)
```

## Research Workflow

```
1. Define Scope  →  2. Discover  →  3. Clone  →  4. Analyze  →  5. Compare
   (SCOPE.md)        (search)       (script)     (manual)       (generate)
```

See [PROCESS.md](PROCESS.md) for detailed methodology.

## Documentation

| Document | Purpose |
|----------|---------|
| [SCOPE.md.template](SCOPE.md.template) | Define what you're researching |
| [GUIDELINES.md](GUIDELINES.md) | Data collection standards |
| [PROCESS.md](PROCESS.md) | Research methodology |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Step-by-step workflows |
| [spec.yaml](spec.yaml) | YAML schema specification |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/clone-all.sh` | Clone all tracked repos to `tmp/` |
| `scripts/check-yaml.py` | Validate YAML files against spec |
| `scripts/generate-tables.py` | Generate markdown comparison tables |

## Example Usage

After defining your scope:

```bash
# Run discovery and create YAML files for each project
# (manual or scripted based on your approach)

# Clone all repos for analysis
./scripts/clone-all.sh

# Validate your YAML files
./scripts/check-yaml.py

# Generate comparison tables
./scripts/generate-tables.py > comparisons/auto-generated.md
```

## Template Origin

This research template is based on the structure used in [mcp-as-cli-tools-comparison](../mcp-as-cli-tools-comparison/), adapted for general-purpose tool comparison research.
