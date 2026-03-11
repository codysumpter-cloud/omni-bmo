#!/usr/bin/env python3
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOTES = ROOT / 'data/council/votes.jsonl'
WINDOW = 30
ZERO_STREAK_LIMIT = 10
MIN_SELECTION_RATE = 0.05


def load_rounds():
    if not VOTES.exists():
        return []
    rounds = []
    for line in VOTES.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
            if isinstance(r, dict) and 'winner' in r and 'participants' in r:
                rounds.append(r)
        except json.JSONDecodeError:
            pass
    return rounds


def main():
    rounds = load_rounds()
    if not rounds:
        print('No council rounds logged yet.')
        return

    recent = rounds[-WINDOW:]
    members = set()
    for r in recent:
        members.update(r.get('participants', []))

    wins = defaultdict(int)
    for r in recent:
        wins[r.get('winner')] += 1

    streak = defaultdict(int)
    for m in members:
        s = 0
        for r in reversed(rounds):
            if r.get('winner') == m:
                break
            if m in r.get('participants', []):
                s += 1
        streak[m] = s

    print(f'Rounds analyzed: total={len(rounds)} recent={len(recent)}')
    flagged = []
    for m in sorted(members):
        rate = wins[m] / max(1, len(recent))
        z = streak[m]
        print(f'- {m}: wins={wins[m]} selection_rate={rate:.2%} zero_vote_streak={z}')
        if z >= ZERO_STREAK_LIMIT and rate < MIN_SELECTION_RATE:
            flagged.append((m, rate, z))

    if not flagged:
        print('No members flagged for replacement.')
    else:
        print('Flagged members:')
        for m, rate, z in flagged:
            print(f'* {m} (selection_rate={rate:.2%}, zero_vote_streak={z})')


if __name__ == '__main__':
    main()
