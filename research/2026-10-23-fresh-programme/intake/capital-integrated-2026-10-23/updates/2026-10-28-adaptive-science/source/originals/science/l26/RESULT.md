# Result: an acquired source-smoothed Stein correction interface

The universal N687 polylogarithmic-query sampler is **not established**. This work constructed and checked a more explicit part of its missing positive correction machinery: a controlled full affine Stein inverse, a finite residual-action implementation, a full-law nonlinear-step bound, and a four-original-query source preimage for the first heat-smoothed residual. A genuine conservative family rejects the unsmoothed inverse route.

## Mathematical and acquisition results

**The source derivative causes actual inverse instability.** For the exact Gaussian affine source X=kappa G+sqrt(1-kappa²)Z, the unique scalar L2 pointwise inverse on source Hermite degree n grows at least a^(-n-1)/(n+2)², a=sqrt(1-kappa²). Thus arbitrarily small kappa does not give a bounded unsmoothed inverse on arbitrary Gaussian L2 residuals. This is stronger than observing that the derivative itself is unbounded. Source-only OU smoothing P_rho restores a bounded inverse exactly when rho<=a in this scalar problem.

**There is a controlled vector inverse after that explicit reserve.** In every d, a simpler choice u=delta_Z J0, together with a divergence-free skew gauge, solves the full affine linearization for the forcing -P_a R. The correction, its source and noise derivatives, and its Stein matrix all have L2 bounds independent of d and chaos degree, using the residual's Frobenius L2 norm. Proof: [CORE_THEOREM.md](CORE_THEOREM.md), Sections 1–4.

**Its correction can be acquired without a realized random matrix.** A fixed Gaussian program uses one action R(Y)V and returns a conditional-unbiased correction Uhat. The exact energy is pi²||R||_(L2,F)²/(8a²). The residual query point and V are exactly independent Gaussian vectors in their marginal law. A fresh tau-Gaussian reserve gives a full-TV randomization bound quadratic in this energy. No mean, derivative, conditional expectation, or matrix square root is executed by this correction. A noisy conditionally unbiased residual action can be substituted, with its actual variance charged.

**The nonlinear integration has a full-law receipt.** For an actual Stein program whose residual is P_a R0 and whose coefficient distance from the affine reference is eta in L2 operator norm, the implemented update obeys

    TV <= H(tau)[A eta r+B r²]+phi(1)c²r²/tau²,
    r=||R0||_(L2,F).

All constants are explicit in CORE_THEOREM.md Section 8. Products need only L1 control, obtained by Cauchy–Schwarz. This is quadratic when eta=O(r). Fixed-reference eta need not shrink after an update; this theorem alone does not justify repeated quadratic convergence or log-log depth. The Gaussian reserve is included in the target covariance.

**The first smoothed residual preimage has legal g-value acquisition.** For h_b(y)=E g(by+sqrt(1-b²)Z), the residual Gamma_b-kappa²I, Gamma_b=sym(K_b Dh_b), has a source preimage P_a R0=Gamma_b-kappa²I whenever

    (kappa²/a²) 2b²/(1-b²) <= beta < 1.

A negative-correlation Gaussian covariance allocation followed by two fresh chi_3 secant actions acquires R0(y)v with at most four original whole-vector g queries on every execution and norm at most (b²L²+kappa²)||v||. The correlated source points become the required independent heat points after source smoothing. This also extends to m-factor fixed-center words at at most 2m queries under the displayed rank-one covariance budget. Proof and exact boundaries: [PREIMAGE_ACTION.md](PREIMAGE_ACTION.md).

## Stress test and checks

The smooth conservative family g_k(x)=kappa x+delta sin(kx)/k has a uniformly bounded actual Stein residual but drives the unsmoothed affine preconditioner at least exp(kappa²k²/(2a²))/poly(k). Its values converge uniformly to the affine source. This is a mechanism counterfamily, not a lower bound for active sampling algorithms. Proof is in CORE_THEOREM.md Section 6; finite spectral diagnostics are in [genuine_family.csv](genuine_family.csv).

Six vector Hermite checks in d=1,2,3 verified both gauges, divergence, and full matrix equations with errors below 2.5e-15. The finite random action's exact covariance and energy identities were checked numerically in d=4; conditional-mean errors were below 0.0011 at 250,000 draws. The legal four-g-query preimage action was checked at three outer points with 400,000 draws each, mean errors below 2.5e-5, and the source covariance identity within 1.2e-16. These are implementation checks; the proofs, rather than finite moments or KS tests, establish the stated full-law bounds.

An additional original-value-only implementation on the explicit sinusoidal family uses nine g queries per run and has a proved O(eta²) full-TV bound. For kappa=0.5,k=2,tau=0.5, eta=0.001 the conservative bound is 0.001473. This is only a mechanism validation: the equally informed ordinary comparator queries g(0), then samples the exact Gaussian in one query. [VALUE_ONLY_RESTRICTED.md](VALUE_ONLY_RESTRICTED.md) states that advantage limitation explicitly.

Executable owned scripts and outputs are `check_vector_inverse.py`, `residual_action.py`, `check_preimage_action.py`, `genuine_family.py`, `value_only_family.py`, and their adjacent data files. The authorised single helper independently derived the sharp scalar inverse, its finite action and Gaussian-reserve bound; its complete proof is [helper/AFFINE_INVERSE.md](helper/AFFINE_INVERSE.md). The main trajectory owns the vector gauge, nonlinear integration, original-value preimage construction, and the scientific conclusions.

## Consequence, prior overlap, and hardest remaining construction

Frozen S3 already supplied the baseline Hodge gauge, formal Newton identity, and baseline L2 estimate. Frozen S4 supplied the bounded two-value heat/resolvent actions. S12 already rejected frozen nonlinear rotations and iid averaging as quadratic updates. This work uses that capital; Gaussian Mehler calculus, Hermite methods and density Taylor expansion are standard. No external novelty or priority search was completed.

The new first preimage action is useful because it acquires a correction field while preserving its common-source correlation and without assuming a realized matrix. Its explicit smoothing budget exposes the cost that a generic residual oracle would conceal. The next attack can now work on an acquired joint starting mean circuit and controlled nonlinear word/preimage closure, rather than inventing this first action from scratch.

The hardest unresolved obligation is still the acquired nonlinear recursive program. **h_b(G) itself is an unacquired mean node in the first preimage theorem.** A joint value-only starting implementation, successive residual preimages, a current-law inverse or subcritical Neumann chain, source retention, noise allocation, all original query counts and every-execution tail caps remain unproved. High-frequency preimage costs can be exponential outside the explicit covariance regime. The fixed-exponent R16 candidate and bounded-input FORS remain stronger end-to-end competitors under their actual contracts. No universal query improvement, practical speedup, new learning capability, or completion of N687 is claimed.

All work stayed inside l26 and its one authorised helper directory. Frozen sources were read only and no source script was executed or active checkout changed.
