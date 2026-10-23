# Fixed finite-grid replay: results and cost audit

**Status:** one bounded synthetic run completed. This is a sampler/cost-mechanics check, not a general learner result. The initial frozen challenge remains byte-for-byte at `PUBLIC_REPLAY_CHALLENGE_FROZEN.md`; its authorized amendments are listed in `FROZEN_OPENING_AMENDMENT.md`. The first executable run is retained under `v1_superseded/` with its known accounting omissions documented.

## Setup and information boundary

The source is the exact recurrence `u[0]=b; u[k+1]=a*u[k]*(1-u[k])`, `K=6`. The prior is uniform over 256 cell-centered points, `a_i=(97+2i)/32` and `b_j=(19+6j)/128`, with `i,j=0,…,15`. Nodes use the hull of their included grid centers, so singleton nodes are exact points. Each task observes a count `s` from `n=8` with `p=1/8+3f/4`. There are eight tasks and sixteen posterior outputs per task. The next count is `(s + final_lead_index + 1) mod 9`, starting at `s=3`.

The lead method receives only its paid interval nodes and the current count. OS* receives its own paid interval tree and exact point evaluations. The full-grid comparator pays for all 256 exact point evaluations and caches one exact posterior weight/CDF vector per distinct observed count. All three receive the same realized lead-generated count sequence `[3,1,1,5,3,5,2,1]`; controls’ outputs do not change that sequence. Their random tapes are independent. No empirical frequency comparison is used to claim a sampling law.

For the lead, a cell is proposed with probability proportional to its prior mass times a certified likelihood upper bound. A point is uniform in that cell. The original selected cell's `U_old` stays pinned while the same lazy uniform is compared exactly to `L/U_old` and `U/U_old`; a split happens only after the uniform is certified to lie between those bounds. On acceptance, the proposal factor cancels:

`(prior mass * U_C) * (1 / number_of_points_in_C) * (W(x)/U_C) ∝ prior(x) * W(x)`.

The remaining unresolved interval is subdivided until the exact point likelihood decides the comparison. This is exact under ideal independent fair bits and almost-sure termination. OS* uses the standard exact point-rejection ratio `W(x)/U_C`; after a rejection it retains the exact point and splits the original proposal cell. The full-grid method samples directly from exact normalized weights. The executable uses deterministic Python `random.Random` tapes, so the exact-law statements are conditional proofs, not claims that this finite PRNG transcript itself is an iid sample.

## Run results

| Method | Paid source calls | Recurrence steps | Likelihood conversions | Proposal trials / rejects | Outputs | Measured seconds |
|---|---:|---:|---:|---:|---:|---:|
| Demand-refinement lead | 273 interval-node calls | 1,638 | 883 | 160 / 32 | 128 | 7.35 |
| Retained OS* | 173 interval-node calls + 101 exact point calls = 274 total | 1,644 | 769 | 187 / 59 | 128 | 5.71 |
| Exact full-grid cache | 256 exact point calls | 1,536 | 1,024 (256 per each of four distinct counts) | direct CDF draws / 0 | 128 | 1.17 |

OS* later reused 64 of its paid exact point values when those locations became singleton tree nodes. Those reuses did not trigger another recurrence call. The full-grid comparator pays for every grid value and still wins this fixture in source calls, recurrence steps, operation count, and measured runtime. It is a competent same-interface control, not a free evaluator oracle.

Task-start evidence-ratio certificates `c=Z_lower/Z_upper` were:

| Task | `s` | Lead `c` | OS* `c` | Full-grid `c` |
|---:|---:|---:|---:|---:|
| 1 | 3 | 0.005010 | 0.005010 | 1 |
| 2 | 1 | 0.137247 | 0.013654 | 1 |
| 3 | 1 | 0.529038 | 0.422917 | 1 |
| 4 | 5 | 0.852333 | 0.783435 | 1 |
| 5 | 3 | 0.745560 | 0.691274 | 1 |
| 6 | 5 | 0.886035 | 0.842781 | 1 |
| 7 | 2 | 0.855739 | 0.677458 | 1 |
| 8 | 1 | 0.916185 | 0.695151 | 1 |

All 16 interval certificates from lead and OS* enclosed the exact task-start evidence computed from the full-grid control's already-paid weight cache; the full-grid certificates equaled that evidence. This separate post-run check used 32 exact integer cross-product comparisons and took about 0.004 s. The lead replay ran first from `LEAD_PUBLIC_TRANSCRIPT.json`; only afterward did the verifier open the OS* and full-grid transcripts. The full-grid table is not passed into either interval method.

Each displayed task group contains sixteen posterior outputs. If converting the source theorem's per-output `Lambda_t/c_t` term using the conservative group-start certificate, count `16*Lambda_t/c_t` for that group (equivalently index all 128 outputs), rather than charging the factor once per group. Within a task, interval refinement only tightens the evidence bounds, so its start `c_t` is a conservative lower bound for later draws in that group. These realized certificates do not estimate the theorem's expected cost.

## Arithmetic, random bits, storage

The operation counts below include the instrumented exact rational additions, subtractions, products, divisions and comparisons, plus lazy-uniform integer cross-product comparisons and `randbelow` comparisons.

| Method | Instrumented operations | Requested GCD reductions | Max reduced rational numerator / denominator bits | Max integer temporary bits | Random bits |
|---|---:|---:|---:|---:|---:|
| Lead | 72,892 | 63,838 | 6,122 / 6,129 | 12,257 | 1,693 |
| OS* | 64,466 | 56,219 | 6,122 / 6,129 | 12,257 | 1,950 |
| Full-grid | 22,141 | 19,964 | 6,120 / 6,121 | 12,241 | 1,153 |

Random-bit breakdowns were lead: 1,244 proposal-CDF, 216 within-cell and 233 threshold bits; OS*: 1,369 proposal-CDF, 340 within-cell and 241 threshold bits; full-grid: 1,153 posterior-CDF bits. The tapes and segments are public and replayed exactly. The actual serialized public transcript sizes were 12,810,513 bytes (lead), 12,102,592 bytes (OS*) and 7,832,945 bytes (full-grid).

Exact-value binary payloads retained at the end were:

| Method | Node/table values | Likelihood or posterior weights | Retained proposal CDF boundaries |
|---|---:|---:|---:|
| Lead | 168,898 B node endpoints | 2,381,406 B likelihood bounds | 312,210 B |
| OS* | 141,250 B node endpoints | 1,966,098 B likelihood bounds | 270,886 B |
| Full-grid | 49,150 B grid table | 3,139,770 B weights plus CDFs | included with weights/CDFs |

The refinement methods evicted old active-tree CDFs after a split: they created 10,349,896 B (lead) and 7,675,406 B (OS*) of temporary proposal-weight fraction payload over the run, with peak exact-fraction working payloads of 617,982 B and 524,829 B. Cumulative evicted CDF-boundary payloads were 11,389,600 B and 9,113,125 B. OS* also retained 37 exact point values that did not later become tree singletons (7,104 B of numerator/denominator payload); the other paid points were represented by singleton nodes.

These are binary payload sizes for exact numerator/denominator values, not process RAM estimates; Python object, dict/list, allocator and interpreter overhead is excluded. The arithmetic ledger records explicit wrapped rational operations and their integer operand/temporary/result bit lengths. It does not count Python `Fraction` constructor reducedness checks, setup constants, bit assembly/shift instructions, or every interpreter instruction. Elapsed time is a single measured run on this host, not a stable performance benchmark. Research/development and proposal-discovery time is unmeasured.

## Interpretation and limits

This run does not show a learner advantage. The strongest included conventional control, exact full-grid caching, is cheaper on the measured source/execution costs in this 256-point fixture. The retention controls are not an exhaustive catalogue; for example, a partial-cache proposal mixture can retain known exact point weights and use a valid global `W_max` for unqueried points. No favorable regime, parameter sweep, or general practical-cost superiority is claimed.

The stated finite-grid source-bound analysis has `C_K=3413.25` and `Lambda=48` for this `K=6`, `n=8`, `epsilon=1/8` instance. Optimizing its explicit source bound over `H∈[0,4]` selects the full 341-node cap for any `A≥1`. Thus this fixture checks the exact replay, pinning, cost and certificate machinery; it does not reach the nontrivial exponent-guarantee regime.

The exact denominator worst-case bounds remain exponential in `K`: for this grid `u_K` denominators are bounded by `2^889`, `p` by `2^891`, and a single `n=8` likelihood by `2^7128`. Executed reduced fractions peaked at 6,129 denominator bits, while intermediate cross-products reached 12,257 bits. Those are manageable at this small setting but prevent source-call counts alone from supporting a practical-cost claim.

## Reproduction and files

Run `python3 benchmark.py` to regenerate the fixed transcripts using the evaluator-only seed manifest. The public `replay_public.py` reads only the lead transcript first and does not need that manifest; it then checks OS* and full-grid outputs, events, bit segments, and exact paid table. `PUBLIC_REPLAY_VERIFICATION.json` contains the pass record and task-start evidence checks. The seeds are kept separately in `private_evaluator_seed_manifest_DO_NOT_PASS_TO_LEARNER.json` and do not appear in public transcripts or summaries.
