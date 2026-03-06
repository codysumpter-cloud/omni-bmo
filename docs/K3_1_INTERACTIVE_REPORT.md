# K.3.1 Interactive Report Template

Date (UTC):
Tester:
Device:
Profile (`snappy|balanced|robust`):

## Environment snapshot

- `git rev-parse --short HEAD`:
- `python3 --version`:
- `ollama --version`:
- Audio devices detected:
- Camera detected:

## Pre-checks

- `./scripts/install_k3_deps.sh`:
  - [ ] pass
  - Notes:
- `./scripts/bmo_omni_doctor.sh`:
  - [ ] pass
  - Notes:
- `./scripts/run_validation_matrix.sh`:
  - [ ] pass
  - Notes:

## Interactive tests

### 1) Wake + short prompt latency

Prompt set (5):
- 1.
- 2.
- 3.
- 4.
- 5.

Response-start latency (seconds):
- 1.
- 2.
- 3.
- 4.
- 5.

Median:
P95:

Pass target (snappy): <= 2.5s median
- [ ] pass
- [ ] fail

### 2) Transport controls

Commands tested:
- `transport`
- `transport auto`
- `transport online`
- `transport mesh`
- `transport reticulum_fallback`
- `/doctor` / `/net-doctor`
- Hotkeys: `F6`, `F7`

Result:
- [ ] pass
- [ ] fail
Notes:

### 3) Omni failure drill

Method used to break Omni path:

Observed behavior:
- [ ] fallback engaged
- [ ] no crash
- [ ] recovered after path restored

Failover activation time:
Recovery time:

### 4) Vision-hybrid drill

Prompt:
Result:
- [ ] pass
- [ ] fail
Notes:

### 5) 30–60 minute soak

Duration:
Crashes:
Audio deadlocks:
UI freezes:

Result:
- [ ] pass
- [ ] fail

## Defects found

1.
2.
3.

## Actions taken during test

-

## Final verdict

- [ ] Ready for K.4 profile hardening
- [ ] Needs fixes before K.4

Summary:
