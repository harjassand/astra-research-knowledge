# Which operation can preserve density while controlling transport?

30 October 2026. Root derivation after the completed Gaussian construction.
This changes the nonlinear target rather than declaring that target solved.
The finite-dimensional identities below are exact. Their use as a limit of
the particle-field apparatus remains unproved. Metric projection and passive
network interconnection are established machinery, not new principles claimed
here.

## 1. The question is about an actual port

Let j be the actual native current, let B be its divergence map, and let M be
a symmetric positive definite native mobility. Fix a full-column-rank matrix H
of protected current directions, with BH=0. We want H* j=0 while preserving
the density response and noise. Put G=H* M H and

    Q=I-H(H*H)^(-1)H*.

Three operations must not be confused: adding reciprocal constraint forces
to the existing native force/current port; transforming both bath force and
delivered current through a new transducer; and adding physical transport
channels with their own matched response/noise. They can impose the same
algebraic constraint and give different density laws. The signed-ladder
construction realizes the first operation at its declared macroscopic
objective. It does not supply the other two for a different native system.

## 2. An exact response-and-noise criterion

At a frozen native state, write the unconstrained infinitesimal current as

    dJ=b dt+sqrt(2M)dW.

The ideal force-only reciprocal constraint adds the Lagrange force H dLambda
before multiplication by M. Eliminating dLambda from H* dJ=0 gives

    T_M=I-MH G^(-1)H*,
    dJ_c=T_M b dt+T_M sqrt(2M)dW,
    M_c=T_M M T_M*=M-MH G^(-1)H*M.                         (1)

For a physical force b=Mf, response is M_c f and covariance is 2M_c dt.
This native metric projection generally differs from Q M Q. The density
covariance removed by it is exactly

    2B(M-M_c)B*=2(BMH)G^(-1)(BMH)*.                        (2)

Consequently these statements are equivalent: density noise covariance is
unchanged; B M_c f=B M f for every force f; and BMH=0. The first follows
because (2) is L L* for L=sqrt(2)BMH G^(-1/2). The response difference is
BMH G^(-1)H*M; multiplication on the right by H proves its converse.

Topology alone, BH=0, is insufficient. The protected directions must remain
divergence free after multiplication by the actual mobility. In the accepted
two-ring theorem M is a spatially constant scalar on each ring, so BMH=0
even when the unknown scalars differ. Spatially varying mobility usually
fails this condition. The general impedance receiver retained the native
metric and did not promise unchanged densities.

There is a useful stronger finite-dimensional statement. Among any symmetric
mobilities M' with 0<=M'<=M and M'H=0, a choice satisfying
B M' B*=B M B* exists if and only if BMH=0. Necessity: L=M-M' is positive,
B L B*=0 implies BL=0 by its square-root factorization, and then
BMH=B M'H+BLH=0. Sufficiency is M'=M_c. A reciprocal passive impedance
added in series at the unchanged native current port has DC mobility at most
M, so this class cannot evade the condition. This is a specified port/DC
statement, not a prohibition on every passive architecture or frequency.

## 3. The nonlinear density-action target changes

Use noise convention 2 chi(rho), native current b=-partial_x rho, and

    I_native(rho,j)=1/4 int (j+partial_x rho)^2/chi(rho),
    chi(rho)=rho(1-rho),  rho_t+partial_x j=0.              (3)

This is a time-rescaled convention of the established exclusion current LDP.
Take smooth profiles bounded away from zero and one for this calculation.
The periodic gradient b has zero mean for every profile, so a harmonic
constraint leaves the typical heat current feasible. It does not make (2)
vanish: chi(rho(x)) sends a constant current direction to a nonconstant one.

For a density path let k(t,x) be its unique zero-mean continuity current.
Every compatible current is k+I(t). Define

    u=k+partial_x rho,
    R=int_0^1 1/chi(rho) dx,
    L=int_0^1 u/chi(rho) dx,        I_*=-L/R.               (4)

Native density contraction chooses I_* with instantaneous cost
`(int u^2/chi-L^2/R)/4`. Pinning I=0 adds L^2/(4R). For two native rings,
imposing equal mean currents adds to their two contracted density costs

    R_1 R_2/[4(R_1+R_2)] (I_(1,*)-I_(2,*))^2.              (5)

The common minimizing current is -(L_1+L_2)/(R_1+R_2). This follows directly
by completing the two current squares. It vanishes for the constant-mobility
harmonic model, where k and rho_x both have zero mean.

An explicit smooth example is rho=m+a cos(2 pi(x-vt)), with
0<a<min(m,1-m). Then k=v(rho-m), the derivative contribution to L integrates
to zero, and

    L=v[(1-m)/sqrt((1-m)^2-a^2)-m/sqrt(m^2-a^2)].           (6)

It is nonzero for nonzero v and m!=1/2. For m=1/4, a=1/8,
R=8/sqrt(3)+8/sqrt(35) and L/v=6/sqrt(35)-2/sqrt(3).
A second flat static ring has I_(2,*)=0. Equation (5) is then strictly
positive on every interval of positive duration. This falsifies the intended
unchanged-density-action target for the ordinary reciprocal constraint law.

At a frozen nonflat profile, the two-ring constraint H=(1,-1) removes a
rank-one density covariance generated by
(-partial_x chi(rho_1),+partial_x chi(rho_2)). It introduces cross-ring density
noise when both profiles are nonflat. Static equilibrium, the typical heat
equation, a flat-profile CLT, and the full nonflat action remain different.

This identifies the ideal metric constraint's consequence. It does not prove
that the particle-field operation converges to (1) or to the constrained
version of (3). Weighted replacement and field averaging under actual tilted
histories are still needed for that receiver.

## 4. Force normalization is part of the physical comparison

For a general drift b let b_c=T_M b. On H* j=0, completion of the square gives

    1/4 (j-b)*M^(-1)(j-b)
      =1/4 (j-b_c)*M^(-1)(j-b_c)
        +1/4 (H*b)*G^(-1)(H*b).                           (7)

The physical constrained Gaussian rate is the first term, with minimum zero.
Restricting the native forced action alone retains the second, spurious term.
For (3), unforced b is feasible; the density penalty (5) instead comes from
the changed minimizing current. No postselection identity is substituted for
an actual changed operation.

## 5. A constructive stronger port and its missing resource

The geometric mobility M_g=Q M Q is symmetric positive, blocks H, and obeys

    B M_g B*=B M B*.                                       (8)

It therefore can preserve native density response to density-conjugate forces
and density noise for nonuniform M. It is a different operation, not a
counterexample to (2). The exact additional channel after (1) is

    M_g=M_c+E,
    E=QMH G^(-1)H*M Q=U U*,    U=QMH G^(-1/2).              (9)

To prove this, project (1) on both sides by Q and use Q M_c Q=M_c. E is
positive and has rank at most the number of constraints. An actual independent
additional current port

    dJ_add=E f dt+sqrt(2)U dV                               (10)

would restore M_g while H* dJ_add=0. Both response and noise must be supplied.
The native current must include this added transport. Adding noise to a
measurement, relabeling an apparatus output or subtracting a measured mean
afterward does not implement (10).

For constant M,B and a regular confining, possibly nonlinear potential V(x),
the combined operation with f=-B*grad V gives

    dx=-B M B*grad V dt+noise of covariance 2B M B*dt.

It has exactly the native complete density law under the same initial law,
while the total current obeys H* dJ=0. This is a mathematical construction
with an explicit additional port. It is not the particle-field apparatus,
and does not inherit its locality or a supplier. State-dependent mobility
also needs its actual stochastic-calculus drift and state-dependent ports.

Only MH and the small matrix G enter (9), identifying a smaller potential
acquisition target than all of M. Nothing here establishes that they have
been acquired. Actual probes need preparation, force/current access, time,
conditioning and error control; a density clamp would be an extra operation.
Realizing the generally extended U requires coordinated native actuation and
matched shared noise, or a justified local dynamic replacement. The algebra
does not supply that capability. The existing complementary role reconstructs
the conventional two-sided transformer separately, including its change of
current interface.

## 6. Selection and primary credit

The completed local signed-ladder law is the main positive result. A nonlinear
extension should target its actual metric-projected law, or build a different
port if unchanged rare density histories are required. Tightening the counter
tail cannot resolve this choice. An ordinary designer given (10) or a two-sided
flow transformer can use it as well.

The native action and contraction are established: Bertini, De Sole,
Gabrielli, Jona-Lasinio and Landim, *Large deviations of the empirical current
in interacting particle systems*, Theory Probab. Appl.51,2-27(2007),
https://arxiv.org/pdf/math/0512394, especially (1.2), (2.6) and Theorem 2.2.
The root read those actual statements. Metric constraints and matched noise
have direct precedent in Lelievre, Rousset and Stoltz,
https://arxiv.org/pdf/1006.4914, equations (1.7), (CL) and their thermal
interface. The contribution here is selection information for the actual
transport-design task, not priority for quadratic contraction or projection.
