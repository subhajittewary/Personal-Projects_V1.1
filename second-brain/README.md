# Second Brain

Second Brain is a personal knowledge and action layer. This repository is the monorepo foundation for the React web application, FastAPI API, asynchronous worker, AI capability packages, and shared contracts.

## Repository layout

```text
apps/
  web/       React + Vite application
  api/       FastAPI HTTP and streaming boundary
  worker/    background jobs
packages/
  shared/    versioned API/domain contracts for TypeScript consumers
  agent/     LangGraph orchestration
  rag/       parsing, chunking, retrieval
  memory/    durable-memory policies
  graph/     graph extraction and retrieval
  mcp/       typed external-tool adapters
contracts/   language-neutral JSON Schemas and API conventions
docs/        architecture decisions and contributor guidance
```

## Prerequisites

- Node.js 22+ and npm 10+
- Python 3.12+

## Quick start

```bash
npm install
npm run lint
npm test
npm run build
```

The Python services intentionally have no runtime dependencies at this initial foundation stage. Their import checks run through `npm test`. FastAPI and worker dependencies will be added with the corresponding delivery stories.

## Local containers (SB-2)

Docker Compose runs the local service topology, including web, API, worker, MCP server, PostgreSQL, Redis, Qdrant, and Neo4j. The API, worker, MCP, and web images are health-ready placeholders until their feature stories replace them with real implementations.

```bash
cp .env.example .env
npm run compose:config
npm run compose:up
npm run compose:smoke
npm run compose:down
```

The `.env` file is local-only and ignored by Git. The values in `.env.example` are development defaults and must not be reused outside local development.

## Commands

| Command | Purpose |
| --- | --- |
| `npm run lint` | Run TypeScript checks and Python syntax checks |
| `npm test` | Validate contracts and package import boundaries |
| `npm run build` | Build all Node workspaces |
| `npm run dev:web` | Start the Vite web workspace |
| `npm run check:contracts` | Validate the canonical JSON Schema files |
| `npm run compose:config` | Validate the Compose configuration |
| `npm run compose:up` | Build and start the local service topology |
| `npm run compose:smoke` | Check that all services report healthy |
| `npm run compose:down` | Stop the local service topology |

## Contract policy

The canonical language-neutral contracts live in `contracts/json-schema`. TypeScript consumers use `@second-brain/shared`; Python services use the same JSON Schema files as their cross-service source of truth. Any public contract change must update its schema, the TypeScript export when applicable, and its version in `contracts/README.md`.

## Status

This implements **SB-1: Establish the monorepo and shared contracts**. Infrastructure, authentication, FastAPI endpoints, and background processing are intentionally deferred to their respective stories.

## API boundary standard (SB-3)

Public routes must be built under `/api/v1` using `second_brain_api.versioning.versioned_path`. Domain failures should use the stable `ErrorEnvelope` through the typed factories in `second_brain_api.errors`; unexpected exceptions are converted to a safe `INTERNAL_ERROR`. Trace IDs are accepted only when safe and are returned through `X-Trace-ID` and the JSON error body.
