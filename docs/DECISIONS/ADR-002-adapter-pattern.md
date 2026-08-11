# ADR-002: One canonical graph, one adapter per source

**Status:** accepted
**Date:** 2026-08-11

## Context

Pylon needs data from sources with incompatible shapes:

- **OoT Randomizer:** declarative JSON. Regions with `exits`, `locations`, and `events`, each mapping to a boolean expression string
- **Archipelago:** live Python objects. Regions, Entrances, Locations, with rules as opaque lambdas
- **sm-json-data:** rooms, nodes, links, strats, with typed requirement objects and a resource model

Three shapes, one question to answer. Where does the translation live?

## Options

### Option A: per-source solvers

Each source keeps its native shape and gets its own reachability implementation.

- ✅ No lossy translation. Each solver can exploit its source's structure
- 🔴 N solvers to test, and every eval must be written N times
- 🔴 Cross-game features become impossible
- 🔴 Adding a source means adding a solver, which is the expensive part

### Option B: canonical model, adapter per source

Every source is translated into one internal graph. The solver only ever sees the canonical form.

- ✅ One solver, tested once
- ✅ **Adding a game is a new file, never a change to the engine.** That is a testable architectural claim
- ✅ Provenance and licensing are handled uniformly at the boundary
- 🔴 Translation is lossy where a source is richer than the canonical model
- 🔴 The canonical model has to be designed before the second source is understood, so it will need at least one revision

### Option C: canonical model, but let it grow per source

Same as B, but extend the core model whenever a source needs something.

- ✅ No loss
- 🔴 The model becomes the union of every source's quirks
- 🔴 Loses the architectural claim entirely, because engine changes track source additions

## Decision

**Option B, with a hard constraint.**

`src/pylon/adapters/` is the only place that knows about upstream formats. `graph/` and `rules/` never import from `adapters/`.

**The Milestone 2 definition of done is three games loaded with zero changes to `graph/` or `rules/`.** If a new source appears to require an engine change, stop and write an ADR rather than making the change. Sometimes the answer will be that the model genuinely needs to grow. It should be a decision, not a reflex.

## Consequences

- Lossy translation is accepted. An adapter may record lower confidence or store an opaque rule reference rather than force a bad fit.
- The known first stress test is OoT's `Time_Travel`, which is stateful (child vs adult) while `CollectionState` assumes monotonic item accumulation. This will force a decision about whether age-state belongs in the core model or the adapter. Flagged in `docs/STATE.md`; write the ADR before week 3.
- CI should eventually assert the import boundary mechanically. A test that fails if `graph/` or `rules/` imports `adapters/` is cheap and worth writing.
