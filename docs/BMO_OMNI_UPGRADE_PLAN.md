# BMO × Omni Upgrade Plan (Non-Destructive)

This plan **builds on** be-more-agent and avoids rewriting stable upstream logic.

## Guardrails

- Keep upstream wake/STT/TTS/GUI loop intact.
- Add Omni as an optional backend layer (`llm_backend=omni`).
- Preserve local fallback (`omni_fallback_to_ollama=true`).
- Keep all additions configurable and reversible.

## Current Completed Milestones

- Milestone A: Omni backend adapter behind config flag.
- Milestone B: direct tool-route mode + streaming chunk tuning.
- Milestone C: vision-hybrid mode + hard fallback ladder.

## Next Delivery Milestones

### Milestone D (Ops hardening)
- systemd service template
- env file template
- launch wrapper + health checks
- one-command diagnostics (`doctor`)

### Milestone E (Voice/Wake polish)
- voice latency tuning profile
- wake-word threshold tuning profile
- interrupt behavior tuning for faster barge-in

### Milestone F (Validation matrix)
- wake -> transcribe -> answer -> speak latency benchmarks
- offline/no-network behavior checks
- Omni endpoint down fallback verification

## Runtime profiles (target)

- `desktop-dev` (fast iteration)
- `pi-live` (stable, low-jitter)
- `demo-mode` (showcase)

## Definition of done (BMO v1)

- wake word works reliably in room noise
- response starts in <= 2.5s median for simple prompts
- graceful fallback to local ollama if Omni endpoint fails
- no crashes over 1h continuous conversation test
