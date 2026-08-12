# Learning log

Append-only. One section per working session, newest last. Never edit a past entry, add a new one.

Git records what changed and `docs/STATE.md` records where the project stands. This file is only worth keeping if it captures the transferable part. The test for every line: **would this help answer an interview question, or stop the same bug happening in a different repo?** If the answer is no, it belongs in a commit message.

## Template

```markdown
## YYYY-MM-DD — <short label>

Milestone: M1 week N
Touched: <paths>

### What changed

One or two lines. Detail lives in git.

### Concepts

Thing → what it actually does → why it matters here.

### Gotchas

The bug, how it surfaced, and the general rule extracted from it.

### Techniques worth reusing

### Open questions
```

---

<!-- entries go below, newest last -->

## 2026-08-11 — environment, Alembic, and the initial migration

Milestone: M1 week 1
Touched: `src/pylon/models/base.py`, `src/pylon/models/graph.py`, `alembic.ini`, `migrations/`

### What changed

Verified the scaffold runs end to end, then added Alembic and generated the first migration for the five canonical tables.

### Concepts

**uv.** Replaces pip + venv + pip-tools. `uv sync` resolves dependencies and builds `.venv`; `uv run X` executes `X` inside that venv without activating it. Two files matter: `pyproject.toml` declares *ranges* (`mypy>=1.14`), `uv.lock` pins *exact* versions.

**Why the lockfile mattered here, concretely.** Resolution picked mypy 2.3.0, pytest 9.1.1, ruff 0.16.2 — all newer majors than the scaffold anticipated. CI runs `uv sync` and resolves independently, so without the lock committed, "green on my machine" and "green in CI" are different claims about different dependency sets. mypy 2.x under `strict = true` is exactly the kind of thing that drifts. General rule: **applications commit the lockfile, libraries do not.**

**Postgres on port 5433.** `infra/docker-compose.yml` maps `5433:5432` deliberately, so the project never collides with a local Postgres on the default port.

**Alembic's model.** Each migration is a *revision* with `revision` and `down_revision` ids forming a linked list. `head` is the newest. Alembic tracks where a given database sits in a one-row `alembic_version` table it creates itself, so the *database* remembers its own position, not the repo. `--autogenerate` diffs `Base.metadata` (what Python says) against the live schema (what Postgres says) and writes the delta.

**Constraint naming conventions.** `MetaData(naming_convention=...)` makes generated constraint and index names deterministic: `pk_regions`, `fk_locations_vanilla_item_id_items`. Without it Postgres invents names, and a later migration cannot `DROP CONSTRAINT` something it is unable to name. Cheap now, its own migration later, which is why it went in *before* the first autogenerate. Explicit names already given in `__table_args__` (`uq_region_game_name`, `ix_entrance_from_to`) still win over the convention.

**Where the database URL lives.** `migrations/env.py` reads `pylon.config.get_settings().database_url` instead of `alembic.ini`'s `sqlalchemy.url`, which is left unset. One source of truth across CLI, app, and migrations; `PYLON_DATABASE_URL` works everywhere; no credentials are ever committed.

**`compare_type` and `compare_server_default`.** Both off by default. Without them autogenerate detects added and dropped columns but silently misses a `String(64)` → `String(128)` change.

### Gotchas

**1. Autogenerate is a draft, not an oracle.** Both bugs below were in generated code that would have run fine on a fresh database and failed later.

**2. Native enums do not get dropped.** `create_table()` emits `CREATE TYPE` for a native Postgres enum, but `drop_table()` does *not* emit the matching `DROP TYPE`. So `downgrade base` leaves the type behind and the next `upgrade head` dies with *"type itemclassification already exists"*. Fixed by hand:

```python
sa.Enum(name="itemclassification").drop(op.get_bind(), checkfirst=True)
```

Autogenerate never writes that line, and **it is silently lost every time the migration is regenerated** — it disappeared during the regeneration for gotcha 3 and had to be re-added. Native enums carry permanent hand-maintenance: adding a value later also needs a hand-written `ALTER TYPE`, because autogenerate does not detect enum changes either.

**3. A native enum stores member *names*, not values.** This one contradicted the project's own spec. `ItemClassification` is a `StrEnum` whose values are lowercase, and `docs/PROJECT.md` documents the vocabulary as `progression / useful / filler`. But SQLAlchemy's default maps a Python enum by `.name`, so the column only accepted `PROGRESSION`:

```
ERROR:  invalid input value for enum itemclassification: "progression"
```

The ORM path hid it. `session.add(Item(classification=ItemClassification.PROGRESSION))` works either way. It only surfaces on raw SQL, bulk insert, or `COPY`, which is exactly how week 3 will load the full OoT world. Fix in `src/pylon/models/graph.py`:

```python
Enum(
    ItemClassification,
    name="itemclassification",
    values_callable=lambda enum: [member.value for member in enum],
)
```

General rule: **when an ORM abstraction hides the wire format, test the path that bypasses the ORM.** A green ORM round-trip proved nothing here.

**4. Generated files must pass the project's own lint gate.** Alembic's stock template emits `from typing import Sequence, Union` and long lines: 11 ruff errors in a file nobody hand-wrote, which would fail CI. Two fixes, both permanent — rewrote `migrations/script.py.mako` to modern typing, and enabled ruff post-write hooks in `alembic.ini` so every future revision is auto-fixed and formatted at generation time.

### Techniques worth reusing

Verifying a migration properly is a round-trip plus an empty-diff check:

```bash
uv run alembic upgrade head          # applies
uv run alembic downgrade base        # must leave zero tables AND zero leftover types
uv run alembic upgrade head          # proves the downgrade was actually complete
uv run alembic revision --autogenerate -m "probe"   # must be empty, then delete it
```

The second `upgrade` is what caught gotcha 2. The empty probe proves models and schema agree; if it is not empty, the migration does not match the models. Both checks are cheap and neither is habitual for most people.

Fix schema mistakes while the migration is uncommitted and the tables are empty. Regenerating was free here; an `ALTER TYPE` migration after ingest would not have been.

### Open questions

- CI has no Postgres service, so nothing in CI exercises the migration. The round-trip above is local only, and M1's definition of done will be judged on it.
- `uv run mypy src` does not cover `migrations/env.py`, which is hand-written project code sitting outside the type gate.
- Carried over: does OoT age-state (child/adult `Time_Travel`) belong in the core model or in the OoT adapter? Needs an ADR before week 3.

## 2026-08-11 — a public repo cannot consume a private GitHub Action

Milestone: M1 week 1 (side quest, abandoned)
Touched: nothing that survived. PR #2 closed.

### What changed

Nothing. Tried to adopt a private PR-review action into this repo's CI, hit a platform
constraint, and backed the whole thing out.

### Concepts

**Action resolution respects repository visibility, and the direction matters.** A private
repo can share an action with other repos owned by the same account via *Settings → Actions
→ General → Access*, which sets `access_level: "user"`. That policy does **not** extend to a
*public* consumer. The failure is at job setup, before any step runs:

```
##[error]Unable to resolve action `khoa002/materia`, not found
```

The access policy was already `user` when this failed, so the setting is not the missing
piece — the consumer being public is.

**The workaround, and its real price.** A private action can be cloned rather than resolved:
check it out with a read token into a path, then `uses: ./that-path`. Composite actions work
fine from a local path, including ones that nest other actions. It works, but it costs a
second long-lived credential in a public repo's secrets, on a separate expiry clock, and fork
PRs get no secrets so the job has to be skipped for them or it fails red on every outside
contribution.

### Gotchas

**Deleting a GitHub secret does not revoke the credential it held.** From the Claude Code
GitHub Actions docs: *"If you delete a secret, the credential it held stays valid."* Removing
the secret only removes the workflow's access. The token itself has to be revoked at its
source — for a GitHub PAT, in account settings. Two orphaned credentials came out of this
detour, which is the actual lesson: **each credential a CI experiment mints is a rotation
obligation, whether or not the experiment ships.**

**A `403` on a git clone is authorization, not authentication.** A token that cannot see a
repo at all generally gives `404`. `403` means the credential was accepted and its
permissions were refused — for a fine-grained PAT, usually repository scope left at "Public
repositories" or `Contents` not set to Read.

### Techniques worth reusing

Push the cheap experiment before designing around a constraint. The whole visibility question
was settled by one commit and a 4-second job. Reading docs would have suggested the answer;
the failed run proved it, and proved the access policy was not the missing piece.

Read the vendor's own prerequisites first. This constraint was documented in the action's own
adoption guide before any of this started.

### Open questions

- Revisit only if the action's repo is ever made public, which collapses adoption back to a
  single `uses:` line and no extra credential.
