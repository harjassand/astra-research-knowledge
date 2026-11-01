# Root next construction: a paid energy-sensitive clock trial

Status: NEW candidate mechanism, not accepted. Current finite retained-clock witnesses have substantial errors; this asks whether a stronger actual trial/dual pair improves the SAME physical model. Ordinary conditional committors and Dirichlet/Thomson methods are components.

Let u=U(z), b=1/2, and I(u)=int_-b^b exp(beta*u*v(t))dt. Use the explicit trial

 h_u(y)=int_y^b exp(beta*u*v(t))dt / I(u),

extended1 on A and0 on B. It is the frozen-z longitudinal committor, NOT the actual full committor. Homogeneity cancels the unknown angular partition in its longitudinal Dirichlet cost:

 C_frozen=beta^(alpha-1)/Gamma(alpha) * int_0^infinity u^(alpha-1)/I(u)du.

The complete Dirichlet price also includes the strictly charged transverse term

 beta^-1 int |partial_u h_u(y)|^2 * grad U^T M_z grad U * w(y,z) dy dz.

Ignoring that term would change the generator and invalidate the argument. Arbitrarily large unknown coefficients/M_z cannot be assumed harmless to this refined trial.

## Obtain a usable derivative price from the actual raw pair-quartic program

For U=sum_i d_i z_i^4+sum_edges g_ij z_i^2 z_j^2 with d_i>=dmin>0, g_ij>=0, and diagonal M_z=diag(mu_i),

 tr(M_z Hess U)=sum_j c_j z_j^2,
 c_j=12 mu_j d_j+2 sum_{i:ij edge}mu_i g_ij.

Hence tr(M_z Hess U)<=||c||_2 * sqrt(U/dmin). All c_j are read/constructed from the actual program; no optimal coercivity or angular expectation oracle is supplied.

A sharper route than a crude pointwise gradient bound is weighted integration by parts. For fixed y, let g(u)=|partial_u h_u(y)|^2 and

 F(u)=int_u^infinity exp[-beta v(y)(s-u)] g(s)ds.

Then beta v F-F'=g, and, provided the ordinary cutoff/tail receiving is earned,

 int g(U) grad U^T M_z grad U exp(-beta v U) dz
 = int F(U) tr(M_z Hess U) exp(-beta v U) dz
 <=||c||_2/sqrt(dmin) * int F(U)sqrt(U)exp(-beta v U)dz.

The final radial integral is one-dimensional by the same homogeneous coarea identity. This retains the average derivative scale instead of charging a worst-direction bound of order U^(3/2). The actual y,u,F integrals and tails, g behavior near u=0, all roots/precision, failed refinements and coefficient-reading work remain to be constructed and paid.

## Matched dual and unresolved burden

For a constant barrier flux fiber pi_a proportional to exp(-beta a U), the longitudinal resistance is R_a=int_S [a^2/(2a-v(y))]^alpha dy where 2a>max_S v. A formal Laplace calculation suggests choosing a=v*(1-1/(2alpha)) reduces the leading excess R_a/R from3/(4alpha) to1/(2alpha), while C_frozen/C0 has leading correction -1/(2alpha). These matching first-order terms could cancel in the energy/inverse-energy product. They are NOT received finite-error bounds or an actual kinetic correction yet.

The old well redistribution/source current must be reconstructed for the new a below v*. Its old a=v* bounds cannot simply be copied. The new global odd trial also changes the slab source residual; it needs a new actual current or separately proved inverse-form bound. A finite-bit receiver must integrate the complete primal/dual costs and refuse if the transverse cost or required work removes the gain.

For the existing nearest-neighbor pair-quartic fixture with unit mobility and coupling20, c_j is92 at interior sites and52 at endpoints. This is an exact acquired derivative datum, not a claim that the final error is already small. It is legitimate to exploit this actual structure, while retaining the stronger arbitrary-angular uniform theorem separately. No higher-dimensional or different-physics fixture is required to hide the current15%/45% acceptance limits.
