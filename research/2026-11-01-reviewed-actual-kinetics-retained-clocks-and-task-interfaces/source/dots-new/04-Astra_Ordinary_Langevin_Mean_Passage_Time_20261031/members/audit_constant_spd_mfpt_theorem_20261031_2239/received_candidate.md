# Ordinary constant-mobility mean passage time without angular relaxation

Status: construction candidate; not yet independently received. Earlier accepted
and frozen sources remain unchanged. This changes the actual model from the
engineered radial lift to ordinary reversible constant-mobility Langevin dynamics.
It does NOT transfer the lift's projected Markov law or fixed-ray initialization.

## 1. Actual question, model and information

Let U:R^m -> R be a coercive homogeneous polynomial of even degree p>=2,
U(z)>=c||z||^p, c>0. Put alpha=m/p, v(y)=1+kappa(1-y^2)^2,
b=1/2, beta,kappa>0. The actual diffusion is

    dY=-v'(Y)U(Z)dt+sqrt(2/beta)dW,
    dZ=-v(Y)M grad U(Z)dt+sqrt(2M/beta)dB,                 (1)

where M is any fixed symmetric positive definite matrix with an acquired floor
M>=mu I, mu>0. Cross mobility is zero and longitudinal mobility is one. The
mean requested is EXACTLY

    T_A=E_{Gibbs conditioned on Y<=-b} tau_{Y>=b}.        (2)

The full conditional Gibbs law is the declared mathematical initial law. Merely
matching its (Y,U) marginal, starting on a fixed ray, or drawing an approximate
finite-bit preparation in small total variation is NOT sufficient here. The
hitting-time function is unbounded; a physical preparation would require a
separate weighted error/moment guarantee. This theorem computes the symbolic
expectation without claiming to physically sample or actuate it.

The first receiver admits complete aligned positive quartic energy programs
U=sum_i d_i z_i^4 + sum_{i<j} J_ij z_i^2 z_j^2, d_i>0, J_ij>=0,
and a declared constant isotropic or diagonal mobility. All listed coefficients
are strictly positive; an absent interaction means zero. It reads every term,
checks the exact degree/sign/pure-term conditions, and acquires

    d_min=min_i d_i, c=d_min/m, alpha=m/4.

Indeed m sum_i z_i^4 >= (sum_i z_i^2)^2. Interaction strength and graph need not
be bounded or mixed rapidly. This is a complete raw mathematical model interface,
not empirical discovery of an unknown force or unknown kinetic matrix.

## 2. Global process and invariant law are earned

The smooth local coefficients of (1) define a unique local solution. With
K=1+kappa/p and V=1+y^2+K z^T M^-1 z,

    L V=2(1+Km)/beta -2[yv'(y)+Kp v(y)]U(z)
       <=2(1+Km)/beta -2p U(z),                          (3)

because yv'>=-kappa and v>=1. V is proper, so localization yields nonexplosion.
There is no singular origin and no Bessel-boundary receiving condition in this
constant-SPD model. Integration by parts gives the reversible Dirichlet form;
the finite Gibbs density exp(-beta v U) is invariant for the conservative
elliptic process. Homogeneous scaling gives the longitudinal marginal, up to one
constant independent of y,

    q(y)=v(y)^(-alpha),
    pi_y(z)=(beta v(y))^alpha exp(-beta v(y)U(z))/Z_U,
    rho=q pi_y,                                         (4)

where Z_U=int exp(-U(z))dz is finite but never evaluated. q is integrable when
alpha>1/4. The finite mean proof below needs alpha>3/4; the numerical backend
chooses integer alpha>=4. These are sufficient admitted conditions, not asserted
sharp conditions for every actual diffusion.

## 3. Full-state source current, with no projected Markov assumption

Work on Omega={y<b}, killed at its target boundary; A={y<=-b} and S={-b<y<b}.
The killed Dirichlet form is

    E(h)=beta^-1 int rho [h_y^2+grad_z h^T M grad_z h].    (5)

For f=1_A or 1_S define J_f(y)=int_-infinity^y q(s)f(s)ds and

    w(y,z)=-v'(y)z/[p v(y)],
    j_f=J_f pi_y (1,w).

The identity partial_y pi_y+div_z(w pi_y)=0 follows directly from homogeneity
z dot grad U=pU. Therefore div j_f=rho f. This is a full-state current whose
coefficient formula is constructed from the supplied energy, not an assumed
committor, conditional sampler, basis or Poisson solver.

Weighted integration by parts/Cauchy gives the source dual bound

    Q_f <= D_f = beta int_-infinity^b J_f^2/q [1+d(y)]dy,
    d(y)=(v'/(p v))^2 E_pi_y[z^T M^-1 z].                (6)

Here Q_f is the increasing zero-resolvent limit of
<f,(lambda-L_killed)^-1 f>. Constants from Z_U cancel. Since M^-1<=mu^-1 I,
coercivity, the homogeneous virial identity E_pi_y U=alpha/(beta v), and Jensen
for 2/p<=1 give

    d(y) <= C v'(y)^2 / v(y)^(2+2/p),
    C=(alpha/(beta c))^(2/p)/(mu p^2).                   (7)

The virial identity is exact by differentiating the scaling partition, or radial
integration by parts. It does not use convexity, angular relaxation or a Poincare
constant. A tiny mu can make the sufficient interval wide; mu is an actual
kinetic premise, not a tunable numerical accuracy knob.

Scalar Poisson trials h'=-beta J_f/q give

    L_f=beta int J_f^2/q <= Q_f.                          (8)

For clarity, the actual mean join is not capacity inversion. At lambda>0 the
killed-resolvent identity and positivity give

    M_A E_A int_0^tau_B exp(-lambda t)dt
        =Q_A(lambda)+Q_AS(lambda),
    0<=Q_AS(lambda)<=sqrt(Q_A(lambda)Q_S(lambda)).

The finite current energies below first prove finite Q_A,Q_S. On the slab
J_A=M_A and J_S<=M_S, and left of it J_S=0, so
D_S<=(M_S/M_A)^2 D_A. Only THEN does monotone convergence earn the finite actual
mean and its bounds

    L_A/M_A <= T_A <= (1+M_S/M_A) D_A/M_A.                (9)

This uses ordinary zero-resolvent variational duality. Compact-domain exhaustion
and finite-energy cutoffs justify the source/current integration and scalar
trials; an L2 zero-resolvent or global spectral gap is not assumed. For x->infinity,
M(x)=int_x^infinity q=O(x^(1-4alpha)); hence M(x)^2/q=O(x^(2-4alpha)).
The correction (7) decays as x^(-2-8/p). Thus all current energies are finite
for alpha>3/4. Fiber tails are controlled by coercivity. The scalar trial grows
only quadratically along the left tail, and truncation errors in energy/source
pairings vanish under the same tail condition; it need not be L2. This is the
same ordinary source-resolvent construction as the separately frozen radial-lift
proof, applied to the full elliptic model with its different inverse mobility.

## 4. Dimension-free quartic slab correction and paid basin contribution

Now p=4, c=d_min/m, alpha=m/4. Formula (7) becomes

    C=alpha/[8 mu sqrt(beta d_min)].

Write a=v(b)=1+9kappa/16 and R=int_-b^b v^alpha. On the half slab let W=v^alpha.
Since -W'>=0 and -v'<=4kappa y,

    C v'^2 v^(alpha-5/2)
      = (C/alpha)[-v'/v^(3/2)](-W')
      <= [4kappa C/(alpha a^(3/2))] y(-W').

Integrating by parts gives int y(-W')=int W-bW(b)<=int W. Evenness yields the
whole slab overhead

    C_s=kappa/[2 mu sqrt(beta d_min) a^(3/2)].           (10)

This bound is ONLY used on the transition slab. For every real y, put
x=|y^2-1| and r=sqrt(kappa)x. Since y^2<=1+x,

    v'^2/v^(5/2)
      <=16[kappa r^2+sqrt(kappa)r^3]/(1+r^2)^(5/2)
      <=16(kappa+sqrt(kappa)) <=32 max(kappa,1).

Thus the global correction bound used in the entire left basin is

    D_max=4alpha max(kappa,1)/[mu sqrt(beta d_min)].       (11)

Define only TWO numerically acquired integrals and explicit constants:

    M=int_b^infinity v^-alpha (=M_A by evenness),
    R=int_-b^b v^alpha,
    delta=1/alpha, c1=v(1+delta),
    S0=(1-b)a^alpha+delta c1^alpha,
    W_far=1/[64 kappa^2(alpha-1)^2 delta].

For integer alpha>=4, v<=a on [b,1+delta]. On that interval M(x)<=M, so the
basin longitudinal resistance is at most M^2 S0. For x>1, convexity gives
M(x)<=v(x)^(1-alpha)/[(alpha-1)v'(x)], while
v'(x)>=8kappa(x-1). Therefore the remaining resistance is at most W_far.
These full-tail bounds explicitly replace a nested cumulative integral; no
conditional or cumulative-mass oracle has been supplied. Finally M_S<=a^-alpha.
Consequently the actual mean is enclosed by

    T_low=beta M R,
    T_high=(1+a^-alpha/M) * {
      beta M R (1+C_s)
      + beta (1+D_max) [M S0+W_far/M] }.                 (12)

Every correction has its proper mobility/time factor. T_low happens to equal
reciprocal scalar free-energy conductance, but is proved as a source-A Poisson
lower bound; equality with the full mean is not claimed. Formula (12) retains
the nonzero basin resistance and cross-source correction. Its failure to meet a
requested width is UNKNOWN from a sufficient bound, not a physical error floor.
At beta=kappa=d_min=1, C_s=32/(125mu). An actual ordinary transverse mobility
M>=64I gives C_s=0.004, independent of fiber dimension, graph or coupling strength.
This is not a claim that default M=I must already achieve sub-one-percent width.

## 5. Consequence and strongest ordinary retaining alternatives

For all admitted raw quartic energies at the same m, beta, kappa and d_min,
and all actual fixed mobilities with the same lower floor mu, (12) is the SAME
outer interval for the Gibbs|A mean. Arbitrary angular interactions and hidden
relaxation times need not be reconstructed to certify this particular observable.
The actual means are NOT asserted equal, nor is (Y,U) asserted Markov. The full
Gibbs initialization remains a real input premise. Unlike a capacity-only bound,
this addresses an autonomous first-passage mean; unlike the earlier engineered
lift, it applies to ordinary constant mobility with no new tensor actuation.

All ingredients are ordinary: homogeneous partition scaling, a variational
restriction, conditional dilation current, inverse-mobility norm, virial/Jensen,
killed-resolvent duality and directed scalar quadrature. The newly assembled
source current and full global/initial-law/tail join are the constructed result;
these ordinary primitives do not establish historical novelty or a proprietary
algorithmic separation. An ordinary variational/Poisson-current implementation
with this derivation gets exactly this result. Counting that implementation as an
independent located predecessor would count the same construction twice.

A verified full elliptic PDE or stochastic barrier solver gets identical raw
energy and mobility, exact initialization, coercivity and all analytic bounds.
The isotropic Gaussian quadratic case has an exact (Y,||Z||^2) radial Markov
reduction and remains a strong lower-complexity comparator. For generic coupled
quartics the Euclidean energy generator contains ||grad U||^2 and Laplacian U,
not solely U: no exact scalar CIR reduction has been assumed. Averaging may be
efficient when conditional mixing is actually quantified; its cost/premise is
not silently given here. No formal computational lower bound or performance
victory over optimized verified solvers is claimed.

The first executable must acquire the whole mathematical model, prove its
mobility floor (compact isotropic or diagonal grammar), evaluate M/R with exact
outward arithmetic and full tails, outwardly enclose the square roots in
(10)-(11), bind the original external tolerance and exact Gibbs initialization,
and recompute every certified endpoint under finite explicit budgets. Raw input
reading and all repeated verification remain paid. Physical parameter inference,
actual implementation and finite-bit preparation are outside this result.
