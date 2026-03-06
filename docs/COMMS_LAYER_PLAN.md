# Omni-BMO Communications Layer Plan

Goal: make Omni-BMO resilient beyond normal internet/Wi-Fi by layering mesh + Reticulum paths.

## Credit & upstream context

This plan builds on open projects and does not replace them:
- Haven MANET toolkit: `buildwithparallel/haven-manet-ip-mesh-radio`
- OpenMANET firmware
- RNode ecosystem and Reticulum by Mark Qvist
- Sideband client (`markqvist/Sideband`)

We are extending the stack for Omni-BMO integration.

---

## Architecture target

### Mode 1: Online (default)
- Omni-BMO uses normal local network / internet path.
- Lowest friction and best throughput.

### Mode 2: Mesh (MANET)
- Omni-BMO reaches peers/services over Haven/OpenMANET BATMAN-adv mesh.
- No central infrastructure required.

### Mode 3: Resilient fallback (Reticulum)
- If IP path is unavailable, use Reticulum message relay for command/control and text payloads.
- Prioritize reliability and sovereignty over bandwidth.

---

## Milestone F — Lab comms baseline (software-first)

### F1. Reticulum + Sideband baseline
- Install Sideband in host lab
- Verify two endpoints can exchange encrypted messages
- Validate identity creation and peer reachability

Success criteria:
- message exchange works both directions
- restart does not break identity/store

### F2. Haven/OpenMANET 2-node simulation plan
- Define Gate + Point test topology
- Document script paths used from Haven repo
- Capture expected IP ranges, service endpoints, and diagnostics

Success criteria:
- known-good runbook exists
- expected node discovery and access paths documented

---

## Milestone G — Omni-BMO transport abstraction

Add a lightweight transport selector (no core loop rewrite):

`transport_mode = online | mesh | reticulum_fallback | auto`

### G1. Config additions
- `transport_mode`
- `mesh_health_check_url`
- `reticulum_bridge_endpoint` (future relay)
- `transport_failover_timeout_sec`

### G2. Runtime behavior
- `online`: use current Omni endpoint
- `mesh`: prefer mesh endpoint / routes
- `reticulum_fallback`: route concise command packets via relay adapter
- `auto`: health-check based failover order

Success criteria:
- mode can be switched without restarting entire app
- fallback decision logged and visible in HUD/status line

---

## Milestone H — Operator UX

### H1. Status visibility
- show transport mode in HUD
- show last failover reason

### H2. Manual control
- hotkey/command for mode override
- command to print connectivity diagnostics

Success criteria:
- operator can force mode in real-time
- diagnostics produce actionable output in < 3s

---

## Validation matrix

### Core checks
- Online path latency
- Mesh path reachability
- Reticulum fallback message delivery
- Recovery after link restoration

### Failure drills
- kill upstream internet
- break primary Omni endpoint
- verify fallback path still receives/responds

---

## Not in scope (yet)

- Final enclosure wiring and shell integration
- RF antenna optimization for production field ranges
- ATAK mission integration details (future extension)

---

## Immediate next actions

1) Add transport config placeholders to `config.json`
2) Add health-check/transport decision helper in `agent.py`
3) Add HUD status line for selected transport mode
4) Build minimal `reticulum_fallback` adapter interface (stub + logging)
