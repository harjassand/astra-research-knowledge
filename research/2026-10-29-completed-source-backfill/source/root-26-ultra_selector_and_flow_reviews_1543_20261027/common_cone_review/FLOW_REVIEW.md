# Accepted: pure-target obstruction for constant coercive coupled flows

For the exact symmetric target in `EXACT_SYMMETRIC_TARGET.json`, root
accepts the following wider representation obstruction. There is no real
constant-coefficient output-coupled second-order flow with uniformly
positive symmetric principal symbol, gamma≥0, closed quadratic two-form
omega and PSD Gram R on the 24 bilinear A_i y_j features such that

    E_C(F−gamma det²)(A,y)+omega_A(B1,B2)=Z24^T R Z24.

This statement concerns the PURE target F−gamma det². It does not exclude
an arbitrary decomposition into an unknown PC energy and an unknown
energy certified by an unknown flow. It does not exclude non-SOS
nonnegative densities, more general form corrections, nonlinear flows,
or quasiconvexity itself.

## Reduction of the flow family

Write u_t=sum C_jk partial_j partial_k u with real 2-by-2 output matrices,
symmetric in j,k; an antisymmetric spatial part is irrelevant because
partial derivatives commute. The symmetric part of the principal symbol
is assumed bounded below by delta |xi|² I for some delta>0. This is the
coercivity hypothesis used here; a weaker spectral-stability condition
is not silently substituted.

The actual target and det² are invariant under left output rotations,
input column swap, and the paired reflection A→DAD, D=diag(1,−1).
Root checked both discrete invariances by literal polynomial substitution.
Conjugating a hypothetical identity by these symmetries preserves
compatible jets, closed forms, PSD Grams and the stated principal-symbol
lower bound. For this FIXED invariant energy, dissipation is linear in C,
so averaging identities also averages operators.

Output quarter-turn averaging makes every block C_jk lie in span(I,J),
J=[[0,−1],[1,0]]. Write C_jk=A_jk I+B_jk J with A,B symmetric spatial
matrices. Input swap imposes A=SAS and B=SBS. Paired reflection imposes
A=DAD and B=−DBD. Thus A=aI and B=bS. Coercivity gives a>0. Dividing
the identity by a reduces the entire family to

    u_t=Delta u+2b J partial12 u,              b arbitrary real.

These normalized flows preserve gradient compatibility. Their Fourier
symbol has symmetric part −|xi|²I, so every nonconstant periodic mode
decays; output rotation from the skew part does not prevent decay.

The bilinear dependence on an energy and its operator is why this
averaging cannot be reused for a simultaneously unknown energy component
and unknown operator. The completed earlier common-cone theorem used
identity diffusion, which commutes with its component-energy averaging.

## Compact gamma range and the exact parameter family

Any proposed density certificate implies quasiconvexity by integration
along its decaying flow: the closed-form integral vanishes, energy is
nonincreasing, and the limit is the affine-background energy. Approximation
transfers the periodic smooth statement to the usual gradient test class.
It therefore implies rank-one convexity.

The peer's `GAMMA_BOUND.json` provides one exact rational A and rank-one
H=e1 tensor eta. Root differentiates the literal F and det² and obtains

    D²(F−gamma det²)(A)[H,H]
       = D²F(A)[H,H]−2 gamma (cofA:H)².

The nonzero cofactor pairing forces gamma at most the exact stored ratio,
which is at most G=25117/100000000. No global optimizer or sharpness claim
is needed. Thus every hypothetical certificate has 0≤t=gamma/G≤1.

The exact family certificate is
`quartic_alternative/combined_full_cone/output_flow_extension/EXACT_FLOW_FAMILY.json`,
SHA256 `1791139d3cde668f22854406f99e62189d2dc39c7f327cd7df4a59073a9fa15e`.
It supplies L(t)=L0+tL1 on all 210 A²y² monomials. Root's independent
SymPy QQ replay, importing no author map or verifier, establishes:

* the 24-by-24 moment matrices at t=0 and t=1 are strictly PD, with all
  48 pivots and full matrices independently reconstructed;
* for each L_i and each of all 60 quadratic two-forms, its pullback value
  is eta_i applied to the literal exterior derivative. Every closed form
  is consequently annihilated;
* all three coefficients of L(t) E_J(F−Gt det²) are exactly zero;
* all three Bernstein coefficients of the quadratic polynomial
  L(t) E_I(F−Gt det²) are strictly negative on [0,1].

The moment matrix at any intermediate t is a convex combination of the
two positive endpoint matrices. Hence L(t) is nonnegative on every
admitted bilinear SOS. It annihilates every closed correction and the
entire b-dependent mixed dissipation. Its value on the remaining identity
dissipation is strictly negative throughout [0,1]. Applying it to a
hypothetical identity gives a contradiction for every real b and every
admitted gamma. The rank-one bound already excludes larger gamma.

This completes the pure-target theorem under the precise class definition.
The exact replay took 0.328 seconds; `INDEPENDENT_FLOW_REPLAY.json` records
the rational facts. The separate 35-dimensional perturbation theorem in
`ATOMIC_REVIEW.md` concerns ROC and polynomial-selector impossibility.
This flow theorem is NOT promoted to that whole box, because its operator
averaging uses actual symmetries of the exact symmetric target.
