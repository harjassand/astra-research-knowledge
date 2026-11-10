ROOT mathematical preparation, 10 November 2026
Local quadratic Fisher metrics and the product-minimum interface

SCOPE. This is a representation obstruction, not an obstruction to finite-mass Landau-Coulomb Cauchy theory. It does not rule out nonlocal, nonlinear, time-dependent, correlation-dependent, or nonmonotone continuation arguments.

1. GENERAL PRODUCT-MINIMUM RIGIDITY.
Let G(v,w) be a smooth symmetric nonnegative 6-by-6 matrix, in blocks A,C,C^T,B, and put
 J_G(F)=integral F (grad log F)^T G (grad log F).
Use positive smooth probability densities and compactly supported, zero-marginal variations; assume the displayed local integrals exist. Suppose EVERY product f(v)g(w) minimizes J_G among joint densities with these same two marginals. Then necessarily
 C=0, A(v,w)=A(v), B(v,w)=B(w).
Conversely those block metrics do have the product-minimum property.

Proof. At a product write log F=a(v)+b(w), p=grad a, q=grad b. The first variation is
 V=-2 div(G(p,q))-(p,q)^T G(p,q).
Every smooth compactly supported zero-marginal signed variation is admissible for both signs at sufficiently small amplitude. Hence V must be a sum of a function of v and a function of w; equivalently each rectangular difference of V vanishes. This follows directly by testing tensor products U(v)W(w) with integral U=integral W=0, and taking shrinking bumps away from a boundary.

The coefficient of the arbitrary Hessian of a at v_1 in such a rectangle is -2[A(v_1,w_1)-A(v_1,w_2)]. Smooth log densities can prescribe that jet at v_1 and zero jets at v_2, with positive integrable tails unchanged outside compact sets. Thus A is independent of w. The same argument makes B independent of v. Now vary the gradient of a only at v_1 and the gradient of b only at w_1. The mixed coefficient in the rectangle is -2 p^T C(v_1,w_1)q. Divergence terms are linear in these two independently varied jets, so cannot cancel it. Consequently C=0 everywhere.

For the converse, conditional Jensen gives
 integral F |grad_v log F|_A(v)^2 >= integral f |grad log f|_A(v)^2,
and the corresponding w inequality. Their sum is exactly the asserted minimum. This also proves the statement for semidefinite block metrics by approximation.

2. CONSEQUENCE FOR THE ANGULAR CORRECTION.
If in addition the joint metric is invariant under common velocity translations and simultaneous rotations, the only metrics above are constant a I on the v block and b I on the w block. Requiring the physical common-temperature Maxwellians to minimize the functional at fixed total mass-weighted energy forces a:b=m_i^-1:m_j^-1. To see this, restrict to centered Gaussian products of variances sigma_i^2,sigma_j^2. Minimize 3a/sigma_i^2+3b/sigma_j^2 at fixed 3m_i sigma_i^2+3m_j sigma_j^2; the minimizer has sigma_i^2:sigma_j^2=sqrt(a/m_i):sqrt(b/m_j), which equals m_i^-1:m_j^-1 only for the claimed ratio.

Therefore a nonconstant relative-angular quadratic correction cannot both repair pair dissipation and retain the universal fixed-marginal product-minimum interface. The explicit Gaussian bump rectangle in the completed P3 answer is one concrete instance; the argument above identifies the whole local quadratic metric limitation. It makes no claim about other lifting mechanisms or arbitrary functionals.

3. THE PAIR CONSTANT IS NOT AN EVOLUTION EXPONENT.
For a pair angular generator proportional to r^gamma Delta_S2, the radial square completion leaves gamma^2 Gamma/4 against lambda Gamma_2. The unrestricted spherical inequality integral F Gamma_2 >=2 integral F Gamma therefore permits lambda>=max(1,gamma^2/8). Coulomb gives lambda=9/8. This reconstructs the constant from the actual spherical threshold, rather than changing the cross-species symmetry assumption.

A fixed time-uniform pair bound I(S_t F)<=9 I(F)/8 is a useful exact linear operation. Under h-time collision/marginalization steps it only gives the bound (9/8)^(T/h), not exp(C T) with a fixed C. Uniform equivalence of E_s to the square-root homogeneous H^s norm likewise gives no collision derivative. Neither observation closes the actual nonlinear continuation estimate.

Governing sources actually read: Zhu, arXiv:2512.17905v1, Proposition2.2, Proposition3.1 and Lemma3.2, https://arxiv.org/html/2512.17905v1; Junne--Winter--Yoldas, arXiv:2512.17082v1, local/continuation framework and Section3.3, https://arxiv.org/html/2512.17082v1. The finite-mass cross threshold excludes gamma=-3; the compensated infinite-mass theorem does not supply the finite-recoil estimate. No computation, optimizer, new worker or extra scientific verification is used here.
