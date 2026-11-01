# Separate candidate note: global envelope without derivative reconstruction

Status: mathematical extension candidate only. The finite receiver still
acquires the narrower explicit fixed-atom-weight family and does NOT accept an
unproved arbitrary-envelope assertion. No earlier freeze is altered.

Let an ACTUAL C^2 potential F on finite-dimensional Euclidean space satisfy
v(y)U(z)<=F(y,z)<=b(y)U(z) globally, with U,v,b as in the localized-envelope
candidate. Let the actual diffusion mobility be a finite constant SPD block
matrix diag(1,M_z). The density w=exp(-beta F)/Z0 is strictly positive, locally
smooth, and has finite total mass because w<=w_v and q_v is integrable.

Consider the regular symmetric form obtained by closing C_c^infinity in
E(f)=beta^-1 int grad f^T D grad f w. Choose smooth Euclidean cutoffs chi_R,
0<=chi_R<=1, equal1 on the radius-R ball, supported in the radius-2R ball,
with |grad chi_R|<=C/R. Then

 ||chi_R-1||_(L2(w)) ->0,
 E(chi_R)<=C^2||D|| int w/(beta R^2) ->0.

The form norm makes the cutoffs Cauchy, so1 lies in the closed form domain and
E(1)=0. Spectral calculus gives P_t1=1: the symmetric semigroup is conservative.
The same cutoffs earn invariance of the finite measure. There is no Poincare
constant, detailed derivative bound, or uniform upper bound on ||D|| across the
family required; each actual matrix is finite and the argument is per model.

The closed-form process agrees locally with the smooth uniformly elliptic
Langevin SDE. Its minimal SDE cannot lose mass through explosion for w-almost
every initial point. For a deterministic initial point, local existence gives
P_x(tau_explosion>delta)->1 as delta decreases to0. At any positive delta,
the surviving local transition has a density and hence puts zero mass on the
exceptional w-null set. The Markov property and conservative almost-everywhere
law give P_x(tau_explosion>t)>=P_x(tau_explosion>delta), for0<delta<t.
Letting delta decrease to0 proves nonexplosion from every point. Thus the
actual global reversible diffusion is received, not merely a formal operator.

All source/current inequalities in the main candidate use only w_b<=w<=w_v,
not its special F=vU+e*gV expression. The explicit source is w_v1E, the price
uses w_b, the actual trial energy uses w_v, and actual initial-law masses are
bounded between the scalar integrals. Consequently the same finite mean/CDF
bounds extend at theorem level to ANY genuinely received global smooth
potential envelope above, even if F has angular or longitudinal derivative
oscillations that make the simple quadratic Lyapunov estimate inconvenient.

This observation does NOT acquire the global envelope from finite local
measurements, authenticate physical calibration, or supply an unrestricted
positivity oracle. It also does not admit state-dependent unbounded mobility,
cross-mobility, nonreversibility, nonsmooth drifts or arbitrary initialization.
The fixed-weight raw program remains the concrete consumer until another
entire program can certify this stronger interface. The argument uses ordinary
Dirichlet-form cutoff/conservativity machinery, not a novelty claim.
