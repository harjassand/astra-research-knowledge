# Critical joint-cap certificate review

I read `certify_joint_cap.py`, its retained output, the interval arithmetic it uses, and the proposed governing argument. I reran the joint-cap script successfully. I found no substantive error in the finite optimum certificate at C_CM<=1/20 and total internal springs<=24.

The extra moment has the correct normalization. With `A=T=4` and `S=4`, source F's exact incident-stiffness formula gives

`E = integral 4*w^3*chi(w) dw = sum(beta_j^2-alpha_j^2) = 16+8*kappa_incident`.

Every positive graph with total internal spring constant at most 24 therefore has E<=208. The candidate star has all internal springs incident on the backbone and sum exactly 24, so E=208. The dual divided by w^3 contains `+4*nu*w^3`, whose integral is `nu*E`; its comparison is exactly

`J-J* = integral R*(chi-chi*) - nu*(E-E*) - eta*(D-D*) >= 0`.

The negative trace multiplier is harmless because the trace equality cancels it; the required inequality multipliers nu and eta are both certified positive.

The spring parameterization is the plus solution of

`C*H^2 + (1-2*h-24*C)*H + 24*h^2 = 0`,

which is equivalent to `h^2/H+(1-h)^2/(24-H)=C`. All displayed mass/spring enclosures are strictly positive. Their sum and compliance are therefore exact algebraic constraints, not numerical residual assumptions. The five endpoint intervals are strictly interlaced. Each of the three disjoint cubic root brackets has opposite signs, exhausting the degree-three polynomial. Breaking bisection when an interval midpoint contains zero retains the previous valid bracket and does not invalidate root enclosure.

The power-series exceptions at n=1 and n=2 are correct: the mu term starts at degree four and the nu term starts at degree six. For n>=3 the nu coefficient is exactly `nu*n*(n-1)*(2*n-1)*(2*n-3)`. The certified even-coefficient signs, together with constant -eta and the lone positive odd coefficient at degree three, have exactly five sign variations. For the quartic P(n),

`P'''(n)=nu*(96*n-72)>0` for n>=14.

The positive certified P'(14) and P''(14) make P strictly increasing thereafter, while the negative eta contribution to B_n also strictly increases. B14>0 therefore proves the whole infinite coefficient tail positive. The finite-sign-variation lemma gives at most five positive roots counted with multiplicity. At the exact h supplied by the fifth-edge residual sign bracket, the five known positive edges exhaust this count and are all simple. Their alternating signs give exactly the candidate's three bands on the full frequency axis.

The objective enclosure is `J_joint in [1.142016098461582733349079,1.142016098461582733349080]`. Since the unique active minimizing spectrum has three nonzero-width bands, its minimal active star has two pendants; one pendant cannot reproduce it. This does not preclude equivalent realizations or added dark modes.

No full phase diagram, broad material advantage, or historical priority is established. The conclusion is a finite, attained, all-topology optimum at the stated joint resource point within the scalar harmonic ideal-contact model.
