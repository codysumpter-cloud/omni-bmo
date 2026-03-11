#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail=0
check() {
  local p="$1"
  if [ -e "$p" ]; then
    echo "[PASS] $p"
  else
    echo "[FAIL] $p"
    fail=$((fail+1))
  fi
}

echo "== Omni-BMO Upgrade Integrity Check =="
check ".github/ISSUE_TEMPLATE/feature-task.yml"
check ".github/ISSUE_TEMPLATE/bug-fix.yml"
check ".github/ISSUE_TEMPLATE/experiment-spike.yml"
check ".github/pull_request_template.md"
check ".github/workflows/promptfoo-evals.yml"
check ".github/workflows/omni-ci.yml"
check "evals/promptfoo/promptfooconfig.yaml"
check "scripts/omni_prepr_check.sh"
check "scripts/bootstrap_omni_stack.sh"
check "docs/OMNI_FULL_UPGRADE_PLAYBOOK.md"
check "PROJECTS/OMNI_PHASE2_BACKLOG.md"

if [ "$fail" -eq 0 ]; then
  echo "All upgrade assets present."
  exit 0
else
  echo "$fail check(s) failed."
  exit 1
fi
