# CLAUDE.md

## What this is

Pylon is a prerequisite-graph engine for video games. It answers "what do I need to do first?"

**The LLM never decides what is required.** Reachability and ordering are deterministic Python, exposed to the model as tools. If you find yourself asking a model to work out prerequisites, stop. That is a bug.

## Stack

Python 3.13, uv, FastAPI, SQLAlchemy 2.0 (typed), Alembic, Postgres, pytest, ruff, mypy strict. Docker Compose locally. Fly.io for deploy (Milestone 2).

## Commands

```bash
uv sync                                        # install
uv run pytest                                  # tests
uv run pytest -x -q                            # fast fail
uv run ruff check --fix . && uv run ruff format .
uv run mypy src                                # must be clean
uv run alembic upgrade head                    # migrate
uv run alembic revision --autogenerate -m "…"  # new migration
uv run pylon --help                            # CLI
docker compose -f infra/docker-compose.yml up -d
```

## 🛑 Release discipline

This project ships in small tagged releases because the failure mode here is drift, not difficulty. See `docs/ROADMAP.md`.

- **Work on the current release only.** It is named at the top of `docs/STATE.md`. Do not build ahead of it, even when the next piece is obvious.
- **Every release ships a demo command**, not just passing tests. If it cannot be demoed in one terminal command, it is not done.
- ⚠️ **If a release is running long, cut scope. Never extend.** Each release in the roadmap names its own scope cut. Take it.
- **New ideas go to `docs/ICEBOX.md`, unopened.** If the user proposes scope mid-release, add it to the icebox and say so rather than building it.
- **Nothing is done until it is tagged and published.** Definition of done for every release includes `git tag`, `git push --tags`, and `gh release create`.

## Rules

- **Write the failing test first.** Tests marked `xfail` encode specs that are not built yet. When you implement one, remove the marker in the same commit.
- Type hints on everything. `uv run mypy src` must be clean before commit.
- Pydantic models at every boundary. No raw dicts crossing module lines.
- **Adding a data source means a new file in `src/pylon/adapters/`.** If a change to `graph/` or `rules/` seems necessary to support a new source, stop and write an ADR first. That constraint is the architecture test.
- Every ingested row carries provenance: source, source version, license, upstream URL, ingested_at. Use `ProvenanceMixin`.
- No new dependency without an ADR in `docs/DECISIONS/`.
- No orchestration framework in `agent/`. Write the loop against the model API directly. Revisit only after Milestone 3 ships.
- Ingest must be idempotent. Running it twice changes nothing.
- **Rewrite `docs/STATE.md` at the end of every session.** Rewrite, do not append. Keep it under 100 lines.
- Commit messages: imperative mood, one line, scope prefix. `rules: add tokenizer for function calls`

## Sources and licenses

| Source | License | Verdict |
|---|---|---|
| OoT Randomizer JSON | MIT | ✅ OK |
| ArchipelagoMW | MIT | ✅ OK |
| sm-json-data | CC BY 4.0 | ✅ OK, attribution required. Deferred |
| speedrun.com | CC BY-NC | ❌ **DO NOT USE.** Non-commercial, and it has no route data anyway |
| SoulsRandomizers (Elden Ring, Dark Souls) | none | ❌ **DO NOT USE.** Unlicensed, derivatives prohibited |
| StrategyWiki, Fandom | CC BY-SA | ⏸️ Deferred. If ever used, it lives in its own schema and never joins into permissive output |

## Non-goals

- ❌ A game catalog. We do not maintain game metadata.
- ❌ Walkthrough prose. We import structured logic.
- ❌ User accounts, contributions, or moderation.
- ❌ Terraform, Kubernetes, or a service mesh. Fly.io plus GitHub Actions is enough.

## Layout

```
src/pylon/
  adapters/   one file per data source. The only place that knows about upstream formats
  models/     SQLAlchemy + Pydantic. The canonical graph schema
  rules/      boolean expression AST, parser, evaluator
  graph/      solver: reachability and ordering. Pure, no I/O
  agent/      tools and the model loop (Milestone 3)
  evals/      harness and scorers (Milestone 3)
  api/        FastAPI (Milestone 2)
  cli.py      Typer entrypoint
```

## Current release

See the top of `docs/STATE.md`. Do not work ahead of it. If something seems worth doing that is not in the current release, put it in `docs/ICEBOX.md` and mention it, rather than building it.
