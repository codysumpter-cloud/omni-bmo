# Contributing to Omni-BMO

Thanks for contributing to `omni-bmo`.

## Scope

This repository owns device/runtime execution, transport selection, pairing state, local/offline helper behavior, and runtime-facing integrations.

It does **not** own the full product shell (`prismtek-apps`) or the deeper operator policy layer (`bmo-stack`).

## Working rules

1. Open a branch first.
2. Open a draft PR early.
3. Keep changes scoped.
4. Do not merge until all required GitHub checks are green.
5. Do not let the lead branch go red.
6. Keep runtime truth explicit: degraded, fallback, and offline states must never be hidden.

## Pull request expectations

Every PR should explain:

- what changed
- why it belongs in `omni-bmo`
- how runtime behavior was verified
- how to roll back safely

## Local validation

At minimum, validate the runtime files you changed.

Useful commands:

```bash
python -m py_compile $(find . -name '*.py' -not -path './venv/*')
```

If you touch JSON config or examples, validate they still parse.

## Security and secrets

- never commit live bridge tokens or secrets
- use placeholders in examples
- redact logs and screenshots before sharing
- report sensitive issues privately as described in `SECURITY.md`
