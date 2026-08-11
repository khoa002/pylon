# STATE

Updated: 2026-08-11 by Cowork (initial scaffold)

## Milestone

M1, week 1 of 4. Goal: repo, tooling, CI, Postgres, canonical schema.

## Done since last update

- Repo scaffolded: pyproject, ruff, mypy strict, pytest, GitHub Actions CI.
- Docker Compose with Postgres 17.
- Canonical SQLAlchemy models: Game, Region, Entrance, Location, Item, with a
  ProvenanceMixin on every ingested table.
- Rule AST node types defined. Parser and evaluator are stubs.
- Adapter protocol defined in `adapters/base.py`. No adapters implemented.
- Typer CLI wired with `ingest`, `can-reach`, and `graph-stats` stubs.
- Docs: PROJECT, ROADMAP, LICENSES, EVALS, ADR 001 to 003.
- Spec tests written as `xfail` for the parser, evaluator, and solver.

## In progress

Nothing. Fresh repo, first session has not run yet.

## Blocked / needs a decision

Nothing yet.

## Next 3 actions

1. `uv sync`, bring Postgres up, confirm `uv run pytest` and `uv run mypy src`
   are both green. Fix anything the scaffold got wrong.
2. Set up Alembic and generate the initial migration from the models.
3. Week 2 work: implement `rules/parser.py` against the xfail tests in
   `tests/test_rules_parser.py`. Remove each xfail marker as it passes.

## Open questions for Cowork

- OoT `Time_Travel` is stateful (child vs adult). The current `CollectionState`
  assumes monotonic item accumulation. Does age-state belong in the core model
  or in the OoT adapter? This decides how general the solver has to be.
  Placeholder ADR not yet written. Raise this before starting week 3.
