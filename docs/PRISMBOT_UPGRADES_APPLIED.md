# PrismBot-Inspired Upgrades Applied

This repo was upgraded with high-impact workflow improvements from PrismBot.

## Added

1. **GitHub issue templates**
   - `.github/ISSUE_TEMPLATE/config.yml`
   - `.github/ISSUE_TEMPLATE/feature-task.yml`
   - `.github/ISSUE_TEMPLATE/bug-fix.yml`

2. **PR quality gate template**
   - `.github/pull_request_template.md`

3. **Prompt evaluation baseline (Promptfoo)**
   - `evals/promptfoo/promptfooconfig.yaml`
   - `evals/promptfoo/prompts/omni-bmo-assistant.txt`
   - `evals/promptfoo/README.md`
   - `.github/workflows/promptfoo-evals.yml`

4. **Pre-PR verification script**
   - `scripts/omni_prepr_check.sh`
   - Runs python compile check + existing validation matrix

## Why these upgrades

- Make changes safer and easier to review.
- Catch prompt/routing regressions earlier.
- Improve contributor consistency with scoped issue + PR structure.
- Keep shipping velocity without sacrificing quality controls.
