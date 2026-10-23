# Reusable forward certificates for exact adaptive inverse tasks — 24 October 2026

This selected unit preserves the source-reported exact posterior-law and source-execution result, the fixed finite comparison, its public source-query/consumed-bit transcripts, and the superseded first-run record. The [manifest](source_manifest.json) pins 26 selected files against the 0417 and earlier frozen 0357 receipts. The broad receipts and evaluator seed manifests are not copied.

## Conditional law and source-cost theorem

The task is a fixed, known recurrence on a finite grid, `u₀=b`, `uⱼ₊₁=a uⱼ(1−uⱼ)`, `f=u₆`, followed by adaptive binomial posterior requests with positive rational likelihoods. The lead pays for exact rational interval executions of the known code. Its retained tree supplies likelihood bounds to later tasks; it does not infer a global range bound from finitely many point samples of an arbitrary unknown smooth map.

For each proposal, the source pins the original proposal-cell upper height `U_old` and threshold `u` through all refinement. The acceptance event remains `u < W(x)/U_old`, including when a split depends on the candidate and threshold. With proposal mass proportional to prior mass times the cell upper bound, the accepted mass is proportional to `π(x)W(x)`. Conditional on each task's starting history, the output has the requested posterior. The post-acceptance tree may contain information about that sample, so the source does not claim posterior independence conditional on that later tree. Finite-grid singleton refinement and positive weights give almost-sure termination; expected aggregate cost still depends on the task-start evidence bounds.

The [current theorem](source/AMORTIZED_SOURCE_THEOREM.txt) retains its finite-tree cap and expected source-call bound. With `B=2ᵈ` children per split, certifier width at depth `j` bounded by `C·2⁻ʲ`, split depth `H`, and preproposal log-likelihood sensitivities `Λₐ`, the reported form is

`E[N] ≤ min(full_tree, (B^(H+1)−1)/(B−1) + 2BC·2^(−H) E[Σₐ Λₐ])`.

Optimizing fixed `H` gives the stated `O_d(1 + (C E[Σₐ Λₐ])^(d/(d+1)))` bound. For output requests, the source substitutes `E[Σₜ Λₜ/cₜ]`, where `cₜ=Z_L/Z_U` is acquired at task start. A group of `qₜ` outputs under one task label requires `E[Σₜ qₜΛₜ/cₜ]`. These are expectation bounds; realized adaptive certificates are not confidence statements. The earlier [0357 theorem](source/frozen_0357/AMORTIZED_SOURCE_THEOREM.txt), [exact-law contract](source/frozen_0357/EXACT_CONTRACT_AND_INFORMATION_GATE.txt), and [exact denominator check](source/frozen_0357/exact_adaptive_law_check.py) are preserved separately from the current grouped-output amendment.

## Fixed acquired case and actual comparison

The reported execution uses 256 cell-centred grid points, `K=6`, `n=8`, `ε=1/8`, eight lead-generated task labels and sixteen posterior outputs per label. It produces 128 outputs but only four distinct likelihoods. All controls replay the same count sequence, `[3,1,1,5,3,5,2,1]`; the sequence is selected from lead outputs, so it supports no general ranking of methods.

| Method | Paid forward calls | Recurrence steps | Proposals / rejects | Instrumented operations | Random bits | One-run seconds |
|---|---:|---:|---:|---:|---:|---:|
| Demand-refinement lead | 273 interval | 1,638 | 160 / 32 | 72,892 | 1,693 | 7.35 |
| Retained OS* | 173 interval + 101 point | 1,644 | 187 / 59 | 64,466 | 1,950 | 5.71 |
| Exact full-grid cache | 256 point | 1,536 | Direct CDF / 0 | 22,141 | 1,153 | 1.17 |

The [current report](source/luna_batched_mean/RESULTS.md) records the full arithmetic, rational-size, temporary-storage and transcript-size ledgers. The full-grid control pays for all 256 exact point values and wins this fixture in source calls, recurrence steps, operation count, random bits and measured time. OS* reuses 64 paid point values when they later become singleton nodes. The lead's repeated `s=1` task-start certificate rises from `c=0.137247` to `0.529038` and then `0.916185`; the full-grid table gives its control `c=1`.

For this case, `C_K=3413.25` and `Λ=48`; the explicit theorem bound already saturates the full 341-node tree cap for every `A≥1`, before outputs are inspected. The run therefore does not demonstrate the nontrivial exponent-guarantee regime. It also does not show an advantage over the conventional cache. The source identifies strong overlap with Moore interval rejection, OS* and A*; novelty of the precise cross-task cost theorem remains `UNKNOWN`.

## Replay, audit, and version history

The current [public replay package](source/luna_batched_mean/) preserves the lead, OS* and full-grid source-query and consumed-bit transcripts, the opening amendment, current cost summary and producer replay-verification record. The [v1 directory](source/luna_batched_mean/v1_superseded/) keeps the first run and its known omissions: obsolete proposal CDFs were retained, 64 OS* point calls were not reused at later singleton nodes, the reported normalizers were final-tree instead of task-start intervals, and the replay opened the full-grid transcript before replaying the lead. The current version documents its repairs without overwriting the first run.

The full-grid transcript contains the exact table acquired and paid for by that comparator; it is retained as a public control transcript. The separate evaluator audit table is not copied or passed to the lead/OS* materials. The producer's audit code and aggregate record are kept at `source/independent_transcript_audit.py` and `.json`, outside the learner replay folder. The private evaluator seed manifests are excluded from both versions. The retained benchmark generators refer to those omitted seed manifests, so they are source evidence rather than directly runnable public learner inputs.

The source reports 100 one-trial mass identities, 25 eventual posterior laws, 16 joint identities, and the wrong-denominator counter. It also reports the corrected public replay and a separate evaluator audit over 256 exact responses. These remain producer-reported checks: this integration verified selected bytes against their receipts and did not execute a benchmark, replay, exact-law checker or evaluator audit, and did not independently validate the theorem or audit conclusions. The mathematical sampling claims assume ideal independent fair bits; the recorded deterministic PRNG tapes establish conditional replay only.

## Scope and open boundaries

The bound counts paid source executions. Likelihood conversion, proposal maintenance, exact arithmetic and integer growth, random bits, storage, rejection trials, validation and discovery work remain separate costs. The reported conservative interval constant grows exponentially with `K`; total research/development effort and practical crossover are unmeasured. This is a finite known-program sampling result, not a physical logistic-law validation or a claim of practical learning advantage. No physical experiment or novelty is established.

The nearby [P3 finite-evidence update](../2026-10-24-p3-finite-evidence-operations/README.md) concerns retained correlations and finite-schedule variance; this unit concerns exact adaptive posterior draws and paid forward-range certificates. They remain separate results.
