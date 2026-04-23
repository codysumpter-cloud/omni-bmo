# Omni-BMO Transport Contract

This document defines the runtime-facing transport contract for Omni-BMO.

## Goal

Keep transport selection predictable across the Pi runtime, bridge adapters, operator HUD, diagnostics, and downstream consumers such as `bmo-stack` and `prismtek-apps`.

## Modes

`transport_mode` accepts exactly these values:

- `online` — use the normal local network or internet path
- `mesh` — prefer MANET / mesh reachable endpoints
- `reticulum_fallback` — route concise command and text payloads through a Reticulum bridge
- `auto` — select the best available mode from health checks and explicit overrides

## Resolution rules

1. Manual override wins over automatic selection.
2. `online` is preferred when healthy because it offers the best throughput.
3. `mesh` is preferred when the IP path is unavailable but a mesh endpoint is reachable.
4. `reticulum_fallback` is the sovereignty / resilience path for control messages and compact text exchanges.
5. Runtime must never silently claim a richer mode than the one currently in use.

## Required config keys

```json
{
  "transport_mode": "auto",
  "mesh_health_check_url": "",
  "reticulum_bridge_endpoint": "",
  "reticulum_bridge_token_env": "RETICULUM_BRIDGE_TOKEN",
  "transport_failover_timeout_sec": 2.0
}
```

## Runtime state surface

Runtime should expose a state object with these fields:

- `selected_mode` — currently active mode
- `requested_mode` — configured mode or active override
- `last_reason` — human-readable reason for the last selection decision
- `online_healthy` — whether the normal path is healthy
- `mesh_healthy` — whether the mesh path is healthy
- `reticulum_available` — whether the bridge endpoint is configured and reachable
- `last_transition_at` — ISO-8601 timestamp for the last mode change
- `override_source` — `none | operator_hotkey | operator_command | config`

See `schemas/transport-state.schema.json` for the machine-checkable shape.

## Bridge expectations

The Reticulum bridge is intentionally narrow.

### Request

The bridge may accept a concise payload containing:

- user text
- request id
- timeout budget
- minimal metadata needed for routing

### Response

Preferred contract:

```json
{ "text": "..." }
```

Accepted compatibility keys:

- `text`
- `message`
- `result.text`

Bridge adapters should normalize these keys before the rest of the runtime sees the response.

## Operator UX

The runtime surface should keep the current operator-visible controls:

- HUD / status line shows `net:<mode>`
- `F6` cycles transport override
- `F7` runs transport diagnostics
- `transport` prints current state
- `transport auto|online|mesh|reticulum_fallback` sets override
- `/doctor` and `/net-doctor` emit actionable diagnostics

## Logging requirements

Every transport transition should log:

- previous mode
- new mode
- reason
- timeout / health-check result that triggered the decision
- whether the decision came from operator override or automatic resolution

## Downstream boundary

- `omni-bmo` owns the executable implementation
- `bmo-stack` should mirror this contract as the canonical operator reference
- `prismtek-apps` should only consume the product-safe subset of this state for pairing and reachability UI
