# One retained bit can defeat uniform closure over changing path controllers

29 October 2026. Complementary ordinary construction for the root's bounded
Markov-force theorem. Independently reviewed at the exact source version saved
under reviewed_versions/, with review in physical_frontier/
ONE_BIT_CONTROLLER_INDEPENDENT_REVIEW.md. No instrument, path record, preparation or controller
has been acquired. The distinction is between the information used to prepare
a control bit and the size of the bit retained after that preparation.

## 1. Native source, known reporter, and exact scope

Fix a>0, A>=a, gamma,tau>0, an observation duration T0>0, actuation duration
h>0 and force ceiling B>0. The driving source is the stationary shear

    dx=v dt,       dv=-gamma v dt+sqrt(2 gamma tau)dW1,
    dy=w dt,       dw=[a sin(nx)-gamma w]dt+sqrt(2 gamma tau)dW2.  (1)

Positions are on the fixed 2pi torus. Its stationary physical entropy rate
sigma_n tends to zero as n grows, with the rate already proved in
THERMAL_STABILITY_DEPENDS_ON_OBSERVATIONAL_RESOLUTION.md. Dimension, bath,
mass, force amplitude and all times used below are fixed.

Adjoin a DECLARED independent free thermal reporter with angle ell and
momentum r:

    d ell=r dt,       dr=-gamma r dt+sqrt(2 gamma tau)dW3.        (2)

Its starting law is independent uniform angle times Maxwell N(0,tau), and
W3 is independent of the entire driving source. These are part of the
physical interface. The baseline candidate potentials are U(x,y), with
||grad U||<=A: they are NOT permitted to add a potential, coupling, hidden
force or different bath to the known free reporter. The explanation starts
from its own stationary Gibbs driving law times the SAME independent free
reporter law.

Thus the full baseline source has force (0,a sin(nx),0), and its entropy is
still sigma_n. Denote its driving path law on [0,T0] by P_n and a candidate
driving path law by Q_U. The theorem below concerns this explicitly restricted
native explanation class. It does not silently exclude reporter couplings
from an otherwise unrestricted three-dimensional potential class.

The acquisition interface supplies the exact driving trajectory on [0,T0]
to a causal decision processor. At T0 it prepares one bit b in {-1,+1}.
It discards the source record, retains b, and during (T0,T0+h] applies ONLY
the reporter force B b. There is no force on the original source. The same
decision rule and calibrated actuator are used under P_n and Q_U.

"One bit" means the retained state during this later actuation. It is NOT
a one-bit bound on the earlier path acquisition, analog accumulator,
temporary workspace, program description, sensor precision or computation.
An instantaneous decision at T0 is part of the mathematical policy contract;
no fixed-latency physical implementation is supplied.

## 2. Uniform full-path gap already available

The common path statistic is

    S_n=int_0^T0 a sin(nx_t) [dw_t+gamma w_t dt].             (3)

Its integrand has finite variation. Equivalently, without stochastic-integral
notation, it is the measurable continuous-path functional

    S_n=a sin(nx_T0) w_T0-a sin(nx_0) w_0
        -int_0^T0 a n cos(nx_t) v_t w_t dt
        +gamma int_0^T0 a sin(nx_t) w_t dt.                 (4)

The established native identities are

    E_P S_n=Delta=a^2 T0/2,       E_QU S_n=0,
    E_P S_n^2<=M_P=2a^4 T0^2+4 gamma tau a^2 T0,
    E_QU S_n^2<=M_Q=2a^2 A^2 T0^2+4 gamma tau a^2 T0.       (5)

The Gibbs mean vanishes because F_n is divergence free and
(-grad U) nu_U=tau grad nu_U. This uses the complete driving configuration,
the stated stationary preparations and the same native bath; it is not an
inference from a coarse visible fit.

Write

    C=M_P+M_Q=2a^2 T0[(a^2+A^2)T0+4 gamma tau],
    delta0=Delta^2/(2C)
           =a^2 T0/{16[(a^2+A^2)T0+4 gamma tau]}>0.         (6)

For any common statistic, its expectation gap squared is at most
2 TV(P,Q)(E_P S^2+E_Q S^2). Hence TV(P_n,Q_U)>=delta0 for every n,U.
This is the accepted finite-window shear separation at its actual scope.

## 3. Candidate-before-controller theorem

First choose ANY allowed candidate U, possibly depending on n. The positive
part of the signed measure P_n-Q_U supplies a measurable driving-path event
E_(n,U) such that

    P_n(E_(n,U))-Q_U(E_(n,U))=TV(P_n,Q_U)>=delta0.            (7)

Canonical finite-window continuous path space is standard Borel; a Hahn
decomposition suffices. For the smooth bounded native models, the equivalent
likelihood-ratio test is also available as an existence statement. No claim
is made that an arbitrary candidate's likelihood has been cheaply learned
or computed.

Set b=+1 on this event and b=-1 otherwise, and store only b after T0. This
is a deterministic causal history rule, selected AFTER U. It is generally
not a function of the current native state and time.

Because the event uses only the driving source, r(T0) remains N(0,tau)
independent of b. Brownian reporter increments after T0 are independent too.
Writing

    m=(B/gamma)(1-exp(-gamma h))>0,

the exact conditional endpoint law is

    r(T0+h) | b  ~ N(m b,tau).                            (8)

Use the FIXED final readout

    Y=1{r(T0+h)+eta Z>=0},       eta>0, Z~N(0,1),           (9)

where Z is a known independent readout noise. This has one binary reported
outcome and a fixed nonzero precision floor, independent of n,U and the
chosen test. Put

    beta=2 Phi(m/sqrt(tau+eta^2))-1>0.                     (10)

If p and q are the probabilities that b=+1 under source and explanation,
then direct Gaussian integration gives EXACTLY

    TV(Law_P Y,Law_Q Y)=beta |p-q|.                       (11)

The same identity holds for the full noisy real readout, since the difference
of the two Gaussian shift densities changes sign at zero. Thus the coarse
binary readout loses none of their mixture-weight TV discrepancy.

Let C_1 denote these exact-history-acquisition, one-retained-bit controllers
with the reporter force cap B. On the fixed total horizon T0+h,

    inf_(U:||grad U||<=A) sup_(controller in C_1)
       TV(Law_source Y,Law_explanation Y) >= beta delta0.   (12)

This is the requested order: ONE candidate is chosen first; its separating
controller is then chosen and used unchanged in both experiments. Since
sigma_n->0, the right side disproves the corresponding uniform extension
of the bounded Markov-force theorem to this history-controller interface.
Equation (12) does not assert a single deterministic driving-record test
that separates every candidate simultaneously. Section 5 gives a stronger
uniform test when a declared independent random threshold is admitted.

The readout in (9) is a fixed uniformly TV-Lipschitz kernel of the physical
path. The test function r->Phi(r/eta) has range [0,1] and Lipschitz constant
1/(eta sqrt(2pi)). For the bounded uniform path metric d=1 wedge d_infinity,
its norm is bounded by L=max(1,1/(eta sqrt(2pi))). Consequently the same
construction gives a physical path d_BL separation at least beta delta0/L.
The effect is therefore a macroscopic controlled-path discrepancy, not only
an exact command trace being reported.

## 4. An explicit deterministic bit for the free candidate

For U=constant there is no need to invoke a general existence test. Let

    V_n=int_0^T0 a^2 sin^2(nx_t)dt.

The driver has the same free law in source and comparator. Conditional on
its entire x path, the receiver innovation Brownian motion is independent,
so

    S_n | x path ~ N(V_n,2 gamma tau V_n) under P_n,
    S_n | x path ~ N(0,2 gamma tau V_n) under Q_0.          (13)

The stationary source's receiver starting correlations do not alter (13):
the combination dw+gamma w dt removes its homogeneous initial term, and
future receiver Brownian noise is independent of the driver. V_n>0 almost
surely, since uniform x_0 avoids the force zeros almost surely and paths are
continuous.

The EXPLICIT acquisition rule b=sign(S_n) therefore satisfies

    Q_0(b=+1)=1/2,
    P_n(b=+1)-1/2
          =E[Phi(sqrt(V_n/(2 gamma tau)))-1/2].            (14)

Moreover 0<=V_n<=a^2 T0 and E V_n=a^2 T0/2, whence
P(V_n>=a^2 T0/4)>=1/3. The bit gap is at least

    delta_free=(1/3)[Phi(a sqrt(T0)/(2 sqrt(2 gamma tau)))-1/2]>0, (15)

uniformly in n. The reporter output gap is at least beta delta_free.
The stronger conditional midpoint test S_n>V_n/2 is another conventional
option, but is not needed for the counterexample.

## 5. Stronger optional result: one randomized test works for all candidates

The universal score in (5) permits a constructive rule independent of U.
Let M=C/(2Delta)>0 and define

    g(s)=1/2+clip(s,-M,M)/(2M).

For every real s,

    |s-clip(s,-M,M)|<=(s^2)/(4M),                         (16)

because for |s|>=M this is equivalent to (|s|-2M)^2>=0. Thus (5) gives

    E_P clip(S_n)-E_QU clip(S_n)>=Delta-C/(4M)=Delta/2,
    E_P g(S_n)-E_QU g(S_n)>=Delta/(4M)=delta0.             (17)

Acquire an independent R uniform on [0,1], and prepare b=+1 iff
R<=g(S_n). The SAME rule now has the bit gap delta0 against EVERY allowed
candidate U. It is causal and retains just b during reporter actuation.
For this explicitly enlarged randomized controller class, the stronger
sup_controller inf_U order is positive too. No such order was assumed in
the deterministic existence argument of Section 3.

The continuous random variable is unnecessary. With K equally likely
midpoint thresholds and K>=4/delta0, the rounding of g changes either bit
probability by at most 1/K. The common rule retains a gap at least delta0/2.
K can be a power of two; the finite random bits used during acquisition
are an additional fixed resource, not counted as one retained bit.

The DECLARED reporter itself can supply this optional randomizer: its
uniform angle ell(T0) is independent of its ENTIRE free momentum history
and of the driving system. This follows by conditioning on all momenta and
using the independent uniform starting angle. A fixed K-bin readout of
ell(T0) is therefore a uniform integer independent of r(T0) and S_n.
Using that integer for the midpoint threshold preserves (8)--(11). This
version is a deterministic rule of the full acquired record, but it charges
an additional coarse reporter-angle readout. It is not a driving-record-only
deterministic test. No new thermal randomness is assumed beyond the stated
free reporter preparation.

## 6. Acquisition precision is not supplied by the retained bit

The key input is S_n, not its eventual one-bit encoding. Formula (4) resolves
the force phase and integrates a term containing a n cos(nx). It changes with
n and has no uniform sensitivity bound as n grows. It cannot be acquired
from the fixed finite-resolution source transcripts whose TV already tends
to zero. Any bit computed from such a transcript has vanishing TV by data
processing; passing it through the reporter gives at most beta times that
vanishing discrepancy.

For an explicit sufficient precision accounting, suppose true and acquired
continuous paths both have |v|,|w|<=P, position error at most epsilon_x,
and each momentum error at most epsilon_p, uniformly on [0,T0]. Evaluate
(4) on both paths. Elementary product bounds yield

    |S_n-Shat_n|
       <=a[n P(2+gamma T0)+n^2 P^2 T0] epsilon_x
         +a[2+gamma T0+2n P T0] epsilon_p.                (18)

This is a conservative SUFFICIENT error budget, not an optimal acquisition
lower bound. It exhibits the missing resolution directly: for bounded P,
epsilon_x=O(n^-2) and epsilon_p=O(n^-1) suffice for a fixed score error by
this representation. Direct force-feature instrumentation or a different
integrator may have different costs; neither is supplied automatically.
Finite-time sampling/interpolation and numerical quadrature errors must
also be included in the warranted score error. No universal time-grid cost
is inferred from a continuous-record assumption.

Uniform momentum-tail estimates from the existing bounded-force theorem
can choose P at any specified confidence, independent of n and U. They do
not certify the instrument errors. If |Shat-S|<=epsilon except on an event
of probability at most zeta under each hypothesis, the randomized rule in
Section 5 retains a bit gap at least

    delta0-epsilon/M-2zeta.                              (19)

Finite threshold discretization adds at most 2/K to the loss. This follows
from g being 1/(2M)-Lipschitz and bounded by one. It supplies a concrete
robustness target for acquisition without pretending that the required
precision, bandwidth or computation time has been acquired.

There is also an actual necessary budget at the earlier Gaussian POSITION
sensor interface. Suppose the acquisition consists of adaptive position
feature queries with actual Lipschitz constants L_i and independent Gaussian
noise standard deviations eta_i, with a pathwise budget
J>=sum_i L_i^2/eta_i^2. Query times, settings and stops must be functions
of preceding CHARGED reports and independent randomization. Exact-path-triggered
timestamps or any other uncharged side channel are excluded. The stationary
shear/free coupling and the proved
adaptive-position transcript bound give

    TV(source acquisition,free acquisition)
          <=(T0/2) sqrt[(tau sigma_n/gamma) J].            (20)

Any computed bit, including independent randomization, has no larger TV.
Obtaining a bit gap d>0 therefore requires

    J>=4 gamma d^2/(tau T0^2 sigma_n)=Omega(n).           (21)

This is a lower bound for THAT specified sensor interface, not for arbitrary
force-feature, momentum or microscopic measurements. It attaches a genuine
acquisition cost to the otherwise one-bit controller. The position-sensor
theorem allows adaptive query times because it uses a position supremum
coupling; no unsupported adaptive point-momentum variance claim is used.

The general likelihood event of Section 3 can require a candidate-specific
description and substantial computation. Section 5 avoids candidate-specific
likelihood evaluation using the known native force and ceiling A; it still
requires the score acquisition. Ordinary likelihood testing, force inference
and noisy actuation can perform exactly these same operations with the same
information. No speed advantage over that equally informed route is claimed.

## 7. Work, preparation, and why this is not a thermodynamic paradox

The reporter is driven by external work. Conditional on either value of b,
its mean momentum after elapsed time s is (B b/gamma)(1-exp(-gamma s)).
Therefore its expected actuation work is the fixed positive amount

    W_reporter=(B^2/gamma)[h-(1-exp(-gamma h))/gamma].      (22)

This is the same under every hypothesis and every bit probability. Its
mean kinetic-energy increase is m^2/2, and its mean dissipated heat during
actuation is W_reporter-m^2/2=gamma int_0^h
[(B/gamma)(1-exp(-gamma s))]^2 ds>=0. No vanishing-entropy claim is made
for the controlled apparatus or the post-acquisition experiment.

Costs include the warranted independent free reporter preparation, the
high-resolution source record, the chosen test computation, preparation and
retention of b, the bounded-force actuator, duration h, and the fixed-noise
readout. Resetting the reporter/controller for another trial has its own
preparation and erasure requirements. The proof neither executes nor prices
that reset. Low entropy concerns the UNCONTROLLED shear baseline only.

Equation (11) actually CONTRACTS input statistical TV by beta<1. The
controller transfers fine-path information into a coarse macroscopic channel;
it does not create information or entropy from nothing. Adjoining b to make
the later dynamics Markov does not restore the original theorem's premises:
the bit has a source-dependent acquired law and is not a native Gibbs degree
of freedom with the specified kinetic bath. A fixed number of retained
states is not a replacement for a preparation/observation contract.

## 8. Scope of the result

This is a sharp boundary to the claimed UNIFORM extension over changing
history-dependent policies. The source-dependent tests vary with n. It does
not refute the fixed-controller argument, the bounded memoryless Markov-force
theorem, or finite-resolution closure for a fixed acquisition interface.
The root's complementary FIXED_SENSOR_FINITE_MEMORY_CONTROL.md constructs
a positive finite-memory closure for a fixed finite schedule/catalog of
finite-alphabet sensor kernels, uniformly over the bounded Markov force
fields on every report-history branch. That theorem permits retained memory;
its proof keeps the sensor identities in the common joint limiting law.
The present controller changes its acquisition kernel with n even though it
retains only one bit. Thus neither "memoryless" nor the number of retained
states is the general criterion. The actual acquisition interface is the
relevant distinction. The new positive theorem is cross-linked as a separate
root construction, not assumed as a premise in this counterexample.

The independent reporter restriction is essential to the proof as stated.
Allowing candidate potentials to couple the reporter, weakening its starting
independence, or observing only a coarse driving record changes the experiment
and needs a different argument.

The mathematical addition is an explicit native realization of the boundary:
vanishing baseline entropy and uniformly valid bounded-Markov equilibrium
closure coexist with a fixed output discrepancy after a one-retained-bit
causal operation supplied with finer information. One-bit storage does not
bound the precision or physical information used to prepare the bit.
The ingredients are ordinary testing, bounded-score randomization and a
linear thermal reporter; no historical novelty or acquired device is claimed.

### Pinned proof inputs

- BOUNDED_MARKOV_FORCE_INTERVENTIONS.md, SHA256
  db1dcfba5eda825e3ba6465736072bc2e0761681c95ef732d6fc2c24075a24ca.
- THERMAL_STABILITY_DEPENDS_ON_OBSERVATIONAL_RESOLUTION.md, SHA256
  2256d2f72b58d5bd7b77faf9a26c26deb08fecaf822c038a0af401b69c6d7f30.
- BOUNDED_FORCE_FINITE_RESOLUTION_EQUILIBRIUM.md, SHA256
  2bd8c75a5e1371b39b7ed346b10fb75810d5387012744888d7aa2b0730f8050f.

This note independently reconstructs the new controller/transduction proof.
The earlier accepted native shear and closure results are reused at their
stated scope; their numerical/physical acquisition is not asserted. No
additional literature or archive retrieval was needed for this challenge.
