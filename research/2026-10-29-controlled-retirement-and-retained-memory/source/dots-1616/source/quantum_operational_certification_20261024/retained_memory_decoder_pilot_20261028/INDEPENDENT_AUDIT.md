# Independent audit: retained-memory decoder numerical pilot

28 October 2026. Reviewer: `producer-workspace/review_prequential_memory_recovery`.

**PASS as a reproducible floating numerical diagnostic, with a substantive practical negative result. NOT an execution of the exact finite theorem, terminal payload service, or hardware.** The final author state is bound by `DELIVERY_MANIFEST.json`, SHA-256 `bf2a83b5f287c48cbfbe7be30a553a0dd11fcf6c7952ed61ef37681641bfb940`; all 180 entries were independently verified. This review acquired **zero new source samples** and did not edit author files.

## Result and what it establishes

Four independently seeded longest trajectories per primary method give these N512 empirical mean conditional Bell losses:

| Method | Prequential decoder | Its own visited-state oracle | Fixed identity on those states |
|---|---:|---:|---:|
| Theorem-step log-det bandit | 0.7496593905 | 0.1019911310 | 0.3678686244 |
| Fresh ordinary Pauli/Procrustes batch | 0.1345041263 | 0.1016113169 | 0.3676412459 |

The depolarizing decoder is exactly 0.75. The bandit has not meaningfully learned at these budgets. Its center loss is 0.7496639599, so the failure is not an artifact of scoring its sampled exploration instead of its center. The ordinary method is substantially more successful **on this favorable common-unitary fixture**, using only Pauli measurements during acquisition. Different probe instruments produce different memory occupations; these are not paired same-trajectory policy advantages or a universal algorithm ranking. Four seed families do not establish expected-risk confidence bounds.

The bandit uses the manuscript's actual conservative step `eta=1/9216`, not a hidden tuned rate. Its centers remain near the replacement center, with final mean coordinate norm about 0.00660 and observed Hessian condition number at most 1.133. Every nonzero update takes two floating Newton steps and passes the logged guards. Thus the poor short-budget learning is not explained by solver failure, loss normalization, a frozen memory, or a sign/transpose error. At the chosen parameters the theorem horizon is 8,388,608, exactly 16,384 times N512. This pilot neither falsifies the theorem nor supports practical performance at its horizon.

## Physical conventions and retained-memory instrument

The normalized output-first Choi convention, Kraus reshaping and decoder action are consistent, including Y/complex entries and nonunital channels. `compile_decoder` factors a 4-by-4 Choi matrix into four qubit Kraus operators, stacks an 8-by-2 Stinespring isometry, and completes an 8-by-8 unitary. That is a **dense floating matrix construction**, not elementary gate compilation. The simulated receiver applies the Kraus channel, which is equivalent to that dilation within the recorded numerical residuals.

The plant has a qubit physical output and a coherent retained qubit memory. Its Kraus maps satisfy

`GI=GX+GZ+H_map`, `GY=0`, and `2 KX†KX+2 KZ†KZ+H†H=I`.

This supplies explicit CP-order witnesses. It does not infer them from data. The source's complete map is the fixed joint CP map `sum_alpha Ad_(U P_alpha) tensor G_alpha`. At a probe outcome, the code sums **all** quantum memory branches weighted by the actual receiver outcome probabilities, then normalizes. There is no sampled microscopic branch label, hidden classical-state reset or substitution of the unconditioned memory.

The reviewer reconstructed the complete 4-by-4 joint source state, actual decoder and projective outcome instrument at **every one of 7,680 recorded calls**, independently of the simulator implementation. Across all calls:

- Born-probability discrepancy: at most `3.34e-16`.
- Conditional post-memory discrepancy: at most `5.58e-16`.
- Nonselective-memory discrepancy: at most `1.19e-15`.
- Between-call memory continuity discrepancy: at most `8.79e-17`.
- Reconstructed branch masses match stored masses exactly.
- Played Choi minimum eigenvalue is at least `0.1946499979`; TP residual is at most `7.86e-17`.

The tiny negative minimum eigenvalue of an initial *pure* memory (`-1.67e-16`) is roundoff, not a materially negative density operator; all recorded post-memory minimum eigenvalues exceed 0.01587. These are numerical checks, not interval/exact PSD certificates.

`RetainedSource.probe` receives decoder/input/measurement arguments because it bundles source and receiver Born sampling. This is not a software security boundary against a malicious source. In the implemented equations those arguments affect only the specified quantum input and post-source instrument; the fixed joint source CP map does not branch on a role or decoder label. The independent joint reconstruction verifies that mathematical interpretation. Physical role sealing, routing/timing isolation and a hostile-device privacy test were not implemented.

## Record-only learning and reproducibility

The bandit policy consumes only private `(i,z)` and the observed integer bit `y`; its module imports no simulator, private state, U, branch probabilities or posthoc score. The ordinary policy consumes only `(j,s,m,b)` and its own running matrix. Public diagnostic fields are inspected for audit, not fed to updates. Scoring is explicitly privileged and posthoc.

The independent checker replayed all 24 trajectories in a separate temporary directory containing only the four public policy/replay/math modules and public records: **no simulator module, metadata or private source audit was present**. All 2,560 bandit post-update coordinate vectors replay exactly; all 5,120 ordinary saved pre-update SVD singular-value vectors match exactly. The same source-disabled replay was repeated during the full-record audit, with zero source calls.

The original ordinary `max_theta_replay_error=0` was vacuous because the method has no saved theta and no comparison was made. The final author replay correctly returns null/not-applicable for that field and reports a real saved-SVD comparison. This verifies the recorded public SVD diagnostics, not an absent saved unitary. Independently reconstructed raw totals and resulting pre-call decoders also reproduce the privileged scores below. The unchanged bandit state replay is a genuine comparison against saved coordinates.

## Scoring and the comparator

The independent audit recomputed Bell fidelity from Kraus traces,

`F_e = sum_alpha p_alpha sum_b |Tr(K_b U P_alpha)|^2 / 4`,

rather than relying on `score.py`'s Choi-target inner products. Every played/center/oracle/identity/depolarizing score and final retrospective score agrees; the largest per-call Bell-score difference is `1.12e-15`. The known-U inverse attains loss `1-p_I` on the recorded conditional memory, as required by the supplied CP-dominance family. No learning update sees that oracle.

All fixed baselines are evaluated on the **actually visited** states of the corresponding run. They are not assigned counterfactual histories that would arise if they had controlled earlier acquisition. The score of the final decoder on its past visited states is retrospective fitting evaluation, not future risk. Conditional Bell scores are analytic privileged evaluations of the simulated channel; they are not direct observations of a Bell experiment or an executed unknown payload.

For the ordinary method, historical raw keys named `played_policy_bell_loss` denote the **pre-call available hypothetical terminal decoder**, not a decoder applied to that calibration output. Ordinary acquisition directly measures a random physical Pauli. The final report/analysis now names and explains this distinction. The bandit decoder, by contrast, actually is applied on every probe.

The ordinary estimator `9 s b e_m e_j^T` is conditionally unbiased for the current Bloch transfer. Procrustes is valid on this fixture because its stronger explicit decomposition gives

`kappa_X=2p_X+h`, `kappa_Y=h`, `kappa_Z=2p_Z+h`, with `h=Tr(H sigma H†)>=0.7118056`.

Thus every conditional transfer, and their average, has the same proper polar rotation U. **Pairwise identity/CP dominance alone does not imply positive Bloch contractions**; for example Pauli probabilities `(0.34,0,0.33,0.33)` satisfy identity dominance but have a negative X contraction. The author corrected that overbroad report wording without changing the numerical comparator. This ordinary baseline is consequently a legitimate structure-exploiting conventional comparator here, not a universal arbitrary-CPTP learner or a result for larger output gauges.

## Finite-control and statistical limitations

The binary64 Cholesky/inverse-dual/Newton calculations implement the intended *floating* formulas and use only actual return bits. Their logged residuals are far below the floating target, and none of the finite iteration/backtracking caps fail. Nevertheless they do not execute the theorem's rational grid, exact PSD/residual certificates, certified weak convex solver or whole-process implementation allowance. A dense Stinespring matrix does not supply gate synthesis, routing, reset quality, padded timing, trusted payload storage or physical noise accounting. No terminal payload or reference-entangled service was executed.

The reported conservative precision table checks: with these parameters, the coordinate-grid fractional-bit requirement is `2N+42` and objective-tolerance bits are `4N+73`; hence 1,066 and 2,121 bits at N512. These are the manuscript's conservative global-floor prescriptions, not observed conditioning or an intrinsic precision lower bound. Binary64 success near the center cannot be relabeled execution of those prescribed exact controls.

The comparison has one fixed U/noise fixture, coherent memory, and four random seed families per primary method. It does not test a broad source distribution, unknown spatial localization, many-body output, selector discovery or generic unflagged recovery. The ordinary algorithm uses the favorable common-unitary structure; both methods may be available to the equally informed conventional learner. No practical quantum advantage is supported.

## Complete ledger and preservation

- Original acquisition: 16 runs and 5,120 simulated complete source calls.
- Additional independently seeded ordinary comparator: 8 runs and 2,560 calls.
- Total: **24 runs, 7,680 recorded/executed simulated calls**, zero recorded acquisition failures, zero terminal payload calls.
- Primary independent evidence: four longest bandit and four longest fresh ordinary trajectories. N128 repeats each corresponding N512 prefix; those are not additional independent seed families. The original cross-algorithm source uniforms are exactly common-random-number coupled and retained as exploratory evidence.
- Every stored sampler draw, call count and per-run private-bit ledger was reconciled. All probes are counted; replay/scoring/audit add no source calls.

All 180 final delivery bindings were verified. Against the two historical manifests, 160 bindings remain unchanged and eight changed report/replay predecessors are preserved byte-for-byte with their original hashes. No raw acquisition, learner, source, Choi math, comparator or score implementation was changed to obtain the final interpretation. The preserved development JSON-serialization failure was not an acquisition failure or a discarded source run.

## Receipt and stopping boundary

`independent_pilot_review_check.py` and `independent_pilot_review_check_final.json` contain the independent full-record checks and data hashes; `independent_historical_preservation_check.json` records the predecessor verification. No unresolved numerical or record-boundary defect remains in the corrected final deliverable. Accept the **practical negative diagnostic** at precisely this scope, not a performance theorem or completion of the exact algorithm's implementation obligations. The current actionable gap is learning/control usefulness at realistic budgets, not an apparent success hidden by a scoring bug.
