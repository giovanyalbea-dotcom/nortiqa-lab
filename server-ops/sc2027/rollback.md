# Rollback - SC2027/Nortiqa

Status: draft operational checklist

## Immediate rollback principle

Prefer reverting the smallest changed surface: config file, container image, app
folder, or compose service. Do not delete volumes during emergency rollback.

## Steps

1. Stop and identify the failing change.
2. Restore the previous config from the latest backup directory.
3. Run config syntax checks before reload/recreate.
4. Recreate/reload only affected services.
5. Run `./healthcheck-prod.sh`.
6. Confirm HTTPS public routes.
7. Record incident notes and follow-up actions.

## Never do during rollback

- Do not run `docker compose down -v` in production.
- Do not delete Postgres, n8n, or Metabase volumes.
- Do not rotate secrets inside an incident without recording ownership.
- Do not keep a partial rollback unrecorded.
