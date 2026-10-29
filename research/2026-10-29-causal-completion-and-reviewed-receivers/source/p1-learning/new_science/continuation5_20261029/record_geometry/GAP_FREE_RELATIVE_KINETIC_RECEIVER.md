# Relative kinetic control is a stronger ordinary receiver than additive local stability

29 October 2026. Complementary analysis by the existing record-geometry role.
This is an ordinary receiving mechanism and an explicit supplier boundary, not
a claim of a new perturbation theorem or of completed physical acquisition.

## 1. What changes the research choice

Uniform mixing is not necessary for every useful uniform-in-time response
guarantee. If an implementation preserves the **same complete equilibrium**
as the target and controls its kinetic error *relative to the dissipative
directions*, then equilibrium correlations and responses to a local change
of the initial density can remain accurate at all deterministic times, even
when the spectral gap vanishes with system size or frozen hidden sectors remain.

The abstract perturbation result is already established: Krešimir Veselić,
*Bounds for contractive semigroups and second order systems*, Theorem 1
(2004 preprint, 2005 publication),
<https://arxiv.org/pdf/math/0404120>. Its symmetric cross-energy condition
gives a semigroup-norm error at most half its form constant. The proof below
specializes that argument to reversible Markov dynamics and identifies the
local physical quantities which would have to be supplied.

This receiver should be considered before restricting every consequential
program to a Dobrushin contraction regime. It does **not** turn an acquired
additive equilibrium L2 closure defect into a relative form certificate.

## 2. Finite-volume statement and short proof

Let A and B be nonnegative self-adjoint operators on L2(mu), where mu is the
same full microscopic probability law for both physical dynamics. Their
Markov semigroups are P_t=exp(-tA) and Q_t=exp(-tB). For definiteness the proof
is finite-state; extensions require the appropriate common form domain and
well-defined semigroups. Write E_A(f,g)=<f,Ag>_mu. Suppose

    |E_B(f,g)-E_A(f,g)|
       <= eta sqrt(E_A(f,f) E_A(g,g)),    0<=eta<1.       (1)

Then, for every t>=0,

    ||P_t-Q_t||_(2->2) <= eta/[2 sqrt(1-eta)] =: c_eta.  (2)

Indeed E_B>= (1-eta)E_A. Differentiating
<Q_(t-s)g,P_s f> and integrating bounds its endpoint difference by

    eta/sqrt(1-eta)
       integral_0^t sqrt(E_B(Q_(t-s)g) E_A(P_s f)) ds.

The energy identities give

    integral_0^t E_A(P_s f) ds
       = (||f||_2^2-||P_t f||_2^2)/2,

and the analogous identity for B. Cauchy-Schwarz in time proves (2).
No inverse gap, state count or lower bound on mu(x) occurs. Comparability
also forces the two null spaces to agree; a new conserved direction is not
an admissible small relative perturbation.

More generally the direct symmetric premise

    |E_B(f,g)-E_A(f,g)| <= zeta sqrt(E_B(f,f) E_A(g,g))  (3)

gives zeta/2. This is the established cross-energy form of the result.

The same finite-dimensional energy argument works for externally prescribed,
time-dependent self-adjoint A_s,B_s in one common L2(mu), with (1) holding
uniformly in s. Test a forward A-evolution against a backward B-evolution.
Their two integrated energies are each at most half the squared endpoint
norm, so the bound is independent of the number of switches as well as
total duration. This allows open-loop control of the kinetic terms.
State/history-dependent control is not automatically an externally
prescribed evolution after conditioning on the observed record.

## 3. Why local errors need not add with volume

Suppose A is a sum of local reversible jump generators, with undirected
edge conductances c_e>=0 in the common full equilibrium. Edges may be
labelled by their physical operation; parallel edges are allowed. For a
choice of one orientation per undirected edge,

    E_A(f,g)=sum_e c_e Delta_e f Delta_e g.

Suppose B has the same support and conductances

    c'_e=(1+theta_e)c_e,    |theta_e|<=eta.             (4)

The sum over edges and Cauchy-Schwarz immediately give (1). In particular,
one does not first add local operator-norm errors into a norm of the global
generator. An analogous local form bound, with the same eta for every
local term, also sums to (1) by Cauchy-Schwarz over those terms.

This applies to interacting Gibbs targets at strong coupling. It also
applies within a direct integral of frozen hidden sectors, provided every
sector has the same intended visible law and (4) holds in each sector.
The frozen-sector law is retained, not prepared or equilibrated.

Exact equilibrium preservation is doing substantive work. A small error in
a local energy ratio generally changes the equilibrium and is not covered
by (4) in a common L2 geometry. The finite-range ring in
COUNTEREXAMPLES_AND_INTERFACE_BOUNDARIES.md has uniformly vanishing
heat-bath row errors but an order-one local equilibrium magnetization error.

## 4. Useful objectives with no global-density penalty

Because P_t and Q_t both preserve constants, for any f,g in L2(mu),

    |<f,(P_t-Q_t)g>_mu|
      <= c_eta sqrt(Var_mu(f) Var_mu(g)).               (5)

Thus two-time equilibrium correlations of bounded local observables have
a uniform-in-time, volume-independent error. This is a correlation
objective, not total variation of the entire subsequent trajectory.

If the initial full law is rho=g_0 mu, the same argument gives

    |rho P_t f-rho Q_t f|
      <= c_eta ||g_0-1||_2 sqrt(Var_mu(f)).             (6)

A local initial reweighting g_0=w(Y_A)/mu[w(Y_A)], with fixed finite A and
0<w_min<=w<=w_max, has a density ratio bounded independently of the total
volume. Formula (6) therefore covers relaxation after a *warranted* local
preparation at critical or strongly coupled equilibria. It does not supply
that initial preparation, the baseline equilibrium, or a bound for a fully
specified microscopic initial configuration whose density is enormous.

For finite initial and terminal readouts U,V with a and b possible values,
the equilibrium two-time joint laws satisfy

    TV(Law_A(U_0,V_t), Law_B(U_0,V_t))
      <= (c_eta/2) sqrt((a-1)(b-1)).                    (7)

For each pair of outcomes, apply (5) to their indicators, sum the absolute
probability differences and divide by two. The inequality
sum_u sqrt(p_u(1-p_u))<=sqrt(a-1) gives (7). Local alphabet sizes occur;
the total number of microscopic sites does not. Cap any TV bound at one.

Positive averages over times, including normalized Laplace transforms,
inherit (5). An unnormalized integral over an infinite time interval,
unsmoothed spectral density, or a diverging susceptibility needs a separate
argument. Nothing here bounds those quantities by merely integrating a
constant over an infinite interval.

## 5. Actual program time must be named

When the physical primitive is a fixed endpoint kernel K_i, the generator
sum_i r_i(K_i-I) describes independent Poisson opportunities to execute
those calls. This can be an actual continuous-time source only if the
clock, isolation, switching and call-duration interface realizes it.

Alternatively it is an exact randomized endpoint program: use Poisson
numbers of sequential calls and report completion endpoints, paying every
call and duration. Its parameter is operational time. It is not a claim
about the distribution at a fixed external wall time. The previous
stationary-change-of-measure compiler explicitly distinguishes these
objects, and that distinction remains necessary here.

A separate discrete-time theorem can be used if both endpoint operators
have nonnegative spectrum. With A=I-K, B=I-K', premise (1) gives

    sup_n ||K^n-(K')^n||_(2->2) <= eta/sqrt(1-eta).     (8)

Telescoping, Cauchy-Schwarz and
sum_(j>=0) E_A(K^j f)<=||f||_2^2 prove (8), because
I-K^2=(I+K)A>=A. Nonnegative spectrum is an extra premise; a reversible
kernel can have negative eigenvalues. An unavailable protected hold is
not silently inserted to make it lazy.

## 6. A concrete physical supplier using the preserved stronger interface

The earlier iid frozen-disorder receiver can supply a relative rather than
absolute kinetic certificate, with actual costs. At site i, let the native
visible flip increments be independent Bernoulli(p_i) conditional on its
unchanged hidden specimen, with a warranted p_i>=p_min>0. This is a
stronger interface than the general operation-algebra acquisition model.

For an integer local target equilibrium ratio r, the preserved bounded
binary compiler has opposite transition probabilities

    a_r(p_i)=1-(1-p_i)^r,       a_r(p_i)/r,             (9)

in the appropriate directions. It therefore fixes the target ratio
exactly without estimating p_i. A target solver may use the same pair
with p_i replaced by its measured estimate p_hat_i. Both kernels satisfy
the same exact local detailed balance. Estimation changes their symmetric
mobility, not the equilibrium weights.

The function a_r is increasing, concave and a_r(0)=0. Consequently

    |p_hat_i/p_i-1|<=eta
      implies |a_r(p_hat_i)/a_r(p_i)-1|<=eta           (10)

for every positive integer r, simultaneously. If (1+eta)p_i>1, use the
fact that a_r(p_i)>=p_i and a_r(p_hat_i)<=1 for the upper inequality.
No derivative or constant growing with r is needed.

Using M iid native increments per site, the usual multiplicative
Bernoulli bound supplies all d relative estimates with failure probability
at most beta whenever

    M >= [3/(p_min eta^2)] log(2d/beta),   0<eta<=1.   (11)

This costs dM native calls, plus sensing and the actual site/word selectors.
It does not justify learning arbitrary heterogeneous sites from one site.
For fixed finitely many local contexts the same estimate p_i can feed all
ratios if the native p_i is indeed independent of context. Otherwise every
distinct physical context needs its own warranted calibration.

Condition on the entire hidden vector and calibration data. On the
simultaneous event, true and fitted programs satisfy (4) for the same
Gibbs law in every sector. Equations (2), (5) and (6) then apply to those
data-selected fitted mobilities. Add the failure probability times the
actual oscillation for unconditional bounded expectations. Finite-sample
coverage is not posterior coverage for each rare realized data record.

This route is compatible with exact, finite-bit target ratios from the
preserved clock compiler. General real energy ratios need their actual
selector/rounding contract. Rounding a ratio breaks exact thermodynamic
preservation and cannot be charged only to the relative mobility error.

## 7. What an acquired equilibrium defect does not provide

The original closure defect measures an additive L2 norm of an omitted
conditional-response direction. It can be small because all visible
motion is slow. It can also be small because a serious defect lies on a
rare hidden sector. Neither fact bounds its magnitude relative to the
Dirichlet energy in every dissipative direction.

For example, a frozen fair hidden sign h with native flip probability
p_h=delta(1+h/2) has output-row residual norm delta/sqrt(2), tending to
zero. Yet its relative conductance deviation from the mean-rate model is
exactly 1/2. At about 1/(2delta) calls, a two-time visible correlation has
a nonzero limiting discrepancy. The explicit derivation is in the
counterexample file.

Even exact finite visible conductance averages determine only the
compressed form. They do not eliminate hidden memory or bound the full
off-diagonal form. A hidden conditional mixing/energy inequality, an
actual pointwise conditional relative-rate supplier, or a new acquired
relative certificate would be an additional physical result. This note
does not infer any of them from equilibrium weights or a finite sample.

## 8. Retained records and deployment

An arbitrary old record Z generally makes the conditional initial density
g_z different from one. A joint extension of (6) uses the actual average
of ||g_z-1||_2, or another proved joint estimate. Small unconditional local
error does not erase an old record which identifies a rare bad specimen.
Equation (7) is a useful special case with a finite initial readout; it
does not include an unrestricted global preparation/calibration transcript.

In the iid per-device supplier, confidence may be uniform conditional on
the fixed hidden vector, so correlation of calibration data with that
vector is allowed. The initial visible law still needs its declared
conditional contract. Calibration ending on the same interacting device
does not by itself prepare a fresh Gibbs law independent of its record.

No speedup, cold-start Gibbs sampler, practical experimental precision,
or new priority for the receiving theorem is claimed.
