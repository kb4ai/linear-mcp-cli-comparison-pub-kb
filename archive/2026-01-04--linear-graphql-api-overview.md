# Linear GraphQL API Documentation Overview

**Source URL:** https://linear.app/developers
**Archive Date:** 2026-01-04
**Summary:** High-level overview of Linear's GraphQL API documentation with links to key features and resources.

---

## Overview

Linear's public API is built using GraphQL. It's the same API Linear uses internally for developing their applications. This provides a comprehensive and powerful interface for building integrations and applications on top of Linear.

## Key API Features

### Pagination

List responses implement "Relay style cursor-based pagination model with first/after and last/before pagination arguments." This enables efficient data retrieval, allowing developers to query specific subsets like "the first 10 issues in your workspace."

### Filtering

The API supports filtering on paginated results. As documented: "Most results that are paginated can also be filtered. This makes it easy to retrieve specific information, like any issues assigned to a particular user, but much more complex queries are also possible."

### Rate Limiting

Rate limits exist to "provide equitable access to the API for everyone and to prevent abuse." The documentation notes that limits may evolve and recommends checking the Slack community API announcements channel for updates.

**Rate Limits:**

* API key authentication: 1,500 requests per hour per user
* OAuth app authentication: 500 requests per hour per user/app
* Unauthenticated requests: 60 requests per hour per IP address
* Complexity-based rate limiting: API key authentication allows 250,000 complexity points per hour per user

## Authentication

The platform offers multiple authentication approaches:

* OAuth 2.0 authentication
* Personal API keys
* File storage authentication
* OAuth actor authorization

## Additional Resources

The documentation references:

* GraphQL Schema available via Apollo Studio
* TypeScript SDK for strongly-typed operations
* CLI importer for data migration
* Webhook support for real-time events
* File attachment handling

Integration guides and a complete Integration Directory are available for developers building on the platform.

## GraphQL Resources

For those new to GraphQL:

* Apollo offers resources for beginners
* Official GraphQL documentation serves as a good reference
* Linear's GraphQL API is explorable and queryable via Apollo Studio (no download or login required)

## Schema Types

The Linear GraphQL schema includes various types such as:

* Generic payload returns from entity deletion mutations
* Documents that can be attached to different entities
* Issue assignee sorting options and issue attachments (e.g., support ticket, pull request)
* Cycle properties, cycle filtering options, and cycle notification subscriptions
* Initiative properties, initiative collection filtering options, and initiative creation properties

---

**Key Resources:**

* **Main Developer Documentation**: https://linear.app/developers/graphql
* **GraphQL API Reference**: https://developers.linear.app/docs/graphql/working-with-the-graphql-api
* **Apollo Studio Schema Explorer**: https://studio.apollographql.com/public/Linear-API/schema/reference
* **GitHub Schema File**: https://github.com/linear/linear/blob/master/packages/sdk/src/schema.graphql
* **API and Webhooks Docs**: https://linear.app/docs/api-and-webhooks
* **Linear API Essentials**: https://rollout.com/integration-guides/linear/api-essentials
