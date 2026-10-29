# From stationary position information to quantitative weak force norms

29 October 2026. Independent construction/check of the root's Duhamel
translation argument, followed by a directly usable learned-candidate bridge.
These are ordinary analytic proofs. They do NOT assert a controlled-path
error rate, identify an unknown source from data, or acquire physical entropy,
position precision, a bath, or a candidate potential.

## 1. Native domain and conventions

Positions lie on the side-2pi d-dimensional torus, with normalized uniform
measure u(dq). Momenta are in R^d. The stationary native model is

    dq=p dt,
    dp=[F(q)-gamma p]dt+sqrt(2 gamma tau)dW,              (1)

with gamma,tau>0, smooth periodic F, and ||F||_infinity<=A. No uniform
bound on derivatives of F is imposed. Let rho be its stationary law and
n=dnu/du its position density. The density will also follow from the
Duhamel formula below. Use the established finite-moment and thermal
entropy/Fisher domain. The entropy is the actual calibrated single-bath
quantity sigma, not an arbitrary observed reversal divergence.

For a real C1 vector test phi define

    ||phi||_C1=max(||phi||_infinity,||Dphi||_infinity,op).

The dual norm is the supremum of absolute pairing over this unit ball.
All L1 density norms below are relative to normalized uniform measure.
W1 is the geodesic position Wasserstein distance. Let D=pi sqrt(d) be
the torus diameter, and let

    P2=(A/gamma+sqrt(d tau))^2

be the established uniform bound on E_rho |p|^2.

The exact static residual from the physical-frontier construction is

    R=F n-tau grad n,
    |<R,phi>|<=sqrt(tau sigma/gamma)
      sqrt[gamma^2||phi||_infinity^2+P2||Dphi||_infinity,op^2]. (2)

It is used as a distributional identity and inequality; no strong force
identification is inferred from it. Conditional Maxwell thermalization also
gives TV(rho,nu x M_tau)<=sqrt[sigma/(4gamma)].

## 2. Free Duhamel representation: signs and domains

Let P0^s be the free Kramers semigroup with the same gamma,tau. For a
smooth periodic position test g,

    d/ds rho(P0^s g)=rho(L0 P0^s g)
                    =-rho[F dot grad_p P0^s g],

because rho is stationary for L=L0+F dot grad_p. Thus

    nu(g)=rho(P0^t g)+int_0^t rho[F dot grad_p P0^s g]ds. (3)

The weak formula has the PLUS sign stated by the root. The smooth tests
have bounded spatial derivatives; the free formula below and the stationary
moment bounds justify differentiating under rho, with momentum localization
if needed. There is no assumption that rho is stationary for the free
semigroup.

For s>0 put

    a_s=(1-exp(-gamma s))/gamma,
    v_s=2gamma tau int_0^s a_r^2 dr
       =(tau/gamma^2)[2gamma s-3+4exp(-gamma s)-exp(-2gamma s)]. (4)

The free position is q+a_s p plus a centered Gaussian of covariance v_s I,
wrapped on the torus. In particular v_s~(2/3)gamma tau s^3 at zero. Let
G_v be that wrapped Gaussian density relative to u. Then

    P0^s g(q,p)=(G_(v_s)*g)(q+a_s p),
    grad_p P0^s g=a_s grad(G_(v_s)*g)(q+a_s p).          (5)

Define the probability measure mu_s as the pushforward of rho by
(q,p)->q+a_s p modulo the torus, and define a vector measure M_s by

    M_s(E)=E_rho[F(q) 1_{q+a_s p in E}],       |M_s|(T^d)<=A.

Distributional integration by parts in (3) gives the DENSITY formula

    n=G_(v_t)*mu_t
        -int_0^t a_s sum_i (partial_i G_(v_s))*M_(s,i) ds. (6)

The density formula has a MINUS sign. This sign has no effect on the norm
bound but should not be confused with the plus sign in (3). The convolution
integral is a Bochner L1 integral: near zero, a_s||grad G_(v_s)||_1 is
O(s^-1/2), hence integrable. Thus (6) also proves absolute continuity of
the position law under the stated stationary hypotheses.

## 3. An explicit uniform L1 translation modulus

Wrapping a Gaussian cannot increase the L1 norms of its derivatives. For
a unit direction e and any torus translation h of length r=|h|,

    ||G_v(.+h)-G_v||_1
           <=min(2,sqrt(2/pi) r/sqrt(v)),
    ||grad G_v||_1<=sqrt(d)/sqrt(v),
    ||D_e grad G_v||_1<=sqrt(d+1)/v.                    (7)

For the last inequality, write the unwrapped Gaussian derivative in terms
of Z~N(0,I_d). Cauchy--Schwarz uses
E|Z(Z dot e)-e|^2=d+1. These constants are independent of the transported
measures in (6).

Subtract a translate of (6), use |M_s|<=A, and obtain

    ||n(.+h)-n||_1
      <=min(2,sqrt(2/pi) r/sqrt(v_t))
        +A int_0^t a_s min(2sqrt(d)/sqrt(v_s),
                                      sqrt(d+1) r/v_s) ds. (8)

This verifies the proposed estimate including the derivative powers.
For explicit constants choose t_*=1/gamma and

    b=(2gamma tau/3)exp(-2).

For 0<s<=t_*, a_s<=s and v_s>=b s^3, since
a_r>=exp(-gamma t_*)r. Hence the integral in (8) is at most

    A int_0^t* min(L s^-1/2,H r s^-2)ds,
    L=2sqrt(d)/sqrt(b),       H=sqrt(d+1)/b.

Splitting at s_0=(H r/L)^(2/3), or simply extending this positive upper
integrand to infinity, gives

    int_0^infinity min(L s^-1/2,H r s^-2)ds
                         =3 L^(2/3) H^(1/3) r^(1/3).

Since r<=r^(1/3) for 0<=r<=1, define

    C_tr=sqrt(2/pi)/sqrt(v_(t_*))+3A L^(2/3)H^(1/3).

Then uniformly over the native stationary class,

    ||n(.+h)-n||_1<=C_tr |h|^(1/3),       0<|h|<=1.    (9)

The left side is also at most two. In standard terms, n has a uniformly
bounded B_(1,infinity)^(1/3) position norm. The explicit difference bound
(9), rather than any convention for that norm, is what subsequent proofs
use. No source-force derivative, configurational mixing rate, or lower
density bound enters this regularity statement.

## 4. Weak position-law fit becomes strong density fit

Let U be ANY smooth periodic candidate with ||grad U||<=A, put
G=-grad U, and let m=dnu_U/du be its normalized Gibbs position density.
Suppose the complete position laws satisfy the warranted bound

    W1(nu,nu_U)<=e.                                     (10)

The Gibbs formula supplies

    m>=c_G=exp(-AD/tau),
    |grad log m|<=A/tau,       ||grad m||_1<=A/tau.      (11)

These bounds concern the candidate, and do NOT require a source density
floor. In particular this learned-candidate bridge does not depend on the
new uniform source floor in physical_frontier.

Fix a nonnegative smooth Euclidean probability bump eta supported in the
unit ball, and let k_delta be its normalized periodization at scale
0<delta<=1. Write J_eta=int_R^d |grad eta(z)|dz. The triangle inequality,
(9), the candidate gradient bound, and any position coupling give

    ||n-m||_1
      <=||n-k_delta*n||_1+||k_delta*(nu-nu_U)||_1
                                  +||k_delta*m-m||_1
      <=C_tr delta^(1/3)+(A/tau)delta+J_eta e/delta.    (12)

For the middle term, integrate
||k_delta(.-q)-k_delta(.-q')||_1 <=(J_eta/delta)d_T(q,q')
over an optimal W1 coupling. This uses the L1 kernel derivative, not its
L-infinity derivative; no dimension-dependent delta^(-d-1) is needed here.

For 0<e<=1, choosing delta=e^(3/4) proves the explicit bound

    theta:=||n-m||_1<=C_pos e^(1/4),
    C_pos=C_tr+A/tau+J_eta.                             (13)

One may take the minimum with two. For e=0 the two measures are equal,
so the same conclusion holds by a limit. This is not a TV-from-W1 claim
for arbitrary densities: source regularity (9) and candidate regularity
(11) are essential.

## 5. The directly acquired-position-to-force bridge

The exact distribution identity is

    (F-G)m=R+tau grad(n-m)+F(m-n).                       (14)

For ||phi||_C1<=1, test it against phi/m. By (11),

    ||phi/m||_infinity<=c_G^-1,
    ||D(phi/m)||_infinity,op<=c_G^-1(1+A/tau),
    ||div(phi/m)||_infinity<=c_G^-1(d+A/tau).

Using (2) and integrating the gradient term against n-m gives

    r:=||F-G||_(C1)* <= C_R sqrt(sigma)+C_N theta,
    C_R=c_G^-1 sqrt(tau/gamma)
                        sqrt[gamma^2+P2(1+A/tau)^2],
    C_N=c_G^-1(tau d+2A).                              (15)

The additional A in C_N is the direct F(m-n) term. In particular,

    ||F-G||_(C1)*
          <=C_R sqrt(sigma)+C_N C_pos e^(1/4).          (16)

Both forces are bounded by A, so r<=2A is another trivial upper bound.
The initial PHASE-SPACE laws satisfy, by conditional Maxwell thermalization,

    TV(rho,nu_U x M_tau)
           <=sqrt[sigma/(4gamma)]+theta/2
           <=sqrt[sigma/(4gamma)]+(C_pos/2)e^(1/4).     (17)

Equations (16)--(17) apply to any bounded-gradient candidate satisfying
(10), including a candidate selected by conventional constrained Boltzmann
fitting. The bound e must actually include data error, position calibration,
dependence/sampling confidence and solver error if it is an acquired fit.
The theorem does not supply those observations, independent starts, or a
physical entropy upper bound. A lower entropy certificate is insufficient
to insert a small sigma on the right.

## 6. Negative Besov force norms with explicit interpolation exponents

Write H=F-G, so ||H||_infinity<=2A. Fix a usual smooth inhomogeneous
periodic Littlewood--Paley decomposition Delta_j on position space,
j>=-1. Constants below depend only on its fixed cutoff and d.

Its convolution kernel has uniformly bounded L1 norm, while its C1 norm
as a test function is at most C 2^((d+1)j) for j>=0. Testing H against
translated kernels and using its amplitude bound therefore gives

    ||Delta_j H||_infinity
              <=min(C A,C r 2^((d+1)j)),               (18)

with the analogous bounded low block. Splitting frequencies at
2^((d+1)j) approximately A/r yields, for 0<alpha<=d+1,

    ||H||_B_(infinity,infinity)^(-alpha)(T^d)
        <=C_alpha A^(1-alpha/(d+1)) r^(alpha/(d+1)).    (19)

The r=0 or A=0 cases are interpreted by continuity; A=0 is trivial.
For alpha>=d+1 one can instead use the simpler bound C_alpha r.
At alpha=d+1 there is no logarithm because the dyadic block norm is a
supremum, not a sum.

For the kinetic anisotropy with POSITION weight 3 and MOMENTUM weight 1,
extend H periodically in q and independently of p to R^(2d). On p-frequency
zero, an anisotropic block j is a position cutoff at frequency order 2^(3j).
Its projected convolution kernel has uniformly bounded position L1 norm
and position C1 norm at most C 2^(3(d+1)j). Thus

    ||Delta_j^kin H||_infinity
              <=min(C A,C r 2^(3(d+1)j)).               (20)

For 0<beta<=3(d+1),

    ||H||_C_kin^(-beta)
       <=C_beta A^(1-beta/[3(d+1)]) r^(beta/[3(d+1)]).  (21)

Here C_kin^(-beta) denotes the explicitly specified inhomogeneous
B_(infinity,infinity) norm with that anisotropy. A fixed bath-coordinate
rescaling changes constants but not these interpolation exponents.
The absence of momentum dependence is essential to the position count
d+1 in (20); this formula should not be transferred to arbitrary moving
full-phase-space fields.

Combining (16) and (21) supplies an explicit negative kinetic force norm
from a warranted entropy upper bound and complete position-law fit:

    ||F-G||_C_kin^(-beta)
       <=C (sqrt(sigma)+e^(1/4))^(beta/[3(d+1)]).       (22)

The constants retain the fixed native parameters and cutoff. This is the
promised information-to-force bridge; it does not itself give a rate for
controlled path laws. Such a use still needs a quantitative kinetic stability
theorem at the same force, control, preparation and observation interface.
A full-trajectory TV conclusion would in fact contradict the native shear
counterexample. The strong bound in (17) concerns INITIAL LAWS only.

## 7. Separate sigma-only construction using the source density floor

This subsection retains the root's original smoothed construction. It is
SEPARATE from the learned-candidate theorem, which required no source floor.
Use the explicit uniform c_*>0 proved in
physical_frontier/QUANTITATIVE_STATIC_FORCE_BALANCE.md, so n>=c_*.

Let n_delta=k_delta*n and U_delta=-tau log n_delta. With the kernel
constants C0,C1 defined in that physical-frontier proof, convolution of (2)
gives

    ||grad U_delta||_infinity<=A+epsilon_delta,
    epsilon_delta=c_*^-1 sqrt(tau sigma/gamma)
        sqrt[gamma^2 C0^2 delta^(-2d)
                                 +P2 C1^2 delta^(-2d-2)]
                 <=E sqrt(sigma) delta^(-d-1),         (23)
    E=c_*^-1 sqrt(tau/gamma)
                          sqrt[gamma^2 C0^2+P2 C1^2].

For delta<=1, scale U_delta by A/(A+epsilon_delta), with the trivial
zero case handled separately, to obtain U_tilde with ||grad U_tilde||<=A.
The gradient of U_delta-U_tilde is at most epsilon_delta. The same bounded
exponential-tilt calculation used in the source proof gives

    ||n_delta-m_tilde||_1<=D epsilon_delta/(2tau),
    m_tilde=dnu_(U_tilde)/du.

Together with (9), the actual density mismatch is therefore

    theta_delta:=||n-m_tilde||_1
         <=C_tr delta^(1/3)+D epsilon_delta/(2tau).     (24)

Apply (15) to this candidate, obtaining exactly the proposed rate structure

    ||F+grad U_tilde||_(C1)*
       <=C_R sqrt(sigma)
           +C_N[C_tr delta^(1/3)+D epsilon_delta/(2tau)]. (25)

This argument avoids differentiating a division by an uncontrolled source
density. Equivalently, direct testing with phi/n_delta also works because
the floor c_* and |grad log n_delta|<=(A+epsilon_delta)/tau control its C1
norm without a new delta-derivative loss.

For E sqrt(sigma)<=1, choose

    delta=(E sqrt(sigma))^(3/(3d+4)).                   (26)

Then delta^(1/3)=(E sqrt(sigma))^(1/(3d+4)), and the upper bound in (23)
for epsilon_delta has the same value. Hence, as sigma decreases to zero,

    ||F+grad U_tilde||_(C1)*=O(sigma^(1/(6d+8))),
    TV(rho,nu_(U_tilde) x M_tau)=O(sigma^(1/(6d+8))).   (27)

The initial TV bound follows from (17) using (24). No physical resetting or
regeneration is performed by this mathematical comparison. The corresponding
negative kinetic Besov bound is

    ||F+grad U_tilde||_C_kin^(-beta)
           =O(sigma^(beta/[3(d+1)(6d+8)])).            (28)

All constants are explicit in the chosen kernel, density floor and native
parameters. They can be very large, and these exponents are not claimed
optimal or practically efficient. Choosing a bandwidth optimal for a static
W1 fit need not be optimal for the stronger density/weak-force objective.

## 8. Scientific and operational boundary

The substantive bridge is quantitative: complete position-law fit, bounded
force and a calibrated small physical entropy upper bound now control BOTH
the initial phase-space law and a negative force norm without a force-
derivative cap. A fixed precision statement about only coarse positions is
not automatically the full W1 input; actual acquisition must warrant it.

The methods are ordinary Gaussian smoothing, Duhamel, the stationary momentum
identity, distribution testing, Gibbs inversion and low/high frequency
interpolation. These lemmas do not assert historical novelty for those
ingredients. They can be used by a strong conventional solver with exactly
the same information. No full-task speedup, controlled stability exponent,
hidden memory contraction or instrument operation has been established here.

The proof input (2) and the optional source-floor construction are from
physical_frontier/QUANTITATIVE_STATIC_FORCE_BALANCE.md. The density-floor
input is not needed for Sections 2--6. The source's accepted conditional
Maxwell identity and bounded-force stationary moment estimates are used at
their existing scope. The new translation, learned-candidate and Besov
lemmas have ordinary derivations here and await separate independent review.
