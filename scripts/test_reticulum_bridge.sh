#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://127.0.0.1:8788/bridge}"

curl -fsS "$URL" \
  -H 'content-type: application/json' \
  -d '{"mode":"reticulum_fallback","text":"hello from omni-bmo test","messages":[{"role":"user","content":"hello"}],"client":"omni-bmo"}'

echo
