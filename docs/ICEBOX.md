# Icebox

**The pressure valve.** Every idea that arrives mid-release lands here, unopened, and is not discussed again until the current release is tagged.

This file exists because the failure mode for this project is scope drift, not difficulty. Writing an idea down is the cheapest way to stop it from eating the week. Adding to this file is always allowed. Acting on it during a release never is.

## Rules

- Anything not in the current release goes here. No exceptions, including good ideas. **Especially** good ideas.
- One line each. If it needs a paragraph, it needs an ADR, and that is itself a reason to defer it.
- Review this file only when cutting a release, never mid-release.
- Deleting things from here is healthy. Most of these will never be worth doing, and that is the correct outcome.

---

## Deferred by decision (see docs/DECISIONS and the Career Development project)

- Community contribution layer: flag / propose / verify, claim locks, federated per-game moderation
- Prose corpus RAG over StrategyWiki or Fandom (viral CC BY-SA, needs its own schema)
- Finance vertical consuming the Bills Helper MCP server
- MCP server exposing Pylon's tools to Claude Desktop
- Expo mobile client, one screen, offline cache, push notification
- Terraform, Grafana, Kubernetes
- `sm-json-data` adapter (Super Metroid, CC BY 4.0)
- Hand-authored game graphs

## Ideas parked mid-flight

<!-- Add one line, with the date. Do not act on these during a release. -->

- 2026-08-11: widen the type gate to cover `migrations/env.py`, or accept it as deliberately excluded
- 2026-08-11: pairwise rule probing for and/or discrimination, if v0.8.0 has to be cut back to one-at-a-time
- 2026-08-11: `pylon why "<step>"` to explain a single step in isolation
- 2026-08-11: graph visualisation, probably graphviz DOT export
- 2026-08-11: spoiler-log ingestion as a cross-check on probed Archipelago rules

## Rejected outright

Kept so they do not get re-proposed. Reasons are in `docs/LICENSES.md` and the project decisions log.

- speedrun.com as a data source: CC BY-NC, and it has no route data at all
- SoulsRandomizers (Elden Ring, Dark Souls): unlicensed, derivatives prohibited
- Building a game catalog: consume IGDB instead, if it is ever needed
- Authoring walkthrough prose
- An orchestration framework in the agent layer before v1.0.0
