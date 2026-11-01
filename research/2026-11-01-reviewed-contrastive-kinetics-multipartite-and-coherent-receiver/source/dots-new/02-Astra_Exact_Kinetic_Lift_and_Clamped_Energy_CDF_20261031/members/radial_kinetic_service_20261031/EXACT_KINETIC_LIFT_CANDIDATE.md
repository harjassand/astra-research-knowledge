# Exact kinetic projection with arbitrary tangent dynamics

Status: construction candidate, not independently accepted. This is a mathematical
model/program consumer. It does not establish that a physical system has the
required mobility or actuators. All earlier accepted conductance sources are unchanged.

## 1. Actual task and model

The target missing from a capacity certificate is an observable **path law**, not
another equilibrium normalizer. Let U on R^m be a C^3 homogeneous polynomial of
even degree p>=2, strictly positive off 0, with acquired U(z)>=a||z||^p, a>0.
Put alpha=m/p>=1, v(y)=1+kappa(1-y^2)^2, beta,kappa>0, F(y,z)=v(y)U(z).
The actual state domain is R x (R^m minus {0}); an initial state has U(z0)>0.

Specify a reversible divergence-form dynamics with longitudinal mobility 1,
zero cross mobility, and transverse mobility

    M(z)=z z^T/(p^2 U(z)) + T(z),
    T(z)=sum_a c_a X_a(z) X_a(z)^T, c_a>=0, X_a·grad U=0.

The X_a are finite C^2 vector fields locally bounded with their derivatives away
from 0. They may be polynomial with arbitrarily large finite coefficients. There
is NO assumption of rapid angular mixing, a conditional Poincare inequality,
known angular partition, or known angular relaxation rate. T may be zero.

The declared actual generator is

    L f = beta^-1 f_yy - v'(y)U f_y
          + beta^-1 exp(beta F) div_z(exp(-beta F) M grad_z f).

The divergence drift is essential. A simulator using just -M grad F and matched
noise, but omitting beta^-1 div M, is a DIFFERENT model and does not qualify.
This construction changes the earlier constant-SPD/Euclidean dynamics. It is not
a reduction of that earlier model merely because the potential is the same.

## 2. Pointwise closure, including tangent kinetics

Euler's identities give z·grad U=pU and z^T Hess(U)z=p(p-1)U. Directly,

    div[z z^T/(p^2 U)] = (m+1-p)z/(p^2 U),
    M_rad grad F = v z/p,
    grad U^T M_rad grad U = U.

Consequently the radial part has

    L_rad U=alpha/beta-vU,  Gamma_rad(U,U)=U/beta.

For ANY smooth scalar g, T grad[g(U)]=g'(U)T grad U=0 IDENTICALLY,
so the entire divergence-form tangent generator annihilates g(U). This is not
an equilibrium average, and does not require div X_a=0. Independence of the
longitudinal and transverse noises gives zero y/U quadratic covariation.
Thus every test f(y,U) has the exact generator

    G f = beta^-1 f_yy - v'(y)u f_y
          + (alpha/beta-v(y)u) f_u + u/beta f_uu.             (1)

An explicit full-state noise representation has one radial column
sqrt(2/(beta p^2 U))z and tangent columns sqrt(2 c_a/beta)X_a. Its drift is

    b_z=z[(m+1-p)/(beta p^2 U)-v/p] + beta^-1 div T.

Ito's formula therefore gives, up to the lifetime,

    dY=-v'(Y)u dt+sqrt(2/beta)dW,
    du=(alpha/beta-v(Y)u)dt+sqrt(2u/beta)dB,                 (2)

where B is exactly the radial Brownian motion and is independent of W. Tangent
noise has no direct or Ito-residual energy increment. Local pathwise uniqueness
on u>0 makes (2) a strong Markov diffusion and proves equality of the FULL
projected path law for every deterministic initial (y0,z0), or any initial law
with the same pushforward (y0,U(z0)). No Gibbs initialization is needed. Hidden
angular histories may be arbitrarily nonmixing and still do not enter this law.

## 3. The global/origin join, not just formal Ito algebra

First stop in compact sets with u bounded away from zero. Define c=2kappa+1 and
W=1+y^2+cu. Since yv'(y)=4kappa y^2(y^2-1)>=-kappa and v>=1,

    G W=(2+c alpha)/beta - [2yv'+cv]u <=(2+c alpha)/beta-u.

Stopping/optional expectation bounds escape to infinity, uniformly in the
unknown tangent coefficients. Coercivity makes bounded u imply bounded z.
Thus the full state cannot explode to infinity, even if its tangent polynomial
coefficients grow very fast. This is NOT a numerical stability or implementation
cost bound for those coefficients.

It remains to rule out finite-time u=0. Before a bounded-y stopping time let
A(t)=int_0^t v(Y_s)ds and Q=e^A u. Ito and a Brownian time change with
s(t)=int_0^t e^{A(r)}/beta dr give

    dQ=alpha ds+sqrt(2Q)dB_s.

Equivalently 2Q is a squared-Bessel process of dimension 2alpha>=2. Its origin
is inaccessible from Q0>0. One may verify the boundary classification directly
with the scale functions log Q (alpha=1) or Q^(1-alpha) (alpha>1), stopping first
between epsilon and a finite upper level and sending epsilon down to zero.
A(t),s(t) are finite before any finite bounded-y stopping time. The preceding
nonexplosion argument removes those stops. Hence u stays strictly positive on
every compact time interval and the full local SDE has an infinite lifetime.

For alpha<1 this argument fails: zero is attainable in the scalar process and
the singular full-state lift needs an additional origin/angle continuation.
The consumer returns UNKNOWN rather than choose that interface implicitly.

Homogeneous radial integration gives the normalized projected Gibbs density

    rho(y,u) proportional to u^(alpha-1) exp[-beta v(y)u], u>0.

Its normalization is finite because int v^-alpha dy has tails |y|^-4alpha and
alpha>=1. The full Gibbs law is also finite. Integration by parts gives symmetry
of the full generator; the conservative diffusion associated with this smooth
local divergence form preserves the finite Gibbs law. No ergodicity or mixing
rate follows when T is degenerate. Equation (1) has the same reversible density.

## 4. A completely acquired polynomial tangent implementation

The first raw consumer admits p in {2,4}, a complete exact rational polynomial
with STRICTLY POSITIVE coefficients on every listed monomial (unlisted terms
are zero), all exponents even, every monomial of degree p, and a positive pure z_i^p term
for every i. If d_min is the smallest pure coefficient then

    U >= d_min sum_i |z_i|^p
      >= d_min m^(1-p/2) ||z||^p.

All listed terms are read; dimensions, degrees, signs, uniqueness, coefficient
bits and total exponent entries are checked. A generic positive form outside
this sufficient grammar returns UNKNOWN. This is not a positivity oracle.

For the actual tangent program use X_ij=(partial_j U)e_i-(partial_i U)e_j
with one common rational weight c_t>=0 and all unordered coordinate pairs.
Mixed partial symmetry gives div X_ij=0 and X_ij·grad U=0 identically.
Writing g=grad U and H=Hess U,

    T=c_t (||g||^2 I-g g^T),
    div T=c_t[H g-(Delta U)g].                            (3)

If c_t>0, T has kernel span(g). Euler gives z·g=pU>0, so its sum with
z z^T/(p^2 U) is SPD at EVERY z!=0. Thus the full mobility need not be rank one,
and angle need not be frozen. No dimension-independent ellipticity is claimed.
A tangent noise square root is sqrt(c_t)||g||(I-g g^T/||g||^2): m normal draws
and a projection suffice after computing g, rather than expanding m(m-1)/2
independent columns. All actual derivatives, vector updates and stiffness are
paid if a full-state trajectory is requested. The observable-law consumer never
pretends to execute or learn those hidden trajectories.

## 5. First finite kinetic query: declared clamped macro protocols

The autonomous two-variable process (2) does NOT have the frozen-y CIR
propagator. A first concrete finite operation instead specifies an external
piecewise-constant clamp y=y_j for positive durations t_j. This is a DIFFERENT,
explicit controlled experiment/model. There is no claim of solving autonomous
barrier hitting times or of implementing the clamp on hardware.

On a segment v_j=v(y_j), energy has the ordinary CIR transition. Across a finite
protocol its law from deterministic u0>0 is exactly characterized by

    E_0=1, B_0=0,
    e_j=exp(-v_j t_j),
    E_j=e_j E_{j-1},
    B_j=e_j B_{j-1}+(1-e_j)/(beta v_j).

At the final time, for theta>=0,

    E[exp(-theta u_T)]
      =(1+B theta)^(-alpha) exp[-E u0 theta/(1+B theta)].   (4)

This follows either from the backward affine Riccati equation or the exact CIR
semigroup and composition. The mean is E u0+alpha B and the variance is
2 E B u0+alpha B^2. At an instantaneous clamp switch potential work is
[v_new-v_old]u; it is not free heat or a hidden acceleration of the original
system. The program records the actual protocol, durations and model interface.

For integer alpha and B>0, a completely ordinary finite scalar CDF engine uses

    u_T/B | N ~ Gamma(alpha+N, rate 1),
    N ~ Poisson(lambda), lambda=E u0/B.

At threshold q>0, x=q/B,

    P(u_T<=q)=sum_n Pois_lambda(n)
      [1-exp(-x)sum_{k=0}^{alpha+n-1} x^k/k!].             (5)

This is the noncentral chi-square/Gamma machinery already supplied by ordinary
CIR methods. Its construction and numerical cost are not claimed new. The
scientific content of the lift is the exact independence of this law from all
admitted angular energies/tangent rates once the model and initial energy have
actually been checked. A general reduced 2D first-passage solver, rare-event
relative-error theorem, empirical physical acquisition and feedback-control
error tolerance remain OPEN; none is supplied by (4) or (5).

## 6. Strong retained alternatives and scope

Bussi, Donadio and Parrinello, JCP126 (2007), arXiv:0803.4060, Eqs.(4)-(7),
already construct scalar energy diffusions preserving the Gamma law by global
rescaling; Appendix A gives an exact frozen-parameter propagator by ordinary OU
coordinates. Their method assumes angular exploration for full canonical
sampling. The primary author's algorithm page warns of a Gamma-scale typo in
the appendix. We use the explicitly derived noncentral-Gamma law, not that typo.
https://arxiv.org/pdf/0803.4060
https://sites.google.com/site/giovannibussi/Research/algorithms

Lelièvre, Santet and Stoltz, arXiv:2410.00525v4, Proposition2 and Remark1 already
show tangential-diffusion freedom in a projected SDE; its added Remark2
(The multidimensional case) designs target projected covariance. This is v4,
not v3, whose differently numbered Remark2 only simplifies a divergence. Their generic drift still requires conditional averaging.
Here the Euler field makes both coefficients pointwise closed. This is a
special exact assembly of ordinary projection/metric-design machinery, not a
new general Markov-function theorem or independent algorithmic separation.
https://arxiv.org/html/2410.00525v4

Legoll and Lelièvre, arXiv:0906.4865, Section1.2 explains the generic non-Markov
closure problem and later obtains approximations under quantitative conditional
mixing assumptions. Such assumptions are not needed when the actual generator
closes pointwise, but our required actual mobility is a substantive restriction.
https://arxiv.org/pdf/0906.4865

For Gaussian U=||z||^2/2 with ordinary constant isotropic mobility gamma I,
energy already obeys du=gamma(m/beta-2vu)dt+2sqrt(gamma u/beta)dB; gamma=1/2
matches (2). The comparator gets the SAME raw potential, coefficients, protocol
and numerical engine. We claim no improvement over that ordinary Gaussian
case, and no unexplained physical advantage from declaring a different tensor.
