# Learning-First Checklist (Before Hardware Shell Build)

Use this checklist to understand the original project deeply before making major changes.

## 1) Read order

1. `README.md` (baseline behavior + install assumptions)
2. `agent.py` (single-file runtime flow)
3. `config.json` (behavior switches)
4. `docs/BMO_OMNI_UPGRADE_PLAN.md` (our extension roadmap)
5. `OMNI_INTEGRATION_MAP.md` (where Omni plugs in)

## 2) Runtime flow to understand

- Wake trigger -> record audio -> transcribe -> LLM -> tool routing -> TTS -> face state updates
- Action JSON path (`extract_json_from_text` + `execute_action_and_get_result`)
- Interruption behavior (space/PTT handling)
- Memory behavior (`chat_memory.json` + session memory)

## 3) Validation goals before shell work

- wake word reliably triggers
- STT transcript quality is acceptable in room noise
- TTS starts quickly and is interruptible
- no crashes over 30+ minute conversation loop
- Omni mode fallback to local ollama works when Omni endpoint is unavailable

## 4) Keep upstream stable

- Avoid rewrites of core loop unless blocker is proven
- Add behavior behind config flags first
- Keep commits small and reversible

## 5) Upstream sync policy

- Track upstream as `upstream` remote
- Rebase/merge upstream changes regularly
- Keep Omni-specific changes modular
