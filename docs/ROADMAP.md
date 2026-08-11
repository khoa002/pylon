# Roadmap

12 weeks, roughly 10 hours per week. Three milestones, each independently useful. Stopping after any one still leaves something worth showing.

---

## 🟩 Milestone 1, weeks 1 to 4: the engine

**Goal: a working CLI that answers reachability questions for Ocarina of Time.**

| Week | Work |
|---|---|
| 1 | Repo, uv, ruff, mypy strict, pytest, GitHub Actions. Postgres in Docker Compose. SQLAlchemy 2.0 typed models plus Alembic for the canonical schema. `docs/LICENSES.md` written first |
| 2 | Rule expression language: tokenizer, AST, parser. Support `and`, `or`, `not`, parentheses, identifiers, and function calls with args. Unit tests on the parser before anything else |
| 3 | `adapters/oot_json.py`. Load the full OoT world into the canonical schema with provenance on every row. Macro resolution from `LogicHelpers.json` |
| 4 | Solver: `can_reach(target, state)` and `required_steps(target, state)` returning an ordered list with the satisfying rule for each step. CLI. **20 golden cases verified by hand**, as plain pytest |

**Definition of done**

- [ ] `uv run pylon ingest oot` is idempotent and loads the full world
- [ ] `uv run pylon can-reach "Fire Temple Boss" --have Slingshot,Kokiri_Sword` returns a correct ordered answer
- [ ] `uv run mypy src` clean, CI green
- [ ] 20 hand-verified golden cases passing
- [ ] `docs/STATE.md` current and at least two ADRs written

---

## 🟨 Milestone 2, weeks 5 to 8: API, deploy, second source

**Goal: prove the adapter pattern generalizes and the thing runs in public.**

| Week | Work |
|---|---|
| 5 | FastAPI: `GET /games`, `GET /games/{id}/graph`, `POST /reachability`, `GET /nodes/{id}` with provenance. Pydantic v2 on every boundary. structlog, request IDs, `/health` |
| 6 | Multi-stage Dockerfile. Deploy to Fly.io behind a real domain. GitHub Actions deploys on merge to main. Migrations run on deploy |
| 7 | `adapters/archipelago.py` part 1: import a world module, walk regions, entrances, and locations into the canonical schema |
| 8 | Archipelago part 2: ⭐ black-box rule probing. Two games loaded end to end. Record extraction confidence per rule. Write it up |

**Definition of done**

- [ ] Deployed, reachable over HTTPS, auto-deploys on merge
- [ ] Three games in one schema (OoT plus two Archipelago titles) with **zero changes to `graph/` or `rules/`**
- [ ] Blog post 1 published: the black-box rule probing technique

### ⭐ Black-box rule probing

Archipelago builds a real region graph in memory. That structure is the game's actual topology and is not shuffled. But its access rules are Python lambdas, so they cannot be parsed.

**They do not need to be parsed. They can be called.**

```
for each rule:
    baseline = rule(state_with_all_items)
    for each candidate item:
        probe = state_with_all_items minus that item
        if rule(probe) != baseline:
            that item is in the rule's dependency set
```

- One-at-a-time removal finds required items.
- Pairwise probing distinguishes `A and B` from `A or B`.
- Cache aggressively. Rule evaluation is cheap, the combinatorics are not.
- ⚠️ This will not recover every rule perfectly. Record confidence per rule, and fall back to storing the rule as an opaque callable reference with its discovered dependency set. Partial extraction is still useful and is an honest result.

This is the most interesting engineering problem in the project. Worth doing well and worth writing up.

---

## 🟥 Milestone 3, weeks 9 to 12: the LLM layer and the eval harness

**Goal: natural language in, correct grounded answer out, with measured quality. This is the milestone that matters most.**

| Week | Work |
|---|---|
| 9 | Tools, all deterministic: `can_reach`, `required_steps`, `explain_rule`, `list_items`. Agent loop written **directly against the model API**. No orchestration framework |
| 10 | ⭐ Eval harness. Golden set of 100 to 150 questions, authored and answered by hand, in `data/golden/`. Scorers: tool selection accuracy, argument correctness, route validity (pure Python check against the graph), grounding (every claim maps to a returned tool result) |
| 11 | CI gate: evals run on every prompt or tool change and fail the build on regression. Cost and p95 latency recorded per run into `docs/EVALS.md`. Same golden set across 3 models, publish the quality vs cost vs latency table |
| 12 | Improve using the numbers. At least three measured changes with before and after. Guardrails: output schema enforcement, refusal on out-of-scope, input validation. Final writeup |

**Definition of done**

- [ ] `uv run pylon evals run` produces a dated report appended to `docs/EVALS.md`
- [ ] CI fails on a regression deliberately introduced to prove the gate works
- [ ] `docs/EVALS.md` shows at least four dated runs with measured movement
- [ ] Blog post 2 published: the eval harness and what the numbers changed

---

## ⏸️ Explicitly deferred

Not cancelled. Revisit only after Milestone 3 ships.

| Deferred | Why |
|---|---|
| Community contribution layer, claim locks, moderation | Product ambition, not the goal |
| Prose corpus (StrategyWiki, Fandom) and RAG over it | A whole ingest problem plus viral CC BY-SA complexity |
| Finance vertical via the Bills Helper MCP | Milestone 2 already proves generalization |
| MCP server | One or two evenings, add after M3 |
| Expo mobile client | Two weekends, purely a resume line |
| Terraform, Grafana, Kubernetes | Fly.io plus GitHub Actions is enough |
| `sm-json-data` adapter, hand-authored games | Only if coverage becomes a real goal |
