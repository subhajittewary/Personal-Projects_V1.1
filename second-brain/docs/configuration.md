# Configuration and secrets (SB-4)

The API loads configuration through `second_brain_api.config.load_settings()` at startup. Missing or malformed required values raise `SettingsError` before the service accepts traffic.

## Sources

- Local development: copy `.env.example` to `.env`; `.env` is ignored by Git.
- Test: pass a mapping to `load_settings()` so tests do not depend on a machine environment.
- Staging/production: inject environment variables from the deployment platform's secret manager. Do not commit production `.env` files.

## Secret policy

`POSTGRES_PASSWORD`, the Neo4j password inside `NEO4J_AUTH`, and `APP_SECRET_KEY` are required secrets. They are stored on the `Settings` object only for dependency injection and are never included in `Settings.redacted()` or health/debug output. Rotate them through the deployment secret manager, restart affected services, verify health, then revoke the old value where the provider supports revocation.

## Naming

Use uppercase names for environment variables. Public non-secret settings may be logged only through the redacted summary. URLs and ports are validated before startup.
