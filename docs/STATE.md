# STATE

Updated: 2026-08-11

## Milestone

M1, week 1 of 4. Goal: repo, tooling, CI, Postgres, canonical schema.

Week 1 is complete. Week 2 is the rule expression language.

## Done since last update

- Local environment verified end to end: `uv sync`, Postgres 17 in Docker on port
  5433, `pytest` (15 passed, 35 xfailed), `mypy src` clean, `ruff` clean.
- `uv.lock` committed. Resolution picked newer majors than `pyproject.toml`
  anticipated (mypy 2.3, pytest 9.1, ruff 0.16), so without the lock, CI and local
  were resolving different dependency sets.
- `MetaData(naming_convention=...)` added to `Base`, before the first autogenerate,
  so constraint and index names are deterministic.
- Alembic set up. `migrations/env.py` reads the URL from `pylon.config.Settings`,
  never from `alembic.ini`, so `sqlalchemy.url` stays unset and no credentials are
  committed. `compare_type` and `compare_server_default` are on.
- `migrations/script.py.mako` rewritten to modern typing, and ruff post-write hooks
  enabled, so generated revisions pass the same lint gate as the rest of the repo.
- Initial migration for all five canonical tables. Verified by round-trip
  (`upgrade` → `downgrade base` → `upgrade`) and by a second `--autogenerate`
  producing an empty diff.
- Two defects found by reading the generated migration rather than trusting it:
  - `drop_table()` does not emit `DROP TYPE` for a native enum, so downgrade then
    upgrade failed. Fixed by hand; the line is lost on every regeneration.
  - The native enum stored member *names* (`PROGRESSION`), not the `StrEnum` values
    (`progression`) documented in `PROJECT.md`. Raw and bulk inserts were rejected,
    which is exactly how week 3 ingest will write. Fixed with `values_callable`.
- `docs/LEARNING.md` started: append-only log, one entry per session.

## In progress

Nothing. Week 1 work is committed on `m1/alembic-initial-migration`.

## Blocked / needs a decision

Nothing blocking.

## Next 3 actions

1. Week 2 work: tokenizer and recursive-descent parser in `rules/parser.py`, against
   the xfail specs in `tests/test_rules_parser.py`. Remove each marker as it passes.
2. Then `rules/evaluator.py` against `tests/test_rules_evaluator.py`, same approach.
   Evaluation must stay pure so it can be memoized.
3. Add a Postgres service to `.github/workflows/ci.yml` plus a test that runs
   `alembic upgrade head`. The migration is currently verified locally only, and
   nothing in CI would catch a broken one.

## Open questions

- OoT `Time_Travel` is stateful (child vs adult). The current `CollectionState`
  assumes monotonic item accumulation. Does age-state belong in the core model or in
  the OoT adapter? This decides how general the solver has to be. Needs an ADR before
  week 3 starts.
- `mypy src` does not cover `migrations/env.py`. It is hand-written project code
  sitting outside the type gate. Widen the gate, or accept it deliberately.
- Native enum maintenance is manual: adding a value to `ItemClassification` needs a
  hand-written `ALTER TYPE`, and the `DROP TYPE` line must be re-added whenever the
  initial migration is regenerated. Revisit if a second enum column appears.
