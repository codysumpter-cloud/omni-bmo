# Omni-Sync Operational Plan: God's Work
## Phase 1: Synchronization & Evolution

### 1. Savage Refactor: omni-bmo `agent.py`
**Goal:** Transition `agent.py` from a monolithic loop to a non-monolithic, skill-based architecture.
- **Current State:** Monolithic class `BotGUI` handling GUI, audio, and action routing in one place.
- **Target State:** 
    - Separate `Core` engine.
    - `Skill` registry for tool execution (replacing the `execute_action_and_get_result` if/else chain).
    - Decoupled `GUI` and `Audio` handlers.
- **Execution:** MARCELINE to lead the "Savage Refactor".

### 2. Dynamic Capability Mirror: `prismtek-apps`
**Goal:** Implement the Dynamic Capability Mirror to unlock Buddy Cognitive Blueprints.
- **Current State:** `BeMoreCapabilityMirror.swift` is a static list of descriptors.
- **Target State:** 
    - Replace static lists with a dynamic loader that reads from a manifest (JSON) or remote sync.
    - Support "Cognitive Blueprints" (mapping capability IDs to specific agent behaviors/prompts).
- **Execution:** FINN to push the implementation.

### 3. Verification: NEPTR
**Goal:** Ensure safety and stability.
- **Checks:**
    - `omni-bmo`: Verify audio/vision loop stability and skill resolution.
    - `prismtek-apps`: Verify capability mirror loading and UI consistency.
- **Execution:** NEPTR to run the validation suite.

### 4. Delivery
- **Branch:** `evolution/phase-1`
- **Final Step:** Push all changes to the origin.

---
**Council Assignments:**
- **BMO_TRON:** Orchestration.
- **MARCELINE:** Refactoring `agent.py`.
- **FINN:** Implementing Dynamic Capability Mirror.
- **NEPTR:** Verification & Safety.
- **COSMIC_OWL/SIMON:** Context and Pattern support.
