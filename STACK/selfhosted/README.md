# Self-hosted Core Stack (Sprint 2)

Services:
- Postgres
- Redis
- MinIO
- Prometheus
- Grafana

## Prerequisites
- Docker Engine + Docker Compose plugin

## Quick start

```bash
cd STACK/selfhosted
cp .env.example .env
# edit .env secrets

docker compose up -d
```

## URLs
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- MinIO API: http://localhost:9000
- MinIO Console: http://localhost:9001
- Postgres: localhost:5432
- Redis: localhost:6379

## Health checks

```bash
bash scripts/stack_sprint2_health.sh
```

## Stop

```bash
docker compose down
```

## Notes
- Default credentials in `.env.example` are for local dev only.
- Rotate secrets before any shared/staging/production use.
