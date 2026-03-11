# Omni-BMO Full Upgrade Playbook

This repo has been upgraded with PrismBot workflow standards.

## Included Upgrades

1. **Issue/PR governance**
   - Feature/Bug/Spike templates
   - PR template with verification and prompt-eval checklist

2. **Prompt quality pipeline**
   - Promptfoo baseline eval config
   - CI workflow to run evals on prompt/routing changes

3. **Core CI safety checks**
   - `omni-ci.yml` compile + pre-PR checks

4. **Pre-PR local checks**
   - `scripts/omni_prepr_check.sh`

5. **Host bootstrap helper**
   - `scripts/bootstrap_omni_stack.sh`

6. **Upgrade integrity check**
   - `scripts/omni_upgrade_check.sh`

7. **Phase 2 backlog**
   - `PROJECTS/OMNI_PHASE2_BACKLOG.md`

## First run sequence

```bash
bash scripts/bootstrap_omni_stack.sh
bash scripts/omni_prepr_check.sh
bash scripts/omni_upgrade_check.sh
```

## Team rule
- Small scoped changes
- Verify before merge
- Keep rollback path explicit for risky changes
