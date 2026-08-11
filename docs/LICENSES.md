# Data source licenses and obligations

Written before any ingest code. Every ingested row records `source`, `source_version`, `license`, `upstream_url`, and `ingested_at`. This file is the human-readable summary of what those values obligate us to.

Pylon's own code is MIT. Imported data keeps its upstream license.

---

## ✅ Approved

### OoT Randomizer

- **URL:** https://github.com/OoTRandomizer/OoT-Randomizer
- **License:** MIT ("All files are MIT licensed unless stated otherwise"; some folders are GPLv2+, avoid those)
- **What we take:** `data/World/*.json` and `data/LogicHelpers.json`
- **Obligations:** include the MIT notice and copyright. Attribute in `README.md` and per-row provenance
- **Notes:** fully declarative region graph with string boolean expressions. This is the reference schema

### ArchipelagoMW

- **URL:** https://github.com/ArchipelagoMW/Archipelago
- **License:** MIT
- **What we take:** region, entrance, location, and item structure from `worlds/` modules, plus rule dependency sets recovered by black-box probing
- **Obligations:** MIT notice and copyright. Attribute per-row
- **Notes:** rules are Python lambdas, not data. We call them rather than parse them. See `docs/ROADMAP.md`

### sm-json-data (Super Metroid) — deferred

- **URL:** https://github.com/vg-json-data/sm-json-data
- **License:** CC BY 4.0 (per `LICENSE.txt`)
- **Obligations:** ⚠️ **attribution is mandatory and must survive redistribution.** Credit in README, in API responses, and in per-row provenance
- **Notes:** a second `LICENSE.md` with unclear terms also exists in that repo. Resolve which governs before ingesting

---

## ❌ Prohibited

### speedrun.com

- **License:** CC BY-NC 4.0
- **Verdict:** **Do not use.** Two independent disqualifiers:
  1. **Non-commercial only**, and incompatible with CC BY-SA so it cannot be merged with wiki-derived corpora
  2. **There is no route data in the API.** A run is one number plus metadata. The one field that pointed at ordered data (`splits.io`) died 2025-03-31
- Also: `robots.txt` disallows `/api`, the rate limit is 100 req/min per IP, and pagination breaks past ~10,000 items

### SoulsRandomizers (Elden Ring, Dark Souls)

- **URL:** https://github.com/thefifthmatt/SoulsRandomizers
- **License:** none. Source-available but explicitly **not freely licensed**, and distribution of derivative works is prohibited
- **Verdict:** **Do not use.** This is why Elden Ring is not a first target despite being a good fit

---

## ⏸️ Deferred, with a hard constraint if ever used

### StrategyWiki, Fandom

- **License:** CC BY-SA (3.0 or 4.0, varies per wiki, must be checked individually)
- **Constraint:** share-alike is viral. ⚠️ If ever ingested, this content lives in its **own schema and its own storage**, and must never join into the permissively-licensed output path. Add a test that fails if it does
- **Status:** deferred out of the 12-week plan

### PCGamingWiki

- **License:** CC BY-NC-SA 4.0
- **Verdict:** the NC clause blocks commercial use, same problem as speedrun.com. Also holds compatibility data, not progression data

---

## Checklist before adding any new source

1. Find the actual license file. Do not trust a README badge
2. Confirm commercial use is permitted, or accept that Pylon stays non-commercial forever
3. Confirm share-alike status. If viral, it gets its own schema
4. Record the attribution string this file requires
5. Add a row to the approved or prohibited table above
6. Add the source to the table in `CLAUDE.md`
7. Only then write the adapter
