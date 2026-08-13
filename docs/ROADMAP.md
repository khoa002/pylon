# Roadmap

**Eleven releases over twelve weeks.** Roughly one per week, at about 10 hours a week.

Every release is tagged, published, and demoable in a single terminal command. If you cannot demo it in one command, it is not a release yet.

---

## 🛑 The rules that make this finishable

These exist because the failure mode for this project is not difficulty. It is drift.

1. **One release at a time.** Never start the next one before the current one is tagged.
2. **Every release ships a demo command.** Not a passing test. Something you can run and show someone.
3. **Timebox: if a release passes 2x its estimate, cut scope, do not extend the deadline.** Move what is left to the next release or to `docs/ICEBOX.md`. A shipped v0.4.0 that does less beats an unshipped v0.4.0 that does more.
4. **No new scope mid-release.** Every new idea goes to `docs/ICEBOX.md` unopened. The icebox is the pressure valve.
5. **Tag it and publish it.** `git tag` plus a GitHub Release. Public and irreversible, which is the point. A checkbox you can un-tick is not completion.
6. ⭐ **v0.5.0 is the honest finish line.** At v0.5.0 Pylon works, answers real questions, and is a complete portfolio piece. Everything after it is upside. If life happens after v0.5.0, you stopped at a finished thing, not a corpse.

---

## Releases

| Tag | Name | What you can newly do | Target |
|---|---|---|---|
| ✅ `v0.1.0` | Scaffold | `uv run pytest` green, `pylon --help` runs | Aug 11 |
| `v0.2.0` | Rules parse | `pylon parse "A and (B or C)"` prints the AST | Aug 18 |
| `v0.3.0` | Rules evaluate | `pylon check "Bow and Bomb_Bag" --have Bow` says what is missing | Aug 25 |
| `v0.4.0` | OoT loads | `pylon graph-stats --game oot` prints real region and edge counts | Sep 1 |
| ⭐ `v0.5.0` | **It answers** | `pylon can-reach "Fire Temple Boss" --have ...` returns an ordered route | Sep 8 |
| `v0.6.0` | API | `curl localhost:8000/reachability` returns JSON | Sep 15 |
| `v0.7.0` | Live | The same curl works against a public URL | Sep 22 |
| `v0.8.0` | Second game | `pylon graph-stats` works for an Archipelago title | Oct 6 |
| `v0.9.0` | It talks | `pylon ask "can I get into the Fire Temple?"` | Oct 13 |
| `v0.10.0` | It is measured | `pylon evals run` prints scored results | Oct 27 |
| 🏁 `v1.0.0` | Shipped | Four dated eval runs showing improvement | Nov 3 |

---

## ✅ v0.1.0 — Scaffold

**Demo:** `uv run pytest && uv run pylon --help`

Repo, uv, ruff, mypy strict, pytest, GitHub Actions. Postgres via Docker Compose. Canonical SQLAlchemy models with `ProvenanceMixin`. Rule AST node types. Adapter protocol. Typer CLI. Docs and ADR-001 to ADR-003. 15 passing tests, 35 `xfail(strict)` specs. Alembic plus the initial migration for all five tables, round-trip verified.

- [x] CI green
- [x] `mypy --strict` clean
- [x] `uv.lock` committed so CI and local resolve identically
- [x] Alembic wired to `pylon.config.Settings`, no credentials in `alembic.ini`
- [x] Initial migration verified by `upgrade` → `downgrade base` → `upgrade`
- [x] Pushed to GitHub
- [ ] **Tagged and published**

---

## v0.2.0 — Rules parse

**Demo:** `pylon parse "can_play(Bolero_of_Fire) and (Bow or Slingshot)"`

Tokenizer and recursive-descent parser. AST serialization that round-trips through JSON.

- [ ] All 15 xfail markers gone from `tests/test_rules_parser.py`
- [ ] `to_dict` / `from_dict` round-trip test passes
- [ ] New `pylon parse` command pretty-prints a rule tree
- [ ] Parses every distinct rule string in OoT's `Overworld.json` without error

⚠️ Scope cut if it runs long: drop `Setting` comparison support and handle it in v0.4.0.

---

## v0.3.0 — Rules evaluate

**Demo:** `pylon check "Goron_Tunic and (Megaton_Hammer or Bow)" --have Bow`

Pure evaluator plus `explain`, which returns the failing leaf terms. This is the first release where output is genuinely useful to a person.

- [ ] All xfail markers gone from `tests/test_rules_evaluator.py`
- [ ] `explain` returns only failing terms
- [ ] New `pylon check` command prints ✅ or ❌ plus what is missing

⚠️ Scope cut: `CanReach` can stay stubbed to always-false. The solver arrives in v0.5.0.

---

## v0.4.0 — OoT loads

**Demo:** `pylon ingest oot && pylon graph-stats --game oot`

The OoT Randomizer adapter. Macro resolution from `LogicHelpers.json`. (Alembic and the initial migration already shipped in v0.1.0.)

- [ ] `pylon ingest oot` is idempotent: running twice changes no rows
- [ ] Every row has provenance populated
- [ ] `graph-stats` prints region, entrance, location, and item counts
- [ ] Unresolved macros are reported as warnings, never silently dropped
- [ ] ⚠️ CI gains a Postgres service and a test that runs `alembic upgrade head`. Migrations are currently verified locally only

This is the first release with a satisfying number attached to it. Put the counts in the release notes.

⚠️ Blocked on ADR-004 (the child/adult age-state question). Resolve that first.

---

## ⭐ v0.5.0 — It answers

**Demo:** `pylon can-reach "Fire Temple Boss" --game oot --have Slingshot,Kokiri_Sword`

The solver. Fixed-point reachability, cycle handling, memoization, ordered prerequisites with the gating rule for each.

- [ ] All xfail markers gone from `tests/test_graph_solver.py`
- [ ] 20 golden cases you verified by hand, passing
- [ ] `can-reach` renders an ordered route with reasons
- [ ] README demo block updated with real output

🛑 **This is the honest finish line.** At this tag, Pylon does the thing it exists to do. If you ship nothing else, this is still a real system with a real test suite and four ADRs. Write the release notes properly and take the win.

---

## v0.6.0 — API

**Demo:** `curl -s localhost:8000/reachability -d '{...}' | jq`

FastAPI over the solver. `GET /games`, `GET /games/{id}/graph`, `POST /reachability`, `GET /nodes/{id}` with provenance. structlog, request IDs, `/health`.

- [ ] OpenAPI docs render and are readable
- [ ] Pydantic models on every boundary
- [ ] `rule_confidence` surfaced in responses

---

## v0.7.0 — Live

**Demo:** the v0.6.0 curl, against a public URL.

Multi-stage Dockerfile, Fly.io deploy, GitHub Actions deploying on merge to main, migrations on deploy.

- [ ] Public HTTPS URL in the README
- [ ] Merge to main auto-deploys
- [ ] `/health` green

First release you can send someone a link to instead of a repo.

---

## v0.8.0 — Second game

**Demo:** `pylon ingest archipelago --game <title> && pylon can-reach ... --game <title>`

⭐ The hardest and most interesting release. Two weeks, deliberately.

**Definition of done includes the architecture test:** a second game loads with **zero changes to `graph/` or `rules/`**. That constraint is the whole point of ADR-002.

### Black-box rule probing

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
- ⚠️ This will not recover every rule perfectly. Record confidence per rule and fall back to a partial AST plus its discovered dependency set. **Partial extraction is an honest result.**

- [ ] Archipelago world module imports and walks
- [ ] Probing recovers dependency sets, with confidence recorded
- [ ] `git diff` on `src/pylon/graph/` and `src/pylon/rules/` is empty for this release
- [ ] Blog post 1 published

⚠️ Scope cut if it runs long: ship one-at-a-time probing only, mark every recovered rule as `And`, and move pairwise and/or discrimination to the icebox. Partial is fine. Unshipped is not.

---

## v0.9.0 — It talks

**Demo:** `pylon ask "I have the Slingshot and Kokiri Sword, can I get into the Fire Temple?"`

Tools: `can_reach`, `required_steps`, `explain_rule`, `list_items`. Agent loop written **directly against the model API**, no orchestration framework.

- [ ] Natural language question returns a grounded answer with citations
- [ ] Guardrails: output schema enforcement, refusal on out-of-scope
- [ ] Every claim traces to a tool result

---

## v0.10.0 — It is measured

**Demo:** `pylon evals run`

⭐ Two weeks. The release that matters most for hiring.

- [ ] Golden set of 100 to 150 questions in `data/golden/`, authored and answered by hand
- [ ] Scorers: tool selection accuracy, argument correctness, route validity, grounding
- [ ] Route validity checked in **pure Python against the graph**, no judge model
- [ ] CI gate fails the build on regression, proven by deliberately introducing one
- [ ] Cost and p95 latency recorded per run into `docs/EVALS.md`

---

## 🏁 v1.0.0 — Shipped

**Demo:** `docs/EVALS.md` showing four dated runs with movement.

- [ ] Three measured improvements with before and after numbers
- [ ] Quality vs cost vs latency table across three models
- [ ] Blog post 2 published
- [ ] README rewritten for a stranger

---

## ⏸️ Explicitly deferred

Not cancelled. These live in `docs/ICEBOX.md` and are revisited only after v1.0.0.

Community contributions, prose corpus RAG over StrategyWiki or Fandom, the finance vertical via the Bills Helper MCP, an MCP server, the Expo mobile client, Terraform and Grafana, the `sm-json-data` adapter, hand-authored games.

---

## How to cut a release

**On your MacBook Pro, in `~/dev/pylon`:**

```bash
uv run ruff check . && uv run ruff format --check . && uv run mypy src && uv run pytest
git tag -a v0.2.0 -m "Rules parse"
git push origin main --tags
gh release create v0.2.0 --title "v0.2.0 Rules parse" --notes "One demo command, what changed, what is next."
```

Then tick the box in `README.md`, update `docs/STATE.md`, and only then open the next release.
