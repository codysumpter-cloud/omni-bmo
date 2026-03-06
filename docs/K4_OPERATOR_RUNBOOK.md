# K.4 Operator Runbook

## 1) Install deps

```bash
./scripts/install_k3_deps.sh
```

## 2) Apply profile

```bash
python3 ./scripts/apply_runtime_profile.py pi-live
# or: dev / field
```

## 3) Validate

```bash
./scripts/bmo_omni_doctor.sh
./scripts/run_validation_matrix.sh
```

## 4) Start agent

```bash
./scripts/bmo_omni_launch.sh
```

## 5) Transport controls in runtime

- Hotkeys:
  - `F6` cycle transport mode
  - `F7` transport doctor summary
- Commands:
  - `transport`
  - `transport auto|online|mesh|reticulum_fallback`
  - `/doctor`

## 6) If Omni path fails

Expected behavior:
- fallback to local ollama path (if enabled)
- `net:` mode/status updates in HUD

Check:
```bash
./scripts/bmo_omni_doctor.sh
```

## 7) Logging and reporting

- Fill `docs/K3_1_INTERACTIVE_REPORT.md` after each field test cycle.
- Track profile + latency + failover outcomes.
