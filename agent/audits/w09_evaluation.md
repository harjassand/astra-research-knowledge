# W09 — bounded evaluation protocol for Astra repository use

## Decision and scope

This is a preregistration proposal, not an evaluation result. It specifies how to test whether the repository improves useful work by Astra while keeping four outcomes separate: (1) retrieval/navigation, (2) correct transfer of a result's information interface, (3) quality of useful novel hypotheses, and (4) actual Astra capability. No paid API calls were made. A 20-worker Luna run can pilot task wording, packet usability, and rubric calibration; it cannot certify Astra performance, research novelty, or a breakthrough.

The knowledge design describes a workload-dependent retrieval system, not a validated universal optimum. `00_START_HERE.txt` says retrieval fixtures establish routing and budgets, not Astra learning quality. The CLI is local and makes no model calls. Its token meter is `o200k_base` when available and otherwise a UTF-8 byte upper bound, not an Astra tokenizer. Therefore freeze and report both the protocol budget and the actual measured bytes/tokens for every presented artifact. Do not describe a local index check as model evaluation.

## Question and estimands

Primary question: under the same task, available evidence, model, and total context/action budget, does structured repository access improve (A) finding the right evidence, (B) preserving its exact interface and limitations, and (C) producing independently judged useful hypotheses, relative to a competent equally informed alternative?

Report four outcomes independently; do not collapse them into one “intelligence” score.

1. **Navigation success:** whether the worker locates the preregistered decisive source/card/proof and cites a resolvable stable source ID and relevant lines. Measure recall@k, reciprocal rank, source-ID validity, citation-to-read success, time/actions, and evidence bytes/tokens consumed. A correct card hit alone does not count as proof retrieval when the task requires a proof.
2. **Interface-transfer correctness:** whether the worker states the object/class, quantifiers, supplied inputs/oracles, acquired inputs, legal outputs, costs, guarantees, dependencies, and failure domain correctly. Use a criterion-level ledger; record omissions, substitutions, and unsupported upgrades. In particular, score passive samples substituted for exact matrix outputs, uncharged oracle/acquisition costs, conditional claims stated unconditionally, and finite diagnostics promoted to proof as distinct errors.
3. **Useful novel-hypothesis quality:** whether a proposed, nonduplicate direction is both technically coherent and useful for a specified next falsifiable step. Score blinded proposals on interface fit, derivation from cited evidence, plausibility, discriminatory prediction, tractability under the resource budget, and value if true. Deduplicate against the frozen repository/prior-art set before rating. “Novel” means novel relative to that frozen set only; priority and external novelty remain unestablished absent literature review and expert assessment.
4. **Actual Astra capability:** performance on the frozen task set when the evaluated model is Astra. Only an Astra run supports Astra claims. Luna results are pilot data for instrumentation and rubric calibration and must not be pooled with, substituted for, or extrapolated to Astra. A system-level advantage requires the Astra arm to beat the declared baseline on preregistered outcomes with uncertainty reported.

## Conditions and equally informed control

Use paired, randomized task assignment across conditions, with fresh model sessions and no cross-condition transcript/state leakage. Keep model version, system prompt, decoding settings, tools, task text, evidence universe, and total budget fixed. Randomize condition order and task IDs. Do not let workers see gold answers or one another's outputs.

- **Structured repository condition:** the documented entry point, topic routers, `knowledge.py` search/packet/read/links interface, and cited full evidence as allowed by the task. Record every query, packet, read, link traversal, and source opened.
- **Equally informed competent baseline:** the same evidence files and source IDs are available through a flat, deterministic file/source manifest plus ordinary filename/text search and direct file reading. The baseline gets the same task statement, evidence universe, maximum evidence bytes/tokens, wall/action budget, and model/tool capabilities. It may not be handicapped by withholding source titles or relevant documents. Its access path is simpler and lacks repository routing, aliasing, packet assembly, and graph navigation. This estimates the value of the structured interface, not the value of giving a model evidence versus no evidence.
- **No-evidence diagnostic (optional, secondary):** same task and model budget but no repository evidence. This estimates the evidence contribution and is not the primary system comparator.

For a retrieval-only subtest, use fixed human-written queries and no model generation: compare structured search/packet against the same manifest plus the baseline search path. For an end-to-end task, let the worker formulate queries and navigate, but preserve a complete action log. Keep these results separate because fixed-query retrieval is not agent navigation.

## Frozen task set and allocation

Before any model sees the tasks, create a versioned manifest with task ID, task type, exact prompt, gold source IDs/line ranges, required proof sources, interface checklist, known counterexamples, expected failure modes, evidence universe, scoring key, and hash of all task/evidence files. Have two humans independently verify keys against originals; resolve disagreement before freeze. Keep a separate held-out set inaccessible to workers, prompt authors, and anyone tuning the router or rubric. Do not use tasks or cards already shown in demonstrations as held-out evidence.

For a bounded first round, use **20 Luna workers as 20 independent task attempts**, each in an isolated fresh session; distribute tasks across four strata (five attempts per stratum):

1. **Direct retrieval/navigation:** identify the right card and decisive primary proof/source; include distractors, alias queries, and a known retrieval edge case such as citation-ID handoff.
2. **Interface transfer:** reconstruct a theorem/result contract, explicitly distinguishing supplied from acquired information and listing costs, bounds, and failure scope.
3. **Negative transfer/counterexample:** apply a representation or obstruction to a nearby task and identify why an attractive shortcut does not transfer.
4. **Hypothesis generation:** propose one next falsifiable direction from a bounded packet, with comparator, missing service/lemma, cost accounting, counterexample, and a discriminating experiment or proof obligation.

Each stratum has one preregistered task template and five task instances. Assign each instance to both access conditions across the worker pool using a counterbalanced schedule; if 20 attempts cannot provide at least five paired instances per stratum, treat strata-level comparisons as descriptive and add no post hoc significance claim. Better, if the “20 workers” means 20 workers per condition, predeclare 40 total attempts and pair them by task. Do not silently change what “20 workers” means after observing results. Workers are repeated model invocations, not independent model families or independent statistical evidence about general capability.

Freeze prompt and tool instructions, temperature/seed if exposed, context cap, maximum 8 retrieval actions per task, wall-clock cap (e.g. 20 minutes), maximum final response length, and total evidence budget (e.g. 12,000 measured tokens per task). Fix values before pilot scoring; the examples here are proposed defaults, not observed optima. Log truncations, timeouts, parser failures, empty retrieval, and abstentions as outcomes, not exclusions.

## Scoring and adjudication

Use separate score sheets and never let a strong navigation score compensate for an incorrect theorem transfer.

- **Retrieval:** gold-source recall@1/@3, reciprocal rank, proof-open rate when proof is required, valid ID rate, citation span overlap, source-opening failures, total actions, elapsed time, and charged input/output bytes/tokens. Report each condition paired by task.
- **Transfer:** for each checklist item, mark correct / missing / incorrect / unsupported. Report exact-interface pass only if all load-bearing items are correct; also report item-level rates and severity-weighted errors. A false upgrade (e.g. reported check to independently replayed proof) is a critical error and must be visible separately.
- **Hypotheses:** remove condition/model labels and randomize proposal order. Two domain-competent raters independently score a preregistered 0–4 rubric for (a) technical coherence, (b) fidelity to cited evidence, (c) a specific discriminating next step, (d) tractability and complete costs, and (e) decision value. Deduplicate before rating against the frozen corpus and bibliography, retaining the duplicate record and source. Report raw dimension scores, agreement, and adjudicated scores. A high score is “promising candidate under this frozen corpus,” never a verified discovery. Verify any leading proposal against exact source/proof bytes and prior art before making a research claim.
- **Astra capability:** after pilot freeze, run the exact protocol with Astra under the same conditions and budgets. Treat model-version changes as a new evaluation. Report per-task paired differences with confidence intervals or exact randomization intervals, plus raw counts; with five paired tasks per stratum, intervals will be wide and conclusions exploratory. No broad capability claim from 20 attempts.

Raters should be blind to condition and model where the output permits. Gold keys should be independently checked against source evidence by two people. Log rubric disagreements, missing expertise, and adjudications. Do not use the generating model as sole judge.

## Cost accounting and acquisition boundary

Record separately: evidence acquisition/download and preprocessing; index build/update; model input bytes/tokens and output tokens; query/packet/read calls and latency; human setup and rating time; tool runtime; persistent repository size; and any external-source or oracle access. The corpus is already supplied in this test: do not count it as free in deployment conclusions. Report sunk corpus cost separately from per-task marginal retrieval cost. Any future external source, paid retrieval/API, oracle evaluation, coefficient extraction, or proof reconstruction is a charged acquisition event and must be logged with source, amount, and returned artifact. Do not conduct paid calls in this pilot.

The represented knowledge can improve access to supplied facts without showing that Astra acquired an expensive representation or can independently reconstruct a result. Score reading, reconstruction, and review separately, consistent with the repository queue. No state update or citation by itself constitutes theorem validation.

## Required replay package

Every task run must save an immutable run record containing: protocol/task-set version and hashes; condition; model/provider/version and settings (or `NOT_RUN`); worker/session ID; prompt hash; all retrieval requests/responses and source IDs/line spans; evidence bytes/tokens and meter; timestamps/actions; final answer; errors/abstentions; raw rubric sheets, rater IDs/blinding, and adjudication; cost ledger; and outcome calculations. Preserve raw outputs before scoring. Provide one replay script or documented deterministic calculation that regenerates aggregate tables from run records; verify it on a tiny hand-checkable fixture. Keep source snapshots immutable and link each cited source to its original hash where available.

The report must include a CONSORT-like flow count: assigned, started, completed, timed out, retrieval/tool failure, excluded with preregistered reason, and scored. Include null/negative cases and counterexamples. Keep the held-out key sealed until all runs and scoring decisions are frozen, then log who opened it and when.

## Interpretation gates

- Better source hit rate alone supports a **navigation improvement** for the frozen tasks.
- Correct interface checklist improvement supports **better transfer on these tasks**, with the exact error distribution stated.
- Better blinded hypothesis ratings support **more promising proposals against this corpus and rubric**, pending source and prior-art audit.
- Only a direct Astra run can support **Astra-specific capability** claims. A Luna pilot cannot do so.
- None of these alone establishes formal proof correctness, external validation, novelty/priority, broad generality, or a breakthrough. Any such claim needs its own evidence and review.

## Repository-specific risks to include in the frozen tests

The interface says citation identifiers may be chunk IDs while `read` accepts document/card IDs; W02 records this as a navigation handoff break. Include it as a declared retrieval failure case, verify current behavior at freeze, and do not make the baseline suffer the same interface-specific defect. W03 and other existing audits can seed risks, but benchmark authors must not cherry-pick only known failures: include blinded tasks from cards/proofs not used to design the benchmark. Source-reported checks, imported records, finite fixture checks, internal reconstruction, formal proof, and external verification must remain distinct labels throughout.

## Stop rules

Stop the pilot after the preregistered 20 Luna attempts and scoring calibration. Do not add tasks, change budgets, tune prompts/router, or redefine “useful hypothesis” after viewing condition outcomes; changes create a new protocol version and require a fresh held-out set. If task keys prove ambiguous, pause scoring for that task, document the ambiguity, repair and re-freeze before exposing condition labels. Advance to the Astra run only after task artifacts, scoring, replay calculation, and cost ledger are frozen. The protocol itself authorizes no paid calls.
