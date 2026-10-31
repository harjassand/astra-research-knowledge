# Independent review: static fiber-tangent stirring capacity

**Verdict: PASS with the explicit domain/observable qualifications below.** Full source read and SHA verified: `FIBER_STIRRING_BOUND_CANDIDATE.md`, `ad8f7653b8b0d4be2390dffbc2508741cb0a45298d589a14f4fbe0d33a76e1a1`. Original unchanged. This receipt is unique to this candidate, not a nonreversible executable or a new stochastic-path theorem.

## Functional analytic receiving

The measure is the actual smooth positive normalizable Gibbs probability, the diffusion matrix is beta^(-1) times identity, and the actual reversible process has already been received globally. The perturbation is a static smooth bounded compactly supported field, divergence-free with respect to that measure and with c_y identically zero. A finite amplitude, however large, meets this interface; uniform bounds on its implementation or mixing are not implied.

For T=b^2-y^2 in the open slab, L T=S T=-2/beta+2y F_y<=-2/beta. Stopping also at finite spatial exhaustion and time, then removing the spatial cutoff using nonexplosion, gives E(tau_exit)<=beta T(y)/2<=beta b^2/2. Nonnegativity and boundedness of T up to exit justify the limit. This is slab exit, not the rare time to reach the slab or complete a basin-to-basin passage.

For compactly supported zero-trace tests the integration-by-parts ground-state identity is correct, including its factors:

    E(f,f)=beta^(-1) integral T^2 |grad(f/T)|^2 dmu
           + integral (-S T/T) f^2 dmu.

Since T<=b^2 and -S T>=2/beta, it supplies Poincare constant beta*b^2/2. Passing to the weighted H1 zero-trace closure preserves the inequality; no angular/fiber Poincare inequality is needed. Smooth positive density makes local traces the usual ones. Cutoffs at transverse infinity are legitimate for finite weighted H1 functions: their gradient errors vanish by L2 tails and an O(1/R) cutoff derivative. Thus the closure/trace interpretation does not add a reflecting boundary at infinity.

The drift form is continuous by bounded c and that Poincare estimate. Its skew identity follows from div(mu*c)=0, compact support and zero plane-normal component. Therefore a(f,f)=E(f,f), with no smallness requirement on c. A bounded scalar interpolation u0 has finite energy (its derivative is bounded and mu is finite). Lax–Milgram for h-u0 is consequently valid. Positive/negative truncations of h show 0<=h<=1; the drift contribution to each truncation is the integral of c dotted with the gradient of a scalar function of h, hence zero. Local elliptic boundary regularity and stopped martingale representation, using the finite exit estimate and bounded h, identify h with the actual committor. No committor computation is supplied or required by the scalar certificate.

One wording precision in the source's global paragraph: mere knowledge that a reversible diffusion is conservative does not literally provide a named Lyapunov function. For the received homogeneous examples an actual Lyapunov function was established, and its added c-gradient term is bounded on compact support. More generally the bounded drift perturbation here can be received by finite-time Girsanov/Novikov absolute continuity of the nonexplosive base diffusion, with local uniqueness from smooth coefficients. Weighted divergence-freedom and the resulting conservative diffusion/Dirichlet-form construction preserve mu. Either is an appropriate justification; do not silently assert an unacquired global Lyapunov certificate for an arbitrary input potential. This does not change the claimed compact bounded-drift result.

## Orthogonality, boundary flux and capacity

For every finite-energy scalar trial u with the committor boundary values, u-h is an admissible zero-trace test. The weak equation gives E(h,u-h)=integral(c.grad h)(u-h). The term against h vanishes by skewness. The term against u equals -integral h(c.grad u)=0 since c_y=0. Thus E(h,u)=E(h,h), and polarization yields exactly

    E(u,u)=E(h,h)+E(u-h,u-h).

This is NOT the ordinary reversible minimization principle applied to a nonreversible generator. It is an exact identity for the restricted trial subspace annihilated by the antisymmetric drift.

The equilibrium capacity equals E(h,h), with h extended by its constants in the basins. This can also be defined/received via weak total boundary flux: pair the harmonic equation with any scalar boundary interpolation, and use the preceding identity. There is no advective boundary flux because c_y=0. Smooth boundary regularity gives the local classical flux interpretation; finite energy and weighted transverse cutoffs remove the boundary at infinity. Reversing the convention 0/1 for the two basins replaces h by 1-h and leaves the energy unchanged. The ordinary symmetric-part Dirichlet minimum over all admissible functions then gives cap_rev<=E(h,h). Minimizing scalar trial energy gives the upper bound [beta integral(1/p)]^(-1), with p the actual normalized marginal. Even if one uses an approximating scalar minimizing sequence rather than assumes the minimizer is classically smooth, the bound follows.

Hence the received reversible lower bound k_free/C and scalar upper bound k_free remain valid for cap_c/mu(A). The denominator is the actual basin mass, unchanged by the stationary drift. This is an equilibrium capacity/mass sandwich, not an arbitrary-start mean waiting-time formula. It establishes neither monotonicity as amplitude varies nor improved mixing, deadlines or angular relaxation.

## Explicit constructor and scope

For coercive smooth homogeneous U, c_z=M psi(y) chi(U) J grad U is bounded and compactly supported if the stated scalar cutoffs are compactly supported. Antisymmetry makes grad U dot J grad U zero and Tr(J Hess U)=0; the cutoff derivative adds only another multiple of the same zero product. Therefore div c=0 and c.grad F=0, proving div(mu*c)=0. The proposed positive-part fourth-power cutoffs are C3, not C-infinity; this is sufficient regularity for these local identities and standard diffusion/form arguments, but a parser advertised as requiring smooth C-infinity inputs should instead use such cutoffs or explicitly admit C3. The source already makes finite-description parsing a separate, unearned step.

A nonzero y drift, changed diffusion/invariant density, partial-fiber targets, time-dependent stirring, or an unbounded field without new domain estimates is outside this receipt. No physical control feasibility or rate-normalized resource cost is certified. The already reviewed parallel factor may be received separately; this candidate's conservative radial factor is sufficient as written.

## Prior comparison and checks

I opened the primary Landim–Mariani–Seo paper, https://arxiv.org/html/1701.00985, including its assumptions and Section 3 energy/flux identities (Lemma 3.1 and equation 3.7). It supplies established non-selfadjoint capacity theory, not automatic coverage of these unbounded-fiber basins. The slab Poincare, trace exhaustion and compact perturbation receiving above are the specific missing hypotheses that must be supplied here. No novelty claim follows from this review.

Separate exact diagnostics are in `reviewer_audit/check_stirring_and_graph.py` and `checks.json`: 4,703 checks including 1,098 small graphs for the companion note, plus the explicit nonradial stirring divergence/tangency and exit-generator identities. These are algebra checks, not a PDE numerical certificate or a replacement for the weak-form proof. Both frozen root sources remained unchanged.
