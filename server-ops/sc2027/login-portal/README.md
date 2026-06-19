# Nortiqa Login Portal

Status: ready to install with root/sc2027 permissions

## What This Adds

- `https://nortiqalab.com/login`
- Same-origin login API proxy:
  - `POST https://nortiqalab.com/api/login`
  - proxied to `http://n8n:5678/webhook/login`

The n8n workflow `SC2027 - Login API` expects:

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

Current response contract:

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

Invalid credentials return HTTP `401`:

```json
{
  "success": false,
  "message": "Credenciales invalidas"
}
```

## Install

Copy `login.html` to the staging path:

```bash
cp login.html /home/deploy/sc2027-staging/login.html
```

Preferred path when the SSH user can run Docker commands and the Nginx host
mounts are present:

```bash
./install-login-portal-docker.sh /home/deploy/sc2027-staging/login.html
```

This starts a temporary helper container, mounts:

- `/opt/sc2027/nginx/html`
- `/opt/sc2027/nginx/conf.d`

Then it copies the page into the host-mounted HTML directory, updates
`default.conf`, validates the running `sc2027-proxy` Nginx config, and reloads
the proxy.

If ownership must be corrected after install, set it explicitly:

```bash
INSTALL_OWNER=sc2027:sc2027 ./install-login-portal-docker.sh /home/deploy/sc2027-staging/login.html
```

Alternative path when operating directly on the host Nginx bind mount as `root`
or `sc2027`:

```bash
./install-login-portal.sh /home/deploy/sc2027-staging/login.html
```

The host-path installer:

1. Copies `login.html` to `/opt/sc2027/nginx/html/login.html`.
2. Backs up `/opt/sc2027/nginx/conf.d/default.conf`.
3. Injects `/login` and `/api/login` routes.
4. Runs `nginx -t`.
5. Reloads `sc2027-proxy`.

## Verification

```bash
curl -k -I https://nortiqalab.com/login
curl -k -i -X POST https://nortiqalab.com/api/login \
  -H "Content-Type: application/json" \
  --data-binary '{"email":"nobody@example.com","password":"wrong"}'
```

Expected invalid-login result: HTTP `401` with JSON.

## Remaining Security Note

This first login version stores user metadata in `localStorage` and redirects to
`/app/`. It does not yet enforce server-side access control for `/app/`.
