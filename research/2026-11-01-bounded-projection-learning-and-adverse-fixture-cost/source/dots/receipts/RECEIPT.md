# Independent bounded-projection acquisition receipt — 2026-11-01

Audited BOUNDED_PROJECTION_ACQUISITION.md as supplied at SHA256 57eef80f88aa8229a2019b8f4884562a01beb40cfe0ff06744ac3abb0fca68dd. This is an independent mathematical review of the new nonlinear receiver, not a transfer of the preceding inverse-Gram or state-norm results. I coordinated with the constructor only to avoid duplicating implementation/testing. No novelty, optimality, practical performance, or physical demonstration is certified.

## Current-byte binding and rounded update

I subsequently read and verified current main-construction SHA256 4dd9265425b1ef0f78c487602c63e6cd8d78b429c1cf7bc67155981e8ad1632f. Its explicit proposed 64r ceiling and prior-method attribution are consistent with this receipt. The mathematical acceptance below applies to those current bytes.

The original unrounded-solver cost warning below is HISTORICAL AND METHOD-SPECIFIC. The separately reviewed author ROUNDED_PROJECTION_SOLVER.md SHA256 972ee67b866093f791d11e8081d379bbdf27037f80549b92c8d29d690ca3640b supersedes that implementation choice. See ROUNDED_SOLVER_ADDENDUM.md in this directory: its rounded solver does achieve sufficient DIGITAL as well as source lambda^-2 accuracy dependence up to logarithms. The original unrounded closure is preserved for audit history, not asserted to limit the rounded algorithm.

## Disposition

No counterexample or unresolved mathematical obstruction found in the stated online, fixed-horizon, same-seed return theorem. Its source-shot accuracy factor lambda^-2 is justified. It is NOT a lambda^-2 bound on total digital work. The proposed exact fixed-step solver can have much larger digital cost. An explicit conservative arithmetic envelope and sufficient bad-event calibration are proved below; the old inverse-based W^10 work bound must not be reused.

Required explicit implementation choices: symmetric Gram estimates; raw Ghat/Khat/Hhat in residual estimators; exact PSD guard for repaired Gbar; each convex solve initialized at zero; rational fixed steps and certified FW gaps; bounded iteration cap; unique descriptor retention; permanent failure latch; binary reports (or a separately charged fixed dyadic alphabet). Actual supplied adjoints and paid physical preparation remain premises.

## Convex surrogate and projection accuracy

Let B=m, alpha=lambda/[128(b+4)b^2], b the next power of two. Symmetric entrywise Gram error has spectral norm <=m alpha, so Gbar=Ghat+m alpha I is PSD on the confidence event. Its nonconstant objective differs from the physical squared-distance objective by at most

    [(m+1)B^2+2B^2]alpha=(m+3)B^2 alpha.

The target H term adds B^2 alpha, giving the stated (m+4)B^2 alpha bound. If c has empirical FW gap <=delta=B^2 alpha, convexity gives empirical suboptimality <=delta. Comparing to a coefficient representing the exact physical projection yields physical suboptimality <=(2m+7)B^2 alpha. Projection's variational inequality then gives

    ||Vc-P_K(T_a Vd)||^2 <=(2m+7)B^2 alpha <=lambda/64.

The last inequality follows from 2m+7<=2(m+4) and m<=b. This requires no uniqueness of coefficients and no positive physical Gram eigenvalue. Projection is onto a compact convex physical image of a coefficient ball, hence exists and is unique as a physical vector even for a singular Gram matrix.

## Corrected output and actual residual bounds

All modeled coefficients remain l1-feasible, so ||y_i||<=B. With raw measured moments, the residual quadratic has total coefficient absolute weight <=4B^2. Thus estimated residual squared plus 4B^2 alpha dominates true residual squared and overshoots by <=8B^2 alpha. Do not silently substitute repaired Gbar into this displayed residual formula without changing its error ledger.

Exact forward Duhamel telescoping gives the scalar error as the sum of residuals paired with actual backward adjoint suffixes. Subtracting the explicitly evaluated correction <b_(l-i),r_i> leaves only the dual suffix approximation error. Contractivity of the true adjoints bounds that error by the corresponding sum of dual residual norms. This establishes the product certificate without orthogonality, a Galerkin equation, an interior margin, or linearity of the modeled operation.

The measured terminal pairing has error <=B alpha. Each correction has two bilinear terms of weight <=B^2, giving D=(B+2lB^2)alpha. The same coefficient estimates may be used adaptively: the simultaneous entrywise event certifies every feasible coefficient vector, so no additional union bound over optimization iterates or later accepted queries is needed.

Exact inflated residual norms are <=3B. For root enclosure width eta=epsilon/[128H^2(B+1)], each residual product gains at most 6B eta+eta^2. There are l(l-1)/2 such products. The proposed bound 3H^2B eta+(H^2/2)eta^2<epsilon/32 is correct. The empty word must use the physical seed self-return. The correction identity applies also at length one, where the product term is empty and the correction algebraically recovers the one-step return up to moment error.

## Rejection, witness selection, and logdet progress

Assume every physical forward and actual reverse-adjoint prefix lies within rho=sqrt(lambda) of K_m. Nonexpansiveness of physical metric projection, contraction of the true action, and projection solve error zeta<=rho/8 imply

    ||y_i-x_i||<=i(rho+zeta),
    ||r_i||<=(2i-1)(rho+zeta).

Residual confidence inflation is <=sqrt(8B^2 alpha)<=rho/8 (since b+4>=5). Hence R_i<=3i rho, and identically S_j<=3j rho. The identity sum_i i sum_(j<=l-i)j=l(l-1)(l+1)(l+2)/24 proves the stated product bound <=(3/4)H^4lambda. Also

    D <=(1+2H)lambda/[128(b+4)] <=3Hlambda/640.

With lambda=epsilon/(128H^4), data, product, and rounding terms sum to substantially less than epsilon/4. Therefore rejection implies a listed physical prefix has distance squared >lambda.

For a candidate prefix x, its self/cross entries have target mass one. The conservative U=(m+4)B^2 alpha remains valid. The convex FW gap gives

    L=qbar(c)-gap-U <=dist(x,K_m)^2,
    L>=dist(x,K_m)^2-2U-delta.

Here U<=lambda/128 and delta<=lambda/640, so 2U+delta<lambda/32. A rejected task therefore has a candidate with L>lambda/2. Only that weaker threshold is needed for retention; one must not claim every retained prefix has distance squared >lambda. Existing descriptors have distance zero, so cannot qualify on the confidence event.

The analytic ridge minimizer with ell_lambda(x)<=lambda/2 has coefficient l2 norm <=1/sqrt(2), hence l1 norm <=sqrt(m/2)<=m=B. Thus its physical fit is feasible, proving dist(x,K_m)^2<=ell_lambda(x)<=lambda/2. Contraposition gives ell_lambda(x)>lambda/2 for each retained witness. This proof does not evaluate or estimate a Gram inverse.

Each addition therefore raises logdet(I+G/lambda) by >log(3/2). Under the stated rank-r width promise nu<=sqrt(lambda)/4, the familiar orthogonal low-rank-plus-tail decomposition gives

    (log(3/2)-1/16)m <=r log(1+m/(r lambda))+log(3/2).

The proposed explicit ceiling M=1+ceil[64r log(8/lambda)] is SAFE. Indeed put x=m/r and L=log(1/lambda). For x>=16, log(1+x)<=x/4. Since lambda<=1, the right-hand logarithm is <=L+log(1+x). At x=64(L+log 8),

    (log(3/2)-1/16-1/4)x > L+log(3/2),

and the difference is increasing thereafter. This contradicts the displayed potential bound beyond that ceiling. No rank, gap, or spanner is supplied to the learner.

## Explicit rational solver and unconditional-work closure

The following is one deliberately conservative implementation, not a practical optimization claim. At each dictionary size initialize EVERY projection solve with c=0. Use the exact l1-ball linear oracle: if g is the empirical gradient, choose s=-B sign(g_j)e_j at a largest absolute coordinate. The gap is <g,c-s>. All operations are on scalar-derived coefficient coordinates, not hidden coordinates.

Because binary empirical matrix entries lie in [-1,1], ||Gbar||<=m(1+alpha)<=2m even off the good event. After the PSD guard passes, curvature on the l1 ball is at most C=16mB^2. The nonconstant objective ranges over an interval of length <=8mB^2. Use theta=delta/C=alpha/(16m) whenever gap>delta. Each such step decreases objective by more than delta^2/(2C). Consequently

    T=1+ceil(256m^2/alpha^2)

is a deterministic iteration ceiling by which gap<=delta must occur. A failed PSD guard or exhausted cap latches terminal failure. This argument uses neither an exact line search nor coefficient conditioning.

Since m<=b<2m and b+4<=6m,

    alpha>=lambda/(3072m^3),  T=O(m^8 lambda^-2).

Let n=W+1, W=sum_(j=0)^H k^j, and use beta=delta_stat/n^64. Let L_* include rational epsilon/delta_stat bitheight, any fixed report-alphabet bitheight, H log2(k+1), and log2(k+H+2), plus one. All matrix entries, alpha, theta, and empirical mean denominators have O(L_*) bits. The logarithm of n is already O(L_*); computing n does not enumerate its descriptors.

Writing theta=p/Q, an iterate initialized at zero has denominator dividing Q^t and O(T L_*)-bit coordinates. At fixed m the same Q is used by every solve, so previous-state coefficients and current iterate can share Q^max(t,t_previous); no horizon-exponential denominator growth occurs. Naive schoolbook exact gradient/gap/update arithmetic costs at most O(m^2 T^2 L_*^2) per iteration, hence O(m^2 T^3 L_*^2)=O(m^26 lambda^-6 L_*^2) per solve. There are O(H) forward, dual, and prefix-witness solves per rejected/acquiring stage and at most n stages. This yields W-degree at most 27 for the dominant solver work.

PSD tests, rational bilinear corrections and fixed-dyadic root bisection are polynomially smaller in W. In particular radicands bounded by 9B^2 use only O(L_*) bisections to absolute tolerance eta, on O(TL_*)-bit rational data. A deliberately loose total DIGITAL acquisition envelope is

    C(k+H+1)^2(H+1)^5 n^32(1+lambda^-1)^6 L_*^6.

The exponent 32 is an explicit conservative envelope for the derived degree 27, not the old inverse-model bound. Confidence beta=delta_stat/n^64 therefore suppresses the exceptional-work contribution to a polynomial in the remaining displayed parameters. Permanent failure and unique descriptors are necessary; request-local refusal followed by unlimited remeasurement would not justify this bound. Accepted-query computation is deployment work and is not claimed to have finite total cost on an infinite request stream.

For SOURCE jobs, precision-epoch caching is important: existing moment entries are remeasured only when b changes; new rows/columns and rejected-prefix tests add O((k+H)m) jobs per addition. Summing dictionary work over dyadic epochs and prefix scans over additions gives O((k+H)M^2) jobs, up to harmless bookkeeping/log factors. With alpha^-2=O(M^6lambda^-2), the claimed sufficient O((k+H)M^8lambda^-2 log(confidence^-1)) report count follows. Refreshing every old entry at every addition would instead add another M factor and should not be described by this sharper count.

Every report still pays stationary preparation, actual chronological descriptor controls (length at most H+1 per side for dictionary moments), endpoint reads, and failed/discarded episodes. No physical timing bound follows without those primitive costs. General bounded analog reports require a separately costed encoding/rounding interface; the digital proof here uses binary reports.

## Scope and relation to the governing earlier construction

N1515 already contains noisy bounded-l1 kernel Frank-Wolfe fitting and failed-successor retention. The specific mathematical changes here are the expanding m-times absolute convex hull, nonlinear requested-word rollout, measured dual-weighted correction, and analytic-ridge determinant progress. This receipt does not establish that their combination is historically new.

The rank-two invariant-polygon obstruction concerns a globally invariant UNIT hull and an exact l1-contractive linear intertwiner. It does not refute this construction: the feasible hull radius expands, projections are nonlinear/approximate, and only finite-horizon requested scalar outputs are certified. Conversely this construction does not claim to solve that exact invariant-polygon problem.

The width promise must cover actual forward and supplied-adjoint prefixes within the fixed horizon. No new readout, guessed adjoint, systematic bias, source drift, growing horizon, general scientific planner, or upfront recognizable all-word closure is included. Within these boundaries, the mathematical source-shot improvement survives this independent audit.
