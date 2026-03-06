# OpenMANET Upstream Tracking (Milestone K.2)

Purpose: keep Omni-BMO aligned with upstream OpenMANET/Haven ecosystem without unnecessary forking.

## Core upstream repos to track

- `OpenMANET/docs`
  - deployment docs, runbooks, architecture guidance
- `OpenMANET/firmware`
  - OpenWRT firmware baseline
- `OpenMANET/openmanetd`
  - low-level configuration/control daemon
- `OpenMANET/atakmaps`
  - ATAK map project resources
- `OpenMANET/packages` + `OpenMANET/packages-repo`
  - package and build artifacts

## Policy (important)

1. Prefer upstream consumption over local forks.
2. Only fork when:
   - patch is required for Omni-BMO compatibility, and
   - upstream contribution path is prepared/documented.
3. Keep Omni-BMO changes in adapters/integration layers, not in upstream internals.
4. Re-check upstream updates on a recurring cadence (weekly/biweekly).

## Suggested cadence

- Weekly upstream scan:
  - docs changes
  - firmware release changes
  - daemon protocol updates
- Monthly compatibility check against current Omni-BMO transport assumptions

## Minimal check commands

```bash
# Track open issues and release activity manually in browser or API.
# For code sync baseline:

git ls-remote https://github.com/OpenMANET/docs.git HEAD
git ls-remote https://github.com/OpenMANET/firmware.git HEAD
git ls-remote https://github.com/OpenMANET/openmanetd.git HEAD
git ls-remote https://github.com/OpenMANET/atakmaps.git HEAD
```

## Notes for Omni-BMO

- We are not replacing OpenMANET; we are integrating transport awareness into Omni-BMO.
- ATAK integration should remain adapter-driven and externalized.
- Reticulum fallback stays bridge-based to keep core voice loop stable.
