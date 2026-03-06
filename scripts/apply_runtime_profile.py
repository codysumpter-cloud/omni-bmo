#!/usr/bin/env python3
"""Apply JSON profile overrides to config.json for K.4 runtime presets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("profile", help="profile name (e.g. dev, pi-live, field)")
    ap.add_argument("--config", default="config.json")
    ap.add_argument("--profiles-dir", default="config/profiles")
    args = ap.parse_args()

    cfg_path = Path(args.config)
    profiles_dir = Path(args.profiles_dir)
    profile_path = profiles_dir / f"{args.profile}.json"

    if not profile_path.exists():
        raise SystemExit(f"Profile not found: {profile_path}")

    base = {}
    if cfg_path.exists():
        base = json.loads(cfg_path.read_text(encoding="utf-8"))

    override = json.loads(profile_path.read_text(encoding="utf-8"))
    base.update(override)

    cfg_path.write_text(json.dumps(base, indent=4) + "\n", encoding="utf-8")
    print(f"Applied profile '{args.profile}' to {cfg_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
