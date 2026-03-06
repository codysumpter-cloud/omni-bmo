# be-more-agent → Omni Integration Map

Goal: keep be-more-agent UX stack (wake word, STT, TTS, face states), but swap/augment LLM brain with OmniAPI.

## 1) What this repo already does

Core file: `agent.py`

Pipeline:
1. Wake detect (`openwakeword`) or push-to-talk key events
2. Record audio (`sounddevice`) with adaptive silence or PTT mode
3. Transcribe (`whisper.cpp` CLI)
4. Build messages (system + memory + user)
5. Call LLM (`ollama.chat(..., stream=True)`)
6. Detect tool JSON intents (time/search/camera)
7. Execute tool
8. Speak response (`piper`)
9. Animate face states (`idle/listening/thinking/speaking/error`)

### Main integration hotspots in `agent.py`
- LLM chat stream: around `chat_and_respond()` (uses `ollama.chat` streaming)
- Tool-action extraction: `extract_json_from_text()` + `execute_action_and_get_result()`
- Memory:
  - `self.session_memory`
  - `self.permanent_memory` (`chat_memory.json`)
- Vision path: `capture_image()` + recursive call to `chat_and_respond(..., img_path=...)`

## 2) Minimal Omni bridge strategy (recommended first)

Do **not** rewrite full app first.

Create a small adapter function:

- `omni_chat(messages, model_hint=None, stream=True)`
- Endpoint: `POST /api/omni/chat/completions`
- Auth: bearer token (`PRISMBOT_API_TOKEN` or dedicated Omni token)

Then swap only this call-site:
- from: `ollama.chat(...)`
- to: `omni_chat(...)`

Keep all wake/STT/TTS/UI code unchanged.

## 3) Mapping of features

| be-more-agent feature | Current impl | Omni integration note |
|---|---|---|
| Chat text | `ollama.chat` | Replace with Omni endpoint call |
| Model routing | static `text_model` in config | Omni `local-first` route + per-profile model |
| Tool actions | JSON in natural reply | keep as-is first; later map to Omni tools routes |
| Vision captioning | moondream via ollama model | optional: keep local moondream path first |
| Memory | local json | keep local first; later sync selected memory to Omni |
| Voice/TTS | Piper local | unchanged |

## 4) Suggested env additions (be-more-agent side)

Add to `config.json` (or env):

```json
{
  "llm_backend": "omni",
  "omni_base_url": "http://127.0.0.1:8799/api/omni",
  "omni_token_env": "PRISMBOT_API_TOKEN",
  "omni_model": "omni-core:phase2"
}
```

## 5) First safe milestone

Milestone A (no hardware changes):
- run be-more-agent unchanged
- implement Omni adapter behind feature flag (`llm_backend`)
- verify:
  - wake -> response works
  - streaming text works
  - TTS queue works
  - tool JSON still recognized

## 6) Known risk points

- Streaming protocol mismatch (Ollama stream chunks vs Omni response format)
  - mitigation: start with non-stream Omni response, then add pseudo-stream text chunking
- Timeouts on heavier models
  - mitigation: use fast profile model for embodied chat path (e.g., `llama3.2:1b`)
- Tool JSON reliability
  - mitigation: keep strict extraction and fallback prompts

## 7) Next files to create

- `omni_adapter.py` (or inline helper in `agent.py`)
- `docs/INTEGRATE_OMNI.md` with runbook

This gives a fast path to “BMO UX + Omni brain” without breaking the proven interaction stack.
