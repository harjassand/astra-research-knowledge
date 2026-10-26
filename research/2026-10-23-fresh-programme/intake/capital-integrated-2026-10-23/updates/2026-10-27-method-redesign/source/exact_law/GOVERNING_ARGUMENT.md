# Checked proposer -> exact sparse law

The construction supports the explicit cube and partition-base inputs of Astra N24. It does not supply a general-matroid oracle, an entropy-sensitive signing theorem, a new stochastic concentration law, or empirical science data.

## Input and output contract

Let `A` be an `R by n` rational matrix with `|A_ij|<=1`, `R,n>=1`, and let `p` be a rational vector in `[0,1]^n`. For partition bases additionally supply a partition of the coordinates into nonempty blocks with integral block sums of `p`.

A completed output is a finite list `(z,w)` with positive rational weights, sum of weights exactly 1, binary atoms, coordinate mean exactly `p`, and at most `n+1` distinct atoms. Coordinates with `p_j=0` or 1 are frozen. Each supplied block quota holds at every atom. The returned discrepancy is independently recomputed as the exact rational maximum of `|A_i(z-p)|` over every output atom and row. Approximate empirical frequencies are never substituted for exact means.

`checked_interface.compile_exact_law` is the process-scoped callable API. `bridge.py` supplies the checked sign adapter and executable comparisons. The original N24 compilers and public GSW modules are preserved byte for byte in `vendor/`; callback installation affects only the isolated process.

## 1. A sign proposal has no statistical authority

For an active direction matrix `D`, the numerical routine proposes a vector `eta`. The adapter rejects an upstream failure flag, incorrect length, nonbinary output, exception, or violation of the exact rational row condition. For the cube condition that check is

`(sum_j D_ij eta_j)^2 < 8*r*s` for every row,

and for the partition condition it is `<16*r*s`, where `r=ceil(log2(2R))` and `s` is the number of active original coordinates. The original N24 exact moment signer is a fallback if none of the eight bounded proposals passes. Every failed proposal and fallback is retained and charged. A cached signing is keyed by the entire exact rational matrix, active size and bound, and is checked again.

A common integer factor `4R` scales the numerical matrix. In N24's direction geometry its entries have magnitude at most 4, so each scaled column has Euclidean norm at most 1. This is only a numerical input transformation. Correctness is checked on the unscaled original rational `D`. No ideal-arithmetic GSW unbiasedness or concentration theorem, and no finite-precision theorem, is used as a premise. The three-bit variant uses the upstream reduced-mantissa arithmetic model, not an IEEE hardware-format claim.

## 2. Arbitrarily biased selection preserves exact means after symmetric branching

In the cube, pair active original coordinates; an odd active set gets one dummy zero column. A proposed pair sign assigns opposite signs to the two coordinates, so total active signing sum is zero or has magnitude at most 1. Partition directions are the source compiler's disjoint two-/four-coordinate exchanges; each preserves every block quota and controls change in the near-vertex defect.

At dyadic level `h`, for any current atom `q` and any accepted signing `xi`, the compiler adds both children

`q_plus=q+2^(-h)*xi`, `q_minus=q-2^(-h)*xi`

with half the parent weight each. Their exact average is `q`. This identity holds for every chosen signing, even if the proposer is biased, adaptively selected, low precision, cached, or selected for its observed score. Conditioning on a parent cannot invalidate the identity. Keeping both children is essential: emitting only one numerical sample would not yield this exact output law.

The original dyadic feasibility and direction rules keep both children in the cube, preserve partition quotas and leave forced face coordinates unchanged. No probabilistic marginal claim from GSW is needed.

## 3. Exact compression does not create an unverified atom

For atom columns `[1;q]`, an exact affine dependence `v` satisfies `sum v=0` and `sum v*q=0`. Moving weights by `w-theta*v`, where `theta=min(w_j/v_j : v_j>0)`, preserves normalization and coordinate means, keeps weights nonnegative and removes at least one positive atom. Removing zero weights and repeating leaves at most the augmented matrix rank, hence at most `n+1` atoms.

Compression retains a subset of already constructed atoms; it does not invent new ones. Every pointwise face, quota and discrepancy property therefore survives. Exact rational arithmetic, including denominator growth, is charged to the computation. Compression need not preserve negative dependence or a sampler's original distribution; neither is part of this contract.

## 4. What the source moment envelope still gives

The accepted per-step inequalities are the same inequalities used by N24's original moment proof. Its mass/defect bounds and geometric sum therefore continue to give the existing cube envelope `<1+12*sqrt(r*mu)` for `mu>1`, with the source small-mass branch for `mu<=1`, and the existing partition envelope `<1+20*sqrt(r*mu)` for `mu>=1`, with its source small-defect branch otherwise. Here `mu=sum min(p_j,1-p_j)`.

This argument depends on the explicit source cube/partition directions and exact per-step verification; it does not transfer to arbitrary exchange systems. The numerical replacement does not improve the asymptotic envelope. Local minimum signing error also need not minimize the final maximum atom error: different signings change later branches and which atoms survive compression.

For the frozen primary dimensions `n<=16,R>=6`, the conservative per-step envelope is loose. Any balanced binary signing can meet it in these small cases. Thus the absence of natural row rejection in those runs is not strong evidence about near-boundary numerical reliability. Separately labelled boundary and large-active-set guard controls exercise genuine strict-bound rejection and fallback.

## 5. Ordinary exact global optimisation is a stronger small comparator

On small instances, enumerate every face/quota-feasible Boolean vertex `z` and its exact error `d(z)`. For a threshold `T`, a law with worst supported error at most `T` exists exactly when `p` lies in the convex hull of vertices satisfying `d(z)<=T`.

A numerical LP is only a proposal for a support. Its weights are reconstructed by exact rational elimination and checked. Infeasibility is accepted only with a rational affine separator `c,b` for which `c*z+b>=0` for every eligible vertex and `c*p+b<0`. The separator directly contradicts any convex combination equal to `p`.

Vertex errors form a finite ordered set. A feasible law at one error level and an exact separator at its immediately preceding level certify the globally minimum possible worst-supported error. If the feasible level is the smallest vertex cost, enumeration already excludes any cheaper atom. All finite vertices, support weights and separating inequalities are checked, not inferred from an LP status code.

The selected post-hoc `n=16` audit uses a common exact integer scale for all row errors. It verifies the scale identities and a bound on every possible integer sum before vectorized int64 evaluation. The final law and predecessor separator are then independently checked by the standalone stdlib/Fraction auditor. Enumerating all vertices is exponential, so no scalable optimisation theorem follows.

## Scope of the completed construction

This is a general correctness-preserving adapter for valid rational cube/partition inputs when it returns successfully, together with actual finite executions and a bounded fallback. It is an implementation of known proposer/checker, symmetric branching and Caratheodory compression operations. N24 already describes replacing its signing routine. The adapter acquires an executable software interface in this folder; it does not acquire an output contract that the existing N24 compiler or ordinary exact optimisation lacked.
