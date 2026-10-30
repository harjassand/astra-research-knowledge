# Uncapped recurrence for a homogeneous fast-connector family

**Frozen theorem candidate, 2026-10-30. Fresh separate whole-proof review pending.** The new local components have child adversarial audits; that is not the same as the completed separate whole review of the older fixed network. No publication or novelty claim. This is NOT the general weakly reversible chemical recurrence conjecture.

## Exact theorem statement under review
Fix integers k>=2 and q>m>=2. Composition species are X_1=A,X_2,...,X_k; B is an additional resource species. Let C be a finite set of nonnegative integer composition complexes of total order m, containing every pure complex mX_i. Let E be a strongly connected directed graph on C, with distinct source/target complexes (self-loop-only or isolated vertices are not used). For each edge y->y', include

    y+qB -> y'+qB.

Add the three connector reactions

    0 -> A+B -> mA+qB -> 0.

Every reaction has an arbitrary FIXED positive mass-action rate constant. The propensity of y+qB->y'+qB is k_e product_i(x_i)_(y_i) (B)_q; connector propensities are k_I, k_T A B, and k_D(A)_m(B)_q. No stochastic averaging, equilibrium distribution, uniform mixing gap, globally supplied barrier, or time-dependent/state-dependent coefficient control is assumed.

**Candidate conclusion:** the full continuous-time chain on nonnegative integer populations is nonexplosive from every state. Every closed communicating class is positive recurrent. For its unique class invariant law pi and every theta>0,

    E_pi exp[theta(N+B)] < infinity,  N=sum_i X_i.

Weak reversibility in fact makes all communicating classes closed, including lattice-residue classes. Global irreducibility is not asserted. Constants and thresholds depend on the fixed graph, parameters, and rates; no uniform-in-dimension or computational-efficiency claim is made. Fixed rates may range over a prescribed positive compact box when taking constants uniform; arbitrary state-dependent interventions are outside this theorem.

## 1. The clearing theorem supplies capability rather than assumes it
`proofs/STRICT_POWER_FAST_CLEARING_V2.md`, separately reviewed in `audits/SEPARATE_STRICT_POWER_REVIEW.md`, proves that the actual conservative fast N-shell killed at c(A)_m has

    sup_x E tau_clear <= C N^{-(m-1+epsilon)}

for some explicit epsilon>0, uniformly over all sufficiently large N and all compositions. It proves small-time deterministic production A(t)>=ct^L from finite complex paths, an elementary shrinking-time martingale/Gronwall approximation, the actual integrated killing hazard, and uniform block iteration. No prior mean or recurrence is used. A common positive catalyst (B)_q divides all times; B>=q is required. Small inactive states are excluded from this estimate and handled explicitly by connector races.

The safe epsilon in the source is enough here. The separate receipt also proves the stronger epsilon=1/(mL+1), but optimizing it is not needed for this global argument. The earlier fractional-factorial/all-face result is independent capital, NOT a load-bearing mean assumption for this theorem. `UNIFORM_FAST_INTERIOR_AND_CLEARING_TIME_V2.md` is included only to preserve the precise family/small-state convention referenced by the reviewed clearing source.

## 2. First actual stopped value: the activity-credit direction
Let I(x)=1 if a fast composition source is enabled and0 otherwise, and h=q-m. Strong connectivity plus the enabled return path makes I invariant under fast jumps. Every pure mX_i has an outgoing edge because k>=2 and the graph is strongly connected. Inactive states satisfy N<=k(m-1). Define

    Z=B-N-h I(x).

Only activation while active raises Z, by h. Immigration turning activity on and clearing that leaves activity on lower Z by h. Other jumps preserve Z. The exact inactive-phase races and actual fast-clearing bound give the uncapped first-exit estimates in `proofs/UNCAPPED_ACTIVITY_CREDIT_TRACE.md`, uniform over ALL hidden compositions:

    P(first Z exit is up)<=C Z^-h,
    E(time to Z exit)<=C Z^(m-1).

The weaker consequence E tau_clear<=C N^(1-m)/(B)_q is sufficient for that proof and follows immediately from the strict clearing theorem. No finite cap or supplied invariant background is used.

For a sufficiently small rational alpha>0, put phi(u)=Gamma(u+1)^alpha on large positive integers. The actual threshold-stopped cost W_Z is finite and satisfies

    L W_Z=-phi(Z) above threshold,
    W_Z<=poly(Z)phi(Z), uniformly in all hidden populations.

Below threshold its only positive leakage comes from active activation in a fixed-width strip and is bounded by C A B. That strip is infinite; it is NOT declared compact.

## 3. Second actual stopped value: N-directed reset and section return
Define H(0)=0 and, for B>=1, write B-1=a(q-1)+v-1 with1<=v<=q-1 and put H(B)=a(m-1)+v. Set

    r=N-H(B),   H(B)=[(m-1)/(q-1)]B+O(1).

Only immigration can raise r (by h); only specified clearings lower it (by h). The crucial real reset output bound is

    E[(1+A_after)^-m; clearing before birth] <= C r^{-(m-1+epsilon)}.

It comes from the clearing compensator and the strict mean, not a claim that A_after is proportional to N. The correlated finite low-phase reset walk is proved in `proofs/N_DIRECTED_RESET_WALK_V2.md`. Its phase-dependent escape estimate is p^{min(q-b,m)/m}, p=r^{-(m-1+epsilon)}; the B0 excursion earns the full p power, whereas arbitrary phases require the phase-dependent bound. Consecutive races are grouped inside positive kernels, not multiplied as unconditional marginals.

`proofs/UNCAPPED_N_DIRECTED_VALUE_CANDIDATE.md` then completes the actual repair. It physically continues neutral bad immigrations instead of treating them as exits. Its pointwise section is B=q, including the full incoming composition. At that section, pointwise hazard comparison gives a downward opportunity at least c r^{-(m-1)}, while upward/bad forcing is O(p r^(alpha h)). Choose alpha h<epsilon. Actual final-clearing kernel disintegration controls even rare selected phases without conditioning a moment bound on observed A. A composed two-type repair kernel earns finite time and weighted cost before any global return assertion.

The actual section-return estimate for Psi(r)=(1+r)^(m-1)phi(r) pays all real running costs. Consequently the threshold-stopped cost W_r is finite and

    L W_r=-phi(r) above threshold,
    W_r<=C(1+r)^(m-1+alpha h)phi(r), uniformly in all hidden populations.

Its exterior positive leakage is bounded by a constant, since only constant-rate immigration can cross its fixed-width threshold band. The older reset-walk file's artificial-stop time is NOT used as an actual return-time bound; the new repair proof closes that previously identified gap.

## 4. Global coupling and all unbounded directions
Let a=(m-1)/(q-1)<1. Since r=N-aB+O(1) and Z=B-N-hI,

    max(r,Z)>=c(N+B)-C.

Each stopped value has a first-holding lower bound

    W >= phi(its residual)/[C(1+N+B)^(m+q)]

inside its domain. Thus V=W_r+W_Z is finite and normlike.

Both components have negative drift when both residuals are above threshold. In the Z leakage strip, r grows linearly with N+B, so -phi(r) absorbs C A B. In the r leakage strip, Z grows linearly and -phi(Z) absorbs the constant leakage. The region where both residuals are below threshold is finite. Hence LV<=-1 outside a finite set, and for every theta>0 the negative margin eventually dominates exp[theta(N+B)]. No entropy selector, finite cap, invariant halo, or frozen infinite fiber appears in this global gluing.

Nonexplosion is also earned independently: fast reactions preserve N+B, and the connector gives L(1+N+B)<=C(1+N+B). For B<q or A<m this is linear; otherwise the negative A^m B^q term dominates A B. Finite-sublevel localization rules out explosion.

State-level complex return paths make classes closed. The normlike Foster inequality yields positive recurrence on each class. For exponential moments, use stopped occupation until a finite set and regeneration within that set: the exp(theta(N+B)) cost of each exterior excursion is bounded by the finite entering V value. Finite-set trace regeneration then gives finite invariant exponential cost without assuming pi(V)<infinity. This is the same standard occupation argument used in the separately reviewed older theorem, not an additional stationarity assumption.

## Scope boundary
This family can have arbitrary composition dimension and positive deficiency; it includes non-complex-balanced rates. It also includes conventional deficiency-zero/product-form members, so no novelty is inferred merely from dimension. The assumptions of a homogeneous conservative fast graph containing all pure complexes, a common catalyst, and the specific q>m connector are genuine restrictions. General weakly reversible recurrence, other connector geometries, q<=m, and arbitrary time/state-dependent rate perturbations remain outside the conclusion.
