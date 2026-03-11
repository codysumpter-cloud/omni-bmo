#!/usr/bin/env python3
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOTES = ROOT / 'data/council/votes.jsonl'
VOTES.parent.mkdir(parents=True, exist_ok=True)

p = argparse.ArgumentParser()
p.add_argument('--question', required=True)
p.add_argument('--participants', required=True)
p.add_argument('--winner', required=True)
a = p.parse_args()

record = {
  'timestamp': datetime.now(timezone.utc).isoformat(),
  'question': a.question,
  'participants': [x.strip() for x in a.participants.split(',') if x.strip()],
  'winner': a.winner.strip()
}

with VOTES.open('a', encoding='utf-8') as f:
  f.write(json.dumps(record) + '\n')

print('Logged:', record)
