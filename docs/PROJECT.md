# Pylon

## What we are building

**A program that answers "what do I need to do first?" in a game, by walking a prerequisite graph.**

Worked example:

- Input: *"I'm in Ocarina of Time with the Slingshot and Kokiri Sword. Can I get into the Fire Temple?"*
- The engine looks up Fire Temple. Its rule is `Goron_Tunic and (Megaton_Hammer or can_use(Bow))`.
- It walks backwards until it hits things you already have.
- Output: *"No. Three prerequisites are missing, in this order, and here is the rule that gates each one."*

## The one architectural rule

> **The LLM never decides what is required.**

Prerequisite resolution is a deterministic Python function. The model does exactly two jobs, both at the edges: turn English into a structured query, and turn the structured answer back into English with citations.

That is what makes the system testable, and it is the design decision the whole project rests on.

## Why this project exists

Primary purpose is learning: Python and LLM application engineering, to a hireable level, with one system that proves it. Secondary purpose is that the tool is actually useful.

Design consequences of that ordering:

- ✅ Answers are objectively right or wrong, so evals measure something real instead of grading vibes.
- ✅ The graph data already exists under MIT and CC BY licenses. **We author no content.**
- ✅ It is a real system (ingest, database, API, agent, evals), not a chatbot demo.
- ✅ The domain is one the author knows well enough to catch a wrong answer instantly, which is a hard requirement for building a golden eval set.

## Non-goals

- ❌ Not a walkthrough site. Not a content platform.
- ❌ Not a game catalog. We do not maintain game metadata.
- ❌ Not a community product. No contributions, moderation, or accounts.

## Architecture

```
sources ──adapters──> canonical graph (Postgres) ──> solver (pure Python)
                                                        │
                                              tools ────┤
                                                        │
                              natural language ──> agent ──> answer + citations
                                                        │
                                                     evals
```

### The canonical model

| Entity | Fields |
|---|---|
| `Game` | id, slug, name |
| `Region` | id, game, name |
| `Entrance` | id, game, from_region, to_region, rule |
| `Location` | id, game, region, name, rule |
| `Item` | id, game, name, classification (`progression` / `useful` / `filler`) |
| `Rule` | parsed boolean expression tree over items, settings, and macro calls |

Every row carries provenance: source, source version, license, upstream URL, ingested_at.

### The adapter pattern

One importer per source, all targeting the canonical model. **Adding a game is a new file, never a change to the engine.**

The definition-of-done for Milestone 2 is three games loaded with zero changes to `graph/` or `rules/`. That constraint is the actual test of whether the architecture holds.

## Extensibility, stated honestly

| Tier | Source | Games | Cost |
|---|---|---|---|
| 1 | OoT Rando JSON, sm-json-data | 2 | An afternoon each. Highest fidelity |
| 2 | Archipelago | 80+ | One adapter, written once. Good fidelity |
| 3 | Hand-authored | Any | Hours per game, as a data file not prose |

⚠️ **The real ceiling is genre.** Randomizers exist for games with item-gated progression: Zelda, Metroid, Souls, Pokemon, Hollow Knight, roguelikes, some RPGs. They do not exist for linear shooters, sports, or MOBAs, because there is nothing to gate. That is the addressable universe, and it is exactly the genre where "what do I need first" is a question people ask.

⭐ **Self-authoring is safe here in a way it would not be for prose.** A hand-written or model-drafted graph is programmatically checkable: is it acyclic, is every location reachable from the start, does a known-good playthrough satisfy every rule, does vanilla item placement produce a completable game. Anything that fails is rejected automatically, with no human reading required.
