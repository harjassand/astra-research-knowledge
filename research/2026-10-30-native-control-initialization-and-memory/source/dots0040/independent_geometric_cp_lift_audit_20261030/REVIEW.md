# Independent hostile review: geometric blocker CP lift

2026-10-30. Reviewer is distinct from the finite-clock author and its child. Sources and exact hashes are in SOURCE_SHA256.txt. No frozen source was edited.

## Verdict

**PASS, scoped:** the idempotent-update construction, exact clock/linked-commutator algebra, geometric blocker payment, finite-depth similarity remainder, and Stinespring local-noise lemma support the stated CLEAN hard-core-range drift. The explicitly different full-tensor DIRECT fresh-K architecture also admits the advertised extra-term absorption.

**One missing load-bearing step in the supplied basin paragraph:** its moment controls T(V), while the safe basin and exit barrier use V. T(V)<=V, and a volume-independent lower comparison is not automatic. Thus the supplied text alone does not finish its basin comparison. An exact two-weight repair is proved in DRESSED_BARRIER_COMPARISON_REPAIR.md in this review directory. It uses only the stated CP generators and compatible parameter slack.

**Not certified:** the original one-site-reset Stinespring compiler on dark/illegal/Kraus-complement sectors; a native two-site Hamiltonian/one-site-dissipation realization of the direct fresh-K jumps; arbitrary noise leaving a clean invariant range without full-space control. The direct fresh-K model and the old compiler have different full-Hilbert generators.

## 1. Idempotence is genuinely CPTP, provided the described channel is used

Let sigma be the finite local syndrome outcome, and let P_sigma be its orthogonal projector. Use Kraus F_sigma P_sigma, where F_sigma is identity on every local minimum (including tied minima) and otherwise maps to a chosen minimum within its reachable affine orbit. First measurement removes coherences between different local syndrome sectors; each output lies in a minimum sector of the same orbit. A second application measures that already block-diagonal sector and applies identity. Hence Phi^2=Phi on ALL operators by linearity, not only on probabilities. Coherences inside one measured sector survive both applications equally.

This depends on choosing identity on every already minimal input. A tie rule that moves one minimum to another need not be idempotent. The proposed rule avoids that issue. Local syndrome orbit enumeration has a fixed finite truth table because the generator/read footprint is fixed-size. It is not a global minimum-decoding oracle. Each nontrivial move decreases total syndrome count by at least one, so beta=1/k0 is valid; the animal constants must indeed be retuned. Active-hub mass is retained because every old accepted candidate witnesses a strictly lower attainable local syndrome.

Consequently d_h=(I-Phi_h*)V>=0, Phi_h*d_h=0 and Delta_h d_h=-d_h hold as actual diagonal-operator identities.

## 2. Clock algebra and B positivity

I independently recomputed the signs. On the legal hard-core space,

    i[H0,n_h]=Y_h,
    i[H0,Y_h]=2G_h-4n_h-sum_{j~h}(a_j†a_h+a_h†a_j),
    D Y_h=-Y_h/2,
    D f(m_h)=m_h[f(m_h-1)-f(m_h)].

Neighbor damping contributes zero to Y_h only in the legal range. The exchange sign is negative. These give exactly the candidate's L_clock B_h.

For B_h=n_h+2nu Y_h+nu²f(m_h), the unblocked 2x2 determinant is nu²(f0-4)+nu⁴f0²>0; blocked legal sectors have B_h=nu²f_m>0. It commutes with neighboring n_j, and sqrt(B_h)n_j sqrt(B_h)=nu²f_m n_j. The square-root dissipator therefore annihilates n_j.

A local full-tensor extension is available for purposes of CP-circuit locality: use n_h ordinary and replace Y_h by G_hY_h. It is positive also on illegal sectors. This mathematical extension of B and T does NOT make the old physical reset generator equal to the fresh-K model.

## 3. Linked commutator and self cancellation

Direct product-rule expansion gives

 [L,Z_h]V=-(L_clock B_h)d_h
   -sum_j a_j†B_h a_j Delta_j d_h
   +sum_j sqrt(B_h)n_j sqrt(B_h) Delta_h d_j
   +sum_j D_sqrt(B_h)*(n_j)d_j.

The j=h terms combine, using Delta_h d_h=-d_h, into D_h(B_h)d_h. In particular the two sqrt(B)n sqrt(B) terms cancel; the leftover is a†Ba-{B,n}/2. This equals (-n_h-nuY_h)d_h on the legal range. There is no assumed commutation of B_h and n_h.

For nonneighbor centers, cancellation requires BOTH disjoint FULL data/read-channel supports (so Phi_h,Phi_j commute) and the relevant clock commutations. The overlap graph must include full channel/read supports, as stated in the earlier clean-lift note. Distance-two clock-star overlap alone is harmless: B_h commutes with a_j,n_j when j is not a graph neighbor, so the two mixed-data terms cancel exactly. It would be wrong to replace this linked cancellation by saying mixed animal differences vanish.

The bounded-patch inequalities |Delta_j d_h|<=C d_j and Delta_h d_j<=C d_h are valid for the actual deterministic bounded-support syndrome updates by the already established completion argument: every noncanceling source animal touches a fixed connected overlap patch, which can be added at bounded weight ratio and bounded preimage cost; the resulting animal contains the active paying move's D. Inactive paying moves give exactly zero. This is not a generic property of arbitrary CPTP maps and must not be detached from this SSF/update construction.

## 4. Geometric blocker absorption

For neighboring j, the activation term is <=C nu² m_h f_m d_h. Choosing f_{m-1}-f_m>=2C f_m leaves half the damping-created blocker service. The other neighbor term is bounded above by C||B_h|| n_j d_j and can be absorbed in the original occupation drift after multiplication by sufficiently small t. The decreasing f choice is essential; the prior scalar-Poisson-credit counterexample does not apply.

Two bookkeeping points should remain explicit:

- The positive +8t nu² n_h term is paid by baseline occupation drift. Service on an occupied h cannot simply be called negative without this payment. Available-empty and blocked sectors have the stated positive qmin; a further small part of baseline covers occupied sectors to yield a uniform service estimate.
- Exchange Cauchy-Schwarz leaves terms C t²nu⁴ n_j d_h, NOT n_j d_j. They are paid using n_j<=I and the uniform tnu² service for that SAME h. Bounded degree then suffices. The child audit makes this payment explicit and it is valid.

For example reserve fixed degree-dependent portions of -sum n_hd_h for own coherence, exchange, positive n_h curvature, and neighbor reset terms. Residuals are O(t²nu²), O(t²nu⁴), and O(tnu³) times sum d_h. First choose nu small relative to qmin and fixed local coefficients; then t small enough for all these residuals and baseline reservations. This yields the candidate's first-order inequality with constants independent of volume. The later restriction t<<nu² for the similarity remainder is compatible with these choices.

## 5. Local finite-depth similarity remainder

For fixed colors, T is a finite-depth product of local exp(tZ_h). Each inverse exp(-tZ_h) is local, unital and HP, although not CP. Conjugating one original local generator through T only encounters its finite circuit causal cone. Disjoint factors commute and cancel; one never estimates a global T inverse norm. Thus each conjugated local term has fixed support and a uniform analytic Taylor remainder O(t²), in cb norm. Its zeroth and first derivatives are the stated L and sum[L,Z_h]. Each remainder is HP and annihilates identity.

The local syndrome-orbit estimate therefore bounds the summed remainder by C t²W. The positive service coefficient is proportional to tnu², so taking t small compared with nu² times the established coverage constant absorbs it. Pushing the resulting inequality through positive unital T is valid. If the drift holds only on the DATA basin, Schrödinger T must preserve that basin; every Phi move is V-nonincreasing and the small-component edge barrier gives precisely that property for the appropriate low-V basin. Clock-range preservation must additionally be imposed in a legal-range-only model.

This is an exact pointwise drift with a bounded, absorbed remainder. It is not a long-time effective-Poisson approximation.

## 6. Stinespring local-noise lemma

The supplied conjugation orientation is correct. For T(O)=E[U†(O tensor I)U] and

 M=Ad_U (N* tensor id_env) Ad_U†,

one has N*T(O)=E[U† M(O tensor I) U]. N commutes through E because it cannot act on the fresh dilation environments. M is HP, identity-annihilating and has the same cb norm. Its physical support is the fixed-depth causal cone; an arbitrary shared external bath is retained as a spectator of the dilation, not counted as a bounded physical support.

The original local-orbit bound applies on the enlarged local Hilbert space and survives positive conjugation/compression. Counting cones intersecting an animal gives epsilon C T(W), with no W² loss. This proves the lemma as stated. It does not prove drift outside a range where clean drift was established.

## 7. Additional full-tensor DIRECT model

I also checked FULL_CLOCK_DIRECT_JUMP_EXTENSION.md and FULL_TENSOR_DIRECT_FRESH_K_AUDIT.md. Their model has unguarded reset jumps sigma_h^- tensor K_hs on ALL clock occupation patterns and guarded Hamiltonian sum G_hX_h. This is a different physical generator from an onsite reset acting on a Stinespring workspace.

On the full clock tensor product the exact additional identities are

 D_j(G_hY_h)=n_jG_{h\\j}Y_h,
 a_j†B_h a_j=n_j[n_h+2nuG_{h\\j}Y_h+nu² f(m_h-1)],
 sqrt(B_h)n_j sqrt(B_h)=(n_hn_j+nu²f_m n_j).

The added gain off-diagonal term cannot be omitted, but the whole a_j†B_h a_j is positive and <=||B_h||n_j, so the same reset-payment bound handles it. The n_hn_j activation term is <=C D n_h d_h and is baseline-paid. New clock terms are h-off-diagonal with sizes O(nu) or O(nu²); their form bounds cost baseline n_hd_h plus O(t²nu²) or O(t²nu⁴)d_h. Uniform blocker service pays the residuals. These computations support the stated full-tensor direct-model clean drift.

The direct model has bounded-body fresh correction jumps and potentially guarded many-body Hamiltonians. It is an explicit stronger-operation architecture, not a native two-site/one-site-reservoir realization.

## 8. Independent finite regression

`check_full_tensor_algebra.py` constructs three full clock qubits on a star, with three full CPTP idempotent data maps, including a hub that activates another hub. It checks the exact linked identity and a first-order drift inequality on ALL clock configurations, including illegal adjacent occupations. Identity errors are <=8.9e-16; B minimum eigenvalues are positive; the tested drift residual maximum eigenvalue is 2.1e-17 (zero within rounding). This is an independently written sanity check, not a substitute for the proofs above.

## Final scope

The requested clean geometric-blocker/CP-lift machinery survives hostile review. The missing original-vs-dressed barrier comparison must be supplied (see the exact separate repair), and full physical robustness remains restricted to the explicitly fresh-K direct model unless the original one-site-reset compiler's dirty sectors are separately controlled. No receipt here certifies that unresolved physical equivalence.
