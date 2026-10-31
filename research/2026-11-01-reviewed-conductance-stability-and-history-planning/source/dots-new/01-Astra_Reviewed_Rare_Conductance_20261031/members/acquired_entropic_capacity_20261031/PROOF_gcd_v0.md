# Acquired entropic conductance: finite-rate variational certificate

Status: author proof, not yet independently reviewed. This is a restricted
mathematical diffusion construction, not a physical implementation, a general
rare-event solver, or a historical novelty claim.

## Actual task and access

Input is a finite list of exact rational coefficients of a polynomial `F(x)`
in the physical Euclidean coordinates, inverse temperature beta > 0, and a
requested numerical quadrature width. No reaction coordinate, eigenbasis,
committor, sampler, mixing time, or planner is supplied. The compiler either
acquires and verifies the class below, or returns UNKNOWN. On success it
returns a unit vector ell, the two explicitly identified basins

    A = {ell.x <= -b}, B = {ell.x >= b}, b=1/2,

and a two-sided interval for the normalized equilibrium conductance
`k_AB = cap_mu(A,B)/mu(A)`. This is not the first-hit CDF from a specified
state, nor is `1/k_AB` asserted to be a mean waiting time for arbitrary
initial data. The executable returns this capacity/mass ratio, not a separate
normalized-capacity number; the latter would additionally require Zbar.

The process is the ordinary overdamped diffusion

    dX = -grad F(X) dt + sqrt(2/beta) dW.

The acquired class, in orthogonal coordinates x=ell*y+z, z perpendicular ell,
is

    F(y,z) = 1/2 z^T [I + v(y) H] z,
    v(y) = (1-y^2)^2,

where H is strictly positive on ell-perp and H ell=0. Write m=n-1 >= 2.
The eigenvalues kappa_i>0 may all differ. They are notation in the proof,
not supplied inputs or a prerequisite to the determinant implementation.

Every y has minimum fiber energy zero: `min_z F(y,z)=0`. Thus minimizing
the fibers erases the entire barrier. The conditional Gaussian volume does
not: the unnormalized marginal is

    q(y)=det(I+v(y)H)^(-1/2), Zbar=integral_R q(y)dy.

For fixed positive kappa bounds, q(0) is exponentially small in m while
q(1)=q(-1)=1. This supplies a genuinely entropic test, not a double well
already encoded in a one-dimensional energy.

## 1. Ordinary conditional-transport capacity sandwich

Consider any smooth positive probability density `mu(dy,dz)=p(y)rho_y(z)dydz`
with isotropic physical Dirichlet form

    E(h)=beta^-1 integral (h_y^2+|grad_z h|^2) dmu.

Suppose a conditional transport w_y(z) satisfies

    partial_y rho_y + div_z(rho_y w_y) = 0,
    K(y)=integral |w_y|^2 rho_y dz < infinity.

Integration by parts gives the exact identity

    d/dy E_rho[h] = E_rho[h_y+w_y.grad_z h].

Cauchy--Schwarz in the conditional Hilbert space implies

    |d E_rho[h]/dy|^2 <= (1+K(y)) E_rho[h_y^2+|grad_z h|^2].   (1)

For full-fiber boundary sets y<=a and y>=b, conditional averaging preserves
the boundary values. Infimize (1) over all admissible h, and use the
one-dimensional Dirichlet principle with conductivity p/(1+K):

  1/[beta integral_a^b (1+K)/p] <= cap_mu(A,B)
                                   <= 1/[beta integral_a^b 1/p].       (2)

The upper bound follows by restricting to h(y,z)=u(y). The scalar minimum
formula follows directly from Cauchy--Schwarz and is attained by u'
proportional to the reciprocal conductivity. Smooth truncations/density
extend the identities to the Dirichlet-form domain; Gaussian tails justify
the fiber integration by parts in the present class.

Alternatively the lower bound is exactly an ordinary Thomson construction:
the unit current `(rho_y, rho_y w_y)` is divergence-free in the transition
slab, and its resistance is beta times integral `(1+K)/p`. Consequently
neither the variational principles nor conditional-transport geometry are
claimed as inventions. The work is acquiring and verifying a usable
current rather than assuming a reduced kinetic law.

For a general Gaussian N(m(y),C(y)), one can acquire
`w=m'+S(z-m)` by solving `SC+CS=C'` for symmetric S. Then
`K=|m'|^2+Tr(S C S)`. This is the familiar Gaussian Wasserstein metric.
No optimality assertion about this broader construction is needed below.

## 2. Acquired current for the polynomial family

Here C=beta^-1(I+vH)^-1 on ell-perp. Since the matrices commute,

    w_y(z) = -v'(y)/2 (I+vH)^-1 H z,
    K(y) = v'(y)^2/(4 beta) Tr[H^2 (I+vH)^-3]
         = 4 y^2 v(y)/beta sum_i kappa_i^2/(1+kappa_i v(y))^3.          (3)

The covariance identity verifies the continuity equation exactly. All
inverses are of positive matrices. The actual projected process y_t is NOT
Markov in general: applying the full generator to u(y) gives

    beta^-1 u'' - v'(y)/2 (z^T H z) u',

which depends on z. Thus (2) is a finite-rate guarantee for the full
diffusion, not a fast-equilibration replacement of its generator.

Define

    R0=integral_-b^b 1/q, R1=integral_-b^b (1+K)/q,
    MA=integral_b^infinity q.

Symmetry gives mu(A)=MA/Zbar. Equation (2) becomes the normalization-free
and directly evaluable guarantee

    1/(beta MA R1) <= k_AB <= 1/(beta MA R0).                         (4)

## 3. The hard step: dimension-independent finite-rate loss

Set b in (0,1), vmin=(1-b^2)^2, w=1/q, and

    c = sup_{i, 0<=y<=b} kappa_i/(1+kappa_i v(y))^2
      <= 1/(4 vmin).

The last inequality follows from t/(1+t)^2<=1/4. Let
`S1=sum kappa_i/(1+kappa_i v)`. On 0<=y<=b,

    -w' = 2y(1-y^2) S1 w,
    K w <= (2c/beta) y(1-y^2) (-w').

Integrating by parts, retaining the sign of the boundary term, gives

    integral_0^b K w
    <= (2c/beta) [-b(1-b^2)w(b)+integral_0^b (1-3y^2)w]
    <= (2c/beta) integral_0^b w.

Therefore, for ALL m, all positive heterogeneous kappa_i, and all beta>0,

    R0 <= R1 <= [1+1/(2 beta (1-b^2)^2)] R0.

At b=1/2,

    k_free/(1+8/(9 beta)) <= k_AB <= k_free,
    k_free=1/(beta MA R0).                                         (5)

At beta=1 this is a factor 17/9 certificate, independent of dimension,
stiffness heterogeneity, barrier height, or an equilibration limit. Direct
integration of (3) can sharpen it but is not required by the main backend.
The exponentially small rate is bracketed multiplicatively, not by a
useless fixed additive error. No path crossing is sampled.

## 4. Normalization, nonexplosion, and the boundary at infinity

For |y|>=T>1, q(y)<=det_+(H)^(-1/2)(y^2-1)^(-m). Hence

    integral_T^infinity q <= det_+(H)^(-1/2)
       (1-1/T^2)^(-m) T^(1-2m)/(2m-1).                            (6)

So Zbar is finite for m>=1 (the acquisition parser below requires m>=2).
No reflecting wall or uncharged truncation is used. In coordinates y,z,

    x.grad F = sum_i [1+kappa_i(3y^4-4y^2+1)] z_i^2
              >= -C |x|^2,

because `min_{t>=0}(3t^2-4t+1)=-1/3`. The generator applied to 1+|x|^2
has a linear upper bound, giving nonexplosion by the usual stopped
Lyapunov argument. The integrable smooth Gibbs density is invariant for
the resulting conservative reversible diffusion; uniform ellipticity
and irreducibility remove competing invariant components. Capacity is
the variational object defined above, so no asymptotic metastability
theorem is needed to compute it.

## 5. Exact acquisition, not a supplied basis

The highest homogeneous part is

    F6=1/2 (ell.x)^4 x^T H x.

Since rank(H)=m>=2, the quadratic factor is square-free over Q. The gcd of
F6 and all its first derivatives is a scalar multiple of `(ell.x)^3`.
Its square-free part yields the unique repeated linear factor ell.x.
Normalize the coefficient vector; the prototype accepts rational unit
normalization and otherwise returns UNKNOWN rather than silently replacing
the physical metric. The mathematical generalization can use exact
algebraic arithmetic, but it has not been implemented here.

Recover H from `2F6/(ell.x)^4`; set P=I-ell ell^T. Check the ENTIRE input
identity `2F=x^TPx+(1-(ell.x)^2)^2 x^THx`, symmetry, `H ell=0`, and strict
positivity on ell-perp by exact LDL on `H+ell ell^T`. No leading-term match
alone is admitted. A coordinate-aligned sparse case is recognized directly
from the common highest-degree monomial, but passes the same identity.
Missing support, extra terms, wrong metric, and indefinite fibers reject.

`D(v)=det(I+vH)` is then acquired by exact characteristic-polynomial
arithmetic; it has degree m and positive coefficients. No eigenvectors are
needed for quadrature. The executed generic backend additionally requires
that its characteristic polynomial factor into rational linear factors;
it checks that factorization exactly and otherwise returns UNKNOWN. A
direct determinant-polynomial backend could remove that restriction but
is not delivered. Sparse diagonal data admit an O(m) product route.
Dense rotations are not free: full raw coefficient acquisition and the
polynomial gcd, coefficient verification, rational matrix arithmetic and
bit growth are charged in COSTS_AND_COMPARISONS.md.

## 6. Exponential obstruction captured, not ignored

If kappa_-<=kappa_i<=kappa_+ with fixed positive endpoints, then
`log(1/q(0))=1/2 sum log(1+kappa_i)=Theta(m)`. A fixed-width interval around
y=0 with width O(m^-1/2) contributes a fixed fraction of
`q(0)^-1/sqrt(m)` to R0. An O(m^-1/2) interval around y=1 contributes
Theta(m^-1/2) to MA; tails and the rest are at most polynomially larger.
Elementary Laplace bounds, or the executed interval integrals, therefore
give `log k_AB = -1/2 sum log(1+kappa_i)+O(log m)` at fixed beta.
Equation (5) fixes the full-rate/free-energy-rate uncertainty at O(1),
not O(m). Fiber minimum energy has no information about this exponent.

The result does NOT address arbitrary nonlinear conditional distributions,
unknown/noisy coefficients, generic reaction-coordinate acquisition,
nonreversible dynamics, underdamped motion, arbitrary basin shapes, or
finite-deadline transition probabilities. Those are distinct unresolved
boundaries, not corollaries of this construction.
