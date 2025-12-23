# Linear CLI Tools Comparison - Research Process

## Discovery Methodology

### 1. Initial Research Sources

* GitHub search: `linear cli`, `linear-cli`, `linear app cli`
* npm search: `linear-cli`, `@*/linear`
* PyPI search: `linear`, `linearator`
* crates.io: `linear`
* AUR: `linear`
* Reddit: r/Linear, r/commandline
* Perplexity/web search for curated lists

### 2. Evaluation Criteria

Each tool is evaluated on:

1. **Existence & Accessibility**
   * Repository is public
   * Code is available
   * Some form of documentation exists

2. **Maintenance Status**
   * Last commit within 12 months (active)
   * Responds to issues (maintained)
   * Clear development trajectory

3. **Functionality**
   * Core Linear API coverage
   * Unique features or focus area
   * Quality of implementation

4. **Installation**
   * Published to package registry (npm, PyPI, crates.io, etc.)
   * Homebrew formula available
   * Binary releases

### 3. Data Collection Process

1. **Clone Repository**

   ```bash
   ./scripts/clone-all.sh
   ```

2. **Analyze README**
   * Extract description, features, installation
   * Note unique capabilities

3. **Examine Code**
   * Identify language, dependencies
   * Check authentication methods
   * Note API integration approach

4. **Check Package Registries**
   * npm: `npm info @scope/package`
   * PyPI: `pip show package`
   * crates.io: `cargo search package`

5. **Capture Metrics**
   * GitHub stars, forks, contributors
   * Last commit date
   * Open issues count

### 4. Update Schedule

* **Weekly**: Check for new tools, major updates
* **Monthly**: Refresh star counts, last-commit dates
* **Quarterly**: Full review of all entries

## Tool Categories

### Primary Categories

| Category | Description | Example |
|----------|-------------|---------|
| `cli-client` | Standard CLI interface | linearator |
| `tui-client` | Terminal UI application | lt |
| `ai-agent-tool` | AI agent integration | linctl |
| `git-workflow` | Git-centric workflow | schpet/linear-cli |
| `cross-team` | Multi-team reporting | @anoncam/linear-cli |
| `importer-exporter` | Bulk operations | linear-issue-importer |

### Feature Tags

* `git-integration` - Detects Linear issue from branch
* `github-pr-creation` - Creates PRs with Linear details
* `kanban-view` - Terminal kanban board
* `ai-integration` - AI-assisted features
* `bulk-operations` - Batch import/export
* `mcp-server` - MCP protocol support

## Research Notes Location

Exploratory findings and discoveries go in `ramblings/`:

```
ramblings/YYYY-MM-DD--topic-description.md
```

Examples:

* `2025-12-22--initial-research-perplexity.md`
* `2025-12-22--git-integration-comparison.md`
