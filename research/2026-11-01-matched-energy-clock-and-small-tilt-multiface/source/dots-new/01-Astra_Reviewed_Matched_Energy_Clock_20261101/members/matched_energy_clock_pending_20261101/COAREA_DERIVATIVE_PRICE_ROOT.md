# Root exact coarea derivative price for the energy-sensitive trial

Status: NEW conditional lemma, independent review pending. The following coarea identity is exact; the final scale estimate is only a diagnostic, not a received finite bound.

Let U be smooth positive homogeneous quartic on R^m, alpha=m/4, with positive coercivity, and constant symmetric positive D. For u>0 define

 A(u)=int_{U=u} (grad U^T D grad U)/|grad U| dS,
 B(u)=int_{U=u} tr(D Hess U)/|grad U| dS.

Euler's identity ensures grad U!=0 on every positive level. The divergence theorem on the bounded smooth sublevel and homogeneity give

 A(u)=int_{U<=u} tr(D Hess U) dz
     =int_0^u B(v)dv =u B(u)/(alpha+1/2).

Here B(v)=v^(alpha-1/2)B(1), since Hess U has degree2. Division by the ordinary coarea density shows

 E[grad U^T D grad U | U=u]
   =u/(alpha+1/2) E[tr(D Hess U)|U=u].

These are geometric conditional averages on the energy shell; they do not assume stochastic angular equilibration or require an angular sampler.

For the received diagonal-mobility pair-quartic class from FROZEN_FIBER_VARIATIONAL_ROOT.md, tr(D Hess U)<=||c||_2 sqrt(U/dmin). Hence

 E[grad U^T D grad U | U=u]
 <= ||c||_2 u^(3/2)/[(alpha+1/2)sqrt(dmin)].

Consequently the COMPLETE transverse Dirichlet cost of h_u is bounded by the explicit two-dimensional scalar integral

 C_trans <= beta^(alpha-1)||c||_2/[Gamma(alpha)(alpha+1/2)sqrt(dmin)]
   *int_-b^b int_0^infinity u^(alpha+1/2)
       |partial_u h_u(y)|^2 exp[-beta v(y)u] du dy.

This also follows by swapping the nonnegative integrals in the earlier F(u) integration-by-parts price; it eliminates the apparent third integration. Unknown transverse partition factors cancel. All unbounded scalar tails, derivative quadrature, floating/finite-bit precision and acquired c coefficients remain to be bounded in a real receiver.

Diagnostic only: a Gaussian barrier expansion predicts relative C_trans/C_frozen of leading order ||c||_2 sqrt(beta) v*^(3/2)/[16 kappa sqrt(dmin) alpha^(5/2)]. For bounded-degree bounded-coefficient pair programs, ||c||_2=O(sqrt(m)), giving O(alpha^-2). For the actual unit-mobility path-coupling20 fixture this rough leading estimate is about32.5/alpha^2, not a finite rigorous admission. Neither cancellation with the optimized dual nor a new target accuracy has been earned by this note.
