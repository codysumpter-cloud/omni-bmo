# Omni-BMO Phase 2 Issue Pack

Total issues: **60**

## core-runtime
1. Harden startup sequence and dependency preflight
2. Add structured runtime error catalog
3. Implement safe auto-restart policy
4. Add config schema validation at boot
5. Add backup-before-write for config updates
6. Add health endpoint summary output
7. Add latency mode switch telemetry
8. Add secure token presence checks
9. Add deterministic warmup state machine tests
10. Document failure recovery runbook

## audio-stack
1. Add microphone auto-calibration command
2. Add speaker playback self-test command
3. Add ALSA profile presets for common devices
4. Add voice activity threshold tuning helper
5. Add barge-in reliability metrics
6. Add audio device fallback selector
7. Add low-latency mode profile for Pi
8. Add audio debug snapshot export
9. Add TTS output clipping guard
10. Document audio troubleshooting decision tree

## vision-stack
1. Add camera warmup timeout fallback
2. Add vision confidence threshold policy
3. Add local frame capture diagnostics
4. Add privacy mode for camera disable/enable
5. Add rotation and framing auto-check
6. Add low-light warning detection
7. Add vision response length controls
8. Add vision model fallback behavior
9. Add camera error recovery retries
10. Document vision safety and privacy runbook

## transport-omni
1. Add transport mode telemetry counters
2. Add reticulum bridge latency metrics
3. Add network doctor enriched report
4. Add timeout profiles per runtime mode
5. Add online->mesh fallback threshold tuning
6. Add bridge auth failure diagnostics
7. Add transport health dashboard output
8. Add message retry strategy by mode
9. Add command override lock for operator
10. Document transport failover playbook

## ux-personality
1. Add concise response mode toggle
2. Add personality presets (helper/friendly/pro)
3. Add session recap command
4. Add what-changed command output
5. Add user teaching mode hints
6. Add short-vs-detailed answer setting
7. Add safe humor mode boundaries
8. Add wake acknowledgement variant selection
9. Add interaction quality feedback command
10. Document UX behavior matrix

## quality-pipeline
1. Expand promptfoo suite to 12 tests
2. Add prompt injection red-team checks
3. Add secret leakage refusal tests
4. Add CI status badge and docs
5. Add pre-PR check script to CI hard gate
6. Add weekly quality report script
7. Add regression baseline snapshots
8. Add test data fixtures for common intents
9. Add release checklist for model/prompt changes
10. Document quality governance process
