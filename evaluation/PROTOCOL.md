# Research effectiveness: sealed, matched, independently adjudicated

Current evidence establishes navigation behavior only. The preserved development fixture has 12 queries and 18 required card spans. Baseline and enhanced scripts each recovered 14/18 full spans; their realized packets were identical in aggregate (mean 1,352.25 o200k tokens and 5,341.33 bytes), under ceilings of 1,500 tokens and 6,000 bytes. There were zero model calls. The fixture and gold spans are public and have been used in engineering: treat them as exposed development data, never as unseen scientific tasks. The flat BM25 arm recovered 8/18 full spans and the bundle arm 13/18. These are historical observations of that frozen corpus, not current-corpus replay results or proof validation.

`FROZEN_TASKS.jsonl` is deliberately empty: no independently acquired unseen research tasks have been registered. `MODEL_COMPARISONS.jsonl` and `VERIFIED_OUTCOMES.jsonl` contain scoped historical navigation evidence; they establish no theorem-discovery advantage, independent scientific verification, novelty or Astra capability improvement. The word VERIFIED in the filename never upgrades the `kind`, scope or checker status of a record.

The local standard-library CLI `research_eval.py` registers evidence and checks hashes, schemas and budgets. It never calls a model, runs a scientific checker, establishes expert independence, certifies that a model never saw a task, or verifies a theorem. Registering an experiment is not authorization to execute it. No new model experiment is part of this repository restructure.

## Admission and sealing

An evaluator independent of the repository builders and run operators acquires genuine research problems and a proof-gate contract before seeing experimental outputs. Start with feasible subtheorems, valid transfers, counterexample construction or proof repair with decisively checkable outputs. Do not select problems because the enhanced system already solves them. Label task split `development` or `unseen_candidate`. Public repository searches, provider disclosure and prior operator/worker exposure are logged; `unseen_candidate` requires independent acquisition attestations, logged no-match screening and no known operator exposure. Foundation-model pretraining exposure is always `unknown`. A hash commitment and an attestation do not establish absolute novelty or unseen status.

Use opaque task IDs. Keep statements, exact common inputs, gold/reference proofs, grading definitions, provider receipts and contamination screens in an evaluator-only directory **outside this repository**, mode 0700. Do not publish private material, working gold, answer locations or arm mappings. The registrar copies exact bytes, records their SHA-256 and byte length, and commits a canonical manifest before the run. The public task ledger reveals IDs/hashes/contamination labels only. Source filenames are not exposed. Public hashes are commitments, not encryption; the private store and task-provider access controls are required.

Gate contracts state exact assertion, quantifiers, assumptions, legal information interface, supplied/acquired boundaries, precision and costs, permitted tools, and explicit acceptance requirements. Each gate has a distinct ID and kind: full mathematical proof, formal kernel declaration, counterexample, subtheorem, finite diagnostic, scope interface or novelty review. Primary IDs are frozen; success requires **every** primary gate. A finite test, compile or archive-integrity check cannot be substituted for a general proof. A valid counterexample is a scientific outcome even when it defeats the motivating conjecture. Novelty gets a separate source/priority review gate and cannot be inferred from correctness.

## Arms and resource parity

For each matched model configuration, freeze two mandatory arms: `raw_archive` and `structured_repository`. They expose the **same acquired source mathematics**, with one exact raw-source inventory hash; the structured arm adds the navigation/lemma/frontier representation being tested. Freeze both versions and hold them fixed. A `no_repository` arm is optional and measures the effect of additional information; it does not isolate structure. All arms receive the same task statement, gate acceptance rules, common input contracts and allowed external information. Reference solutions, gold locations and held-out tasks remain hidden from retrieval indexes.

The public arm IDs are opaque; store the condition mapping privately. Randomize task/run order and record the assignment file before any run. Use separate clean worker contexts and isolated filesystem/tool permissions, without shared scratch, exposed answer ledgers, cross-arm messages or result feedback. A same-directory agent cannot be assumed blinded merely because it is instructed to ignore a file. Checkers receive anonymized exact output bytes and task contracts, without the arm mapping. This CLI commits mappings and checks recordings; process isolation and actual blinding require the evaluator's independent implementation and receipts.

Freeze provider, model ID, available immutable version, reasoning effort, context-window size, tokenizer and tokenizer version. Reject `latest`/`unknown` version labels. If the provider does not expose a reliably fixed version, record that limitation and do not claim strict version control. Compare model configurations in separately stratified experiments; this registrar's paired arms must use identical models, tool policies, hardware/compute recipe and maximum budgets. Preserve real request IDs/version receipts in the sealed transcript.

Exact budget keys are `context_tokens` (peak), `input_tokens_total`, `output_tokens_total`, `model_calls`, `tool_calls`, `wall_seconds`, `cpu_seconds`, `gpu_seconds`, `compute_usd`, `parallel_workers` (peak). Token totals include prompts, retrieved material, context repetition and failed calls; tool totals include acquisition/retrieval/checking. CPU/GPU time aggregates workers. Wall time includes experiment-specific setup and preparation; charge prebuilt index construction as a stated, frozen amortization schedule with both marginal and total cost reported in the resource receipt. Zero is measured zero, never unmeasured. Unknown actual usage is recorded as `null` and makes the run cost-ineligible. Missing, failed, timed-out, aborted and over-budget attempts remain in the assigned denominator; no free rerolls or hidden screening calls.

Retrieval-only accuracy and latency are useful secondary engineering measures. The primary scientific metric is independently adjudicated passage of all frozen primary proof gates per assigned task at the identical budgets. Also report correct repaired claims, valid counterexamples, failed transfers, residual proof gates, cost, and completion. Publish paired task-level results and uncertainty appropriate to the sample size; a few successful demonstrations do not establish broad capability. Follow-up checks and selection must be charged and disclosed. No comparative gain is claimed from an incomplete or exposed trial.

## Recording and review

Register the task and comparison plan before starting any model call. Do not rewrite accepted JSONL rows; use new IDs and explicit later reassessment receipts. CLI mutations are serial; a lock guards appends. Run artifacts contain exact submitted proofs/code, complete transcript, model configuration and resource receipts. The CLI rejects duplicate task/arm/replicate records, begins-after-freeze violations, changed sealed bytes and undeclared resource fields. It retains over-budget and unknown-cost failures without awarding primary success.

An independent external expert or independent formal-checker operator submits a checker receipt tied to the exact output SHA-256. Record one result for each frozen gate, including failed/unknown/not-assessed. Include mathematical criticism or exact checker declaration, version, command, logs and scope; no placeholder verification. Checker independence and blinding need evidence. The registrar can require their receipts but records them as **attested**, not certified. Internally agreed proofs and producer-run diagnostics belong in ordinary claim evidence, not new independent outcome rows. `report` produces descriptive counts, paired task results, measured charges and missing-run flags only; it does not infer discovery, historical priority, significance or model superiority. When every assigned run has an outcome, an evaluator supplying `--private-root` can reveal the committed arm mapping in the report; public-only reports keep the mapping sealed.

Historical navigation rows have `kind=historical_navigation_*`, `scientific_discovery_evidence=false`, `independent_scientific_verification=false`, and a precise original-byte receipt. They remain separate from future `comparison_plan`, `run_record`, and `checker_outcome` rows.

## Local commands

Commands below are registration/validation examples, not authorization to run a trial. Use the JSON shape templates in `templates/`; REPLACE values are placeholders, not registered tasks or results.

```sh
python3 evaluation/research_eval.py validate
python3 -m unittest discover -s evaluation -p 'test_*.py'
python3 evaluation/research_eval.py --private-root /absolute/evaluator/private register-task task-contract.json
python3 evaluation/research_eval.py --private-root /absolute/evaluator/private register-comparison comparison-plan.json
python3 evaluation/research_eval.py --private-root /absolute/evaluator/private record-run run-record.json
python3 evaluation/research_eval.py --private-root /absolute/evaluator/private record-outcome checker-receipt.json
python3 evaluation/research_eval.py --private-root /absolute/evaluator/private validate
python3 evaluation/research_eval.py report comparison-id
```

Paths inside supplied JSON contracts are read as filesystem paths from the caller's working directory. Use absolute paths to remove ambiguity. Create the private directory with mode 0700 first. The registrar does not generate an unseen task, run a solver/model, hide files from workers, or execute checker commands.

The common-information SHA-256 is computed from the exact public task commitments: canonical JSON of `{task_id: [file_record for task_file if kind in (task_statement, common_input, proof_gates)]}` across the registered task IDs, with keys sorted, separators `(',',':')`, UTF-8, `ensure_ascii=False`. Both informed arms' `allowed_information_manifest_sha256` is the SHA-256 of the same exact raw-source inventory file, including original source hashes; arm-specific representations have their own frozen snapshot/version in `compute_recipe`. The registrar verifies byte equality of the inventory commitments; semantic completeness, leakage screening and information parity require the evaluator's review.

The small unit-test fixtures use synthetic bytes solely to attack registry bookkeeping in temporary directories. They are never admitted as unseen scientific tasks or appended to published ledgers. No scientific scripts, models, external checkers or paid services run in those fixtures.
