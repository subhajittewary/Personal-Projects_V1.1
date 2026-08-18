#!/usr/bin/env bash
set -euo pipefail

compose_file="infra/compose/docker-compose.yml"
services=(web api worker mcp-server postgres redis qdrant neo4j)

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker CLI is required. Install Docker Desktop and retry." >&2
  exit 1
fi
if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 is required (docker compose)." >&2
  exit 1
fi
if [[ ! -f .env ]]; then
  echo "Missing .env. Run: cp .env.example .env" >&2
  exit 1
fi

failed=0
for service in "${services[@]}"; do
  state="$(docker compose --env-file .env -f "$compose_file" ps --format '{{.Service}} {{.State}} {{.Health}}' "$service" 2>/dev/null || true)"
  if [[ "$state" == *"healthy"* ]]; then
    echo "PASS $service: $state"
  else
    echo "FAIL $service: ${state:-not running}"
    failed=1
  fi
done

if (( failed )); then
  echo "One or more services are not healthy. Inspect: docker compose --env-file .env -f $compose_file logs" >&2
  exit 1
fi
echo "All SB-2 services are healthy."
