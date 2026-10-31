# Qualitative consequence: asymptotic exactness without fiber mixing

Status: separately UNREVIEWED consequence; not a new executable claim and not an
optimization of the slab-contraction constant. It follows from the stronger
intermediate bound in PARALLEL_CHANNEL_CANDIDATE.md.

Fix kappa>0 and homogeneous degree p, while m grows. Allow arbitrary admitted
U_m in each dimension, with whatever finite coercivity constant and angular
interactions are needed for its conservative reversible process. The earlier
parallel proof yields

    I_minus(alpha)/I_plus(alpha) <= k_full/k_free <=1,
    alpha=m/p,
    I_minus=int_-b^b exp[alpha log(1-Delta/a)]dy,
    I_plus =int_-b^b exp[-alpha log(1+Delta/a)]dy,
    Delta/a=(kappa/(1+kappa))y^2(2-y^2), b=1/2.

Both scalar integrands have their unique maximum1 at y=0. With
c=2kappa/(1+kappa)>0, both exponents equal -c y^2+O(y^4). Standard elementary
Laplace scaling y=sqrt(alpha)^(-1) u gives

    sqrt(alpha) I_minus ->sqrt(pi/c),
    sqrt(alpha) I_plus  ->sqrt(pi/c).

For completeness, on the whole compact slab each negative exponent is bounded
above by -c0 y^2 for some c0>0: use Delta/a>=7kappa y^2/[4(1+kappa)] and
log(1+t)>=t/(1+d), -log(1-t)>=t. After the rescaling these are integrable
Gaussian dominators; outside the scaled slab the integrands can be set to0.
Pointwise convergence and dominated convergence prove both limits, with no
assumption on any U_m. Hence

    k_full/k_free ->1,

uniformly over the admissible angular models in each dimension, because the
bounding functions do not contain U_m. This is not an assertion that full
trajectories become Markovian, that fiber relaxation is fast, or that arbitrary
initial conditions equilibrate. It is a result only for equilibrium full-fiber
capacity/mass. Fixed kappa and p are essential to this stated limit; no uniform
claim over arbitrary dimension-dependent profile parameters is made.

An executed finite precision certificate can retain a fixed numerical width
unless its requested quadrature tolerance is also reduced. The theorem does not
silently turn the current fixed1% output into an exact value.
