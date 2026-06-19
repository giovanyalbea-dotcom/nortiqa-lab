# Server Ops Handoff - 2026-06-18 - Login Portal

## Metadata

- Date: 2026-06-18
- Project: Nortiqa Lab / SC2027 login portal
- AI actor: Codex
- Responsible user: Gio
- State: ready for privileged install

## Current State

- `https://nortiqalab.com/` is online.
- `https://nortiqalab.com/login` currently returns the same static landing page.
- n8n has active workflow `SC2027 - Login API` with webhook path:
  - `POST /webhook/login`
- Current public webhook URL:
  - `https://n8n.nortiqalab.com/webhook/login`
- Database table `sistema.usuarios` exists and has 3 users.

## Login Contract Found

Request body:

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

Invalid credentials response:

```json
{
  "success": false,
  "message": "Credenciales invalidas"
}
```

Successful response shape:

```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "nombre": "Nombre",
    "rol_global": "rol",
    "proyectos": []
  }
}
```

## Work Completed Locally

Created deployable package:

- `server-ops/sc2027/login-portal/login.html`
- `server-ops/sc2027/login-portal/install-login-portal.sh`
- `server-ops/sc2027/login-portal/README.md`

The login page posts to same-origin endpoint:

```text
POST /api/login
```

The installer injects this Nginx route:

```text
/api/login -> http://n8n:5678/webhook/login
```

## Why Nginx Proxy Is Needed

Direct browser fetch from `https://nortiqalab.com` to
`https://n8n.nortiqalab.com/webhook/login` would require CORS. The n8n webhook
did not expose the required CORS headers in the tested response path.

Using `/api/login` on the same origin avoids CORS and keeps the frontend simple.

## Blocker

Publishing requires write access to:

- `/opt/sc2027/nginx/html/login.html`
- `/opt/sc2027/nginx/conf.d/default.conf`

These paths are owned by `sc2027:sc2027` or root-owned files. The current SSH
user `deploy` cannot write them and `sudo` requires a password.

## Install Command Once Privileged Access Is Available

Copy `login.html` to:

```bash
/home/deploy/sc2027-staging/login.html
```

Then run as `root` or `sc2027`:

```bash
cd /home/deploy/sc2027-staging
/path/to/install-login-portal.sh /home/deploy/sc2027-staging/login.html
```

Or copy the local package to the server and run:

```bash
chmod +x install-login-portal.sh
./install-login-portal.sh /home/deploy/sc2027-staging/login.html
```

## Verification After Install

```bash
curl -k -I https://nortiqalab.com/login
curl -k -i -X POST https://nortiqalab.com/api/login \
  -H "Content-Type: application/json" \
  --data-binary '{"email":"nobody@example.com","password":"wrong"}'
```

Expected invalid-login result:

- HTTP `401`
- JSON: `{"success":false,"message":"Credenciales invalidas"}`

## Remaining Security Work

- `/app/` is not server-side protected yet.
- First version stores user metadata in `localStorage`.
- True session/token enforcement should be a follow-up block.

