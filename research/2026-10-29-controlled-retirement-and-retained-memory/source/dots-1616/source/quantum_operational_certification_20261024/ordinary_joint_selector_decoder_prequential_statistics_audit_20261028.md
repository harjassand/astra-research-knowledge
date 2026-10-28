# Independent statistics/control audit: joint selector and decoder discovery

28 October 2026. Reviewer: `producer-workspace/audit_count_pilot_fresh`.

**PASS at the supplied common-decoder, one-terminal, additive-regret scope.** Final source `ordinary_joint_selector_decoder_prequential_20261028.md`, SHA-256 `ead2aaf47370e5fa0882cf90802325e0c914b8d25cbb05f86981f91a02cd6d4e`. The earlier `00a6705a…` source is preserved. The clarification fixes a dyadic mesh and explicitly pays rational selector-sampling bits; it does not change the risk or query theorem. This audit imports no forthcoming main receipt, so the receiving graph is acyclic. No source calls, RNG draws, acquisition simulation or generic optimizer execution occurred.

## 1. Current conditional laws and nonnegative excess

At a fixed actual prior history, a fresh selector and logical input meet the same conditional complete source channel. The supplied CP-order promise gives `H_I(x)>=H_alpha(x)` for every selector and conditional memory state. The received Bell-block dual argument therefore makes the same fixed D_* optimal for every x and history. Restricting the physical selector effect to real vectors gives a real symmetric quadratic for both loss and excess. Nonnegative excess for every real unit vector is exactly PSD of its real coefficient matrix. Hence its value at any unit vector is at most its trace, which is m times the uniform-basis average. This pointwise argument also applies to a decoder chosen from the prior record.

The factor m transfers EXCESS, not raw anchor noise. It introduces neither an inverse gauge eigenvalue nor a supplied contrast. The fixed common oracle is the load-bearing structural promise; no generic joint encoder/decoder family is covered by this reduction.

## 2. Actual two-role gradients on one correlated history

The decoder role's physical single-copy Pauli record is the received normalized-Choi gradient. Averaging its known uniform basis anchor gives the current anchor-calibration gradient. It does not require applying the current decoder, reading a Pauli coefficient or resetting source memory.

For the selector role, real finite design moments are

`E zz^T=I/m`,

`E[(z^T A z)zz^T]=(2A+Tr(A)I)/(m(m+2))`.

They follow directly from the basis/Rademacher mixture: fourth diagonal moments are `3/(m(m+2))`, paired distinct moments are `1/(m(m+2))`, and odd mixed moments vanish. The actual current-decoder return bit has mean z^T A z, so

`E[y T(z)]=A`, with `T(z)=m(m+2)zz^T/2-mI/2`.

For every design point, T has one eigenvalue `m(m+1)/2` and m-1 eigenvalues `-m/2`. Therefore `||T||_F^2=m^3(m+3)/4<=m^4`. Its entries are rational: for a sign vector, `zz^T=ss^T/m`. The sampler does not enumerate its exponentially many sign vectors; it draws m fair bits and actually prepares the known real selector.

The role coin is fresh and fair at the SAME pre-call memory history. Thus `2 I_D g_D` and `2 I_S yT` have the two stated conditional means and deterministic norm bounds. Their records and future histories need not be independent. In fact they cannot generally be independent: only one block is nonzero on a given call. The selector loss matrix may depend on the current decoder and the entire previous record; it is fixed before the fresh role/design coins, which is the requirement used by online regret.

## 3. Exact repaired projection constants

Both feasible sets have squared initial radius at most 1 and diameter at most sqrt(2). For a gradient bound 2G and step `1/(2G sqrt(N))`, the received projection-gap argument gives

`sum <G_t,Z_t-Z_*> <= 1/(2eta)+(eta/2)N(2G)^2+3N sqrt(xi)/(2eta)`

` = (11/4)G sqrt(N) <4G sqrt(N)`.

The two cases are G=G0 and G=m^2. The approximate projection residual `3sqrt(xi)` follows by comparing squared distances of two feasible points, each at most the feasible diameter from the comparator. It does not require exact spectral projection. Gradient-step norms remain at most 2, exactly as needed for the inherited Choi objective repair.

For the real selector repair, trace correction gives `lambda_min(Xhat)>=-(1+1/m)delta`. Adding 3delta I and renormalizing yields exact trace 1 and the stated positive lower bound. More sharply than needed,

`||Xphys-Xtilde||_1 <=(6m+1)delta<=7m delta`.

Indeed `||Xhat||_1<=1+2(m+1)delta`, and the subsequent mixture with I/m costs at most 6m delta. The source's 10m delta bound is therefore safe. For `||Y||_F<=2`, the source's repair bound changes the quadratic objective by at most

`10m delta(6+10m delta)<61m delta`

at its chosen delta. With `delta=xi/(4096m)`, this is less than 0.015xi. Solver and rounding allowances below xi/4 each, plus a conventional center/interior allowance if required, fit strictly below xi.

The largest dyadic mesh `u<=delta/(128m)` has polynomially many bits. Symmetric entry rounding changes operator/Frobenius norm and trace by at most m u, so a starting feasibility tolerance delta/2 remains safely within delta; its quadratic objective debit also fits the displayed rounding allowance. Fixed output grids reset denominator lengths. The known interior and bounded feasible set give a standard finite quadratic convex task with exact rational repair/certification on every history. This review does not assert execution of that generic solver. A physical numerical fallback cannot claim an unearned optimization guarantee.

## 4. Rational LDL is an actual pure-selector ensemble

Write u=1/Q. Substitution into the repair formula gives a common selector denominator dividing

`K=mQ(65536N^2+3)`.

This K is fixed before observations, and its bit length is O(log m+log N). Retained zero-gradient iterates and the initial I/m also have denominators dividing K.

For the integer SPD matrix B=KX, let a_i be its positive leading principal determinants, with a_0=1. Fraction-free LDL identities give `D_i=a_i/(K a_(i-1))` and entries of column l_i with denominators dividing a_i. Thus each `w_i=D_i||l_i||^2` has denominator dividing `K a_(i-1)a_i`. All weights are positive and sum to Tr X=1, and the exact reconstruction is

`X=sum_i w_i (l_i/||l_i||)(l_i/||l_i||)^T`.

Here 'positive integer matrix' means integer SPD, not entrywise nonnegative; negative entries cause no problem. Since B is PSD with trace K, `a_i<=K^i`. Therefore

`J=K a_m product_(i<m)a_i^2<=K^(m^2+1)`

is a valid integer common sampling denominator. Unit-diagonal LDL columns have norm at least 1, so normalizing a selected vector does not divide by a tiny mixture weight. Finite exact rational LDL and determinant bit bounds are polynomial in m and log K.

Sampling an integer below J and applying cumulative integer weights gives exactly the desired distribution on success. The selected normalized real vector generally has algebraic, not rational, amplitudes. Its known amplitude controls are compiled and paid; the source does not assert rational exact gate angles or an uncharged eigenbasis. This is a classical mixture of pure selectors, not a retained purification.

## 5. Conditional expectations, joint regret and terminal channel

Pathwise regret can be averaged against each FIXED C_* and X_* because the iterates are predictable and both gradients are conditionally unbiased. Correlation between the blocks introduces no additional term. The result does not choose a hindsight comparator separately for each trajectory or compare to a different source occupation induced by another policy.

Choose C_* for the pointwise optimal common D_* and any fixed real pure selector x_*. The selector regret controls the first loss difference. PSD excess domination controls the decoder remainder by m times its anchor regret. Multiplying the ordinary mismatch risks by 3/2 gives precisely

`average Bell loss <= ell_*+6(m^2+mG0)/sqrt(N)`.

Optimizing the expected fixed-selector objective is legitimate by compactness; a pure real selector attains the linear objective over real densities. A history-adaptive encoder can be better and is not the comparator. A single implementation discrepancy does not transfer the benchmark to different imperfect-control histories.

The stable received private-terminal prefix proof applies to the actual two-role process. At T the current learned density is physically sampled by its LDL ensemble and the current decoder is applied to the fresh independently held payload; no gradient is obtained from that unknown input. The resulting convex mixture of complete CPTP maps is exactly the source's equation (17), also with an arbitrary initially independent reference. There is no unseen-future or reusable-decoder claim.

The least power-of-four choice of N gives statistical excess at most epsilon/2 and

`N<576(m^2+mG0)^2/epsilon^2`

` <=[1152m^4+2304m^2 d^5]/epsilon^2`.

This includes the one terminal payload. The remaining epsilon/2 is one declared complete implementation allowance. It is an EXPECTED averaged-terminal result, not a record-wise high-probability acquisition certificate. The scalar m=1 edge case is valid: the selector set is a singleton, its actual regret is zero, and the conservative formulas still hold.

## 6. Explicit random bits and physical controls

A full conservative bit bound implied by the source is obtained with

`b_max=max{2,ceil(log2(m+2)),1+(m^2+1)ceil(log2 K)}`,

`R=ceil(log2(16N/nu_rng))`:

`log2 N + N(m+2w+2) + 8NR b_max`.

The direct bits cover role, logical sign, all possible sign-design entries and physical Pauli words. The capped terms cover all indices, mixture choices and the worst-case rational LDL sampler. At most 8N conditional rejection failures, each at most 2^(-R), give total at most nu_rng/2. The exact local success law is not used to condition the entire statistical proof on successful sampler histories; instead the finite implementation couples to the ideal process until exhaustion and pays its uniform abort probability once. A general rational mixture is not charged only log m bits.

Every source input uses one logical qubit and ceil(log2 m) selector qubits. General known selectors cost O(m) amplitude preparation before precision/routing overhead. Every selector-effect probe pays the actual general CPTP decoder and return measurement; anchor probes pay local physical-Pauli readouts. Compile/pad before possible terminal calls, count both finite projection procedures and their classical duration, and charge trusted payload storage throughout. Raw records can require O(N(m+w+log m)) bits; they are not IID counts. Known Choi/selector matrices and their bounded-bit processing, ancillas, dense receiver synthesis and all complete control discrepancies remain paid.

This is not efficient solely in log m or physical output width w. The equally informed conventional competitor has the same finite online convex estimators and structural promises. No source-query or practical performance advantage over it is asserted.

## 7. Exact independent evidence and rate boundary

`joint_selector_decoder_prequential_statistics_check_20261028.py/.json` records 18 exact effect/design cases over 441 finite design terms; a same-history physical role covariance of -1/3; 12 exact real-density repair/LDL/common-denominator cases including negative matrix entries; 12 bounded integer-sampler laws; and 45 full regret, query and bit-budget cases. All use deterministic rational arithmetic. The checks do not execute a source, RNG, OGD trajectory pilot or generic SDP solver.

The source's noisy-anchor obstruction is correct: the selector Pauli effects sum to I, their identity effect dominates each alternative, a hidden selector is perfect, yet the uniform-anchor oracle Bell loss is `(3/4)(1-1/m)`. A first-order raw-anchor-loss bound does not automatically become a fast excess bound. The source therefore correctly retains epsilon^(-2), rather than importing the fast bandit's epsilon^(-1) behavior or a reset-source active-design theorem. A separate short-horizon empirical bandit comparison is not evidence for or against this unexecuted polynomial guarantee.

No unresolved statistical, finite-selector or sampler-budget objection remains. Receive only the supplied common-decoder, known real-selector family, fixed known output patch and one privately timed terminal encoder/recovery decision with the declared complete interface.
