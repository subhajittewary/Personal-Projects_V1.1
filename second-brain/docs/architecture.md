# Architecture boundaries

This scaffold intentionally separates application boundaries before feature work begins:

- **Web** consumes only versioned API contracts and shared TypeScript types.
- **API** owns HTTP, authentication context, response validation, and streaming boundaries.
- **Worker** owns long-running, idempotent background work.
- **Domain packages** own orchestration, retrieval, memory, graph, and tool logic; they do not own HTTP concerns.
- **Contracts** are language-neutral JSON Schema files; PostgreSQL, Qdrant, Neo4j, Mem0, and provider APIs are not directly accessed by the web app.

This prevents the “one giant agent” design and allows each future story to add behavior behind a stable boundary.
