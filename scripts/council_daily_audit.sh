#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p data/council
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
OUT="data/council/audit-${TS}.txt"
LATEST="data/council/audit-latest.txt"
{
  echo "Omni-BMO Daily Council Audit"
  echo "Timestamp: $TS"
  echo
  python3 scripts/council_audit.py
} | tee "$OUT" > "$LATEST"

echo "Wrote: $OUT"
