source: <https://www.perplexity.ai/search/linux-unix-cli-tools-for-linea-jEmXiBT9QvGuVAwjeAlqTw>

Based on my comprehensive research, I can now provide you with a detailed analysis of solutions for accessing Linear's MCP server (and similar authenticated HTTP MCP endpoints) from the Linux command line.

## Solutions for Accessing Authenticated MCP Endpoints from Linux Command Line

### The Core Problem

Your research correctly identified that **mcptools currently does not support HTTP transport or passing authorization headers**. The tool is designed exclusively for stdio transport, and its `configs` subsystem is meant only for reading/writing IDE configuration files—not for directly using those servers. According to the developer's blog, HTTP transport support is on the roadmap but not yet implemented.[1][2][3]

### Working Solutions

#### 1. **MCP Inspector CLI Mode** (Immediate, No Setup Required)

The official MCP Inspector supports bearer token authentication and has a CLI mode that works with HTTP/SSE endpoints.[4][5][6]

**Basic Usage:**
```bash
# List tools
npx @modelcontextprotocol/inspector --cli \
  --url https://mcp.linear.app/mcp \
  --header "Authorization: Bearer <your-token>" \
  tools

# Call a tool
npx @modelcontectprotocol/inspector --cli \
  --url https://mcp.linear.app/mcp \
  --header "Authorization: Bearer <token>" \
  call <tool-name> --params '{...}'
```

**Extract token from Claude's credentials:**
```bash
TOKEN=$(cat ~/.claude/.credentials.json | \
  jq -r '.mcpOAuth."linear-server|ABCDEF0123456789".accessToken')

npx @modelcontextprotocol/inspector --cli \
  --url https://mcp.linear.app/mcp \
  --header "Authorization: Bearer $TOKEN" \
  tools
```

#### 2. **Proxy Solutions** (Bridge stdio ↔ HTTP for mcptools)

These proxies act as intermediaries, allowing mcptools to connect via stdio while the proxy handles HTTP authentication.

##### **A. mcp-stdio-to-streamable-http-adapter** (Recommended)

This TypeScript adapter specifically supports bearer tokens via environment variables.[7]

**Setup:**
```bash
# Create wrapper script: ~/.local/bin/linear-mcp
#!/bin/bash
export URI="https://mcp.linear.app/mcp"
export BEARER_TOKEN="$(cat ~/.claude/.credentials.json | \
  jq -r '.mcpOAuth."linear-server|ABCDEF0123456789".accessToken')"
npx @pyroprompts/mcp-stdio-to-streamable-http-adapter "$@"

# Make executable
chmod +x ~/.local/bin/linear-mcp

# Use with mcptools
mcptools tools ~/.local/bin/linear-mcp
mcptools shell ~/.local/bin/linear-mcp
```

##### **B. mcp-proxy** (Python)

Python-based proxy supporting `--api-access-token` flag.[8][9]

```bash
# Install
pip install mcp-proxy

# Use with mcptools
TOKEN=$(cat ~/.claude/.credentials.json | \
  jq -r '.mcpOAuth."linear-server|ABCDEF0123456789".accessToken')

mcptools tools mcp-proxy --api-access-token "$TOKEN" \
  https://mcp.linear.app/sse
```

##### **C. mcp-stdio-http-proxy**

Handles full OAuth flow automatically.[10]

```bash
# Set up environment
export OAUTH_CLIENT_ID="your_client_id"
export OAUTH_CLIENT_SECRET="your_client_secret"
export MCP_SERVER_URL="https://mcp.linear.app/sse"

# Run proxy in background
npx mcp-stdio-http-proxy &

# Connect with mcptools
mcptools tools npx mcp-stdio-http-proxy
```

#### 3. **Direct HTTP Testing with curl** (For Testing/Scripts)

You can interact with MCP servers directly using curl by following the JSON-RPC protocol.[11][12][13]

**Complete workflow:**
```bash
# Step 1: Initialize (get session if using stateful HTTP)
curl -X POST https://mcp.linear.app/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2025-06-18",
      "capabilities": {},
      "clientInfo": {"name": "curl-client", "version": "1.0"}
    }
  }'

# Step 2: Send initialized notification
curl -X POST https://mcp.linear.app/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "jsonrpc": "2.0",
    "method": "notifications/initialized",
    "params": {}
  }'

# Step 3: List tools
curl -X POST https://mcp.linear.app/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
  }'

# Step 4: Call a tool
curl -X POST https://mcp.linear.app/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "search_issues",
      "arguments": {"query": "bug"}
    }
  }'
```

#### 4. **Alternative CLI Tools**

Several alternative MCP CLI tools support HTTP authentication:

##### **chrishayuk/mcp-cli**
Supports HTTP, SSE transports with environment variables and headers for authentication.[14]

##### **mcp-superassistant-proxy**
Supports `--oauth2Bearer` flag for bearer tokens:[15]
```bash
npx @srbhptl39/mcp-superassistant-proxy \
  --sse https://mcp.linear.app/sse \
  --oauth2Bearer "your-token"
```

### Linear-Specific Solution

Linear's official MCP server now supports **direct Bearer token authorization** as an alternative to the interactive OAuth flow:[16][17]

```bash
# Using Linear API key directly
npx @modelcontextprotocol/inspector --cli \
  --url https://mcp.linear.app/mcp \
  --header "Authorization: Bearer lin_api_xxxxxx" \
  tools
```

This means you can use a Linear API key (generated from Settings → API) instead of OAuth tokens.

### Recommended Approach

**For immediate testing:**
Use MCP Inspector CLI mode with your Linear API key:
```bash
LINEAR_API_KEY="lin_api_xxxxxx"
npx @modelcontextprotocol/inspector --cli \
  --url https://mcp.linear.app/mcp \
  --header "Authorization: Bearer $LINEAR_API_KEY" \
  tools
```

**For ongoing use with mcptools:**
Create a wrapper script using `mcp-stdio-to-streamable-http-adapter`:
```bash
#!/bin/bash
# ~/.local/bin/linear-mcp
export URI="https://mcp.linear.app/mcp"
export BEARER_TOKEN="lin_api_xxxxxx"  # Or extract from Claude credentials
exec npx @pyroprompts/mcp-stdio-to-streamable-http-adapter "$@"
```

Then use with mcptools:
```bash
mcptools shell ~/.local/bin/linear-mcp
```

### Known Issues & Feature Requests

1. **mcptools HTTP support**: On the roadmap but not yet implemented[2]
2. **MCP Inspector custom headers**: Issue #879 requests better custom header support[18]
3. **MCP Inspector multiple headers**: Issue #572 requests multiple custom headers in UI[19]

### Summary

While mcptools doesn't natively support authenticated HTTP endpoints, you have several working alternatives:

1. **MCP Inspector** for ad-hoc testing
2. **Proxy adapters** to bridge stdio/HTTP for mcptools compatibility  
3. **Direct curl** for scripting and automation
4. **Alternative CLI tools** with native HTTP/auth support

The proxy approach is most seamless if you prefer mcptools' interface, while MCP Inspector CLI mode is best for immediate testing without setup.

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/393414/ac4c51b1-7c78-48e7-a005-367a221c7cc8/mcp_linear_app_issue_with_passing_authorization.md)
[2](https://blog.fka.dev/blog/2025-03-26-introducing-mcp-tools-cli/)
[3](https://www.reddit.com/r/Linear/comments/1m15z6m/linctl_a_linear_cli_purposebuilt_for_agents_like/)
[4](https://www.npmjs.com/package/@modelcontextprotocol/inspector)
[5](https://www.stainless.com/mcp/mcp-inspector-testing-and-debugging-mcp-servers)
[6](https://github.com/modelcontextprotocol/inspector)
[7](https://dxt.services/mcp/mcp-stdio-to-streamable-http-adapter/)
[8](https://pypi.org/project/mcp-proxy/0.3.2/)
[9](https://pypi.org/project/mcp-proxy/)
[10](https://lobehub.com/mcp/sr-auto-mcp-stdio-http-proxy)
[11](https://ragflow.io/docs/mcp_client)
[12](https://vunda.ai/blog/fast-mcp-deep-dive)
[13](https://zuplo.com/docs/articles/manual-mcp-oauth-testing)
[14](https://github.com/chrishayuk/mcp-cli)
[15](https://www.npmjs.com/package/@srbhptl39/mcp-superassistant-proxy)
[16](https://linear.app/docs/mcp)
[17](https://www.linkedin.com/pulse/how-connect-linear-mcp-server-claude-code-mark-mitchell-pkawc)
[18](https://github.com/modelcontextprotocol/inspector/issues/879)
[19](https://github.com/modelcontextprotocol/inspector/issues/572)
[20](https://gofastmcp.com/servers/context)
[21](https://mcp-auth.dev/docs)
[22](https://gofastmcp.com/clients/auth/bearer)
[23](https://www.solo.io/blog/part-two-mcp-authorization-the-hard-way)
[24](https://www.stainless.com/mcp/mcp-authentication)
[25](https://www.reddit.com/r/mcp/comments/1m15igp/how_to_manage_user_access_within_a_tool/)
[26](https://stytch.com/blog/MCP-authentication-and-authorization-guide/)
[27](https://modelcontextprotocol.info/docs/concepts/tools/)
[28](https://mcp-auth.dev/docs/configure-server/bearer-auth)
[29](https://modelcontextprotocol.io/docs/tutorials/security/authorization)
[30](https://gofastmcp.com/servers/auth/authentication)
[31](https://community.postman.com/t/mcp-request-how-to-pass-the-bearer-token-in-call-to-a-tool/80736)
[32](https://modelcontextprotocol.info/specification/draft/basic/authorization/)
[33](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization)
[34](https://github.com/modelcontextprotocol/python-sdk/issues/1414)
[35](https://developers.openai.com/codex/mcp/)
[36](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/mcp-authentication?view=foundry)
[37](https://github.com/google/adk-python/discussions/2482)
[38](https://github.com/modelcontextprotocol/python-sdk/issues/750)
[39](https://developers.openai.com/apps-sdk/build/auth/)
[40](https://www.npmjs.com/package/mcp-http-server)
[41](https://eliteai.tools/mcp/chrishayuk-mcp-cli/alternatives)
[42](https://modelcontextprotocol.io/docs/tools/inspector.md)
[43](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)
[44](https://blog.fka.dev/blog/2025-03-27-mcp-inspector-vs-mcp-tools/)
[45](https://www.youtube.com/watch?v=XcepHL3KgzA)
[46](https://www.npmjs.com/package/@aurracloud%2Fmcp-cli)
[47](https://github.com/wong2/awesome-mcp-servers)
[48](https://en.bioerrorlog.work/entry/how-to-use-mcp-inspector)
[49](https://www.npmjs.com/package/@mcp-use/cli)
[50](https://www.reddit.com/r/mcp/comments/1kcfemq/whats_the_best_opensource_mcp_client_if_its/)
[51](https://dev.to/yigit-konur/the-ultimate-guide-to-the-mcp-inspector-by-cli-non-interactive-mode-4k6b)
[52](https://www.npmjs.com/package/@mcpc-tech%2Fcli)
[53](https://www.merge.dev/blog/model-context-protocol-alternatives)
[54](https://en.bioerrorlog.work/entry/how-to-use-mcp-cli)
[55](https://generect.com/blog/mcp-tools/)
[56](https://modelcontextprotocol.io/docs/tools/inspector)
[57](https://modelcontextprotocol.io/docs/develop/build-server)
[58](https://www.qodo.ai/blog/best-cli-tools/)
[59](https://docs.litellm.ai/docs/mcp)
[60](https://blog.logto.io/mcp-auth-implementation-guide-2025-06-18)
[61](https://biomcp.org/developer-guides/04-transport-protocol/)
[62](https://docs.scalekit.com/authenticate/mcp/quickstart/)
[63](https://cardinalops.com/blog/mcp-defaults-hidden-dangers-of-remote-deployment/)
[64](https://github.com/microsoft/copilot-intellij-feedback/issues/354)
[65](https://supertokens.com/docs/authentication/ai-authentication)
[66](https://gofastmcp.com/deployment/running-server)
[67](https://github.com/microsoft/semantic-kernel/issues/12890)
[68](https://www.npmjs.com/package/mcp-remote)
[69](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)
[70](https://github.com/BerriAI/litellm/issues/14413)
[71](https://community.n8n.io/t/mcp-bearer-authorization/110628)
[72](https://gofastmcp.com/deployment/http)
[73](https://github.com/MCP-Mirror/huanshenyi_mcp-server-bearer-auth)
[74](https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools)
[75](https://www.youtube.com/watch?v=E1W1zsLd7AE)
[76](https://github.blog/changelog/2025-12-10-the-github-mcp-server-adds-support-for-tool-specific-configuration-and-more/)
[77](https://blog.christianposta.com/understanding-mcp-authorization-step-by-step-part-two/)
[78](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
[79](https://pypi.org/project/mcp-proxy/0.3.0/)
[80](https://www.infracloud.io/blogs/securing-mcp-servers/)
[81](https://www.npmjs.com/package/mcp-proxy)
[82](https://www.solo.io/blog/understanding-mcp-authorization-step-by-step-part-one)
[83](https://github.com/agno-agi/agno/issues/5568)
[84](https://fly.io/docs/mcp/transports/stdio/)
[85](https://github.com/neeraj15022001/curl-mcp-server)
[86](https://github.com/agno-agi/agno/issues/5026)
[87](https://github.com/sparfenyuk/mcp-proxy)
[88](https://stackoverflow.com/questions/79556268/mcp-python-sdk-how-to-authorise-a-client-with-bearer-header-with-sse/79573523)
[89](https://mcp-auth.dev/docs/0.1.1/tutorials/whoami)
[90](https://modelcontextprotocol.io/specification/draft/basic/authorization)
[91](https://github.com/gomarble-ai/mcp-proxy-nodejs)
[92](https://www.reddit.com/r/modelcontextprotocol/comments/1jptxqj/supergateway_v26_add_auth_and_other_headers_when/)
[93](https://www.mcpevals.io/blog/mcp-inspector-guide)
[94](https://libraries.io/npm/@pyroprompts%2Fmcp-stdio-to-streamable-http-adapter)
[95](https://libraries.io/pypi/mcp-proxy)
[96](https://pypi.org/project/mcp-openapi-proxy/)
[97](https://lobehub.com/mcp/gws8820-secure-mcp-proxy)
[98](https://github.com/iceener/linear-streamable-mcp-server)
[99](https://grafana.com/docs/grafana-cloud/machine-learning/assistant/mcp/add-linear-mcp-server/)
[100](https://github.com/geropl/linear-mcp-go)
[101](https://mariozechner.at/posts/2025-08-15-mcp-vs-cli/)
[102](https://docs.port.io/ai-interfaces/port-mcp-server/overview-and-installation/)
[103](https://skywork.ai/skypage/en/mcp-openapi-proxy-ai-agents/1978638151140888576)
[104](https://www.getclockwise.com/blog/claude-code-mcp-tools-integration)
[105](https://github.com/modelcontextprotocol/python-sdk/issues/431)
[106](https://linear.app/changelog/2025-05-01-mcp)
[107](https://playbooks.com/mcp/vinayak-mehta-linear)
[108](https://apidog.com/blog/linear-mcp-server/)
[109](https://github.com/google/adk-python/issues/3156)
[110](https://github.com/modelcontextprotocol/go-sdk/issues/104)
[111](https://github.com/langchain-ai/langchain-mcp-adapters/issues/235)
[112](https://forum.cursor.com/t/using-linear-app-with-cursor/73812)
[113](https://www.reddit.com/r/modelcontextprotocol/comments/1jlh1d2/you_can_now_build_http_mcp_servers_in_5_minutes/)
[114](https://mcpcat.io/guides/understanding-json-rpc-protocol-mcp/)
[115](https://linear.app/integrations/claude)
[116](https://mcpservers.org/servers/coucya/mcp-server-requests)
[117](https://mcpservers.org/servers/ciresnave/json-mcp-server)
[118](https://linearb.helpdocs.io/article/ckyv4dylbs-configuring-the-mcp-service-in-linear-b)
[119](https://opencode.ai/docs/mcp-servers/)
[120](https://github.com/shanejonas/openrpc-mcp-server)
[121](https://linear.app/integrations/builder-io-mcp)
[122](https://developers.openai.com/apps-sdk/concepts/mcp-server/)
[123](https://playbooks.com/mcp/pskill9-website-downloader)
[124](https://httpie.io)
[125](https://skywork.ai/skypage/en/website-downloader-ai-engineer-guide/1980869402091515904)
[126](https://composio.dev/blog/how-to-set-up-linear-mcp-in-claude-code-to-automate-issue-tracking)
[127](https://github.com/httpie/cli)
[128](https://github.com/IBM/mcp-context-forge/issues/323)
[129](https://skywork.ai/skypage/en/HTTPie-Download:-Your-Gateway-to-Simplified-API-Interaction/1976160752673812480)
[130](https://milvus.io/ai-quick-reference/whats-the-best-way-to-test-an-model-context-protocol-mcp-server-locally)
[131](https://foojay.io/today/understanding-mcp-through-raw-stdio-communication/)
[132](https://hexdocs.pm/conduit_mcp/readme-2.html)
[133](https://playbooks.com/mcp/mcp-get-curl)
[134](https://www.bitsight.com/blog/exposed-mcp-servers-reveal-new-ai-vulnerabilities)
[135](https://macocci7.net/blog/2025/10/27/curl%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%81%A7%E3%81%AEmcp%E3%82%B5%E3%83%BC%E3%83%90%E3%83%BC%E3%83%86%E3%82%B9%E3%83%88/)
[136](https://lobehub.com/mcp/247arjun-mcp-curl)
[137](https://docs.langchain.com/oss/python/langchain/mcp)
[138](https://stackoverflow.com/questions/24368745/jsonrpc-request-with-curl)
[139](https://developers.cloudflare.com/agents/guides/test-remote-mcp-server/)
[140](https://github.com/modelcontextprotocol/python-sdk/issues/195)
[141](https://community.openai.com/t/mcp-server-passes-all-json-rpc-tests-but-agent-builder-fails-with-424-failed-dependency/1363529)
[142](https://community.n8n.io/t/need-help-mcp-server-trigger-not-working-curl-18-error/105492)
[143](https://platform.openai.com/docs/guides/tools-connectors-mcp)
[144](https://github.com/MartinPSDev/curl-mcp)
