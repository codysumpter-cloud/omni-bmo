#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== Omni-BMO pre-PR checks =="

# Python syntax check
python3 -m py_compile agent.py

echo "[PASS] agent.py compiles"

# Existing validation matrix if present
if [ -x "scripts/run_validation_matrix.sh" ]; then
  echo "[RUN] scripts/run_validation_matrix.sh"
  bash scripts/run_validation_matrix.sh
fi

echo "Pre-PR checks complete."
