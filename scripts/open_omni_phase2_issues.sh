#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-codysumpter-cloud/omni-bmo}"
JSON_FILE="PROJECTS/omni-phase2-issues.json"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found"
  exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "gh auth missing. Run: gh auth login"
  exit 1
fi
if [ ! -f "$JSON_FILE" ]; then
  echo "Missing $JSON_FILE"
  exit 1
fi

for lbl in phase-2 feature; do
  gh label create "$lbl" --repo "$REPO" --force >/dev/null 2>&1 || true
done

python3 - "$REPO" "$JSON_FILE" <<'PY'
import json, subprocess, sys
repo, jf = sys.argv[1], sys.argv[2]
items = json.load(open(jf))
for i,it in enumerate(items,1):
    cmd=['gh','issue','create','--repo',repo,'--title',it['title'],'--body',it['body'],'--label',','.join(it.get('labels',[]))]
    print(f"[{i}/{len(items)}] {it['title']}")
    subprocess.run(cmd, check=True)
print('Done')
PY
