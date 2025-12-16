# Contributing Guide

Step-by-step instructions for conducting research and maintaining this repository.

## Quick Reference

| Task | Command |
|------|---------|
| Clone all repos | `./scripts/clone-all.sh` |
| Update existing clones | `./scripts/clone-all.sh --update` |
| Validate YAML files | `./scripts/check-yaml.py` |
| Validate strictly | `./scripts/check-yaml.py --strict` |
| Generate tables | `./scripts/generate-tables.py > comparisons/auto-generated.md` |

## Initial Setup

Before beginning research, complete the scope definition:

```bash
# 1. Copy and fill out the scope template
cp SCOPE.md.template SCOPE.md
# Edit SCOPE.md with your research parameters

# 2. Customize the YAML schema
# Edit spec.yaml to add/remove fields for your research

# 3. Commit and tag
git add SCOPE.md spec.yaml
git commit -m "Define research scope: [your title]"
git tag -a scope-defined -m "Research scope defined"
```

## Common Workflows

### 1. Adding a New Project

```bash
# 1. Create YAML file with naming convention: {owner}--{repo}.yaml
touch projects/newowner--newrepo.yaml

# 2. Add required fields (minimum viable entry)
cat > projects/newowner--newrepo.yaml << 'EOF'
last-update: "2025-12-16"
repo-url: "https://github.com/newowner/newrepo"

name: "newrepo"
description: "Brief description of what it does"
EOF

# 3. Clone the repo for analysis
./scripts/clone-all.sh

# 4. Analyze and fill in remaining fields
# See "Analyzing a Repository" section below

# 5. Validate your YAML
./scripts/check-yaml.py projects/newowner--newrepo.yaml

# 6. Regenerate comparison tables
./scripts/generate-tables.py > comparisons/auto-generated.md

# 7. Commit your changes
git add projects/newowner--newrepo.yaml comparisons/auto-generated.md
git commit -m "Add newowner/newrepo to comparison

* Category: {category}
* Stars: {stars}
* Key features: {features}"
```

### 2. Updating an Existing Project

```bash
# 1. Update the clone
./scripts/clone-all.sh --update

# 2. Get current date for last-update field
date +%Y-%m-%d

# 3. Get current commit hash
cd tmp/owner--repo && git rev-parse --short HEAD && cd ../..

# 4. Update the YAML file with new info

# 5. Validate and regenerate tables
./scripts/check-yaml.py
./scripts/generate-tables.py > comparisons/auto-generated.md
```

### 3. Running Discovery

```bash
# 1. Run GitHub searches defined in SCOPE.md
# Document findings in ramblings/

# 2. Create rambling file for discovery session
date +%Y-%m-%d  # Get current date
vim ramblings/$(date +%Y-%m-%d)--discovery-session.md

# 3. For each project found, create a YAML file
# See "Adding a New Project" above
```

### 4. Monthly Maintenance

```bash
# 1. Update all clones
./scripts/clone-all.sh --update

# 2. Refresh star counts (manual or with gh CLI)
for f in projects/*.yaml; do
  url=$(yq '.repo-url' "$f")
  echo "Check: $url"
done

# 3. Update last-commit dates
for dir in tmp/*/; do
  name=$(basename "$dir")
  last=$(cd "$dir" && git log -1 --format='%Y-%m-%d')
  echo "$name: $last"
done

# 4. Regenerate tables
./scripts/generate-tables.py > comparisons/auto-generated.md

# 5. Commit updates
git add projects/ comparisons/
git commit -m "Monthly refresh: update star counts and commit dates"
```

## Analyzing a Repository

### Step 1: Basic Information

```bash
cd tmp/owner--repo

# Get repo info
cat README.md | head -50

# Check language
find . -name "*.py" -o -name "*.ts" -o -name "*.go" | head -20

# Check license
cat LICENSE 2>/dev/null || cat LICENSE.md 2>/dev/null
```

### Step 2: Features & Capabilities

```bash
# Check README for features
grep -i "feature\|support\|capability" README.md

# Check CLI commands (if CLI tool)
grep -r "command\|subcommand\|arg" --include="*.ts" --include="*.py" .

# Check API coverage
grep -ri "api\|endpoint" .
```

### Step 3: Documentation Quality

```bash
# Check for docs
ls -la docs/ README* CONTRIBUTING* 2>/dev/null

# Count examples
ls -la examples/ example/ 2>/dev/null

# Count test files
find . -name "*test*" -o -name "*spec*" | wc -l
```

### Step 4: Security Analysis (if needed)

```bash
# Python: eval/exec
grep -rn "eval(\|exec(\|compile(" --include="*.py" .

# Python: subprocess with shell=True
grep -rn "shell=True\|os.system" --include="*.py" .

# JavaScript/TypeScript: eval
grep -rn "eval(\|Function(" --include="*.js" --include="*.ts" .
```

### Step 5: Fill in YAML

Based on your analysis, update the YAML file with all relevant fields from your `spec.yaml`.

## Git Commit Practices

```bash
# Adding a new project
git commit -m "Add owner/repo to comparison

* Category: cli-client
* Stars: 500
* Key feature: interactive mode"

# Updating existing project
git commit -m "Update owner/repo with latest analysis

* Updated to commit abc1234
* Added new features from v2.0"

# Monthly refresh
git commit -m "Monthly refresh: update star counts

* Updated N projects with current star counts
* Regenerated comparison tables"
```

## Research Notes

Document interesting findings in ramblings/:

```bash
# Get current date
date +%Y-%m-%d

# Create rambling file
vim ramblings/$(date +%Y-%m-%d)--topic-name.md
```

Template:
```markdown
# Topic Name

**Date:** YYYY-MM-DD
**Context:** Why you're writing this

## Findings

Your observations...

## Recommendations

What to do with this information...
```

## Troubleshooting

### YAML Validation Fails

```bash
# Check specific file
./scripts/check-yaml.py projects/problematic-file.yaml

# Common issues:
# - Missing required fields (last-update, repo-url)
# - Invalid date format (must be "YYYY-MM-DD" in quotes)
# - Invalid URL format
# - stars must be integer, not string
```

### Clone Script Fails

```bash
# Try shallow clone
./scripts/clone-all.sh --shallow

# Force update
./scripts/clone-all.sh --update
```

## Related Documents

* [SCOPE.md](SCOPE.md) - Research scope definition
* [PROCESS.md](PROCESS.md) - Research methodology
* [GUIDELINES.md](GUIDELINES.md) - Data collection standards
* [spec.yaml](spec.yaml) - YAML schema
