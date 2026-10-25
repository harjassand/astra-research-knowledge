# Optional research-workflow observations

This sidecar fills a recording gap in the existing matched-evaluation system.
It records how a research instance began, what context it retained, what it cost
when measurable, its decisive advance or failure, and its scientific status.
It does not execute a model, label unseen tasks, rank prompts or certify outcomes.
Historical ledgers and [`PROTOCOL.md`](../PROTOCOL.md) remain unchanged authorities.

The [first completed methods tranche](FIRST_METHODS_TRANCHE_20261025.md) is a
descriptive report with an explicit sample and comparison limits. Its curator
extraction adds no reporting requirement or sealed-evaluation claim.

Copy [`WORKFLOW_TRACE.json`](../templates/WORKFLOW_TRACE.json), preserve cleared
exact initiating prompt and output bytes, and store a new versioned record in
`evaluation/workflows/records/RW-<stable-id>/v0001.json`. Hash-pin earlier versions
for reassessment. Never rewrite earlier usage, failure or verification records.

Choose a primary mode and record the actual conversation/context separately:

| Mode | Meaning |
| --- | --- |
| `targeted_warm_continuation` | Same conversation, targeted continuation of its current research |
| `fresh_direction_retained_context` | New direction in the same conversation with earlier context retained |
| `new_instance` | New research conversation; supplied context still needs explicit description |
| `source_intensive_multi_agent` | Source-heavy coordinated research; worker use recorded independently |
| `independent_selective_capital` | Independent research with explicitly selective access to Astra Capital |
| `UNKNOWN` | Evidence does not establish the initiating configuration |

These categories can overlap; use the primary intervention being studied and
describe other factors in context and receipts. “Independent research” means
an independent agenda or instance, not independent correctness verification.
Exact context exposure can be unknown even when the mode is source-reported.
Do not reconstruct missing prompts from an output or infer retained context from
topic similarity. Old process notes remain historical evidence, not backfilled
traces with invented settings or elapsed inference.

Record model/provider/version/reasoning settings when known; otherwise `null`.
Reported inference duration is separate from measured wall/CPU/GPU time and
token/call expenditure. Usage has the same charge names as the matched protocol,
including context repetition, preparation, retrieval/checking, failed attempts
and all workers. A measured value, including zero, needs a receipt; unknown is
`null`. Worker invocations and peak parallel workers are distinct. A reported
duration is not an actual resource receipt or a basis for estimating tokens.

An advance needs exact output and scoped evidence references. Correctness,
independent checking, novelty, significance and technological readiness remain
separate. High verification labels require an independent receipt bound to the
exact output hash; this validates receipt linkage, not expert independence or
scientific truth. Producer diagnostics and compiled manuscripts remain internal
evidence. Failed, missing, aborted and timed-out attempts belong in the record;
do not retain successes only or silently reroll a failed attempt.

The scientific objective is **independently consequential and subsequently
established advances per inference expenditure**. Paper/card/worker counts are
not that metric. Consequence requires a separately justified significance and
priority review, and establishment requires appropriately scoped independent
proof, computational or experimental validation. No such gain is established
by this architecture or its fixtures.

To test prompting or workflow advantages, preregister the intervention, genuine
tasks and decisive gates under the existing matched protocol; freeze source and
context access, model configurations, controls, budgets and denominators. Treat
retained conversation context as an information treatment, account for its
creation, and do not compare it to an uninformed fresh instance as though only
prompt wording changed. Record every assigned attempt and independent blinded
outcome with uncertainty. The current registrar retains mandatory raw-archive
and structured-repository arms; this sidecar does not expand or relax those arms.
Other interventions need an explicit future compatible protocol extension before
claiming controlled superiority. Optional `matched_run_id` must reference an
actual registered run with identical output hashes and usage, not navigation rows.

```sh
python3 evaluation/workflow_trace.py validate --include-fixtures --immutable-base <full-PR-base-SHA>
python3 evaluation/workflow_trace.py report
python3 -m unittest discover -s evaluation -p 'test_*.py'
python3 evaluation/research_eval.py validate
```

Reports show descriptive live trace counts and missing costs only. Synthetic
fixtures are excluded from the live denominator; prior versions are retained but
not counted as new attempts. This release includes only a missing-run fixture,
with unknown prompts, outputs, model and costs. No real trial was registered.

Matched tasks, prompts and gold stored privately by the existing registrar must
stay private. This sidecar is for cleared public observations only; do not expose
private task statements, arm mappings, reference answers, datasets, proprietary
inventions or credentials. A disclosure assertion and hashes do not grant consent.
