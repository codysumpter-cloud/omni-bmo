## Summary
- What changed:
- Why:

## Verification
- [ ] Ran `bash scripts/omni_prepr_check.sh`
- [ ] Updated docs/config notes if behavior changed
- [ ] Included rollback/safety notes for risky changes

### Commands run
```bash
# paste commands used
```

## Prompt/Agent Logic Checklist
If this PR changes prompt/routing/tool behavior (`agent.py`, `config*`, `adapters/*`):
- [ ] Ran prompt eval baseline:
  ```bash
  cd evals/promptfoo
  npx promptfoo@latest eval -c promptfooconfig.yaml
  ```
- [ ] Noted failures/fixes in PR description
