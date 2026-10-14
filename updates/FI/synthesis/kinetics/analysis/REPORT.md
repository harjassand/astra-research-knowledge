# Reverse-relaxation kinetics packet audit

Audit date: 14 October 2026. Scope: read-only review of the acquired kinetics packet and current capital routes, plus bounded replays and new exact witnesses saved only under `work/FI-kinetics`.

## Result

The packet’s conditional result survives a separate exact recertification: on the canonical synthetic fixtures, a freshly constructed exact local supersolution validates each stored scalar `alpha_lower`, and the stored tensor response then rebuilds each original rational endpoint exactly when paired with that stored scalar. The original unmodified `audit_reverse.py` replay still fails its exact endpoint-equality assertion. That failure and the precise upper-endpoint differences are preserved as first-class evidence; the separate recertification does not turn the original replay into a pass.

The packet supports a useful but conditional acquisition claim: from 172 exact energy readings and 2,772 exact downhill-clock readings at `n=18`, it reconstructs the model within the declared pairwise-energy, reversible heat-bath, positive degree-at-most-two attempt-law class. The class is assumed rather than inferred from those observations. A new exact four-coordinate countermodel shows why: one positive degree-three mobility term leaves every degree-two probe unchanged while changing the uniform-source mean lifetime by about 7.11%.

An independently assembled full-state comparator, driven by the same acquired B transcript, was solved in six preconditioned-CG iterations and recertified by exact rational arithmetic over all 262,144 states. Its interval ratio is `1.0007217375652144`, compared with `1.0188947563570727` for the fresh exact-alpha tensor certificate. The full-state method is both tighter and, in the packet’s original matched end-to-end run, faster: 3.263 s versus 6.577 s. The new local Mac run is not a fresh end-to-end tensor-vs-full benchmark because the tensor proposal was loaded from its saved witness; its 2.162 s fresh tensor recertification omits proposal generation.

All of these are finite synthetic computational results. No physical rate, molecular trajectory, equilibrium sample, experimental preparation cost, or general molecular capability was established.

## Endpoint and alpha audit

The original audit exits with code 1 at the exact endpoint comparison in the unchanged `audit_reverse.py`, through its replay helper. Exact lower endpoints match in all three cases. Regenerated local-SciPy upper endpoints differ from the stored endpoints as follows (stored minus regenerated):

| Saved witness | Stored ratio | Regenerated ratio | Stored upper minus regenerated upper |
|---|---:|---:|---:|
| A | 1.000018763181896 | 1.000018763180078 | +0.00027058704623416903 |
| B | 1.0000000545486118 | 1.0000000545486174 | −0.0000013177458936032306 |
| Matched tensor | 1.0188947609202876 | 1.0188947629027998 | −0.45644596207365556 |

The exact rational differences, the original traceback, and the unchanged source/replay script hashes are in `audit_reverse_failure.json` and `audit_reverse_endpoint_differences.json`. The numerical upper differences arise because the source `alpha_bound` regenerates a local solve and a 46-bit dyadic proposal; the proposal changes across the source Linux/Python 3.13.5 environment and this local macOS/Python 3.13.2 environment.

The saved `.npz` files contain only the three tensor-train response arrays for each witness. Their array members are plain `float64` and have no object dtype. The JSON records `alpha_lower`, a residual scalar, and a maximum-trial scalar, but not the local vector `u` used to establish that alpha. Consequently the original local alpha witness cannot be recertified as the same vector. The independent checker instead solves the acquired local 64-state matrix at high precision, rounds to a 112-bit dyadic vector, and exactly checks positivity, the infinity residual, and nonpositive off-diagonals. It verifies `alpha_old <= alpha_new` exactly, then contracts the saved response tensor and rebuilds the stored upper using `alpha_old`. This validates the stored scalar and its endpoint for the retained response; it does not recover or certify the missing historical `u` vector.

Fresh exact-alpha intervals are:

| Case | Lower | Upper | Ratio |
|---|---:|---:|---:|
| A | 148,838,921.68597248 | 148,841,714.37678564 | 1.000018763175529 |
| B | 230,236,128.12863976 | 230,236,140.68769790 | 1.0000000545485985 |
| Matched tensor | 230,236,127.69668200 | 234,586,383.23410672 | 1.0188947563570727 |

The exact rational endpoint strings and exact 112-bit local witnesses are in `fresh_replay_results.json`. Under the refreshed intervals, `B_lower/A_upper = 1.5468521650174498`. This is a model-conditional separation for the acquired fixture: A and B share equilibrium weights and all-zero-context rates, while their context-dependent mobility differs.

## Full-state matched comparator and resources

The comparator was reconstructed from `reverse_matched_full_transcript.json`; its weights and reverse rates exactly match the B transcript. It uses the acquired partition and local preconditioner, but constructs the full state arrays intentionally. Its six-iteration float solve was followed by a new integer-scaled exact contraction over the complete state space. The exact checker forms rational transition rates, source weights, normalization, `L`, and residual square; it does not use private fixture truth or a saved full-state response file.

The fresh exact interval is `[230236128.11812487, 230402298.18065727]` (exact rationals in the result JSON), with ratio `1.0007217375652144`. The fresh local run took 4.551 s total: 0.918 s transcript/model reconstruction, 0.083 s state setup, 0.547 s PCG and directed checks, and 3.000 s exact rational certificate. It represented all 262,144 states, used a 2,097,152-byte integer response vector, and had 321,355,776-byte process peak RSS. The retained transcript is 149,244 bytes. Peak RSS includes Python, NumPy, exact integer temporaries, and all solver arrays; it is not an estimate of the response vector alone.

For context, the packet reports its original matched full-state end-to-end run at 3.2627 s and the matched tensor run at 6.5769 s. The tensor witness file is 71,389 bytes and has 9,088 stored coefficients; it avoided constructing a 262,144-entry response vector in that run. The source record itself says full state was faster. The storage advantage is therefore a representation result, not a runtime win. Comparisons of the new local timings are not fair end-to-end algorithm comparisons because the local tensor path only recertifies a precomputed proposal.

## Acquisition boundary and exact countermodel

Energy recovery uses 172 pairwise weight readings. The kinetic scan queries all local contexts with at most two other coordinates excited, 2,772 readings at `n=18`. Reverse relaxation removes the energy suppression in the two-state flip law but still presumes access to the original local clock after preparing the less probable state. Context preparation, resets, sampling variance, measurement calibration, and physical access to the microscopic move remain outside the synthetic reading count.

The new four-coordinate exact countermodel has `W(x)=1`, target hazard `k(x)=x_0`, and base attempts `a_i(y)=1`. In the hidden law, only `a_0` changes, to `1−(99/100)y_1 y_2 y_3`; it remains strictly positive. Every empty, singleton, and pair-context clock query returns exactly `1/2` under both laws, and the energy transcript is identical. Exact solution of the 16-state killed system gives uniform-source means 3 and `5500371/1711720`, ratio `1833457/1711720 ≈ 1.07111969247`. The exact response vectors satisfy `K u=1` and are positive. For this particular countermodel, one additional downhill-clock query at context `y_1=y_2=y_3=1` separates the laws. For unrestricted higher-order support, a degree bound or sufficient context coverage remains necessary.

## Strong-coupling and rank evidence

The packet’s dense `n=18` preflight has 153 interaction edges. The implemented partition/compiler reduces it to eighteen singleton blocks, at least 108 cross edges, and an enormous product comparison factor (`2094022385695512357790224343235599197987723902362520427429888`). It reports `compiled: false` because explicit cross-term expansion and the comparison constant are prohibitive. This is a compiler/access-structure failure, not a lower bound against other methods.

The retained earlier rank sweep is also nonuniform: rank 2 ends at ratio 1.1397 after eight iterations and misses the 5% target; rank 4 reaches 1.02323 with 1,536 coefficients, while rank 12 reaches 1.02305 with 9,920 coefficients (about 6.46 times as many). This is evidence for a fixture-specific rank/accuracy tradeoff, not a low-rank guarantee. Separately, the `strong_repair` fixture does reach ratio 1.00000672 after 16 iterations at rank 16, 18,432 coefficients, and 16.86 s end-to-end; it does not resolve the dense preflight obstruction.

## Current capital fit

The current N801, N798, N793, and N795 dossiers and their linked proof routes were read before applying their historical claims. Their status remains `source_derived_unreviewed`; external correctness, novelty, and physical capability are `UNKNOWN`.

- N801’s all-source complement result is conditioned on its supplied homogeneous ferromagnetic-cycle and Glauber class. Its open gate still calls for physically obtainable microscopic clocks and coverage of nonintegrable hidden traps. The present degree-two local attempt assumption does not discharge that gate.
- N798 keeps global source/form envelopes, full-source load coverage, and normalization separate from a compact representation. Its open gate requires acquired envelopes or an independently source-complete certificate and matched costs against strong solvers. The full-state result here is the strongest observed comparator and is faster in the packet’s own run.
- N793’s static-data hidden-mobility obstruction remains relevant: exact equilibrium weights do not reveal clocks. The reverse-rate protocol supplies a new conditional microscopic oracle in the synthetic model; preparation and physical access costs are not paid, and no nontranslated molecular mobility/tail certificate is produced.
- N795 assumes a specified finite graph, known masses, possible moves, and independent conductance intervals. Its exact completion query rules do not imply that unknown higher-order clock supports are cheap to find. The degree-three countermodel above illustrates the information gap.

The N795/N793 direct-rate and hidden-mobility results are compatible as scoped statements. Treating the acquired degree-two law as a physically justified global description would require an additional model-validation premise and acquisition-cost evidence.

## Prior art and access depth

The main computational overlap is [Masetti and Robol, *Tensor methods for the computation of MTTA in large systems of loosely interconnected components* (2019)](https://arxiv.org/html/1907.02449v1). Its full 570-line arXiv HTML was reviewed through the CTMC/TT formulation, MTTA method, convergence discussion, case study, and experimental section. It already covers local/synchronization splitting and tensor-train solution of mean absorption times. The current packet therefore does not establish novelty for tensor response solving, local decomposition, or CG/residual identities. The potential distinction is the conditional reverse-relaxation acquisition plus a source-complete rational certificate from that acquired law; historical priority is unresolved.

Three primary molecular-method comparators were also inspected at full HTML depth: [Verma, Benner, and Nüske (2026)](https://arxiv.org/html/2609.06446) (481 lines; tensor generator learning from MD trajectories, reaction coordinates, and state-dependent diffusion), [Ryu et al. (2025)](https://arxiv.org/html/2504.21663v3) (461 lines; weighted-ensemble trajectory management and MFPT estimates on Trp-cage and NTL9 systems), and [Swinburne and Perez (2018)](https://arxiv.org/html/1803.05273v1) (388 lines; accelerated atomistic trajectory exploration, transition matrices, and residence-time uncertainty). They use trajectory or atomistic simulation information rather than the packet’s exact local downhill-rate oracle, so no one-to-one numerical comparison was made. They remain relevant stronger physical baselines if a laboratory or molecular claim is attempted. This was a focused source audit, not an exhaustive literature search; novelty stays UNKNOWN.

Three additional kinetic-inference and MFPT records narrow any broad acquisition novelty claim. [Achitouv, Chavalarias, and Lahoche (2026)](https://arxiv.org/html/2609.23690v1) was reviewed at full 400-line HTML depth: it fits heat-bath kinetic-Ising transition laws, including persistence variants, to temporal social-network data and compares predictive loss and forward simulations. It is empirical discrete-time opinion dynamics, not molecular reversible CTMC/MFPT certification, but establishes that data-driven kinetic-law inference is an existing general activity. [Zeng et al. (2010)](https://arxiv.org/abs/1011.6216) and [Wei, Dudas, and Rosta (2024)](https://arxiv.org/abs/2406.08964) were checked only at abstract/metadata depth because full HTML retrieval was unavailable. The former reports network inference for asynchronously updated kinetic Ising models; the latter uses MFPT relations to optimize enhanced sampling, with NaCl and Ras applications. These two are leads rather than completed method comparisons. Taken together with the tensor-CTMC and molecular trajectory papers above, they leave priority unresolved and reinforce that only the narrowly specified reverse-clock acquisition plus exact conditional certificate is even a candidate distinction; it has not been established as novel.

## Reproducibility and files

The exact source tree and user-selected pasted source were snapshotted byte-for-byte. All 114 NPZ members were inspected by reading only NumPy headers before any array load; no member has object dtype. During replay, the source `audit_reverse.py` remained unchanged. Only the replica’s loader in `audit.py` was changed to pass `allow_pickle=False`; replay writes stayed inside `work/FI-kinetics/replica`. The source’s hard-coded `/mnt/data` entry point in `solve.py` was not run.

The local replay environment was Python 3.13.2, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0, and mpmath 1.3.0, with one BLAS/OpenMP thread. The packet records a different Python patch release and Linux environment, so exact endpoint strings and timings are not expected to match bit-for-bit.

Primary artifacts:

- `audit_reverse_failure.json` — unchanged original FAIL and traceback.
- `audit_reverse_endpoint_differences.json` — exact old-versus-regenerated endpoint deltas.
- `fresh_replay_results.json` — exact-alpha tensor recertifications and fresh full-state rational comparison.
- `kinetics_audit.py` — independent replay and exact arithmetic checker.
- `degree3_countermodel.py` and `degree3_countermodel_results.json` — exact hidden-clock countermodel and response witnesses.
- `source_integrity.json` and `source_manifest.json` — source equality and input hashes.
- `read_ledger.json` and `replay_receipts.json` — source paths, hashes, commands, and run outcomes.
- `proof_alpha_and_countermodel.md` — derivations behind the fresh alpha and cubic countermodel.
- `owned_manifest.json` — frozen byte/hash inventory of this owned work package, excluding the virtual environment and generated bytecode.
