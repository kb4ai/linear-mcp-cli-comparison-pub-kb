# clone-all.sh

Clone all repositories listed in `projects/*.yaml` to the `tmp/` directory.

## Requirements

* **bash** - Bourne Again Shell
* **git** - For cloning repositories
* **yq** - YAML processor (install: `brew install yq` or `pip install yq`)

## Usage

```bash
# Clone all repos (skip existing)
./scripts/clone-all.sh

# Shallow clone (faster, less disk space)
./scripts/clone-all.sh --shallow

# Update existing clones
./scripts/clone-all.sh --update

# Show help
./scripts/clone-all.sh --help
```

## Behavior

1. Reads all `projects/*.yaml` files
2. Extracts `repo-url` field from each
3. Clones to `tmp/{owner}--{repo}/` directory
4. Skips repos that already exist (unless `--update`)

## Output Structure

```
tmp/
├── czottmann--linearis/
├── linear--linear-mcp-server/
├── sparfenyuk--mcp-proxy/
└── ...
```

## Options

| Flag | Description |
|------|-------------|
| `--shallow` | Clone with `--depth 1` (faster, saves space) |
| `--update` | Run `git pull` on existing repos |
| `--help` | Show usage information |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (all operations completed) |
| 1 | Partial failure (some repos failed) |

## Summary Output

```
=========================================
Summary:
  Total YAML files:  10
  Cloned:            5
  Updated:           3
  Skipped:           2
  Failed:            0
=========================================
```
