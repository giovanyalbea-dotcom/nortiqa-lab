#!/usr/bin/env bash
set -euo pipefail

fail=0
check() {
  local name="$1"
  shift
  if "$@" >/tmp/healthcheck.out 2>/tmp/healthcheck.err; then
    echo "OK   $name"
  else
    echo "FAIL $name"
    cat /tmp/healthcheck.err || true
    fail=1
  fi
}

cd /home/deploy/sc2027-staging
check "staging compose ps" docker compose ps
check "staging QueryOS HTTP" curl -fsS http://127.0.0.1:18501/app/
check "staging postgres healthy" bash -lc "docker inspect sc2027-staging-db --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' | grep -qx healthy"

if docker ps --format '{{.Names}}' | grep -qx sc2027-staging-n8n; then
  check "staging n8n HTTP" curl -fsS http://127.0.0.1:15678/
else
  echo "SKIP staging n8n not running"
fi

if docker ps --format '{{.Names}}' | grep -qx sc2027-staging-metabase; then
  check "staging metabase HTTP" curl -fsS http://127.0.0.1:13000/
else
  echo "SKIP staging metabase not running"
fi

docker logs --tail 80 sc2027-staging-queryos 2>&1 | grep -Ei 'error|exception|traceback' && fail=1 || true
exit "$fail"
