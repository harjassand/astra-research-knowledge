# An actual phase-corrected head and tail-feedback construction
Status: NEW UNREVIEWED v2 extension (non-complex-balanced rate choice). This is a mechanism test on a modified graph, not a novelty claim or general recurrence result. Frozen v1 is unchanged.

## Network and exact scalar failure
Retain unit-rate connector 0 -> A+B -> 3A+4B -> 0. Replace the old fast chain by the bidirectional triangle on cubic A-counts 0,1,3, all with +4B:

    3C+4B <-> A+2C+4B <-> 3A+4B <-> 3C+4B.

All fast constants are one EXCEPT 3C+4B -> A+2C+4B, whose constant is two. The earlier all-unit mechanism test is complex balanced at A=C=B=1 and supplies no new recurrence example. This version deliberately removes that shortcut: fast complex-balance weights have ratios pi_1/pi_0=5/3 and pi_3/pi_0=4/3, incompatible with the required monomial ratios a/c and (a/c)^3. The connector contributes zero net fast-junction flux at a complex-balanced point, so it cannot repair this incompatibility. N=A+C; g_N=4 floor(N/3)+(N mod3); s=B-g_N. At (A,C)=(2,1), no fast source or clearing is enabled. Activation has rate 2B and increases s by one; immigration has rate1 and preserves s. First-up probability is at least2B/(1+2B)->1. The previous scalar first-exit lemma is genuinely unavailable.

## Fixed head and phase normalization earned from exact algebra
Take head N<=5 (21 states). Its seven fast-inactive phases are

    (0,0),(0,1),(1,0),(0,2),(1,1),(2,0),(2,1).

Set eta(0,2)=-1, eta(2,1)=1, eta=0 otherwise, and corrected head coordinate r=s+eta(A,C). This is NOT an asserted invariant on the tail.

A head birth exiting N<=5 lands at N=6 or7. Suppress further births until the next clearing and return to N=3 or4. On these fixed fibers, fast conversions and clearing have exactly the same (B)_4 factor. Their absorption probability matrix P_N is a constant rational matrix, computed by (-Q_N)^(-1)K_N. Every row sums to one. This is a birth-SUPPRESSED upper bound on the actual zero-birth return kernel, NOT that actual substochastic kernel.

Compress only these exterior excursions, retaining ALL actual reactions within the head. For each resulting gain, use corrected residual increment delta (including eta of the terminal phase), and multiply its gain by t^delta times2 when delta!=0, with t=r^alpha. Keep original outgoing losses. Source B is r+g_N-eta. Let G be this inflated finite-head matrix.

Solve

    -G v=f,  f_j(r)=r^2 on fast-active phases, f_j=1 otherwise.

The fast-active forcing is deliberately stronger; it will pay for actual omitted-birth feedback at precisely the phases from which the tail can be entered.

## Exact leading certificate and its two-scale justification
`exact_holey_head_nonbalanced_slack.py` uses z=1/r and keeps t symbolic. Row-scale active equations by z^4, inactive A>0 equations by z, and inactive A=0 equations by1. The active leading block is a fixed invertible killed fast matrix. Its exact Schur complement on the seven inactive phases has determinant

    z^2 (3494/3653)(1-2/t) + higher z orders.

The seven Cramer numerators have leading z order0, with coefficients 20/13 for the first six, and

    4480/3653 + 2280/(3653 t)

for the last phase. The physical r^2 active forcing does not change these coefficients. Exact output is HOLEY_NONBALANCED_HEAD_EXACT.json.

These are finite algebra, not floating-point eigenvalue tests. The full row-scaled 21x21 matrix is polynomial in z and Laurent polynomial in t, with per-entry t degree between -1 and1. Full determinants thus have t exponents between -21 and21. The leading fast determinant is constant and positive. Therefore choosing, for example, 0<alpha<1/43 makes every additional z power dominate any competing t-power advantage, and the displayed positive leading terms remain leading along t=z^(-alpha). All inactive v_j are positive and asymptotic to positive constants times r^2. The active block is a Metzler-transient fast perturbation; its inverse is nonnegative for large r, and its coupling to inactive phases is nonnegative after moving terms to the right. Thus active v_j are positive and O(r^2) too.

Choose alpha rational and also below the other bulk requirements. Each v_j is rational-Puiseux, so fixed shifts have ratio1+O(1/r). Use

    phi(r)=Gamma(r+1)^alpha exp[(log r)^(1+p/2)],
    H_j=phi(r)v_j(r),   0<p<1.

The tilt has fixed-shift ratio1+o(1); factor2 absorbs all actual nonzero-shift errors. Zero corrected shifts have no error. The birth-suppressed compressed physical generator therefore satisfies

    L_supp H <= -r^2 phi(r) on active head phases,
    L_supp H <= -phi(r) on inactive head phases.

## True tail extension and quantitative incoming feedback
Use the actual polylog cap N<=L(s)=floor((log s)^p), with a sufficiently large fixed s threshold. Every conservative fiber N>=4 reaches clearing: some enabled fast complex is present, and its complex path reaches 3A. The number of shell states is N+1, so the crude finite-graph bound is exp(CN logN)/(B)_4. Taking p<1 gives tail first-birth probability s^(-3+o(1)) and tail stopping time s^(-4+o(1)), uniformly up to the cap. No mixing estimate is used.

Define W=H on the fixed head. On the actual tail, define W as the expected terminal H at the first head return, plus the integral of phi(s_t), stopped also at actual cap exit or the low-s threshold with terminal zero. Weighted renewal, in weight psi(s)=(1+s)^(2+alpha)phi(s), proves finiteness and

    W <= C s^(2+alpha)phi(s),
    LW=-phi(s) on the tail.

For a head-to-tail entrance, the zero-birth terminal term is bounded ABOVE by the birth-suppressed kernel already in G. Returns containing at least one competing birth contribute at most

    s^(-3+alpha+o(1)) psi(s)
       = s^(-1+2alpha+o(1)) phi(s).

Tail running cost adds only s^(-4+o(1))phi(s). Every head-to-tail jump originates at N=4 or5, hence in an active phase with eta=0. Its rate is O(s), and its ORIGINAL residual shift is nonpositive (N4 activation:0; N5 activation:0; N5 immigration:-1). Thus the full additional head forcing is at most

    s^(2alpha+o(1))phi(s) = o(s^2 phi(s)).

It is absorbed by the deliberately earned active-head margin. Inactive head phases have NO direct tail exits, so their weaker margin is untouched. This closes actual tail feedback; it does not replace a physical exit by killing or assume a reflecting boundary.

## Global cap matching and scope
The extension W is zero outside its actual capped domain. Only clearing can enter the large-s cap from outside, through its fixed-width N collar. The same quantitative factorial separation B-s=g_N~4N/3 makes its polynomial-profile incoming forcing negligible against the existing factorial F on that collar. The old low-B connector construction and controlled r=N-h_B certificate depend only on the connector and preservation of N,B, so they remain available.

For the modified fast triangle, the required extreme-composition negative F drift must be explicitly checked rather than inherited numerically: its homogeneous fractional-factorial fast functional is strictly negative near A/N=0 or1, because the pure endpoint complex has positive outflow and every other source vanishes in that limit. Falling-factorial boundary errors are lower order uniformly, while the previously earned low-B clearing-return error is O(A^(3-delta)). Balanced high-B drift follows from the same finite-complex bulk lemma with a possibly smaller alpha. These statements give the same two extreme cones and entropy coupling, but await full review for the modified graph.

The significance is the joint mechanism: an exact finite matrix supplies phase offsets and places a stronger margin on the actual entrance phases; a true weighted tail-return estimate then pays the omitted births. This is not a claim that arbitrary heads admit such a matrix sign or that arbitrary networks have the needed resource order and collar gap.
