# A finite Gaussian reservoir with paid preparation and precision

29 October 2026. Working mathematical construction; no physical preparation,
quantum state, Hamiltonian case or trajectory is executed. This provides a
bounded-degree GRAPH-local apparatus. Uniform bounded-density embedding
in physical3D is NOT established. The source coupling is generally constant-
body after the Pauli-prefix pullback. These boundaries are part of the result.

## 1. One fixed passive spectrum for every low temperature

One can avoid even temperature-dependent spectral hardware. Fix once

    dmu(nu)=fminus(-nu)^2 dnu/(2pi), 1/2<=nu<=3/2.         (1)

An oscillator continuum with this coupling measure, positive one-particle
Hamiltonian nu, and inverse temperature b has square-root emission factor

    hphys_b(-nu)=fminus(-nu)/sqrt(1-exp(-b nu)),
    hphys_b(nu)=exp(-b nu/2)hphys_b(-nu).                 (2)

This is a single fixed Hamiltonian bath, not a bath spectrum computed from
the many-body Hamiltonian. Its Bose factor changes with temperature.
For b>=1, write c_b=(1-exp(-b nu))^-1/2. Its convergent positive series
has coefficients binom(2l,l)/4^l<=1. Since exp(-b nu)<=exp(-1/2)<=2/3,

    |d_nu^k c_b|<=k! 3^(k+1)b^k,
    |d_nu^k(c_b-1)|<=k! 3^(k+1)b^k exp(-b/2).           (3)

For k=0 the second inequality follows from r/(1-r); for k>=1 use
sum_l l^k r^l<=k! r/(1-r)^(k+1). The first bound includes the constant1.

Thus the negative filter differs from the exact plateau by a spatial-
moment error polynomial(b)exp(-b/2). Negative jumps STILL annihilate the
exact vacuum. The CP-martingale relative bound becomes
b_rel<=C lambda+C polynomial(b)exp(-b/2), not n times that error. At one
smaller fixed lambda and one larger fixed T0 it is <=1/4 for every b>=T0.
All all-cold parent/coercivity proofs consequently hold for (2). The heated
parent perturbation retains polynomial(b)exp(-b/4) tails.

Here is the literal scalar compiler. Let F_j be the frozen integer bounds
for the j-th derivative of the flat filter, 0<=j<=4. Put

    T_k=sum_(a=0)^k binom(k,a)(k-a)! 3^(k-a+1),
    B_k=sum_(j=0)^k binom(k,j)F_j T_(k-j),
    C_B=64[1+max_(k<=4) B_k].                            (3a)

Leibniz and(3) show that BOTH hphys_b and its symmetrized filter q_b have
k-th derivative bounded by B_k(1+b)^k on each of their two bands. The
extra exponential factor has exponent coefficient at most1, overpaid in
T_k. Four integrations by parts, with flat vanishing at band endpoints,
give |g(u)|<=A_B min(1,|u|^-4), where A_B=C_B(1+ceil(b))^4. Thus each of
integral|g|, integral|u g| and integral u^2|g| is <=4A_B. The same bounds
hold for q_b. Replace A in MICROSCOPIC_COMPOSITION by A_B. No old numerical
gate or C_* is silently reused for the Bose-normalized filter. The scalar
recurrence is executed in compile_resources.py; native smallness gates
remain UNEVALUATED.

## 2. A bounded-degree chain, with finite-horizon mode count

Use the ordinary orthogonal-polynomial chain mapping for (1). Its Jacobi
matrix J is real tridiagonal, satisfies 1/2 I<=J<=3/2 I, and has bounded
entries. Each system seed couples only to the FIRST mode of its independent
chain, with coupling alpha sqrt(mu([1/2,3/2])). This is a nearest-neighbour,
number-conserving passive oscillator chain, with a positive energy gap.
The map and this coefficient specification are strong established tools,
not an invention here.

For the actual error use [Woods--Cramer--Plenio, PRL115,130401(2015),
Theorem1 and AppendixA1d](https://arxiv.org/pdf/1504.01531). It treats
arbitrary system Hamiltonians, is uniform for every system observable of
norm<=1, and adds truncation errors for independent baths. Therefore
duality gives the FULL reduced system trace-norm error, not just a selected
observable. In its particle mapping X=P=J and c=3/2. At b>=1 the initial
thermal position/momentum covariance norm is <=4, uniformly in volume.
The system coupling norm is <=2alpha. The theorem implies the conservative
per-chain estimate

    error_R^2 <=64(1+tau) exp(3tau/2)
                           (3tau/2)^(R+1)/(R+1)!.       (4)

Here tau is the required PHYSICAL time U/alpha^2. Taking

    R+1>=ceil(32(1+tau))
                     +4ceil(log2[128m(1+tau)/epsilon_B]) (5)

makes the summed m-chain error <=epsilon_B/8, after harmless rounding
up of endpoints. Indeed k!>=(k/3)^k and k>=12(3tau/2) make the factorial
factor at most4^-k; its exp(3tau/2) is absorbed while retaining2^-k.
Thus R is polynomial in preparation time plus logarithmic precision, with
no smallest many-body or bath Bohr-gap requirement.

The infinite reservoir in the microscopic theorem is only a proof model
at this step. The final apparatus below is finite and uses a finite-chain
initial state that is actually specified independently.

## 3. Finite-chain thermal state is not an assumed infinite-bath marginal

Let J_M be the principal M-mode Jacobi matrix. Its own Gibbs state has
gauge-invariant Gaussian occupation covariance

    C_M=(exp(b J_M)-I)^-1.                               (6)

This is generally different from restricting the infinite-bath state to M
modes. That difference has to be charged. On the fixed interval[1/2,3/2],
n_b(z)=(exp(bz)-1)^-1 is analytic on the Bernstein ellipse of parameter2:
its real part stays >=3/8 and |n_b(z)|<=4 for all b>=1. Its degree-k
Chebyshev approximation therefore has uniform error <=16*2^-k.

Polynomials of degree k<M-R agree on the first R modes for J and J_M,
because the matrix is tridiagonal. Consequently their first-R occupation
covariances differ by

    ||C_infty,R-C_M,R||_1<=32R*2^-(M-R-1).               (7)

Every gauge-invariant Gaussian state of occupation covariance C>=0 has a
POSITIVE mixture of product coherent states |z>, with complex Gaussian
amplitude covariance C. Couple two such amplitude laws by the same standard
Gaussian and use the Powers--Stormer square-root inequality. Coherent-state
trace distance then gives

    ||rho(C)-rho(C')||_1<=2 sqrt(||C-C'||_1).             (8)

It has no inverse occupation or inverse minimum-eigenvalue factor; the
zero-temperature limit is benign. Choose M>=R+1 plus a sufficiently large
multiple of log2[m(R+1)/epsilon_B].

Compare both the infinite bath and the M-mode bath to their common R-mode
truncation. Equation(4) applies to EACH, with covariance norm<=4, while
(7),(8) bound the initial R-mode state mismatch. Triangle inequality then
pays a finite-chain replacement error <=epsilon_B/2 with M=O(tau+log(m/
epsilon_B)). A finite-chain Gibbs state is actually used; an inaccessible
infinite thermal marginal is not supplied as a hidden input.

## 4. Acquiring the finite Gaussian initial state without system quantum gates

The one-particle covariance (6) is a classically computable M by M matrix.
The bath measure (1) is fixed and equals a positive constant on a known
subinterval. Its moments through degree2M are computable by scalar Gevrey
quadrature to any requested bits. For a moment Gram matrix of size d,

    lambda_min(G_d)>=1/[32 d^3 24^(2(d-1))].             (8a)

Indeed mu has density>=1/8 on I=[3/4,5/4]. Expand p(1+y/4) in normalized
Legendre polynomials on[-1,1]. The recurrence bounds the coefficient l1
norm of P_j(y) by3^j. Substitution y=4x-4 multiplies it by at most8^j,
and normalization by at most j+1. Cauchy--Schwarz bounds the monomial
coefficient norm by d^(3/2)24^(d-1) times the Legendre l2 norm. Integrating
with dmu>=dy/32 proves(8a). Thus Stieltjes/Gram orthogonalization needs
polynomially many PRECISION BITS, not an exact-polynomial oracle. Interval
elimination/Cholesky with this positive pivot floor terminates when input
moment error is below a polynomial in that floor times requested accuracy.
The known fixed Gevrey filter admits scalar quadrature at polynomial cost
in requested bits. Final physical Jacobi coefficients are bounded and may
be rounded to Section6's inverse-polynomial tolerance. No coefficient
table has been generated or claimed physically calibrated in this packet.

Analytic matrix-function approximation or ordinary high-precision matrix
arithmetic computes C_M and its positive square root in polynomial work.
Its spectrum stays bounded at b>=1. To acquire the bath state:

1. Prepare local oscillator vacua, with their total initial-state error
   explicitly allocated. These are one-mode product ground resources,
   not interacting clock Gibbs states.
2. Draw a CLASSICAL complex Gaussian vector z of covariance C_M. Finite
   random-bit quantile approximations and Gaussian tail clipping give an
   arbitrarily small mean-square amplitude error with polynomial bits/work.
   Equation(8)'s coherent coupling proof pays the output state error.
3. Apply local CLASSICAL linear force pulses that displace each vacuum by
   z_j. These are specified finite-time analog controls, with finite peak,
   bandwidth and precision; ideal universal coherent gates are not assumed.

With the passive chain on, its classical amplitude satisfies
zdot=-iJ_M z-iF(t). For duration1 use w(s)=6s(1-s), 0<=s<=1, and

    F(s)=i w(s) exp(-iJ_M s)exp(iJ_M)z.

Its integral produces exactly z from vacuum. It vanishes at both ends;
peak and every fixed slew/derivative bound are polynomial. The carrier
frequencies lie in the fixed one-particle band. The FINITELY SWITCHED pulse
is not claimed exactly band-limited. Smooth rounding/time discretization
at inverse-polynomial accuracy pays finite bandwidth/precision. Only the
BATH matrix is compiled; no H_system-dependent evolution or universal
coherent quantum gate synthesis occurs.

For a literal common budget let B=mM, choose bath-state tolerance eta,
and radially clip the complex Gaussian at radius

    r_z=ceil[64(B+1)/eta].

Since C_M<=2I, E||z||^4<=8(B+1)^2; clipping changes the coherent mixture
in trace norm by at most2sqrt(8)(B+1)/r_z<eta/8. Coordinate quantization,
positive covariance approximation, and inverse-CDF random-bit generation
can each be assigned another eta/8. These are distributional finite-bit
algorithms, not claims about a seeded PRNG. For every retained draw the
whole drive has integrated coefficient l1 norm Lambda<=B r_z. Vacuum
errors are allocated independently and sum over the B modes.

These local vacua and calibrated classical harmonic controls are explicit
physical resource assumptions. Their hardware preparation/calibration has
NOT been performed. This construction does not assert a fully passive,
thermal-only initializer from an unspecified laboratory environment.

## 5. Polynomial occupation capacity; no infinite free local memory

The finite passive baths have B=mM modes and conserve total boson number
N_B under H_B. Only the m bounded-system linear couplings change it by1.
For R_B=N_B+B+1, let M2(t)=expectation R_B^2. Sector Cauchy--Schwarz gives

    |d M2/dt|<=16alpha m M2^(3/4),
    M2(t)^(1/4)<=M2(0)^(1/4)+4alpha m t.                 (9)

For the thermal Gaussian initial state M2(0)<=22(B+1)^2. To pay ACTUAL
finite-level state preparation, include the classical drives. Replacing
alpha m in the derivative bound by the instantaneous sum of absolute
linear-force coefficients gives the same inequality during the driven
stage. It starts in product vacuum, not a supplied finite interacting
Gibbs state. With alpha<=1 and Lambda<=B r_z, the simple polynomial

    M2bar=[4(B+1+B r_z+m tau)]^4                         (10)

bounds M2 throughout BOTH drive and cooling. It also bounds locally
occupation-truncated dynamics, since truncating an annihilator cannot
increase its sector norm. To justify(9), resolve
total-number sectors: a coupling matrix element between l and l-1 has
norm at most sqrt(l); the difference of R_B^2 is <=2R_B. The inequality
2sqrt(p_l p_(l-1))<=p_l+p_(l-1) bounds the derivative by a fixed multiple
of alpha m expectation R_B^(3/2), then Holder gives(9). No assumed
independence of the evolving system and bath is used.

First compare the WHOLE driven-and-cooling protocol to a GLOBAL total-number
cutoff K. Both start in vacuum. The passive bath has no matrix element
across this boundary; only linear coupling/drive does. On a truncated
evolving vector the escaping term is bounded by a fixed multiple of
(sum absolute linear coefficients)sqrt(K+1)sqrt(Pr[N_B=K]). Equation(10)
bounds the last probability by M2bar/(K+1)^2. Duhamel gives vector error
at most

    16(1+B r_z+alpha m tau)sqrt(M2bar)/sqrt(K+1).         (11)

There is no initial tail in this vacuum-start implementation; the extra1
also covers a terminal projection comparison if used. Choose

    K+1>=[1024(1+B r_z+m tau)sqrt(M2bar)/epsilon_B]^2.

It is polynomial. Trace distance is at most twice purified vector distance.
For a physical LOCAL-level truncation, use levels0,...,2K+1 at each mode.
Full and local-level-truncated dynamics agree on the common total-number
sector N_B<=K. Apply(11) to both using that common intermediate Hamiltonian;
triangle inequality pays the local truncation as well. This avoids a false
assumption that individual-mode hopping boundaries commute with total N_B.

Local oscillator capacity, total bath energy, number of modes, and the
classical drive resources are all polynomial in tau,m,1/epsilon_B. No
infinite local Hilbert space is being counted as a finite qudit for free.

## 6. Calibration, locality, and the exact surviving boundary

After finite level truncation the total Hamiltonian has O(n+mM) local
terms, bath-hopping norm O(K), and linear-end coupling norm O(sqrt(K)).
An absolute coefficient tolerance

    delta_coeff<=epsilon_cal/[4096(1+tau)(n+mM)(1+K)]     (12)

pays unitary channel error by Duhamel. Frequencies, weak alpha, classical
forces and switching ramps can be assigned inverse-polynomial precision
and bandwidth within this finite model. Classical computation may use
more internal bits to obtain the bounded Jacobi coefficients, but the
PHYSICAL coefficient tolerance in(12) is inverse-polynomial. No tiny
many-body Bohr separation is used as an apparatus setting.

The construction has bounded degree and finite interaction range in the
source-plus-bath-chain GRAPH; each source coupling has constant support
from its known prefix table. It does NOT establish uniform bounded-density
physical3D layout. For example attaching an independent long tail at every
site of a full3D grid produces radius-R balls of order R^4. That graph
cannot have uniformly bounded-length edges and bounded density in R3.
No such lower-growth obstruction is asserted for the particular recursive
code geometry without its own layout analysis.

The result being constructed is finite-time conditional Gibbs preparation
in an explicit microscopic model, with polynomial apparatus/time/precision
and declared local Gaussian-control assumptions. It is not an autonomous
constant-overhead physical3D controller, a two-body-only apparatus, an
actually calibrated bath, or a long-storage theorem. The global linear-time
microscopic approximation cannot by itself pay stretched-exponential
storage at fixed bath coupling; a local MULTI-TIME fault budget remains
unacquired here and is not inferred from the preparation estimate.
