# Frozen Markov query transfer: a small conventional interface check

## Outcome and interpretation

The admitted Pro3 expansion fixture supports the observation-equivalence operation, with a consequential restriction: the valid representation depends on the query. Conventional exact probabilistic partition refinement recovers the original **6-level quotient** for the entire terminal level, but produces **24 blocks** for the frozen proper subset A={15,16,19,26}. Those 24 blocks preserve every finite binary observation-history law for every initial distribution.

At the original horizon64 and original native proposal start, the refined chain exactly matches full native propagation for the entire first-hit distribution, first-hit time jointly with final membership, and exit followed by reentry. The six-level representation cannot observe the subset. Even adding subset-membership to the level gives a nonlumpable seven-block representation.

The most useful failure is that the seven-block chain's natural q-weighted averaged kernel gives the **exact correct endpoint subset mass**, while giving the **wrong first-hit and return laws**. Endpoint checks alone would have accepted the wrong representation.

This is a small local receiving-operation check. Thirty-two native states do not constitute a difficult capability benchmark. The successful method is ordinary exact Markov aggregation; no separate acquired-method arm outperforms it. The experiment establishes neither new scientific reach, representation invention, a novel algorithm, nor stronger general intelligence.

## Frozen operation and source

The source was not changed:

- Native fixture: expansion_native32 in Pro3 Cycle9 evidence/exact/EXACT_INPUTS.json.
- A breadth-first-labelled binary tree of depth4 has vertices0–30; native core is31.
- Parameters remain eta=1/2, kappa=4, R=3/2, M=2, n=64, b=1/2, p=1/512, alpha=1/2 and KL budget K=1.
- The actual native kernel is C=(I+alpha G+(1-alpha)L)/2, including global moves, local moves, rejections and every return.
- Start is the actual native q, uniform within each original level.
- New observation is membership in A={15,16,19,26}; original event is all terminal vertices15–30.

The producer's source rigorously admits this fixture, with recorded KL about0.7871982549<1. Admission is inherited from that source. The new adapter independently required exact agreement of q, pi, original level C, native proposal/local edge digest, native stochasticity and detailed balance. Its computed final native law, aggregated into the original levels, also equals the source's saved full law at n=64.

The larger coalescence_native5462 fixture was not run and is not scientific evidence here: its frozen KL admission fails K=1. No larger replacement fixture was invented.

The protocol, proof, complete worker code, scientific source code, inputs and admitted evidence were hash-frozen at 2026-10-22T19:12:13.217264+00:00, before native preparation or refinement. Event, horizon, model, algorithm and resource caps were not changed after outcomes. The only initial launch failure was an unavailable /usr/bin/time binary; no worker started. That failure is retained, and a standard-library resource wrapper was separately frozen before the sole scientific execution.

## What the conventional operation does

The procedure starts from the two observation classes. It repeatedly splits a block whenever two native states have different exact transition-mass vectors into the current blocks. The old full-terminal event stabilizes after three strict rounds at the six original levels. The changed subset stabilizes after six strict rounds at 24 blocks.

At stabilization, every pair of native states in a block has identical transition probabilities into each destination block. The resulting projected process is Markov for every initial law. Since observation is constant on each block, it has the same entire binary observation-history distribution as the native process. First hit, survival, first hit jointly with final membership, and exit/reentry are functions of that observation history. QUERY_SUFFICIENCY.md supplies the full induction and the standard coarseness argument.

The result is the coarsest **strongly lumpable refinement of the event observation**. It is not claimed to be the smallest possible representation for only the chosen initial law, only horizon64, or a restricted set of endpoint queries.

For exact propagation, both the native and refined kernels use a common integer denominator, with integer matrix-vector products. The native kernel denominator has126 bits. No comparison uses floating-point equality or repeated dense matrix powers. Floating-point values below are only readable diagnostics of saved exact fractions.

Returns are included through a four-phase path monitor: never hit; hit but never subsequently exited; exited after a hit but not yet reentered; reentered at least once. Every phase uses the actual full native or quotient kernel. The reentered phase continues evolving and still counts the event if the chain is outside A again at the final horizon. A backward full-kernel continuation calculation gives the first-hit/final-membership joint law. Post-hit motion is never made absorbing for these queries.

## Exact failures of the old representations

### Six levels cannot encode the changed observation

Vertices15 and17 are both at terminal level4, but only15 belongs to A. Thus membership in A is not a function of the six-level quotient. This alone does not establish that every statistic about A is inaccessible: the original q start and tree symmetry still permit a correct one-time marginal.

### Seven level-by-membership blocks are not strongly lumpable

Vertices7 and8 are both nonselected states at level3. Vertex7 has the two selected children15 and16, whereas vertex8 has no selected child. Their exact one-step subset probabilities are

    C(7,A) = 1853035221237377 / 12971141321962887
    C(8,A) = 2147483648 / 1853020188851841
    C(7,A) - C(8,A) = 1/7.

The global component is identical for these same-level parents; the local selected-child incidence causes the difference. Even a level representation augmented with the current observation therefore lacks enough information for a generic next-observation law.

### The failure affects the actual q-start history, not only arbitrary starts

For completeness, the protocol also froze the natural q-weighted average of rows in those seven blocks. It is a valid stochastic matrix, but it is not an exact representation of the native observation process.

Its first disagreement with the native first-hit distribution occurs at time2:

    native P(T_A=2)     = 0.00002414742951811212...
    averaged P(T_A=2)   = 0.00002414744106656169...
    exact difference   = -1048576 / 90797989253740209.

It also changes the joint probability of first hit at time0 and membership at time64. The exact difference is saved, with diagnostic value about2.3392529e-9.

Nevertheless, its one-time subset mass at64 is exactly correct. Without conditioning, the native q-start law remains uniform within levels. Conditioning on not having hit A, or on an earlier hit and exit, breaks the relevant uniformity. This separates a valid endpoint calculation from an invalid history representation.

## Exact query results

All65 first-hit probabilities, all65 first-hit/final-membership joint probabilities, survival and the explicit exit/reentry event agree as exact fractions between native32 and refined24. Their full laws are retained in EXACT_LAWS.json.

| Native event through horizon64 | Probability, diagnostic |
|---|---:|
| Never hits A | 0.9856243500493369 |
| Hits A at least once | 0.014375649950663075 |
| Hits, subsequently exits, then reenters | 0.00000899765022485348 |
| Is in A at time64 | 0.012779836931944283 |

The source's full-terminal mass at64 is exactly four times the last value, as expected for four selected leaves out of16 under the unconditioned symmetric start. The invalid seven-block average overstates ever-hit probability by about5.9676034e-6 and understates exit/reentry probability by about5.9651245e-6. These are errors in a changed query, not errors in Pro3's original level theorem.

## Costs and limits

One scientific worker ran successfully. Its full process cost, including preparation, checks and output, was **0.511385 CPU seconds**, about0.51556 wall seconds, with **19,460 KiB** peak RSS (about19.00 MiB). The worker had an80-second soft/85-second hard CPU limit and512 MiB address-space limit. No resource limit was reached.

| Stage | Observed CPU seconds |
|---|---:|
| Native source preparation and validation | 0.010227 |
| Ordinary refinement for the old terminal event | 0.004002 |
| Ordinary refinement for the changed subset | 0.007978 |
| Full native exact history queries | 0.207982 |
| Refined exact history queries | 0.127981 |
| Invalid seven-block average history queries | 0.035986 |

The very short quotient-build and certificate-write stages reported zero CPU at the process clock's resolution, with nonzero wall duration. These are descriptive clocks from one small run, not evidence for a meaningful speedup, a timing distribution or a cost advantage over an independent strong ordinary method. Development, model inference and analytical review costs are unmetered. The conventional exact refinement procedure is itself the strong ordinary method.

No owner scientific suite, larger inadmissible fixture, altered parameter, alternate event or outcome-tuned rerun was executed. This check does not change Pro3's sharp asymptotic question.

## Consequence for the meta hypothesis

The generic idea “retain exactly what admitted future observations can distinguish” has a valid executable receiving use in a second actual model. Its success depends on rederiving the appropriate interface: retaining native history semantics, checking lumpability, and refining when the observation changes.

That is weaker than a transferable invention capability. Here the principal supplied the event, the native model is tiny, exact transitions are available, and the ordinary algorithm already solves the problem. What the run usefully falsifies is the stronger shortcut that an existing scientifically valid compression can be carried unchanged into a changed question because endpoint statistics still look correct.

No donor-derived quotient or learned transformer was imported from the port experiment. This investigator implemented conventional refinement afresh using the same observation-equivalence principle. The result establishes applicability and scope of that principle on the actual second model; it does not isolate a causal benefit from acquiring the first model's representation or code.

## Independent review

A separate investigator completed a read-only audit of the native adapter, sufficiency proof, refinement and return-query code, saved rational laws, fixture identity, and eleven file hashes. The scoped verdict is PASS, with no concrete gap found. This was independent static review and checking of saved certificates, not an independent rerun of the native model, refinement, or owner's admission suite. Full scope and limitations are recorded in INDEPENDENT_AUDIT.md.

## Evidence and identities

- PROTOCOL.json: 788c848aa69c6f5402dfd51ad7cf1b31baee420a23043b59fbddba11bc9fdd7f.
- Worker markov_query.py: d196b360c6942f613f99dfdb3d581b9ac5cf3a22ce34342d84cb8009a51de21a.
- QUERY_SUFFICIENCY.md: ca3cb1c6aae41f7149390fe0b735d61dc1c52a1a996b529880e62a73ea404c98.
- Initial FREEZE.json: 71a201892038b22d0bbb485919ba9b56b718b840640b328c8104384f813cab6d.
- EXACT_LAWS.json: dcfcff6d1a697a59be80d635ca7a39249f0fc854aad9fd909abfea1a89e4eeff.
- CERTIFICATE.json: b2321e361199627e264916b0f993d76fbf5e813667a781cbcd560a9df2bb8b82.
- RESULT.json contains all stage costs,320 focused checks and diagnostic summaries; PROCESS_RESOURCE.json contains whole-worker resources.
- LAUNCH_FAILURE.json, LAUNCH_FREEZE.json and launch_once.py preserve the failed external timer launch and the subsequent standard-library wrapper.

Scientific source, relative to the Cycle10 input directory: pro3/Astra_Amplification_Cycle9_PRO3_20261022/code/exact_checks.py:125–243 for native construction and lumping;243–340 for the original different marked event, full law and admission; evidence/exact/EXACT_INPUTS.json and expansion_native32.json for the unchanged admitted fixture. Their exact hashes are retained in FREEZE.json.
