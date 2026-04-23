# Omni-BMO Source Upgrade Plan

## Purpose

This document captures the external upgrade signals feeding Omni-BMO and maps them to the correct repo owners.

## Source inputs used in this pass

- Parallel / Reticulum field networking material
- `markqvist/Sideband`
- `unsigned.io/rnode`
- Sunshine host documentation
- Moonlight client documentation
- `brenpoly/be-more-agent`
- linked BMO upgrade videos, including the embodied and printer direction as an experimental hardware track

## Stable upgrade tracks

### 1. Mesh-first transport posture

Omni-BMO should keep transport as a first-class runtime concern.

Keep and deepen:
- `transport_mode` routing
- `auto | online | mesh | reticulum_fallback`
- transport doctor flows
- bridge endpoint failover
- operator-visible health summaries

Direct additions:
- Sideband-compatible message and telemetry posture
- Reticulum-native bridge contracts
- RNode-aware field profiles
- OpenMANET-style hybrid mesh readiness notes
- neighborhood, city, tunnel, and relay deployment profiles

### 2. Remote operator surface

Sunshine + Moonlight belongs in the Omni-BMO ecosystem as a remote operations path.

Treat it as:
- operator assist
- low-latency remote control
- remote field support
- screen and session handoff for maintenance and demos

### 3. Embodied hardware expansion

The embodied BMO upgrade path remains valid.

Safe direction:
- camera-aware embodied agent
- audio-first local interaction
- field and mobile transport awareness
- optional print and capture output path

Important honesty rule:
- the linked Odradek and printer direction is promising, but it remains experimental until its electrical, print, spool, and command contract is written down in-repo

## Ownership split

### Omni-BMO should own
- embodied runtime behavior
- transport routing and failover logic
- bridge contracts for mesh and Reticulum
- field hardware profiles
- remote ops runtime glue
- local diagnostics and embodied operator loops

### BMO Stack should absorb
- policy language for mesh and remote ops safety
- operator runbooks
- validation matrices
- capability taxonomy
- cross-repo ownership rules
- execution and approval posture for remote interventions

### Prismtek Apps should absorb
- product-facing capability manifests
- app-level transport status surfaces
- remote ops entrypoints and product framing
- Buddy-facing bindings for field operator workflows
- honest UI boundaries so the app does not pretend to own radio or runtime internals

## Recommended next implementation order

1. Formalize a Reticulum and mesh bridge contract
2. Add explicit field profiles for `online`, `mesh`, and `reticulum_fallback`
3. Add a remote stream and operator session profile for Sunshine and Moonlight handoff
4. Write a hardware contract for capture and print output before claiming printer support as stable
5. Export capability manifests downstream into `bmo-stack` and `prismtek-apps`
