#!/usr/bin/env bash
set -euo pipefail

HTML_SRC=${1:-/home/deploy/sc2027-staging/login.html}
HTML_DST=/opt/sc2027/nginx/html/login.html
NGINX_CONF=/opt/sc2027/nginx/conf.d/default.conf
STAMP=$(date -u +%Y%m%dT%H%M%SZ)

if [ ! -r "$HTML_SRC" ]; then
  echo "Missing login HTML source: $HTML_SRC" >&2
  exit 1
fi

if [ ! -w "$(dirname "$HTML_DST")" ]; then
  echo "Cannot write $(dirname "$HTML_DST"). Run as root or user sc2027." >&2
  exit 1
fi

if [ ! -w "$NGINX_CONF" ]; then
  echo "Cannot write $NGINX_CONF. Run as root or user sc2027." >&2
  exit 1
fi

cp -a "$HTML_SRC" "$HTML_DST"
cp -a "$NGINX_CONF" "$NGINX_CONF.bak-login-$STAMP"

python3 - "$NGINX_CONF" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()

routes = """
    # BEGIN NORTIQA LOGIN ROUTES
    location = /login {
        root /usr/share/nginx/html;
        try_files /login.html =404;
    }

    location = /api/login {
        proxy_pass http://n8n:5678/webhook/login;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Proto https;
        proxy_buffering off;
    }
    # END NORTIQA LOGIN ROUTES
"""

if "BEGIN NORTIQA LOGIN ROUTES" not in text:
    marker = "    location /n8n/ {"
    if marker not in text:
        raise SystemExit(f"marker not found: {marker}")
    text = text.replace(marker, routes + "\n" + marker, 1)
    path.write_text(text)
PY

docker exec sc2027-proxy nginx -t
docker exec sc2027-proxy nginx -s reload

echo "Login portal installed:"
echo "- https://nortiqalab.com/login"
echo "- POST https://nortiqalab.com/api/login"
