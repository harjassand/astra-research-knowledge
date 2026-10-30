# Exact short-time local-noise transfer: explicit incidence bound
2026-10-30. Root derivation, awaiting independent review.

This closes the connected-cluster counting placeholder in SHORT_TIME_CP_AVERAGE.md. It does not prove native weighted service.

## 1. Local operator algebra and norms
Work in the Heisenberg picture. Let L=sum_X L_X be the clean Lindblad generator, each term HP and identity-annihilating, supported on at most r physical sites. Set

    J = sup_i sum_(X containing i) ||L_X||_cb < infinity.

Let N=sum_Z N_Z be an unknown HP identity-annihilating perturbation with |Z|<=q and incidence

    eta = sup_i sum_(Z containing i) ||N_Z||_cb.

Terms may contain a retained common bath factor of arbitrary dimension. Count only physical system sites; clean L_X acts trivially on the bath. Bath-only dynamics is removed by its interaction picture. A perturbation acting only on the bath annihilates the barrier and can be kept in that picture. Norms are completely bounded, not a scalar effective noise rate.

For a representation M=sum_Z M_Z with max support size u, write m(M)=sup_i sum_(Z containing i)||M_Z||_cb. Expand [L,M] into the actual pairs (X,Z) with X intersect Z nonempty; disjoint maps commute. Every resulting term is HP and annihilates identity. Its support is X union Z, size <=u+r, and norm <=2||L_X||||M_Z||.

For each anchor i split union membership into i in Z or i in X (double counting is harmless). Then

    sum_(X,Z: i in Z, X meets Z) 2||L_X||||M_Z|| <=2u J m(M),
    sum_(X,Z: i in X, X meets Z) 2||L_X||||M_Z|| <=2r J m(M).

Therefore

    m([L,M]) <=2J(u+r)m(M).

Iterating, if M_n=ad_L^n(N),

    u_n<=q+nr,
    m(M_n)<=eta (2Jr)^n (1+q/r)_n,

where (a)_n=a(a+1)...(a+n-1). This is a decomposition norm bound; cancellations are unnecessary. It is uniform in system size.

## 2. Relative animal-orbit estimate
Suppose f_A=exp(a|A|) product_(v in A) w_v, where all w_v are commuting positive local factors with theta I<=w_v<=I. Each physical site belongs to supports of at most k factors, and each factor has at most b physical sites. Syndrome checks and duplicated controller-flag factors satisfy this after fixed geometry/token choices.

A map M_Z annihilating identity acts only on factors whose supports meet Z; there are at most k|Z| such factors. Factor out the rest, which commutes with M_Z and with its output. The remaining positive factor has spectrum in [theta^(k|Z|),1]. The amplified cb bound gives

    +/- M_Z(f_A) <= ||M_Z||_cb theta^(-k|Z|) f_A.

The result is zero if Z misses the physical support of f_A. The support of f_A has at most b|A| sites. Hence for a family with support size at most u and incidence m,

    +/- M(V) <= b m theta^(-ku) W,
    V=sum_A f_A, W=sum_A |A|f_A.

This is an operator inequality, including a reference/common bath, not an entrywise or stochastic estimate. Completely bounded norm is taken on operator norm; for Schrödinger generators this is the corresponding diamond norm of the adjoint.

## 3. Convergent exact similarity for a short fixed horizon
For finite volume the exponential similarity is an exact entire matrix identity:

    M(s)=exp(-sL) N exp(sL)
        =sum_(n>=0) (-s)^n/n! ad_L^n(N).

Define x(s)=2Jr theta^(-kr) s and a_*=1+q/r. The incidence/orbit series converges uniformly in volume for x(s)<1. Using the binomial generating function,

    +/- M(s)V <= b eta theta^(-kq) (1-x(s))^(-a_*) W.       (1)

This is a concrete bound. The smallness requirement is on a FIXED proof horizon, not on total storage time.

Because exp(sL) is unital CP,

    N exp(sL)V = exp(sL) M(s)V.

If the ACTUAL clean semigroup satisfies exp(sL)W<=W, then (1) gives

    N exp(sL)V <= C_T eta W,
    C_T=b theta^(-kq)(1-x(T))^(-a_*),   0<=s<=T.

Consequently for F_T=integral_0^T exp(sL)V ds,

    N F_T<=C_T eta T W.                              (2)

For time-dependent perturbations apply (2) pointwise to N_t; the clean similarity still uses the same L. No approximation of the full noisy dynamics, inverse CP map, environment reconstruction, or error accumulating with storage time is used.

## 4. Conditional drift consequence and what remains
If exp(TL)V-V<=-alpha W+b0 N I, then exactly

    (L+N_t)F_T <=-(alpha-C_T eta T)W+b0 N I.

Since W>=V and F_T<=TV when L V<=0, this also gives a conventional linear F_T drift. A two-weight raw-barrier comparison and an invariant safe basin must still be supplied, as described in SHORT_TIME_CP_AVERAGE.md.

For a basin-restricted inequality, do NOT multiply an order valid only inside P by exp(sL) unless the clean semigroup preserves P. The native proof must verify this. The norm derivation itself is global and independent of such an assumption.

Status: newly derived root lemma, not yet independently reviewed. It applies to any actual local clean generator satisfying V/W monotonicity and earned finite-window service. Those premises are substantive and remain open for the native transactional construction.
