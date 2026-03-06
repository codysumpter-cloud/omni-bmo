# ATAK Integration Plan (Milestone K)

This plan layers ATAK interoperability into Omni-BMO without replacing upstream be-more-agent architecture.

## Credit / upstream

- ATAK-CIV: `deptofdefense/AndroidTacticalAssaultKit-CIV`
- Reticulum/RNode ecosystem: Mark Qvist + community
- Haven/OpenMANET stack references from buildwithparallel
- Omni-BMO remains an extension project built on `brenpoly/be-more-agent`

## Integration approach

Treat ATAK as an external operations client and bridge through transport adapters.

### K1. Data model alignment

Define normalized event envelope used by Omni-BMO and bridge(s):

```json
{
  "id": "uuid",
  "ts": 1700000000000,
  "source": "omni-bmo",
  "type": "text|telemetry|location|alert|command",
  "payload": {"...": "..."}
}
```

### K2. Reticulum bridge contract (implemented + documented)

Omni-BMO currently sends to `reticulum_bridge_endpoint` in fallback mode.

Request:

```json
{
  "mode": "reticulum_fallback",
  "text": "user utterance",
  "messages": [{"role": "user", "content": "..."}],
  "client": "omni-bmo"
}
```

Accepted response keys:
- `text`
- `message`
- `result.text`

### K3. ATAK adapter boundary

Do NOT embed ATAK internals into core voice loop.

Create adapter boundary:
- `adapters/atak_bridge.py` (future)
- inputs: normalized event envelope
- outputs: normalized event envelope

This keeps Omni-BMO decoupled and testable.

### K4. Security & access

- bearer token auth for bridge endpoints
- explicit allowlist of commands that can execute remotely
- no arbitrary shell command passthrough

### K5. Validation goals

- transport failover still works when ATAK bridge unavailable
- command latency remains acceptable in `online` mode
- no crash in voice loop when adapter times out

## Immediate next tasks

1. Add local reticulum bridge mock service for deterministic tests
2. Add adapter interface docs for ATAK bridge
3. Add simple replay test fixture for fallback payloads
