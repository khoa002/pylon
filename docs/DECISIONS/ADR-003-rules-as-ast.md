# ADR-003: Rules are a parsed AST, not strings or callables

**Status:** accepted
**Date:** 2026-08-11

## Context

Every source expresses access rules differently:

- OoT: a string, `"can_play(Prelude_of_Light) and can_leave_forest"`
- Archipelago: a Python lambda over a `CollectionState`
- sm-json-data: nested JSON requirement objects

The solver needs to evaluate these. It also needs to **explain** them, because "here is the rule that gates this step" is a product requirement, not a nicety. And the eval harness needs to inspect them to check route validity.

## Options

### Option A: store the raw string, `eval()` at runtime

- ✅ Almost no work
- 🔴 Arbitrary code execution on ingested data. Unacceptable
- 🔴 Not inspectable or explainable
- 🔴 Only works for sources that happen to be Python-shaped

### Option B: store an opaque callable

- ✅ Handles Archipelago natively
- ✅ Always correct, since it is the source's own logic
- 🔴 Cannot be explained, serialized, diffed, or stored in Postgres
- 🔴 Requires the source package importable at query time

### Option C: parse into a typed AST

Nodes: `And`, `Or`, `Not`, `HasItem`, `CanReach`, `Setting`, `Macro`, `Literal`.

- ✅ Evaluable, explainable, serializable, diffable, and testable in isolation
- ✅ Enables "which term failed" for the explanation surface
- ✅ Source-agnostic. Each adapter's only job is producing this shape
- 🔴 Needs a real tokenizer and parser (week 2 of the roadmap)
- 🔴 Archipelago lambdas cannot be parsed, only probed, so recovery there is partial

## Decision

**Option C.** Rules are a typed AST, stored serialized, evaluated by a pure function against a `CollectionState`.

For Archipelago specifically, black-box probing recovers a dependency set and, where pairwise probing is conclusive, the and/or structure. Where it is not conclusive, the adapter stores a partial AST plus a confidence score and marks the rule as approximate. **Partial extraction is an honest result and is better than either of the rejected options.**

Never `eval()`. The parser is a real parser.

## Consequences

- Week 2 is spent on a tokenizer and recursive-descent parser before any adapter exists. That ordering is deliberate: the AST is the contract every adapter targets.
- Evaluation must be pure and side-effect free, so it can be memoized. Reachability will call it heavily.
- `explain_rule` becomes cheap: walk the AST, evaluate each leaf against current state, return the failing terms.
- Approximate rules need a visible confidence field, surfaced in API responses. Users should be able to tell a verified OoT rule from a probed Archipelago one.
