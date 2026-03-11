#!/usr/bin/env bash
set -euo pipefail

# Omni-BMO host bootstrap helper (Ubuntu/Debian)
# Requires sudo privileges for package installation.

echo "== Omni-BMO Bootstrap =="

echo "[1/4] Install core CLI + runtime dependencies"
sudo apt-get update
sudo apt-get install -y \
  ripgrep fd-find fzf bat jq \
  docker.io docker-compose-plugin \
  python3-venv python3-pip \
  libasound2-dev portaudio19-dev ffmpeg

echo "[2/4] Alias ubuntu binary names"
mkdir -p "$HOME/.local/bin"
command -v fd >/dev/null 2>&1 || ln -sf "$(command -v fdfind)" "$HOME/.local/bin/fd"
command -v bat >/dev/null 2>&1 || ln -sf "$(command -v batcat)" "$HOME/.local/bin/bat"
if ! grep -q 'HOME/.local/bin' "$HOME/.bashrc"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi


echo "[3/4] Python env"
if [ ! -d venv ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt


echo "[4/4] Quick checks"
rg --version || true
fd --version || true
bat --version || true
docker --version || true

echo "Bootstrap complete. Run: bash scripts/omni_prepr_check.sh"
