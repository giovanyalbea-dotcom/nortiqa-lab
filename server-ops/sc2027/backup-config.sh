#!/usr/bin/env bash
set -euo pipefail

ROOT=/home/deploy/sc2027-staging
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
BACKUP_DIR="$ROOT/backups/$STAMP"
mkdir -p "$BACKUP_DIR" "$BACKUP_DIR/staging" "$BACKUP_DIR/prod" "$BACKUP_DIR/docker"

copy_if_readable() {
  local src="$1"
  local dst="$2"
  if [ -r "$src" ]; then
    cp -a "$src" "$dst"
  else
    printf 'SKIP unreadable: %s\n' "$src" >> "$BACKUP_DIR/backup.log"
  fi
}

record_file_meta() {
  local src="$1"
  if [ -e "$src" ]; then
    ls -l "$src" >> "$BACKUP_DIR/file-permissions.txt"
    sha256sum "$src" >> "$BACKUP_DIR/file-sha256.txt" 2>/dev/null || true
  fi
}

copy_if_readable "$ROOT/docker-compose.yml" "$BACKUP_DIR/staging/"
copy_if_readable "$ROOT/init-db.sql" "$BACKUP_DIR/staging/"
copy_if_readable "$ROOT/README.md" "$BACKUP_DIR/staging/"
copy_if_readable "$ROOT/staging-up.sh" "$BACKUP_DIR/staging/"
copy_if_readable "$ROOT/staging-up-full.sh" "$BACKUP_DIR/staging/"
copy_if_readable "$ROOT/staging-status.sh" "$BACKUP_DIR/staging/"
copy_if_readable "$ROOT/staging-down.sh" "$BACKUP_DIR/staging/"

copy_if_readable /opt/sc2027/docker-compose.yml "$BACKUP_DIR/prod/"
if [ -d /opt/sc2027/nginx/conf.d ]; then
  mkdir -p "$BACKUP_DIR/prod/nginx-conf.d"
  find /opt/sc2027/nginx/conf.d -maxdepth 1 -type f ! -name '.htpasswd*' -print | while read -r f; do
    copy_if_readable "$f" "$BACKUP_DIR/prod/nginx-conf.d/"
  done
fi

record_file_meta "$ROOT/.env"
record_file_meta /opt/sc2027/.env
record_file_meta /opt/nortiqa/agents/nortiqa-console/.env
record_file_meta /home/deploy/mcp.env

docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' > "$BACKUP_DIR/docker/containers.txt"
docker volume ls > "$BACKUP_DIR/docker/volumes.txt"
docker network ls > "$BACKUP_DIR/docker/networks.txt"

echo "Backup written to $BACKUP_DIR"
echo "Secrets were not copied; only metadata was recorded. Rotate/manual-backup secrets separately."
