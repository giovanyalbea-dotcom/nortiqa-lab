#!/usr/bin/env bash
set -euo pipefail

HTML_SRC=${1:-/home/deploy/sc2027-staging/login.html}
PROXY_CONTAINER=${PROXY_CONTAINER:-sc2027-proxy}
HELPER_IMAGE=${HELPER_IMAGE:-nginx:alpine}
HOST_HTML_DIR=${HOST_HTML_DIR:-/opt/sc2027/nginx/html}
HOST_CONF_DIR=${HOST_CONF_DIR:-/opt/sc2027/nginx/conf.d}
INSTALL_OWNER=${INSTALL_OWNER:-}

if [ ! -r "$HTML_SRC" ]; then
  echo "Missing login HTML source: $HTML_SRC" >&2
  exit 1
fi

docker run --rm -i \
  -e INSTALL_OWNER="$INSTALL_OWNER" \
  -v "$HTML_SRC:/src/login.html:ro" \
  -v "$HOST_HTML_DIR:/html" \
  -v "$HOST_CONF_DIR:/conf" \
  "$HELPER_IMAGE" sh -s <<'SH'
set -eu

NGINX_CONF=/conf/default.conf
STAMP=$(date -u +%Y%m%dT%H%M%SZ)

cp /src/login.html /html/login.html
cp -a "$NGINX_CONF" "$NGINX_CONF.bak-login-$STAMP"

if ! grep -q "BEGIN NORTIQA LOGIN ROUTES" "$NGINX_CONF"; then
  awk '
    /    location \/n8n\/ \{/ && ! inserted {
      print "    # BEGIN NORTIQA LOGIN ROUTES"
      print "    location = /login {"
      print "        root /usr/share/nginx/html;"
      print "        try_files /login.html =404;"
      print "    }"
      print ""
      print "    location = /api/login {"
      print "        proxy_pass http://n8n:5678/webhook/login;"
      print "        proxy_http_version 1.1;"
      print "        proxy_set_header Host $host;"
      print "        proxy_set_header X-Real-IP $remote_addr;"
      print "        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;"
      print "        proxy_set_header X-Forwarded-Host $host;"
      print "        proxy_set_header X-Forwarded-Proto https;"
      print "        proxy_buffering off;"
      print "    }"
      print "    # END NORTIQA LOGIN ROUTES"
      print ""
      inserted = 1
    }
    { print }
  ' "$NGINX_CONF" > "$NGINX_CONF.tmp"
  mv "$NGINX_CONF.tmp" "$NGINX_CONF"
fi

if [ -n "${INSTALL_OWNER:-}" ]; then
  chown "$INSTALL_OWNER" /html/login.html "$NGINX_CONF"
fi
SH

docker exec "$PROXY_CONTAINER" nginx -t
docker exec "$PROXY_CONTAINER" nginx -s reload

echo "Login portal installed:"
echo "- https://nortiqalab.com/login"
echo "- POST https://nortiqalab.com/api/login"
