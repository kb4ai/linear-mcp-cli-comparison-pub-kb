# Archive Directory

This directory contains properly attributed archives of external specifications and documentation relevant to the Linear MCP/CLI comparison research project.

## Archive Organization

Each archived resource follows a consistent file naming pattern:

* `YYYY-MM-DD--{descriptive-name}.md` - Clean markdown version
* `YYYY-MM-DD--{descriptive-name}.url` - Source URL (single line)
* `YYYY-MM-DD--{descriptive-name}.meta.json` - Metadata including URL, timestamp, extraction method
* `YYYY-MM-DD--{descriptive-name}.{format}` - Original format files (e.g., .graphql, .pdf)
* `YYYY-MM-DD--{descriptive-name}.repo.json` - Repository source information (for git-hosted files)

## Current Archives

### 2026-01-04: Linear GraphQL API Documentation

**Linear GraphQL Schema** (`2026-01-04--linear-graphql-schema.*`)

* Source: https://github.com/linear/linear/blob/master/packages/sdk/src/schema.graphql
* Format: GraphQL schema definition (37,827 lines)
* Description: Complete Linear GraphQL API schema including all types, queries, mutations, and subscriptions
* Files: .graphql, .url, .meta.json, .repo.json

**Linear GraphQL API Getting Started Guide** (`2026-01-04--linear-graphql-api-getting-started.*`)

* Source: https://linear.app/developers/graphql
* Format: Markdown documentation
* Description: Comprehensive tutorial covering authentication (OAuth 2.0, API keys), queries, mutations, and best practices
* Files: .md, .url, .meta.json

**Linear GraphQL API Overview** (`2026-01-04--linear-graphql-api-overview.*`)

* Source: https://linear.app/developers
* Format: Markdown documentation
* Description: High-level overview of API features including pagination, filtering, and rate limits
* Rate Limits: 1500/500/60 requests per hour, 250k complexity points per hour
* Files: .md, .url, .meta.json

### 2026-01-04: Linear MCP Server Documentation

**Linear MCP Server Documentation** (`2026-01-04--linear-mcp-server-documentation.*`)

* Source: https://linear.app/docs/mcp
* Format: Markdown documentation
* Description: Complete setup guide for Linear's MCP server across multiple platforms (Claude, Cursor, VS Code, Codex)
* Endpoints:
  * HTTP: https://mcp.linear.app/mcp
  * SSE: https://mcp.linear.app/sse
* Files: .md, .url, .meta.json

### 2026-01-04: Model Context Protocol Specification

**MCP Protocol Specification Version 2025-11-25** (`2026-01-04--mcp-protocol-specification-2025-11-25.*`)

* Source: https://modelcontextprotocol.io/specification/2025-11-25
* Format: Markdown specification document
* Description: Official MCP specification (latest version) covering architecture, security, and protocol details
* Key Technologies: JSON-RPC 2.0, OAuth 2.1, Server-Sent Events, Streamable HTTP
* Files: .md, .url, .meta.json

### 2025-09-03: Linearis Blog Post

**Linearis Blog Post** (`2025-09-03--linearis-blog-post.md`)

* Source: Linearis blog
* Format: Markdown
* Description: Historical context about the Linearis project

## Archive Quality Standards

All archives maintain the following quality standards:

1. **Source Attribution**: Every file has a corresponding .url file with the source URL
2. **Metadata**: Each archive includes structured metadata in .meta.json format
3. **Timestamps**: All archives are dated with retrieval timestamp
4. **Repository Information**: Git-hosted files include .repo.json with commit hash and clone information
5. **Preservation**: Original formats are preserved when possible (e.g., .graphql schema)
6. **Readability**: Markdown versions created for easy reading and searching

## Extraction Methods

* **WebFetch**: Primary tool for fetching web documentation
* **WebSearch**: Used for discovery and finding additional resources
* **curl**: Direct downloads from raw GitHub URLs
* **jina.ai_reader**: Enhanced content extraction (when needed)

## Related Resources

* Main project README: /home/gw-t490/kb/code-kb/mcp-servers/linear-mcp-cli-comparison-pub-kb/README.md
* Research scope: /home/gw-t490/kb/code-kb/mcp-servers/linear-mcp-cli-comparison-pub-kb/SCOPE.md
* Project catalog: /home/gw-t490/kb/code-kb/mcp-servers/linear-mcp-cli-comparison-pub-kb/projects/

## Updating Archives

When updating existing archives:

1. Create new dated files (don't overwrite existing archives)
2. Update all related files (.md, .url, .meta.json, etc.) in the same commit
3. Document changes in commit message
4. Preserve historical archives for comparison

## Future Archive Candidates

Potential resources to archive in the future:

* Linear CLI documentation (when located)
* Additional MCP implementation examples
* Linear SDK documentation
* Linear webhook specifications
* OAuth 2.1 and RFC 8707 specifications
