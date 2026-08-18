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

The Python services intentionally have no runtime dependencies at this initial foundation stage. Their import checks run through `pnpm test`. FastAPI and worker dependencies will be added with the corresponding delivery stories.

## Commands

| Command | Purpose |
| --- | --- |
| `npm run lint` | Run TypeScript checks and Python syntax checks |
| `npm test` | Validate contracts and package import boundaries |
| `npm run build` | Build all Node workspaces |
| `npm run dev:web` | Start the Vite web workspace |
| `npm run check:contracts` | Validate the canonical JSON Schema files |

## Contract policy

The canonical language-neutral contracts live in `contracts/json-schema`. TypeScript consumers use `@second-brain/shared`; Python services use the same JSON Schema files as their cross-service source of truth. Any public contract change must update its schema, the TypeScript export when applicable, and its version in `contracts/README.md`.

## Status

This implements **SB-1: Establish the monorepo and shared contracts**. Infrastructure, authentication, FastAPI endpoints, and background processing are intentionally deferred to their respective stories.
