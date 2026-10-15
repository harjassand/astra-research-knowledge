# Independent audit of the sharp variance dual certificate

Audit status: **PASS as an internal mathematical audit, after one explicit endpoint clarification.** No critical defect was found. This is not formal verification, external review, or historical priority clearance.

Audited author source: `workers/quantum_extremal_astra/GLOBAL_OPTIMALITY_PROOF.md`. The exact reviewed snapshot is saved in `sources/AUDITED_GLOBAL_OPTIMALITY_PROOF.md`, SHA256 `0c2c0a5d20e240f004fe9085aea4595e530ba486b9e66d1d56c184238f97408b`; acquisition receipt is `DUAL_AUDIT_INPUT_RECEIPT.json`. It includes the endpoint estimate requested during this audit. My own construction was frozen before reading the author source; that provenance is in `INDEPENDENT_FREEZE_RECEIPT.json`. Agreement is not being used as evidence for the dual argument.

## Result supported by the audit

Let G be the plateau renewal profile in my independent proof: G=1 on [0,2], `2(s−1)G'=−G−G(s−2)` for s>2. Put `K=∫[1,∞)G`, `c=(4K+2)^−1` and

`v_*=23/9−2c/9`, approximately 2.533766978.

For every positive scalar radial law ν on R^3 with finite variance, if a positive normalized qubit POVM satisfies

`hat M(t)=hat ν(t) exp(i t·σ)` for every t,

then `Cov(ν)=vI` has `v≥v_*`. The explicit plateau scalar-noise law attains the bound and has every exponential moment. Thus the all-exponential-moment radial optimization has the same minimum as the larger finite-variance class.

For arbitrary scalar noise of finite covariance, first translate ν and M to center the noise, then twirl both under SO(3) and the spin representation. The contract and positivity survive, and the scalar covariance becomes `(tr Cov ν/3)I`. Therefore `tr Cov ν≥3v_*`. This is an average-variance lower bound; it is not a matrix inequality `Cov ν≥v_*I`.

## Kernel and renewal identity

Write `a(t)=d(t)^−1`, with d as defined in the author proof. Then `a'=((1−e^(−2t))/(2t))a` and `a(0)=1`. For r>0, integrating `r exp(−rt)a` by parts gives exactly

`2r ell(r)=1+∫[r,r+2]ell(u)du`.

The upper boundary is zero because a(t) grows only like sqrt(t); the lower boundary is precisely 1. Differentiating this identity gives `2r ell'+3ell=ell(r+2)`, with the sign and coefficient 3 correct.

The exponential-integral formula gives `a(t)=e^(γ/2)sqrt(2t) exp(E1(2t)/2)`. Subtracting its sqrt(t) leading term leaves a function with every polynomial moment integrable. Consequently

`ell(r)=Q/(4r^(3/2))+B0+O(r)`, `3B0=ell(2)`.

The extra constant relation follows from the differentiated renewal identity. It verifies the stated cancellations in U and V.

The Laplace transform of the triangular forcing in the plateau renewal equation is `(1−e^(−t))²/t²`. Solving the transformed first-order equation with the boundary at +infinity yields

`K=(1/2)∫[0,∞)(1−e^(−t))²/[t²d(t)] dt`.

The same expression is `∫[0,1]w(s)ds` by Tonelli. Integrability is O(t^−3/2) at infinity and bounded at zero. Hence the normalization of f, `∫[0,1]f=0`, is exact.

## Multiplier positivity

I independently differentiated the expressions for U and V using only the renewal identities, and recovered equations (17) and (18).

For U, the singular terms in `F+4cr²ell` cancel; its derivative is

`r[(1−r)(2−r)+c]+cJ(r)+2cr ell(r+2)>0`.

Its limit at zero is 0, so U is strictly positive. For V, let `G_*=F−2r f(1−r)`. Its derivative divided by r has derivative bounded below by

`15−14r−(5/2)c[−ell'(1)]>0`.

The strict bound is justified without numerical quadrature: `c<1/8`, and

`−ell'(1)≤(e/2)[1+3sqrt(π)/4]<16/5`.

For example, e<68/25 and sqrt(π)<1773/1000 give the rational upper bound 158423/50000=3.16846<16/5. The threshold product `(5/2)(1/8)(16/5)` equals exactly 1. Since 15−14r>1 for 0<r<1, the required derivative is strictly positive.

Both endpoints of G_* are zero. Therefore its derivative has one sign change from negative to positive, and G_*<0 inside; this proves V>0. The monotonicity argument is sound and does not infer positivity from sampled values.

## Endpoint cancellation and the requested clarification

At zero, `F=−cQ sqrt(r)+O(r²)`. The r^−3/2 terms in U and V cancel. Substituting `B0=ell(2)/3` gives

`U(0+)=V(0+)=1+c/2+(2c/3)ell(2)>0`.

At the other central endpoint, w(s)=2ell(1)s+O(s³), so with `a0=1−c−2c ell(1)`,

`f(s)=a0 s+O(s³)`, `F(1−s)=−a0 s²/2+O(s⁴)`,

and `V(1−s)=O(s)`.

The first proof version said only that V was bounded and vanished at 1. That wording did not by itself prove the claim that all expanded integrals are controlled by `∫(s+s³)h`; the reflected term contains `h(1−r)`. I requested the linear endpoint estimate. It was added before the audited snapshot was saved and closes this issue. No construction or multiplier changed.

## Exact adjoint identity and absolute integration

The polynomial part of P gives the cubic target plus a constant discrepancy. The ell contribution supplies exactly that missing constant using `2r ell−∫ell=1`.

For 1<s<2, the correction `ψ=F/(3r²)` cancels against V via

`∫[r,1](V−ψ)=−2rψ`.

For 0<s<1, the correction is `−2r(ψ+V)=−(4/3)f(s)`, exactly the negative of the central polynomial-plus-kernel residual. This verifies the coefficient identity on all three intervals.

One must not globally separate U into P and ψ near r=0: each piece is singular. The proof correctly expands the original bounded U and V first; it uses the split only pointwise for fixed s≠1, where the integration endpoints stay positive. There is no unrecorded integration of the singular pieces across zero.

All original expanded terms are absolutely integrable. U is bounded at zero and O(r²) at infinity; V is bounded and vanishes linearly at 1. The interval integral kernel has length 2min(s,1), and the reflected V term is O(s) at scalar radius zero. Every term is therefore bounded by a constant times `∫(s+s³)h`. Fubini is valid under finite scalar variance; no exponential tail is required for an arbitrary competitor.

Positivity of both multipliers and both radial eigenvalue slacks then gives the sharp lower bound. Both slacks vanish for the explicit plateau construction, so the lower bound is attained.

## Singular laws, finite variance, and twirling

Gaussian smoothing of ν and M preserves positivity and the exact scalar multiplier identity. Its covariance charge is εI, so application to the smoothed law gives `v+ε≥v_*`, and letting ε decrease to zero extends the result to singular radial laws.

The construction of the polar densities q,b from smooth positive M and the projection identities uses only q integrability and |b|≤q for every r>0. It does not require a separate second-moment theorem for M. The integrals of s h and s³h are obtained directly from the smoothed scalar law ν. Thus the author proof's optional characteristic-function moment lemma is unnecessary; the finite-variance extension follows already from the preceding argument.

For nonradial laws, center first. Twirling without centering would replace covariance by the average second moment and add the squared noise mean. With centering, the trace covariance is preserved exactly. This closes the claimed anisotropic average-variance corollary.

## Smooth attainment and operational scope

The same dual certificate also settles the smooth-density question. Equality for smooth radial h forces both slacks to vanish pointwise, because U,V are strictly positive. On the central interval their sum forces `h(1+r)=h(1−r)`, and differentiation of the saturated renewal relation then forces h to be constant on (0,2). A scalar spatial density smooth at the origin has `h(s)=2πs p(s)→0`; hence that constant would be zero. The tail renewal relation would then force h≡0, contradicting normalization. Therefore every smooth scalar density has v>v_*, although Gaussian smoothing of the attaining law approaches v_*.

The optimal measurement is ordinary covariant spin followed by independent radial randomization, with R≥1. The direction can be recovered exactly from the output, so the experiments are equivalent. Sharp scalar-convolution variance is not increased quantum information or a better ordinary linear decoder. Finite-bit sampling, control synthesis, device errors and historical novelty remain separate open gates.

## Verification artifacts

`check_dual_algebra.py` checks the exact derivative identities, outer and central polynomial adjoint identities, and rational positivity constants. It supports the hand audit; it does not formally verify measure theory, Laplace transforms, asymptotic estimates, or historical priority. No numerical LP optimum was used to establish the audit verdict.
