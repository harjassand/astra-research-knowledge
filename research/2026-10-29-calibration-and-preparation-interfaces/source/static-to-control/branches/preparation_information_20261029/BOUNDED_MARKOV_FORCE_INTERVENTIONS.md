# One equilibrium explanation under an entire bounded Markov force interface

29 October 2026. Root continuation of BOUNDED_FORCE_FINITE_RESOLUTION_EQUILIBRIUM.md.
This is a new intervention theorem, not an inference from the passive-record
corollary. The proof identifies the controlled native limit. Its complete
ordinary proof was independently reviewed in physical_frontier/
MARKOV_INTERVENTION_CLOSURE_INDEPENDENT_PROOF.md; the exact reviewed version
is preserved under reviewed_versions/. STATIC_INFORMATION_TO_CONTROL.md
develops the additional static-information model-selection consequence.

## 1. Consequence and quantifiers

Keep the baseline source class, physical entropy sigma(F), force ceiling A,
fixed torus dimension/size, masses, bath gamma,tau and stationary law rho_F
from the bounded-force closure theorem. Fix T<infinity and a finite B.

An admitted intervention is a deterministic Borel Markov force

    u:[0,T] x (T^d x R^d)->R^d,  |u(t,q,p)|<=B.           (1)

It acts in the momentum equation, in the SAME noisy force directions:

    dq=p dt,
    dp=[F(q)+u(t,q,p)-gamma p]dt+sqrt(2gamma tau)dW.       (2)

This includes prescribed time-position fields and bounded memoryless state
feedback. Ability to sense/configure/execute a selected u is a physical
interface, not granted by the formula. The comparison permits the SAME
calibrated u in source and equilibrium explanation.

Start the source at its baseline stationary rho_F; start an equilibrium
explanation at its baseline Gibbs law mu_U. Controlled experiments need not
be stationary or dissipate little heat. Only sigma(F) of the UNCONTROLLED
source is constrained.

With d_BL from the preceding theorem, define

    D_(B,T)(F,U)=sup_(|u|<=B)
                        d_BL(P_F;u^rho_F,P_-gradU;u^mu_U). (3)

Then

    sup_(F smooth, ||F||<=A, sigma(F)<=s)
        inf_(U smooth periodic, ||grad U||<=A) D_(B,T)(F,U)
                                      ->0 as s->0.       (4)

ONE Gibbs potential works uniformly over the whole bounded Markov force
class on the specified finite window. It is not a different fitted potential
for each intervention. Neither source nor feedback derivatives need a
uniform cap. Small baseline entropy does not bound the work or total
entropy of the later controlled experiment.

The same statement holds in every finite Wasserstein order for the
unbounded uniform physical path metric. It also holds in output TV for
a fixed countable-output or bounded-density observation kernel K; uniformly
TV-Lipschitz record families inherit a common bound from d_BL.

Exact state-dependent command values u(t,Z_t), if reported, are additional
readouts. A control amplitude ceiling does NOT bound their sensitivity/noise.
The output-TV claims require fixed K or uniformly bounded observation
resolution, INCLUDING any command channel. Arbitrary varying history-
dependent controllers with unspecified memory are outside (4).

## 2. Compact occupation on time and FULL phase space

Let mu_0=uniform_position x Maxwell and P_0 its stationary free Kramers law.
For every fixed bounded measurable g(t,q,p), the operator

    A_g:L2([0,T] x mu_0)->L2(P_0),
    A_g f=int_0^T f(t,Z_t)g(t,Z_t)dt                     (5)

is compact.

For h>0 write r=exp(-gamma h). The free velocity-pair Mehler kernel m_r
relative to Maxwell x Maxwell satisfies, by direct Gaussian integration,

    int m_r(p,p')^2 M(dp)M(dp')=(1-r^2)^(-d).             (6)

In one normalized coordinate the squared-kernel Gaussian precision matrix
has determinant one and prefactor (1-r^2)^(-1); dimensions multiply.

Conditional on endpoint momenta p,p', the lifted position displacement
has mean [(1-r)/(gamma(1+r))](p+p') and covariance

    c_bridge(h) I,
    c_bridge(h)=(2tau/gamma^2)
                       [gamma h-2tanh(gamma h/2)]>0.    (7)

This is a joint-Gaussian Schur complement. The bracket is zero at h=0 and
has positive derivative tanh^2(s/2) in s=gamma h. Its small-h covariance
is tau gamma h^3/6. The wrapped displacement kernel has finite maximum
C_h independent of the endpoint momenta.

The free FULL-state pair density k_h relative to mu_0 x mu_0 therefore has

    ||k_h||_L2(mu0 x mu0)^2
                  <=C_h^2(1-exp(-2gamma h))^(-d),         (8)

uniformly finite for h in [epsilon,T]. This is actual noise smoothing,
not a hidden Markov closure assumption.

Write A_g* A_g as a double time integral. On |s-t|>=epsilon, (8) gives a
Hilbert--Schmidt kernel on ([0,T] x phase_space)^2. On |s-t|<epsilon,
stationarity and Cauchy--Schwarz bound each integrand by

    ||g||_infinity^2 ||f(s,.)||_2 ||h(t,.)||_2.

Young's L2 convolution inequality gives diagonal-strip operator norm
at most 2epsilon ||g||_infinity^2. Hence A_g* A_g is an operator-norm
limit of compact operators, so A_g is compact. Weak L2 convergence of
time-state force fields gives strong L2 convergence of their fixed-test
occupation integrals.

## 3. A native limit with moving intervention fields

For any baseline sequence sigma(F_j)->0, the preceding proof supplies a
subsequence, a periodic Lipschitz U, F=-grad U and rho=mu_U, with

    F_j weak-* ->F,
    TV(rho_j,r_j mu_0)->0,
    r_j uniformly L2 and weakly ->d rho/d mu_0.           (9)

The r_j are the mathematical one-step smoothing construction, not a reset.
For ANY sequence u_j satisfying (1), weak-* compactness on finite measure
dt mu_0 supplies a subsequence u_j ->u with |u|<=B. Both F_j(q) and u_j
then converge weakly in L2(dt mu_0), and their sum tends weakly to F+u.

Controlled-path likelihoods from r_j mu_0 relative to the common free law
have the uniform bound

    ||R_j||_2^2
       <=exp[(A+B)^2 T/(2gamma tau)] ||r_j||_2^2.         (10)

A weak L2 limit is a normalized positive density and supplies SETWISE
path convergence. In the martingale identity the moving term is

    int_s^t [F_j+u_j-F-u](a,Z_a) dot grad_p phi(Z_a)da.

The lemma (5) makes this tend to zero in L2(P_0). Cauchy--Schwarz and (10)
handle a bounded past test. All remaining terms are fixed bounded measurable
functionals, so they pass to the weak L2 limit.

The limit solves native Kramers dynamics with time-state force F+u.
This bounded Borel drift lies in the noisy momentum range. Forward and
inverse Girsanov against free Kramers motion give uniqueness in law.
Thus the limit is exactly P_F;u^rho, with no additional controller memory.

Initial TV in (9) propagates through each controlled kernel, uniformly
in u_j. The same conclusion therefore holds for actual rho_j starts.
This handles moving interventions; it does not call intervention
postprocessing of an uncontrolled path.

## 4. One explanation works uniformly over interventions

Choose smooth periodic mollifications U_j of the Lipschitz U such that

    U_j ->U uniformly, grad U_j ->grad U strongly in L2(position),
    ||grad U_j||<=A, dmu_Uj/dmu_0 ->dmu_U/dmu_0 in L2(mu_0).             (11)

For the SAME arbitrary u_j, the explanation's controlled force
-grad U_j+u_j converges weakly in L2(dt mu_0) to F+u. Its initial densities
are uniformly L2. Section 3 therefore makes its path law converge setwise
to exactly the SAME native P_F;u^rho. Both path sequences converge weakly
to this common limit, so

    d_BL(P_Fj;uj^rho_j,P_-gradUj;uj^mu_Uj)->0.             (12)

If (4) failed, some low-entropy sequence would stay separated by epsilon
after infimizing over every Gibbs U. Choose (9) and the single U_j from
(11). For each j select a bounded u_j with discrepancy >=epsilon/2.
Weak-* extract those controls and apply (12), a contradiction. This proves
the order inf_U sup_u. A hidden reset, model fit or rank closure is not
substituted into the proof.

For fixed countable-output K, the same two controlled sequences converge
setwise to one law. Every output probability therefore converges to the
same value, and discrete Scheffe gives output TV convergence. For fixed
k(z|omega) bounded in omega at almost every z, apply setwise convergence
pointwise in z and then Scheffe. The same contradiction proves the uniform
control statement for those records. Uniformly TV-Lipschitz sensor families
follow directly from d_BL.

## 5. Finite-window unbounded consequences

Baseline stationary moment bounds are proved in
physical_frontier/BOUNDED_FORCE_WASSERSTEIN_UPGRADE.md. During interventions
the mild equation has force magnitude at most A+B. For r>1,

    ||sup_(t<=T)|p_t|||_Lr
       <=(2A+B)/gamma+sqrt(tau)c_(d,r)
           +2sqrt(2gamma tau T)[r/(r-1)]c_(d,r),          (13)

where c_(d,r)=(E|N(0,I_d)|^r)^(1/r). The initial A/gamma contribution
comes from the baseline stationary state; the subsequent force integral
is bounded by (A+B)/gamma. Brownian maximal bounds give the last term.
Every Gibbs explanation obeys the same bound. Adding the torus diameter
supplies a uniform high moment for distance from a fixed reference path.

The moment/coupling interpolation in the Wasserstein note upgrades (4)
uniformly over u to every finite W_p. The SAME BL-selected U_j works for
all fixed finite p. Finite-window displacement, momentum maxima and
uniformly polynomial-sensitive kinetic-energy expectations are controlled.
There is no interchange with an integral over all future hitting times.

## 6. Information, cost and strongest conventional route

This is an existence/stability principle. Within the declared native class,
small baseline heat cannot hide a finite-window macroscopic response that
stays separated from EVERY equilibrium explanation under the bounded
Markov force interface. One explanation is chosen for the whole interface.

It is NOT identification from a coarse baseline record. There is no acquired
U, effective entropy-to-error modulus, calibrated controller, physical
preparation or full-task speedup. Correct physical reversal, bath, finite
dimension, bounded force, baseline preparation and noise-range access
remain substantive. The paired finite-family heat record and the relational
actuator-frame record are separate constructive acquisition results at
their narrower source/observation interfaces.

History-dependent controllers require their actual internal state, memory,
observation and reset contracts. The weak-* compactness used here concerns
functions of CURRENT physical state and time; it does not identify the
limit of an arbitrary varying controller that processes an exact path.
Reported command values must also respect the stated readout contract.
An amplitude bound alone is not an information bound on a controller.

Kinetic SDE stability, Girsanov and force matching are established methods.
An equally informed conventional equilibrium model can adopt this conclusion
and solve its controlled dynamics by ordinary means. The candidate scientific addition
is the native low-entropy closure with its UNIFORM infimum/
supremum order over interventions, and the explicit boundary between Markov
actuation, controller memory and measurement resolution. Priority remains
unresolved.

