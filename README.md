# AgentForge

AgentForge is a 90-day AI engineering build: a Next.js dashboard, FastAPI service, PostgreSQL storage, and a LangGraph planning workflow. Each daily run selects one roadmap item, asks a bounded coding agent for a small edit, checks it, and opens a pull request.

## Local start

```sh
docker compose up --build
```

Open http://localhost:3000. The API is at http://localhost:8000/docs.

## Automation status

The daily schedule is intentionally disabled during initial review. See [SETUP.md](SETUP.md) for costs, secrets, permissions, and activation. The runner never marks GitHub contribution credit from a successful workflow alone.
