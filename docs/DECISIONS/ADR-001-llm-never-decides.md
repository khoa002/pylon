# ADR-001: The LLM never decides what is required

**Status:** accepted
**Date:** 2026-08-11

## Context

Pylon answers "what do I need to do first?" A language model can produce a plausible answer to that question directly, from training data, with no graph at all. That is the obvious build, and it is much less work.

The problem is that it is unfalsifiable. If the model says you need the Goron Bracelet before the Fire Temple, there is nothing in the system that can confirm or deny it. Any eval reduces to another model grading the first one.

## Options

### Option A: model answers directly from its own knowledge

- ✅ Trivial to build. Working demo in an afternoon
- ✅ Covers every game, no ingest, no adapters
- 🔴 No ground truth. Cannot be tested, only spot-checked
- 🔴 Wrong answers are confidently phrased and expensive to detect
- 🔴 As a portfolio piece it demonstrates prompt writing, not engineering

### Option B: model reasons over retrieved graph data

- ✅ Grounded in real data with citations
- 🔴 The model still does the reasoning, so it can still get the logic wrong while citing correct sources
- 🔴 Validity is not checkable, only plausibility

### Option C: deterministic solver, model at the edges only

- ✅ **Route validity is objectively checkable in pure Python.** Evals measure something real
- ✅ Wrong answers surface as failing tests rather than as plausible prose
- ✅ Model failures are isolated to two narrow surfaces: query parsing and explanation
- 🔴 Requires the whole ingest and graph layer before anything works at all
- 🔴 Coverage is limited to games with importable logic

## Decision

**Option C.** Prerequisite resolution is a deterministic Python function. The model does exactly two jobs, both at the edges:

1. Turn a natural-language question into a structured query
2. Turn the structured answer back into English with citations

## Consequences

- The eval harness (Milestone 3) can score route validity objectively, with no judge model. This is the single most valuable property of the project.
- Milestone 1 has no LLM in it at all, and that is correct. The engine must be right before anything talks to it.
- If a future feature seems to require the model to work out prerequisites, that is a signal the solver is missing a capability. Extend the solver, do not move the reasoning.
- Coverage is bounded by what can be imported. Accepted. See `docs/PROJECT.md` on the genre ceiling.
