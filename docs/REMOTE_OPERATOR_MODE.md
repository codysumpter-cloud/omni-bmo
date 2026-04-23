# Remote Operator Mode

This runbook defines the intended split between resilient control and rich remote access for Omni-BMO.

## Goal

Give operators two dependable paths:

1. **Resilient control path** for low-bandwidth text, command, and status exchange
2. **Rich remote session path** for full desktop, UI, and troubleshooting workflows

## Recommended stack split

### Path A — resilient control

Use Reticulum ecosystem tooling for off-network or degraded-network control:

- Sideband for encrypted messaging and operator-side control workflows
- RNode / Reticulum transports for resilient delivery
- bridge adapter for concise request/response exchange with Omni-BMO

This path is for:

- command and control
- short text prompts and replies
- transport diagnostics
- heartbeat / reachability
- emergency fallback when richer IP connectivity is unavailable

This path is **not** the primary channel for heavy media or full desktop streaming.

### Path B — rich remote session

Use Sunshine on the host and Moonlight on the client for low-latency remote UI access.

This path is for:

- remote desktop interaction
- GUI debugging
- full operator workflows that need the running app surface
- vision / camera assisted workflows where a richer session is appropriate

## Decision rules

Prefer these operating states:

1. **Normal case:** `online` transport + Sunshine/Moonlight available as needed
2. **Degraded IP case:** `mesh` transport if reachable
3. **No useful IP path:** `reticulum_fallback` for compact control traffic
4. **Do not block operator control** just because the rich streaming path is unavailable

## Product boundary

- `omni-bmo` owns host-side runtime behavior, transport decisions, and bridge adapters
- `bmo-stack` owns the mirrored operator contract and runbooks
- `prismtek-apps` may show paired / reachable / degraded status, but should not inherit the full field-ops surface

## Recommended operator states

### Connected

- online path healthy
- rich remote session optional
- HUD shows current transport and no degradation warning

### Degraded

- online path unhealthy
- mesh reachable or Reticulum bridge available
- operator alerted that fallback is active

### Remote session only

- rich stream works
- runtime may still be using online or mesh underneath
- remote UI access should not misrepresent transport health

### Control only

- Reticulum bridge available
- rich remote session unavailable
- only compact command/status flows should be assumed

## Minimum status fields to expose

- runtime pairing state
- selected transport mode
- last transport decision reason
- whether remote session endpoint is available
- whether only control-mode is available
- last successful heartbeat timestamp

## Validation checklist

- verify `transport` reports the active mode accurately
- verify manual override still works while remote session tools are available
- verify loss of Sunshine / Moonlight does not break text control
- verify loss of normal IP path still permits fallback control when the bridge is healthy
- verify diagnostics can tell the operator whether they have full remote access or control-only access

## Follow-on implementation notes

Suggested follow-on files:

- `schemas/transport-state.schema.json`
- paired endpoint metadata for remote session reachability
- a compact operator summary command that reports:
  - transport mode
  - bridge health
  - mesh health
  - remote session availability
