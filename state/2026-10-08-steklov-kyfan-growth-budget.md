# A Steklov–Ky Fan growth budget for harmonic functions on uniformly controlled polar ends

**Date:** 8 October 2026 (Australia/Brisbane).  
**Status:** Independently derived proof for the explicit geometric class below; not formally certified or independently peer reviewed. Priority remains UNKNOWN. In particular, this note does **not** certify the existing Astra single-metric construction and does not assert a historic open-problem resolution.  
**Pinned Astra base commit:** 687dfc0640ee80654bcbdbe38cb13d6e1f1586ce.  
**Related Astra cards:** N175–N178; primary release family 361.  
**Research purpose:** Test whether the factor 9v/4 suggested by the one-metric angular construction can be a universal sharp ceiling, and whether persistent excess at every sufficiently large growth degree is possible.

## Theorem (controlled polar harmonic-dimension bounds)

Let n=d+1 >=2. On R^n, let g be smooth, Euclidean near the origin, and for all sufficiently large r of the form

    g = dr^2 + f(r)^2 H(log r),

where f(r)>0, f(r)/r -> a in (0,infinity). Assume H(t) is a smooth family of metrics on S^d satisfying:

1. Its Riemannian volume form is the SAME pointwise round volume form dmu for all t (not merely the same total volume).
2. Its range is precompact in the smooth C-infinity topology; in particular, all angular metrics are uniformly elliptic and have uniform spatial derivative bounds.
3. sup_{t sufficiently large} ||partial_t H(t)||_{C^0} < infinity.

Let h_k(g) be the dimension of entire real harmonic functions satisfying |u(x)| <= C_u(1+r(x)^k), for nonnegative integers k. Define C_d=2/d!, which is the leading coefficient of h_k(R^{d+1}) ~ C_d k^d. Then each h_k is finite and

    liminf_{k->infinity} h_k(g)/(C_d k^d) <= a^d,
    limsup_{k->infinity} h_k(g)/(C_d k^d) <= [(d+1)/d]^d a^d.

The asymptotic volume ratio is AVR(g)=a^d. The theorem does NOT require a Ricci-curvature hypothesis.

Moreover, when the union of the polynomial-growth harmonic spaces is infinite dimensional, choose an adapted basis u_1,u_2,... and its nondecreasing integer birth degrees b_i (the least k with h_k >= i). There is the stronger spectral-budget inequality

    liminf_{p->infinity} p^(-1-1/d) sum_{i=1}^p b_i
       >= [d/(d+1)] a^(-1) C_d^(-1/d).

For n=3, C_2=1, giving

    liminf h_k/(k+1)^2 <= v,
    limsup h_k/(k+1)^2 <= 9v/4,   v=AVR(g)=a^2.

The precise normalization k versus k+1 does not affect limits.

## Proof

### Step 1: all spheres share one Hilbert space and have a positive self-adjoint growth generator

Write t=log R. Because dvol(H_t)=dmu pointwise, all sphere functions are identified with the fixed real Hilbert space L^2(S^d,dmu). For smooth boundary data v on r=R, let E_R(v) be its unique harmonic extension to B_R, and define the rescaled Dirichlet-to-Neumann operator

    Lambda_t(v) = R [partial_r E_R(v)]|_{r=R}.

Its quadratic form on L^2(dmu) is

    <v,Lambda_t v> = R/f(R)^d int_{B_R} |grad E_R(v)|^2 dvol_g.

Hence Lambda_t is nonnegative self-adjoint with discrete eigenvalues
0=lambda_1(t)<=lambda_2(t)<=..., repeated with multiplicities.

If u is any ENTIRE harmonic function and v_u(t) its trace at r=e^t, the restriction of u to B_{e^t} equals E_{e^t}(v_u(t)). Thus

    partial_t v_u(t) = Lambda_t v_u(t).

This is an exact identity, not a frozen-spectral approximation. Notice that a moving spherical area measure would introduce additional terms: the pointwise fixed-area hypothesis is used essentially here.

### Step 2: a uniform sharp lower Steklov Weyl bound via one short collar

Fix eps>0. Choose a short logarithmic collar [t-delta,t] with delta>0 small, then T large. Put b(s)=f(e^s)/e^s. For any u defined in the collar, the normalized energy appearing in the preceding quadratic form, restricted to that collar, is exactly

    int_{t-delta}^t e^{(d-1)(s-t)}
      [ (b(s)/b(t))^d ||partial_s u||^2_{L2(dmu)}
       + b(s)^{d-2}/b(t)^d q_{H(s)}(u) ] ds,

where q_H(u)=int_{S^d}|grad_H u|^2 dmu. This follows by substituting r=e^s in the radial and angular parts of the metric energy.

Since b(s)->a uniformly in the collar at large t, the e^{(d-1)(s-t)} factor is close to one for small delta, and H(s) is C^0-close to H(t) uniformly over this collar by the bounded time derivative. Hence, after choosing delta,T in that order, the form is bounded below by

    (1-eps) int_{t-delta}^t
      [||partial_s u||^2 + a^(-2) q_{H(t)}(u)] ds

for every t>=T, with the free inner-end trace unconstrained. The full-ball energy exceeds its collar energy.

Let D_t=a^(-1) sqrt(-Delta_{H(t)}). Minimizing the constant-coefficient collar energy with prescribed trace u(t)=v and free trace at t-delta gives the exact Neumann-inner-end quadratic form

    <v, D_t tanh(delta D_t) v>.

Consequently, for every t>=T, in quadratic-form order,

    Lambda_t >= (1-eps) D_t tanh(delta D_t).

The classical smooth compact-manifold Weyl law, uniformly over the smooth-precompact set {H(t)}, gives

    #{j: sqrt(eigenvalue_j(-Delta_H(t))) <= L}
        = (C_d+o(1)) L^d

uniformly in t as L->infinity, since each H(t) has the round sphere volume. The uniformity follows alternatively from a finite smooth/metric cover, min-max form comparison, and the fixed-metric Weyl law. The constant C_d is the round-sphere Weyl coefficient, 2/d!.

By min-max, tanh(delta D_t)->1 uniformly in high angular indices, and eps is arbitrary, we obtain the needed UNIFORM lower Steklov spectral sum:

    liminf_{p->infinity} inf_{t>=T}
       p^(-1-1/d) sum_{j=1}^p lambda_j(t)
       >= [d/(d+1)] a^(-1) C_d^(-1/d),

interpreted with an arbitrarily small relative loss and a corresponding sufficiently late T. No control of the geometry INSIDE the short collar is needed for this lower bound. In particular this step does not assume a degree-uniform bound from the Astra spectral-crossing construction.

### Step 3: exterior-volume identity and the Ky Fan variational principle

For any p linearly independent entire harmonic functions u_1,...,u_p, let v_i(t) be their traces and let

    G_ij(t)=<v_i(t),v_j(t)>_{L2(dmu)},
    W_p(t)=sqrt(det G(t)).

G(t) is positive definite for every t: a nonzero linear combination vanishing on one sphere vanishes in its entire enclosed ball by uniqueness for the Dirichlet problem, and hence vanishes globally by unique continuation.

Differentiate using partial_t v_i=Lambda_t v_i and self-adjointness:

    (d/dt) log W_p(t)
      = tr( G(t)^(-1) [<v_i(t),Lambda_t v_j(t)>]_{i,j} )
      = Tr(P_t Lambda_t),

where P_t is the orthogonal projection onto span{v_1(t),...,v_p(t)}. Ky Fan's min principle gives

    (d/dt) log W_p(t) >= sum_{j=1}^p lambda_j(t).

If |u_i(x)|<=C_i(1+r(x)^{m_i}), then
||v_i(t)||_2<=C'_i e^{m_i t} for large t. Hadamard's determinant inequality yields

    W_p(t) <= prod_i ||v_i(t)||_2
           <= C_p exp(t sum_i m_i).

Integrate the previous differential inequality from any fixed large T to t, divide by t, then let t->infinity. Step 2 implies, as p->infinity,

    sum_{i=1}^p m_i
      >= ([d/(d+1)] a^(-1) C_d^(-1/d) - o_p(1))
           p^(1+1/d).

The o_p term is independent of the chosen harmonic functions; more precisely one first fixes eps and T in Step 2, proves a uniform constant with eps loss for all sufficiently large p, then lets eps->0. This proves the asserted birth-degree budget by choosing an adapted basis with m_i=b_i.

The same argument with p arbitrary harmonic functions all of growth <=k gives
p*k >= c p^(1+1/d) for large p, which proves that h_k is finite even without assuming nonnegative Ricci curvature.

### Step 4: the two asymptotic bounds

For p=h_k, every one of the first p birth degrees b_i is <=k. Hence

    p k >= sum_{i<=p} b_i
        >= ([d/(d+1)] a^(-1) C_d^(-1/d)-o(1))p^(1+1/d).

Rearranging proves

    limsup_{k->infinity} h_k/(C_d k^d)
       <= [(d+1)/d]^d a^d.

For the lower-limit assertion, suppose contrariwise that some c>C_d a^d satisfies h_k >= c k^d for ALL sufficiently large k. Then, by the definition of the birth degrees,

    b_i <= ceil((i/c)^(1/d))  for all sufficiently large i.

Consequently

    sum_{i=1}^p b_i <= [d/(d+1)] c^(-1/d) p^(1+1/d)+O(p).

Since c>C_d a^d, this strictly contradicts the budget constant in Step 3. Thus

    liminf h_k/(C_d k^d) <= a^d.

If the union of growth spaces is finite dimensional, both conclusions are immediate. This completes the proof.

### Step 5: asymptotic volume ratio

The coordinate r is distance to the origin, since all radial rays have unit speed and every curve from the origin to radius R has length >=R. Pointwise fixed angular volume gives

    Vol_g(B_R)=Vol(S^d) int_0^R f(r)^d dr
              ~ [Vol(S^d)/(d+1)]a^d R^(d+1).

Therefore AVR(g)=a^d, as used in the theorem.

## Sanity check against exact cones

For an exact cone with H(t)=the round metric and f(r)=a r on the end, the large-degree radial harmonic exponent corresponding to spherical degree l is

    gamma_l = [-(d-1)+sqrt((d-1)^2+4 l(l+d-1)/a^2)]/2
             = l/a+O(1).

The multiplicity of degree l matches Euclidean spherical harmonics. Hence h_k/(C_d k^d)->a^d. This saturates the lower-limit coefficient and respects the larger upper coefficient. It checks the normalization but is not an independent proof certificate for the general argument.

## Connection to the unverified Astra common-metric claim

The candidate N175–N178 construction has d=2, angular metrics with the same area form, smooth compact angular-library closure, and quantitative time-derivative estimates ||partial_t H||_{C^q}=O(t^-3/4). Its radial factor obeys f(r)/r->sqrt(v). Thus, IF its full countable Ricci-nonnegative construction and harmonic lower bound withstand expert auditing, the theorem in this note applies to that SAME metric and gives

    limsup h_k/(k+1)^2 > c > 1 > v >= liminf h_k/(k+1)^2.

In particular, the normalized harmonic-dimension sequence would oscillate and fail to converge on ONE complete smooth Ricci-nonnegative three-manifold. As the candidate allows every c<9v/4, the universal polar-end limsup upper coefficient 9v/4 would be optimal as a supremum over this model class, conditional on the candidate's correctness. This is stronger conceptual organization of its spectral mechanism, NOT independent certification of its existence proof.

The fixed-area constraint is essential to the clean fixed-Hilbert-space trace identity. No general theorem is claimed for all Ricci-nonnegative manifolds or for arbitrary noncompact ends. Dropping angular compactness, the short-collar geometry bound, or pointwise common volume form requires new work.

## Adversarial scope and priority ledger

- **Proved here under the listed assumptions:** short-collar Steklov lower spectral asymptotic; fixed-Hilbert-space Gram volume derivative; Ky Fan growth-budget inequality; liminf and limsup dimension bounds.
- **Not proved here:** existence of a single Ricci-nonnegative metric attaining the limsup excess; external correctness of N175–N178; arbitrary-geodesic-sphere/Ricci-only analogue; historical novelty of the Ky Fan formulation.
- **Classical prerequisites:** smooth compact-manifold Weyl law, elliptic Dirichlet uniqueness and unique continuation, Ky Fan variational principle, min-max for self-adjoint forms, finite-dimensional Gram determinant identity.
- **Potential priority overlaps to check with specialists:** Colding–Minicozzi harmonic-dimension estimates; Huang, *Harmonic functions with polynomial growth on manifolds with nonnegative Ricci curvature* (arXiv:2109.07534), which assumes unique tangent cone; literature on Steklov variation and asymptotically conical manifolds.
- **Primary OpenAI comparison:** family 361, *A Three-Dimensional Counterexample to Integer-Degree Harmonic Dimension Comparison* (2026), which produces degree-dependent metrics, not the common metric here.
- **Novelty status:** UNKNOWN; no claim of first discovery or field-changing significance. The derivation should be independently checked for the uniform angular Weyl and short-collar operator-form steps before specialist dissemination.

Links:
- https://github.com/openai/math/tree/main/preprints/A-Three-Dimensional-Counterexample-to-Integer-Degree-Harmonic-Dimension-Comparison-September-26-2026/build/sections
- https://arxiv.org/abs/2109.07534
- https://arxiv.org/abs/1705.05008
- https://github.com/harjassand/astra-research-knowledge/blob/687dfc0640ee80654bcbdbe38cb13d6e1f1586ce/frontier/review_cards/N175-single-metric-harmonic-limsup.txt
