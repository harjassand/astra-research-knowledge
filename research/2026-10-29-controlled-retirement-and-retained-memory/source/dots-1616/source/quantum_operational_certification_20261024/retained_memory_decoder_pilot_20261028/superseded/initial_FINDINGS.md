# Retained-memory decoder pilot: a practical negative result

28 October 2026 · Astra science only · **Floating numerical diagnostic, not the exact certified finite algorithm or hardware.**

## Result first

At `d=2`, the manuscript’s conservative log-det bandit step is executable cheaply in floating point, but does **not meaningfully learn in 128 or 512 calls**. An ordinary, record-only Pauli/Procrustes comparator learns a substantially better decoder on this deliberately favorable common-unitary qubit fixture, with much less per-probe quantum control. This is not a universal method comparison: each acquisition instrument creates its **own actual memory occupation**, and the ordinary construction uses the fixture’s common-unitary structure.

Means over four seeds per row; entries are empirical means of conditional Bell losses along each run’s own actual visited states, **not exact expected occupation risks or confidence bounds**:

| Acquisition / prequential decoder | Calls per run | Learned played policy | Known-U oracle on same visited states | Fixed identity on same visited states | Acquisition wall time |
|---|---:|---:|---:|---:|---:|
| Log-det bandit, theorem η | 128 | 0.75034 | 0.10761 | 0.37129 | 0.163 s |
| Ordinary Pauli / Procrustes | 128 | 0.20157 | 0.10697 | 0.37090 | 0.053 s |
| Log-det bandit, theorem η | 512 | 0.74966 | 0.10199 | 0.36787 | 0.575 s |
| Ordinary Pauli / Procrustes | 512 | 0.13450 | 0.10161 | 0.36764 | 0.217 s |

The fixed completely depolarizing decoder has loss exactly **0.75** on every row. The bandit center policy at N512 has mean loss 0.749664; the sampled played policy has 0.749659. Small finite-sample differences between those are expected. No claim that a particular bandit seed improved is supported: one N512 final decoder’s retrospective loss is 0.75150.

The ordinary N512 policy losses range 0.12108–0.15125 across its four seeds. Its final decoder’s mean retrospective loss on its already visited states is 0.10822, versus 0.74914 for the bandit. **Those retrospective final-decoder scores do not certify future calls or a train-then-use deployment.** The prequential table is the relevant comparison.

## What was actually sampled and preserved

- Known physical patch: one qubit (`d=2`); retained source memory: one coherent qubit, never reset within a run.
- Ordinary six-state inputs; the bandit gets only its actual binary return outcome, its own coordinates, and private exploration coins. No source unitary, branch probability, conditional memory state, expected loss, or oracle score is passed to an update.
- Every bandit probe applies the **sampled played decoder**, not the center. A floating 4×4 normalized Choi matrix is converted to four Kraus operators and an 8×8 Stinespring unitary matrix before the call. The simulator applies the Kraus channel and the ordinary return measurement.
- The ordinary comparator has separate actual random input/output-Pauli records and updates only from `(j,s,m,b)`.
- **7,680 simulated complete source calls in 24 trajectories; zero acquisition failures.** The original batch has 5,120 calls. A further 2,560 ordinary-comparator calls use independently offset seeds for the primary table.
- The first batch used separate process instances with common numerical seeds across algorithms. Those coupled runs remain untouched in `runs/` as exploratory evidence, but are not used as the primary ordinary comparison. Primary bandit seeds are 17,31,47,73; primary ordinary seeds are 10017,10031,10047,10073.
- Primary independent evidence is **eight independently seeded longest trajectories: four bandit and four ordinary**, plus eight shorter prefix reruns. Another eight original shared-randomness ordinary runs are exploratory.
- Within an algorithm, N128 and N512 reuse the same four seeds: the shorter records are deterministic prefix reruns, **not four additional independent seed families**. All calls were nevertheless actually executed and counted.
- The per-run files contain public records, separate private source audits, all diagnostics, explicit empty-or-populated failure lists, metadata and post-hoc scores. No failed or unfavorable run was erased.
- No terminal unknown payload was inserted. This is the hypothetical all-probe experiment used by the theorem; post-hoc Bell scoring is analytic evaluation, not an extra sampled experiment. There were no source calls in replay, scoring, or tests.

## A genuine quantum retained-memory source

Set memory effects

`A = .045 (I + .65 Z)`, `B = .055 (I + .60 X)`.

Use `KX = Rz(.63) sqrt(A)`, `KZ = Rx(.83) sqrt(B)`, and `H = sqrt(I − 2A − 2B)`. Define

- `GX(σ) = KX σ KX†`, `GZ(σ) = KZ σ KZ†`, `GY = 0`;
- `GI(σ) = GX(σ) + GZ(σ) + H σ H†`.

The complete source is `sum_α Ad_(U Pα) ⊗ Gα`, with fixed unknown `U = exp[−i 1.17 (n·σ)/2]`, `n ∝ (.31, −.72, .62)`. It is not changed or fitted to outcomes. The initial pure memory vector is `(sqrt(.63), exp(.47i) sqrt(.37))`.

Trace preservation follows from `2KX†KX + 2KZ†KZ + H†H = I`; measured floating residual is 4.82e−16. `I−2A−2B` has minimum eigenvalue 0.71181. CP-order dominance has explicit witnesses `GI−GX = GZ + H_map`, `GI−GZ = GX + H_map`, `GI−GY = GI`. These are sums of CP maps, not dominance inferred from a finite sample. The effect commutator has Frobenius norm 0.00273014, so the two effects do not commute.

At an actual return outcome `y`, the retained state updates to

`σ′ = [sum_α Pr(y | α, input, actual decoder) Gα(σ)] / Pr(y)`.

No microscopic branch label is sampled, exposed, or used to update the learner. This is a CP quantum instrument on the joint output-memory state. Direct 4×4 joint-state calculations agree with the compact update to <1.4e−16 at selected actual histories. The source preserves nonzero quantum coherence (maximum recorded off-diagonal magnitude about 0.46). Conditional versus unobserved next-memory trace distance averages 0.000989 for the N512 bandit and 0.017998 for the independently seeded ordinary comparator. Thus the actual outcomes do change the retained state, and the two occupations are not interchangeable.

## Why the ordinary comparator is legitimate here

For this common-U Pauli fixture, the conditional Bloch transfer is `M_t = R_U diag(κ_t)` with nonnegative diagonal entries under identity dominance. Fresh independent uniform input axis `j`, input sign `s`, output axis `m` and actual output sign `b` give the record-only unbiased estimator

`Mhat_t = 9 s b e_m e_j^T`.

The learner averages these records. At each pre-call time it computes a proper orthogonal Procrustes factor: if the empirical matrix is `L Σ V^T`, take `Rhat = L diag(1,1,det(L V^T)) V^T`, and decode by its inverse qubit unitary. The population polar factor of a strictly positive diagonal contraction times `R_U` is exactly `R_U`. The finite sample estimator is noisy; the code is not supplied U or the actual diagonal contractions.

This comparator is equally informed about the fixture family but is **not a proved substitute for the arbitrary-CPTP retained-memory theorem**, nor a claim for larger gauge outputs. Its probe instrument measures one physical Pauli directly; its terminal decoder is only a pre-call hypothetical choice until a terminal call is made. That different probe instrument is precisely why its visited memory law differs from the bandit’s.

## Measured iteration and control bill

For the primary N512 bandit runs, mean measured times are:

| Component | Seconds / 512 calls |
|---|---:|
| Choi Hessian, Cholesky whitening, action checks | 0.0639 |
| Floating Newton prox and residual checks | 0.1356 |
| Kraus + dense Stinespring matrix construction | 0.1336 |
| Source / measurement simulation | 0.1313 |
| Total including record serialization and bookkeeping | 0.5751 |

For ordinary acquisition, the 3×3 SVD/rotation decoder calculation costs 0.0908 s, record updates 0.00084 s, source simulation 0.1039 s, total 0.2170 s. These are single-process measurements with BLAS thread counts fixed to one, **not hardware latency or scalable performance estimates**.

The bandit constructs and applies 512 general CPTP probe decoders per N512 run, each with four Kraus operators and an 8×8 unitary matrix realization (one input/output qubit plus two reset ancilla qubits). The ordinary comparator uses 512 single-output-Pauli measurements and no general CPTP probe decoder. **Elementary gate decomposition, routing, finite gate-set synthesis, physical reset, runtime padding, payload idle storage, and physical noise were not implemented or timed.** A dense matrix is not a gate compilation result.

Every mismatch update took two Newton steps; matches skipped optimization. N512 runs used 454–538 Newton steps total, no backtracks, and no solver failures. Maximum stationarity residual across the bandit batch is 7.01e−13 against the requested floating residual target 4.2386e−7. Maximum locality quadratic form is 1.206e−5 (guard 1/4); minimum played-Choi eigenvalue is 0.19465; maximum Hessian condition number is 1.1324. Maximum played TP residual is 7.86e−17 and Stinespring-unitary residual 2.44e−15. The realized local second-moment bound ratio is 8/9, below one.

## The exact finite algorithm was not executed

The main runs use `gamma=1`, `epsilon=.25`, `eta=1/(64·12²) = 1/9216`; no tuned learning rate or plant-informed heuristic was substituted. At these parameters the manuscript’s horizon threshold is 7,077,888 and its least power-of-two cap is **8,388,608**, far beyond 512. The flat small-N result does not contradict that theorem.

The implementation uses binary64 Cholesky, inverses, Newton solves, eigenvalue checks and matrix completion. It does **not** return rational dyadic centers, compute exact rational inverse-dual whitening, verify rational PSD/residual certificates, execute the specified weak-convex optimization, or supply a whole-process operational error budget. Finite pseudorandom rejection sampling and floating Bernoulli simulation are diagnostic substitutes for ideal fair bits and exact quantum Born sampling. The logged floating guards are evidence of numerical behavior, not theorem certificates.

The manuscript’s *conservative prescribed worst-case* precision bill is illuminating:

| N | Learner lower bound μ | Coordinate-grid fractional bits sufficient under §6 prescription | Objective-tolerance fractional bits |
|---|---:|---:|---:|
| 128 | 2^−132 | 298 | 585 |
| 512 | 2^−516 | 1,066 | 2,121 |
| 8,388,608 | 2^−8,388,612 | 16,777,258 | 33,554,505 |

These numbers follow directly from equations (18)–(20), not observed ill-conditioning. The observed centers stay near the depolarizing interior. A more economical exact certified solver may exploit that slack; this pilot does not prove an intrinsic lower bound or impossibility. The executable floating solver plus these explicitly unimplemented exact-control requirements are the precise current implementation boundary.

## Verification, rejected interpretations, and files

`test_results.json` passes the nonunital Choi/Kraus convention, six-state/Bell identity, direct joint CP instrument, conditional bandit gradient enumeration, second-moment bound, ordinary estimator, population Procrustes recovery, and a source-disabled replay with private files physically absent. Maximum direct conditional-gradient enumeration residual is 4.03e−15; bandit replay matches every saved post-update coordinate exactly on this stack. Ordinary `replay.py` executes from public records but its `max_theta_replay_error=0` field is a placeholder (there is no saved theta for that method), **not a verification statistic**; see the independent audit for actual ordinary-record checks.

Rejected interpretations: no practical bandit advantage, no failure of the finite theorem, no inferred source CP promise, no resetting or classicalizing the retained memory, no counterfactual-oracle trajectory, no expected-risk confidence interval from four seeds, no fixed-final-decoder future guarantee, no exact rational or hardware execution, and no transfer of a terminal-channel claim to repeated payload service.

- `learner.py`: source-disabled log-det learner.
- `ordinary_comparator.py`: source-disabled conventional comparator.
- `simulator.py`: private retained quantum-memory plant.
- `quantum_math.py`: known decoder math; `pilot.py`: acquisition controller.
- `replay.py`, `score.py`, `analyze.py`, `test_pilot.py`: reproducibility and checks.
- `runs/`, `runs_independent_comparator/`: immutable raw and derived run evidence.
- `ANALYSIS.json`: primary aggregates, exact call ledger, source hashes, precision calculation.
- `FROZEN_IMPLEMENTATION_MANIFEST.json`: initial frozen implementation and 5,120-call batch.
- `development_failures.md`: preserved development error and tooling limit. The numeric tests first reached their JSON writer successfully but failed serializing a NumPy boolean; conversion was fixed, no acquisition was changed, and all tests reran.
- Independent reviewer files, when received, bind the final audited state separately.

## Governing sources

1. `../ordinary_prequential_small_loss_decoder_bandit_20261028.md`, SHA256 `6edb6a3af1118947c1a864113a24d77eef437386eafb7d8694a4aa651dc8d1dc`: positive-loss return bit; rational Pauli coordinates; whitening; estimator; log-det prox; source horizon; exact-control bill.
2. `../ordinary_prequential_terminal_memory_recovery_20261028.md`, SHA256 `20e59391aeab608e0fb76dbaee3fee6825d434991892a2c63fe5e57634316079`: retained-memory complete-port model, actual occupation comparator, terminal transfer, CP-order common oracle.

No external publication, upload, or communication was made.
