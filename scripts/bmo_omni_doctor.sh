#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "[doctor] be-more-agent root: $ROOT"

check_cmd() {
  local cmd="$1"
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "[ok] command: $cmd"
  else
    echo "[warn] missing command: $cmd"
  fi
}

check_file() {
  local path="$1"
  if [[ -e "$path" ]]; then
    echo "[ok] file: $path"
  else
    echo "[warn] missing file: $path"
  fi
}

check_cmd python3
check_cmd ollama
check_cmd rpicam-still
check_cmd arecord
check_cmd aplay

check_file "$ROOT/agent.py"
check_file "$ROOT/config.json"
check_file "$ROOT/wakeword.onnx"
check_file "$ROOT/whisper.cpp/build/bin/whisper-cli"
check_file "$ROOT/piper/piper"

echo "[doctor] config snapshot"
python3 - <<'PY'
import json, os
cfg = {}
try:
    cfg = json.load(open('config.json'))
except Exception as e:
    print('[warn] cannot read config.json:', e)
    raise SystemExit(0)

for k in ['llm_backend','text_model','vision_model','omni_base_url','omni_model','omni_tool_route_mode','omni_fallback_to_ollama','omni_vision_mode']:
    print(f"  {k}: {cfg.get(k)}")

token_env = cfg.get('omni_token_env','PRISMBOT_API_TOKEN')
print(f"  omni_token_env: {token_env}")
print(f"  token_present: {bool(os.getenv(token_env,''))}")
PY

echo "[doctor] done"
