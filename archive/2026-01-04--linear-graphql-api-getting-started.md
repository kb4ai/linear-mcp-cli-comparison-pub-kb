# Linear GraphQL API: Getting Started Guide

**Source URL:** https://linear.app/developers/graphql
**Archive Date:** 2026-01-04
**Summary:** Complete documentation for getting started with the Linear GraphQL API, including authentication, queries, mutations, and best practices.

---

## Overview

Linear's API is built on GraphQL—the same technology powering their internal applications. The service provides a modern alternative to REST APIs with introspection capabilities and strongly-typed queries.

## API Endpoint

The GraphQL endpoint is located at `https://api.linear.app/graphql`. The endpoint supports schema introspection, allowing developers to explore available queries and types programmatically.

## Authentication Methods

### OAuth 2.0

For applications serving multiple users, "OAuth2 authentication is recommended" when building integrations. After completing the OAuth flow and obtaining an access token, include it as: `Authorization: Bearer <ACCESS_TOKEN>`

### Personal API Keys

For scripts and personal use cases, API keys provide simpler authentication. Create and manage keys via the Security & access settings. Include keys using: `Authorization: <API_KEY>`

## Core Queries

**Getting the authenticated user:**

```graphql
query Me {
  viewer {
    id
    name
    email
  }
}
```

**Retrieving teams:**

Teams organize issues. Query available teams to identify which workspace to interact with:

```graphql
query Teams {
  teams { nodes { id name } }
}
```

**Fetching team issues:**

```graphql
query Team {
  team(id: "9cfb482a-81e3-4154-b5b9-2c805e70a02d") {
    issues { nodes { id title description } }
  }
}
```

## Mutations: Creating & Modifying Data

**Creating issues:**

```graphql
mutation IssueCreate {
  issueCreate(input: {
    title: "New exception"
    description: "Detailed error report"
    teamId: "9cfb482a-81e3-4154-b5b9-2c805e70a02d"
  }) {
    success
    issue { id title }
  }
}
```

Issues created without a `stateId` default to the team's first Backlog state, or Triage if enabled.

**Updating issues:**

```graphql
mutation IssueUpdate {
  issueUpdate(id: "BLA-123", input: {
    title: "Updated Title"
    stateId: "NEW-STATE-ID"
  }) {
    success
    issue { id title state { name } }
  }
}
```

Changes within the first 3 minutes of creation aren't logged as modifications.

## Advanced Features

**Markdown mentions:** Reference resources using their URLs—"mentions can be created in Markdown by using the plain URL of the resource."

**Collapsible sections:** Use `+++ Section title` and `+++` delimiters to create expandable content blocks.

**Image access:** Linear hosts authenticated assets. Only authenticated API users can access images; self-hosting is recommended for external displays.

## Fetching Updates Efficiently

**Recommended approaches:**

* Register webhooks for real-time notifications
* Order results by update timestamp for polling
* Filter at query-level rather than in application code

**Avoid:**

* Polling individual issues repeatedly (triggers rate limits)

## Error Handling

"GraphQL queries can partially succeed with a 200 HTTP status, returning some data while including errors for failed fields." Always inspect the `errors` array before assuming success. Monitor HTTP status codes and rate limit headers accordingly.

## SDK Alternative

The Linear TypeScript SDK provides strongly-typed operations without manual GraphQL construction. It wraps the GraphQL API with improved developer ergonomics.

## Support

Questions and issues can be directed to the customer Slack community or `hello@linear.app`.

---

**Additional Resources:**

* GraphQL Schema: https://github.com/linear/linear/blob/master/packages/sdk/src/schema.graphql
* Apollo Studio Schema Explorer: https://studio.apollographql.com/public/Linear-API/schema/reference
* Linear Developers Portal: https://linear.app/developers
