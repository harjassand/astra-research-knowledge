Unknown time-varying diffusivities: a paid physical pulse and a form comparison
11 November 2026 Brisbane

1. Exact physical MHD pulse with time-dependent coefficients.

Let nu(t),rho(t) lie in supplied positive intervals contained in(0,1], with Lipschitz constants<=L_t. Let H be any unknown constant magnetic mean, |H|<=M. For F=e_i s(x_j), i!=j, s=sin(kappa x_j) or cos(kappa x_j), kappa=2pi, the FULL physical MHD ansatz
 u=x(t)F, B=H+[z(t)/kappa]s'(x_j)e_i
with force g(t)F and zero disturbances is still invariant. Its amplitudes U=(x,z) solve
 U'=A(t)U+g e1,
 A(t)=[[-kappa^2 nu(t),-kappa H_j],
       [ kappa H_j,-kappa^2 rho(t)]].                 (1)
The symmetric part is negative, so its evolution is contractive in Euclidean norm. No derivative of nu or rho enters that energy identity.

Use the inherited r(z)=z^2(1-z)^2(14z^2-14z+3), two zero moments, and SAME rational degree-four physical force g=a h^-2 r''(t/h), starting from U(0)=0. Let A0=A(0) and U_c solve the frozen constant system. Write B_H=100+14M, which bounds ||A0||, and assume B_H h<=1. From the inherited exact formulas,
 U_c=R'e1+A0 V_c,
 V_c=R e1+A0 integral_0^t exp[A0(t-s)]R(s)e1 ds,
 R=a r(t/h), V_c=integral_0^t U_c.
Thus
 sup|V_c|<=|a|(1+B_H h),
 |V_c(h)|<=|a|B_H^3 h^3/2,
 |U_c(h)|<=|a|B_H^4 h^3/2.                            (2)

The elementary expansion r=3z^2-20z^3+45z^4-42z^5+14z^6 gives integral_0^1|r'|<=124. Hence integral_0^h|U_c|<=126|a|; use1000|a| as a rational common bound. Also
 ||A(t)-A0||<=49 L_t h.
For E=U-U_c, variation of constants with the ACTUAL contractive evolution gives
 sup_(t<=h)|E(t)|<=49000 L_t |a|h,
 sup_(t<=h)|integral_0^t E|<=49000 L_t |a|h^2.         (3)
Consequently the actual unknown-time-coefficient physical pulse obeys
 |U(h)|<=|a|B_H^4h^3/2+49000 L_t|a|h,
 |integral_0^h U|<=|a|B_H^3h^3/2+49000 L_t|a|h^2.    (4)
Its magnetic amplitude has no h^-1 blowup: it is bounded by
 B_H|a|(1+B_Hh)+49000 L_t|a|h.

The force evaluates neither H nor either coefficient profile. Peak and integrated force are <=C|a|h^-2 and C|a|h^-1, with ordinary rational degree-four time coefficients. Inverse-polynomial choices of h in M,L_t,|a| and desired errors pay all these numerical and binary costs. These are actual coupled-sector bounds, not an exact universal return. Different orientations can still have different mean-dependent profiles. The sector does not address arbitrary initial fluctuations, nonlinear erasure or the full compiler. The successful constant-parameter construction instead uses a viscosity-only proof reference; no obligation to use(1) follows.

2. Uniform rough-data comparison from variational forms.

Here is an abstract operator estimate with its assumptions explicit. Let V embed densely and continuously in H, and let a_t,atilde_t be measurable bounded forms on V with the same constants alpha>0,omega>=0:
 Re a_t(v,v), Re atilde_t(v,v)>=alpha||v||V^2-omega||v||H^2.
Assume
 |(a_t-atilde_t)(u,v)|<=epsilon||u||V||v||V
almost everywhere. Let S,Stilde be their variational evolution operators for u'+A_tu=0. Then on any interval of length T,
 ||S(T,0)-Stilde(T,0)||_(H->H)
 <=epsilon (1+2omega T)exp(2omega T)/(2alpha).         (5)
In particular omega T<=1 gives the bound12epsilon/alpha. There is NO number-of-cells factor and no time derivative of the forms.

Proof. Forward energy gives sup||u||H^2<=exp(2omega T)||x||H^2 and
 integral||u||V^2<= (1+2omega T)exp(2omega T)||x||H^2/(2alpha).
The backward adjoint evolution has the same estimate, since the real part of the adjoint form has the same coercivity. Pairing a forward Stilde solution with a backward S-adjoint solution yields the integrated difference of the two forms. Cauchy--Schwarz in time gives(5). This can first be derived for finite Galerkin systems; the variational energy limits and duality give the same identity for rough H initial data. No operator-norm Taylor expansion of a second-order generator, endpoint differentiability, or H-maximal-regularity assertion is used.

For a piecewise frozen scalar coefficient on cells of maximum length ell, a Lipschitz profile differs from its frozen values by<=L_t ell. If the spatial pulled-back forms have a common domain and polynomial boundedness/coercivity constants, the form difference is <=C_geom L_t ell. Equation(5) gives a WHOLE-macro operator error polynomial in the geometric envelope, alpha^-1 and L_t, times ell, provided omega T<=1. Summing separate one-cell operator bounds would lose the useful ell factor. The common-domain and dual-energy hypotheses must be checked for the ACTUAL pulled-back operators; merely naming a parabolic generator does not supply them.

For the intended MHD use, H=H1 and V=H2 are possible energy spaces for spatially smooth conjugated coefficients. This is a conditional application of(5), not an assertion that arbitrary rough non-autonomous forms have H-maximal regularity or that all nonlinear estimates have already been proved.

3. Coefficient-free schedules can freeze in the proof.

The existing constant-parameter compiler emits a force independent of the actual values. A proof may freeze nu,rho at the beginning of each chosen cell without evaluating those values in the output program. The new residuals must still be paid.

For a fixed carrier word of physical duration d and polynomially bounded impulses and leg count, its velocity carrier has a smooth envelope P/d. A coefficient difference<=L_t d therefore creates a smooth momentum source bounded by L_t P, rather than L_t P/d. Its L2-time norm is <=L_t P sqrt(d). In a local conjugated H1 energy estimate this can be assigned an inverse-polynomial duration cap. The small affine proof correction and transported magnetic reference add their own polynomial smooth terms. This observation is a residual budget, not a complete reset/writer theorem. Couplings of the rough errors remain in the actual uniformly positive principal operators.

Cell-by-cell frozen stirring averages can have different unknown scalar heat coefficients d_j. Their heat factors commute EXACTLY:
 product_j exp(ell_j d_j Delta)=exp[(sum_j ell_j d_j)Delta].
If d_j>=c rho_- a^2, the accumulated mean-zero contraction uses the same lower bound, and constants stay fixed. Neither the individual d_j nor their integral must be computed by the compiler. This algebra does not by itself extend the accepted two-sided telescope to the changing frozen references. Its common spatial estimates, full-space constant column, local smooth residuals, reset composition and global nonlinear Duhamel bootstrap must be constructed together.

The fixed erasing superword can be frozen as a whole; its internal affine cancellation then uses one coefficient value. Different completed superwords need only uniform partial/end bias estimates. An entire closed target-writing palindrome must likewise share one frozen value within its proof. Lowering's zero-primitive condition acquires an explicit error of order L_t A ell^2 per cell when a coefficient varies within that cell. All these scales have polynomial candidates, but they are not silently declared a completed non-autonomous compiler.

4. A real contrary boundary for rougher uncertainty.

For a fundamental shear, the accepted constant-coefficient affine map is
 A_F^nu(a)z=Q_F(a)z+nu a Delta F,
 Q_F(a)Delta F=Delta F.
If its nominal inverse and forward leg have different constant values nu1,nu2, then exactly
 A_F^nu2(a)A_F^nu1(-a)z=z+(nu2-nu1)a Delta F.         (6)
The residue does not shrink with physical compression. Even a finite jump can be placed inside a preassigned word. This is an obstruction to that literal constant-coefficient cancellation under unrestricted switching, not a negative for every admissible controller. A supplied Lipschitz bound provides a genuine means of bounding this difference by the word duration. It does not make the coefficients constant, observable or known.

5. Read primary contracts and actual limits.

Arendt--Dier--Laasri--Ouhabaz, Maximal Regularity for Evolution Equations Governed by Non-Autonomous Forms, author preprint https://www.uni-ulm.de/fileadmin/website_uni_ulm/mawi.inst.020/arendt/downloads/publications/preprints/ADLO5-11.pdf, Theorem1.1 and its surrounding assumptions, gives the inherited measurable bounded quasi-coercive variational framework in V'. Stronger H-maximal regularity has additional hypotheses. The governing statement was read; the comparison(5) is derived here from its energy/adjoint identities.

Fackler, J.-L. Lions' problem concerning maximal regularity of equations governed by non-autonomous forms, https://www.numdam.org/item/10.1016/j.anihpc.2016.05.001.pdf, Theorem1.1 and Theorems4.1/5.1 were read. The abstract counterexamples, including symmetric one-half-Holder forms, refute an automatic upgrade to H-maximal regularity. They do not refute(5), the variational V' energy theory, or this specific smooth-space scalar-diffusivity MHD problem.

The complete constant-parameter unknown-flux construction is in P2_PRO_7D2DFD_MAGNETIC_FLUX_RETURN_20261111.md263635UTF8/SHA4903894b9cc4cc195a64deb2520726d9c00e265eba9831a4fd10cfaac31103c3. Its complete copied final/current activity/six chat-wide helper panels are available; helper accessibility math is sometimes fragmented/repeated, and no ZIP was visible. Its full-space constant-column estimate, harmonic-bias recurrence, Lorentz budget and transported-mean writer are inherited capital, not a theorem about time-dependent diffusivities. The physical matrix sector and two-moment polynomial in(1)--(2) are inherited from ROOT_MAGNETIC_MEAN_COUPLED_PULSE_AND_AFFINE_BIAS_20261111.txt9076UTF8/b9f488ce; (3)--(5) and the temporal-freezing interface are the composition derived here. Equation(6) is the previously identified switching boundary, retained rather than counted again.

No time-varying all-data/all-weak compiler, common nonlinear reference schedule, global polynomial resource closure, unknown coefficient observation or stronger physical experiment is claimed by this note. Those remain the full research endpoint, with freedom to use other representations.
