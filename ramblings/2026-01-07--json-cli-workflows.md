# JSON CLI Workflows: jq, CSV, and Terminal Tables

JSON output from CLI tools like linearis enables powerful command-line workflows without LLM involvement.

## Core Tools

### jq - JSON Processor

The Swiss Army knife for JSON:

```bash
# Install
brew install jq      # macOS
pacman -S jq         # Arch
apt install jq       # Debian/Ubuntu

# Pretty print
linearis issues list | jq '.'

# Extract fields
linearis issues read ABC-123 | jq '.title, .state'

# Filter issues
linearis issues list | jq '.[] | select(.state == "In Progress")'

# Transform to custom format
linearis issues list | jq '.[] | {id: .identifier, title, status: .state}'
```

**jq Docs:** https://jqlang.github.io/jq/

### CSV Conversion with jq

The `@csv` operator properly handles escaping:

```bash
# Basic CSV export
linearis issues list | jq -r '.[] | [.identifier, .title, .state] | @csv'

# With headers
(echo "ID,Title,State"; linearis issues list | jq -r '.[] | [.identifier, .title, .state] | @csv') > issues.csv

# Include more fields
linearis issues list | jq -r '.[] | [.identifier, .title, .state, .priority, .assignee.name // "unassigned"] | @csv'
```

Note: `-r` flag outputs raw strings (no quotes around the whole output).

### Terminal Table Viewers

Pretty tables without leaving the terminal:

**csview** (fast, Rust):

```bash
cargo install csview
# or AUR: csview

linearis issues list | jq -r '.[] | [.identifier, .title, .state] | @csv' | csview
```

**xsv** (CSV toolkit):

```bash
cargo install xsv

linearis issues list | jq -r '...' | xsv table
```

**csvlens** (interactive):

```bash
cargo install csvlens

csvlens issues.csv  # Interactive viewer with search
```

## Practical Pipelines

### Daily Standup View

```bash
# My in-progress issues
linearis issues list --assignee me | jq -r \
  '.[] | select(.state == "In Progress") | [.identifier, .title] | @csv' | csview
```

### Priority Dashboard

```bash
# High priority unassigned
linearis issues list | jq -r \
  '.[] | select(.priority <= 2 and .assignee == null) | [.identifier, .title, .priority] | @csv' | csview
```

### Export for Spreadsheets

```bash
# Full export for team review
linearis issues list | jq -r '
  ["ID","Title","State","Priority","Assignee","Labels"] as $headers |
  ($headers | @csv),
  (.[] | [
    .identifier,
    .title,
    .state,
    .priority,
    (.assignee.name // ""),
    ((.labels // []) | map(.name) | join(";"))
  ] | @csv)
' > team-review.csv
```

### Quick Counts

```bash
# Issues by state
linearis issues list | jq 'group_by(.state) | map({state: .[0].state, count: length})'

# Issues by assignee
linearis issues list | jq 'group_by(.assignee.name) | map({assignee: .[0].assignee.name, count: length})'
```

## Why This Matters

1. **Zero tokens** - Scripts run without LLM
2. **Instant execution** - No API roundtrips to AI
3. **Customizable** - Tailor to YOUR workflow
4. **Composable** - Pipe to other tools (grep, awk, sort)
5. **Scriptable** - Add to cron, git hooks, CI

The LLM generates the jq query once, then it runs forever.

## Tool Links

* **jq:** https://github.com/jqlang/jq
* **csview:** https://github.com/wfxr/csview
* **xsv:** https://github.com/BurntSushi/xsv
* **csvlens:** https://github.com/YS-L/csvlens
