# Promote staging to production - SC2027/Nortiqa

Status: draft operational checklist

## Gates before promotion

- Gio confirms Hetzner snapshot exists.
- Gio confirms exposed tokens were rotated where applicable.
- `./backup-config.sh` completed and backup path was recorded.
- `./healthcheck-staging.sh` passes.
- `./healthcheck-prod.sh` passes before changes.
- No unreviewed secrets are copied from staging to production.

## Promotion checklist

1. Record current production container state.
2. Record current git/image/app version if available.
3. Apply only the reviewed delta from staging to production.
4. Run `docker compose config` in production path.
5. Recreate only affected services.
6. Run `./healthcheck-prod.sh`.
7. Verify public HTTPS URLs from outside the VPS.
8. Record final result and rollback point.

## Hard stops

- Do not promote if HTTPS is broken.
- Do not promote if auth is disabled for n8n, Metabase, or MCP.
- Do not promote if database backups/snapshots are missing.
- Do not promote Bot Telegram / Docker socket work without separate PAO.
