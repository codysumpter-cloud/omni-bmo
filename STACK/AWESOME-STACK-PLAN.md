# Awesome Stack Integration Plan (PrismBot)

This integrates **useful** patterns/tools from:
- sindresorhus/awesome
- vinta/awesome-python
- awesome-selfhosted/awesome-selfhosted
- trimstray/the-book-of-secret-knowledge
- avelino/awesome-go

## Why curated (not "everything")

Installing everything from awesome lists would create bloat, breakage risk, and maintenance debt.
We adopt a **curated core stack** aligned to Prismtek goals:
1) Prompt Forge
2) Pixel/game asset pipeline
3) Arcade + leaderboard platform
4) Private AI/privacy-first workflow

---

## Layer 1: Core CLI + Dev Ergonomics

- `ripgrep` (fast search)
- `fd` (fast file find)
- `fzf` (fuzzy finder)
- `jq` (JSON processing)
- `bat` (readable file output)
- `htop` (process visibility)
- `tmux` (session multiplexing)

Source alignment: book-of-secret-knowledge + awesome

---

## Layer 2: JS/TS Product Stack

- React + React Router (UI)
- Vite (frontend build)
- Node 20+ runtime
- zod (schema validation)
- axios/fetch wrappers
- vitest + testing-library (tests)

Source alignment: awesome + react ecosystems

---

## Layer 3: Python/AI Pipeline Stack

- fastapi + uvicorn (service/API)
- pydantic (data models)
- httpx (HTTP client)
- pillow/opencv-python (image processing)
- numpy/pandas (data handling)
- pytest (tests)

Source alignment: awesome-python

---

## Layer 4: Self-hosted Privacy Stack (phased)

Phase A (now):
- Postgres
- Redis
- MinIO (object storage)
- Grafana + Prometheus (monitoring)

Phase B (later):
- Sentry-compatible error stack
- Workflow queue workers
- Internal auth/SSO layer

Source alignment: awesome-selfhosted

---

## Layer 5: Optional Go Path (performance services)

Not default now. Use for future high-throughput leaderboard microservice.
- Gin/Echo/Fiber (pick one later)
- sqlc / goose migrations
- zap logging

Source alignment: awesome-go

---

## Adoption Policy

- Add tools in small batches.
- Every addition must have:
  - owner
  - use case
  - rollback path
  - verification command
- Quarterly prune: remove unused tools.
