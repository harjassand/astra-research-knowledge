# Exact attainable conductance range with unidentified transverse mobility

Status: NEW full proof candidate, independently unreviewed. The earlier accepted
isotropic/parallel/finite-Jensen sources and ZIPs are unchanged. This is a
mathematical model-family result, not a recovered matrix or a physical calibration.

## 1. Precise model and claim

Let U:R^m->R, m>=1, be a homogeneous polynomial of even degree p>=2, positive
away from0, with acquired U(z)>=a0||z||^p, a0>0. Let kappa,beta>0 and4m>p.
Set F(y,z)=v(y)U(z), v(y)=1+kappa(1-y^2)^2. For each constant finite symmetric
positive-definite transverse matrix M, consider exactly

  dy=-v'(y)U(z)dt+sqrt(2/beta)dW_y,
  dz=-v(y)M grad U(z)dt+sqrt(2M/beta)dW_z,

with zero cross covariance and unit longitudinal mobility. Basins are full
fibers A={y<=-1/2}, B={y>=1/2}. The Gibbs probability mu does not depend on M.
The actual observable is k(M)=cap_mu,M(A,B)/mu(A).

Write alpha=m/p, b=1/2, q(y)=v(y)^(-alpha),

  Q=int_R q, MA=int_b^infinity q, R0=int_-b^b v^alpha,
  R(t)=int_-b^b exp[v(y)t]dy,
  k_free=1/(beta MA R0),
  k_parallel=1/(beta MA Gamma(alpha))
                int_0^infinity t^(alpha-1)/R(t)dt.         (1)

Then the EXACT set of attained rates is

  { k(M): M is constant finite SPD } = (k_parallel,k_free).(2)

The interval is nonempty and open. Both endpoints are approached, neither is
attained by any finite SPD matrix. In particular inf=k_parallel and sup=k_free.
For EVERY fixed SPD shape matrix B, gamma->k(gamma B) is finite, continuous and
strictly increasing on(0,infinity), with exactly this same image.

All these endpoint expressions depend on m,p,kappa,beta but not on U's angular
shape, coefficients or partition constant. This is NOT equality of actual rates
at a fixed M, and NOT independence of finite-time projected dynamics from U/M.
The accepted finite-Jensen computation gives a computable OUTER enclosure of(2),
not a numerical evaluation of the exact integral defining k_parallel.

## 2. Conservative reversible process for every member

The strict coercivity of U makes Z_U=int exp(-U) finite. Scaling gives
Z=Z_U beta^(-alpha)Q and mu(A)=MA/Q. The q tail is O(|y|^(-4alpha)), integrable
by4m>p. Smooth local coefficients and SPD M define a nondegenerate local process.
With K=1+kappa/p, the coercive function

  V_M=1+y^2+K z^T M^(-1)z

has generator

  L_M V_M=-2[yv'+Kpv]U+2(1+Km)/beta <=2(1+Km)/beta,

since yv'>=-kappa and v>=1 give yv'+Kpv>=p. The stopped Lyapunov argument proves
nonexplosion for each fixed M. Constant block mobility with matching drift/noise
makes finite mu reversible. No uniform Euclidean Lyapunov comparison, angular
mixing rate or effective convergence time as M becomes ill-conditioned is claimed.
The inverse matrix in this analytical proof is not a numerical operation required
by a universally quantified family certificate.

## 3. Variational space, minimizer existence and boundary closure

Use the global weighted Hilbert space

  H^1(mu)={h in L^2(mu): distributional grad h in L^2(mu)},

with its usual sum norm. Because mu has a smooth everywhere-positive density,
local weighted and unweighted norms are equivalent on compact sets. Distributional
derivatives are closed, making this a Hilbert space. Let K_AB be its closed convex
subset with0<=h<=1, h=1 mu-a.e. on A, h=0 mu-a.e. on B. These are closed convex
L^2 constraints, hence weakly closed; no unproved compact embedding is required.
The global H^1 condition supplies the usual matching traces at y=+/-b from the
constant interior values on the basins. Conversely truncation to[0,1] does not
increase a positive quadratic Dirichlet energy, so this class gives the capacity.
A smooth scalar transition makes K_AB nonempty with finite energy.

For each fixed SPD M the energy

  E_M(h)=beta^(-1)int[h_y^2+(grad_z h)^T M grad_z h]dmu

controls the derivative part of H^1 up to a positive M-dependent constant.
A bounded-energy minimizing sequence in K_AB also has L^2 norm<=1. Weak Hilbert
compactness and lower semicontinuity give a minimizer h_M in K_AB. Strict
quadratic convexity, connectedness and the fixed basin values make it unique:
if two minimizers differ, their difference has zero gradient, hence is a constant
and must vanish. Local elliptic regularity for the constant SPD principal matrix
and smooth potential makes h_M smooth in the open transition slab.

## 4. Universal bounds and the low-mobility limit

The accepted fiberwise weighted Cauchy argument gives

  E_M(h)>=cap_parallel,   cap_parallel=mu(A)k_parallel,

because the transverse energy is nonnegative and each fixed fiber has a unit
boundary drop. The scalar optimal trial gives cap_M<=cap_free=mu(A)k_free.

For the lower endpoint define, inside the slab, the decreasing fixed-fiber
committor

  h_parallel(y,z)= [int_y^b exp(beta v(s)U(z))ds]
                  /[int_-b^b exp(beta v(s)U(z))ds],

extended by1 on A and0 on B. Its longitudinal energy is EXACTLY cap_parallel.
Its U-derivative is beta times a covariance of a bounded indicator with v under
the normalized interval density proportional exp(beta v(s)U), hence

  |partial_U h_parallel| <= beta osc_slab(v).

Thus |grad_z h_parallel|<=beta osc(v)|grad U|. On the compact y slab the Gibbs
weight is bounded above by exp(-beta v_min U)/Z. Since grad U is polynomial and
U coercive, all required transverse squared-gradient integrals are finite.
The extension has matching values at the boundary planes and is in H^1(mu).
For each fixed SPD B,

  E_(gamma B)(h_parallel)=cap_parallel+gamma C_B,
  C_B=beta^(-1)int(grad_z h_parallel)^T B grad_z h_parallel dmu<infinity.

Together with the lower bound this proves

  lim_(gamma down0) cap_(gamma B)=cap_parallel.            (3)

C_B may depend on unknown angular quantities/B. This is an existence/limit proof,
not an advertised acquired convergence modulus or algorithm producing a finite
gamma from a requested error for free.

## 5. The high-mobility limit without a conditional Poincare assumption

Fix SPD B and let gamma_n->infinity. Choose its minimizers h_n (near-minimizers
would also suffice). For gamma_n>=1 the scalar upper bound implies

  int h_n,y^2 dmu <= beta cap_free,
  int ||grad_z h_n||^2 dmu
       <= beta cap_free/[gamma_n lambda_min(B)] ->0.

With0<=h_n<=1 this is a bounded global H^1 sequence. Pass to a weak H^1
subsequence h, which remains in the weakly closed K_AB. Strong convergence of
the z-gradients to0 gives grad_z h=0. Positivity of the weight on compacts then
implies distributionally that h(y,z)=g(y) almost everywhere, since each entire
fiber R^m is connected. There is no mass-escape or compactness-of-embedding step:
only weak Hilbert compactness and closed basin constraints are used.

Lower semicontinuity of the longitudinal energy yields

  liminf cap_(gamma_n B)
    >= beta^(-1)int |g'(y)|^2 dmu
    >= cap_free,

the last inequality being the scalar Dirichlet minimum with the inherited basin
values. The reverse bound is already known. Every divergent gamma sequence has
this lower bound, proving

  lim_(gamma to infinity) cap_(gamma B)=cap_free.          (4)

This does not identify a rate of convergence or establish a Markovian limiting
trajectory over finite times; it is solely the variational conductance limit.

## 6. Strictness, continuity and the complete range

No finite-M minimizer can be fiber-constant. If h_M=g(y), its interior weak
Euler-Lagrange equation, made pointwise by local regularity, is

  beta^(-1)g''(y)-v'(y)U(z)g'(y)=0 for all z.

At z=0, U=0 gives g''=0. At any z with U(z)>0, and at every y except0 in the
transition slab, v'(y)!=0 gives g'=0. Continuity and the two basin traces then
contradict the unit boundary drop. Hence the transverse gradient has positive
weighted energy for every SPD shape B.

Consequently cap_M>cap_parallel: at its minimizer, the longitudinal energy is
at least cap_parallel and the transverse quadratic energy is strictly positive.
Also cap_M<cap_free: equality would make the scalar optimal trial a minimizer,
contradicting the same non-scalar fact. This proves strict endpoint exclusion and
in particular cap_parallel<cap_free.

For gamma2>gamma1>0, use the gamma2 minimizer in the gamma1 variational problem:

  cap_(gamma1 B)
    <=cap_(gamma2 B)-(gamma2-gamma1)E_B^transverse(h_(gamma2 B))
    <cap_(gamma2 B).

The function cap_(gamma B) is the infimum of affine functions of gamma, hence
concave. It is finite throughout the open positive axis, so it is continuous
there (alternatively local slope bounds follow from the energy bound divided by
gamma). By(3),(4) and strict continuity, its image is the entire open interval
(cap_parallel,cap_free). The family over all SPD M contains this path and, by
strict endpoint exclusion, nothing outside that interval. Dividing by the same
positive mu(A) proves(2).

## 7. Exact information loss and honest computational receiving

For fixed m,p,kappa,beta, every admitted angular U has the same attainable rate
interval when transverse SPD mobility is unidentified. Moreover for every fixed
SPD shape B there is exactly one positive scalar gamma achieving a specified
interior rate. When m>=2 (as in the current raw quartic consumer), an observed interior
conductance alone cannot identify the MATRIX SHAPE: distinct nonproportional
shapes can each be scaled to realize it.
Across angular models it likewise cannot identify U. This does not contradict
uniqueness of gamma if BOTH U and the shape B are already known.

The existence assertion is not a constructive inverse-mobility solver. No free
planner, PDE oracle, realized gamma, or actual system calibration is provided.
The executed finite-Jensen interval is a computable outer enclosure of the exact
unknown-mobility range, and can be narrow without learning hidden relaxation
rates. A new family-scoped schema must explicitly quantify over fixed block-SPD
mobility; existing isotropic certificates are not silently relabeled.

The structural interface still excludes longitudinal mobility changes, cross
mobility, variable/singular M, nonreversible drifts and time-dependent controls.
For example [[1,1],[1,1+epsilon]] is SPD but gives energy epsilon to gradient(1,-1),
so dropping its cross-coupled fiber term would not retain h_y^2. Full-fiber basins,
known potential/beta, Gibbs/FDT structure and global existence remain essential.
The ordinary variational, weak Hilbert, homogeneity, Gamma and concavity tools
are credited; historical priority and scientific-system applicability are open.
