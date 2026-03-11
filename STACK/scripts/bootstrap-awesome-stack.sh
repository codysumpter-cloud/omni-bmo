#!/usr/bin/env bash
set -euo pipefail

# Safe bootstrap: verifies common tools and prints install guidance.
# Does NOT force install package managers or system changes.

have() { command -v "$1" >/dev/null 2>&1; }
check() {
  local bin="$1"
  if have "$bin"; then
    echo "[PASS] $bin"
  else
    echo "[MISS] $bin"
  fi
}

echo "== PrismBot Awesome Stack Bootstrap Check =="

for b in rg fd fzf jq bat htop tmux node npm python3 pip3 git gh; do
  check "$b"
done

echo
echo "Next steps:"
echo "1) Install missing core CLI tools via your OS package manager."
echo "2) Python stack: pip install -r STACK/manifests/python-ai-requirements.txt"
echo "3) Node stack: install packages from STACK/manifests/node-core-packages.txt"
echo "4) Selfhosted stack: provision services from STACK/manifests/selfhosted-core.yml"
