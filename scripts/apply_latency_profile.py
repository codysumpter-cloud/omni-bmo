#!/usr/bin/env python3
"""Apply latency tuning profile to be-more-agent config.json.

Profiles:
- snappy: fastest interactions, more aggressive endpointing
- balanced: default compromise
- robust: more tolerant in noisy environments
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PROFILES = {
    "snappy": {
        "wake_word_threshold": 0.43,
        "ptt_toggle_debounce_sec": 0.20,
        "adaptive_pre_record_sec": 0.12,
        "ptt_pre_record_sec": 0.08,
        "silence_threshold": 0.0060,
        "silence_duration_sec": 0.55,
        "max_record_time_sec": 8.0,
        "tts_tail_sec": 0.12,
        "thinking_sound_initial_delay_sec": 0.15,
    },
    "balanced": {
        "wake_word_threshold": 0.45,
        "ptt_toggle_debounce_sec": 0.25,
        "adaptive_pre_record_sec": 0.20,
        "ptt_pre_record_sec": 0.15,
        "silence_threshold": 0.0055,
        "silence_duration_sec": 0.65,
        "max_record_time_sec": 8.0,
        "tts_tail_sec": 0.20,
        "thinking_sound_initial_delay_sec": 0.25,
    },
    "robust": {
        "wake_word_threshold": 0.50,
        "ptt_toggle_debounce_sec": 0.30,
        "adaptive_pre_record_sec": 0.30,
        "ptt_pre_record_sec": 0.20,
        "silence_threshold": 0.0050,
        "silence_duration_sec": 0.85,
        "max_record_time_sec": 10.0,
        "tts_tail_sec": 0.28,
        "thinking_sound_initial_delay_sec": 0.35,
    },
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("profile", choices=sorted(PROFILES.keys()))
    ap.add_argument("--config", default="config.json")
    args = ap.parse_args()

    p = Path(args.config)
    cfg = {}
    if p.exists():
        cfg = json.loads(p.read_text(encoding="utf-8"))

    cfg.update(PROFILES[args.profile])
    p.write_text(json.dumps(cfg, indent=4) + "\n", encoding="utf-8")
    print(f"Applied profile '{args.profile}' to {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
