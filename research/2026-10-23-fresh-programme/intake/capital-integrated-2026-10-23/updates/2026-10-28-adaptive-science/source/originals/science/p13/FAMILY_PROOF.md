# General five-root principle and analytic two-cost design family

This extends the finite construction to an all-frequency conditional design
theorem, a nonsingular analytic resource inverse, and an open family of
finite global optima near the certified joint budget. It does not assert
coverage of every possible resource tuple. `PROOF.md` owns the convergent
series sign-variation lemma and frozen-source identities;
`JOINT_CAP_PROOF.md` supplies a certified nonempty member. Frequencies below
are dimensionless in the case's fixed frequency units; logarithms can
equivalently use any fixed positive reference w_ref=1 in those units.

## Universal five-root bound

At theta=1/2 let

    F(w)=w^3 g(w)+lambda*w^2+2mu*w^4+4nu*w^6-eta,
    nu>0, eta>0,

with arbitrary real lambda and mu. Define Q=F*sinh^2(w)/w^2. Its constant
is -eta, sole odd term is +w^3, and positive multiples of its even
coefficients are

    B1=lambda-eta/3,
    B2=lambda+6mu-2eta/15,
    Bn=lambda+mu*n(2n-1)+nu*n(n-1)(2n-1)(2n-3)
          -4eta/[(2n+2)(2n+1)]  (n>=3).

For real x>=3 extend the final expression to B(x). Direct differentiation
gives the strict sign

    B'''(x)=nu*(96x-72)
          +192eta*[(2x+1)^(-4)-(2x+2)^(-4)] > 0.

Rolle's theorem bounds the real zeros of B in this interval by three with
multiplicity. Thus the sampled tail B3,B4,... has at most three sign
variations after zero coefficients are omitted, and it ends positive.
If its first nonzero sign is negative, the tail has at most three
variations and the prefix [-eta,B1,+w^3,B2,negative] at most two. If its
first sign is positive, its eventual positive sign makes its variation
count even, hence at most two, while the prefix has at most three.
In either case the entire Q series has **at most five sign variations**.

The convergent-series lemma therefore bounds the positive roots of F,
counting multiplicity, by five. If F has five distinct positive roots, all
are simple and its negative set is exactly three alternating bands.
This holds for every lambda,mu whenever nu,eta>0, without a candidate
specific coefficient-tail computation. For general theta>0 set a=2theta
and w=a*x; dividing F by a^3 gives the barred parameters

    lambda_bar=lambda/a, mu_bar=mu*a,
    nu_bar=nu*a^3, eta_bar=eta/a^3.

Their proper signs persist, so the theorem applies at every positive
temperature.

## Conditional global optimality and minimal active order

Take any actual finite strict three-band spectrum with its complete trace
and log moments fixed, whose interpolated dual has all five edges roots
and nu,eta>0. For every legal finite graph with no larger incident-stiffness
moment E and compliance moment D, the whole-axis negative-set argument is

    J-J_*=integral R(chi-chi_*)-nu*(E-E_*)-eta*(D-D_*) >=0,
    R=F/w^3.

Total spring cost is at least incident cost, so this includes total-spring
caps saturated by the candidate star. Source F's complete inverse realizes
every strict three-band response as a positive two-pendant star. Three
nonempty bands require two active internal resonances and that order
suffices. Additional dark modes do not change the response.

This is conditional on actual existence at the desired resources. The
finite construction supplies it at the main joint-cap example, and the
executable interval procedure below supplies nine additional points.

## A nonsingular analytic resource inverse

Write a_vec=(lambda,mu,nu,eta). In the proper five-root region, order the
roots x1<...<x5 and set epsilon=(+1,-1,+1,-1,+1). Define

    ell=sum_i epsilon_i*log(x_i/w_ref),
    T=sum_i epsilon_i*x_i^2,
    E=sum_i epsilon_i*x_i^4,
    D=(sum_i epsilon_i*x_i^(-2)-1/2)/2.

The fixed reference contributes only a constant to ell. On ell=log(sqrt2)
with w_ref=1, T=4, these are precisely D=C_CM/4 and
E=16+8*k_incident. Off that fixed-ell slice D is simply a mathematical
fixed-reference moment; no changed-mass compliance interpretation is
assumed.

The root equation R(x,a_vec)=0 has

    u(x)=(1/x,2x,4x^3,-x^(-3))^T,
    dx=-u(x)^T da_vec/R'(x).

The exact root-to-resource Jacobian is consequently

    D_a(ell,T,E,D)
      =-sum_i [epsilon_i/R'(x_i)] u(x_i)u(x_i)^T.              (6)

Every weight is strictly positive by the alternating simple-root signs.
Any four distinct u vectors span R^4: multiply a vanishing linear
combination by x^3 to get a cubic in x^2 with four distinct roots, which
must have every coefficient zero. Hence (6) is symmetric **strictly
negative definite** and nonsingular.

The roots, resources, and local inverse are real analytic by the implicit
and inverse function theorems. Positive star masses/springs and proper
multiplier signs persist on an open neighborhood of the certified design.
Restricting ell and T to their fixed-mass values gives an **open analytic
two-parameter family** of finite globally optimal two-pendant cells as
(C,kappa) vary near (1/20,24). This continuum claim follows from the
Jacobian proof, not a finite sweep. No uniform neighborhood size or
conditioning bound is asserted.

The map is injective onto its whole proper five-root resource image.
Two duals with equal resources give global comparisons both ways; equality
forces the same minimizing indicator and five edges. Their difference,
multiplied by w^3, is a cubic in w^2 with five distinct roots, and hence is
identically zero. The local inverses therefore agree on overlapping
images. We have an analytic inverse onto this open image, without claiming
that the image covers all feasible resources or a global phase diagram.

The optimum value V satisfies dV=-a_vec dot d(ell,T,E,D). Since (6) is
strictly negative definite, its resource Hessian is strictly positive
definite. On the physical fixed-mass slice,

    partial V / partial kappa = -8nu,
    partial V / partial C     = -eta/4.

At the certified point these are approximately -5.67825231557415e-6 and
-0.3883275483906613. These are local marginal resource values, not promises
about a large change or fabrication tolerances.

## Executed construction across nearby resources

`construct_joint_family.py` constructs all nine points from
C in {0.049,0.05,0.051} and kappa in {23.5,24,24.5}. For every point,
high-precision arithmetic proposes a scalar h bracket; exact rational
interval arithmetic then proves opposite fifth-edge residual signs,
positive finite components, proper nu,eta, and full Bose integral bounds.
Each star enforces C and kappa algebraically before the scalar search.
The universal five-root theorem proves globality of each exact candidate.
Outputs are retained in `CERTIFIED_JOINT_FAMILY.txt`. For example,

    C=.049,kappa=24: J in [1.142404896294113979,
                           1.142404896294113980],
    C=.051,kappa=24: J in [1.141628237579639369,
                           1.141628237579639370].

`construct_joint_extended.py` additionally certifies five points at C=1/20
and kappa in {20.01,20.1,21,30,100}, with full positive realization and
proper multipliers. These include small slack above the exact feasibility
boundary and a much larger finite stiffness budget. They are global
optima at their exact specified resources, but the finite list does not
prove coverage of every intermediate kappa. Their outputs are preserved
in `CERTIFIED_JOINT_EXTENDED.txt`.

The open analytic family, finite interval-certified members, complete
positive inverse, and physical limits are distinct claims. No historical
priority, actual device, or practical advantage is established.
