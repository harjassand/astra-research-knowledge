# Independent audit — direct CPTP Bures-risk decoder bridge

Auditor: `producer-workspace/independent_bures_bridge`.
Date: 27 October 2026. No uploads, merges, or physical quantum execution.

**Standalone mathematical composition: PASS.** The finished standalone, root candidate, actual imported source statements, and independent algebra/numerics have been inspected. Receipt is recorded separately against the final standalone hash.

## Exact objective and uniform risk

The six Pauli rank-one projectors obey

`(1/6) sum_j P_j tensor P_j = (I+SWAP)/6`.

For every qubit TP channel Λ this gives average state fidelity `(1+2 F_e(Λ))/3`. Thus the decoder objective

`R_rho(D)=(1/4) sum_j [1-Tr(P_j D(rho_j))]`

is exactly `1-F_e(D E)` when `rho_j=E(P_j)`. CP and TP imply `0<=D†(P_j)<=I`, so the individual loss effects `L_j=(3/2)(I-D†(P_j))` lie in `[0,(3/2)I]`. This argument covers every CPTP decoder, not merely a chosen architecture. It does not transfer unchanged to arbitrary trace-decreasing accepted decoders.

For arbitrary density estimates `tau_j`, use mathematical Uhlmann purifications and apply `sqrt(L_j)` in their direct sum. The vector-distance upper bound is `sqrt(3 delta)`, where `delta=(1/6)sum_j(1-F_root(rho_j,tau_j))`. Reverse triangle inequality proves

`|sqrt(R_rho(D))-sqrt(R_tau(D))| <= sqrt(3 delta)`

uniformly over all feasible decoders. There is no assumption that the estimates form a physical channel, are unbiased, or have independent errors. For an eta-optimal empirical CPTP decoder,

`sqrt(R_rho(Dhat)) <= sqrt(ell_opt)+2 sqrt(3 delta)+sqrt(eta)`.

Minkowski in the record probability space replaces `delta` by its expectation bound `m`. Let `u=2 sqrt(3m)+sqrt(eta)`. Then `u²<=24m+2eta`, and for `0<gamma<=1`,

`(sqrt(ell_opt)+u)² <= (1+gamma)ell_opt+(1+1/gamma)u²`

`<= (1+gamma)ell_opt+48m/gamma+4eta/gamma`.

The constants in the candidate are correct. This is the key distinction from the earlier unitary-witness composition, which incurred a factor-two loss comparator.

## Actual common frame and source chronology

A Choi-rank upper bound R provides a Kraus family of size at most R. The common output support has dimension at most `2R`, and each pure-input output has rank at most R. Set `k=min(s,2R)` and `r=min(R,k)`. All six pre-acquired n-copy banks and the later independent datum must enter one joint reduction. Its arbitrary-operator identity extends with an untouched reference by linearity. Conditional on its mathematical common U, the banks are iid within labels, independent across labels and from the reference/datum, and their output orientation agrees with the datum. Restriction/extension along the unknown support isometry proves invariance of the unrestricted optimum; this is a comparison argument, not an implemented source inverse.

Actual source checks: [Lowe–Tan v2, Theorem 1.1 and Section 5.2](https://arxiv.org/html/2606.23592v2) state the arbitrary-supported-operator channel identity and polynomial gate approximation in number of registers, log ambient dimension and log inverse diamond error. Its Theorem 3.1 explicitly includes random purification for rank **at most** the auxiliary dimension. The paper attributes the reduction primitive to earlier universal-decoder work. [PSTW v1, Theorem 1.1 and Section 3.3](https://arxiv.org/html/2511.15806v1) supply an actual efficiently approximable purification channel. These are imported representation-theoretic circuit theorems, not independently re-proved or physically run in this audit.

One applies purification separately to each homogeneous n-copy bank. No simultaneous purification of heterogeneous inputs is asserted. The direct decoder needs no coherent learner inversion: after joint reduction the bank may be measured, discarded, and classically processed, while the compressed datum remains stored. The obtained classical decoder is tied to that particular consumed quantum frame, not a reusable decoder on future physical data.

## Tomography constants and confidence

After padding `kr<=D<2kr` to a power of two, Clifford measurement gives `X=(D+1)P-I`, with exact moments `E X=Phi` and `E(X-Phi)²=D I+(D-2)Phi<=2D I`. Since `||X-Phi||<=D+1`, the Bernstein denominator at `0<t<=1` is at most `5D`. The resulting tail is

`Pr(||Xbar-Phi||>t)<=2D exp(-n t²/(5D))`.

A computed top vector of a nearby Hermitian matrix with backward error a has pure infidelity at most `min(1,4(e+a)²)`, where `e=||Xbar-Phi||`. The bound does not require a gap for the empirical matrix. Tracing out the known auxiliary register, with a CPTP completion for padding leakage, cannot increase root-infidelity beyond the pure infidelity bound.

For the high-probability interface choose `t=a=sqrt(m)/4`, with `0<m<=1`. The pure infidelity is at most m on the good event. The exact six-bank union bound is `12D exp(-nm/(80D))`; hence

`n>=80D log(12D/beta)/m`

suffices. The expectation interface follows by integrating the clipped tail and using `min(1,4(e+a)²)<=2min(1,4e²)+8a²`, yielding `m<=40D[log(2D)+1]/n+8a²`. Exact-uniform Clifford randomness is an ideal finite-distribution specification; any capped sampler or finite-gate seed approximation must be paid in the implementation discrepancy.

The high-probability event is conditional on a mathematical frame/purification decomposition. It is not a guarantee for every exposed physical training record. A later independent same-frame validation record is a separate issue. Approximate physical implementation must be debited separately rather than silently promoted to exact event-level behavior.

## Finite SDP and exact feasibility

With unnormalized input-first decoder Choi matrix C, the program is

`min Tr(H C), C>=0, Tr_out C=I_k`,

`H=(1/4)sum_j tau_j^T tensor (I_2-P_j)>=0`.

There is a known strict primal point `C0=I_k tensor I_2/2`, total feasible trace k, and strict dual point `Y=-I_k` for `Y tensor I_2<=H`. The coefficient norm obeys `||H||<=b=3/2`, and more sharply `Tr H=b`. Standard finite-dimensional SDP weak optimization is polynomial with these bounded, interior-feasible data. Floating-point solver status alone is not a CPTP certificate.

An especially simple rational feasibility repair is available. Mix a sufficiently accurate feasible primal with `lambda C0`, yielding minimum eigenvalue at least `lambda/2`. Let Cround be a Hermitian dyadic rounding with operator error at most h, and put

`Cfix=Cround+(I_k-Tr_out Cround) tensor I_2/2`.

This is exactly TP in rational arithmetic. The partial trace amplifies operator norm by at most the output dimension 2, so the repair adds operator error at most h. Thus `Cfix>= (lambda/2-2h)I`, positive for `h<=lambda/8`. Its difference from the mixed target has operator norm at most `2h`, and positivity of H with `Tr H=b` bounds the objective debit by `2bh` (the looser trace-norm bound `4bkh` also suffices). Mixing, coefficient rounding, weak optimization and this correction can all fit within eta using inverse-polynomial tolerances. For a near-feasible dual, shifting `Y` downward by `delta I_k` loses `k delta` in the dual objective, so the dual slack tolerance must explicitly scale with `eta/k`. Seed total-variation error delta contributes at most `2 delta` to an unhalved diamond budget. Known Kraus/Stinespring synthesis then uses polynomial-size dense linear algebra and paid gate precision. No source-state inverse or source spectral floor enters.

The candidate's inverse-square-root partial-trace normalization is also valid when the trace matrix remains uniformly close to I. The affine repair simply gives an exact rational alternative with transparent constants.

## Independent checks and their limits

`independent_bures_bridge_checks.py` uses a fixed independent seed. It executed 60 random physical source/decoder cases (compressed dimensions 2,3,4,6,8), 120 pure-state eigenvector perturbation cases, and exact symbolic six-Pauli/design moment identities. Its JSON reports maximum six-Pauli/entanglement-loss residual below `3.4e-16`, Choi objective residual below `7.8e-16`, no positive Bures/Young/top-vector violation, and affine TP repair residual below `1.6e-16`. It also exactly checks the statistical/optimization half-budget and Bernstein constants.

The optimization spot check chooses the empirical optimum of a finite feasible decoder family, not the full SDP. Neither a full Schur/purification learner circuit nor final gate synthesis was run. Numerical corroboration is not the asymptotic proof.

The author also supplied three dyadic primal/dual decoder SDP certificates. I read and replayed its exact verifier successfully; the certified gaps are approximately `3.5224e-7`, `4.9273e-7`, and `8.4688e-7`, each below `1e-6`, for the explicitly rounded coefficient problems. A separate independent exact-LDL replay is included rather than treating a floating Newton solver as certification. These finite certificates verify exact TP, strict primal positivity, dual-slack positivity and objective gap, not the full learner implementation.

## Scope retained

The final standalone retains the stated imported interfaces and precision allocations, including the audited eta/k dual-slack repair, twice-TV seed debit, and beta-scale inner record approximation needed for a high-confidence interface. The expected deployment bound is mathematically justified. `D<4R²` gives `O(R² log(2R)/(gamma epsilon))` source calls and theoretical polynomial gates/classical work. This does not claim small constants, practical hardware performance, novelty, generic many-qubit-noise scalability, diamond-optimal recovery, approximate-rank robustness, or quantum-program reuse. R can be exponential in physical qubit count. The bank is consumed jointly with one datum; future data do not inherit this frame.
