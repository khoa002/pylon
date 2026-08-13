# ⚡ Pylon

> *You must construct additional pylons.*

Pylon answers one question about a video game: **what do I need to do first?**

Give it a game, what you currently have, and where you want to get to. It walks the game's prerequisite graph and returns an ordered list of what is missing, with the rule that gates each step.

```
$ pylon can-reach "Fire Temple Boss" --game oot --have Slingshot,Kokiri_Sword

No. 3 prerequisites are missing:

  1. Goron_Bracelet     gated by: can_reach(Goron City) and Bomb_Bag
  2. Goron_Tunic        gated by: Goron_Bracelet
  3. Megaton_Hammer     gated by: Goron_Tunic and can_reach(Fire Temple)

  Target rule: Goron_Tunic and (Megaton_Hammer or can_use(Bow))
```

## The one architectural rule

> **The LLM never decides what is required.**

Prerequisite resolution is a deterministic Python function. Once the agent layer exists, the model does exactly two jobs, both at the edges: turn English into a structured query, and turn the structured answer back into English with citations.

This is what makes the system testable. It is not negotiable.

## Where the data comes from

Pylon authors no game content. Randomizer projects must answer "is this seed beatable?", which forces them to encode each game's prerequisite graph as machine-readable logic. Pylon imports that.

| Source | License | Status |
|---|---|---|
| [OoT Randomizer](https://github.com/OoTRandomizer/OoT-Randomizer) `data/World/*.json` | MIT | Adapter in progress |
| [ArchipelagoMW](https://github.com/ArchipelagoMW/Archipelago) world modules | MIT | Planned, 80+ games |
| [sm-json-data](https://github.com/vg-json-data/sm-json-data) | CC BY 4.0 | Deferred |

See [`docs/LICENSES.md`](docs/LICENSES.md) for obligations and for sources that are explicitly off limits.

## Progress

Eleven releases, roughly one a week. Each is demoable in one command. ⭐ `v0.5.0` is the point where Pylon does the thing it exists to do.

- [x] **v0.1.0** Scaffold — `uv run pytest && pylon --help`
- [ ] **v0.2.0** Rules parse — `pylon parse "A and (B or C)"`
- [ ] **v0.3.0** Rules evaluate — `pylon check "Bow and Bomb_Bag" --have Bow`
- [ ] **v0.4.0** OoT loads — `pylon graph-stats --game oot`
- [ ] ⭐ **v0.5.0** It answers — `pylon can-reach "Fire Temple Boss" --have ...`
- [ ] **v0.6.0** API — `curl localhost:8000/reachability`
- [ ] **v0.7.0** Live — the same curl, public URL
- [ ] **v0.8.0** Second game — an Archipelago title loads, engine untouched
- [ ] **v0.9.0** It talks — `pylon ask "can I get into the Fire Temple?"`
- [ ] **v0.10.0** It is measured — `pylon evals run`
- [ ] 🏁 **v1.0.0** Shipped — four dated eval runs showing improvement

Full detail in [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Quickstart

Requires [uv](https://docs.astral.sh/uv/) and Docker.

```bash
git clone <your-fork> pylon && cd pylon
cp .env.example .env
docker compose -f infra/docker-compose.yml up -d
uv sync
uv run alembic upgrade head
uv run pytest
uv run pylon --help
```

## Project docs

| Doc | What it is |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Conventions and guardrails. Read before writing code |
| [`docs/PROJECT.md`](docs/PROJECT.md) | What this is and is not |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | Eleven releases, one demo command each |
| [`docs/ICEBOX.md`](docs/ICEBOX.md) | Parked ideas. Where mid-release scope goes to wait |
| [`docs/STATE.md`](docs/STATE.md) | Current session state. Rewritten every session |
| [`docs/DECISIONS/`](docs/DECISIONS/) | ADRs |
| [`docs/EVALS.md`](docs/EVALS.md) | Every eval run, dated, with numbers |
| [`docs/LICENSES.md`](docs/LICENSES.md) | Per-source licenses and obligations |

## License

MIT. See [LICENSE](LICENSE).

Game logic data is imported under its own upstream license, recorded per row as provenance and summarised in `docs/LICENSES.md`.
