# K.3 Baseline Report — Transport Lab Bring-up

Date (UTC): 2026-03-06
Repo: `omni-bmo`

## Scope

- Validate local Reticulum bridge mock path
- Run static validation matrix
- Record blockers for full interactive transport drills

## Executed checks

### 1) Reticulum bridge mock (local)

Command sequence:

```bash
python3 adapters/reticulum_bridge_mock.py --host 127.0.0.1 --port 8788
scripts/test_reticulum_bridge.sh http://127.0.0.1:8788/bridge
```

Observed result:

- ✅ Pass
- Response:
  - `[reticulum-mock:<ts>] relay acknowledged: hello from omni-bmo test`

Conclusion:
- Reticulum fallback request/response contract is functioning against local mock.

### 2) Validation matrix static checks

Command:

```bash
./scripts/run_validation_matrix.sh
```

Observed result:

- ✅ Pass (static checks)
- config sanity: OK
- compile checks: OK

### 3) Environment blockers for full end-to-end interaction tests

- `rpicam-still` missing
- `arecord` missing
- `aplay` missing
- `whisper.cpp/build/bin/whisper-cli` missing
- `piper/piper` missing

These prevent full wake/STT/TTS field-loop verification on this host.

## K.3 status

- ✅ Reticulum mock path verified
- ✅ Static validation matrix verified
- ⚠️ Full interactive voice/camera transport drills pending device/runtime deps

## Recommended next actions

1. Install missing media/runtime dependencies on target device using:
   - `./scripts/install_k3_deps.sh`
2. Set `reticulum_bridge_endpoint` to local mock and run voice-loop fallback drill.
3. Add one mesh health endpoint and run `transport auto` failover checks with doctor logs.
4. Record latency/failover timings in this report as K.3.1.
