# Volume-independent finite-time local field control for the actual gauged interactions

2026-11-03. This strengthens the finite-box gate without claiming the missing local mirror splitting. All identities are for the actual compact-link Hamiltonian and the compiled finite-charge interacting matter terms of FINITE_TIME_QUANTUM_LINK_GATE.md.

Let

 H=g²/(2a) Σ_l E_l² +1/(g²a) Σ_p(1−Re U_p)+h(U),
 U_p=Π_l U_l^(s_pl), [E_l,U_p]=s_pl U_p,
 ||∂_l h||≤J_l.

Define rescaled electric and curvature operators

 e_l=g E_l,   B_p=(U_p−1)/g.

The operator e_l is unbounded. Neither the electric spectrum nor gauge link Hilbert space is truncated. B_p is bounded at each nonzero g, but its norm2/g is NOT used as a smallness estimate.

## Exact equations and state-dependent inequalities

For a normalized finite-energy state ψ(t), set x_l(t)=||e_lψ(t)|| and y_p(t)=||B_pψ(t)||. Work first on the smooth electric core. The Heisenberg equations give

 dot e_l=−(1/(ag)) Σ_p s_pl sin F_p −g ∂_l h,
 dot B_p=(i/(2a)) Σ_l s_pl U_p (2e_l+g s_pl).

Signs do not affect the following bounds. The first uses the EXACT inequality

 ||(sin F_p/g)ψ||≤||B_pψ||,

because sin F=(1+U†)(U−1)/(2i). The second uses unitarity of U_p, not a bound on E. For the upper Dini derivatives of the norms,

 D⁺x_l≤a^-1 Σ_(p∋l)y_p+gJ_l,
 D⁺y_p≤a^-1 Σ_(l∈p)(x_l+g/2).

No commutation of the interacting h with E is assumed. It commutes with U_p because h is matrix-valued multiplication in link coordinates. Closed-form-domain approximation extends the inequalities to finite local second moments.

Let z=max(number of plaquettes incident on a link,number of links in a plaquette), J*=sup_l J_l, and m0=sup_l,p{x_l(0),y_p(0)}. On a cubic spatial lattice z is a fixed coordination number, independent of volume. Gronwall gives

 m(t):=sup_l,p{x_l(t),y_p(t)}
 ≤exp(z|t|/a)[m0+g(J*+z/(2a))|t|].

The same estimate applies to infinite volume by uniform finite-volume approximation whenever such an initial state and dynamics are supplied. The statement does not claim their construction from the interacting ground state automatically.

Consequently, for any finite collection C of plaquettes and any0<ε<π,

 Pr(max_(p∈C)|Arg U_p|≥ε)
 ≤ |C| g² m(t)² /[4sin²(ε/2)].

This bound is local: C is a chosen physical region and no factor from the total lattice volume appears. It is exactly insensitive to large pure-gauge link angles. A state with finite rescaled electric/curvature density therefore remains locally weak-curvature for finite time at weak coupling, even though its total gauge zero-point energy is extensive and E bandwidth infinite.

## Why this is stronger than the naïve gauge LR estimate

A direct bounded-interaction Lieb–Robinson estimate treats the magnetic norm1/g² as a propagation velocity. The differential inequalities above instead combine electric and magnetic coefficients into their physical frequency1/a. Their growth rate does not diverge as g→0. This is only a local second-moment propagation estimate, NOT by itself a full Lieb–Robinson bound for coupled matter observables.

## What remains missing for actual mirror decoupling

A local curvature bound does not construct a local mirror projector. The previously acquired parent is a gapped two-massed-face block. Its global ground projector and the spanning-tree finite-volume perturbation threshold deteriorate with volume and cannot be inserted into this local field estimate to claim a fixed-coupling theorem.

The next necessary object is a gauge-covariant family of local/quasilocal mirror defects M_x(U), with:

1. A coercive mirror excitation estimate independent of tangential volume and normal thickness, while a desired light face remains gapless.
2. Link derivative bounds localized near x, controlling Σ_l ||∂_l M_x|| and second derivatives, rather than derivatives of a whole-system ground projector.
3. A continuity equation or local response estimate for [h(U),M_x] so its time evolution can be controlled using the local field moments above; M_x need not commute individually, but its currents must be controlled.
4. A Gauss-invariant low-mirror state with uniform local x_l,y_p bounds. The finite-box initial wavepacket exists explicitly, but its global spanning-tree electric dressing does not establish a uniform infinite-volume preparation.

Our global Gaussian purification W at zero links does not automatically provide these: it is not a symmetric finite-depth unitary, gauging its nonsymmetric generator is not the same as gauging the symmetric Hamiltonian, and simply replacing h by sign(h) when the desired face is gapless loses the uniform locality premise. Likewise, declaring the gauge field slowly varying does not control quantum electric transitions. These are precise remaining operations, not an anomaly condition.

An energy-only mirror leakage theorem fails because the gauge vacuum energy is O(V/a). The finite-box commutator theorem avoids that error and the present local moments avoid the spurious g^-2 propagation rate, but neither has yet closed items1–4. The strongest established anomaly-free Abelian overlap measure remains the relevant baseline, not a mere reduced SMG toy model.

## Independent algebra audit and crucial actual-resource qualification

Independent audit confirmed both commutators and the finite-energy-domain extension. It also identified an essential resource qualification: the bound is structurally independent of total volume ONLY when J*=sup_l||∂_l h|| and the interaction incidence are uniform. Our currently paid auxiliary cutoff N and, in its finite-volume compression variant, range R can grow with volume. Thus q_x and J_l for THAT sequence can grow with volume. Insert their actual acquired values; do not advertise a volume-uniform gauge theorem for that sequence. A fixed finite-charge, fixed-range model obeys the volume-independent moment statement, but a fixed-capacity thermodynamic mirror model has not yet been supplied. This is a second independent reason the local moment estimate does not close the intended fixed-coupling consequence gate.
