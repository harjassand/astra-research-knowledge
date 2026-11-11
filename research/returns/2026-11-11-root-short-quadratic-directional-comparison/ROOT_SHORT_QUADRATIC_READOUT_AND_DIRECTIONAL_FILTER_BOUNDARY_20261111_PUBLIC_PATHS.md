A coefficient-blind short quadratic window and a directional-filter comparison

Scope. The complete nonlinear-response return constructs stable logical arithmetic and leading readout symbols, but not a full physical compiler. This note constructs a DIFFERENT actual local readout window from prepared magnetic packets and a full-space positive-time comparison for the proposed finite-rank magnetic restore. The first leaves large magnetic garbage; the second is not yet an allowed physical actuator. Their limitations are part of the statements.

1. Quadratic velocity generation before appreciable diffusion.

Let kappa=2pi. Start the UNFORCED actual coupled MHD equations from u=0 and
 B=H+A sum_j[b_j exp(i kappa k_j.x)+conjugate],
where k_j are actual integer frequencies, k_j.b_j=0, coefficients may be unknown odd functions of H, sum|b_j|<=P, |H|<=M, and |k_j|<=C L Q. The finite number/tag geometry and L are supplied bounds, not observations of H. Fix a slow output set |m|<=N independent of Q. The initial field is smooth and real; the theorem is conditional on preparing THIS actual field, not on an extra magnetic force.

Choose Q=q^4,A=q^6,T=q^-12=A^-2, with q a polynomially large integer in P,L,M,N and requested reciprocal error. The exact constant-H linear Fourier propagator has negative diagonal diffusivity part and skew-Hermitian Alfven coupling, hence norm at most1 for EVERY unknown positive scalar coefficient history. No coefficient value is sampled. Its deviation from identity on the packet band is at most C[(LQ)^2+MLQ]T.

Expand the actual reference solution into homogeneous terms in its nonconstant initial packet coefficients. A degree-n term has frequency at most C nLQ. The bilinear MHD term is a divergence/curl, so its Fourier output derivative is the OUTPUT frequency. Time integration divides by n-1, while the support bound contributes at most n; n/(n-1)<=2. A Catalan majorant therefore converges when
 theta=C P A LQ T=C P LQ/A<1/2.
Through each FIXED spatial order r, the full reference has an actual bound C_r(P,M,L) A(LQ)^r; these are computed Fourier envelopes, not an unknown PDE norm.

For a slow output m, replace the final derivative bound C nLQ by N. Summing every degree n>=3 gives a slow remainder at most C(P,M,L,N)LQ/A. The quadratic velocity term is
 u_m(T)=i kappa P_m sum_(k_j+k_l=m)[(b_j.m)b_l] +error,         (1)
with the sum over ORDERED packet pairs, including the real conjugates. Here A^2T=1. Formula (1) is the actual quadratic Leray-divergence symbol. For two distinct packets, it is i kappa P_m[(b_1.m)b_2+(b_2.m)b_1]. Its diffusive/Alfven error is at most a polynomial times[(LQ)^2+MLQ]T; the entire higher-degree slow tail is O(P_poly q^-2). Known polarization and unique-tag formulas in the return can arrange the desired h_j R_j coefficient and avoid unwanted quadratic slow pairs. No inverse unknown rho factor occurs: diffusion has not normalized this pulse.

2. Arbitrary incoming errors are controlled on THIS short window.

The same convergent reference bounds give
 integral_0^T ||D(u_ref,B_ref)||infinity dt <=C(P,M,L)LQ/A,
 integral_0^T ||D^2(u_ref,B_ref)||infinity dt <=C(P,M,L)(LQ)^2/A.
The first is small for polynomial q; the second is polynomial in q (q^2 for fixed L). The joint relative-energy identity therefore gives, for arbitrary spatial perturbations and admitted L-infinity_t L2_x disturbances,
 E_L2(T)<=C[E_L2(0)+eta T],                                  (2)
with an absolute endpoint factor after q is chosen. The reference is strong by the convergent Fourier construction. The relative-energy inequality applies to EVERY corresponding energy weak realization at its prescribed energy trace; it is not restricted to the packet Fourier subspace.

For an H1 input error in a sufficiently small inverse-polynomial ball, the usual differentiated joint estimate has a first-derivative coefficient paid by the first integral, a second-derivative coupling paid by the second integral times the L2 error, and a cubic perturbation term absorbed by a polynomial small-ball choice using positive mu=min(nu_-,rho_-). Thus one obtains
 E_H1(T)<=C_poly[e1+(LQ)^2 e0/A+eta sqrt(T/mu)],              (3)
under explicit polynomial bootstrap thresholds. To make these thresholds numerical, take the Fourier coefficient-sum majorants above, the fixed Sobolev product constants and their Young-inequality majorants, then require T mu^-3 times the fourth power of the proposed H1 error bound to be at most a fixed small constant. Every quantity is a fixed polynomial in the input envelopes,q,mu^-1 and reciprocal tolerance. Equation (3) claims no H1 estimate for an unbounded input error ball. In contrast, (2) uses the actual relative-energy comparison for arbitrary L2 errors.

This removes the large-gradient exponential from a SHORT quadratic write itself. It does not establish the long resistive-decay readout proposed in the return.

3. The magnetic garbage is a real unpaid physical interface.

At time T the high magnetic packets still have amplitude of order A. A subsequent ordinary heat decay of duration of order Q^-2 would produce a further Lorentz impulse of order A^2/(rho Q^2), which is large in this scaling. It cannot be ignored. The accepted general heat service uses velocity resets and therefore does not automatically preserve the newly written UNKNOWN even velocity response. A full compiler using this short window needs a joint cleanup preserving the low unknown velocity and magnetic memories, or a different design. This note supplies neither that physical cleanup nor a variable-degree register compiler. Treating it as a completed final readout would be false.

4. Directional heat gives a full-space finite-rank COMPARISON without a rough-data identity limit.

Use the return's exact finite-rank operator
 R=P_y T_1(Phi) P_x P_z,
 Phi=2sum_j chi_j(z)w_j(y), D_z chi_j=w_j,
 T_1(Phi)B=B+kappa^-1 curl(e1 Phi B1).
It sends selected coefficients of B1(y) to e2-coded z modes and retains the mean; ||R||_(H1->H1)<=1. Its code band is at most F and its finite Fourier coefficient/derivative envelopes are paid by a polynomial P_Phi.

For a fundamental shear F0=e_i f(x_j), i!=j, f=sin(kappa x_j) or cos(kappa x_j), let M_a be its exact induction pushforward. Direct differentiation gives
 M_a^-1 partial_j M_a=partial_j-a f' partial_i+a f''(e_i tensor e_j).
Squaring, averaging a and-a, then averaging the sine/cosine pair cancels all linear terms and the f'f'' matrix term. Since(e_i tensor e_j)^2=0, the ACTUAL full-vector operator identity is
 average M_a^-1 Delta M_a=Delta+(kappa^2 a^2/2)partial_ii.     (4)
Constants and full-space vector columns are included. This is an operator identity, not a nonlinear physical-flow theorem.

Let S_i=exp[D_i(Delta+chi_i partial_ii)], with positive D_i in[rho_- t_i,t_i], chi_i>=1. D_i is unobserved; the comparison works uniformly for every value in this interval. Define
 R_D=S_y T_1(Phi) S_x S_z.
The positive baseline heat makes this composition a bounded H1 operator even though the bare first-order T_1 is not bounded H1->H1 on arbitrary fields. A direct Fourier calculation gives
 ||R_D-R||_(H1->H1)
 <=C P_Phi(1+F)^C[(D_x+D_y+D_z)F^2
       +(1+D_min^-1) exp(-c min_i chi_i D_i)],               (5)
for fixed absolute C,c>0 and D_min=min D_i. Explanation: the desired finite-dimensional entries acquire only heat attenuation on frequencies at most F. Every undesired input/output entry has a nonzero killed coordinate and gains a directional exponential. The first derivative and H1 weights are paid by baseline heat, bounded by a fixed polynomial in D_min^-1 and F. Multiplication by Phi shifts frequencies by at most F and has only its paid finite coefficient sum. This proves a uniform operator estimate on arbitrary H1 discrepancies, not just a reference Fourier band.

Choose small rational t_i first so the first term is below the assigned tolerance, then polynomially large chi_i so the exponential beats its explicit polynomial prefactor uniformly on D_i>=rho_- t_i. The bound exp(-x)<=r!x^-r at a FIXED sufficiently large integer r gives a polynomial choice, without a logarithm or exact-real oracle. Rational shear impulses with paid pi enclosures realize the required comparison chi_i bounds. The number of factors is fixed and ||R_D||<=1+assigned_error. No operator-norm convergence of ordinary heat to identity on the whole H1 space is asserted: the finite-rank complete composition is essential.

5. Remaining physical work and literature scope.

To use (5) one must still realize the conjugated directional diffusion in the ACTUAL coupled system with the twelve mechanical actuators, finite clocks, positive unknown time-dependent nu/rho, full-space harmonic columns, Lorentz terms, disturbances and all weak realizations. The accepted common-domain whole-macro estimates provide relevant machinery, but their adaptation and any joint UNKNOWN-velocity-memory preservation are not proved here. No additional magnetic force or effective anisotropic diffusivity is an emitted actuator by assumption.

Feola--Franzoi--Montalto--Pena2607.25836v1, https://arxiv.org/html/2607.25836v1, equations1.1--1.12/Theorem1.1 was actually read. It concerns constant positive coefficients, a two-dimensional rectangular torus, a maintained VELOCITY shear with constant magnetic field, and profile-dependent long-wave stability/instability conditions; the source notes the nonzero transverse-field reference error. It is not a theorem about the present unforced decaying magnetic packets, not a polynomial ensemble compiler and not an all-control obstruction. No tearing-growth law for these packets is imported from search metadata. The held JDE S0022039625002529 and every other held source remain unopened. No new source failure or held recovery.
