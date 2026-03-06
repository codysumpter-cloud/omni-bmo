#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "[matrix] Omni-BMO validation start"

echo "[matrix] 1/4 doctor"
./scripts/bmo_omni_doctor.sh

echo "[matrix] 2/4 py compile"
python3 -m py_compile agent.py

echo "[matrix] 3/4 apply balanced latency profile"
python3 ./scripts/apply_latency_profile.py balanced --config config.json

echo "[matrix] 4/4 config sanity"
python3 - <<'PY'
import json
cfg=json.load(open('config.json'))
required=['llm_backend','omni_base_url','transport_mode','omni_tool_route_mode']
missing=[k for k in required if k not in cfg]
if missing:
  raise SystemExit(f"missing config keys: {missing}")
print('config ok:', {k:cfg.get(k) for k in required})
PY

echo "[matrix] Static checks passed. Run manual interaction tests from docs/VALIDATION_MATRIX.md"
