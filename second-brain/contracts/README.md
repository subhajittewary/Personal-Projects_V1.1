# Contracts

This directory owns the language-neutral contracts between the web application, API, worker, and domain packages.

## Versioning

- Each schema has a stable `$id` including a major version.
- Additive compatible changes remain within a major version.
- Breaking changes require a new major-version schema and a migration period.
- Public API routes are versioned independently under `/api/v1`.

## Current contracts

| Contract | Consumers | Purpose |
| --- | --- | --- |
| `error-envelope.v1.json` | web, API, worker, packages | consistent machine-readable failures |
| `document.v1.json` | web, API, worker, RAG | document lifecycle model |
| `chat-event.v1.json` | web, API, agent | server-sent chat event model |

JSON Schema is intentionally used here so Python and TypeScript use the same canonical definition. Language-specific validation adapters must not silently broaden the schema.
