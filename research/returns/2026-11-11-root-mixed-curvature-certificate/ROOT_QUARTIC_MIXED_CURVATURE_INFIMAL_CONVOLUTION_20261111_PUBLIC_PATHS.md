Original-row mixed curvature, kernel defects and a finite certificate

Mathematical source binding. Use the original J_k, ell=3k-1,n=k+1, and the complete P1 second-row Bregman allocation
 B_F(z)>=theta z^T H_F z+[1-2/(3(1-2theta))]q_k(z), 0<=theta<=1/6,
 H_F=D_y^2 J_k(F)>=0,
 q_k(z)=ell[k^2 z1^4+2z1^2z2^2+z2^4]/(8n).
This is one allocated original remainder, not two independent reserves. Its full optimized Psi_F remains available. The calculation below selects one simpler minorant of it; it is not asserted to improve Psi_F pointwise.

1. A mixed minorant without a positive Hessian floor.

Let gamma=ell min(k^2,1)/(24n)>0. Since q_k>=3gamma|z|^4, theta=1/12 gives
 B_F(z)>=mathcal F_H(z):=z^T H z/12+g|z|^4,
 g=3gamma/5, H=H_F.
This remains valid at every degenerate row Hessian, for all real F and k>1/3. It requires no orientation condition, adapted Hessian, L4 constitutive stress or artificial positive quadratic floor.

Define C_a=3/(4^(4/3)a^(1/3)). Convex conjugation of the sum gives the exact infimal convolution
 mathcal F_H^*(e)
 =min_(r in range H){3 r^T H^dagger r+C_g|e-r|^(4/3)}.             (1)
The minimum is attained. The quadratic conjugate is infinity off range H; the quartic conjugate is finite continuous everywhere, so the finite-dimensional sum-conjugate formula has no closure gap. Equation (1) splits a stress error into a curvature-paid part and a quartic-paid part. A nonzero component in ker H no longer makes the entire quadratic estimate unusable: it can be left in e-r. The coefficient3 comes from THIS allocated quadratic reserve, not the stronger coefficient3/2 available when the whole remainder is assigned to curvature. There is no claim that (1) uniformly beats both extremal bounds with their different constants.

For any actual candidate F0=(a+Df;b+Dg0), any solenoidal tau in L^(4/3), and e=D_y J_k(F0)-tau, integration against D(g-g0) gives
 m(f;a,b):=min_g integral J_k(a+Df,b+Dg)
 >=integral J_k(F0)-integral mathcal F_(H_F0)^*(e).                (2)
Natural L4--L^(4/3) regularity suffices: the conjugate is bounded above by C_g|e|^(4/3). The right side does not assume a bounded inverse Hessian. Its defect is NOT known to be paid by integral J_k(F0)-J_k(A) for arbitrary f, means and k. A negative lower bound in (2) is not a negative original gap.

2. A one-scalar pointwise representation, not an exact-real oracle.

The unique maximizing z solves
 e=(H/6)z+4g|z|^2z.
For e=0 it is z=0. For e!=0, put lambda=4g|z|^2>0. Then
 z=(H/6+lambda I)^(-1)e,
 lambda=4g|(H/6+lambda I)^(-1)e|^2.                            (3)
The left side increases strictly; the right side decreases on lambda>0. There is exactly one root. The interval (0,1+4g|e|^2) brackets it: the inverse norm is at most1/lambda, and L^3>4g|e|^2 for L=1+4g|e|^2. This uses a two-by-two positive matrix inverse at positive rational lambda, never H^dagger evaluation at a singular point. The value is
 mathcal F_H^*(e)=z^T H z/12+3g|z|^4.                          (4)
For rational data, bisection with rational comparisons gives the root. To approximate z, one can continue until both rational endpoint vectors in (3) differ by the requested absolute accuracy; continuity at the strictly positive root proves termination. No uniform bit bound independent of tiny e, g or conditioning is asserted. No numerical execution of (3) has been made here.

3. Finite Fourier integrated upper and lower certificates.

Even pointwise root evaluation is unnecessary in the final integrated certificate. For ANY finite Fourier trial w(x), set
 r_w=e-Hw/6-4g|w|^2w,
 L_w=e.w-mathcal F_H(w).
The Euclidean quartic Bregman inequality is
 |w+d|^4-|w|^4-4|w|^2 w.d >= |d|^4/3.
Indeed, divide by |d|^4, write w/|d|=a d/|d|+b with b perpendicular to d, and minimize6a^2+4a+1+2|b|^2 at a=-1/3,b=0. Adding the nonnegative quadratic Bregman term proves
 mathcal F_H(w+d)>=mathcal F_H(w)+Dmathcal F_H(w).d+(g/3)|d|^4.
Hence the ACTUAL finite two-sided pointwise certificate is
 L_w <= mathcal F_H^*(e) <= L_w+C_(g/3)|r_w|^(4/3).             (5)
For rational k, rational finite Fourier rows and stress, H,e,w,r_w and L_w have rational finite Laurent coefficients. The integral of L_w is the exact constant Laurent coefficient. The fractional-moment upper bound in the complete row-solver construction applies to r_w: choose rational M>=||r_w||infinity and majorize M^(4/3)z^(2/3), z=|r_w|^2/M^2 in [0,1], by the paid Bernstein polynomial with rational upward cube-root enclosures. The displayed degree choice N>=max(1,ceil(2M^4/rho^3)) gives integrated excess at most rho after the stipulated coefficient rounding is included. This incurs the actual convolution degree, arithmetic and coefficient-bit costs; it is not exact quadrature or a norm oracle. Rational bounds for C_(g/3), obtained by cube-root enclosure, add a paid absolute integral error.

For a chosen w, let U_w be that rational upper bound on the integral in (5). Then
 m(f;a,b)>=integral J_k(F0)-U_w.                              (6)
Any strictly positive margin relative to J_k(A) is a genuine certificate for that input first row and means. No search was run and no positive margin is claimed in this note. Searching finite Fourier w, g0 and solenoidal tau remains an actual unbounded search unless a successful-stage bound is separately established. Unlike replacing the stress topology by L4, (5) has exactly the natural residual topology. It combines curvature and quartic payment within one allocated original Bregman remainder.

4. Interface with the new compatible corrector.

At k=1,A=I, the actual Fourier second-row corrector
 g0=-2 Delta^(-1)partial_12 f
annuls the linear gradient stress. For a fixed smooth f scaled by a, the remaining gradient stress is O(a^2), rather than O(a). When the row Hessian is uniformly positive on this fixed small-amplitude neighborhood, (1) may take r=e, so the defect is O(a^4), versus the pure quartic estimate O(a^(8/3)). The old uncorrected pure-quartic estimate would be O(a^(4/3)). Constants depend on that fixed smooth profile and neighborhood; this is not a uniform-amplitude or concentration-free theorem. At degeneracy (1) still retains a finite quartic payment for the uncurved stress component, but there is no proof that this component is globally small enough. This identifies the genuine remaining operation: a compatible first-row reserve paying the mixed stress defect for arbitrary amplitudes/means/k, or a different universal representation or actual negative witness.

5. Source and scope.

The complete P1 continuation supplies the mixed Bregman allocation, optimized Psi, natural row duality, compatible linear corrector, paid fractional integral and total conditional minimizer enumeration. The present infimal convolution, scalar resolvent and trial-field two-sided certificate are deductions using those actual operations, not newly imported external theorems. The earlier all-k compatible range condition b_G perpendicular ker H_G remains accepted; the unresolved all-mean sharp comparison is b_G^T H_G^dagger b_G<=2c_G. Do not turn a previously paid range condition into a new gate.

Agazzi et al., https://arxiv.org/html/2609.28311v2, Theorem1/Corollary2 was refreshed at its arbitrary-mean periodic vector-gradient/vector-potential Burkholder scope. It does not itself identify this anisotropic original quartic with a touching quasiconvex minorant. Finite-affine and regular-core exclusions leave nonlinear, infinite and field-dependent constructions available. A conditional optimizer, several complete positive compatible families, or failure of the mixed certificate does not resolve the universal original inequality in either direction.
