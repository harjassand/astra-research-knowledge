# A uniform angular-independent passage law at original constant mobility

Status: new theorem candidate, separate from the finite receiver freeze. It
requires the well-current proof207d9ee314c2c3f4638d0a3c45eaa7e23fd85246010ef799fd538201a0278ab7
and the separately received trial/separate-current spectral principles. No
candidate asymptotic statement automatically accepts a finite numerical output.

## 1. Precise class and conclusion

Fix positive beta,kappa,d_0,mu, independent of dimension. For m=4alpha with
integer alpha>=4, allow EVERY finite homogeneous quartic polynomial U satisfying

    U(z)>0 for z!=0, U(z)>=d_0 ||z||^4/m,

and EVERY finite constant SPD transverse matrix M_z>=mu I. The admitted
positive-coefficient graph grammar with pure coefficients>=d_0 is one directly
acquired subclass. No uniform upper bound on angular interaction coefficients,
condition number, curvature, angular mixing time or partition constant is assumed.
Each actual model is ordinary reversible Langevin with potential v(y)U(z),
v(y)=1+kappa(1-y^2)^2, unit longitudinal mobility and zero cross mobility.
The initial law is its EXACT FULL Gibbs law conditioned on A={y<=-1/2};
tau_B is first arrival at B={y>=1/2}.

Define scalar quantities independent of U and M_z:

    M_alpha=int_(1/2)^infinity v^-alpha,
    R_alpha=int_(-1/2)^(1/2) v^alpha,
    T_alpha=beta M_alpha R_alpha.

Then the well-current and spectral constructions imply

    sup_(U,M_z) |E_A tau_B/T_alpha -1| ->0,
    sup_(U,M_z) sup_(s>=0)
      |P_A(tau_B/T_alpha<=s)-(1-exp(-s))| ->0             (1)

as alpha tends to infinity. Every supremum is over actual models satisfying
these precise fixed lower-bound premises. Their exact finite-dimensional means
and distributions need not coincide. The actual geometry/kinetic matrix is not
changed to accelerate the model. This is not an arbitrary-start theorem or a
uniform limit down to zero mobility at fixed dimension.

## 2. Entire-domain scalar limits, proved directly

Put v_*=1+kappa and c_R=2kappa/v_*. The scalar integrals obey

    sqrt(alpha) M_alpha -> sqrt(pi)/(2sqrt(kappa)),
    sqrt(alpha) R_alpha/v_*^alpha -> sqrt(pi/c_R),
    sqrt(alpha) Rplus_alpha/v_*^alpha -> sqrt(pi/c_R),    (2)

where Rplus=int_slab[v_*^2/(2v_*-v)]^alpha.

For M, set x=sqrt(alpha)(y-1), extend the rescaled integrand by zero below
x=-sqrt(alpha)/2, and use pointwise convergence to exp(-4kappa x^2).
Since y>=1/2 implies y+1>=3/2,

    v(y)>=1+(9kappa/4)(y-1)^2.

For alpha>=4, monotonicity of (1+t/alpha)^alpha in alpha yields a single
integrable dominating function

    [1+(9kappa/16)x^2]^-4.

Monotonicity follows from log(1+u)-u/(1+u)>=0, itself obtained by differentiation.
Dominated convergence proves the FIRST limit over the FULL infinite basin;
there is no truncated-well or local-only mass assumption.

For R set x=sqrt(alpha)y and extend by zero outside |x|<=sqrt(alpha)/2.
On the entire slab,

    v(y)/v_*=1-u(y),
    u(y)=(kappa/v_*)(2y^2-y^4)
       >=[7kappa/(4v_*)]y^2,
    0<=u<=7kappa/(16v_*)<7/16.

Thus the rescaled integrand is bounded by exp(-c_1 x^2), c_1=7kappa/(4v_*)>0,
and converges pointwise to exp(-c_R x^2). For Rplus/v_*^alpha the integrand is
(1+u)^-alpha. The inequality log(1+u)>=u/(1+u_max) gives another fixed Gaussian
dominator, and its pointwise limit is the SAME exp(-c_R x^2). This proves both
remaining limits in(2), hence Rplus/R ->1.

Consequently the common leading time scale is

    T_alpha ~ [beta*pi*sqrt(1+kappa)/(2sqrt(2)*kappa)]
                         * (1+kappa)^alpha/alpha.        (3)

This equivalence is about the scalar reference and, by(1), the actual full
Gibbs|A mean uniformly over the admitted family. It does not specify physical
units or authenticate a real process over that horizon.

## 3. Why all other source costs disappear uniformly

Use the explicit well-current constants

    a_b=1+9kappa/16,
    G_1=v_*^2/(2v_*-1), G_b=v_*^2/(2v_*-a_b).

For every fixed kappa>0, 1<a_b<v_* and G_1,G_b<v_*.
The remaining parameters K=alpha/[8mu sqrt(beta d_0)] and D_max are O(alpha)
with constants depending ONLY on the fixed beta,kappa,d_0,mu. Using(2) in the
explicit B_new of the finite proof gives

    b_alpha:=B_new/(beta M_alpha^2 R_alpha)
       = Rplus_alpha/R_alpha + E_alpha,

where E_alpha>=0 is bounded by a fixed polynomial in alpha times

    (G_b/v_*)^alpha + (G_1/v_*)^alpha + v_*^-alpha.

For example the near-well term is O(sqrt(alpha)(G_b/v_*)^alpha); the middle and
vertical terms together are O(alpha^(5/2)(G_1/v_*)^alpha); the far term is
O(sqrt(alpha)v_*^-alpha). All constants may depend on the fixed lower bounds,
not on U, its unknown angular partition or the actual matrix above its floor.
Therefore E_alpha vanishes exponentially up to these polynomial factors.

The true slab-to-basin ratio eta obeys

    eta<=a_b^-alpha/M_alpha=O(sqrt(alpha)a_b^-alpha).      (4)

The separate S-current factor1+C_s is dimension-independent for the fixed
parameters. The finite mean upper from the explicit source join reads

    1<=E_A tau_B/T_alpha
      <=(1+eta/2)b_alpha +(eta/2)(1+C_s).                 (5)

Equations(2),(4),(5) prove the first uniform limit in(1). This is a source
Poisson bound, not an assumption that mean equals inverse capacity.

## 4. Uniform distribution law, without an angular spectral argument

The scalar transition trial has energy1/(beta R_alpha), equals1 on A,0 on B,
and lies between0 and1. The separate-current spectral theorem gives the
conservative spectral defect

    epsilon_alpha <=(1+eta)[b_alpha+eta(1+C_s)]-1.

Its all-time actual-initial-law comparison adds
eta+sqrt(eta(1+eta)). The right side tends to zero by(2)--(4), with the SAME
bound for every admitted U and M_z. This proves the second limit in(1).
Neither an actual committor, an eigenvector, a conditional sampler, a recurrence
time nor a Poincare constant has been acquired or assumed.

For each fixed finite alpha, scalar far-tail trial functions
psi(-y/L), supported on y in(-2L,-L), have killed Rayleigh quotient O(L^-2).
Thus the global and killed spectral gaps are ZERO. There is no contradiction:
our estimates control the spectral measure of one task-specific trial vector,
not the bottom of the full spectrum. Small spectral weight may accumulate at
zero, and tiny extreme-tail probabilities remain outside absolute accuracy.

The mean convergence in(1) is proved separately by(5), not inferred from CDF
convergence. No higher moment convergence, exponential moment, relative-tail
asymptotic or uniform relative quantile error is asserted.

## 5. Optional universal first correction for this chosen witness

The limit proof above suffices. If a rate is desired, elementary local Taylor
expansion yields

    Rplus_alpha/R_alpha=1+3/(4alpha)+O_kappa(alpha^-2).    (6)

Here is the derivation including remainder control. Write d=kappa/v_* and
c=2kappa/v_*. Near zero,

 log(v/v_*)=-c y^2+(d-c^2/2)y^4+O_kappa(y^6),
 log([v_*^2/(2v_*-v)]/v_*)
            =-c y^2+(d+c^2/2)y^4+O_kappa(y^6).

Both functions are analytic on a fixed neighborhood of the origin. With
x=sqrt(alpha)y, split the integral at |x|=alpha^(1/12). In the inner part,
Taylor expansion of the exponential after factoring exp(-c x^2) has remainder
bounded by a constant times alpha^-2(x^6+x^8)exp(-c x^2), for all sufficiently
large alpha. This follows from |exp(r)-1-r|<=r^2 exp(|r|)/2 and the uniform
analytic sixth-order remainder; the scaled corrections are uniformly small on
that inner part. Their polynomial Gaussian integrals are finite. The outer
part is smaller than every inverse power of alpha by the Gaussian dominators
already proved in Section2. Thus each rescaled integral equals

 sqrt(pi/c) * [1+3 A/(4c^2 alpha)+O_kappa(alpha^-2)],

with A=d-c^2/2 for R and A=d+c^2/2 for Rplus. The Gaussian fourth moment follows
by integration by parts. Dividing the two expansions proves(6).

Together with the explicit exponentially small source corrections this gives
uniform UPPER errors O(1/alpha), with leading upper coefficient3/4, in(1).
It does NOT assert that actual model error equals3/(4alpha), nor that this
chosen witness is optimal. The O-constant has not been turned into a finite
receiving certificate; finite requested tolerances must still use the exact
interval engine, not an asymptotic substitution.

## 6. Ordinary priors and computational meaning

Homogeneous scaling, Laplace/Taylor estimates, Poisson-current duality and
spectral-mixture exponential approximation are ordinary existing tools.
Aldous--Fill's completely-monotone approach, recurrence-based metastability,
and exact task-specific coarse-graining remain strong priors, not erased by
this construction. No historical priority or generic new exponentiality theory
is claimed.

The structural result assembled here is uniform full-GibbsA kinetics across
arbitrary admitted angular energies and all constant mobilities above a fixed
floor, obtained from acquired radial coercivity and an explicit source current,
without identifying hidden angular relaxation or evaluating its partition.
The finite raw receiver remains essential: it verifies actual mathematical
membership, pays complete input reading and all three scalar integrals, and
returns UNKNOWN when its finite budget or requested total interval fails.
Its fixed default dimension/precision budgets are not a claim to execute an
infinite-dimensional limit. Empirical membership, approximate initialization
and implementation remain unearned; no broader physical conclusion follows.
