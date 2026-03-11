#!/usr/bin/env python3
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOTES = ROOT / 'data/council/votes.jsonl'
OUTDIR = ROOT / 'data/council'
OUTDIR.mkdir(parents=True, exist_ok=True)
WINDOW=30
ZERO_STREAK_LIMIT=10
MIN_SELECTION_RATE=0.05

rounds=[]
if VOTES.exists():
    for l in VOTES.read_text(encoding='utf-8').splitlines():
        try:
            r=json.loads(l)
            if isinstance(r,dict) and 'winner' in r and 'participants' in r:
                rounds.append(r)
        except: pass

name = datetime.now(timezone.utc).strftime('weekly-report-%Y-%m-%d.md')
out = OUTDIR / name
latest = OUTDIR / 'weekly-report-latest.md'

if not rounds:
    txt = '# Weekly Council Report\n\nNo council rounds logged yet.\n'
    out.write_text(txt, encoding='utf-8')
    latest.write_text(txt, encoding='utf-8')
    print(out)
    raise SystemExit

recent=rounds[-WINDOW:]
members=set()
for r in recent: members.update(r.get('participants',[]))
wins=defaultdict(int)
for r in recent: wins[r.get('winner')] += 1
streak=defaultdict(int)
for m in members:
    s=0
    for r in reversed(rounds):
        if r.get('winner')==m: break
        if m in r.get('participants',[]): s+=1
    streak[m]=s

lines=['# Weekly Council Report','',f'- Generated: {datetime.now(timezone.utc).isoformat()}',f'- Total rounds: {len(rounds)}',f'- Window: last {len(recent)} rounds','','| Member | Wins | Selection Rate | Zero-vote Streak |','|---|---:|---:|---:|']
flag=[]
for m in sorted(members):
    rate = wins[m]/max(1,len(recent))
    lines.append(f'| {m} | {wins[m]} | {rate:.2%} | {streak[m]} |')
    if streak[m] >= ZERO_STREAK_LIMIT and rate < MIN_SELECTION_RATE:
        flag.append((m,rate,streak[m]))

lines += ['','## Recommendation','']
if not flag:
    lines.append('No retire/replace action needed this week.')
else:
    lines.append('Flagged members for replace review:')
    for m,rate,z in flag:
        lines.append(f'- **{m}** (selection_rate={rate:.2%}, zero_vote_streak={z})')

text='\n'.join(lines)+'\n'
out.write_text(text,encoding='utf-8')
latest.write_text(text,encoding='utf-8')
print(out)
