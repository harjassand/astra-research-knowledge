# Independent hostile whole-proof and raw-compiler audit: pivot-star closure

31 October 2026. Abstract count-process mathematics only.

## Verdict

**Accept the stated sufficient pivot-star construction at the exact versions
below**, including nonexplosion, classwise positive recurrence, and every finite
exponential total-count moment. The core, pivot and neutral remainder are acquired
from the raw list; the unbounded satellite fiber is not silently made finite and
no stationary or mixing oracle is supplied. Acceptance is an independent internal
mathematical/code review, not external refereeing, historical novelty, a general
weak-reversibility result, or physical/operational validation.

I found no counterexample or omitted interface under the exact source contract.
The one correction requested during review was to strengthen the stationary-
moment integration step so that it does not presuppose integrability. The author
incorporated the stopped-semigroup/concave-truncation proof in Section 6; that
revised text was inspected and is the accepted proof version. The code did not
need repair.

## Frozen versions

* Accepted theorem: `PIVOT_STAR_THEOREM.md`, SHA-256
  `24166432f3f19f9fbb4891c20896b1c2c3e340d70420a7187592264f412b12cc`.
  A frozen copy is `pivot_audit/PIVOT_STAR_THEOREM_REVIEWED.md`.
* Code: `pivot_lift.py`, SHA-256
  `69408dd5cf0235d4a92947696e5db505857062b42703e9cfbf1c1fdf2c91e519`.
  The frozen imported copy is `pivot_audit/pivot_lift.py`.
* Original results: `pivot_lift_results.json`, SHA-256
  `6880adc44888c88d67b706c2af6662bdcd361a9d175e11e450a05c56f16c1008`.
* The initially audited theorem had SHA-256
  `0425bd515bd35959c85b0a5273f30a9ef8969a320911266a50313326369b3daf`;
  its frozen `pivot_audit/PIVOT_STAR_THEOREM.md` remains for chronology.
  The accepted revision changes only the stationary-moment proof paragraph.

## 1. Raw-list acquisition and exact guards

The recognizer deletes genuine null channels, verifies full weak reversibility,
then scans each possible distinguished species. It classifies every remaining
reaction, not just a favorable subgraph, as one of:

1. a reaction involving the pivot alone, in a separately weakly reversible core;
2. an exact edge `2A -> A+B_j` or its reverse, with parallel rates aggregated;
3. a reaction preserving BOTH the pivot count and total count.

Every nonpivot species must have strictly positive direct forward and reverse
star rates. A missing reverse cannot be supplied merely by an indirect global
return path. An extra rule preserving total count but changing the pivot is not
neutral for the correction. These are binding restrictions, not proof conveniences
that may be dropped after recognition. Rejection gives no instability verdict.

I independently challenged those guards with a globally weakly reversible list
having a missing direct B-star reverse, and with an extra reversible total-count-
conserving rule that changes A. Both were rejected. Species order and label names
are not used to supply the pivot.

## 2. Exact generator algebra, including two dangerous boundary layers

Write `V=t^N g(a)` with `g(a+1)/g(a)=a/(a+c)` for a>=1. A forward star jump keeps
N fixed and has ratio `g(a-1)/g(a)-1=c/(a-1)` when a>=2. Multiplying by its
propensity `alpha_j a(a-1)` gives exactly `c alpha_j a`. A reverse star jump has
ratio `-c/(a+c)` and propensity `beta_j a b_j`. Their sum is precisely the source's
formula. Neutral channels contribute identically zero, regardless of degree.

**At a=1**, the forward source is disabled: the positive `c alpha a` term must be
removed. The negative satellite contribution remains `-c/(1+c) sum beta_j b_j`.
The code uses `H_1=P(1)`, not the generic a>=2 formula. A core jump 1->0 may have
positive corrected reward because g(0) is large; it is included exactly in P(1)
and is paid by the first-layer threshold/Foster constant, not omitted.

**At a=0**, all star propensities vanish. Each enabled inflow 0->v has ratio
`t^v g(v)/g(0)-1<0` by the acquired finite choice of g(0). The generator quotient
is therefore a strictly negative constant uniform over every satellite state.
This is the essential extinction-face estimate. Extrapolating the positive-a
recurrence to g(0) would be invalid; the source does not do so.

If the core contains no inflow, its weak reversibility excludes every non-null
core edge incident to 0. Positive-a states cannot reach a=0 through the star
(since forward star stops at 1), core, or neutral remainder. The a=0 sector is
closed and each of its reachable classes lies in a finite fixed-N shell. Such a
class need not be a singleton: an independent test has B<->C motion on that face.
No global strict-drift claim is incorrectly imposed across infinitely many such
finite shells.

## 3. Pivot-tail and exact coefficient certificate

For a>M, all finite product ratios used by the core are valid and their
denominators are positive. Since every core complex is a source, a maximal-source
non-null reaction points strictly down. Its leading coefficient is
`sum_(M->v) kappa(t^(v-M)-1)<0`. For M>=2, this dominates the added positive
linear star term. For M=1, the separately acquired small c leaves a strictly
negative coefficient of a. The no-satellite branch also retains that sign.

The reduced rational function H+1=Q/D is sign-normalized. Its numerator has
negative leading coefficient and denominator positive leading coefficient, so
all nonzero derivatives have the respective eventual signs. Doubling R until
all shifted coefficients have the asserted signs therefore terminates. The
resulting witness certifies H(a)<=-1 on the entire real halfline a>=R, not merely
at sampled populations. Cancellation does not invalidate the identity: the
certificate also requires D(R+z)>0 for z>=0.

The challenge script independently recomputed Q/D=H+1 symbolically, reconstructed
the shifted polynomial coefficients, checked their signs, and bound the rational
H to exact full-generator evaluations beyond R. It exactly reproduced the frozen
original certificate. SymPy constructs exact polynomials; no floating solver or
approximate root bound is used.

For each finite pivot layer, the bound using beta_min is directionally correct:
`sum beta_j b_j >= beta_min sum b_j`. The ceiling-based B_a safely bounds every
integer satellite total above the threshold, and the finite C bound uses the
maximum possible `t^(a+sum b)` in each retained layer. Negative B_a values are
safe to omit because the quotient is already sufficiently negative for b=0.
The one-species/no-satellite branch correctly sets the only satellite total to 0.

## 4. Nonexplosion with high-degree neutral reactions

The corrected V is positive and normlike: for a>=1, its polynomial g(a) loss is
dominated by the exponential t^N, and the a=0 value is g(0)t^N. A stopped Dynkin
estimate from LV<=C bounds the probability of exiting finite V-sublevels before
fixed time by `(V(x)+Ct)/R`. All outgoing rates are finite at each state.

Potential cancellation alone would not rule out arbitrarily many jumps hidden on
an infinite level set. Here each V-sublevel is finite, and even every fixed-N
shell is finite because there are finitely many species. The total rate is bounded
on such a finite set, including the arbitrary high-degree neutral channels. Thus
explosion cannot occur without escaping the sublevels; the stopped estimate rules
that out. This argument does not require an a priori upper degree bound shared
across networks or an unproved fast-fiber mixing assertion.

Outside a finite set, strict Foster drift gives finite expected hitting time.
Full weak reversibility supplies actual population return paths and closed
irreducible reachable classes. Finite-set regeneration then gives positive
recurrence. The separately conservative sectors are finite-state chains.

## 5. Stationary moments: accepted strengthened argument

The original short reference to invariant generator integration was not used as
an unexplained moment-domain assumption. The accepted revision first obtains

    P_T V <= r V+b,  r=exp(-epsilon T)<1,
    b=C(1-r)/epsilon

by stopped exponential Dynkin and Fatou after nonexplosion. This is a pointwise
bound and already establishes finite E_x V(X_T) for every finite state x.
For the existing invariant probability pi, concavity of phi_n(v)=min(v,n) gives

    pi(phi_n(V))=pi(P_T phi_n(V))
                <=pi(phi_n(P_T V))<=pi(phi_n(rV+b)).

The difference of the integrands is bounded below by -b. Fatou as n tends to
infinity yields `(1-r) pi(V)<=b`, hence `pi(V)<=C/epsilon`, without assuming that
pi(V), pi(Lambda), or an unbounded generator integral exists beforehand.

For any requested finite theta>0, choose rational t>exp(theta). Since
`g(a)>=exp(-c)a^(-c)` and a<=N on positive-a states, there is a positive constant
K with `V>=K exp(theta N)`; the a=0 sector is even simpler. Thus every finite
exponential N moment is finite. The same invariant probability is used for all
choices of t, by classwise uniqueness. Constants are not uniform across t, rates,
species count, or conserved finite shells.

## 6. Independent executable challenges

Run `python pivot_audit/hostile_checks.py`; results are preserved in
`pivot_audit/hostile_results.json`. This imports the frozen code without executing
its demonstration main block. All completed challenges passed:

| Case | Tail R | Exact corner/layer states |
|---|---:|---:|
| Frozen three-species non-complex-balanced witness | 8 | 219 |
| No-zero core with moving finite a=0 face | 5 | 156 |
| Four-particle core plus seventh-order neutral reactions | 10 | 261 |
| Linear core requiring fractional c | 16 | 159 |
| One-species core with no star | 6 | 9 |
| Empty core | finite conserved shells | structural check |

Total new corner/layer checks: 804, plus symbolic halfline-certificate checks,
exact reproduction of the original certificate, and two failed-acquisition
mutations. These finite checks challenge implementation and guards. They do not
replace the all-count algebra and probabilistic proof above.

The non-complex-balance witness is exact: the separate 0<->A component forces
positive concentration a=1, whereas the leaf 3A forces 2a^2=a^3, hence a=2. The
neutral component does not repair that contradiction.

## 7. Scope that remains outside this acceptance

* An arbitrary core involving several species is not accepted.
* Missing reverse star edges, arbitrary catalytic exchange graphs, changing
  pivot counts in the neutral remainder, or total-count-changing satellite
  channels are not silently admitted.
* Recognition is sufficient and may reject stable networks.
* The doubling certificate terminates for the stated algebraic class, but no
  efficient worst-case bit or constant-size certificate bound is claimed.
* The abstract theorem has fixed positive real rates; the executable exact
  acquisition contract is rational input rates and rational t>1.
* Product-form comparisons, historical novelty and practical leverage were not
  settled by this audit. The baseline is already classically complex balanced.
* No external publication, communication, upload, laboratory activity, biological
  procedure, or denied-source transfer was performed for this review.

A separate earlier terminal-gap regression transport anomaly was resolved by
reading already-existing files, not retrying. Its output demonstrates completion
through its final result print despite missing transport acknowledgement. That
regression is not part of the pivot-star theorem's evidence.
