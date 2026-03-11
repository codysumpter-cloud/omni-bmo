#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UNIT_DIR="$HOME/.config/systemd/user"
mkdir -p "$UNIT_DIR"

cp "$ROOT/deploy/systemd/omni-council-daily.service" "$UNIT_DIR/"
cp "$ROOT/deploy/systemd/omni-council-daily.timer" "$UNIT_DIR/"
cp "$ROOT/deploy/systemd/omni-council-weekly.service" "$UNIT_DIR/"
cp "$ROOT/deploy/systemd/omni-council-weekly.timer" "$UNIT_DIR/"

systemctl --user daemon-reload
systemctl --user enable --now omni-council-daily.timer
systemctl --user enable --now omni-council-weekly.timer

echo "Council timers installed and started."
