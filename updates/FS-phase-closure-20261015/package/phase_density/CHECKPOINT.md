# Continuation state: phase-density route

## Established in this investigation

1. For any homogeneous rank-one-convex F and any fixed smooth unit direction field n(x), E(rn) is convex in rho=r^p. This does not require output invariance or quasiconvexity. Section 2 of the main note has the complete short proof.
2. The exact direction-preserving Picone identity is equation (3.1); quartic remainder (3.2) has coefficient mu_F/3. General analytic positivity is not delegated to the exact checker.
3. For quartic mu_F>0, fixed-direction, fixed-fourth-mass amplitude minimization with prescribed admissible boundary values is convex and attained. Constant target translation puts every smooth planar affine-boundary test into this representation. Replacement cannot increase energy. Strict positivity of minimizers is NOT established.
4. In planar output-invariant form E_theta(rho)=int rho f_grad(theta)(grad rho/(4rho)). Reference sigma gives scalar dual g_sigma and all-amplitude inequality (5.3), with a quantitative positive remainder.
5. For the explicit G and coupled phase theta=y+3sin(x)/25+sin(y)/10+2sin(x+y)/25, the supplied rational sigma certifies sigma>1/10 and g_sigma>=1 on the whole torus. Adaptive interval proof completed; input is phase_density_certificate.json. This is a fixed-phase theorem at zero affine background, not the full problem.
6. Joint phase-density convexity is FALSE: even F=|A|^4 has Hessian [[1,8],[8,18]] at the explicit constrained two-parameter field of Section 7. Alternating minimization is not a global solver for the complete problem.

## Exact/interval evidence

- verify_directional_density.py: ten exact algebra groups; passed.
- audit/prior_replay.log: preceding universal-profile checker, ten groups; passed.
- certify_adaptive_dual.py: complete adaptive cover, 6,550,288 tested cells, no unresolved cells, terminal denominator8192. It uses outward-rounded IEEE arithmetic and rational Taylor trigonometry; it is NOT a proof-assistant proof.
- certify_phase_density.py 512: rigorous candidate-energy upper bound below25/8. Its pointwise dual bound is inconclusive; do not substitute it for the adaptive proof.

## Actual failed negative search

Six smooth sine-basis affine-boundary tests were minimized in alternating convex density and phase blocks. No negative result; all returned close to affine. These experiments are limited and quadrature based. Saved complete results: dirichlet_search.json. Do not treat 1e-12-scale values as certified positive margins.

## Audit of a potential external premise

The displayed Step2 of Proposition6.1 in Pedregal arXiv1905.06571v4 passes from full span of a positivity-feasible set to equality with the whole vector space. A proof that the required nonnegative weights survive is missing from that inference. No counterexample to the proposition was constructed; no conclusion on community acceptance is claimed. Do not import the complete theorem.

## The exact next mathematical obligation

For arbitrary admissible direction n (or phase theta after a target translation) and affine boundary Bx+c, bound the attained fixed-mass scalar amplitude minimum below |Omega|F(B), or find one that is smaller. A sufficient certificate is a scalar flux j whose interior Fenchel residual and fixed boundary term in equation(5.5) give that bound. A valid continuation must derive such fluxes uniformly or discover a negative direction; defining the minimum or calling it a ground-state energy is not progress by itself.

The directional replacement is global, but the remaining direction optimization can have correlated negative interactions. Small phase is not a uniform simplification: large target translations make every test have small phase while preserving its gradient. Do not repeat local profile densities, fixed Poisson actions, single-carrier proofs, or another positive finite graph.

No negative compatible cycle/Dirichlet witness has been established. No universal quasiconvexity theorem, external review, proof-assistant verification or priority clearance is claimed.
