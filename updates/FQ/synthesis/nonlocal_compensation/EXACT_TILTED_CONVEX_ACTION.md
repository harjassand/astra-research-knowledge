# Exact oriented free-time actions for the convex complex-tilt family

Date: 15 October 2026. Supplement to NO_LINEAR_SELECTOR.md.

## Result and scope

For real t and rho>0, consider the convex, left-SO(2)-invariant quartic

    C_(t,rho)(X|Y)=|X+(t+i rho)Y|^4.

Let k be any integer and a any complex number. Minimize the action on a strip of width T>0 joining zero to the profile U(y)=a exp(iky), allowing arbitrary smooth multi-frequency strip interiors. Define lambda=rho k and

    I_(lambda,T)=integral_0^T exp((4lambda/3)(T-s)) ds
      =3(exp(4lambda T/3)-1)/(4lambda),  lambda !=0,
      =T,                                      lambda =0.

Then the exact fixed-width minimum is

    Incoming_T(0,U)=|a|^4 I_(lambda,T)^(-3).             (1)

The exact return minimum, with the same arbitrary-interior allowance, is

    Return_T(U,0)=exp(4lambda T)|a|^4 I_(lambda,T)^(-3). (2)

Taking the infimum over all positive widths gives

    Incoming(0,U)=(64/27)rho^3(-k)_+^3 |a|^4,
    Return(U,0)  =(64/27)rho^3( k)_+^3 |a|^4.           (3)

The shear t changes only an optimal phase, not the value. For nonzero a, every fixed-width minimum is attained by a smooth strip. None of the free-width infima in (3) is attained at a finite width: all are limits as T tends to infinity. The trivial profile a=0 has zero action attained at any width.

This is an exact convex-family value calculation, including all compatible interior frequencies. It is not a quasiconvexity advance for negative-valued energies, a solution of the universal left-invariant problem, or a historical novelty claim. Originality remains UNKNOWN.

## 1. Averaging eliminates all interior frequencies except k

Let Phi(x,y) be any smooth competitor with the stated boundary profiles. For theta in the transverse circle, set

    (G_theta Phi)(x,y)=exp(-ik theta) Phi(x,y+theta).

Both boundary profiles are fixed by G_theta. The complex multiplier is a constant output rotation, and the shift is a transverse translation. Therefore C_(t,rho) has the same action on every G_theta Phi.

Average these competitors:

    Psi(x,y)=(1/(2pi))integral_0^(2pi) G_theta Phi(x,y) dtheta
            =r(x)exp(iky).

Convexity of C_(t,rho), applied pointwise to the gradient and then integrated, gives action(Psi)<=action(Phi). Thus restricting to this single transverse mode does not change the global fixed-width infimum. The reverse inequality holds because single-mode strips are admissible competitors.

This is an energy-decreasing symmetry projection justified by convexity. The same argument cannot be imported for a general rank-one-convex nonconvex quartic.

## 2. Phase gauge and exact Holder bound

For Psi=r(x)exp(iky), the complex quantity inside the fourth power is

    (r'+ikt r-rho k r)exp(iky).

Write r(x)=exp(-ikt x)z(x). The action becomes

    integral_0^T |z'-lambda z|^4 dx,
    z(0)=0, z(T)=exp(ikt T)a

for an incoming path. Put v=z'-lambda z and A=exp(ikt T)a. The endpoint equation is

    A=integral_0^T exp(lambda(T-s))v(s) ds.

Holder's inequality with exponents 4 and 4/3 gives

    |A| <= (integral_0^T |v|^4 ds)^(1/4)
             I_(lambda,T)^(3/4).

Therefore the action is at least |a|^4 I_(lambda,T)^(-3).

Equality is achieved by the explicit smooth control

    v(s)=A exp(lambda(T-s)/3)/I_(lambda,T).              (4)

Indeed its endpoint integral equals A and its fourth-power integral equals |A|^4 I^(-3). Solving z'=lambda z+v with z(0)=0 produces a smooth minimizer with exactly the prescribed endpoint. This proves (1).

For a return path z(0)=a and z(T)=0, the endpoint equation instead requires

    integral_0^T exp(lambda(T-s))v(s) ds=-exp(lambda T)a.

The same Holder bound and equality control give (2).

## 3. Free-width limits and attainment

If lambda>0, I increases without bound, so the incoming infimum is zero. For the return value,

    exp(4lambda T) I^(-3)
      =(4lambda/3)^3(1-exp(-4lambda T/3))^(-3),

which decreases strictly to (4lambda/3)^3.

If lambda<0, I increases strictly to 3/(4|lambda|), so the incoming value decreases strictly to (4|lambda|/3)^3. The return value tends to zero.

If lambda=0, both values are |a|^4/T^3 and tend to zero.

For nonzero a the relevant fixed-width formulas are strictly above their limiting values at every finite T. This proves the nonattainment assertion and (3). The formal controls on an infinite strip explain the limits, but finite-strip limiting sequences suffice for the proof.

## 4. An actual nonlocal nonlinear model, and its limitation

For this convex family define the required supply on an arbitrary smooth profile U by the infimum of incoming actions over all finite widths and compatible strips from zero to U. Pointwise nonnegativity gives a lower bound zero. A unit-width straight strip gives a finite upper bound. Thus the value is finite without invoking quasiconvexity.

Concatenating an almost minimizing incoming strip with any prescribed transition proves that this value is a dominating profile functional. Piecewise smooth concatenations can be smoothed near their joins while keeping the outer traces fixed and approximating the quartic action in W^(1,4). This is the established required-supply construction; its existence here is independently secured by pointwise nonnegativity.

Equation (3) computes its value on every individual circular Fourier mode even though its definition allows arbitrary-frequency interiors. It has quartic amplitude scaling, cubic frequency scaling, orientation sensitivity and cubic dependence on the ellipticity parameter rho.

This is a useful exact model for a genuinely nonlocal, nonlinearly coefficient-dependent construction. It does not solve the hard part of extending it to negative-valued rank-one-convex energies: there the required-supply lower bound is not automatic. The supplement is not offered as a renamed no-negative-cycle solution.

Any normalized dominating functional for C_(t,rho) must lie between negative return cost and incoming cost. Therefore on a mode,

    -(64/27)rho^3(k)_+^3|a|^4
       <= P_C(a exp(iky))
       <= (64/27)rho^3(-k)_+^3|a|^4.                    (5)

Both sides are the sharp extremal-storage bounds: incoming required supply dominates, and negative return cost also dominates by concatenation. They give an exact calibration test for nonlinear proposals.

## Verification and provenance

The proof is analytic, based on convex group averaging, a scalar linear ODE and Holder equality. The accompanying verify_no_linear_selector.py additionally checks the finite-T equality-control integrals and free-width constants by exact symbolic calculation. It does not sample all competing fields.

The general storage/required-supply framework is prior:

[J. C. Willems, Dissipative Dynamical Systems, Part I: General Theory (1972)](https://doi.org/10.1007/BF00276493).

Convex averaging, linear controllability and Holder duality are standard ingredients. No comprehensive priority search for the present explicit family formula was performed. Originality is UNKNOWN.
