# Server Ops Handoff - 2026-06-17 - Nortiqa/SC2027

## Metadata

- Date: 2026-06-17
- Project: Nortiqa Lab server / SC2027 VPS
- AI actor: Codex
- Responsible user: Gio
- State: operational checkpoint completed

## Canon / Plan Context

- Intended plan: Claude DICT-SC2027-001 / Plan OPS before Route Critical.
- Notion connector was unavailable during this turn: MCP handshake returned HTTP 404.
- Work was limited to operational checks, deploy-owned files, staging kit files,
  and permission hardening that did not require reading secrets.

## Work Completed

- Verified VPS identity and active Docker containers.
- Confirmed public services:
  - `https://nortiqalab.com/` returns 200.
  - `https://api.nortiqalab.com/health` returns 200.
  - `https://n8n.nortiqalab.com/` returns 200.
  - `https://mcp.nortiqalab.com/` returns 401, as expected.
- Installed OPS kit in `/home/deploy/sc2027-staging/`:
  - `backup-config.sh`
  - `healthcheck-staging.sh`
  - `healthcheck-prod.sh`
  - `promote-staging-to-prod.md`
  - `rollback.md`
- Ran `backup-config.sh`.
- Ran staging and production healthchecks successfully.
- Hardened readable secret files owned by `deploy`:
  - `/home/deploy/mcp.env` -> `600`
  - `/opt/nortiqa/agents/nortiqa-console/.env` -> `600`

## Verification

- Backup path:
  - `/home/deploy/sc2027-staging/backups/20260617T172009Z`
- `./healthcheck-staging.sh`: passed.
- `./healthcheck-prod.sh`: passed.
- `docker exec sc2027-proxy nginx -t`: passed through prod healthcheck.

## Blockers / Manual Actions

- `/opt/sc2027/.env` is still `-rw-r--r--` and owned by `sc2027:sc2027`.
  `deploy` cannot change it without sudo/root.
- Nginx hardening against scanner paths such as `.env`, `wp-config.php`, and
  `phpinfo.php` could not be applied because `/opt/sc2027/nginx/conf.d` is not
  writable by `deploy`, and `sudo` requires a password.
- Gio still needs to confirm:
  - Hetzner snapshot exists.
  - exposed tokens were rotated where applicable.

## Next Safe Step

Use root/sudo or the `sc2027` owner account to:

1. `chmod 600 /opt/sc2027/.env`
2. Add Nginx deny/404 rules for sensitive scanner paths.
3. Run `docker exec sc2027-proxy nginx -t`.
4. Reload Nginx only after syntax passes.

