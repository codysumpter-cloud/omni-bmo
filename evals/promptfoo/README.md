# Promptfoo Evals for Omni-BMO

Run prompt quality/safety checks before merging prompt/routing changes.

## Run

```bash
cd evals/promptfoo
export OPENAI_API_KEY=sk-...
npx promptfoo@latest eval -c promptfooconfig.yaml
npx promptfoo@latest view
```

If using local Ollama only, keep the openai provider disabled or unset key.
