# Omni-BMO Phase 2 Backlog

## Reliability
- [ ] Add structured error code map for runtime failures
- [ ] Add watchdog heartbeat monitor
- [ ] Add safe auto-restart strategy after recoverable failures
- [ ] Add startup self-test summary output

## Audio Path
- [ ] Add dynamic mic gain calibration command
- [ ] Add speaker output sanity test command
- [ ] Add audio device profile presets (USB mic/headset)
- [ ] Add audio troubleshooting quick doctor report

## Vision Path
- [ ] Add camera warmup timeout fallback
- [ ] Add vision confidence guardrails in responses
- [ ] Add local frame capture diagnostics
- [ ] Add explicit privacy mode toggle for camera use

## Omni Transport
- [ ] Add transport fallback metrics counters
- [ ] Add Reticulum bridge latency telemetry
- [ ] Add `/transport doctor` richer output
- [ ] Add adaptive timeout profile by mode (field/dev/live)

## Safety + Ops
- [ ] Add no-secrets logging guard
- [ ] Add config schema validation at boot
- [ ] Add safe config backup before writes
- [ ] Add one-command rollback script

## Product UX
- [ ] Add concise personality modes (helper/friendly/pro)
- [ ] Add response length controls
- [ ] Add session recap command
- [ ] Add simple "what changed" changelog command

## Quality Pipeline
- [ ] Expand Promptfoo tests to 10+ cases
- [ ] Add red-team config for prompt injection and secret leakage
- [ ] Add CI gate for pre-PR checks on core files
- [ ] Add weekly upgrade audit script
