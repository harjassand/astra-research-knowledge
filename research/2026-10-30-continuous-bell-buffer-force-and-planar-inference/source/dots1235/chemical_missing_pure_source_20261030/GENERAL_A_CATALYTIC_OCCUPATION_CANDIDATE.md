# General A-catalytic occupation comparison beyond pure-source coverage
Status: NEW PERSONAL DERIVATION, unreviewed. Separate from the frozen fast-connector theorem. No whole-chain recurrence conclusion yet.

## Graph contract
Fix k>=2,m>=2. The fast composition graph is finite, strongly connected, homogeneous of degree m, and EVERY complex contains at least one A. It contains mA and every A+(m-1)X_i, i!=A. From each latter source there is at least one positive-rate edge increasing the A count. All constants are fixed positive. A common qB catalyst and clearing at k_D(A)_m may be added, with q>m.

Fast moves preserve A>=1, but A=0 is a genuine inactive siphon on the fast subsystem. At large N every composition with A>=1 is active: if A<m, some reservoir species has at least m-1 copies, enabling its A+(m-1)X_i source. Thus high-N inactive states are exactly A=0, and one ACTUAL connector immigration activates them. No deterministic positivity from the A=0 face is claimed.

## Uniform logarithmic drift on the active class
For A=a<=epsilon N, one reservoir species has a positive fraction of N. Its designated A-increasing source supplies positive L log A drift at least cN^(m-1): its rate is >=c aN^(m-1), and its bounded positive A jump has logarithmic increment >=c'/a.

Any A-decreasing edge has source A multiplicity at least2, because all product complexes still contain A. Its logarithmic increment has magnitude <=C_m/a, and its rate is bounded by C a^u N^(m-u), u>=2. Summing negative contributions gives at most C aN^(m-2). Choose epsilon small. Then

    L_fast log A>=cN^(m-1) on a<=epsilon N,
    |L_fast log A|<=CN^(m-1) globally on the active class.

The latter bound uses that every source contains A: total rate<=CaN^(m-1), while logarithmic jumps are O(1/a), including finitely many small-a cases.

With W=2log(N+1)-log A, killing dominates the possible O(N^(m-1)) positive drift when A>=epsilon N. Therefore

    sup_active E tau_clear<=C log N/N^(m-1).              (1)

This is an actual killed drift bound and permits arbitrary conservative composition classes; it does not require mixing among reservoir species.

## Relative occupation, not an absolute strict-power mean
Let gamma=(m-1)/(2m) and K=floor(N^gamma). Log drift gives active hitting time of A>=K at most ClogN/N^(m-1). Before that time clearing hazard is at most CK^m, so clearing before this mesoscopic hit has probability O(K^m logN/N^(m-1))=o(1).

From the first mesoscopic hit, A lies in[K,K+m]. On a time interval c/N^(m-1), before leaving[K/2,2K], total fast rate is at most C K N^(m-1). A bounded-jump/Markov estimate with small c gives probability at least1/2 of staying in that interval; killing probability is o(1). Thus

    E integral_0^tau A_t dt >=c K/N^(m-1)

for every active initial A<=K. Combined with (1), this yields T/U<=C logN/K there. From A>K, stop at killing or first A<=K; prior occupation satisfies U_pre>=K T_pre, and the bounded jump lands in[K-m,K], where the same lower bound holds. Strong Markov therefore gives uniformly over ALL active starting compositions

    T(x)<=C N^-gamma logN * U(x),                         (2)

where T=E tau, U=E integral A dt.

## Actual connector competitors
Restore (B)_q and add immigration and activation as competing killing events. Bounds (1)-(2) remain valid uniformly B>=q: below the mesoscopic level their added hazard is at most C(1+KB), whose integral before hitting K is o(1); the dwell interval has the same small added hazard. Added killing only improves the mean upper bound. Thus (2) applies to T_*,U_* stopped at the first of the three actual connector events.

One also needs clearing-first probability to tend to one. The killing compensator gives E integral(A)_m dt<=C after removing the catalyst factor, and A^m<=C[(A)_m+1]. Hölder for the occupation measure gives

    U<=C T^((m-1)/m)(1+T)^(1/m)=o(1)

uniformly in active composition as N grows. Hence activation-before-clear is at most C B^(1-q)U=o(1), and immigration-before-clear is at most C B^-q T=o(1), uniformly B>=q. This is not obtained by the too-crude bound A<=N when m=2.

## Why the refined first-reset comparison matters
At the N-directed section B=q, let t be its first clearing-output inverse-m-th-moment bound and p_0=C logN/N^(m-1) the later worst-case reset bound. The first-run decomposition from RELATIVE_OCCUPATION_GAP.md gives

    P(upward/bad low walk)
      <=C t+C sum_(ell=1)^(m-1)t^(ell/m)p_0^((m+1-ell)/m).

Here t<=C T_* and the actual activation probability is proportional to U_*. Pointwise hazard comparison still gives U_*>=cN^(-(m-1)); (2) gives T_*/U_*<=C N^-gamma logN. These inequalities make the whole displayed escape bound a vanishing power times the ACTUAL activation opportunity, not merely a bound compared to a worst-case N^(-(m-1)) lower estimate.

## New repair obligation that must not be hidden
A neutral clearing at high B can now land at A=0, where the next immigration is CERTAIN, not an O(p_0) fast competition. Its occurrence is rare because the reset inverse moment bounds its probability by O(p_0), but its physical continuation must be included as a new inactive-seeding branch. From such a state, one actual immigration waits a constant mean time, can raise the N-directed residual by h, and then activates the fast graph. Its weighted cost is at most a polynomial factor r^(alpha h), not zero.

The old repair proof therefore cannot simply be copied unchanged. A new active/inactive-seed kernel, the relative section-return bound, and the complementary uncapped trace must be written and checked before any global extension is claimed.
