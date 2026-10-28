# Independent algebra and finite-cap review of the bounded-matrix terminal refinement

28 October 2026. Auditor: `producer-workspace/audit_algebra_extraction`.

This note reviews the separate refinement of the frozen rational-C base protocol. It does not modify the base, assert that a Frobenius majority estimator has the new rate, or claim a new matrix concentration theorem. The bounded matrix-Bernstein inequality is received through a separate primary-source review. All calculations below concern the actual Bernoulli matrix Y=y||Cz||^2 T(z), not a supplied matrix observation.

## 1. Noncommutative operator variance and range

Let F=CAC, with the same rational polynomial C and the same exact projective design as the base. Conditional on a good prior envelope A<=B,0<=F<=CBC<=I and s=||Cz||^2<=1/tau. Define

    S_m=m^2(m+3)/4, R_m=m(m+1), P_m=2S_m+R_m.

Directly squaring T=alpha P−bI, with alpha=m(m+2)/2,b=m/2 and E P=I/m, gives E T^2=S_m I. Because each T^2 is PSD and the scalar coefficient s(z^TFz) lies in[0,1/tau],

    E Y^2=E[s(z^TFz)T^2]<=(S_m/tau)I.

No F/T commutation is required. Also

    E(Y−F)^2=E Y^2−F^2<=(S_m/tau)I,
    ||Y−F||<=m(m+1)/(2tau)+1<=R_m/tau.

The centered range holds for all m>=1 and0<tau<=1. It is a conservative operator-norm bound on the centered summands, not a mistaken substitution of the uncentered range.

For N independent centered Hermitian matrices, the received bounded Bernstein inequality applied to both signs gives

    Pr(||Fhat−F||>delta)
       <=2m exp[−N delta^2/(2S_m/tau+(2/3)R_m delta/tau)].

With0<delta<=1, L=ceil log2(4mH/beta) and

    N(tau,delta)=ceil[P_m L/(tau delta^2)],

this is at most2m exp(−L)<=2m 2^(−L)<=beta/(2H). Uniformity over a fixed legal prior envelope permits conditional first-failure union bounds over adaptive stages. Independence across different learned envelopes is neither true nor needed. The new estimator is a rational arithmetic MEAN, not the base majority rule.

## 2. The relative regime epsilon<gamma

Choose

    J=ceil log2(gamma/epsilon), H=J+1,
    tau_j=2^(−j), c0=1/16, delta0=1/64.

Each coarse stage uses one Bernstein mean at delta0, then the exact base reconstruction, largest-dyadic update grid and PSD accept/abort guard with c0. The frozen base invariant proof therefore gives

    A+tau_j I<=B_j<=(8/7)A+2tau_j I.

At the endpoint,

    epsilon/(2gamma)<tau=tau_J<=epsilon/gamma.

The procedure has paid only constant accuracy in these coarse stages. It has not retained the base's unnecessary gamma-level estimation at every tau scale.

Freeze B_J, build its rational C, and take an independent terminal average with delta=gamma/64. Exact reconstruction M=C^(-1)Fhat C^(-1) gives

    −2delta B_J<=M−A<=2delta B_J.

There is no PSD projection of M and none is needed. For every real unit x, put p(x)=x^TAx. The uniform invariant implies

    |x^T(M−A)x|<=u p(x)+v,
    u=gamma/28, v=gamma tau/16.

Indeed2delta*(8/7)=gamma/28 and2delta*2tau=gamma tau/16. If the finite known-matrix eigensolver returns x with Rayleigh slack zeta=epsilon/16 for M, compare x against an actual minimizer of A:

    (1−u)p(x)<=(1+u)p_*+2v+zeta.

Both appearances of v are required; omitting one would be an incorrect eigenvector-transfer argument. Since u<=1/28 and v<=epsilon/16,

    (1+u)/(1−u)<=1+2gamma/27,
    (2v+zeta)/(1−u)<=(3epsilon/16)/(27/28)=7epsilon/36.

Thus p(x)<=(1+2gamma/27)p_*+7epsilon/36, which is stronger than(1+gamma)p_*+epsilon/4. The eigensolver may handle an indefinite M; no fitted minimum-eigenvalue gap or source spectral floor has been introduced.

## 3. The additive regime epsilon>=gamma

Use the explicitly different direct experiment C=I, x=z, Y=yT, so E Y=A. The same bounded moments hold with tau=1. With one mean at delta=epsilon/16 and one known-matrix minimum Rayleigh computation with slack epsilon/16,

    p(x)<=p_*+2delta+epsilon/16=p_*+3epsilon/16.

This costs O(m^3/epsilon^2), no larger than O(m^3/(gamma epsilon)) when epsilon>=gamma. It is important not to force an unnecessarily expensive gamma-precision terminal batch in this regime. The direct branch is separately defined and does not mix C-query weights with exact-square-root controls.

## 4. Finite source ceilings

For epsilon<gamma,

    sum_(j=0)^(J−1)tau_j^(-1)=2^J−1<2gamma/epsilon,
    tau_J^(-1)<2gamma/epsilon.

Each coarse accuracy has inverse square4096, and the terminal inverse square is4096/gamma^2. The ceiling contribution is one per estimate, hence

    T_coarse<=J+8192P_m L gamma/epsilon,
    T_terminal<=1+8192P_m L/(gamma epsilon),
    T_total<=H+16384P_m L/(gamma epsilon).

The last line uses gamma<=1. For epsilon>=gamma,

    T_total<=1+256P_m L/epsilon^2
            <=1+256P_m L/(gamma epsilon).

The confidence union costs at most beta/2 for the reference matrix events. Every executed call on an aborted history remains charged. A payload call is additional to these TRAINING bounds. Since P_m=(m^3+5m^2+2m)/2, the selector rate is O_tilde(m^3/(gamma epsilon)); no optimality lower bound is claimed.

## 5. Finite controls and end-to-end scope

All native controls are inherited with the NEW deterministic count ceiling. The coarse c0 update uses the corresponding largest permissible dyadic grid and exact PSD guard. Terminal reconstruction is a one-time rational calculation, so it does not introduce unbounded repeated bit growth. The base series satisfies C>=I/2 on every legal history; every Y has norm at most m(m+1)/(2tau), so

    ||M||<=2m(m+1)/tau

on EVERY terminal record history, whether or not the statistical bound holds. A certified gap-free minimum Rayleigh routine thus has a fixed known arithmetic/precision cap even for indefinite, statistically bad M. The final real-unit-vector state preparation is approximate and charged in the whole-process control budget.

Finite integer/sign samplers, dense selector synthesis, global logical test circuits, the frozen receiver and payload controls must all use the new complete horizon in their discrepancy allocation. Polynomial selector dimension does not imply poly(log m) amplitude preparation; the known O(m) rotations remain. The independent matrix batches are conditional reference experiments; finite physical errors are transferred through the separately paid whole-process channel/record discrepancy, not hidden in the Bernstein event.

Only the selector primitive in Section7 of the frozen base is replaced. The NEW m-anchor rho, margin and weighted-locality promises remain; regret still transfers by m, with the same sharp boundary witness. Its decoder eta, structural approximation floor, final Bell-risk conversion, acquisition failure allocations, complete input/output traffic and final payload remain unchanged. The stronger selector event has more additive reserve than the base requires. Finite-time physical widths must still suppress the full m q A_geom tail and pay4^w; no old constant-width or linear-m/q statement is restored.

## 6. Exact independent evidence

`growing_selector_bernstein_refinement_independent_check_20261028.py` performs no random sampling or source calls. It exactly checks:

- eight rational-C moment fixtures with m=1,...,4 and tau=1,1/2, including noncommuting A/B, both centered range cases and Loewner operator-variance inequalities;
- twelve terminal eigenvector examples, including four indefinite raw M matrices, eight noncommuting A/M pairs and degenerate true effects;
-72 exact ceiling/confidence cases,24 relative and48 additive, and the rational7/36 constant.

These are prescribed operator/matrix tests and analytic expectation sums, not acquired count performance or a numerical verification of the primary concentration theorem. General confidence and complexity are proved analytically above. Earlier frozen sources and evidence remain unchanged.
