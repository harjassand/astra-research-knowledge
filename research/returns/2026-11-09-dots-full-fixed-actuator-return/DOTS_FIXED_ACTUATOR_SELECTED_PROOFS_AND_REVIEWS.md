# Selected supplied Dots proof and completed review text

Source: unchanged producer fixed_actuator_reproducibility_20261109.zip; SHA256 f33df2dc0e68c62358584b011275236c13318f0d658fbd1d89a19bf83315fa52.
Selection: only the permitted governing proof, separate H3 extension, both completed reviews and needed physical-L6/native-filter proofs. Original member text is retained below with member identities and hashes. No archive tree was unpacked; no producer code or scientific checker was executed. Other members and held predecessors are not claimed read.

## ARCHIVE MEMBER: fixed_actuator_reproducibility_20261109/fixed_actuator_universal_return_20261109/PROOF_CANDIDATE.md

Original member bytes: 16605; SHA256: d27a5663b6fc139733e1de7147b2acfc550dbca0019c5fda517bbf22a3d18875.

# Three fixed-actuator blocks with universal static calibration

Date: 2026-11-09. End-to-end constructive candidate. The new physical-fiber L6 dependency, the separate local-filter challenge, inherited Astra premises, and execution limits are explicit below. This document is not a claim of practical control, experimental validation, external novelty, or an independently executed PDE theorem.

## 1. Target and exact uncertainties

On the unit three-torus retain the actual equation

    u_t + P[(u.grad)u] = nu Delta u + P[(b.grad)u].

Here P is Leray, nu>0 and K>=1 are rational, and the initial velocity is any smooth, real, mean-zero, divergence-free field with H3<=K. One prescribed rational programme must work simultaneously for this entire initial ball.

The only nominal frequency/direction pairs, in order, are

    (p1,a1)=(e1,e2), (p2,a2)=(e1,e3), (p3,a3)=(e2,e1).

During pulse j the actual field is

    b_j(t,x)=f_j(t) theta_j(a_j+e_j)
                    cos(2*pi*p_j.x+phi_j),

where |theta_j-1|<=rho0, |e_j|<=rho0, e_j.p_j=0 and rho0=1/1024. The phase is arbitrary. Each gain, direction error and phase is static within its own pulse and may differ independently between pulses. Timing and frequency indices are exact. There is no measurement, feedback, random-phase success event, or shared-calibration assumption.

The programme has three nonnegative rational-polynomial C2 pulses separated by zero-driver intervals. It will give unique global strong evolution, an explicit common rational global H3 bound M, and a common rational T at which H1<=nu/4. All numerical resources are bounded by C_*(2+K+nu+nu^-1)^4000000 for an explicitly computable universal constant C_*. Synthesis has polynomial bit work and output height/length in the full binary input length. These are huge formal resource bounds, not a practical proposal.

## 2. Dependencies and their scope

A. Current Astra N1777/A43D supplies quantitative fundamental Jacobi dispersion. The existing accepted 8EB/BCA interfaces supply native short-pulse continuation and small-critical-Fourier global continuation. Their exact sources are inherited from fixed_actuator_return_20261109/sources and followup_review. A fresh default-branch N1777 read on this date returned the unchanged blob8234680c3c1d9c9959ffd3725a80de3fee32f2cc. It still declares the fixed-spatial-actuator nonlinear endpoint open; its existing full 2B5 theorem instead permits growing spatial frequencies. We do not re-count the current polynomial Jacobi result as new work.

B. For a coordinate shear U(S), both native velocity polarizations give, on the sectors |v.xi|>=|xi|/2,

    ||U(S)||H1->Hdot^-1 <= Q S^(-1/13), Q=2^3000, S>=1.  (2.1)

This is a consequence of the already audited beta^8 dispersion plus the trivial beta^-2 bound. It does NOT require the newer proposed uniform-beta dispersion. Both phase gauges and the admitted gain are included. L2 is exactly unitary on each transverse fiber.

C. The NEW spectral dependency is fluid_uniform_spectral_edge_20261109/PHYSICAL_LP_CANDIDATE.md, SHA6b4ddd9328498adafa0774102cfbde188a2c9cea09574ea9a3fc775a3f6f2923. For one fixed nonzero transverse fiber, the physical longitudinal L6 operator norm of any static native inviscid shear is <=C_f=2^200*6^4, uniformly in action, direction and phase. The zero transverse fiber is unchanged. Its proof uses positive monotone own-half Jost coefficients and full-circle spectral reconstruction. This is not a full three-dimensional L6-to-L6 or viscous-semigroup theorem. It has separate narrow analytic reads, not a PDE experiment; the end-to-end candidate depends on this precise operation.

D. The local actual nonlinear filter, endpoint reset and heat-reference comparison are in fixed_actuator_critical_heat_bridge_20261109: L6_BACKGROUND_NATIVE_FILTER.md (c6f87541...), STRONG_ENDPOINT_RESET.md (f3bb8bf2...), NATIVE_HEAT_REFERENCE.md (b114fb07...). A separate source/algebra challenge at fixed_actuator_l6_filter_challenge_20261109/REVIEW.md (b627ef25...) found no local blocker. It is not clearance of this new composition.

For clarity, their usable local interface is restated. Write incoming state v0+w0 with L6(v0)<=A and Hcal(w0)<=eps, where Hcal(f)^2=integral_0^infinity ||heat(t)f||infinity^2dt. Put C=2^40. Given eta>0 choose

    delta=min{1/nu, nu^3/(80 C A)^4,
                       eta^8 nu^7/(128^8 A^16)},
    eps=min{nu/(32C), eta*nu*delta/64}.                 (2.2)

Then the ACTUAL unforced native wait exists strongly and ends within eta in H^(3/4) of exp(nu delta Delta)v0. Its two error terms are

    32eps/(nu delta)^(7/8)
       +64A^2 nu^(-7/8)delta^(1/8) <=eta.             (2.3)

Its endpoint H3 is <=16||incoming state||2/(nu delta)^(3/2), with rational reserve16K/(nu delta)^2. During the interval, initial H3 bound Z>=1 gives the polynomial reserve

    2Z max{1,2^18 Z^2 delta/nu}.                     (2.4)

The reference in (2.3) is legal only because the nonlinear background-to-heat error is explicitly paid. Native self-advection is not switched off during any gap.

Also, uniformly over any one such inviscid shear and all actions,

    Fminus1(Ug)<=16||g||H^(3/4),
    Hcal(g)<=Fminus1(g)/sqrt(2), Hcal(g)<=8||g||H1.  (2.5)

The first is only fiber unitarity plus summable transverse weights. It does not assume arbitrary-word propagation in a critical norm.

## 3. Action- and wait-independent reference backgrounds

Let D_j=exp(nu delta_j Delta), and let U_j denote the actual calibrated inviscid propagator for the selected action. Define

    f0=u0, f1=D1 U1 f0, f2=D2 U2 f1.

Set E to be the Fourier projection onto k=(n,0,0), and Q0=I-E. Since the first two shears share p=e1, they preserve every transverse fiber xi=(k2,k3), and they fix xi=0 exactly. Thus

    E f2=D2 D1 E f0,  ||E f2||H3<=K.                (3.1)

The physical fiber L6 bound in dependency C composes TWICE because p is unchanged. Longitudinal heat is a one-dimensional L6 contraction and transverse heat is scalar damping. Summing the INITIAL transverse fiber L6 norms with the H3 Cauchy estimate gives the common bound

    ||U1 f0||6<=A,
    ||U2 D1 U1 f0||6<=A,
    ||U3 E f2||6<=A,
    A=2^600 K.                                     (3.2)

No endpoint H3 from a previous wait enters (3.2). In particular A does not change when a wait is shortened or an action is increased. This is the specific repair of the failed generic H3-reset recurrence. The discarded Q0 f2 will be small and is charged as a critical remainder, not added to the third background.

The reference fields depend on the actual unknown calibration and initial datum only in the proof. No implementation step computes or observes them.

## 4. Backward rational wait and error allocation

Use the function delta(A,eta),eps(A,eta,delta) in(2.2), with the same A for all blocks. First choose

    e3=zeta3=nu/4096,
    delta3=delta(A,e3), eps3=eps(A,e3,delta3).

Then choose

    e2=q2=eps3/64,
    delta2=delta(A,e2), eps2=eps(A,e2,delta2),
    e1=eps2/32,
    delta1=delta(A,e1), eps1=eps(A,e1,delta1).

Finally allocate native pulse H1 implementation errors

    rho1=eps1/8, rho2=eps2/16, rho3=eps3/16.          (4.1)

This is a finite backward rational computation. All waits are now fixed, before any action is selected. It is not the earlier forward allocation whose background norm depended on the preceding wait.

## 5. Calibrated linear reference estimate

For the first two actual transverse vectors v_j=theta_j(a_j+e_j),

    max(|v1.xi|,|v2.xi|)>=|xi|/2, xi!=0.            (5.1)

Indeed each coordinate error is at most(2rho0+rho0^2)|xi|<|xi|/256, and 2(1/2+1/256)^2<1. Let E1 be the sectors active for pulse1. E1 commutes with both first shears and both heat operators, since they preserve xi. Its definition need not be known to the controller.

Write t_j=nu delta_j<=1 and theta=3/4. Heat multipliers, (2.1), and unitarity give

    ||E1 f2||Htheta
      <=2 Q K t1^(-1/2)t2^(-3/8) S1^(-1/13),
    ||(I-E-E1) f2||Htheta
      <=4 Q K t1^(-1/2)t2^(-7/8) S2^(-1/13).       (5.2)

In the first line heat1 changes Hdot^-1 to L2 and heat2 changes L2 to Htheta. In the second line heat1 supplies H1 from the original L2 bound, pulse2 mixes, and heat2 changes Hdot^-1 to Htheta. This keeps all longitudinal modes and both polarizations. It does not use an inviscid L2-to-negative contraction, which would be false.

Choose integer actions

    S1=S2=ceil(max{1,[16 Q K/(q2*t1*t2)]^13}),
    S3=ceil(max{1,[8 Q K/(zeta3*t3)]^13}).           (5.3)

The first two lines of (5.2) then sum to less than q2, since t_j<=1. Every nonzero k1-axis mode is active for the third actual vector near e1 with p3=e2. Equation(3.1), mixing, and heat3 give

    ||D3 U3 E f2||Htheta
      <=2 Q K t3^(-7/8) S3^(-1/13)<zeta3.          (5.4)

All three actions are selected AFTER the waits. Increasing them cannot invalidate (3.2).

## 6. Actual native state tracking

Implement each U_j by a sufficiently short native pulse with H1 error at most rho_j. The quantitative implementation is given in the next section; it includes both viscosity and self-advection.

For block1, use background U1 f0 and the pulse error. Its Hcal size is at most8rho1<=eps1. The filter gives actual output

    u1=f1+w1, ||w1||Htheta<=e1.

Before the second filter, the background is U2 f1, not U2 u1. The remainder is U2 w1 plus pulse implementation error. By(2.5),

    Hcal(remainder)<=16e1+8rho2<=eps2.

Thus the actual second output is

    u2=f2+w2, ||w2||Htheta<=e2.

Before the third filter use background U3 E f2. The remainder is U3(Q0 f2+w2) plus pulse error. Equations(4.1),(5.2) give

    Hcal(remainder)<=16(q2+e2)+8rho3<=eps3.

Consequently

    ||u3-D3 U3 E f2||Htheta<=e3,
    ||u3||Htheta<=e3+zeta3=nu/2048,
    Fminus1(u3)<=nu/128.                            (6.1)

This is a critical-space endpoint, not merely a small L2 conclusion. The backwards budgets specifically pay the inherited remainders through the next shear and nonlinear wait. The programme does not need any actual projection or pinching of the velocity.

## 7. Legal native pulses and the complete strong-solution ledger

Let M0=K and, after each wait, use the rational actual endpoint reserve

    M_j=16K/t_j^2.                                  (7.1)

Native energy is nonincreasing throughout every pulse and wait, because the prescribed field is divergence-free and Leray is orthogonal. Thus the same K bounds every actual L2 norm.

For pulse j set

    L_j=(1+2^29 S_j)^3, b_j=2L_j,
    Z_j=4L_j M_(j-1), C0=2^20,
    tau_j=min{1/3, 1/[32 C0 L_j^2 M_(j-1)],
                       rho_j/[b_j(nu Z_j+C0 Z_j^2)]}. (7.2)

The inherited native BCA hierarchy applies uniformly since the actual coordinate shear vector has bounded length, independently of its particular angle. It gives actual H3<=Z_j and existence throughout the pulse. Duhamel in H1 against the ACTUAL calibrated inviscid shear gives

    ||u_after-U_j u_before||H1
       <=tau_j b_j(nu Z_j+C0 Z_j^2)<=rho_j.         (7.3)

No comparison with a nominal direction is made; there is no small-angle perturbative loss in(7.3).

On the pulse interval beginning at a rational breakpoint a_j use

    f_j(t)=(S_j/tau_j)*140 r^3(1-r)^3,
    r=(t-a_j)/tau_j,

and zero elsewhere. Its integral is S_j; its first two derivatives vanish at both endpoints. Each pulse is followed by the ACTUAL unforced wait delta_j. All coefficients and breakpoints are rational. The total input remains smooth, with a globally C2 prescribed field.

During wait j take the H3 reserve

    F_j=2Z_j max{1,2^18 Z_j^2 delta_j/nu}.          (7.4)

Equation(7.1) then replaces it at the endpoint. This does not shrink the already selected wait: the local filter lifespan is independent of this possibly enormous Z_j. The reference amplitude remains the different bound(3.2).

Let T0=sum_j(tau_j+delta_j), and define a rational common bound

    M=2^1000 max{K,Z1,Z2,Z3,F1,F2,F3,M3}.

After T0 set the field to zero permanently. From(6.1) and the inherited torus inequality

    (Fminus1)' +(nu-Fminus1) Fplus1<=0,

the solution remains globally strong and H3<=M. The usual H3 commutator reserve1000 is more than covered by2^1000, since integral_(T0)^infinity Fplus1<=1/127. Mean-zero energy decay and interpolation give H1<=nu/4 at the common rational time

    T=T0+[1+64K^2 M/nu^3]/nu.                      (7.5)

This final zero-driver interval is also nonlinear native evolution, not linear heat. Strong existence follows block by block from the pulse hierarchy, the local filter, and then the critical continuation; no arbitrary-data global regularity is assumed.

## 8. Explicit resource exponents and bit work

Put X=2+K+nu+nu^-1. Each entry below means a computable universal constant times X to the displayed exponent. Negative powers are bounded through the indicated reciprocals. Independent arithmetic gives:

    e3^-1:1; delta3^-1:31; t3^-1:32; eps3^-1:33;
    e2^-1:33; delta2^-1:287; t2^-1:288; eps2^-1:321;
    e1^-1:321; delta1^-1:2591; t1^-1:2592; eps1^-1:2913.

    S1,S2:37882; S3:442.
    L1,L2:113646; L3:1326.
    M0:1; M1:5185; M2:577; M3:65.
    Z1:113647; Z2:118831; Z3:1903.
    tau1^-1:343853; tau2^-1:351629; tau3^-1:5165.
    max F_j, M:356495; T:356501.

For example, delta^-1 has degree max{1,7,8deg(eta^-1)+23}; eps^-1 has degree max{1,deg(eta^-1)+deg(delta^-1)+1}. These reproduce the full backward table without a parameter search.

Peak spatial W3 actuation is bounded by a fixed multiple of sum S_j/tau_j, and the time derivative in W2 by sum S_j/tau_j^2. The integrated squared actuation/derivative cost is bounded by a fixed multiple of sum S_j^2(tau_j^-1+tau_j^-3), with degree at most1130651. Expanding the degree-six envelope in global time has coefficients bounded by C S_j tau_j^-7 times breakpoint powers at most6. All active breakpoints are <=1+3/nu, so degree2499291 suffices. The announced4000000 envelope covers these quantities, all nonzero piece-duration reciprocals, M,T and fixed frequencies. Constants can be computed directly from the displayed finite formulas.

There is a fixed number of rational operations, integer powers of fixed degree, comparisons, and integer ceilings. If B is the complete binary input length, every numerator and denominator has O(B+1) bits with a very large absolute multiplier. Standard rational arithmetic therefore gives polynomial bit work and output length. There is no spectral search, calibration measurement, PDE solve, real-root oracle or count depending on a numerical value such as nu^-1. The enormous fixed bit multiplier is not concealed as practical efficiency.

Three active degree-six pieces and their zero-driver gaps suffice. The last wait and subsequent continuation can be represented as one zero piece while retaining the analysis breakpoint. No full coefficient synthesis or fluid propagation has been executed in preparing this candidate.

## 9. Why this differs from the failed routes

The old fixed-length INVISCID phase/resonance floors remain valid. This programme uses actual native waits, explicitly approximated by heat only within paid errors. The finite-frequency escape is then converted by heat, so the inviscid floors do not contradict it.

The failed generic filter allocation fed an endpoint H3 cost back into the next background amplitude. Here the first two same-p fiber bounds and the unchanged axis make all three reference amplitudes depend only on initial K. Actual H3 is still paid, but only in separately chosen native pulse durations and common regularity bounds. It never changes a previously chosen wait or critical-error budget.

The programme uses no uniform physical three-dimensional L6-to-L6 shear theorem, no viscous maximum principle, no simultaneous stochastic stirring, and no assumed enhanced-dissipation nonlinear theorem. The genuinely new dependency is the fixed-fiber physical-L6 synthesis, whose precise proof status must accompany this candidate. Known local Koch--Tataru/heat smoothing and inherited Astra control/spectral operations receive their existing scope and credit.

## 10. Verification status

The local filter has a separate algebra/source challenge; the older shrinking-angle controller had its own independent scoped audit. Neither automatically clears this stronger composition. The active-sector and backwards-budget calculations are being independently challenged in the current team. No claim of a published new theorem, priority, physical experiment, realistic calibration cost, or unforced arbitrary-data Navier-Stokes result is made. Preserve the earlier failed generic allocation and all frozen sources.


## ARCHIVE MEMBER: fixed_actuator_reproducibility_20261109/fixed_actuator_universal_return_20261109/H3_BALL_EXTENSION.md

Original member bytes: 7525; SHA256: c96b7118b18b0d63195a8dfaba05175ed10902e467dc2ec17b0754614f2037f3.

# Extension from smooth inputs to the entire closed H3 ball

Date: 2026-11-09. Separate mathematical addendum. Governing smooth-data proof: PROOF_CANDIDATE.md, SHA d27a5663b6fc139733e1de7147b2acfc550dbca0019c5fda517bbf22a3d18875. No frozen proof, compiler, source check, or earlier manifest is changed.

## 1. Literal earlier scope and strengthened conclusion

The frozen governing statement explicitly assumes smooth initial velocities. Its written statement therefore does not, by itself, claim every nonsmooth H3 datum.

The same construction and bounds extend to EVERY real, mean-zero, divergence-free u0 in H3(T3) with ||u0||H3<=K, including the boundary of this closed ball. For each allowed actual pulse-static calibration, the same prescribed programme has a unique global strong solution

    u in C([0,infinity);H3) intersect L2_loc([0,infinity);H4),
    partial_t u in C([0,infinity);H1).

The solution is classical for positive time, with spatial smoothing. No classical differentiability at t=0 beyond that supplied by H3 is asserted. It has the SAME rational common global H3 bound M, switch-off critical bound, terminal time T and terminal H1<=nu/4 bound. The same static-calibration quantifiers and exclusions apply.

This conclusion retains all spectral/control premises and analytic-review qualifications of the governing candidate. The extension does not strengthen those premises, cover arbitrary energy-class data, or claim uniqueness among arbitrary nonsmooth solution notions.

## 2. One explicit H3 product and stability estimate

Write Lambda=(1-Delta)^(1/2), and use Euclidean vector/Frobenius tensor norms. The elementary convolution estimate on the unit torus is

    ||f tensor g||H3 <=16 ||f||H3 ||g||H3.            (2.1)

Indeed, with q_k=2*pi*k, the weight obeys

    (1+|q_(l+m)|^2)^(3/2)
       <=4[(1+|q_l|^2)^(3/2)+(1+|q_m|^2)^(3/2)].

Young's sequence inequality and sum_k |fhat(k)|<=2||f||H3 give(2.1). The latter Fourier inequality includes the zero mode: square-shell counting gives

    sum_k(1+4*pi^2|k|^2)^(-3)
      <=1+[26/36^3]*sum_(r>=1)r^(-4)<4.

No H4 norm is hidden in this product estimate.

Let u and v be two smooth solutions driven by the SAME actual prescribed b, and w=u-v. Their exact difference equation can be written

    w_t-nu Delta w =-P div F,
    F=w tensor u+v tensor w-w tensor b,

with the tensor convention (div F)_i=sum_j partial_j F_ij. The prescribed b is divergence-free, so this is exactly the original transport term. On an interval on which both H3 norms are <=M, put B(t)=||b(t)||H3. Then

    ||F||H3 <=16[2M+B(t)]||w||H3.

Leray and Lambda commute and are orthogonal/self-adjoint on the divergence-free component. Pairing against Lambda^6 w and integrating the divergence by parts gives

    (1/2)d||w||H3^2/dt+nu||grad w||H3^2
      <=||grad w||H3||F||H3
      <=(nu/2)||grad w||H3^2
          +[128/nu][2M+B(t)]^2||w||H3^2.

Consequently, for every finite L>0,

    sup_(0<=t<=L)||u(t)-v(t)||H3
      <=exp{[128/nu] integral_0^L [2M+B(s)]^2 ds}
                     ||u(0)-v(0)||H3.              (2.2)

The field b is a finite collection of spatial trigonometric modes with bounded C2 time envelopes, followed by zero forcing. Thus B is finite and bounded on every finite interval. A uniform rational upper bound over the admitted actual calibration follows from the displayed actuator bounds; for example2^20 sum_j S_j/tau_j suffices. This estimate does not require derivatives of u or v above H3 on its right side.

The exponential in(2.2) is an existence/stability proof constant. It is NOT used as an additional controller amplitude, waiting time, synthesis cost, or physical resource. No operational approximation of u0 is required by the programme.

## 3. Same-programme Fourier approximation

Let Pi_n cut off the Fourier cube |k|infinity<=n and put u0_n=Pi_n u0. Then:

- u0_n is a smooth trigonometric polynomial;
- it remains real, mean-zero and divergence-free;
- ||u0_n||H3<=||u0||H3<=K, without replacing K by K+epsilon;
- u0_n converges strongly to u0 in H3.

Fix ANY one of the allowed actual calibration tuples. Use the SAME prescribed programme and that SAME tuple for every u0_n. The governing smooth-data result produces global smooth positive-time solutions u_n, all with the same global H3 bound M and endpoint bounds. Formula(2.2) applies to every pair u_n,u_m. They are Cauchy in C([0,L];H3) for each finite L. Completeness yields consistent limits u on all finite intervals, hence a global u in C([0,infinity);H3), with u(0)=u0 and ||u(t)||H3<=M.

This is strong H3 convergence, not merely weak compactness. In particular no lower-semicontinuity argument is being used to infer strong continuity at t=0.

## 4. Passing the equation, regularity and uniqueness

The product estimate(2.1) makes the nonlinear fluxes and prescribed transport flux converge in C([0,L];H3). The heat-divergence multiplier has H3 operator bound at most[nu(t-s)]^(-1/2), integrable in s. Therefore one may pass to the exact mild equation on every finite interval. Equivalently, the equation passes in C([0,L];H1), since Delta:H3->H1 and divergence:H3->H2 are continuous.

The uniform H3 energy estimate also gives a finite bound on integral_0^L ||u_n||H4^2: absorb the flux against nu||grad u_n||H3^2 using(2.1), the uniform M, and the bounded prescribed B. Weak compactness in L2H4 identifies the same strong H3 limit, proving u in L2_loc H4. The mild equation then gives partial_t u continuous into H1. Standard local parabolic smoothing, applied on intervals bounded away from zero with this smooth spatial coefficient field, gives the positive-time classical solution. The C2 time envelope is sufficient for the classical time derivative; no infinitely smooth time dependence across switches is claimed.

For any other H3-strong solution with the same datum and actual b, use(2.2) on each finite interval with the maximum of the two finite H3 bounds. The initial difference is zero, so the two solutions agree. This proves uniqueness in the stated strong class. It does not infer unrestricted weak-solution uniqueness.

## 5. Endpoints and all-calibration quantifiers

The actual smooth solutions all satisfy the switch-off H^(3/4) and Fminus1 bounds and the terminal H1 bound. Strong H3 convergence preserves H1 and H^(3/4) norms. It also preserves Fminus1, since the proved embedding Fminus1(g)<=16||g||H^(3/4) is continuous. Thus the SAME inequalities hold for u at the SAME rational times.

The argument fixed an arbitrary admissible actual calibration tuple. All programme choices and bounds M,T were independent of that tuple, and the B bound in(2.2) can also be chosen uniformly. Therefore the conclusion holds for every allowed tuple, with no exceptional set, feedback or calibration-dependent programme.

## 6. Resource and verification scope

No programme parameter is changed. The Fourier approximation is solely a proof device, not an additional synthesis algorithm, input measurement, spectral oracle or physical preparation. The exact numerical and bit-resource claims remain those already displayed in the governing candidate.

No PDE propagation, numerical initial-data approximation, full giant synthesis or hardware test was executed for this addendum. Its role is to close the literal smooth-versus-H3 statement gap using the already uniform smooth-data theorem and a directly displayed strong stability estimate. Separate mathematical review of this addendum should be recorded without rewriting the frozen source proof.


## ARCHIVE MEMBER: fixed_actuator_reproducibility_20261109/fixed_actuator_heat_sandwich_audit_20261109/END_TO_END_CHALLENGE.md

Original member bytes: 11868; SHA256: aa127bf109ded3446b2eb4a60f4ac49f44fa3434ca2592c64d4a292c2afabba9.

# Hostile end-to-end challenge of the universal-calibration candidate

Date: 2026-11-09. This is an additional analytic review, not an inference from the scalar checks. It preserves the earlier memo review unchanged. Exact version bindings are in END_TO_END_BINDINGS.json.

## Finding

The full candidate survives this challenge: I found no concrete counterexample, circular dependency, missing critical-continuation step, or incompatible inherited hypothesis at its stated static-calibration scope. The fixed-fiber physical-L6 estimate received a substantive mathematical check, not merely a check that the composition cites its conclusion.

This is a coordinated separate review by the same reviewer who earlier examined the physical-Lp candidate. It is not a fresh blind replicate, an independently implemented PDE solver, a proof-assistant certificate, a hardware trial, or a publication/priority judgment. The full argument still depends on the explicitly recorded standard Jacobi spectral/Riesz-projection facts and inherited native 8EB/BCA interfaces. The scalar script is bookkeeping only.

## 1. Re-derivation of the sensitive physical-L6 step

Write w_n=2a_n, c_n=1-w_n^2 and A_n=product_(m>=n)w_m. Substituting f_n=z^n g_n/A_n into the eigen-equation gives

    g_(n-1)+z^2(1-c_n)g_(n+1)=(1+z^2)g_n,

and hence exactly

    g_n-g_(n-1)=z^2[g_(n+1)-g_n-c_n g_(n+1)].

The vanishing-at-infinity coefficients therefore obey the repaired recurrence, not the obsolete index interpretation. At order z^2, Q1(n)=sum_(m>=n+1)c_m. At higher orders, summing the difference equation yields

    Qr(n)=Q_(r-1)(n+1)+sum_(m>=n+1)c_m Q_(r-1)(m+1).

All coefficients are nonnegative. Subtracting the equation at n+1 from that at n proves that each Qr decreases with n>=0. A_n increases toward1, so d_(n,r)=A_n^-1 Qr(n) is also nonnegative and decreasing. This direction of monotonicity was checked rather than inferred from positivity alone.

At z=1 the equivalent future-directed Volterra equation has kernel (m-n)c_m and later argument m+1. In its iterates the selected bond indices strictly increase. Replacing each m-n by m+1 bounds the expansion by the subset expansion of product_m[1+(m+1)c_m]. The inherited first-moment budget bounds this by exp(21), and A_0^-1<=exp(21). Thus sum_r d_(0,r)<=exp(42). This is a uniform coefficient-mass bound with no beta-dependent exponential.

For each r, the decreasing multiplier d_(n,r)1_(n>=0) is a positive mixture of finite interval Fourier projections plus its limiting half-line projection. Its total mass equals d_(0,r). The classical Riesz projection estimate consequently gives an Lp multiplier bound <=p d_(0,r) for p>=2; its adjoint at p has the same estimate by the dual exponent. Modulation is isometric. The series of modulation times these multipliers converges in operator norm, yielding both physical-circle Jost synthesis and adjoint bounds <=p exp(42).

This is an actual physical Fourier multiplier argument. It does not confuse a sequence-space lp wave-operator theorem with an Lp theorem on the circle. The zero-order coefficient's nonzero limit contributes a paid half-line projection; it is not omitted.

## 2. Spectral reconstruction: explicit checks against a triangular truncation failure

I reread the primary EHT paper directly: https://arxiv.org/html/1506.06555v2, Section2 scattering relation(2.5), spectral kernel(3.2)-(3.3), and the same-sign case formula in Section3. Its first-moment spectral theorem gives only possible point spectrum outside[-1,1]. Here the Jacobi norm is at most1, and the positive form excludes endpoint eigenvectors. Thus no unrepresented point-spectrum evolution remains. The scattering coefficients obey the required modulus bounds.

On the right half-line the ordered kernel, after scattering substitution, has two terms:

    integral m_t(theta) f_n(theta) f_k(-theta) dtheta,
    integral m_t(theta) R(theta) f_n(theta) f_k(theta) dtheta,

where m_t(theta)=exp(it cos(theta)). The second expression is manifestly symmetric in n,k. The first becomes its swapped version after theta -> -theta, because m_t is even. Therefore the factorized kernel covers the entire same-half block, not merely one triangle. There is no unbounded triangular truncation to be paid.

Each term is a composition of a Jost map or adjoint, reflection if needed, and multiplication by a bounded spectral function. The opposite-half block similarly uses only its own-side Jost factors and T. The left block follows by reflection. This verifies the operator factorization needed for physical Lp, not just entrywise kernel estimates. The use of the full circle is essential.

There are finitely many terms, covered by the reserved factor16. Spectral phase, reflection and T/R multiplication do not acquire time-dependent Lp norms. Combining both Jost factors gives the claimed scalar bound16 exp(84)p^2, uniformly in beta and time.

The native in-plane polarization components beta/sqrt(beta^2+n^2) and n/sqrt(beta^2+n^2) have bounded variation on their two half-lines, uniformly in beta. Each component multiplier can conservatively be bounded by4p. Extraction and reconstruction each cost at most12p after summing the three physical components. The in-plane part is therefore bounded by2304 exp(84)p^4, below2^200 p^4. The perpendicular free part is a physical multiplication of modulus one. Constant changes needed to add it fit the same large reserve. Static phase is a physical translation, not an extra oscillatory multiplier estimate.

The physical-L6 theorem therefore has a complete analytic route at the scope used by the composition. This recheck did not find an action growth, an omitted half-line projection, a missing bound state, an uncontrolled inverse scattering multiplier, or a polarization loss that would invalidate it.

## 3. Full composition rather than a scalar test

The first two shears share the same transverse fiber label; their action-independent L6 bounds compose with the actual linear heat reference within that decomposition. The initial H3 fiber sum pays both. The third large background is only the unchanged longitudinal axis, whose H3 remains at mostK. This background/remainder separation is maintained at every native filter admission.

Actual nonlinear errors need not preserve any active sector. They are instead admitted in the critical heat norm through the uniform ONE-shear H^(3/4)-to-Fminus1 map. The sector decomposition applies only to the exact linear reference. This avoids an otherwise invalid nonlinear cone-invariance assumption.

The full candidate incorporates gains into the actual transverse vectors. The safe perturbation bound is |v_j-a_j|<=2rho0+rho0^2<1/256, not merely rho0. Its displayed cover2(1/2+1/256)^2<1 is valid. On the surviving axis the third projected speed is at least(1-rho0)^2 times the transverse magnitude. Unknown actual phase/gain/error is used only in analysis; no algorithm reads it.

All reference actions are selected after the backwards waits/errors. The first two reference L6 amplitudes and the axis amplitude are unchanged by increasing those actions. Actual H3 influences only the subsequently selected pulse durations. This is a genuine acyclic dependence, not a claim that any fixed-depth rational factory must be feasible.

The final state is small in H^(3/4), hence in Fminus1. It is not a claim that a small L2 endpoint implies strong global continuation. All leave-and-return paths remain in the unitary operators and heat factors; there is no intervening physical projection.

## 4. Inherited native assumptions matched explicitly

The BCA differentiated hierarchy uses derivatives parallel to the actual shear direction and normal to its spatial frequency. The direction is static and transverse, exactly as required here. Its rotation is an analysis choice and does not need rational coefficients. Constant derivatives commute with Leray. Every shear commutator lowers the normal derivative count, native viscosity is nonpositive in those energies, and the self-advection estimate is an energy-pairing estimate, not a false H3-to-H3 bound on the nonlinearity.

For coordinate frequency |p|_1=1 and the admitted actual vector, |v|_1<=4. Thus the BCA envelope(1+2^24 S |v|_1(1+|p|_1)^3)^3 is covered by L=(1+2^29 S)^3. The chosen duration1/(32 C0 L^2 M_input) supplies the stated4L M_input reserve. The actual-versus-inviscid H1 Duhamel error uses nu||u||H3 plus C0||u||H3^2 and the paid partial-propagator bound2L. No nominal-direction comparison or small-angle interpolation is involved.

The governing duration formula omits the extra1/(24Z) cap used in my earlier conservative memo ledger. That cap is NOT needed here: it belonged to an earlier calibration-comparison allocation. The present BCA existence and local H1 error use only the three listed caps. Moreover its degree was smaller than the controlling reciprocal-duration degree in all three stages, so this omission does not change the conservative resource table.

For each native gap the admitted background is smooth, mean-zero and divergence-free, as is the full remainder. The local filter accepts a large H3 norm with small critical remainder and fixed L6 background. Its endpoint reset and intermediate polynomial H3 bound apply separately. The H^(3/4) source singularity is7/8<1; replacing it by an unintegrable H1 kernel would invalidate the proof, but the candidate does not do that.

The heat-reference discrepancy is explicitly the sum32eps/(nu delta)^(7/8)+64A^2 nu^(-7/8)delta^(1/8). The two min-conditions each pay half of the target. Thus the wait is genuinely nonlinear native Navier-Stokes, not a silently switchable heat semigroup.

At the final endpoint Fminus1<=nu/128, the torus Fourier inequality gives integral Fplus1<=1/127. The inherited H3 commutator coefficient1000 is covered by multiplication by2^1000. Mean-zero energy decays under both native self-advection and the prescribed skew transport. Interpolation H1^3<=L2^2 H3 then validates the stated rational common terminal time. Strong existence is obtained successively, never assumed for arbitrary initial data through the entire experiment.

## 5. Resources and quantifier boundaries

The governing full formulas match the earlier independent degree ledger. The constant3+3/nu used there can be tightened to1+3/nu because all three pulse durations are<=1/3. The post-control long interval must not be used as the pulse-start bound when expanding coefficients. With actual pulse starts, the degree2499291 bound remains valid and the4,000,000 common envelope has margin.

The numerical-resource constants are computable by finite arithmetic from displayed constants. The bit-work argument relies on a fixed number of rational operations and fixed powers, not polynomial runtime in the numerical value nu^-1. No infinitely precise calibration, spectral search, real oracle or PDE solve enters synthesis.

The nominal actuator programme is rational; the actual unknown phases/directions need not be. Uniform bounds cover them without claiming the actual perturbed field has rational coefficients. Exact frequency indices, exact switching times and pulse-static uncertainties remain essential. No claim for drifting phase, inaccurate frequencies/timing, residual forcing during nominal zero gaps, or arbitrary stochastic hardware error follows.

## Conclusion

The earlier generic sandwich loop is a failed sufficient allocation, preserved honestly. The full new candidate repairs it through fixed-coordinate fiber composition and an axis/critical-remainder split. The substantive new physical-L6 lemma and the end-to-end native norm chain both survived this hostile analytic challenge. This finding is stronger than agreement of scalar arithmetic, but narrower than an external independent validation, implemented scientific experiment, or novelty claim.


## ARCHIVE MEMBER: fixed_actuator_reproducibility_20261109/fixed_actuator_heat_sandwich_audit_20261109/H3_BALL_EXTENSION_REVIEW.md

Original member bytes: 4720; SHA256: 1ffe278b78d36d0ddb9d699266fbdf7ce9647f30062b4525738f8046258832f9.

# Narrow review of the closed-H3-ball extension

Date: 2026-11-09. Inspected source: fixed_actuator_universal_return_20261109/H3_BALL_EXTENSION.md, SHA256 c96b7118b18b0d63195a8dfaba05175ed10902e467dc2ec17b0754614f2037f3. Governing smooth-data proof remains SHA256 d27a5663b6fc139733e1de7147b2acfc550dbca0019c5fda517bbf22a3d18875. Neither source was edited.

## Disposition

No mathematical blocker was found in this extension, assuming the governing uniform smooth-data result and its stated dependencies. It legitimately extends the same programme to every real, mean-zero, divergence-free datum in the closed H3 ball, with the same resource and endpoint bounds. This is an analytic review; no numerical solve or initial-data approximation was executed.

## Checks

1. Product constant. The weight inequality follows from the triangle inequality for sqrt(1+|q|^2) and (a+b)^3<=4(a^3+b^3). Young convolution and the stated Fourier-l1 embedding give4*(2+2)=16. The three-dimensional maximum-coordinate shell has24r^2+2<=26r^2 points; 4pi^2>36 and sum r^-4<2 leave ample room in the embedding constant2. Euclidean vector/Frobenius tensor norms obey the same convolution estimate without another dimension factor.

2. Divergence form. With F_ij=w_i u_j+v_i w_j-w_i b_j, div F=(u.grad)w+(w.grad)v-(b.grad)w, using div u=div w=div b=0. This is precisely the difference of the two native equations. The sign and order of the prescribed-transport term are correct.

3. Difference energy. Pairing after three Bessel derivatives and integrating the divergence by parts costs one derivative of w, which viscosity pays. The bound16(2M+B)||w||H3 gives128(2M+B)^2/nu after Young's inequality. The squared-norm Gronwall exponent is256/nu; the stated NORM exponent128/nu is therefore correct. There is no hidden H4 norm of u or v on the right side.

4. Approximation at the boundary. Symmetric Fourier cube truncation preserves reality, mean zero, divergence-free constraint, and H3 norm<=K exactly. All approximants use the same programme and the same fixed actual calibration tuple. The finite-time stability factor is independent of truncation, so their H3 convergence is strong and uniform in time on every compact interval. This proves C([0,infinity);H3), including strong continuity at t=0, without claiming weak compactness supplies it.

5. Passing the equation and regularity. Products converge in C_tH3. In mild form, the derivative heat singularity is(t-s)^(-1/2), which is integrable. Alternatively the PDE right side converges in C_tH1. The uniform H3 flux-energy estimate controls integral ||grad u_n||H3^2, hence integral ||u_n||H4^2; weak compactness identifies the same already-established strong H3 limit. Its right side is continuous in H1, so u_t is continuous in H1, with the one-sided initial derivative understood at t=0. Standard local parabolic spatial smoothing gives a classical positive-time solution. The globally C2 time envelope is sufficient for this assertion; infinite time differentiability across switches is not claimed.

6. Uniqueness. The difference estimate extends to the stated H3-strong class by the energy argument with u,v in L2_locH4 and their time derivatives in L2_locH2, or by regularization. On each compact interval, the finite maximum of the two H3 bounds replaces M. Zero initial difference forces equality. No assertion of uniqueness among arbitrary energy-class weak solutions follows.

7. Uniform endpoints and calibration. Strong H3 convergence preserves the common terminal H1 and switch-off H^(3/4) estimates. The continuous H^(3/4)-to-Fminus1 embedding preserves critical smallness. The argument fixes an arbitrary allowed pulse-static calibration tuple; programme parameters and bounds are independent of that choice, and the prescribed-field bound can be uniform. No countable-net, exceptional-set or feedback argument is required.

8. Resources. The exponential stability bound is solely a mathematical existence/convergence constant. No cutoff is computed, measured, or used by the controller, and no error radius from this exponential enters the programme. Thus the extension does not add an uncharged exponential physical resource or synthesis cost. It does not establish efficient numerical approximation of each H3 initial datum, which is a different claim.

## Scope

The extension corrects a literal statement gap between smooth inputs and the closed H3 ball. It does not strengthen the underlying spectral or native control premises, cover frequency/timing errors or time-varying calibration, qualify an implemented solver, or independently validate the entire controller a second time. The earlier smooth-data proof and failed allocation records remain unchanged.


## ARCHIVE MEMBER: fixed_actuator_reproducibility_20261109/fluid_uniform_spectral_edge_20261109/PHYSICAL_LP_CANDIDATE.md

Original member bytes: 10109; SHA256: 6b4ddd9328498adafa0774102cfbde188a2c9cea09574ea9a3fc775a3f6f2923.

# Physical-space bounds for one native inviscid shear

Date: 2026-11-09. Status: new author proof candidate, not independently cleared. This is not a viscous maximum principle, a full three-dimensional Lp-to-Lp theorem, a repeated-word theorem, or a universal-calibration controller. No propagation or timing experiment has been run.

## 1. Target and distinction from sequence-space dispersion

Fix one coordinate spatial frequency p=e_i, any fixed transverse direction a, any static phase, and any real action s. Let U_a(s) be the native divergence-free inviscid propagator generated by P[(a cos(2 pi p.x+phase)).grad]. On a nonzero transverse Fourier fiber xi, beta=|xi|>=1, the two velocity polarizations are the free Jacobi chain and J_beta from PROOF_CANDIDATE.md. Their effective time may be arbitrarily large or zero.

The candidate conclusions are:

1. For 2<=p_exp<infinity, the scalar Jacobi propagator, conjugated by the Fourier transform in its longitudinal sequence index, is bounded on the PHYSICAL one-dimensional Lp_exp circle uniformly in beta and time. One may take 16 exp(84) p_exp^2.
2. Restoring the native velocity polarization gives a bound at most 2^200 p_exp^4 on each physical longitudinal fiber.
3. Summing transverse fibers with the stated input regularity gives

   ||U_a(s) f||L^(p_exp)(T3) <= 2^256 p_exp^4 ||f||H3(T3).       (A)

There is no action factor in (A). It covers every static phase and direction; no active-sector condition is required. The mean-zero xi=0 fiber is unchanged.

The H3 input in (A) must not be replaced by Lp input without a separate operator-valued transverse multiplier argument. A uniform scalar-fiber operator norm alone does not prove that argument.

## 2. Monotone positive Jost coefficients

Use the repaired recurrence, not the superseded source-index interpretation:

 Q_1(n)=sum_(m>=n+1)c_m,
 Q_r(n)=Q_(r-1)(n+1)+sum_(m>=n+1)c_m Q_(r-1)(m+1), r>=2.

For n>=0, every Q_r(n) is nonnegative and nonincreasing in n. Indeed Q_1 has this property, and subtracting the recurrence at n+1 from that at n gives

 Q_r(n)-Q_r(n+1)
  =Q_(r-1)(n+1)-Q_(r-1)(n+2)
    +c_(n+1) Q_(r-1)(n+2) >=0.                         (B)

No monotonicity assumption on c itself is needed for (B).

Let A_n=product_(m>=n)w_m, and write

 d_n(z)=g_n(z)/A_n=sum_(r>=0) d_(n,r) z^(2r).

Since A_n^-1 is positive and nonincreasing in n, every coefficient d_(n,r) has the same property. Its n->infinity limit is 1 for r=0 and 0 otherwise. The Volterra product bound from the companion proof gives

 sum_(r>=0) d_(0,r)=d_0(1)<=exp(42).                    (C)

Using the weaker inherited 22 exp(42) instead would only change the fixed constants. The stronger (C) follows from the ordered Volterra expansion bounded by product_(m>=0)(1+(m+1)c_m)<=exp(21), and A_0^-1<=exp(21).

Reflection gives the left Jost functions f_-(z,n)=f_+(z,-n), so the same statement applies on their own half-line.

## 3. Jost synthesis is bounded in physical Lp

Let P_[0,N] be the Fourier projection on longitudinal frequencies 0,...,N. The classical Riesz projection theorem gives

 ||P_[0,N]||Lp->Lp <=2 csc(pi/p_exp)<=p_exp, p_exp>=2.

The same bound holds on the dual exponent, because csc(pi/p')=csc(pi/p). Modulation and reflection are Lp isometries. A nonnegative decreasing multiplier sequence a_n on n>=0 is a positive sum of these interval projections, plus its limiting half-line projection. Its total coefficient mass is a_0. Consequently its Lp norm and its adjoint Lp norm are at most p_exp a_0.

Define the right own-half-line Jost synthesis in the physical circle by

 (J_+ h)(theta)=sum_(n>=0) hhat(n) e^(in theta) d_n(e^(i theta)).

Expanding d_n gives

 J_+=sum_(r>=0) M_(2r) D_r,

where D_r is the monotone Fourier multiplier d_(n,r)1_(n>=0), and M_(2r) is modulation. Equation(C) therefore gives

 ||J_+||Lp->Lp, ||J_+^*||Lp->Lp <=p_exp exp(42).          (D)

The adjoint follows either by duality or by reversing the multiplier/modulation order. This is a physical-space statement: the input is the Fourier series with coefficients hhat(n), not an lp sequence norm. No theta derivative of a scattering coefficient is used. All sums converge in operator norm by (C). Reflected/shifted variants have the same bound.

## 4. Spectral reconstruction and the ordering issue

Use the standard full-line Jost kernel and scattering identities in Egorova--Holzleitner--Teschl, arXiv:1506.06555v2, sections 2--3. Flux conservation gives |T|,|R_+|,|R_-|<=1 on the circle. The companion proof excludes omitted point spectrum.

Split input/output sequence indices at zero. For opposite half-lines the spectral kernel is a product of the two own-half-line Jost functions and T. For equal half-lines the scattering identity replaces the wrong-half-line function by a sum of a reflected own Jost function and R times an own Jost function. The resulting operator blocks factor through Jost synthesis/adjoints, reflection, and multiplication by e^(it cos theta), T, or R.

The usual kernel formula initially orders the two indices. This does NOT introduce an unbounded triangular truncation: in the same-half-line free term, interchanging the two indices gives the same full-circle integral after theta->-theta, because the Jost coefficients are real and cos is even. The reflected R term is already symmetric in the two indices. Thus the factorized expression applies to the entire half-line block, not just its ordered triangle.

There are at most six such terms across the four blocks; sixteen is a safe allowance. Every spectral multiplier just listed has modulus at most one. Applying(D) to both ends yields the first claimed bound 16 exp(84) p_exp^2. The free channel is multiplication by an oscillatory phase in physical space and is itself an Lp isometry.

This argument does not invoke a general Lp wave-operator theorem on sequence space. In particular, existence/completeness of Jacobi wave operators in l2 is not the missing physical-space conclusion.

## 5. Native polarizations and transverse summation

For fixed nonzero xi, the in-plane polarization has scalar components proportional to

 beta/sqrt(beta^2+n^2),  n/sqrt(beta^2+n^2),

and fixed transverse direction cosines. Each scalar sequence is bounded and has uniformly bounded total variation on the two frequency half-lines. The interval-projection argument therefore bounds its physical longitudinal Lp multiplier by a fixed multiple of p_exp, uniformly beta. The native extraction and reconstruction each cost such a factor. Combining their finitely many components with section 4 is safely bounded by 2^200 p_exp^4.

For a full vector field f, Minkowski gives

 ||U_a(s)f||Lp(T3) <= sum_xi ||U_(a,xi)(s) f_xi||Lp(T1).

For p_exp>=2, one-dimensional Sobolev embedding bounds ||f_xi||Lp by a universal multiple of ||f_xi||H1 in the longitudinal variable. Cauchy--Schwarz in the nonzero two-dimensional transverse lattice gives

 sum_(xi!=0)||f_xi||H1
 <= (sum_(xi!=0)|xi|^-4)^(1/2)
      (sum_xi |xi|^4 ||f_xi||H1^2)^(1/2)
 <= C ||f||H3(T3).

The lattice sum converges. The xi=0 term is unchanged by the shear and obeys the same H1 embedding. Elementary unit-torus lattice estimates and all finite component factors fit inside 2^256 in(A). Static phase is a physical longitudinal translation, and changing the real effective time does not change any Lp multiplier bound.

## 6. Optional logarithmic L-infinity corollary

The already accepted native single-shear hierarchy gives

 ||U_a(s)f||H3 <=2(1+2^29 |s|)^3 ||f||H3

over the admitted fixed calibration range. Sobolev embedding therefore gives a Lipschitz envelope of the same polynomial size. On the compact three-torus, the elementary ball-around-a-maximum argument implies, for p_exp>=4,

 ||v||infinity <= C ||v||Lp^(p_exp/(p_exp+3))
                      ||v||W1,infinity^(3/(p_exp+3)).

Choose p_exp=max(4,log(2+2^29|s|)), increasing to the next integer if desired. Combining with(A) yields

 ||U_a(s)f||infinity
 <= C_* [1+log(2+2^29|s|)]^4 ||f||H3.                  (E)

C_* is an explicit universal constant assembled from the displayed bounds. This corollary is not needed when the nonlinear interface uses L6. It is included to show that the old cubic Sobolev growth need not also be the physical amplitude envelope.

## 7. Exact scope and missing viscous operation

The result concerns ONE static inviscid native shear. It does not justify:

- multiplying a fixed Lp constant through infinitely many heat/shear Trotter factors;
- declaring the actual linear viscous semigroup Lp-contracting;
- treating a time-varying phase as one static Jost problem;
- iterating(A) as an Lp-to-Lp bound for a three-dimensional word;
- claiming small critical heat norm from single-shear mixing without treating resonant fibers;
- using a random phase average for the required all-phase programme.

The exact next operation for the nonlinear route is either an actual viscous mixed-norm estimate (for example, a shear-adapted equivalent norm in which diffusion has a controlled generator bound), or a robust repeated inviscid word together with paid regular-to-critical transfer. The auditor's relative-energy L6 estimate uses the actual viscous comparison path and so is not closed by(A) alone.

## 8. Prior and verification status

Primary scattering source actually read: Egorova, Holzleitner and Teschl, arXiv:1506.06555v2, sections 2--3, https://arxiv.org/html/1506.06555. The classical interval-projection estimate is an application of the Riesz projection bound; Hollenbeck--Verbitsky, Journal of Functional Analysis 175 (2000), 370--392, DOI10.1006/jfan.2000.3616, is the sharp-constant primary reference. Its indexed abstract was retrieved; the publisher full-page fetch returned403, so no full-text reading is claimed. Only a generous classical O(p_exp) bound is needed.

This is an author analytic construction from the repaired recurrence. No independent physical-space synthesis review, numerical qualification, PDE simulation, or fixed-calibration theorem is claimed. Preserve the distinction between the proof candidate and a completed nonlinear controller.


## ARCHIVE MEMBER: fixed_actuator_reproducibility_20261109/fixed_actuator_critical_heat_bridge_20261109/L6_BACKGROUND_NATIVE_FILTER.md

Original member bytes: 13254; SHA256: c6f87541b7e2108cf8de8bdeffa2e59bb30e4af1b202b8a424796b6d8f9ec443.

# Native filter with a physical L6 background and a critical heat remainder

Date: 2026-11-09. Analytic construction. No fluid propagation, numerical scattering, hardware experiment or completed universal-calibration controller is claimed. This is an explicit quantitative application of local Koch--Tataru theory, not a new generic Navier--Stokes regularity principle.

## 1. Precise operation

On the unit three-torus take smooth, real, mean-zero, divergence-free initial data u0=v0+w0. The actual equation during the filter is the UNFORCED native equation

    u_t=nu Delta u-P div(u tensor u).

No artificial viscosity, physical projection or linearization is substituted. Suppose rational upper bounds A>=max(1,||v0||6), K>=max(1,||u0||H3) and epsilon>=Hcal(w0) are supplied, where

    Hcal(f)^2=integral_0^infinity ||exp(t Delta)f||infinity^2 dt.

Set C=2^40. Choose

    epsilon<=nu/(32 C),
    0<delta<=min{1/nu, nu^3/(80 C A)^4}.                 (1)

Then the actual native strong solution exists on [0,delta]. Let v be the native nonlinear solution with initial data v0, not its linear heat image. The following estimates hold:

    ||u(delta)-v(delta)||infinity
        <=4 epsilon/sqrt(nu delta),                    (2)

and therefore the same bound holds in every finite physical Lp on this unit-volume domain. Also

    sup_(0<=t<=delta)||u(t)||H3
        <=2K max{1, 2^18 K^2 delta/nu}.                 (3)

The permitted waiting time does not involve ||v0||H3, Fzero(v0), or ||w0||H3. The total initial H3 norm still appears in the polynomial intermediate bound (3); it has not been erased from the resource ledger.

The input split is an admission condition, not an oracle. A preceding calibrated control word must actually prove its L6-background and small-Hcal-remainder bounds. This packet does not supply that robust word.

## 2. Explicit local critical-space constant

This section works first on R3, with unit viscosity. It will be applied to periodic extensions. For T>0 define

    ||z||X_T =
       sup_(0<t<=T) sqrt(t)||z(t)||infinity
       +sup_(x,0<R<=sqrt(T))
           [ |B_R|^-1 integral_0^(R^2) integral_(B_R(x)) |z|^2 ]^(1/2),

    ||F||Y_T =
       sup_(0<t<=T) t||F(t)||infinity
       +sup_(x,0<R<=sqrt(T))
           |B_R|^-1 integral_0^(R^2) integral_(B_R(x)) |F|.

Vector and tensor norms are Euclidean and Frobenius. For the retarded Oseen bilinear operator

    B(z1,z2)(t)
      =integral_0^t exp((t-s)Delta) P div(z1 tensor z2)(s) ds,

we claim the deliberately generous numerical bound

    ||B(z1,z2)||X_T <= C ||z1||X_T ||z2||X_T,
    C=2^40,                                            (4)

uniformly in T. The proof below pays the constant rather than treating the critical-space theorem as a numerical oracle.

### 2.1 The Oseen kernel

The R3 Gaussian is G_t=(4pi t)^(-3/2)exp(-|x|^2/(4t)). The kernel of exp(t Delta)P div is a first derivative of G_t plus a time integral from t to infinity of third derivatives of G_s. Differentiating the Gaussian and taking the full tensor Hilbert norm gives the safe bounds

    |D G_t(x)|<=t^-2 exp(-|x|^2/(8t)),
    |D^3 G_t(x)|<=t^-3 exp(-|x|^2/(8t)).

For the second inequality one bounds
[(r/sqrt(t))^3/8+3sqrt(3)(r/sqrt(t))/4]
exp(-r^2/(8t))/(4pi)^(3/2) by 1. If r<=sqrt(t), integrate s^-3 directly. If r>=sqrt(t), use

    t^-2 exp(-r^2/(8t))<=36 r^-4,
    integral_0^infinity s^-3 exp(-r^2/(8s))ds=64 r^-4.

Both regimes are contained in

    |Oseen(x,t)|<=2^12(sqrt(t)+|x|)^-4.                 (5)

Its L1 norm is at most 2^15 t^-1/2, since the radial integral of r^2/(sqrt(t)+r)^4 is 1/(3sqrt(t)). There is no hidden dependence on a driving field, as this filter is genuinely unforced.

### 2.2 Localization and pointwise estimate

Scale and translate a target cylinder to B_1(0) times (0,1); this is legitimate for every cylinder allowed in X_T. Split F into F_near supported in B_2 times (0,1) and F_far.

Write Y=||F||Y_T in these rescaled coordinates. Cover space by unit cubes centered at integer points. Each cube lies in a unit ball and carries time-integrated mass at most 6Y. For x in B_1, y outside B_2, the kernel is bounded by 2^12|x-y|^-4. The 343 cubes with maximum coordinate index <=3 cost at most 343*6*2^12 Y. In the maximum-coordinate shell n>=4 there are <=26n^2 cubes and distance >=n/2. Since sum n^-2<=2, their total costs at most 26*6*16*2*2^12 Y. Thus

    ||Oseen*F_far||Linf(B_1 times (0,1))<=2^25 Y.       (6)

The near source has total space-time L1 mass <2^10Y (125 covering cubes suffice). At (0,1), split its source time at 1/2. The early part costs at most 4*2^12*2^10Y=2^24Y by (5). The late part has L-infinity norm <=2Y, and the L1 kernel bound makes its integral <2^17Y. Together with (6), the normalized pointwise X_T contribution is <2^26Y.

### 2.3 The localized L2 estimate without a cutoff oracle

For the near source write, at its source time s,

    F_near(s)=(I-exp(s Delta))F_near(s)
                 +exp(s Delta)F_near(s).               (7)

This heat split replaces the compact Fourier cutoff in the usual proof. The high part satisfies

    ||(I-exp(s Delta))F_near(s)||Hdot^-1
       <=sqrt(s)||F_near(s)||2.

The inhomogeneous heat energy estimate therefore bounds the global space-time L2 norm squared of its gradient evolution by

    Y ||F_near||L1(space-time).

For the low part, its gradient evolution is exactly

    z(t)=grad exp(t Delta) integral_0^t F_near(s) ds.

Integration in t, or first performing it for finite smooth sources, gives

    integral_0^1 ||z(t)||2^2 dt
     = Re integral_0^1 <F_near(s),
          [exp(2s Delta)-exp(2 Delta)]
            integral_0^s F_near(theta)dtheta> ds.        (8)

Both heat convolutions on the right have L-infinity norm <=2^18Y. To see this, use cubes of side sqrt(s) for exp(2s Delta), and unit cubes for exp(2 Delta). Each cube has time-integrated mass <=6s^(3/2)Y or <=6Y. The Gaussian shell sum is bounded by

    6[1+26 sum_(n>=1) n^2 exp(-n^2/32)] <2^18.

Indeed, integration over [n-1/2,n+1/2] gives the safe bound sum n^2 exp(-n^2/32)<=1296. This proves that (8) is at most 2^19Y||F_near||1.

Leray and tensor divergence cost no extra L2 factor relative to the full gradient norm. Adding high and low parts, using ||F_near||1<2^10Y, and then adding (6), the normalized local L2 contribution is <2^26Y. The pointwise and local contributions together are <2^27Y. Taking 2^40 in (4) leaves ample room.

Finally,

    ||z1 tensor z2||Y_T <=||z1||X_T ||z2||X_T

by pointwise multiplication and Cauchy--Schwarz on each cylinder. This completes (4). The argument is exactly the established Koch--Tataru localization/critical-space mechanism with a fully displayed conservative ledger. It is not presented as a new general mapping theorem.

## 3. The admitted initial heat extension

The unit-torus heat bounds previously established in L6_NATIVE_INTERFACE.md give

    ||exp(t Delta)v0||infinity<=2t^-1/4 A.

Thus its X_T pointwise part is <=2A T^1/4 and its local L2 part is <=sqrt(8)A T^1/4. Consequently

    ||heat(v0)||X_T<=5A T^1/4.                         (9)

For w0, heat-kernel contraction makes ||heat(w0)(t)||infinity nonincreasing in t. Hence

    t||heat(w0)(t)||infinity^2
       <=integral_0^t ||heat(w0)(s)||infinity^2 ds
       <=epsilon^2.

Its local space-time component is also <=epsilon, so

    ||heat(w0)||X_T<=2epsilon.                        (10)

These hold for periodic extensions on R3. No finite total R3 energy is assumed. The heat equation of the periodic extension agrees with the torus heat equation.

## 4. Native nonlinear contraction and endpoint difference

Rescale viscosity by U(tau)=u(t)/nu, tau=nu t, and let T=nu delta. Equations (9)-(10) and (1) imply

    ||heat(U0)||X_T
      <=5(A/nu)(nu delta)^1/4+2epsilon/nu
      <=1/(8C).

The mild fixed point contracts on the ball ||U||X_T<=1/(4C): its self-map reserve is 3/4 of the radius and its Lipschitz factor is at most 1/2. The background V separately satisfies ||V||X_T<=1/(8C).

Their difference W obeys

    ||W||X_T
       <=2epsilon/nu
          +C(||U||X_T+||V||X_T)||W||X_T
       <=2epsilon/nu +(3/8)||W||X_T.

Therefore ||W||X_T<4epsilon/nu. The pointwise part at T yields (2). Periodicity follows by translation uniqueness in this same contraction class.

For smooth data the mild solution agrees initially with the ordinary local strong solution. On every compact subinterval away from zero, its velocity is bounded in L-infinity. The standard Serrin continuation argument then precludes an earlier strong-solution singularity. The next section supplies a fully polynomial H3 bound, rather than leaving intermediate regularity as a qualitative assertion.

## 5. Complete polynomial H3 bound

An elementary explicit tame estimate on the unit torus is

    ||u tensor u||H3<=128||u||infinity ||u||H3.          (11)

One can verify it without an unspecified interpolation constant. Put M=||u||infinity, a=||Du||6, b=||D^2u||3, c=||D^3u||2. Periodic integration by parts gives

    a^2<=6Mb,    b^2<=3ac,

so ab<=18Mc. A second-order version gives ||Du||4^2<=6M||D^2u||2. The ordered Leibniz rules then bound the third derivative by (2+6*18)Mc=110Mc, the second by 14M||D^2u||2, and lower orders by still smaller constants. The Bessel H3 norm is the binomial sum of these ordered derivative squares, proving (11) with 128.

Let Y=||u||H3. Its native energy inequality and (11) give

    Y'<=2^13 ||u||infinity^2 Y/nu.                     (12)

The crude Fourier embedding ||u||infinity<=2Y implies Y'<=2^15Y^3/nu. Therefore Y<=2K up to

    t_* = min{delta, nu/(2^18 K^2)}.

For later times use the actual critical-space solution, not the crude embedding:

    ||u(t)||infinity^2 <=nu/[16 C^2 t].

Equation (12) gives Y'<=Y/t because C=2^40. Integrating from t_* proves (3). The same proof applies to the smooth background with its own supplied initial H3 norm if that bound is needed. This norm affects intermediate resources, not the permitted waiting time.

All estimates can first be performed on smooth approximations. The mild critical-space solution and the strong solution coincide, so neither regularity nor uniqueness is assumed as the conclusion of an a priori bootstrap.

## 6. A nontrivial amplitude-versus-Fourier distinction

For N>=1 let

    v0=e1 cos(2pi x3+N cos(2pi x2)).

It is divergence-free, mean zero, and ||v0||6<=1 regardless of N. Its Fourier absolute mass and Sobolev norms need not stay bounded as N grows. For n>=2 add

    w0=epsilon(2pi n)e2 cos(2pi n x1).

Here Hcal(w0)=epsilon/sqrt(2)<=epsilon. The two native cross advections are nonzero, so the full solution is not merely a passive scalar or linear heat example. The admissible filter interval (1) is independent of N and n, while (3) honestly retains their effect through the total initial H3 norm.

This is an analytic input family, not an executed PDE experiment. It illustrates precisely why replacing a Fourier-absolute background bound by a physical L6 bound can matter.

## 7. Compiler, costs and remaining gap

Given rational bounds A, K, nu and epsilon satisfying (1), the waiting field is exactly zero. Choosing delta as the minimum of the two rational quantities in (1) is a finite rational operation. Every numerical resource displayed is polynomial in A, K, nu, nu^-1 and the requested output tolerance.

For an L6 or L-infinity reset error eta, it suffices additionally to require

    epsilon<=eta sqrt(nu delta)/4.

For the displayed factory, sqrt(nu delta) is rational on either branch: it is 1 or nu^2/(80CA)^2. Thus no real-root oracle is needed. The conservative constants are enormous; no practical runtime or control claim follows.

The input Hcal certification is not free. The preceding lemmas Hcal<=4(Hdot^-1)^1/4(L6)^3/4 and Hcal<=8H1 provide possible paid routes, but an adversarially calibrated repeated word still needs to produce the required split. Single-shear H3-to-L6 bounds cannot be iterated as full L6-to-L6 bounds. A fixed-word low-mode floor cannot be removed merely by changing the continuation norm.

The filter's reference v(delta) is its own nonlinear background solution. It is not asserted close to v0 without an additional regularity/time charge, nor is this a projection onto a known low-dimensional state. No generic fixed-universal-calibration theorem is claimed.

## 8. Primary prior and verification status

Primary source read directly: Koch--Tataru, Well-posedness for the Navier--Stokes equations, Theorems 2--3 and Lemmas 3.1--3.2, https://math.berkeley.edu/~tataru/papers/nas.pdf . Its local critical-space theorem is the exact methodological prior. The quantitative heat split (7), constants, viscosity allocation, physical-L6 background, difference endpoint and polynomial H3 bookkeeping above are the present programme's explicit specialization.

Germain--Pavlovic--Staffilani, https://arxiv.org/html/math/0609781 , supplies stronger known analyticity/derivative context but is not needed as an unpriced numerical constant in this proof. The companion native Wiener filter credits the periodic analytic-Wiener literature separately.

This note is author-derived and awaits a scoped mathematical challenge. No independent constant replay, PDE execution or external novelty assessment is implied.


## ARCHIVE MEMBER: fixed_actuator_reproducibility_20261109/fixed_actuator_critical_heat_bridge_20261109/STRONG_ENDPOINT_RESET.md

Original member bytes: 6065; SHA256: f3bb8bf29ffc06487d1ddcb02de1384eb9156d7d77dbc1a5708fe36ad9492c2f.

# Strong endpoint reset for the L6-background native filter

Date: 2026-11-09. This is an analytic addendum to L6_BACKGROUND_NATIVE_FILTER.md, SHA c6f87541b7e2108cf8de8bdeffa2e59bb30e4af1b202b8a424796b6d8f9ec443. No preceding proof is overwritten. The parent theorem's hypotheses and constants C=2^40, nu*delta<=1 remain in force.

## 1. The full state loses its pre-filter Sobolev cost

Write K2=||u0||2. The actual unforced native filter satisfies

    ||u(delta)||H3 <=16 K2/(nu delta)^(3/2).             (1)

The same bound holds for the background v with K2 replaced by ||v0||2<=A. In particular, the endpoint H3 cost does not depend on the initial H3 norm. The parent theorem still pays a polynomial bound on that norm during the initial portion of the interval; endpoint smoothing is not retroactive regularity.

Here is a direct energy proof with constants. Set E_k(t)=||u(t)||Hk^2 for k=0,1,2,3,4. The explicit tame product estimate with constant128 from the parent proof applies for every k<=3. Therefore

    E_k'+nu E_(k+1)
       <=[nu+2^14 ||u||infinity^2/nu] E_k,
       k=0,1,2,3.                                    (2)

The Hk convention is the Bessel weight (1+4pi^2|k|^2)^k, so the gradient norm squared is exactly E_(k+1)-E_k. This explains the harmless extra nu in (2).

On the final interval [t0,delta], t0=delta/4, critical-space control gives

    ||u(t)||infinity^2 <=nu R^2/t, R=1/(4C).

Put a=nu+2^16 R^2/delta. Since nu*delta<=1, a*delta<2. For F_k(t)=exp[-a(t-t0)]E_k(t), equation(2) reads F_k'+nu F_(k+1)<=0. The derivative of

    sum_(k=0)^3 [nu(t-t0)]^k F_k(t)/k!

is nonpositive. Thus, using native L2 energy contraction,

    E_3(delta)
      <=exp(2) *6/[nu*(3delta/4)]^3 *E_0(t0)
      <128 K2^2/(nu delta)^3.

This proves (1) with16. The argument applies after the already-proved strong existence and also follows uniformly from smooth approximations.

## 2. Fractional regularity of the small remainder

For w=u-v the endpoint estimate improves to

    ||w(delta)||H^(3/4)
        <=32 epsilon/(nu delta)^(7/8).                 (3)

Only an integrable heat singularity is used; no unpriced H1 maximal-regularity theorem is invoked.

On [delta/2,delta], the parent proof gives

    ||w(t)||2 <=||w(t)||infinity
                 <=6 epsilon/sqrt(nu delta),
    ||u(t)||infinity+||v(t)||infinity
                 <=4R sqrt(nu/delta).

Consequently the exact difference source F=v tensor w+w tensor u has

    ||F(t)||2 <=24R epsilon/delta.

For mean-zero data and 0<nu*t<=1, elementary Fourier multipliers give

    ||heat(t)f||H^(3/4) <=2(nu*t)^(-3/8)||f||2,
    ||heat(t)P div F||H^(3/4)
           <=2(nu*t)^(-7/8)||F||2.

Restart the exact difference Duhamel formula at delta/2. Its heat term is below16 epsilon/(nu delta)^(7/8). The source term is at most

    384R epsilon/(nu delta)^(7/8),

because integral_0^(delta/2) t^(-7/8)dt=8(delta/2)^(1/8). Since R=1/(4*2^40), the sum is below32 times the displayed scale. This proves (3).

This bound is substantially stronger than mere L2 proximity. It remains a bound on the native nonlinear remainder; the background is its own actual nonlinear evolution.

## 3. A single subsequent inviscid shear has an action-independent error map

For ANY one native coordinate shear, any static admissible direction/phase/gain, and any action s, its exact inviscid propagator U satisfies

    Fminus1(Uf)<=16||f||H^(3/4).                       (4)

This follows from fiber L2 unitarity, not a physical Lp maximum principle or a scattering constant. For transverse xi!=0, beta=|xi|>=1,

    sum_n 1/(n^2+beta^2)<=5/beta.

Thus the longitudinal contribution is at most
sqrt(5)/(2pi) beta^(-1/2)||f_xi||2. Cauchy--Schwarz over the transverse two-dimensional lattice uses

    sum_(xi!=0) beta^(-5/2)
       <=8 sum_(n>=1) n^(-3/2)<=24.

The complementary weight beta^(3/2) is bounded by the H^(3/4) Fourier weight. The zero-transverse fiber is unchanged and is bounded separately by the ordinary one-dimensional Fourier Cauchy inequality. All fixed factors fit well below16.

The vector polarizations and the phase gauge preserve fiber L2 exactly. Therefore (4) includes both physical polarizations without an additional action-dependent factor.

Combining (3)-(4),

    Fminus1(Uw(delta))
       <=512 epsilon/(nu delta)^(7/8)
       <=512 epsilon/(nu delta).                     (5)

The latter is a simpler entirely rational reserve because nu*delta<=1. Also Hcal<=Fminus1/sqrt(2), so the same conservative bound controls the critical heat error after this one inviscid shear.

This is NOT permission to propagate the same error through an arbitrary word for free. A native short pulse still needs its paid approximation error; successive filters and backgrounds require their own admission budgets. In particular, neither full three-dimensional L6-to-L6 control nor the robust repeated word has been assumed.

## 4. Finite resources and interpretation

The sharper endpoint exponents in(1),(3) can be evaluated with certified rational roots, but this is unnecessary. Since nu*delta<=1, the rational bounds

    ||u(delta)||H3 <=16 K2/(nu delta)^2,
    ||w(delta)||H^(3/4)<=32epsilon/(nu delta)

suffice. They are polynomial in the parent's supplied bounds and reciprocal parameters. For a desired one-shear critical error eta, epsilon<=eta*nu*delta/512 is a paid rational choice.

The important incremental operation is an ACTUAL native nonlinear wait that resets endpoint Sobolev cost using only initial energy, while keeping a small critical remainder with a subsequent action-independent one-shear error map. It removes the need to carry a pre-filter action-cubed H3 bound indefinitely. Producing the admitted L6-background/critical-remainder split under unknown fixed-size transverse errors, and avoiding circular budgets over a growing word, remain open.

All ingredients are established heat, Sobolev and critical-stability methods specialized with explicit constants. No external novelty claim, independent numerical replay, or completed universal-calibration controller is made.


## ARCHIVE MEMBER: fixed_actuator_reproducibility_20261109/fixed_actuator_critical_heat_bridge_20261109/NATIVE_HEAT_REFERENCE.md

Original member bytes: 6238; SHA256: b114fb078476d5baa1fbdc5048ec0431c494df12dfbf0b01dc0d4d68449a1ee1.

# Native heat-reference endpoint and legal shear--heat block

Date: 2026-11-09. Analytic addendum to the frozen L6_BACKGROUND_NATIVE_FILTER.md (c6f87541b7e2108cf8de8bdeffa2e59bb30e4af1b202b8a424796b6d8f9ec443) and STRONG_ENDPOINT_RESET.md (f3bb8bf29ffc06487d1ddcb02de1384eb9156d7d77dbc1a5708fe36ad9492c2f). No existing proof bytes are changed.

## 1. The background has a paid L6 bound

Under the parent filter hypotheses, the actual unforced nonlinear background v obeys

    sup_(0<=t<=delta)||v(t)||6<=2A,                     (1)

where A>=max(1,||v0||6). This is not a maximum principle. It follows from ordinary local heat-Kato contraction with explicit constants.

The Euclidean Oseen kernel bound from the parent proof gives, by Young's inequality and periodization, for 0<nu*t<=1,

    ||exp(nu*t*Delta)P div F||6
       <=2^24 (nu*t)^(-3/4)||F||3.                    (2)

A conservative constant ledger is as follows. Its R3 L^(6/5) norm is below 2^15 t^(-3/4), by the kernel bound 2^12(sqrt(t)+|x|)^(-4) and the radial integral
integral_0^infinity r^2/(1+r)^(24/5) dr <=1/3.
For periodic convolution, the 27 nearest translated cubes cost less than 2^20 t^(-3/4). The remaining maximum-coordinate shells cost below 2^21 because their distances are at least half their index and sum_(n>=2)n^-2<=1. Since t<=1, all of this fits within 2^24 t^(-3/4). Tensor and vector norms remain Frobenius/Euclidean.

Heat itself is L6-contracting. Thus the native mild map on a ball sup||v||6<=2A has bilinear constant at most

    4*2^24 nu^(-3/4) delta^(1/4).

It contracts whenever delta<=nu^3/(32*2^24 A)^4. This is implied by the stronger parent choice delta<=nu^3/(80*2^40 A)^4. The resulting native solution agrees with the parent background by local strong uniqueness, proving (1).

## 2. Native nonlinearity versus literal heat

The true background is not silently replaced by heat. Its difference from heat is the exact Duhamel term

    v(delta)-exp(nu*delta*Delta)v0
       =-integral_0^delta exp(nu(delta-s)Delta)
             P div(v tensor v)(s) ds.

The unit torus has volume 1, so (1) implies ||v tensor v||2=||v||4^2<=4A^2. The fractional Fourier heat estimate from STRONG_ENDPOINT_RESET.md gives

    ||exp(nu*t*Delta)P div F||H^(3/4)
        <=2(nu*t)^(-7/8)||F||2.

Integrating the singularity, which is strictly integrable, yields the paid bound

    ||v(delta)-exp(nu*delta*Delta)v0||H^(3/4)
        <=64 A^2 nu^(-7/8) delta^(1/8).               (3)

This is the key positive time exponent. The analogous direct H1 kernel would have exponent1 and cannot be integrated from an L2 source by the same argument. The choice H^(3/4) is deliberate: it still feeds a single subsequent shear into the critical Wiener norm with a uniform constant.

## 3. Full nonlinear filter compared to heat of the admitted background

Combining (3) with the previously proved difference estimate gives

    ||u(delta)-exp(nu*delta*Delta)v0||H^(3/4)
       <=32 epsilon/(nu delta)^(7/8)
          +64 A^2 nu^(-7/8) delta^(1/8).              (4)

For a requested error eta>0, the entirely rational sufficient choices are

    delta <=min{1/nu, nu^3/(80*2^40 A)^4,
                         eta^8 nu^7/(128^8 A^16)},
    epsilon<=min{nu/(32*2^40), eta*nu*delta/64}.        (5)

The first term of(4) is at most eta/2 because nu*delta<=1; the second is at most eta/2 by the third waiting-time constraint. Therefore the left-hand side is <=eta.

The full native state also has the endpoint smoothing bound

    ||u(delta)||H3<=16||u0||2/(nu delta)^(3/2),

and its intermediate H3 cost is polynomial as stated in the parent theorem. Thus the waiting stage has both a paid linear-reference error and a genuine Sobolev reset.

## 4. How this can realize one shear--heat block

Suppose a separately certified native short pulse applied to f approximates the ACTUAL calibrated inviscid shear U_s f in H1 with error at most rho. Suppose also a proved action-uniform bound

    ||U_s f||6<=A

is available. These are separate inputs: the current physical-Lp construction is a candidate for the second, and the audited BCA short-pulse machinery supplies the first after its required duration/cost allocation.

Decompose the true post-pulse state as

    u0=v0+w0, v0=U_s f.

The already proved Hcal<=8H1 inequality makes epsilon=8rho an admissible bound. Following the real short pulse by the unforced native wait allocated in(5) produces

    ||actual block output-exp(nu*delta*Delta)U_s f||H^(3/4)<=eta.

The wait time is independent of the shear action s once the action-uniform A is paid. The native pulse duration can be chosen separately after s is known. This avoids identifying the short pulse duration with the viscosity/filter duration, which was the earlier source of the delta*action^6 incompatibility.

No fictitious heat evolution was performed: heat is an analysis reference, and(4) pays the actual nonlinear difference. No extra viscosity was introduced. Native energy gives the L2 bound used in the endpoint H3 reset.

## 5. Remaining composition and verification obligations

A robust finite shear--heat word is not proved here. In particular:
- the action-uniform native inviscid H3-to-L6 estimate must be checked at its stated physical-space scope;
- the linear word must be uniformly contracting for every allowed transverse error and phase, retaining all leave-and-return paths;
- pulse durations, actual H3 input bounds, filter intervals and every approximation error must be allocated sequentially without circular or super-polynomial growth;
- the final critical-smallness continuation and terminal-time requirements retain their existing costs.

A potentially useful feature is that the linear shear and literal heat stages are L2 contractions, so already-paid L2 approximation errors cannot be amplified by later LINEAR blocks. This does not by itself prove the active/resonant sector decomposition or the nonlinear implementation.

The local nonlinear theorem, (1)-(5), uses only established heat-Kato/critical-space methods with displayed constants. The three-stage robust composition is owned by the separate return/composition worker. There has been no PDE propagation, numerical control optimization, or external novelty claim.


