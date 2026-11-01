# A different application gate: reusable schedule design for lattice-field Monte Carlo

Conclusion: this is a scientifically consequential and algebraically honest candidate, unlike a fabricated hidden-state device. It nevertheless does NOT currently qualify as a demonstrated major enabling operation. The precise blockers are stationary source preparation, switched task dimension, the mismatch between finite-horizon absolute correlation error and long-run scientific precision, and absent same-access advantage. No experiments performed.

## 1. Why this is a serious downstream operation

Lattice-field simulations need reliable precision per unit of expensive compute. Critical slowing and topological freezing impede that objective. A possible reusable operation is: after paying for acquisition once at a fixed action/lattice/parameter setting, evaluate many adaptively proposed schedules of already implemented, individually reversible updates, then choose a schedule with better variance per compute. The update alphabet could contain different Metropolized trajectory lengths, masses/preconditioners or local update choices, PROVIDED each marginalized transition really preserves the same measure and is individually reversible. Acceptance decisions, solver tolerances and momentum refresh are part of a primitive, not omitted overhead.

This is not a proposal to recover every lattice configuration or reconstruct the Gibbs law. The hidden Hilbert vectors are functions on configuration space, so reading a sampled configuration does not expose a full hidden Hilbert vector. However ordinary methods naturally have configurations and other diagnostic observables: artificially withholding them would be a comparison restriction, not an application advantage. At minimum the strong comparator gets every scalar episode, word and retained observation used here.

A future change in lattice spacing, action, physical parameters or update definition changes the operators/source. No free cross-setting transfer follows.

## 2. Return access is physically earned, conditional on preparation

Let π be the fixed target distribution and T_a its reversible Markov operators on real L²(π). Take |f|≤1; for a mean-zero fluctuation task, its centering must be known by symmetry or independently estimated and charged. Finite-volume charge diagnostics can be bounded, but clipping changes the scientific observable; predictions for a clipped diagnostic are not automatically predictions for topological susceptibility.

Use the governing convention T_w=T_{a_l}…T_{a_1}. For u=(u_1,…,u_k), v=(v_1,…,v_l), start X_0 from π and execute the PHYSICAL chronological kernel list

u_1,…,u_k,v_l,…,v_1.

Then Z=f(X_0)f(X_{k+l}) is bounded and

E Z=<f,T_u† T_v f>_π=<T_u f,T_v f>_π.

The list is u then reverse(v), rather than the Schrödinger-channel chronology in the separate quantum note. This is just a convention distinction; explicit multiplication removes any ambiguity. No negative probabilities, state cloning or reverse random-number tape is needed. Every update is a genuine fresh randomized Markov step.

But the theorem requires each episode to be conditionally unbiased given previous adaptive history. Continuing a long stationary chain gives correlated endpoints and, conditional on the observed history, generally does NOT provide that contract. New PRNG seeds do not reset the physical/configuration state. Independent exact π resets would suffice, but are the expensive sampling problem in precisely the regime at issue. An exact sampler, a certified burn-in/mixing bound or a replacement dependent-data theorem must be paid for. An existing equilibrated configuration library is useful capital, not free conditional-unbiased access: reuse/adaptation introduces empirical-measure error and selection dependence that require analysis.

If a reset distribution is within TV distance δ of π, bounded-product return bias can be up to 2δ. This bias must fit the entry error budget α or be propagated in a changed acquisition proof. Error in a Markov step can add linearly with return length under ordinary telescoping bounds. Successful local fits do not certify global equilibrium or absent topological sectors.

Per shot charge stationary preparation/burn-in, all updates and rejected proposals, solver work, observable measurement (including smoothing if used), randomization/control/storage, and discarded attempts. Source calibration and burn-in can dominate the attractive reused model cost.

## 3. Exact downstream task, not a hand-wavy correlation objective

For a repeated schedule s with Markov operator P_s and cycle cost C(s), define γ_k(s)=<f,P_s^k f> for mean-zero f. With a stationary start, the N-cycle sample-mean variance is exactly

V_N(s)=[N γ_0+2 Σ_{k=1}^{N−1}(N−k) γ_k(s)]/N².

This holds for a nonreversible composition too. All γ_k are sequence returns; words require length up to (N−1)|s|. Therefore the goal-oriented theorem could evaluate V_N for adaptively proposed schedules. If each γ_k has absolute error ε, the weighted propagated error is at most ε (including γ_0). This sounds useful until one notes V_N is usually of order 1/N: relative precision η then typically requires ε of order η/N, while the horizon scales with N. It is not a fixed-accuracy short-horizon task.

For asymptotic precision per work the objective is C(s)[γ_0+2Σ_{k≥1}γ_k]. A finite-horizon model does not certify this infinite sum. Truncation needs a proved tail bound; inventing a spectral gap or fitting an exponential tail is not supplied by the scalar acquisition theorem. Optimizing among supplied schedules is also distinct from globally optimizing over exponentially many words.

## 4. Rank-two counterexample: low task dimension does not fix tiny slow tails

Take the four states (x,y)∈{−1,+1}² with common uniform π. At each step independently refresh x; retain y through a reversible binary kernel with eigenvalue 1−γ, 0<γ≤1. Define

f=(√(1−a)x+√a y)/√2, 0<a<1.

This f has mean zero, |f|≤1, γ_0=1/2, and for k≥1

γ_k=(a/2)(1−γ)^k.

Its reachable function span has dimension at most TWO, with no large-state or nonlinear obstruction. Compare with the full-refresh kernel (γ=1). Every nonempty return differs by at most a/2, for ALL horizons, and Gram returns obey the same small bound. Yet

σ²_asym=γ_0+2Σ_{k≥1}γ_k=1/2+a(1−γ)/γ,

which becomes arbitrarily large as γ→0 at fixed a. Consequently any absolute-accuracy report contract coarser than a/2 can be completely correct while failing to resolve the important variance penalty. Even exact low rank and genuinely common-stationary reversible access do not bridge that downstream task gap. This is not a counterexample to the finite-horizon theorem; it is a counterexample to promoting its guarantee into automatic resolution of critical slowing.

## 5. Few slow modes of each kernel does not establish switched low width

The assumption needed is one low-dimensional approximation space for all requested forward AND reverse prefixes. Evidence that one fixed update has a few important slow modes is insufficient. Even two reversible permutation involutions have seed cyclic dimension at most two individually, while their products can generate a long dihedral orbit and a high-dimensional joint reachable span. Adding a common uniform-refresh component makes each kernel ergodic without removing the algebraic distinction. Thus physical slow-mode papers cannot be used as evidence for the theorem's switched-family width without additional work.

An acquisition certificate can reject and add features; that is valuable fail-safe behavior, not evidence that acquisition will be cheap in lattice QCD.

## 6. Comparator and compounding test

A strong ordinary learner can retain all return experiments, estimate correlations directly, fit slow-mode/time-series or controlled realization models, adaptively race schedules, and exploit known reversible/nonreversible MCMC improvements. The proposed learner may offer its specific rigorous output certificate, but a separation in lifetime scientific accuracy per compute has not been established. No claim that existing methods already prove the identical gap-free adaptive theorem is made.

A legitimate compounding win would require, at a fixed source setting:

(1) a paid independent/certifiably biased source cheaper than the eventual saved production work;
(2) low JOINT forward/adjoint task width at the needed accuracy;
(3) a finite-run objective or independently controlled correlation tail;
(4) acquisition + search + deployment cost below a retaining same-access baseline at equal precision;
(5) enough future production/schedule reuse to amortize acquisition before source drift/change.

None is established for a consequential lattice platform in this pass. The correct verdict is no qualifying platform found, with an explicit serious candidate and a precise task-mismatch obstruction—not a generic application list.

## Primary source evidence and access ledger

* Schaefer, Sommer, Virotta, “Critical slowing down and error analysis in lattice QCD simulations,” https://arxiv.org/abs/1009.5228 (opened successfully). Their study finds severe topological slowing and discusses incorporating slow-observable information into physical-observable error analysis. It does not establish low switched reachable width.
* Schaefer and Virotta, “Autocorrelations in Hybrid Monte Carlo Simulations,” https://arxiv.org/abs/1011.5151 (search-index abstract retrieved). Supports the scientific relevance of slow-mode contamination.
* Neal, “Improving Asymptotic Variance of MCMC Estimators: Non-reversible Chains are Better,” https://arxiv.org/abs/math/0407281 (opened successfully). Supplies a substantive ordinary algorithmic comparator: nonreversible modification with no worse asymptotic variance under its stated finite-state assumptions. It is not claimed to solve arbitrary switched learning or lattice QCD.

An unnecessary legacy open of https://www.osti.gov/servlets/purl/1235276 returned HTTP 502 during this pass; it was not retried or bypassed and supports no claim in this note. No denied sources accessed; no publication or external communications.
