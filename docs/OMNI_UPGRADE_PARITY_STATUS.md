# Omni-BMO Upgrade Parity Status

This repo now includes the same major upgrade systems added today in PrismBot:

## Included in codebase
- Council governance + strict mode + replacement policy
- Daily/weekly audit + reports + timer units
- Issue/PR templates
- Promptfoo eval baseline + redteam config + CI workflow
- Pre-PR checks
- Bootstrap/install scripts
- Phase 2 backlog + issue pack scripts
- Curated STACK manifests and self-hosted Sprint 2 configs (`STACK/`)

## Important: host-level installs are not automatic by git push
CLI tools/services still must be installed on the target machine by running install commands.

Use:
```bash
bash scripts/bootstrap_omni_stack.sh
```

That installs:
- ripgrep, fd-find, fzf, bat, jq
- docker + compose plugin
- python venv + requirements

Then run:
```bash
bash scripts/omni_prepr_check.sh
bash scripts/omni_upgrade_check.sh
```
