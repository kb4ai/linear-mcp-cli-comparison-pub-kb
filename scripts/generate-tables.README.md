# generate-tables.py

Generate comparison tables from `projects/*.yaml` files.

## Requirements

* **Python 3.8+**
* **PyYAML** - Install: `pip install pyyaml` or `pip install -r requirements.txt`

## Usage

```bash
# Generate all tables (default)
./scripts/generate-tables.py

# Save to file
./scripts/generate-tables.py > comparisons/auto-generated.md

# Specific views
./scripts/generate-tables.py --by-category
./scripts/generate-tables.py --by-transport
./scripts/generate-tables.py --by-stars
./scripts/generate-tables.py --reputable-only

# JSON output
./scripts/generate-tables.py --json
```

## Output Sections

### Summary Statistics
```markdown
## Summary Statistics

- **Total projects:** 10
- **Reputable sources:** 3
- **Combined stars:** 5,000 (from 8 projects with star data)

### By Category
- linear-cli: 4
- mcp-cli-auth: 3
- proxy-bridge: 3
```

### Overview Table (sorted by stars)
| Project | Stars | Language | Category | Description |
|---------|------:|----------|----------|-------------|
| [linearis](url) | 500 | TypeScript | linear-cli | Lightweight Linear CLI... |

### Reputable Sources Table
| Project | Organization | Category | Description |
|---------|--------------|----------|-------------|
| [linear-mcp-server](url) | Linear | official | Official MCP server... |

### Transport Support Matrix
| Project | stdio | SSE | HTTP | WebSocket |
|---------|:-----:|:---:|:----:|:---------:|
| linearis | ✓ |  | ✓ |  |

### By Category (with --by-category)
Grouped tables for each category.

## Flags

| Flag | Description |
|------|-------------|
| `--by-category` | Group projects by category |
| `--by-transport` | Show transport support matrix |
| `--by-stars` | Sort by star count (default) |
| `--reputable-only` | Only show reputable sources |
| `--json` | Output as JSON instead of markdown |
| `--help` | Show usage information |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (e.g., no projects found) |
