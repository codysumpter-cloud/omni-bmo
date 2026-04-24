# Buddy Runtime Boundary

This document defines the role of `omni-bmo` in the Buddy product system.

## Goal

Keep `omni-bmo` as the runtime/device layer for Buddies without letting it absorb product-core identity or pack logic.

## What `omni-bmo` should own

- device/runtime execution
- transport selection and failover
- local bridge adapters
- local/offline helper mode
- edge receipts for runtime actions
- remote operator mode
- product-safe pairing and reachability state
- runtime health checks and diagnostics

## What `omni-bmo` should not own

- flagship Buddy product identity model
- pack definitions for Creator/Teen/Field Tech Buddies
- template marketplace logic
- publish sanitation policy
- premium memory ranking logic
- trust scoring policy for the full product family

Those belong in a private Buddy-core layer and the product shell.

## Runtime modes to support

### Full hybrid

- local continuity helpers
- cloud reasoning / orchestration path available
- normal tool access

### Limited hybrid

- reduced cloud/tool posture
- continuity and core notes/tasks still available

### Offline helper

- local notes/tasks/checklists/continuity summary
- no heavy remote orchestration requirement

### Read-only continuity

- show memory, receipts, tasks, and pairing state
- avoid heavy action execution

## Canonical runtime outputs for Buddy products

`omni-bmo` should expose product-safe state like:

- runtime reachable / unreachable
- selected transport mode
- last transport reason
- last heartbeat timestamp
- remote session available or not
- limited/degraded mode indicators
- edge-generated action receipts

This should be enough for product surfaces to stay honest without importing operator-only complexity.

## Required integration contract

Suggested shared contract objects:

- `RuntimePairingState`
- `RuntimeActionReceipt`
- `RuntimeCapabilityState`
- `RuntimeModeSummary`

These should be stable for consumers in `prismtek-apps` and future private Buddy-core code.

## Guardrails

1. never make the app guess runtime truth
2. never claim rich runtime capability if only fallback/control-only mode is available
3. always surface degraded state explicitly
4. keep operator-only controls separate from product-safe status
5. keep edge/runtime receipts machine-readable

## Immediate next actions

1. freeze product-safe runtime state shape
2. add receipt contract for runtime-triggered actions
3. verify offline helper mode is explicit and not hand-wave copy
4. keep Creator/Teen/Field Tech behavior out of runtime repo ownership
