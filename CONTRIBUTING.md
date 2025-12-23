# Contributing to Linear CLI Tools Comparison

## Adding a New Tool

### 1. Create Project YAML

Create a new file in `projects/` following the naming convention:

```
projects/{owner}--{repo}.yaml
```

### 2. Minimum Required Fields

```yaml
last-update: "2025-12-22"
repo-url: "https://github.com/owner/repo"

name: "tool-name"
description: "Brief description"
language: "Python"
category: "cli-client"
```

### 3. Recommended Fields

```yaml
stars: 100
last-commit: "2025-12-20"

features:
  git-integration: true
  issue-creation: true
  issue-view: true

installation:
  pip: "package-name"
  # or npm, brew, cargo, go-install, deno, aur

authentication:
  env-var: "LINEAR_API_KEY"

platforms:
  linux: true
  macos: true
  windows: false
```

### 4. Validate

```bash
./scripts/check-yaml.py projects/owner--repo.yaml
```

### 5. Regenerate Tables

```bash
./scripts/generate-tables.py > comparisons/auto-generated.md
```

### 6. Commit

```bash
git add projects/owner--repo.yaml comparisons/auto-generated.md
git commit -m "Add owner/repo to Linear CLI comparison"
```

---

## Updating Existing Tools

### Refresh Star Counts

```bash
# Update stars from GitHub API (requires gh cli)
./scripts/update-stars.sh
```

### Update Last Commit Date

Check the repository and update `last-commit` field.

### Add New Features

If a tool adds new features, update the `features` section.

---

## Monthly Maintenance

1. **Update clones**

   ```bash
   ./scripts/clone-all.sh --update
   ```

2. **Refresh metrics**

   * Star counts
   * Last commit dates
   * Open issues

3. **Regenerate tables**

   ```bash
   ./scripts/generate-tables.py > comparisons/auto-generated.md
   ```

4. **Commit**

   ```bash
   git commit -am "Monthly refresh: update metrics YYYY-MM"
   ```

---

## Writing Comparison Documents

### Location

Comparison documents go in `comparisons/`:

* `features.md` - Feature matrix
* `by-language.md` - Language grouping
* `git-integration.md` - Git workflow comparison

### Format

Use tables for comparison matrices:

```markdown
| Tool | Feature A | Feature B | Feature C |
|------|-----------|-----------|-----------|
| tool1 | ✅ | ❌ | ✅ |
| tool2 | ✅ | ✅ | ❌ |
```

### Keep Curated vs Auto-Generated Separate

* `auto-generated.md` - Script output, regenerated
* Other files - Hand-curated analysis

---

## Research Notes

Put exploratory notes in `ramblings/`:

```
ramblings/YYYY-MM-DD--topic.md
```

Always check current date:

```bash
date +%Y-%m-%d
```
