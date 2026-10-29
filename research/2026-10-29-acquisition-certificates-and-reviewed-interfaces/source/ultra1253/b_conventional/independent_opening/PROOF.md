# An evaluable global analytic potential from compatible torus jets

29 October 2026. New internally derived construction. Historical priority
UNKNOWN. Ordinary analytic extension/interpolation is established; the
specific operation acquired here is an explicit global formula, including a
global Hessian bound and an exponential Fourier truncation rule. It is not a
new physical computing device, a numerical trajectory accelerator, or a
claim that a representation theorem alone is a leading civilisation-scale
capability. The equally informed ordinary comparison is in PRIOR_AND_DECISION.md.

## 1. Native input and output

Let Q:T^n -> R^D be analytic and supply a fixed REAL LINEAR map
L:R^D -> R^(2n)=C^n such that

    L Q(phi) = i(phi) = (exp(i phi_1),...,exp(i phi_n)).       (1)

This supplies an embedding and an explicit coordinate interface, not an
unacquired inverse or nearest-point projection. Let analytic f:T^n->R and
g:T^n->R^D obey the exact jet compatibility

    DQ(phi)^T g(phi) = Df(phi).                             (2)

For some known rho>0 assume finite weighted Fourier norms

    M= sum_k exp(rho |k|_1) ||Qhat_k||_2,
    F= sum_k exp(rho |k|_1) |fhat_k|,
    G= sum_k exp(rho |k|_1) ||ghat_k||_2.                    (3)

Coefficients, norm upper bounds and coefficient-evaluation costs are INPUTS.
For the previously acquired finite-Fourier/Gunther torus construction, its
explicit analytic contraction acquires them; arbitrary black-box smooth
functions do not. The theorem below is independent of a Turing simulator.

Output a globally real-analytic W:R^D->R, evaluable by the series/formula
below, with

    W(Q(phi))=f(phi),   grad W(Q(phi))=g(phi),
    W(0)=0,            grad W(0)=0,                         (4)

and an explicit global Hessian bound linear in F and G at fixed Q,L,rho.
The same construction controls every prescribed finite derivative order.
In particular, if that Hessian bound is less than eta<1, then

    V(q)=|q|^2/2+W(q),   (1-eta)I <= D^2 V <= (1+eta)I,     (5)

with unique minimum V(0)=0. Global real analyticity is asserted, not
holomorphic extension to all of C^D, a polynomial potential, or compact
support. A nonzero analytic correction cannot have compact support.

## 2. A radially flat bounded extension of each Fourier mode

For w=(w_j) in C^n and k in Z^n define

    Phi_k(w)=prod_j w_j^(k_j+) wbar_j^(k_j-)
                 exp[|k_j|(1-|w_j|^2)/2].                 (6)

Every factor has modulus r^m exp[m(1-r^2)/2] <=1 on the REAL
2-plane, by log r <=(r^2-1)/2. For m=0 it is identically one.
At r=1 it has angular value exp(i k_j phi_j) and radial derivative zero.
Consequently, for any Fourier input a set

    E_a(w)=sum_k ahat_k Phi_k(w).                          (7)

The series is real for real-valued a, linear in a, agrees with a on the
unit torus, and its ambient derivative there kills every radial direction.

Here is a global complex-tube bound, so real analyticity does not follow
merely from smooth termwise convergence. Complexify the real and imaginary
coordinates of w. If the imaginary displacement of one real 2-plane has
Euclidean size delta, the absolute value of its degree-m factor is at most

    exp{m sup_(r>=0)[log(r+delta)+(1-r^2+delta^2)/2]}.

At the maximizer r_delta(r_delta+delta)=1 and r_delta<=1.
The derivative of this supremum with respect to delta equals
r_delta+delta<=1+delta. Its value at zero is zero. Hence the supremum is
at most delta+delta^2/2. If each complexified real coordinate has imaginary
part at most h<=1/4, delta<=sqrt(2)h and this is at most4h.
Thus |Phi_k|<=exp(4h|k|_1) on the WHOLE complex tube, uniformly in its real
part. Choose

    h=min(1/4,rho/8),   c_j=j! (2n/h)^j,   ell=||L||_op.   (8)

Then E_a is holomorphic on a larger open tube than the closed tube used
for these estimates and has absolute value/norm at most ||a||_rho there.
Cauchy's formula, followed by ||v||_1<=sqrt(2n)||v||_2<=2n||v||_2, gives

    sup_w ||D^j E_a(w)||_op <= c_j ||a||_rho.               (9)

The vector-valued version follows directly from the normed Cauchy integral.
These are conservative finite constants, not sharp derivative estimates.

## 3. The exact value/force formula

For q in R^D put

    w=Lq,                 r=q-E_Q(w),
    a=E_g(w)-L^T grad_w E_f(w),
    B=E_f(w)+r.a,
    z=|Lq|^2/n,           p=2z-z^2,
    W(q)=p exp(-|r|^2) B.                                 (10)

All operations are finite except the explicitly controlled Fourier sums.
No convex envelope, optimization oracle, implicit closest-point solve or
analytic continuation oracle occurs.

At q=Q(phi), r=0. Let P be the orthogonal projection on the tangent space
of the STANDARD unit torus at w=i(phi). Radial flatness and (1) give

    L D E_Q=P,       grad E_f=P grad E_f.

Compatibility (2), applied to arbitrary angular directions, gives

    (D E_Q)^T g=grad E_f.

Therefore (D E_Q)^T a=grad E_f-P grad E_f=0 and

    grad_q B=L^T grad E_f+(I-L^T(D E_Q)^T)a=g.

Also B=f. The Gaussian factor equals one with zero gradient at r=0;
p equals one with zero gradient when |Lq|^2=n. This proves both graph jets
in (4). At q=0, p=0 and grad p=0, while every other factor is analytic and
finite. This proves the two origin conditions even if r has extraneous
zeros away from the specified torus. It is not necessary that r^{-1}(0)
coincide with Q(T^n).

## 4. A literal global Hessian bound

The following polynomial recipe uses only nonnegative rational/algebraic
upper bounds. Let u be a formal NONNEGATIVE scalar. Define

    F_j=c_j ell^j F,
    A_j=ell^j(c_j G+ell c_(j+1) F),       j=0,1,2,
    R1=1+c_1 ell M,       R2=c_2 ell^2 M.

These bound E_f(Lq), a(q), Dr and D^2r. Since |E_Q|<=M,
|q|<=u+M whenever u=|r(q)|. Form the coefficient-positive polynomials

    b0=F_0+u A_0,
    d0=F_1+R1 A_0+u A_1,
    e0=F_2+R2 A_0+2 R1 A_1+u A_2,
    b1=d0+2 R1 u b0,
    b2=e0+4 R1 u d0+(4 R1^2 u^2+2 R1^2+2 R2 u)b0.

For a0=ell^2/n and v=u+M define

    p0=2 a0 v^2+a0^2 v^4,
    p1=4 a0 v+4 a0^2 v^3,
    p2=4 a0+12 a0^2 v^2,
    H(u)=p0 b2+2 p1 b1+p2 b0=sum_j H_j u^j.                (11)

Leibniz and chain rules give

    ||D^2 W(q)|| <= exp(-u^2) H(u),  u=|r(q)|.

For example ||D exp(-|r|^2)||<=2 exp(-u^2) R1 u and
||D^2 exp(-|r|^2)||<=exp(-u^2)(4R1^2u^2+2R1^2+2R2u).
The three p bounds follow from z=|Lq|^2/n and |q|<=u+M.
Finally exp(-u^2)u^j<=j! for all integers j>=0: for u<=1 this is
immediate, and for u>=1 use the ceil(j/2)-th term of exp(u^2).
Thus the entirely explicit sufficient bound is

    ||D^2 W||_global <= C2 = sum_j H_j j!.                 (12)

H has degree at most seven. At fixed Q,L,rho, C2 is linear in F,G. Its
constants can be very large. The proof bounds the entire Euclidean space,
not a Hessian grid. Repeating this elementary finite polynomial majorant
gives any fixed C^r bound. The origin multiplier increases the degree of
that bound but introduces no uncontrolled global tail.

## 5. Evaluation and real costs

There is a stronger uniform analytic norm, not only separate real derivative
bounds. Complexify ALL real position coordinates and choose

    a=h/[2 max(1,ell)],       Ac=G+2 ell c_1 F.

On the global tube ||Im q||_2<a, the argument Lq is in the inner half of
the extension tube. Hence |E_Q|<=M, |E_f|<=F, and |a(q)|<=Ac by Cauchy
on the remaining half tube. Here the vector named a(q) in (10) is distinct
from the scalar tube radius a. If R=||Re q|| and u=(R-M)_+, then

    |Im r|<=a+M,       |Re r|>=u,
    |exp(-r.r)|<=exp[(a+M)^2-u^2].

The dot products in this display are the HOLOMORPHIC complexification of
the real squares, not Hermitian squares. Put a0=ell^2/n. The coefficient-
positive degree-five polynomial

    Pc(u)=[2a0(u+M+a)^2+a0^2(u+M+a)^4]
                        [F+(u+2M+a)Ac]                   (16)

therefore pays

    sup_(||Im q||<a) |W(q)|
       <=exp[(a+M)^2] sum_j [Pc]_j j!.                    (17)

The right side is linear in F,G at fixed Q,L,rho. The tube radius is
independent of the real position and of a small-parameter family with
uniform Q/L/strip bounds. In particular, such W_epsilon tend to zero in
ONE fixed global holomorphic-tube supremum norm, not only in every fixed
real C^r norm separately. All real derivatives also decay faster than any
fixed inverse polynomial at real infinity. No entire complex extension is
inferred from a fixed tube.

If one truncates to |k|_1<=K, each coefficient tail has weighted rho/2 norm
at most exp(-rho K/2)||a||_rho. Applying the same tube argument with
h=min(1/4,rho/16) controls every fixed derivative of the omitted extension
by c_j exp(-rho K/2)||a||_rho. Elementary interval composition of (10)
then gives any requested local value/force accuracy. It is the FULL series
that has the exact graph jets; truncation is a certified evaluation, not a
different exactly invariant finite polynomial model.

The number of lattice modes is O(K^n). It is exponential in the variable
torus dimension; no dimension-free polynomial algorithm is claimed. If the
input coefficients themselves require expensive computation, that cost is
added. Exact computable coefficients with NO effective tail bound would
not be sufficient for this evaluator. The result supplies no acceleration
of long trajectories or their infinite-time limits.

For a rational one-variable Fourier function, positive/negative Laurent
parts can instead yield a finite expression in algebraic functions,
exponentials and rational operations. The executed constructor implements
that stronger finite operation on the compatible curve family below.

## 6. A complete nonlinear finite-expression input

Take n=1,D=3 and

    Q(phi)=(cos phi,sin phi,delta cos 2phi),
    v2=|Q'|^2=1+4delta^2 sin^2 2phi,
    Z=v2^(-1/2) partial_phi,
    A=Z(ZQ)=Q''/v2-Q' v2'/(2v2^2),
    f=(1-|Q|^2)/2,       g=-A-Q.                           (13)

This has a genuinely nonconstant analytic speed when delta!=0. The curve
is a unit-speed geodesic for its induced one-dimensional metric; hence A
is normal and (2) holds. L is the first-two-coordinate projection. The
script verifies the cleared Laurent compatibility identity EXACTLY.

Using Fourier weight 2^|k| (rho=log2>1/2), one may take h=1/64 and
c_j=j!128^j. Literal rational input bounds are

    M=4+4delta,     F=17delta^2/4,
    U=34delta^2,    U1=128delta^2,
    G=12delta+(4+16delta)U/(1-U)
                       +(4+8delta)U1/[2(1-U)^2],          (14)

provided delta>0,U<1. They follow by the absolutely convergent geometric
series for v2^{-1},v2^{-2}, with the cancellation -Q''-Q retained. The
actual radius/force data and coefficient acquisition are paid here; no
unsolved isometry is an input to this particular execution.

Write S=sqrt(1+4delta^2), c=(1+2delta^2+S)/2 and
r=2delta^2/(1+2delta^2+S). Then

    v2=c(1-r z^4)(1-r z^(-4)),  0<r<1,
    [v2^(-2)]_(4m)=r^|m|(a+b|m|),
    a=(1+r^2)/[c^2(1-r^2)^3], b=1/[c^2(1-r^2)^2].         (15)

The numerator of g is a finite Laurent polynomial. For every monomial
z^k times (15), split m>=0 and m<0 at the finite point where k+4m
changes sign. The remaining rays have the closed forms

    sum_(m>=N) r^m(a+bm) zeta^(k+4m)
      =r^N zeta^(k+4N)[(a+bN)/(1-r zeta^4)
                              +b r zeta^4/(1-r zeta^4)^2],

and its conjugate-variable version, where
zeta=w exp[(1-|w|^2)/2]. Both denominators are globally nonzero on real
input because |zeta|<=1 and r<1. Thus (10) for this input is a FINITE
evaluable global real-analytic potential, with no Fourier-sum oracle.

The exact rational majorant compiler and the high-precision finite-expression
evaluation are separate outputs. Numerical force agreement at a declared
point is a diagnostic of that implementation; it is not the global proof.

## 7. Consequence for the earlier analytic-torus natural construction

This paragraph uses the previously accepted root_natural_well geometry and
the explicit PERIODIC_GUNTHER analytic contraction; it is NOT a new audit of
their universal simulator import. In its retained block write the anchor
and e_i pairs as complex coordinates

    z0=s a exp(i theta),
    z_ci=s c cos(x_i) exp(i theta),
    z_si=s c sin(x_i) exp(i theta).

The FIXED LINEAR extractor

    w0=z0/(s a),       wi=(z_ci+i z_si)/(s c)

has values (exp(i theta),exp(i(theta+x_i))). The corresponding phase map
(theta,x)->(theta,theta+x_i) is an integer torus automorphism. The theorem
therefore applies without changing the embedded configuration dimension,
retained readout coordinates or source dynamics.
One explicit rational upper bound is ell=max{1/(sa),2/(sc)}. Under this
phase substitution a Fourier frequency k becomes k' with |k'|_1<=2|k|_1,
so halving the old analytic-strip width pays the coordinate change. Any
further derivative-strip loss is fixed before epsilon is decreased.

For analytic source Y and the analytic isometry Q_epsilon, use the exact
jets f=(1-|Q_epsilon|^2)/2 and g=-Z_epsilon^2 Q_epsilon-Q_epsilon.
They tend to zero in a smaller fixed analytic Fourier norm as epsilon->0.
This follows from the convergent fixed-point constructor, differentiation
with a fixed strip loss, and Z_epsilon->partial_theta. Its baseline has
|Q_0|=1 and partial_theta^2 Q_0=-Q_0. Q's weighted norm and ||L|| stay
bounded, so (12) tends to zero. Halving rational epsilon until (12)<eta
terminates with computable bounds, at potentially enormous cost/clock
slowdown. Every fixed higher derivative can be paid similarly.

Consequently the old smooth-cutoff torus conclusion can be strengthened to
globally REAL-ANALYTIC near-harmonic natural potentials, still with unique
minimum at zero, V=1/2 and speed one on the invariant torus, common energy
one, and the same quadratic position readout. The compact-support conclusion
is dropped, as it must be. The level V=1/2 is a real-analytic nearly round
strictly convex hypersphere, and the same encoded motions are its geodesics.

This does not turn exact asymptotic noncomputability into a practical
computational capability. Initialization/noise precision, exceptional
invariant geometry, clock slowing, input coefficient costs and long-time
limits remain as in the earlier construction. Only analytic sources are
covered; arbitrary C-infinity source data do not become analytic by this
extension. No universal coefficient table or trajectory has been executed.
