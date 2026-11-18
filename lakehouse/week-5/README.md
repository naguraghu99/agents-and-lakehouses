# Week 5: Data Quality & Governance

## Goals

- Add governance and metadata discovery to the lakehouse
- Validate data quality with simple assertions
- Inspect Iceberg history for auditability
- Define catalog-driven accountability and lineage

## Topics

- Data quality checks and validation
- Iceberg metadata history and lineage
- Governance best practices for local lakehouse projects
- Catalog discovery and compliance checks

## Prerequisites

- Week 2 done (you have a Gold layer to assert against).
- Hiver Phase 4 context: lineage connects silver version → golden label → score.

## Expected artifact

- DQ assertions on Gold (nulls, dupes, referential integrity) wired as a step in the pipeline,
  plus a written lineage/auditability note.

## How to run

```bash
python week-5/dq_checks.py              # assertions over the gold tables
# then inspect catalog history:
curl -s http://localhost:8181/v1/config # Iceberg REST is a JSON API, no UI
```

## Definition of done

- [ ] DQ assertions on gold (nulls, dupes, referential integrity)
- [ ] Lineage documented: silver version → golden label → score
- [ ] Iceberg metadata history inspected for auditability
- [ ] Golden `tweet_id`s held out from retrieval (no eval leakage)

## Common mistakes

- **DQ as an afterthought.** Run checks in the pipeline, not by hand in a notebook.
- **Ignoring eval leakage.** Week 5's governance includes the golden holdout — see
  `concepts/14` and `concepts/16`.
