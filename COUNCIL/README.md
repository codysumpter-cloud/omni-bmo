# Omni-BMO Council System

Council mode is enabled for high-impact decisions and can be run as strict mode for all user-facing answers.

## Core Rules

1. Call all active council members.
2. Collect one candidate answer per member.
3. Score answers (1-5) on correctness, clarity, safety, actionability.
4. Reality Checker can veto unsafe candidates.
5. Highest score wins.
6. Log participation + winner in `data/council/votes.jsonl`.

## Active Council (default)
- frontend-developer
- ai-engineer
- rapid-prototyper
- reality-checker
- social-media-strategist
- professor-agent
- pixel-art-director
- hd-visual-video-producer

## Files
- `COUNCIL/roster.yaml`
- `COUNCIL/voting-rubric.md`
- `COUNCIL/replacement-playbook.md`
- `COUNCIL/STRICT_MODE.md`
- `scripts/council_log_round.py`
- `scripts/council_audit.py`
- `scripts/council_daily_audit.sh`
- `scripts/council_weekly_report.py`

## Automation
- Daily audit snapshot script
- Weekly retire/replace recommendation script
- Optional systemd timer units in `deploy/systemd/`
