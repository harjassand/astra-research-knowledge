# Interaction-assisted boundary discovery: genuine extra information, exact residual blindness

29 October 2026. Private ordinary proof/code. Mathematical model construction and
exact algebra checks, not laboratory acquisition, a new universal inverse theorem,
novelty clearance, or independent acceptance of any Astra claim.

## Result and selection decision

**Natural hard-core exclusion does break the saved exact single-particle
similarity family.** Two particles on the saved four physical sites have a
six-state exclusion generator whose boundary-occupancy response separates every
nonzero allowed r from r=0. A finite-rate two-token source at the same boundary
retains the separation, without instantaneous interior reset. A nonzero exact
Jacobian determinant establishes generic LOCAL identifiability of six hidden
rates in that known four-site topology. Uniform contact also separates this pair.

**This does not support universal or uniformly stable scalable discovery.** A
five-site counterexample with a degree-one physical boundary remains exactly
indistinguishable under hard-core exclusion at EVERY particle number, arbitrary
boundary injection/extraction, and nonanticipating boundary feedback. A related
uniform-contact counterexample remains indistinguishable with two labeled
replicas, even if reaction events are also reported. In both, internal entropy
production ranges from zero to infinity while rates stay bounded and the
one-particle stationary distribution stays uniform. The mechanism is an explicit
controlled lumping, not insufficient samples or an untested similarity guess.

The proposed bulk operations are physically different from a supplied arbitrary
coordinatewise nonlinearity: real particles can inherently block or react when
co-located without naming hidden sites. But that only applies when CTMC states
are genuine occupiable physical sites and the hopping/interaction law is
independently warranted. It does not apply automatically to arbitrary hidden
conformations, mesostates or mathematical realizations. No qualifying apparatus
has been acquired. Existing nonlinear inverse-boundary and interacting-walk
methods already use interaction-generated inverse information.

**Decision: retain the new explicit operational tests and counterexamples; reject
this branch as a demonstrated broad Astra flagship.** No rate fitting, paper,
upload, external publication, or instrument claim was performed.

## 1. Exact physical operation

Let Q be a row generator on physical sites V. For k indistinguishable classical
hard-core particles, states are subsets Z of V with |Z|=k. Define

    L_k(Z, Z\{i} union {j}) = q_ij,     i in Z, j not in Z,
    L_k(Z,Z) = -sum_(i in Z,j not in Z) q_ij.                 (1)

A hop to an occupied site is rejected; unblocked hopping rates are unchanged.
Observation is ONLY n_0=1_{0 in Z} at the same gateway 0. Particles may be injected
or collected at 0 using counted local source/sink events. Site labels, interior
occupancy and L_k are not given to a learner. Equation (1) specifies the forward
physical model, not a hidden-generator oracle.

This is a meaningful extra operation only if occupancy exclusion is a real
bulk law. Electrostatic interactions, density-dependent barriers, different
particle species, or site capacities can invalidate (1). Identifying an arbitrary
latent Markov state with a one-particle site would assume the missing capability.

### Not a free-fermion exterior-power argument

For independent walkers, the generator Q tensor I + I tensor Q transforms by
S tensor S under one-particle similarity. Linear exterior-power propagators are
also functorial under similarity. With correspondingly lifted access, a new
particle count alone need not break an old gauge. Pauli statistics alone is not
a proof of new inverse information.

Classical stochastic exclusion (1) has a different diagonal: it removes blocked
hops from the total exit rate so rows still sum to zero. An exterior-power
one-particle generator retains different diagonal/sign structure and is not
this conservative Markov process. The computation here uses (1), not an
antisymmetric lifted single-particle propagator.

## 2. Constructing the actual saved pair

Read ../foundational_hidden_gate_20261029/PROOF.md and experiment.py. The gateway
0 connects only to site 1, q_01=q_10=1. The internal generator is

    K_0 = [ -3   1   2 ]
          [  1  -4   3 ]
          [  2   3  -5 ],

    S_r = [ 1   0     0 ]
          [ 0  1+r   -r ]
          [ 0   0     1 ],

    K_r = S_r^-1 K_0 S_r,
    Q_r = [ -1       e_1^T ]
          [ e_1   K_r-e_1e_1^T ].                         (2)

Here 0<=r<r_*=(sqrt(37)-1)/6. All hidden offdiagonal rates are positive.
The saved proof establishes equality of every one-particle binary boundary law
under arbitrary independent entry/exit controls, including feedback, not just
finite scalar tests. Hidden dissipation nevertheless diverges as r increases to
r_*.

Construct (1) on the ordered pair states

    01, 02, 03, 12, 13, 23.

The entire exact symbolic six-by-six L_r is saved in
symbolic_pair_results.json. For a=e_01^T and b_Z=1_{0 in Z}, define

    h_r(t) = a exp(t L_r) b.

Direct exact multiplication gives

    h_r^(j)(0)-h_0^(j)(0) = 0,                 j=0,1,2,3,
    h_r^(4)(0)-h_0^(4)(0) = 2 r(r-1).                    (3)

Thus the original gauge family is not an exclusion equivalence: the analytic
boundary laws differ for every 0<r<r_*<1. At r=1/10 and t=1, the floating values
are h_0=0.7080789303363126 and h_r=0.7078035242386006. This numeric value is not the
proof; (3) is exact.

The fourth derivative alone is symmetric under r versus 1-r. That is NOT an
entire-law counterexample. Exact calculation gives

    h_r^(5)(0)-h_(1-r)^(5)(0) = 23(2r-1).                (4)

For r=1/5 and 4/5 (both allowed), this is -69/5. These are explicit moment/Hankel
word witnesses: they already rule out any all-record controlled equivalence for
these pairs. They are not an assertion that every unknown six-rate model has
been globally identified.

## 3. A finite boundary source, no instantaneous hidden preparation

The ideal state 01 can be approached by inserting the second particle immediately
after the first leaves 0. It is NOT granted as a free primitive. A delay ell
permits the first particle to move again with probability at most Lambda ell,
if a true total-exit bound Lambda is warranted. Source failure, missed events and
latency would enter the initial-state TV error and hence any bounded report.
Without a rate bound and source timing budget, this event-triggered preparation
is unqualified.

The actual second computation therefore avoids it. Start from a cleared specimen
and a boundary source with exactly TWO tokens. While a token remains and 0 is
empty, the source injects at finite rate alpha=1. It stops after the second
counted successful delivery. There is no extraction during the observation
window and particles are conserved. Hence "at most two particles" is maintained
by the known source inventory, NOT by measuring hidden total occupancy.

The augmented configurations are empty, four singletons and six pairs: eleven
states. Internal transitions obey (1), source injection adds 0, and the boundary
observable remains n_0. Every source event and the two-token inventory are local.
Reset requires collecting the known delivered number of particles through 0;
its time, detector error and finite completion probability are real costs. A
source run is not assumed to reset arbitrary unknown pre-existing contamination.

For r=1/10 versus 0, the first unequal derivative of this finite-source boundary
probability is order SEVEN, exactly -9/25. For r=1/5 versus 4/5 it is order EIGHT,
exactly -171/5. At fixed t=8 the r=1/10 versus 0 gap is about 1.5768673e-4. Thus a
strictly boundary-local finite-rate acquisition really does retain extra
information; the pair-state calculation did not depend essentially on an
instantaneous hidden reset.

## 4. Limited generic information and adverse cost

For the known four-site topology, take all six directed internal rates

    theta=(q_12,q_13,q_21,q_23,q_31,q_32)

as unknown. At theta=(1,2,1,3,2,3), the exact Jacobian of finite-source moments
h^(4)(0),...,h^(9)(0) has determinant 65586. With a ONE-token source the moment
Jacobian has rank four instead. Code differentiates the stated forward generator;
it does not pass those derivatives to an inverse receiver or fit unknown rates.

Since moment derivatives are polynomial in the rates, the nonzero determinant
proves generic local structural identifiability in this specified six-parameter
class. This is not a finite-size numerical rank guess. It is not global
identifiability, an order-discovery theorem, a result for arbitrary networks, or
a stable reconstruction algorithm.

It also implies that some finite scalar probability settings have a nonsingular
Jacobian: put t_j=epsilon z_j at six distinct positive z_j. The leading determinant
is a nonzero Vandermonde-type determinant times 65586 and

    epsilon^(4+5+6+7+8+9) / (4!5!6!7!8!9!).

Thus derivative measurements need not be supplied as an oracle. But the
confluent limit is catastrophically ill-conditioned, not free information.
For the explicitly fixed times [.1,.2,.5,1,2,4], a floating Frechet-derivative
check gives two-token sigma_min about 2.81e-10 and condition number 2.69e8.
Those are source-local diagnostics, not outward-rounded certification. The
one-token Jacobian has the two expected zero directions (floating residuals
below 1e-17).

For one unknown instrument promised to be one of the saved two known hypotheses,
a simple Hoeffding threshold at t=8 has 95% error control using the sufficient
bound 2 log(40)/gap^2, about 296,711,349 independent trials. This is NOT a necessary
sample count, NOT optimized experimental design, and NOT an actual trajectory
simulation. Every trial additionally pays source, observation and reset time.
Equally informed likelihood fitting or active design receives the same physical
operations; no cost advantage over it is established.

## 5. Exact all-particle exclusion counterexample behind a degree-one gateway

Use sites {0,1} union M, with |M|=m>=3. The observed gateway 0 has ONLY neighbor 1.
Let q_01=A(t), q_10=B(t). Attach 1 uniformly to all sites i in M:

    q_1i=a,       q_i1=c,

and allow ANY internal generator K on M. Boundary source/sink controls alpha(t),
beta(t) add/remove a particle at site 0 when permitted. No interior control or
observation is needed or granted.

For every hard-core configuration define

    z=(n_0,n_1,k_M),     k_M=sum_(i in M) n_i.

The rates of transitions of z are

    0->1 edge:     A n_0(1-n_1),
    1->0 edge:     B n_1(1-n_0),
    1->module:    a n_1(m-k_M),
    module->1:    c (1-n_1) k_M,
    source:       alpha(1-n_0),
    sink:         beta n_0.                                      (5)

Internal K moves preserve z. Therefore z is strongly lumpable for EVERY K.
All rates in (5) are independent of K. If P is the configuration-to-z indicator
matrix, the exact identity is

    L_K(A,B,alpha,beta) P = P Lbar(A,B,alpha,beta).          (6)

Boundary observations and source/sink marks are functions/transitions of this
same quotient. Any matched quotient initial law gives identical complete
boundary records. Piecewise controls follow from exponentiating (6); time-varying
controls follow from the controlled finite-state equation. Under common
nonanticipating feedback, conditional future controls are the same until the
same boundary history changes, so the law equality persists. This is an
all-record/all-control proof, not agreement of sampled words.

The check uses m=3, all 32 configurations (EVERY particle number), a=c=1 and
symbolic A,B,alpha,beta,u,v. It verifies (6) onto 16 quotient states and verifies
that the quotient does not depend on u or v. Thus even unlimited density variation
and a physical degree-one boundary do not remove this obstruction.

Choose K to be a directed cycle on M with clockwise rate u and counterclockwise
rate v. At A=B=a=c=1, its full one-particle stationary law is uniform on five
sites. Its entropy production is

    sigma_1 = (3/5)(u-v) log(u/v).                         (7)

Take u=2-epsilon and v=epsilon, 0<epsilon<=1. At epsilon=1 this is equilibrium;
as epsilon decreases to zero, sigma_1 diverges. All baseline individual jump rates stay <=2,
stationary masses stay 1/5, and total module-site jump activity stays 3.
Every controlled exclusion boundary law remains identical.

At fixed particle number k, the stationary law is uniform over k-subsets because
the full one-particle rates are balanced. Its entropy production is

    sigma_k = [3k(5-k)/20](u-v) log(u/v),      1<=k<=4.    (8)

The combinatorial factor is the stationary probability of occupied i and vacant
j. Thus this is not merely a hidden one-particle thermodynamic label: dissipation
of the actual interacting system also diverges while its boundary data agree.

## 6. Uniform contact: a different operation, another exact residual quotient

For two independently hopping labeled particles at physical positions x,y, add
an intrinsic uniform contact reaction at rate kappa whenever x=y. For specificity
both disappear upon reaction. The pair generator before reaction is

    C = Q tensor I + I tensor Q - kappa diag(1_{x=y}),     (9)

with a dead state receiving each killing transition. The receiver need not know
the coordinate matrix in (9); it is a mathematical description of physically
co-located particles reacting with a uniform calibrated rate. That calibration,
reaction product handling and preservation of single-particle hopping remain
premises, not consequences of a boundary fit.

On the SAVED four-site pair, preparing both particles at accessible site 0 and
using kappa=1 gives a boundary mean-count first difference of order seven,
138/25 at r=1/10 versus 0. This allows double occupancy at the boundary and is a
different physical model from hard core. It is not used to bypass the finite-rate
exclusion-source accounting. Exact values are in contact_results.json.

For the FIVE-site uniform-module example, retain both outside positions when
outside M, and when both particles are in the cycle retain only

    d = y-x modulo m.

When both are inside, d jumps +1 at rate u+v and -1 at rate u+v: either particle's
motion contributes, and common directional circulation cancels. Exit rates to
site 1 are uniform. Entry from 1 is uniform over M, hence distributes d uniformly.
When only one particle is inside, its absolute position is irrelevant. Contact
occurs at rate kappa precisely at d=0, or when the two outside positions coincide.
Consequently the entire quotient depends on u and v only through u+v.

The producer code verifies an exact 26-to-12-state controlled quotient, including
an explicitly observed death state. The separate review strengthens it to a
36-state process with independently injected/removed labeled particles and
independent A_1,B_1,A_2,B_2 boundary-edge controls; its 18-state quotient also
preserves separately counted contact-reaction marks. Thus even reporting
reaction events, in addition to the original boundary records, does not identify
u-v when the internal motion of the two replicas is identical. All boundary
source timing/feedback stays within the quotient.

With u+v=2, the family in (7) again ranges from zero to unbounded hidden entropy
while having exactly equal two-replica contact data. Independently changing one
replica's BULK hopping or circulation would be a different operation and could
break this argument; it is not boundary control and is not granted here.

## 7. Near-lumpable systems: generic uniqueness cannot imply uniform cost

The exact counterexamples occupy a structured class; they do not by themselves
disprove a generic uniqueness theorem on a different qualified class. They DO
forbid universal reconstruction, and nearby examples obstruct uniform stability.

For the five-site module, perturb the six connector/module rates by at most
epsilon each, keeping all other rates and the interaction law fixed. In an
exclusion configuration at most one direction on each of the three connector
edges is active, so total changed outgoing rate is at most 3 epsilon. Standard
common-jump coupling gives full-path TV distance at most 3 epsilon T between a
perturbed process and its unperturbed quotient model over time T. For two
independent contact replicas, a safe bound is 6 epsilon T.

Two different hidden-cycle models with the same unperturbed boundary law
therefore have perturbed boundary-law distance at most 6 epsilon T for exclusion
or 12 epsilon T for contact. Observation cannot increase path TV. The argument
also allows common boundary feedback up to the first discrepant coupled event;
source/sink events use identical local controls. Over multiple trials T is the
total time budget. Constant reliable distinction requires a time scale at least
of order 1/epsilon in this bound. This is a conservative coupling obstruction,
not an optimal statistical lower bound.

No network dimension alone bounds the departure epsilon from these quotient
symmetries. Thus even excluding exact lumpability and achieving generic local
rank does not grant uniformly polynomial acquisition time or noise tolerance.
A quantitative visibility/identifiability margin is a new required premise.

## 8. Astra and the strongest existing comparisons

Read the COMPLETE current N1298 governing proof and packet at revision
95c99ce592a48d4505dd4bfcc0925d7ebad0efdd; the source SHA256 is verified in
SOURCES.json. It already distinguishes real distributed onsite nonlinearity from
port-only or isotropic nonlinearities, and explicitly declines apparatus,
novelty and broad flagship claims. Its globally calibrated Kerr actuator and
phase-coherent modal preparation are different from occupancy exclusion/contact;
this work does not promote its pending model construction into an accepted
physical premise.

The focused primary review is in LITERATURE.md. In particular:

* Gamble et al. already use a uniform on-site interaction to distinguish graphs
  that noninteracting walks fail to distinguish, including a fourth-order effect.
  Their full two-particle Green-function access is stronger than this boundary
  contract. [Primary paper](https://arxiv.org/pdf/1002.3003).
* Nonlinear Calderon higher-order linearization and nonlinear hyperbolic inverse
  problems already extract interior information from naturally interacting waves;
  they pay rich boundary/open-region source and measurement interfaces and
  geometric/regularity assumptions. [Elliptic primary paper](https://arxiv.org/abs/1903.12562),
  [hyperbolic primary paper](https://arxiv.org/abs/1405.3386).
* Burgarth--Maruyama acquires Hamiltonians through an infecting gateway on a known
  graph. A topology/access promise matters; a noninfecting source is not solved
  by relabeling that theorem. [Primary paper](https://arxiv.org/pdf/0903.0612).
* Covi--Lassas's current partial random-walk inverse result explicitly recovers
  a hidden-block similarity class under its cross-block rank conditions; use its
  2026 v2 rather than a stronger-sounding indexed v1 abstract.
  [Primary v2](https://arxiv.org/html/2408.05072v2).

No cited graph-isomorphism theorem is silently imported as a CTMC no-go. The
negative result here is the explicit controlled lumpability proof (5)--(9).
No absence of a matching paper in this focused search is a novelty claim.

## 9. Reproduction and failure record

Run these ordinary scripts from this directory:

    python symbolic_saved_pair.py > symbolic_pair_results.json
    python finite_boundary_tests.py > finite_boundary_results.json
    python exact_counterexamples.py > counterexample_results.json
    python contact_saved_pair.py > contact_results.json
    python conditioning.py > conditioning_results.json

Review artifacts additionally replay independent source/contact checks. Exact
SymPy algebra verifies identities and determinant; SciPy floating exponentials
supply diagnostics only. There is no sampled-trajectory claim, no hardware
measurement, no learner handed a hidden matrix, and no successful generic global
or scalable inverse algorithm.

Failures retained: an initial contact script tried to mutate SymPy's immutable
Kronecker result and stopped before contact verification; conversion to a mutable
Matrix corrected it, and the full check was rerun. A symbolic test initially used
structural expression equality instead of subtract-and-simplify, rejecting two
algebraically equal forms; corrected and rerun. Initial ideal pair preparation
was explicitly replaced by the finite-rate two-token source rather than assumed
free. The unfavorable conditioning and large sufficient trial count were kept.

The actual remaining scientific question is a QUALIFIED class-specific theorem
and feasible apparatus with a measured visibility margin, compared against
existing nonlinear inverse and equally informed fitting/design methods. This
work has not acquired either. No additional source-label oracle should be added
to rescue the broad claim.

## 10. Differential-mobility scope check, not a free clock oracle

The identical-replica contact quotient removes a common absolute circulation
reference. It is not a theorem for arbitrary independently tunable bulk clocks.
If a DIFFERENT physical interface warrants Q_1=c_1 Q and Q_2=c_2 Q, relative cycle
rates become p=c_2u+c_1v and q=c_1u+c_2v, with

    pq = c_1 c_2 (u+v)^2 + (c_1-c_2)^2 uv.

For c_1!=c_2, fixed u+v no longer fixes relative contact laws: for a uniform
relative starting law on the three-cycle, contact-survival derivative four is
kappa^2[(kappa+p+q)^2+2pq]/3. Reflection can still hide the sign of circulation.
This conditional algebra is a scope clarification, not a new reconstruction
campaign or an acquired operation.

A genuine shared overdamped landscape with common force, temperature and domain,
and globally proportional mobility tensors M_s(x)=c_s M(x), does imply generator
scaling. But independently measuring two tracers' mobility in a reference fluid,
even with an Einstein relation, does NOT establish those hidden bulk conditions.
Species can change wall coupling, accessible geometry, adsorption, barriers and
force response. A coarse CTMC further requires a common valid Markov reduction.
Primary two-particle microrheology obtains its additional information from
embedded displacement correlations, not from boundary-only global-clock
calibration. Detailed source scopes and the continuum derivation are in
MOBILITY_SCOPE.md.

No qualifying specimen or independent bulk-law evidence is available in this
work. Therefore the same-clock no-go is retained with its exact scope, the
conditional escape is acknowledged, and this local-family campaign stops.
