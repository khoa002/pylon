# STATE

Updated: 2026-08-11

## Current release

**v0.2.0 — Rules parse.** Target Aug 18.

Demo it must produce: `pylon parse "can_play(Bolero_of_Fire) and (Bow or Slingshot)"`
prints the AST.

🛑 Work this release only. Ideas that arrive mid-release go to `docs/ICEBOX.md`.

v0.1.0 is complete but **not yet tagged**. Tag it before starting v0.2.0.

## Done since last update

**Roadmap restructured (Cowork).** Three 4-week milestones became eleven tagged
releases, each demoable in one terminal command, each with a named scope cut to
take if it runs long. `v0.5.0` is marked as the honest finish line: at that tag
Pylon works and is a complete portfolio piece. Added `docs/ICEBOX.md` as the
pressure valve. README carries the release checklist. `CLAUDE.md` gained a
release-discipline section.

**Week 1 work, merged in PR #1:**

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
- ⭐ Two defects found by reading the generated migration rather than trusting it:
  - `drop_table()` does not emit `DROP TYPE` for a native enum, so downgrade then
    upgrade failed. Fixed by hand; the line is lost on every regeneration.
  - The native enum stored member *names* (`PROGRESSION`), not the `StrEnum` values
    (`progression`) documented in `PROJECT.md`. Raw and bulk inserts were rejected,
    which is exactly how the ingest release will write. Fixed with `values_callable`.
- `docs/LEARNING.md` started: append-only log, one entry per session.
- Materia (a private PR-review GitHub Action) was evaluated and rejected. Pylon is
  public and the action is private, which GitHub does not allow even with the action
  repo's access policy set to `user`. See `docs/LEARNING.md`.

## In progress

Nothing. `main` is clean and CI is green.

## Blocked / needs a decision

Nothing blocking v0.2.0. ADR-004 blocks v0.4.0, see open questions.

## Next 3 actions

1. **Tag and publish v0.1.0.** It is already done; take the win.
   `git tag -a v0.1.0 -m "Scaffold" && git push origin main --tags`
   then `gh release create v0.1.0 --title "v0.1.0 Scaffold" --notes "..."`
2. Start v0.2.0: tokenizer and recursive-descent parser in `rules/parser.py`,
   against the xfail specs in `tests/test_rules_parser.py`. Remove each marker as
   it passes.
3. Add the `pylon parse` command that pretty-prints a rule tree, then confirm it
   parses every distinct rule string in OoT's `Overworld.json` without error.

## Open questions

- ⚠️ **ADR-004, needed before v0.4.0.** OoT `Time_Travel` is stateful (child vs
  adult) while `CollectionState` assumes monotonic item accumulation. Does age-state
  belong in the core model or in the OoT adapter? This decides how general the solver
  has to be. Cowork is researching how OoT Randomizer's own search, Archipelago, and
  sm-json-data each handle it.
- CI does not run migrations. The initial migration is verified locally only, and
  nothing in CI would catch a broken one. Scheduled into v0.4.0, which is the first
  release that actually touches the database.
- `mypy src` does not cover `migrations/env.py`. It is hand-written project code
  sitting outside the type gate. Widen the gate, or accept it deliberately. Parked in
  `docs/ICEBOX.md`.
- Native enum maintenance is manual: adding a value to `ItemClassification` needs a
  hand-written `ALTER TYPE`, and the `DROP TYPE` line must be re-added whenever the
  initial migration is regenerated. Revisit if a second enum column appears.
