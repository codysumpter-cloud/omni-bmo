# Omni-BMO Validation Matrix (Milestone I)

Run this before declaring a profile/build stable.

## Preconditions

- `agent.py` starts successfully
- `config.json` exists and points to intended backend
- `./scripts/bmo_omni_doctor.sh` returns expected dependency status

## Test Matrix

### 1) Wake + STT + TTS loop
- Trigger wake (or PTT)
- Speak short prompt: "what time is it"
- Verify: state transitions `listening -> thinking -> speaking -> idle`
- Verify response heard clearly

### 2) Snappy profile latency check
- Apply `snappy` profile
- Ask 5 short prompts
- Target: response start in <= 2.5s median (device-dependent)

### 3) Transport controls
- Run `transport`
- Run `transport online`, `transport auto`
- Press `F6` cycle mode
- Press `F7` doctor summary
- Verify HUD shows `net:<mode>`

### 4) Omni failure fallback
- Temporarily break Omni endpoint (or set invalid `omni_base_url`)
- Ask a prompt
- Verify no crash and fallback behavior engages

### 5) Vision-hybrid check
- Trigger camera intent ("what do you see")
- Verify image capture + response generation

### 6) Long-run stability
- Continuous interaction for 30–60 minutes
- Verify: no lockups, no runaway audio process, no unrecoverable error state

## Pass Criteria

- No crashes during matrix
- Core wake/speak loop always recovers to `idle`
- Transport controls and diagnostics produce deterministic results
- Fallback path works when Omni is unavailable

## Notes

Keep results in an ops log (date/profile/device) to compare regressions over time.
