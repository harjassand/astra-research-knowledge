# Candidate global extension with a genuine fast siphon and physical seeding
Status: NEW UNREVIEWED personal synthesis. The frozen pure-source family theorem is unchanged. This extension must not inherit its review verdict.

## Exact proposed family
Use the contract in GENERAL_A_CATALYTIC_OCCUPATION_CANDIDATE.md: homogeneous degree-m strongly connected fast graph, all complexes containing A, containing mA and A+(m-1)X_i for every reservoir species, and a positive A-increasing edge from each latter source. Common catalyst qB, q>m>=2. Add0->A+B->mA+qB->0. All coefficients fixed positive.

The fast subsystem has an actual A=0 siphon. No fast clearing bound is claimed there. Physical connector immigration is explicitly responsible for seeding it. The target conclusion would be the same nonexplosion, classwise positive recurrence and all exponential total-count moments as the frozen theorem, but it remains unreviewed.

## 1. Local estimates supplied by actual drift
For active large-N starts, the occupation candidate derives

    T<=C logN/N^(m-1),
    T<=epsilon_N U,  epsilon_N=C N^-gamma logN,
    gamma=(m-1)/(2m),

where T is time and U is A-occupation until the first clearing/competing birth, after restoring the appropriate catalyst scaling. At the fixed section B=q, constants absorb that fixed factor. Clearing-first probability is1-o(1); its output inverse-mth moment is at most CT. Later worst-case reset moments are at most

    p_0=C logN/N^(m-1).

The estimates are uniform over active compositions. Active-state access is not silently extended to A=0.

## 2. A relative first-reset estimate closes the N-directed section
Use the same N residual r=N-H(B), with h=q-m, and section S={B=q,A>=1}. Every actual low-phase activation entering B=q has A>=m, so this section is naturally reached without an imposed equilibrium law.

Let t be the FIRST clearing-reset inverse moment for the incoming section state, so t<=CT_*. Let p_0 be the later worst-case reset bound. A first-run decomposition gives

    upward/bad low escape
       <=Ct+C sum_(ell=1)^(m-1)t^(ell/m)p_0^((m+1-ell)/m). (1)

The first run of zero immigrations activates directly back to S. A run of at least m costs O(t). A shorter positive run followed by reset must climb again, producing the extra p_0 power. Subsequent reset walks are exactly the phase-dependent positive-kernel argument from the frozen family, with p_0 in place of p.

The true activation opportunity at the section is proportional to U_*. Also U_*>=cN^(-(m-1)) by pointwise activation/clearing hazard comparison and clearing-first probability1-o(1). Hence (1), divided by U_*, is O(epsilon_N): for lambda=ell/m,

    t^lambda p_0^(1+1/m-lambda)/U_*
      <=C epsilon_N^lambda (p_0/N^(-(m-1)))^(1-lambda)p_0^(1/m)
      =o(epsilon_N).

Immigration-first probability at the section is also at most C epsilon_N times the activation opportunity. Choose alpha h<gamma. Then epsilon_N r^(alpha h)->0, so the actual weighted return argument retains a negative margin at least c r^(-(m-1))phi(r), even though the absolute mean is not a strict power smaller than N^(1-m).

This is a relative occupation comparison, not the invalid replacement of a composition-dependent activation rate by N.

## 3. New inactive-output branch in actual repair
In the old pure-source family, sufficiently large N guaranteed all compositions active. Here a clearing can leave A=0 at high B. Treat that as a NEW bad-output branch, not as another active fast episode. Its probability is <=Cp_0 because (1+A_after)^-m=1 at A_after=0.

At high N, one actual immigration from A=0 waits a constant mean time and turns activity on. It can raise r by at most h. Therefore the inactive-seeding branch has weighted repair factor at most C p_0 r^(alpha h), which tends to zero. It is included alongside the old active bad-immigration branches. An arbitrary initial high-N A=0 state pays this seeding cost once, giving the same allowed polynomial r^(alpha h) initial factor.

Fresh low-phase laws have beta_0=p_0^(1/m), so their repair up factor is beta_0 r^(alpha h)->0 when alpha h<gamma<(m-1)/m. Thus the composed repair kernel is still contractive. Physical seeding time is included in the running cost. The section remains pointwise in the full ACTIVE incoming composition; the initial A=0 case is handled before entering it.

## 4. Complementary activity-credit value without pure reservoir sources
Let I indicate an enabled fast composition source and Z=B-N-hI. Fast transitions preserve I; inactive activation lands active through pure mA. For all sufficiently large N, inactive states are exactly A=0, and immigration immediately turns activity on, producing a downward Z jump.

The normalized clearing mean is uniformly bounded over active states. The killing compensator and A<=C[1+(A)_m] give uniformly bounded A-occupation as well. Therefore, for B>=q,

    P(activation before clearing)<=C B^(1-q),
    P(immigration before clearing)<=C B^-q,

uniformly in the unbounded hidden N. A large active state clears with probability1-o(1). If its target stays active, Z goes down. If it lands inactive, then for large N it has A=0 and the next immigration goes down after constant mean time. Thus large N has a near-one downward block. The only remaining inactive A>=1 states have bounded N and use the same finite-head forced-immigration protocol as before.

This yields the same uncapped Z-exit bounds and stopped value. No finite cap or assumption of a closed inactive background is used.

## 5. Conditional global coupling and outstanding verification
If the local logarithmic/occupation proof, refined first-reset bound, and new active/inactive repair kernel above pass review, the two actual values have the same residual geometry and threshold leak bounds as the frozen theorem. Their sum then gives the same global Foster and moment conclusions. Nonexplosion via L(1+N+B)<=C(1+N+B) is unchanged because fast reactions preserve N,B and the connector is unchanged.

This file is a candidate for that extension, not a completed proof review. The exact new obligations are the relative reset estimate under the actual stopping kernels, inclusion of every inactive seeding branch, and the pointwise section-cost argument after the new conditioning. General weakly reversible recurrence remains open, as do fast graphs without the explicit A-production source coverage.
