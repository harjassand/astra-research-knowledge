# Direct actual-model capacity by a finite-support exact residual

This construction computes a deterministic probability/capacity interval for
the **actual specified nonquadratic generator**, without a Gaussian formula,
a rare-event observation, an approximate committor oracle, or whole-state
enumeration. It uses ordinary potential theory and Galerkin/CG. The parent
supplied the variational proposal; the identities and integer implementation
below were independently derived in this worker. No historical priority or
new rarity complexity class is claimed.

## 1. Exact model and requested observable

There are M even occupation bits eta_0,...,eta_(M-1), restricted to even
parity. M>=4. Supplied rational inputs satisfy 0<theta_i<1, alpha_i>0 and
delta>=0. State a=0 is vacuum, state b=2^M-1 is full occupation. Adjacent
pair i toggles sites i and i+1. If its bits, ordered from the low site, are
00,10,01,11, the reference rates are respectively

    c_i=alpha_i*theta_i*theta_(i+1)/(1+theta_i*theta_(i+1)),
    r_i=alpha_i*theta_(i+1)/(theta_i+theta_(i+1)),
    l_i=alpha_i*theta_i/(theta_i+theta_(i+1)),
    a_i=alpha_i/(1+theta_i*theta_(i+1)).

The ACTUAL rate multiplies this by 1+delta*eta_j, where j=i-1 for i>0 and
j=2 for i=0. That bit is untouched by the pair flip. Consequently each edge
and its reverse have the same multiplier. Both reference and actual chains
are irreducible on even parity and reversible in

    w(x)=product_i theta_i^(eta_i), w(a)=1, w(b)=rho=product_i theta_i,
    Z_even=[product_i(1+theta_i)+product_i(1-theta_i)]/2.

For delta>0 the local rate for creation depends on an unchanged outside bit;
the accepted prior unit proves a witness excluding a quadratic generator in
the standard occupation-fermion representation. No claim excludes every
alternative integrable representation. The present method needs none.

Every vacuum multiplier is one, so R_a=sum_i c_i is the ACTUAL vacuum exit
rate and its exit law gives pair i probability c_i/R_a. The requested p_exc
is success under that law: hit b before returning to a. It is not a fixed-start
committor or the probability of observing this excursion in a fixed duration.
The normalized capacity/reactive flux is pi(a)*R_a*p_exc.

## 2. Positive inverse problem and capacity bridge

Q is the BACKWARD generator: (Qf)(x)=sum_y q(x,y)[f(y)-f(x)]. Put H=-Q,
with inner product <f,h>_w=sum_x w(x)f(x)h(x). It is self-adjoint,
nonnegative, and has constants as its kernel. The rational source

    u=rho*1_a-1_b

has weighted mean zero and norm squared rho*(1+rho). Retain both components,
including the small vacuum component. Let x=H^+u and

    I=<u,H^+u>_w/rho=x(a)-x(b)>0.

Then h=(x(a)-x)/I is zero at a, one at b and harmonic elsewhere; it is the
usual hit-b-before-a function. At a, Hh(a)=-rho/I=-R_a*p_exc. Also its
unnormalized Dirichlet energy is rho/I. Therefore

    p_exc=rho/(R_a*I),   cap(a,b)=rho/(Z_even*I).

Equivalently, spectral integration gives the positive potential-kernel form

    I=integral_0^infinity f(t)dt,
    f(t)=<u,exp(-tH)u>_w/rho
        =rho*P_t(a,a)+P_t(b,b)-2*rho*P_t(b,a).

Here P_t(x,y) means start x, end y. These are ordinary potential/Dirichlet
identities; the continuous-time exit-rate factor is essential. Primary
antecedents are [Aldous--Fill, occupation identities](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch2.S2.html)
and [their continuous-time Dirichlet statement](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S7.html).

## 3. Acquired analytic gap within the supplied source class

Map walls to n=M-1 interior spins with fixed positive endpoints. With
J_j=-log(theta_j)/2>0, reference spin i is refreshed at rate alpha_i from its
conditional Gibbs law. Its conditional mean is A_i*s_left+B_i*s_right,
where A_i,B_i>=0 and

    A_i+B_i=(1-theta_i*theta_(i+1))/(1+theta_i*theta_(i+1)).

Use common refresh clocks and common uniforms for an ordered extreme-state
coupling. If d_i is the disagreement probability, its exact linear evolution
is d_i'=alpha_i*(A_i*d_left+B_i*d_right-d_i); endpoint disagreements vanish.
The sup norm contracts at least at rate

    g0=min_i alpha_i*(1-A_i-B_i)=2*min_i c_i>0.

Coupling bounds total variation by n*exp(-g0*t). For a finite reversible
chain this implies every nonzero eigenvalue of H_reference is >=g0: apply
the bound to a nonconstant eigenfunction and let t tend to infinity.

Actual rates are at least reference rates on every edge with the SAME w.
Their Dirichlet form is therefore at least the reference form, while the
variance is unchanged. The Rayleigh principle gives gap_actual>=g0. This
does not assume attractiveness of the actual occupation-dependent chain.

Every actual exit rate is at most Rstar=(1+delta)*sum_i alpha_i. Gershgorin
and reversibility give largest eigenvalue <=2*Rstar. Thus

    mu=(1+rho)/(2*Rstar) <= I <= (1+rho)/g0.

The gap and weights are consequences of the exact stipulated source law,
not quantities inferred from a few observed transitions.

## 4. Exact certificate for ANY trial

For any real y, including an arbitrary constant component, put r=u-Hy and

    L=[2<u,y>_w-<y,Hy>_w]/rho.

Completing the square, with x=H^+u, gives

    I-L=<x-y,H(x-y)>_w/rho=<r,H^+r>_w/rho.

The weighted mean of r is zero. Hence

    L <= I <= L+<r,r>_w/(rho*g0).                         (C)

If y has finite support, Hy is supported on that set and ALL its graph
neighbors. Formula C uses the full residual, not a residual projected onto
the trial support. For a positive interval [Il,Iu], inversion gives the
deterministic output [rho/(R_a*Iu),rho/(R_a*Il)]. Capacity uses Z_even
instead of R_a. Intersecting valid intervals with [mu,(1+rho)/g0] is valid.

Choose y in span{u,Hu,...,H^(k-1)u}; exact Galerkin makes r orthogonal to
this space. This is the classical CG/Krylov operation, not a new linear
solver; [Hestenes--Stiefel (1952)](https://math.nist.gov/mcsd/Reports/2002/hestenes-steifel-52.pdf)
is the primary ordinary antecedent. The gap-based upper bound in C is also
an elementary ordinary spectral residual bound.

## 5. Integer scaling and implemented formulas

Write each reduced theta_i=n_i/d_i. Define

    W=product_i d_i, N=product_i n_i, rho=N/W,
    W_x=W*w(x)=product_i [n_i if eta_i=1 else d_i],
    U=W*u: U(a)=N, U(b)=-W.

All W_x are positive integers. Let D be the least common multiple of every
actual local rate denominator (both outside-bit contexts and all four pair
states), so A=D*H has integer entries. Generate V_0=U, V_j=A*V_(j-1).

Sparse application of A must be BACKWARD. For a source coordinate x with
value v, add D*exit(x)*v to coordinate x. For each neighbor y, add
-D*q(y,x)*v to coordinate y. The latter is the REVERSE edge rate. Using
q(x,y) there would instead multiply the forward generator and is wrong.
The code constructs both rates and checks W_x*q(x,y)=W_y*q(y,x) exactly.
All full generated powers have sum_x W_x*V_j(x)=0.

Let G_ij=sum_x W_x*V_i(x)*V_j(x). For i,j=0,...,k-1 solve

    S_ij=G_(i,j+1), t_i=G_(i,0), S*alpha=t.

S is positive definite until the Krylov subspace has reached its invariant
cyclic space. At that last independent degree the exact residual is zero
and the implementation stops. The trial is

    y=(D/W)*sum_(j=0)^(k-1) alpha_j V_j.

Set beta=(1,-alpha_0,...,-alpha_(k-1)). Galerkin gives

    L=D*(alpha^T*t)/(W^2*N),
    <r,r>_w/rho=(beta^T*G*beta)/(W^2*N).

Therefore C is an exact rational enclosure. In particular there is NO
extra D in the residual-error term. The implementation uses exact integer
moments and an exact rational k by k FLINT solve, then verifies S*alpha=t.
No matrix conditioning is hidden as floating-point accuracy. Decimal
numbers in reports are display approximations; saved hexadecimal rational
numerators/denominators are the certificate endpoints.

## 6. State, bit and conditioning costs

Define spin coordinates by prefix parity of the occupation bits. Every
adjacent pair toggle changes exactly one spin coordinate. Thus V_j is
supported within Hamming distance j of a or b, with at most

    S_j <= min(2^(M-1), 2*sum_(h=0)^j binomial(M-1,h))

states. Dictionary unions count overlaps once; no disjointness assumption
enters the algorithm. At M24, a and b have spin distance12, so radius3
balls are disjoint. Their sizes are 2*2048=4096. The degree3 trial has at
most 554 coordinates and its FULL residual has 4096. There are 554 cached
source transition rows and 554*23=12742 local edge evaluations.

Let B be the input rational bit budget. log W, log N and log D are bounded
by sums of input/local-rate denominator bit lengths, O(M*B) for bounded-size
local formulas. The row absolute sum of A is at most 2*D*Rstar. Hence

    ||V_j||_infinity <= W*(2*D*Rstar)^j.

Gram bit lengths are bounded by log S_k +3 log W
+2k log(2*D*Rstar), up to fixed sign/rounding constants. Exact k by k
determinant/minor bounds give rational-solve bit lengths polynomial in k
and this Gram bit bound. Generation uses O(M*sum_(j<k) S_j) local terms;
the simple implementation uses at most O(k^2*S_k) integer Gram terms,
plus a k by k rational solve. It stores O(sum_(j<=k) S_j) power entries
and O(M*S_(k-1)) cached transitions. Generating rational source tables,
LCMs, weights, powers, Gram moments, the solve and all final bounds is
inside the reported certificate-function timer.

For the executed three cases, D has 171/175/172 bits, W has 128 bits,
the largest Gram entry has 1384/1410/1393 bits and the largest coefficient
denominator has 1698/1698/1697 bits. This explicitly pays source precision
and exact cancellation; it does not pay 1/rho arithmetic operations.

There is NO assertion that k=3 works uniformly. On the executed small
models the degree 3 widths remain between about 2.8% and 34.8%. If k must
grow, S_k can approach the full exponential state space. The global gap
may be tiny, and uncertain weights/rates may dominate any arithmetic bound.
The supplied input class, posterior certificate and measured finite example
are the supported scope, not an all-model polynomial deterministic solver.

## 7. Equally informed ordinary alternatives

An ordinary sparse Galerkin/CG solver receives the SAME full local rate law,
weights, gap, Krylov trial construction and preprocessing resources. It can
produce exactly this certificate. There is no claimed performance advantage
over it. The prior Gaussian implementation computed a reference integral
and transferred 5%/50% envelopes; direct Galerkin now resolves each specified
actual model. This changes the completed output, not the status of CG.

There is also a generic ordinary finite-horizon Monte Carlo route to I
under these promises, so rare p alone is not an inverse-p barrier. Since
0<=f(t)<=(1+rho)*exp(-g0*t), take T with tail<=(eta*mu). For uniform
t in[0,T], simulate independent trajectories from a and b, and use

    Y=T*[rho*1{Xa_t=a}+1{Xb_t=b}-2rho*1{Xb_t=a}].

Its expectation is integral_0^T f, and its range length is at most
(1+3rho)*T<=4T. Hoeffding gives additive eta*mu error with failure zeta
for N>=(1+3rho)^2*T^2*log(2/zeta)/(2*eta^2*mu^2) samples. Add the
nonnegative tail, intersect with I>=mu and invert. eta proportional to
the requested relative tolerance suffices. Uniformization costs expected
O(Rstar*T) events per trajectory. With inverse gap and rates polynomially
bounded, this event/sample cost is polynomial without 1/p. Honest exact-law
simulation/randomness and source promises are premises; a complete exact
finite-bit simulator proof is not claimed. No wasteful huge simulation was
executed merely to instantiate this ordinary bound. Its statistical coverage
is distinct from the deterministic rational certificate above.

## 8. Source and review boundaries

The input is the exact rational source fixture, not acquired physical data.
The accepted SOURCE_ACQUISITION.md in the parent directory charges local
rate-context exposure, Gibbs-ratio estimation, mixing, coverage and confidence
inside a promised finite-local reversible Markov class. A fugacity log-box
eta_theta and rate log-box eta_rate can widen p by
exp(plus/minus[M*eta_theta+2*eta_rate]); direct numerical accuracy cannot
remove that source uncertainty. Finite observations do not prove absence
of hidden jumps, exact reversibility or a finite Markov memory. If only a 5%
conductance envelope is acquired, it remains a 5% envelope; narrowing the
specified exact actual model is not a data-acquisition shortcut.

check_direct.py independently constructs small full generators from Gibbs
weight ratios rather than the candidate rate table, solves both killed and
full Poisson equations, checks full sparse/dense backward orientation,
recomputes residual norms/energies and tests arbitrary constant shifts.
Nine M4/M6 models and 27 degree intervals pass. These checks do not prove
the all-size theorem, which is supplied above.

Root separately constructed every full backward residual from candidate
trial proposals on all three M24 cases at degrees 1,2,3, using separate
Fraction rates and weights. All nine raw bounds matched exactly. This
reconstruction does not enumerate the large chain or assume Gaussianity.
The final whole-proof acceptance status is recorded separately after root
finishes reviewing these artifacts; it is never inferred just from hashes.

The operation is mathematically/computationally achieved at this supplied
model scope. Physical source validity, historical originality and practical
advantage remain unestablished. The civilisation-level mission remains
100/100 NOT_ACHIEVED.
