Unknown viscosity: an open-shear tracking boundary and the meaning of phase accuracy
11 November 2026 Brisbane

1. Precise scope.

Use the unit three-torus and F=e_i sin(kappa x_j) or e_i cos(kappa x_j), i!=j, kappa=2pi. Then
 Delta F=-kappa^2F, (F.grad)F=0,
 ||F||2^2=1/2, ||grad F||infinity=kappa.
Take two constants 0<nu_-<nu_+<=1 and T<=1. The SAME ordinary integrable mechanical force f(t,x) is used for both viscosities in
 u_t=nu Delta u-P[(u.grad)u]+f, div u=0.
The force may use all twelve allowed fields, or even arbitrary spatial fields; the proof only requires its projection onto F to be the same. These are admissible zero-magnetic/zero-disturbance realizations of the resistive MHD system. This is a boundary for tracking a specified carrier, NOT a negative theorem for the full endpoint compiler, which permits large intermediate excursions and different parameter-dependent trajectories.

2. A projected identity insensitive to the large reference amplitude.

Let w(t,x)=b(t)F(x), with b(0)=b(T)=0 and impulse a=integral_0^T b(t)dt. Suppose solutions for the two viscosities satisfy u_nu=w+v_nu with
 sup_(0<=t<=T)||v_nu(t)||2<=r.
The bound includes endpoint traces, or follows there from weak continuity and the corresponding essential bound. Smooth solutions suffice; the smooth-test weak momentum identity also proves the statement for energy weak solutions with the stated bounds.

For every solenoidal v,
 <(F.grad)v,F>=-<v,(F.grad)F>=0,
 <(v.grad)F,F>=integral v.grad(|F|^2/2)=0.
Thus ALL reference and mixed terms cancel exactly in the projected convection:
 <((w+v).grad)(w+v),F>=<(v.grad)v,F>.
Its time integral has absolute value at most kappa T r^2. In particular no factor sup|b| or integral|b| enters this nonlinear error.

Let E_nu=integral_0^T<v_nu,F>dt, so |E_nu|<=Tr||F||2. The integrated weak equation is
 <u_nu(T)-u_nu(0),F>
 =-nu kappa^2[a||F||2^2+E_nu]
   -integral_0^T<(v_nu.grad)v_nu,F>dt
   +integral_0^T<f,F>dt.
Subtract the two parameter equations. The chosen force cancels, giving

 kappa^2(nu_+-nu_-)|a|||F||2^2
 <=4r||F||2+kappa^2(nu_++nu_-)Tr||F||2+2kappa Tr^2.  (1)

If both initial velocities are exactly zero, the first constant4 can be replaced by2. The version with4 permits viscosity-dependent entrance errors of size r and therefore applies to a segment inside a larger word. For disturbances bounded by eta in L-infinity L2, add2T eta||F||2; taking disturbances zero already gives the necessary condition(1).

Using 6<kappa<7, ||F||2<1, T<=1 and r<=1 yields the simple necessary bound

 r>=(nu_+-nu_-)|a|/8.                                  (2)

Indeed the left side of(1) is greater than18(nu_+-nu_-)|a| and its right side is at most116r; 18/116>1/8. Numerical force amplitude does not enter this bound. A fixed nonzero open-shear impulse cannot be tracked with arbitrarily small absolute L2 error for two separated viscosities while the velocity starts and ends near rest.

This does not exclude a whole word with zero net projected impulse, impulses shrinking with r, parameter-dependent reference carriers, or a trajectory that leaves the specified shear neighborhood. Nor does it assert that a finite-field endpoint target must be followed continuously. It prevents silently treating an unknown viscosity term on a large carrier as a uniformly tiny additive disturbance without paying the actual path error.

3. An exact isolated-pulse return cannot hold on a parameter interval.

For a single Fourier shear starting from zero, pure-shear force g(t)F gives the EXACT physical solution x_lambda(t)F, where
 x_lambda'+lambda x_lambda=g(t), lambda=nu kappa^2.
If x_lambda(T)=0 for EVERY lambda in a nonempty open interval, then
 integral_0^T exp(lambda s)g(s)ds=0
on that interval. This finite-interval Laplace transform is analytic. All derivatives at an interior lambda0 vanish, so the signed finite measure exp(lambda0 s)g(s)ds annihilates every polynomial. Polynomial density in the continuous functions on[0,T] forces g=0 almost everywhere.

Therefore a nontrivial ordinary isolated pulse cannot have EXACT zero terminal velocity for an entire viscosity interval. The conclusion is for this scalar physical subspace; arbitrary nonlinear multi-field returns are not excluded. Approximate returns with paid tolerance are allowed and are the ones actually supplied by the moment-cancelled construction.

4. The existing two-moment pulse has good phase and endpoints, not small interior velocity error.

Retain r0(z)=z^2(1-z)^2(14z^2-14z+3) from the earlier interface, and apply
 g(t)=A h^-2 r0''(t/h), 0<=t<=h.
Let beta(t)=A h^-1 r0'(t/h) be the ideal prescribed carrier amplitude and alpha_lambda=integral x_lambda. Exact scalar balance gives
 x_lambda(t)-beta(t)=-lambda alpha_lambda(t).
The inherited phase bound is
 |alpha_lambda(t)-A r0(t/h)|<=|A|Lambda h, Lambda=49,
and endpoint phase/velocity are O(h^3). These statements are unchanged.

However r0(1/2)=-1/32. If Lambda h<=1/64, then
 |alpha_lambda(h/2)|>=|A|/64,
 ||x_lambda(h/2)F-beta(h/2)F||2
 >=lambda|A|/(64sqrt2).                                (3)
The right side does NOT tend to zero merely by shrinking h at fixed A,lambda. In fact beta(h/2)=0 by symmetry of r0. The small phase error is obtained by time integration, not by an O(h) instantaneous velocity error.

There is no contradiction with(1): the ideal moment-cancelled loop has a=integral beta=A[r0(1)-r0(0)]=0. Its known, viscosity-independent FORCE is a useful operation. A parameter-dependent exact carrier x_lambda F is also legitimate in a proof of a common-force theorem, provided all estimates are uniform and its computation/observation is not required by the output algorithm. What is invalid is replacing that carrier by beta F in a bootstrap that needs a much smaller absolute velocity perturbation and overlooking(3).

5. Resource and source binding.

The obstruction uses one explicitly known smooth test field and finite integrals. It imposes no external source, computation, observation, parameter oracle or additional physical control. Equation(1) pays an error in the specified trajectory model; it is not a lower bound on every possible endpoint-control force or a claim that the current ensemble question is impossible.

The current full scientific contract is P2_FULL_UNKNOWN_DIFFUSIVITY_ENSEMBLE_MHD_COMPILER_PRO_20261111.txt6772ASCII/SHA2f6bc37b9910bfd6fcc5d5767f8a71b504713b45b1e86426b0e9587f5ae4fd0a. The exact scalar pulse/phase/endpoint identities are inherited from ROOT_UNKNOWN_VISCOSITY_MOMENT_CANCELLED_SHEAR_INTERFACE_20261111.txt9846ASCII/SHA902bd5533f25b20b5a576762339db6f67c2a2709785963aaa8a9363edf4985c7. That construction never claimed uniform interior velocity tracking. The new operations here are the projected nonlinear error floor for an open impulse, the exact-return uniqueness boundary for an isolated pulse, and the explicit interior-velocity lower bound distinguishing the available phase estimate from an unavailable stronger norm estimate. No assertion is made about an unobserved current scientist construction.
