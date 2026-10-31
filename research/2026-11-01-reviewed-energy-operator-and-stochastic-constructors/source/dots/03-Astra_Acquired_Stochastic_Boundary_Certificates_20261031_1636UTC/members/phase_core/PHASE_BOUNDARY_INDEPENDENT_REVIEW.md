# Independent whole-proof and exact-code audit: acquired inactive-head patch

31 October 2026. Mathematical count-process research only.

## Verdict and frozen subjects

**Accept the sufficient phase-core/shared-hub theorem and its exact acquisition
construction at the versions below.** The accepted conclusion is nonexplosion,
classwise positive recurrence, and every finite exponential total-count moment,
under all stated raw-list and boundary-compatibility guards. No substantive
mathematical or code gap was found. This is an independent internal acceptance,
not external refereeing, a general weak-reversibility result, priority clearance,
efficient computation, or a physical capability.

Reviewed and frozen:

* `PHASE_BOUNDARY_THEOREM.md`:
  `bc2dbe0187c9005897c636ac3a07fc58072a005f5644b0973d7d92560e129f31`.
* `phase_boundary.py`:
  `61548708b9d3cb6711afdc6c23631e143a19bec1e0ddb6793e67d6dcff05bd08`.
* `results.json`:
  `400e6b752a1609da44e67e16ed6930c643a1f71d63147033f1fe9e991e98bef7`.

Exact copies are in `independent_audit/frozen_*`. The entire demonstration was
replayed from frozen code; `replayed_results.json` is byte-identical to the frozen
original. The new verifier/challenges import the frozen code, not a mutable future
version. The prior pivot-star and terminal-gap packages were not changed.

## 1. The acquired architecture is genuinely larger, but still restricted

The raw finder enumerates nonempty proper service subsets, requires strong
connectivity of the full monomolecular core including zero and every nominated
service species, detects actual star rows, and rejects any unclassified reaction.
It does not accept a supplied good grouping without checking the whole input.

Every detected hub has a complete positive forward/reverse row to every satellite.
All direct service deaths must be at hubs, and every hub must have a direct death.
Neutral means preservation of EVERY service count and total count, not merely of
their sum. These conditions are binding. Full weak reversibility by itself does
not replace a missing reverse row or the no-inactive-death condition.

In the five-species witness, the former one-pivot architecture is genuinely
excluded by two actual edges: 0->A forces A as that old pivot, while A->E is
neither its one-species core, its exact star shape, nor A-neutral. This is a
structural noninclusion, not a statement that every present instance lies outside
all previous recurrence criteria.

## 2. Equal hub weights are acquired correctly

For inactive service types, the finite conversion chain hits H before it can die:
any core path to zero must first reach a species with a direct death, and all such
species are hubs. Hence the inactive killed conversion matrix is transient and
its exact first-hit equations have positive solution t.

Setting v_i=L+t_i, with t_h=0, gives Qv_i=-1 on inactive rows. On hub rows,

    (Qv)_h=sum_(i inactive) k_hi t_i-d_h L<=-1

by the acquired maximum defining L. This remains true with unequal hub deaths and
hub-to-inactive return conversions; both were independently tested. Choosing
q_i=1+eta v_i makes every hub q_h equal to the common satellite base T. This plateau
is essential: using unrelated full-lifetime weights could leave exponential star
ratios different from one and destroy the sign of the satellite-leading term.

The code checks Qv<=-1 exactly. The new verifier independently recomputes the core
rates, first-hit equations, q and v identities, and hub plateau directly from the
raw reaction list. It does not trust the recognizer's classification as a premise.

## 3. Tail algebra and all service compositions

For r>=2, conversions do not change r. Equation (3) in the proof supplies weighted
linear core drift <=-delta r. The g-factor only lowers immigration contribution,
so the stated bound B is safe. Each death adds correction

    (c/(r-1)) sum_i (d_i/q_i)y_i <=2cD.

A forward star has zero exponential-weight change because q_h=T. Its g increment
is c/(r-1), and the total forward term is bounded by c alpha r. A reverse star has
ratio r/(r+c), hence the exact negative term

    -(c/(r+c)) sum_(h,j) beta_hj y_h z_j.

These identities hold for arbitrary service compositions. They do not assume
independent populations, mean-field phase balance, or a fast invariant law. The
neutral contribution is exactly zero for all degrees.

The code's c<=delta/(4alpha) leaves positive tail margin. Its exact ceiling R
satisfies the all-state tail inequality, with epsilon_tail=delta/4. The new
verifier checks every inequality and the sign/normalization conditions using only
rational arithmetic. This is not a fitted tail from a finite grid.

## 4. The head uses actual exit values and stays finite in the right variables

F contains every no-hub service configuration with r<R. It does NOT truncate the
satellite total. Every F state has a positive-probability core path to leave F;
immigration handles the empty service state, and conversion into a hub handles
positive inactive populations. The finite killed generator is therefore
transient. This is a genuine finite acquisition: its size is
binomial(R+|I|-1,|I|), or one when I is empty.

The exact equation

    (-Q_F)u=1+Q_FB h_0

contains the true tail boundary value at each actual exit. Therefore the patched
function has LV=-T^(sum z) everywhere over F. A homogeneous Poisson equation or
an arbitrary boundary constant would not establish this conclusion. All u values
are positive; epsilon<=min 1/u gives the required multiplicative head drift.

There is no nonexplosion circularity hidden in the finite projection: while
service stays in F, satellite total is unchanged, service total is bounded by R,
and neutral motion stays in a finite integer shell. Even before the global proof,
no infinitely fast neutral explosion can hide inside that finite stopped region.

The new verifier independently enumerates F and checks every Dirichlet equation
against raw core jumps and actual exit values. It does not call the implementation's
linear solver, constructor, value routine, or generator routine. Tampering with
a single head value is rejected.

## 5. Patch leakage is fully classified and paid

The compatibility argument is valid and is the key nontrivial assembly step.

* A no-hub state with r>=R cannot jump into F: inactive service has no death,
  conversions preserve r, and immigration only increases it.
* An active state at r>=R+1 cannot enter F by a monomolecular core jump. Stars
  preserve activity: a forward consumes two hub particles but leaves one, and a
  reverse adds one. Neutral motion preserves every service count.
* Thus only the finitely many active service states with 1<=r<=R can see patched
  destinations.

For each such state, the core correction changes only a finite constant quotient.
All star endpoints remain active, so their original g-ratios survive unchanged.
Every satellite retains strictly positive slope

    a_yj=(c/(r+c)) sum_h beta_hj y_h>0.

The full positive reverse rows are used exactly here. The code enumerates all
active service layers, computes their actual constants and slopes, then acquires
integer satellite head bounds and a rational C. The new verifier independently
reconstructs every row, checks complete layer coverage, verifies thresholds and
C, and rejects deletion of a layer row.

A mutation can remain globally weakly reversible while lacking one required direct
reverse star. Such a mutation was rejected. This shows that global return paths
are not being substituted for the quantitative leakage guard.

The proof explicitly does not cover direct inactive death. That would allow an
inactive boundary layer to enter F with no negative satellite-leading coefficient.
The current head construction does not establish that broader compatibility claim.

## 6. Probabilistic closure and stationary exponential moments

The patched V is positive and normlike. Outside F, all weights are >=T>1 and g has
only polynomial loss; over F, service values form a finite positive set and
T^(sum z) controls every satellite direction. Thus finite V-sublevels are finite
integer sets, even with multiple unbounded phases and satellites.

Stopped Dynkin from LV<=C rules out finite-time escape to arbitrarily large
sublevels. Every finite sublevel has bounded total rate, including arbitrary
high-degree neutral channels. Hence explosion cannot be hidden on a level set.
The strict exterior drift gives finite expected hitting time of a finite set.
Weak reversibility supplies enabled population return paths; finite-set
regeneration yields classwise positive recurrence.

The stationary moment transfer is correctly justified without assuming either
pi(V) or stationary jump intensity is finite. Stopped exponential Dynkin gives
P_t V<=aV+b. Invariance, concavity of min(v,n), and Fatou then yield pi(V)<=C/epsilon.
For any finite theta, choose rational T>exp(theta). Polynomial g loss and the
finite positive patched values give V>=K exp(theta N). Uniqueness within the
communicating class means the same stationary probability receives each of these
moment conclusions. No uniformity over exponent, rates, dimension, or rare phase
access is claimed.

Rare activation is not hidden: it enlarges finite hitting times, u, satellite
thresholds, C, matrix sizes, and bit cost. An independent rare-immigration/unequal-
death test produced a 3,161-bit Foster constant even though its inactive head still
had only three states. A small head is not a small quantitative stability bound.

## 7. Executed independent verification and challenges

`independent_audit/verify_and_challenge.py` provides a separate exact verifier and
six executed structural challenge cases. Its certificate verifier does not call
`recognize`, `construct`, `solve`, `value`, or `generator` from the submitted code.
Results are in `independent_audit/challenge_results.json`.

| Challenge | T | R | Head size | Active layers | Exact state checks |
|---|---:|---:|---:|---:|---:|
| Frozen five-species witness | 2 | 2 | 3 | 9 | 280 |
| Same raw network, smaller exponent base | 3/2 | 2 | 3 | 9 | 280 |
| Same raw network, larger exponent base | 4 | 4 | 10 | 55 | 840 |
| Unequal hub deaths and hub return conversions | 2 | 2 | 3 | 9 | 280 |
| Two satellites and seventh-order neutral mixing | 2 | 2 | 3 | 9 | 840 |
| No inactive service species | 2 | 2 | 1 | 5 | 60 |

Total new state checks: **2,580**. All passed, together with independent all-head,
all-active-layer and rational-tail certificate verification. Exact head-value and
layer-coverage tampering were rejected. An incomplete reverse row was rejected
even though the mutated full graph remained weakly reversible. The frozen main
run was independently replayed byte-identically, retaining its separate 1,260
state challenges. Finite checks are implementation challenges, not proof of the
infinite-state theorem.

## 8. Work-budget and moment-exponent distinction

The implementation defaults to a 2,000-state finite-head budget. On the SAME demo
network with T=100, it returns the explicit decline

    required_head_states=3570, budget=2000, R=84.

No matrix solve is attempted after that decline. This is UNKNOWN due to a work
budget, not instability and not failure of the mathematical finite construction.
The all-exponent theorem is an ordinary all-parameter proof; it is not a claim that
the default-budget implementation has executed or will execute every exponent.
The original T=2 run alone controls exponential moments with exponent below log 2;
this review additionally executed T=3/2 and T=4, but still makes no extrapolation
from a finite list of tests.

The scanner's finite subset search is complete for finding some qualifying raw
architecture. The dense exact head solve and active-layer enumeration may be
expensive; a more economical block-by-r solve is only an identified improvement,
not an implemented feature of the reviewed code.

## 9. Conventional comparison and limits of acceptance

The positive weighted-linear obstruction in Section 8 of the proof is sound,
including the necessary minimum-satellite argument when several satellites and
neutral redistribution are present. The forward-axis test initially constrains a
weighted sum; the minimum-satellite reverse-axis test makes all its summands
nonnegative, so they must all vanish. All hub/satellite weights then coincide,
and positive immigration defeats global linear Foster drift on the service-empty
face. This is a limitation of that proof architecture, not an instability claim.

Finite Poisson equations, Dirichlet problems, M-matrix positivity and Foster theory
are standard. The incompatible star ratios prove the witness is not complex
balanced, but do not establish novelty relative to non-product-form or network-
decomposition criteria. No external-priority determination was performed here.

Acceptance excludes inactive deaths, incomplete positive hub rows, nonlinear
service cores, arbitrary fast conservative fibers, and any unverified extension
of the patch interfaces. General weak reversibility remains unresolved by this
package. No upload, publication, outreach, laboratory procedure, biological
activity, or denied-source retry was part of this audit.
