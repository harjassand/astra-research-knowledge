# Independent review: guarded graph-state factory

2026-10-29. Reviewer: audit_graph_state_factory. Source snapshots are identified in SOURCE_SHA256.txt. This review is mathematical, not a literature/novelty review. Exact 36-dimensional regressions were not used as a substitute for proof.

## Verdict

**The proposed size-uniform joint bare-data syndrome conclusion follows for this specified guarded graph-recovery model**, subject to the explicit uniformity and noise assumptions below. I found no substantive algebraic obstruction in the full-space dressing, radius-two flag construction, gentle-projection healing, arbitrary-finite-time local polynomial construction, packing, or bare-output containment. This certifies neither the separate two-site lease architecture nor arbitrary-channel data recovery, unknown-payload memory, a universal computational threshold, or practical advantage.

The statement is an existence-level finite-resource, local-parameter theorem. Its constants may be catastrophically poor. The ordinary bounded-depth graph-state circuit and ideal stabilizer-dissipation comparator remain essential.

## Assumptions to make explicit

1. Use bounded degree, bounded physical box size and overlap multiplicity, fixed finite local Hilbert dimensions, finite interaction range, and volume-independent clean strength bounds. The progress proof as written directly covers uniform g_x=g>0 and kappa_x=kappa>0. A nonuniform formulation needs uniform positive lower bounds and the corresponding modified progress constants, not just positive rates separately in each finite volume. Letting g_min vanish with volume defeats the claimed uniform preparation time.
2. Every local noise summand used in a termwise operator inequality must be Hermiticity preserving and annihilate the identity in the adjoint. Group summands if necessary. Total evolution must be CPTP. A legitimate total generator alone does not make an arbitrary non-Hermiticity-preserving decomposition suitable for the displayed order inequalities.
3. Norm budgets apply to the actual local system-bath maps (or completely bounded extensions adequate for retained baths), not merely an unamplified system-only map norm. Bounded physical support and bath-coupling norm are required; arbitrary bath initial correlations are allowed. Bath-only dynamics contributes zero to the system observables.
4. Packing and eta_R count physical support, including the enlargement by U and by the polynomial construction. Noise range and per-support budget are uniform in volume and time. The useful regime is K eta_R/r<1, and the stated transient p(t) only becomes nontrivial when K q(t)<1.

## Algebra and locality

The displayed excited-sector completion is unitary: its first row projects onto the two orthogonal syndrome spaces, its second row is the same decomposition followed by Z_y, and cross row products vanish. Adjacent guarded U factors cannot be simultaneously nontrivial in an occupancy block; nonadjacent data supports are disjoint. Thus all factors commute, preserve occupancy, and admit a bounded-depth coloring.

For each H_x, all adjacent clocks are ready wherever the guarded term acts. Adjacent U factors are therefore identity there; nonadjacent factors commute with it. Only U_x transforms H_x, giving the clock-only ready/label-1 transition on the full Hilbert space, not just the legal code.

For a reset at x, only U_x and neighboring U factors can fail to commute with it. Their data support is the union of boxes in the closed overlap neighborhood of x; their guard clocks extend at most to overlap radius two. A stabilizer box y can overlap that union only when dist(x,y)<=2. Hence R_y=B_2(y) suffices. On B_x=0, any nonzero reset input has x in label 1 with all adjacent clocks ready, so the reset is exactly the intended Kraus action; x ready contributes zero. Its output has x ready, and neighboring dressings remain identity on this branch. Bad B flags cannot be created.

Consequently A_y L_xs(I-A_y)=0 for all transformed reset jumps. The summed loss is kappa_x Q_x, which commutes with A_y. The Hamiltonian commutes with A_y. These facts establish the negative Gram identity, not merely invariance of classical states. In particular, the A_y corner is invariant under the adjoint semigroup, and all derivatives and polynomial approximants starting at A_y remain A_y-supported.

## Healing from arbitrary states

Controller damping gives Tr[(I-P)rho(t1)]<=|R_y|exp(-kappa_min t1), with P the joint good-controller projector in R_y. This is a commuting-projector union bound, not a measurement inserted into the physical evolution. Let c>0 be the uniform probability of at least one y emission during t2. Choose the upper bound eta<=c^2/16. For sigma=P rho(t1)P, gentle projection gives ||rho(t1)-sigma||_1<=2sqrt(eta)<=c/2.

The sigma branch stays good in R_y. Its first y reset clears d_y under every Kraus outcome, and subsequent clean dynamics cannot recreate A_y. The full-space progress theorem therefore bounds the final A_y expectation on sigma by (1-c)Tr sigma<=1-c. Trace norm contractivity charges the discarded coherences by c/2. Thus the evolved A_y effect has norm <=1-c/2. Invariant-corner support promotes this to exp(T L*)A_y<=(1-c/2)A_y. This last step is essential; an absolute norm bound alone would not suffice for the polynomial argument.

The progress dependency was checked through EXPLICIT_LOCAL_OBSERVABILITY.md and FULL_GUARDED_KRAUS_EXTENSION.md. The full-space curvature residual uses E_x<=Q_x, adjacent terms are x-off-diagonal, and reset neighbor-count identities are unchanged by internal labels. The nested cutoff argument forces a positive integrated occupation, and bounded emission intensity converts that into a positive emission probability. No global mixing assertion enters.

## Arbitrary finite healing time: polynomial audit

For support size s and local support cap r0, put a_int=max(1,r0-1), C=J a_int. Connected local-term sequences give

    ||L*^k O|| <= J^k product_{i=0}^{k-1}(s+i a_int)||O||
                 <= C^k (s)_k ||O||.

Local terms must individually annihilate I here, as do clean Hamiltonian and Lindblad summands. At delta C<=1/4, the factorial-normalized coefficients are bounded using binom(s+k-1,k)<=2^(s+k-1). Summing the tails verifies both stated exponential and integral bounds. R_K integrates terms through order K-1; its first omitted term has order K, consistent with the stated delta 2^(s-K) bound.

Choose each K_j to bound exponential error by epsilon/M and integral error by delta epsilon/M using ||O_{j-1}||<=1+epsilon<=2. Contractivity gives endpoint error <=j epsilon/M. The integral approximation accumulates at most

    sum_j [delta epsilon/M + delta (j-1)epsilon/M]
       = T epsilon (M+1)/(2M) <= T epsilon,

which is even smaller than the documented (1+T)epsilon allowance. Crucially, L*F_j=O_j-A_y is exact for every j, so no volume-dependent ||L|| is applied to an approximation error. Each approximation difference is A_y-supported, making all errors relative order errors. The chosen tolerances imply (a/2)A_y<=F_y<=(3T/2)A_y and L*F_y<=-[c_heal/(3T)]F_y, where c_heal is the actual healing contraction (c/2 in the preceding section). Support grows recursively but only with fixed local parameters.

## Packing and arbitrary-initial-state comparison

Choose buffered disjoint F supports so that each clean/noise term touches at most one factor. Then the product generator identity has no dissipative cross term. Normalize Z=F/b0. For a packed U, positivity and locality imply

    m'_U <= -r|U|m_U + eta_R sum_{x in U}m_{U\\{x}}.

Since 0<=Z<=I, arbitrary initial states satisfy m_U(0)<=1. Induction in |U| compares to q(t)^|U|, where q'=-rq+eta_R and q(0)=1. Retained-bath correlations do not invalidate this operator-based comparison. Since A_y commute and A_y<=K Z_y, a packed subset U of any S yields (Kq)^|U|. If Kq<1 and |U|>=|S|/P, this is at most [(Kq)^(1/P)]^|S|. The direction of the exponent inequality is correct specifically in that regime.

## Bare data, not only a dressed subsystem

For x!=y, every data block of U_x commutes with d_y: S_x commutes with S_y and Z_x commutes with S_y. Thus U* d_y U=U_y* d_y U_y. On (I-d_y)(I-B_y), U_y is identity: either y is ready, or it is good excited label 1 and its data has positive syndrome. Hence U* d_y U<=d_y OR B_y<=A_y as an exact projector range inclusion.

The family U*d_yU commutes internally, as does the family A_y. Intersection of their ranges gives the product containment for every S; cross-family commutativity is unnecessary. Thus the sparse syndrome law holds for the actual bare reduced data at each qualifying time, without a decoder or empty-clock postselection. It remains a syndrome-probability contract, not automatically a graph-basis stochastic Pauli mixture unless an additional twirl is performed. Output transport, downstream operations, and their noise are not priced by this equal-time statement.

## Outcome and residual scope

No permissions were blocked; all requested local sources were read. The only repairs identified are making the uniform-rate and noise-map hypotheses explicit and carefully distinguishing the progress probability c from the healing contraction c/2 in substituted constants. No patch to the original proof files was made, avoiding concurrent edits. The main mathematical chain survives this independent review under those assumptions.

### Final-source qualification update, 20:45 UTC

The root has now explicitly added fixed volume/runtime-independent g_x=g>0 and kappa_x=kappa>0 to GRAPH_STATE_DATA_BRIDGE.md, and Hermiticity-preserving identity-annihilating local noise terms with actual retained-bath support norms to that document and the shared repair/defect/progress statements. These additions were inspected and satisfy the qualification requests above. SOURCE_SHA256.txt now records these final reviewed versions; INITIAL_SOURCE_SHA256.txt preserves the previous snapshot manifest. This removes those qualifications as outstanding editorial fixes; the substantive assumptions remain part of the theorem.
