# U acquired precision from paid source observations — 24 October 2026

This completed learning unit reports one synthetic paid-observation chain under a specified linear-Gaussian operator interface. It learns a shared task subspace from paid source responses, certifies observed coverage and projector precision, and uses that certificate to allocate exposure for new noisy solution tasks at successively tighter tolerances. This is a bounded conditional mechanism—not a new PCA method, a physical-material model, a worker-allocation law, or an established practical advantage.

The [checkpoint](source/experience_chain/ACQUIRED_PRECISION_CHECKPOINT.txt) gives the source-reported result and boundary. The [paid-chain proof/report](source/experience_chain/luna_batched_mean/PAID_SOURCE_CHAIN.md), [new-task lower bound](source/experience_chain/NEW_TASK_PRECISION_LOWER_BOUND.txt), [conditional precision-investment theorem](source/experience_chain/PRECISION_INVESTMENT_THEOREM.txt), and [source manifest](source/experience_chain/luna_batched_mean/public_manifest.json) retain the governing statements and learner inputs.

## Interface and acquired geometry

The fixture supplies `b=e1`, `delta=1`, `sigma=0.15`, and a rank ceiling `r=3`. A hidden fixed rank-3 subspace `T` lies in `b`-perp. Each source and future task has a fresh unit vector `v` in `T` and a new operator

`A_v = I + (delta/2)(b+v)(b+v)^T`, with target `x_v=A_v^{-1}b`.

A paid input at `b` returns a full vector with independent per-coordinate Gaussian noise of variance `sigma^2/m`; its exposure cost is `m`. Each source exposure is `128`. The model class, fixed shared `T` promise, rank bound and direction distribution are supplied; the orientation of `T` and whether the paid sources cover it are learned. The proof requires source directions independent of the complete source-noise matrix, fresh target noise independent of source data, and each future `v` to remain in the same `T`. It does not establish adaptive-source martingale coverage or any off-class guarantee.

The learner uses the empirical source covariance `S_K=VV^T/K`, not a population-covariance approximation. At cumulative source checkpoints `K=32,64,128,256`, the observed coverage/precision certificate was `s=0.33492, 0.22703, 0.14810, 0.10139`. The coverage gate opened at `K=32`, but its precision was insufficient for the first requested tolerance `0.15`. The selected blocks used `K=64`, `128`, and `256` for 512 new operators each at tolerances `0.15`, `0.10`, and `0.06`. Old source observations remained charged at each upgrade.

For each new task, the source certificate bounds squared error by

`beta^2 s^2/4 + sigma^2 Q_r(alpha_t)/((1+delta)^2 m)`,

where `beta=delta/(1+delta)` and `Q_r(alpha)=r+2 sqrt(r log(1/alpha))+2 log(1/alpha)`. The policy first upgrades sources until `s <= epsilon/beta`, then buys the smallest integer target exposure meeting its bound. The source reports the valid union-bound allocation over all 12 source checkpoints and all target indices as `0.0390199211` (less than `0.04`); the realized checkpoint-alpha sum alone is only diagnostic and is not a stopping-valid bound.

## One executed synthetic chain and its comparator

For `n=64`, `r=3`, `delta=1`, and `sigma=0.15`, the run used 256 source queries and 1,536 target queries: 112,006 total exposure, 114,688 returned scalar coordinates and 1,792 distinct operators. The source report states that an evaluator counted 0 of 1,536 target outputs outside their requested tolerances. This is one seeded synthetic realization, not a repeated-trial success estimate or significance result. Its ordinary float64 gate calculations have no outward-rounded or machine-verified roundoff certificate.

The principal point-estimate comparator is standard rank-3 PCA. An independently computed SVD-PCA matched the proposed eigendecomposition-PCA estimates to floating-point precision (maximum absolute difference `4.7e-16`) on the same data and exposures. This is a point-estimate tie, not a refutation of the paid-source precision chain; it also does not establish an advantage over a competent retaining controller. A same-data Wiener/shrinkage control and an unpooled ablation are reported separately in the [source results](source/experience_chain/luna_batched_mean/PAID_SOURCE_CHAIN_RESULTS.json).

The [public manifest](source/experience_chain/luna_batched_mean/public_manifest.json), [public source observations](source/experience_chain/luna_batched_mean/public_source_observations.npz), and [public target observations](source/experience_chain/luna_batched_mean/public_target_observations.npz) define the learner-visible data. The [public-only replay program](source/experience_chain/replay_public_precision_chain.py) reads only those two archives; its source-reported output is retained at [public_precision_replay.json](source/experience_chain/public_precision_replay.json). Exact finite-check programs and their saved outputs are retained for the lower-bound and allocation identities, but this intake did not execute them.

The [interface-repair provenance](source/experience_chain/luna_batched_mean/INTERFACE_REPAIR_PROVENANCE.md) records that earlier learner-facing seed names and a pre-repair result were superseded. Private evaluator truth, evaluator seeds, pre-repair private results, the generator that writes those evaluator-only artifacts, and the broad snapshot receipt are not copied. The final source-results JSON is an evaluation report, not a learner input; raw private truth remains excluded.

## Separate lower bound and conditional allocation envelope

The noisy new-task lower bound allows arbitrary adaptive inputs, retained state and free postprocessing. For an allowed `q`-dimensional task-vector space with `q>=2`, error tolerance `epsilon` and per-output-coordinate Gaussian noise, it gives

`B >= sigma^2(q-1)(1-2alpha)^3 / [27(1-alpha)(1+delta)^2 epsilon^2]`,

in its stated local range, plus a separate confidence lower bound. The source explicitly excludes `q=1`, where the unit-vector task has only two signs and the continuous `1/epsilon^2` conclusion fails. This is a classical Assouad/Gaussian-testing specialization, not a new lower-bound method or source-acquisition optimality theorem.

The investment theorem is conditional on an additional retained-refinement contract `bias^2 <= A/E`. Under that premise it derives fixed-horizon optimum `(sqrt(A)+sqrt(T B))^2/epsilon^2` and an anytime policy at most twice the best offline exposure-envelope allocation. The actual uncurated source class does not itself provide a deterministic `A/E` envelope; the run uses observed certificates. The allocation theorem is therefore not a worker-allocation law or a competitiveness claim for the completed fixture.

## Status

Proofs, public data, and public replay/check outputs are preserved as supplied. The source reports independent internal audits of the Gaussian certificate, projector step and adaptive lower bound; those reviewer reports are not all included in this selection, and this intake did not repeat the reviews or run scientific code. Shared-subspace representation learning and standard PCA have established prior art; exact-composition novelty is `NOT_ESTABLISHED`. External usefulness, physical validation, and total practical advantage remain unestablished. The parallel in-progress finite-guide fracture and finite-width anion-control constructions are intentionally not included here; they remain in the local source snapshot for a later coherent intake.
