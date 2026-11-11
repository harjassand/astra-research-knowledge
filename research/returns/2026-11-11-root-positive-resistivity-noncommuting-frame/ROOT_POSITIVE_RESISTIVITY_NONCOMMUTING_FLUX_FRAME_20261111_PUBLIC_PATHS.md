Positive resistivity leaves the ideal commuting-frame sector: an exact example
ROOT, 11 November 2026 Brisbane

RESULT AND SCOPE. In the actual resistive INDUCTION equation with a prescribed
smooth-in-space velocity, two finite-duration nonnegative shear pulses produce
a determinant-one, divergence-free, mean-I response matrix whose columns do
not commute. The conclusion holds uniformly for EVERY unknown measurable
scalar rho(t) in[rho_-,rho_+],0<rho_-<=rho_+<=1. No inverse heat or negative
resistivity is used. The response has an explicit positive L2 distance from
EVERY single volume-preserving ideal-flow frame. This settles a kinematic
representation boundary, not the full coupled twelve-force MHD compiler.

1. TWO FINITE PULSES AND AN EXACT FINITE FOURIER SOLUTION

Put kappa=2pi, l=e1,k=e1+e3,m_+=2e1+e3,m_-=e3. Choose rational
0<a,b<=1/512. On the first interval[0,a] prescribe
 u(t,x)=v(t)e3 sin(kappa x1), v(t)=4t(a-t)/a^2.
On the second interval[a,a+b], with local time t in[0,b], prescribe
 u(a+t,x)=w(t)e2 sin(kappa(x1+x3)), w(t)=4t(b-t)/b^2.
Both velocities vanish at their interval endpoints. They are continuous at
the switch, nonnegative scalar pulses with peak one and integrals2a/3,2b/3.
There is no impulse in the induction equation. Write
 lambda(t)=kappa^2 rho(a+t)
on the second interval. Only positive scalar diffusion is present.

Starting from ANY constant vector H, the first pulse gives exactly
 B=H+q(t)H1 cos(kappa x1)e3,
 q'=kappa v-kappa^2 rho(t)q, q(0)=0.
Let q0=q(a)>0. During the second pulse set
 B1=H1,
 B3=H3+q(t)H1 cos(kappa x1),
 B2=H2+r(t)(H1+H3)cos(kappa(x1+x3))
       +s_+(t)H1 cos(kappa(2x1+x3))
       +s_-(t)H1 cos(kappa x3).
Direct substitution into B_t=rho Delta B-(u.grad)B+(B.grad)u gives
 q'=-lambda q,                 q(0)=q0,
 r'=kappa w-2lambda r,         r(0)=0,
 s_+'=kappa w q/2-5lambda s_+, s_+(0)=0,
 s_-'=kappa w q/2-lambda s_-,  s_-(0)=0.                 (1)
The advection term vanishes in this second interval because all fields are
independent of x2. The first interval also has vanishing advection on its
displayed solution. Product-to-sum of cos(l.x)cos(k.x) gives the TWO cross
frequencies. Their squared lengths5 and1, rather than3, are essential.
Equations (1) are finite explicit integral formulas, valid for bounded
measurable rho; no derivative or sample of rho is evaluated by the pulses.

At the endpoint write B=Pi_rho H and C_j=Pi_rho e_j. Then
 C1=e1+[r cos(kappa k.x)+s_+cos(kappa m_+.x)
             +s_-cos(kappa m_-.x)]e2+q cos(kappa l.x)e3,
 C2=e2,
 C3=e3+r cos(kappa k.x)e2.                              (2)
Every column has zero divergence, mean Pi_rho=I, and det Pi_rho=1 pointwise.
All coefficients q,r,s_+,s_- in (2) mean their values at t=b.

2. THE POSITIVE-TIME COMMUTATOR DEFECT HAS A FIXED SIGN

For the usual vector-field bracket define
 d_+=s_+-qr/2, d_-=s_--qr/2.
Since (qr/2)'=kappa w q/2-3lambda qr/2, (1) gives EXACTLY
 d_+'=-5lambda d_+-lambda qr,
 d_-'=-lambda d_-+lambda qr, d_+(0)=d_-(0)=0.             (3)
Here q>0 and r>0 in the interior. Therefore d_+(b)<0<d_-(b) for EVERY
admitted rho. Direct differentiation of (2) yields
 [C1,C3]=kappa[d_+sin(kappa m_+.x)
                    +d_-sin(kappa m_-.x)]e2.           (4)
For rho=0 the defects vanish and the ideal frame is recovered. With positive
rho, unequal cross-mode diffusion gives the nonzero bracket. This is an
actual finite-time induction evolution, not merely its Lie algebra.

3. A UNIFORM PAID LOWER BOUND

Let lambda_+=kappa^2 rho_+. For0<=t<=b,
 q(t)>=(2kappa a/3)exp[-lambda_+(a+t)],
 r(t)>=kappa exp[-2lambda_+t] integral_0^t w(s)ds.
The integrating factors in (3) and lambda>=kappa^2 rho_- imply
 |d_+(b)|,d_-(b)
 >=(2kappa^4 rho_- a/3)exp[-lambda_+(a+5b)]
           * integral_0^b integral_0^t w(s)ds dt
 =(2kappa^4 rho_- a b^2/9)exp[-lambda_+(a+5b)].           (5)
The last equality uses the symmetry of w and integral w=2b/3, so the double
integral is b^2/3. Since a,b<=1/512,rho_+<=1,kappa^2<40, the exponent in
(5) is below one. Thus both defects have magnitude at least
 D0=2kappa^4 rho_- a b^2/27.                             (6)
This lower bound has polynomial inverse numerical cost in rho_-^-1,a^-1,
b^-1. It is uniform over arbitrary coefficient switching, not only Lipschitz
profiles. It does not make the four endpoint coefficients profile independent.

4. POSITIVE L2 DISTANCE FROM ALL SINGLE IDEAL-FLOW FRAMES

A smooth volume-preserving diffeomorphism pushes constants to divergence-free
columns F_j=Phi_*e_j satisfying[F1,F3]=0. This property is closed under strong
L2 convergence of the frame columns: for divergence-free columns the bracket
is the distributional divergence of their antisymmetric tensor product, and
strong L2 convergence makes those products converge in L1.

The explicit version uses the test e2 sin(kappa m_+.x). Orthogonality in (4)
gives an absolute pairing kappa|d_+|/2. Put delta=||Pi_rho-F||L2,Frobenius.
The tensor-product difference and Cauchy--Schwarz give
 kappa|d_+|/2
 <=2kappa sqrt(5) delta(||C1||2+||C3||2+delta).
The elementary upper bounds
 q<=2kappa a/3, r<=2kappa b/3,
 0<=s_+,s_-<=2kappa^2 ab/9
imply ||C1||2+||C3||2<=4 in the selected range. If delta<=1, then
 delta>=D0/(20sqrt(5))>=D0/60.
If delta>1 the same weaker bound holds since D0<1. With kappa>6 this gives
the simple rational conservative separation
 ||Pi_rho-Phi_*I||L2 >=rho_- a b^2.                     (7)
This is a separation from SINGLE ideal-flow responses and their strong-L2
closure, not an obstruction to other resistive evolutions or a negative for
the full magnetic-response compiler. Arbitrary high derivatives in Phi do
not invalidate the tensor-product argument.

5. NORMS, REPRESENTATION, AND THE MISSING PHYSICAL INTERFACE

There are only four nonzero Fourier frequencies in (2). Direct orthogonality
gives
 ||Pi_rho||H1^2=3+[(1+kappa^2)q^2+2(1+2kappa^2)r^2
              +(1+5kappa^2)s_+^2+(1+kappa^2)s_-^2]/2<4.
Thus the response is inside the norm bound K=2 used by the current question.
Every fixed H^m norm is bounded polynomially in a,b and the integrated pulse
amplitudes. The prescribed velocity has bounded spatial derivatives, integral
norm O(a+b), temporal slope O(a^-1+b^-1), and rational quadratic temporal
coefficients of bit length O(log a^-1+log b^-1). These are velocity/induction
costs, not the emitted FORCE costs of the full MHD question.

Material limitations remain:
 - The second spatial shear is diagonal, outside the twelve fundamentals.
   Algebraic mode generation or a velocity endpoint writer does not provide
   the prescribed velocity trajectory used in this prototype.
 - Velocity is prescribed here. Lorentz backreaction, unknown viscosity,
   actual momentum-force compilation, all-H1 disturbances/weak realizations
   and a velocity reset preserving magnetic memory are NOT constructed.
 - Pi_rho depends on the unknown resistivity history. Nonzero defects with a
   uniform sign and lower bound do not give a chosen fixed Pi for all histories.
 - Coefficients are explicit real integrals, generally irrational. Rational
   approximation for a known profile needs actual effective profile access
   and quadrature error; no such access is granted to the ensemble compiler.
 - No general matrix-target reachability or claimed100-point consequence follows.

This note uses direct finite Fourier substitution, scalar integrating factors
and an L2 tensor estimate. No source recovery, PDE/optimizer oracle, numerical
experiment, additional worker or external theorem is needed. It supplies a
specific positive-resistivity mechanism that escapes the ideal-frame sector,
while exposing the exact interfaces still needed for the physical question.
