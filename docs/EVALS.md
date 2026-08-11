# Eval runs

Append-only log. One section per run. Never edit a past entry, add a new one.

Populated from Milestone 3, week 10 onward. Milestone 1 golden cases live in `tests/` as plain pytest; this file starts when the agent layer exists and quality becomes a measurement rather than a pass/fail.

## What gets measured

| Scorer | What it checks | Ground truth |
|---|---|---|
| Tool selection accuracy | Did the agent call the right tool | Hand-labeled per question |
| Argument correctness | Were the tool args right | Hand-labeled per question |
| Route validity | Does the returned route satisfy the prerequisite graph | ⭐ Pure Python check, objective, no judge model |
| Grounding | Does every factual claim map to a returned tool result | Automated, unsupported claims flagged |
| Cost | Tokens and dollars per question | Measured |
| Latency | p50 and p95 | Measured |

Route validity is the important one. It is objectively checkable, which is the entire reason this project was chosen over a prose-based one.

## Template

```markdown
## YYYY-MM-DD — <short label>

Golden set: vN (<n> questions)
Model: <model id>
Change under test: <what moved since the last run>

| Metric | Value | Delta |
|---|---|---|
| Tool selection accuracy | | |
| Argument correctness | | |
| Route validity | | |
| Grounding | | |
| Cost per question | | |
| p95 latency | | |

Notes:
-
```

---

<!-- runs go below, newest last -->
