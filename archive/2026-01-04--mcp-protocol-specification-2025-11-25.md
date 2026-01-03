# Model Context Protocol (MCP) - Version 2025-11-25 Specification

**Source URL:** https://modelcontextprotocol.io/specification/2025-11-25
**Archive Date:** 2026-01-04
**Summary:** Official specification for the Model Context Protocol (MCP) version 2025-11-25, defining the standard for connecting AI applications to external data sources and tools.

---

## Overview

The Model Context Protocol (MCP) is an open protocol that standardizes integration between LLM applications and external data sources and tools. It enables seamless connection of language models with contextual information and capabilities through a standardized interface.

## Key Architecture Components

### Core Participants

* **Hosts**: LLM applications that initiate connections
* **Clients**: Connectors within the host application
* **Servers**: Services that provide context and capabilities

### Base Protocol Foundation

* **Message Format**: JSON-RPC 2.0
* **Connection Model**: Stateful connections
* **Negotiation**: Server and client capability negotiation

## Protocol Features

### Server Features

Servers provide any combination of:

1. **Resources**: Context and data for users or AI models
2. **Prompts**: Templated messages and workflows
3. **Tools**: Functions for AI models to execute

### Client Features

Clients may offer:

1. **Sampling**: Server-initiated agentic behaviors and recursive LLM interactions
2. **Roots**: Server-initiated inquiries into URI or filesystem boundaries
3. **Elicitation**: Server-initiated requests for user information

### Additional Utilities

* Configuration management
* Progress tracking
* Cancellation support
* Error reporting
* Logging capabilities

## Security and Trust & Safety Principles

### Key Requirements

1. **User Consent and Control**
   * Explicit user consent for all data access and operations
   * Users retain control over data sharing and actions
   * Clear UIs for reviewing and authorizing activities

2. **Data Privacy**
   * Explicit user consent before exposing user data to servers
   * No transmission of resource data without consent
   * Appropriate access controls on user data

3. **Tool Safety**
   * Tools represent arbitrary code execution requiring appropriate caution
   * Explicit user consent before tool invocation
   * Clear user understanding of tool behavior

4. **LLM Sampling Controls**
   * Explicit user approval for LLM sampling requests
   * User control over:
     * Whether sampling occurs
     * The actual prompt sent
     * What results servers can access
   * Limited server visibility into prompts (intentional design)

### Implementation Guidelines

Implementors **SHOULD**:

1. Build robust consent and authorization flows
2. Provide clear security documentation
3. Implement appropriate access controls
4. Follow security best practices
5. Consider privacy implications in feature design

## RFC 2119 Key Words

The specification uses standard RFC 2119 terminology:

* **MUST**: Absolute requirement
* **MUST NOT**: Absolute prohibition
* **REQUIRED**: Essential requirement
* **SHALL/SHALL NOT**: Equivalent to MUST/MUST NOT
* **SHOULD/SHOULD NOT**: Recommended/not recommended
* **RECOMMENDED/NOT RECOMMENDED**: Guidance for best practices
* **MAY/OPTIONAL**: Optional features

## Specification Structure

The complete specification is organized into:

### Base Protocol

* Lifecycle management
* Transport mechanisms
* Authorization
* Security best practices
* Utilities (cancellation, ping, progress, tasks)

### Server Features

* Prompts specification
* Resources specification
* Tools specification
* Server utilities (completion, logging, pagination)

### Client Features

* Roots
* Sampling
* Elicitation

### Additional Resources

* Architecture documentation
* Schema reference
* Implementation examples
* SDK documentation

## Protocol Versioning

Current versions available:

* **Version 2025-11-25** (Latest) - Current release
* **Version 2025-06-18** - Previous release
* **Version 2025-03-26** - Earlier version
* **Version 2024-11-05** - Earlier version
* **Draft** - Development version

## Implementation Resources

* **Official Repository**: https://github.com/modelcontextprotocol
* **Schema Reference**: TypeScript schema at `schema/2025-11-25/schema.ts`
* **Documentation**: https://modelcontextprotocol.io
* **Blog**: https://blog.modelcontextprotocol.io

## Related Standards

The protocol takes inspiration from the Language Server Protocol (LSP), which standardized programming language support across development tools. MCP applies similar standardization principles to AI application integration.

## Recent Developments

In December 2025, Anthropic donated the MCP to the Agentic AI Foundation (AAIF), a directed fund under the Linux Foundation, co-founded by Anthropic, Block and OpenAI, with support from other companies.

The November 2025 specification release marked MCP's first anniversary. The protocol has grown significantly since its inception and has been adopted by numerous developers and organizations, evolving from an experimental open source project to becoming the standard for connecting data and applications to Large Language Models (LLMs).

## Technical Details

* MCP re-uses the message-flow ideas of the Language Server Protocol (LSP) and is transported over JSON-RPC 2.0
* The protocol is transport agnostic; servers can be hosted over Server-Sent Events or Streamable HTTP
* The specification includes protected resource metadata, OAuth 2.1 flows, and dynamic client registration for access control without proprietary handshakes

## June 2025 Security Updates

The changelog released on June 18, 2025, introduces updates that clarify how authorization should be handled for MCP Servers and how MCP Clients should implement Resource Indicators to prevent malicious servers from obtaining access tokens.

MCP clients are now required to implement Resource Indicators, as specified in RFC 8707. By using a resource indicator in the token request, a client explicitly states the intended recipient (the "audience") of the access token.

---

**Note**: This is the authoritative specification version 2025-11-25. For detailed protocol messages, implementation examples, and comprehensive API documentation, refer to the complete specification at https://modelcontextprotocol.io/specification/2025-11-25.

**Additional Resources:**

* GitHub Repository: https://github.com/modelcontextprotocol/modelcontextprotocol
* Official Documentation: https://modelcontextprotocol.io
* Blog: https://blog.modelcontextprotocol.io
* TypeScript SDK: https://github.com/modelcontextprotocol
* RFC 8707 Resource Indicators: https://www.rfc-editor.org/rfc/rfc8707
