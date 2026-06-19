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

check "main site HTTPS" curl -fsS https://nortiqalab.com/
check "API health HTTPS" curl -fsS https://api.nortiqalab.com/health
check "n8n HTTPS" curl -fsS https://n8n.nortiqalab.com/
check "MCP protected HTTPS" bash -lc "code=\$(curl -k -s -o /dev/null -w '%{http_code}' https://mcp.nortiqalab.com/); test \"\$code\" = 401"
check "prod postgres healthy" bash -lc "docker inspect sc2027-db --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' | grep -qx healthy"
check "nortiqa console local health" curl -fsS http://127.0.0.1:8000/api/health
check "ollama local tags" curl -fsS http://127.0.0.1:11434/api/tags
check "nginx config syntax" docker exec sc2027-proxy nginx -t

docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
exit "$fail"
