# Independent algebra/source check: clean-core transport threshold

26 October2026. PASS for the stated sufficient region in `clean_core_operator_transport_curvature.md`; no general conditional-curvature conclusion.

I independently reacquired the Haar representation from the actual denominator determinants. For a Haar qubit vector, alpha=<A2>,beta=<H2>; the first Ip term is2/[beta+(h/t+2)(alpha+t)]^2. Setting x=2t gives exactly K(beta+h+2alpha,2alpha h). The second term integrates to1/(beta+3alpha). There is no missing factor2 or3.

The expansion R(2u,h)-L(u)=2u^2+(C+2h)u+hA-B+hB/(2u) is exact. AM-GM gives the displayed lower bound; the smaller positive root of hA+sqrt(2hB(C+2h))=B is precisely B/[A+C+sqrt(C^2+2AC+4B)]. The unsquared branch is valid because this root has hA<B. Strict2u^2 receives equality at the threshold.

The exact rational/log derivative in the lower K bound was independently symbolically checked. At a double scalar root K=1/(3r), while the upper bound follows by dropping the positive d term and integrating1/(x+c)^2. For the actual Haar variables beta>0 gives strictness even when the scalar lower-bound comparison is at equality.

The identity delta+sqrt(2delta)=1 for delta=2-sqrt3 gives the strict bracket delta*amin<h_star<amax. The source-dependent C threshold was independently simplified symbolically to

 C>=amax-(3-sqrt3)amin+delta*amin^2/(2amax).

The required unsquared quantity B-delta*amin*A is positive because amax>=amin and1-2delta>0. The condition-number corollary follows by maximizing h_cert as C tends to0, yielding kappa/(sqrt(kappa)+1)^2<=delta. No uniformity in a vanishing noise eigenvalue is claimed.

Finally Q0 is exactly the first two terms of the actual real invariant Hessian direction(-3,1); its omitted third term is nonpositive. Thus Q0(h_star)<0 is a genuine curvature exclusion in the displayed parameter region. It does not prove Ip(h_cert)>0 in general, nor settle the remaining anisotropic small-main clean core.
