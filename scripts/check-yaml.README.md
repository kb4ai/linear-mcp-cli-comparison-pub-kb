# check-yaml.py

Validate YAML files in `projects/` against the schema defined in `spec.yaml`.

## Requirements

* **Python 3.8+**
* **PyYAML** - Install: `pip install pyyaml` or `pip install -r requirements.txt`

## Usage

```bash
# Validate all project YAML files
./scripts/check-yaml.py

# Validate specific file(s)
./scripts/check-yaml.py projects/czottmann--linearis.yaml

# Strict mode (fail on warnings)
./scripts/check-yaml.py --strict

# Show help
./scripts/check-yaml.py --help
```

## Validation Checks

### Required Fields
* `last-update` - Must be present, YYYY-MM-DD format
* `repo-url` - Must be present, valid HTTP(S) URL

### Type Validation
* `stars`, `forks`, `watchers` - Must be integers
* `reputable-source` - Must be boolean
* `last-commit` - Must be YYYY-MM-DD format

### Structure Validation
* `transports` - Must be a dictionary (if present)
* `features` - Must be a list (if present)
* `security` - Must be a dictionary (if present)

## Output

```
[OK] czottmann--linearis.yaml
[FAIL] bad-project.yaml
      ERROR: Missing required field: repo-url
      ERROR: last-update must be YYYY-MM-DD format, got: invalid

Validated 2 files: 1 valid, 1 invalid
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All files valid |
| 1 | One or more files invalid |

## Strict Mode

With `--strict`, warnings become errors:
* Invalid `last-commit` format
* Non-boolean `reputable-source`
* Unknown field types
