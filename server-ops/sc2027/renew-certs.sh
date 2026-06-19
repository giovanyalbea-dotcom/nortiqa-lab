#!/usr/bin/env bash
set -euo pipefail

MODE=${1:-renew}
CERTBOT_IMAGE=${CERTBOT_IMAGE:-certbot/certbot:latest}
PROXY_CONTAINER=${PROXY_CONTAINER:-sc2027-proxy}
LETSENCRYPT_DIR=${LETSENCRYPT_DIR:-/opt/sc2027/letsencrypt}
WEBROOT_DIR=${WEBROOT_DIR:-/opt/sc2027/nginx/certbot}

args=(renew --webroot -w /var/www/certbot)

case "$MODE" in
  renew)
    args+=(--quiet)
    ;;
  dry-run)
    args+=(--dry-run)
    ;;
  *)
    echo "Usage: $0 [renew|dry-run]" >&2
    exit 2
    ;;
esac

docker run --rm \
  -v "$LETSENCRYPT_DIR:/etc/letsencrypt" \
  -v "$WEBROOT_DIR:/var/www/certbot" \
  "$CERTBOT_IMAGE" "${args[@]}"

docker exec "$PROXY_CONTAINER" nginx -t
docker exec "$PROXY_CONTAINER" nginx -s reload
