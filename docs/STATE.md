# STATE

Updated: 2026-08-11 by Cowork

## Current release

**v0.2.0 — Rules parse.** Target Aug 18.

Demo it must produce: `pylon parse "can_play(Bolero_of_Fire) and (Bow or Slingshot)"`
prints the AST.

🛑 Do not work ahead of this release. Ideas go to docs/ICEBOX.md.

## Done since last update

- v0.1.0 scaffold committed and pushed to https://github.com/khoa002/pylon
- Repo made public. Secret scanning and push protection confirmed on.
  Dependabot security updates enabled.
- Roadmap restructured from 3 milestones into 11 tagged releases, each with a
  single demo command and a named scope cut.
- Added docs/ICEBOX.md as the pressure valve for mid-release ideas.
- README now carries the release checklist.

## In progress

Nothing yet. v0.1.0 still needs its tag.

## Blocked / needs a decision

- ⚠️ **v0.4.0 is blocked on ADR-004**, not v0.2.0, so this is not urgent yet.
  OoT `Time_Travel` is stateful (child vs adult) while `CollectionState` assumes
  monotonic item accumulation. Cowork is researching how OoT Randomizer's own
  search, Archipelago, and sm-json-data each handle it. ADR-004 to follow.

## Next 3 actions

1. Tag and publish v0.1.0. It is already done; take the win.
   `git tag -a v0.1.0 -m "Scaffold" && git push origin main --tags`
   `gh release create v0.1.0 --title "v0.1.0 Scaffold" --notes "..."`
2. `uv sync`, bring Postgres up, confirm `uv run pytest` and `uv run mypy src`
   are green on the Mac. Set up Alembic and generate the initial migration.
3. Start v0.2.0: implement `rules/parser.py` against the xfail tests in
   `tests/test_rules_parser.py`, removing each marker as it passes. Then add the
   `pylon parse` command.

## Open questions for Cowork

- ADR-004, above. Needed before v0.4.0, not before v0.2.0.
