# Cross-review of the synchronized-anchor asynchronous certificate

Reviewer: gd_async_genesis. Date: 2026-10-16. This review was explicitly
requested by the root task after the independent investigation was written.
It is same-team analytic review, not external validation.

Reviewed artifact:
`/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-16-joint-structured-genesis-v1/workers/gd_async_adversary/ANALYSIS.md`

Reviewed-byte SHA-256:
`c1bebc3bbe42cda4a1562837d56de103b98d16bd12263e1fa84895a1a3c7d237`.

**Assessment: the anchored certificate is valid under the canonical
fixed ideal-pinch contract and its stated parity-preserving common-dilation
extensions.** I found no gap in the history-OR, whole-real-axis, clipping
or zero-case steps. It remains a partial bound, not the full asynchronous
product-Q theorem.

For a synchronized anchor subset A, write

    M_A² = product_(i in A) Q_i,
    C_j = min(1,sum_k s(a_jk)),
    s(a) = sin²(min(a,pi/2)).

The reviewed result is

    E(all selected history-OR flags)
      <= M_A² product_(j outside A) C_j P_s.           (1)

The terminal all-flipped effect is bounded by the same quantity.

## 1. What the anchor theorem may treat as its bath

All outside V_j preserve every anchor parity, by the exact cross-parity
assumption. Their pinches preserve those parities too. They can be part
of the anchor's sector-preserving baseline and fixed intervening record
isometries. They need not commute with the anchor's bath coefficients or
with one another. The anchor's conditional state can include every outside
physical coordinate, every retained outside record and an arbitrary
reference as part of an enlarged finite bath.

At a common anchor node, the entering anchor joint sector is actually
resolved. The synchronized Q induction conditions only on past anchor
records. An outside record isometry inside the next common anchor gap
does not insert an additional anchor pinch and does not change that
entering-sector premise. Its parity preservation is sufficient for the
one-gap deletion/type argument. Thus the anchor theorem applies in the
presence of arbitrary asynchronous outside pinches.

This conclusion requires exact preservation on the relevant whole input
domain. A generic intervention that merely resembles a dephaser or whose
support/completed dilation is unqualified cannot be imported by notation.
The canonical complete commuting pinches satisfy the requirement.

## 2. The whole real axis really is available

Choose one own gap k_j for each retained outside coordinate j, scale its
entire V_j restriction by z_j, and project onto all anchor history flags
and all those chosen outside gap mismatches. Let F(z) be the compressed
record amplitude.

For **every** real tuple x, the scaled outside terms are Hermitian and
still preserve every anchor parity. Their real scales may be arbitrarily
large; the anchor baseline has no norm cap. The anchor envelopes, actions,
common nodes and history projectors are unchanged. The synchronized anchor
theorem therefore gives

    ||F(x)|| <= M_A for every x in R^r.                 (2)

This does not incorrectly assert that the scaled outside terms satisfy
their original physical norm budgets. Those budgets are unnecessary for
(2), because these terms are baseline terms in the anchor-only theorem.
They return to their original values when evaluating the desired effect.

For one complex z_j with all other parameters real, the imaginary
perturbation has norm growth at most exp(a_jk_j |Im z_j|). Fixed record
isometries and output projectors are contractions. Hence that variable
has the required entire type. After evaluating any previous scale at 1,
that scale is again real; the same type argument applies to the next
variable. The first sine estimate is uniform over the whole remaining
real parameter domain, so its improved bound is a legitimate global
real-axis constant for the next sine estimate. No bound with several
nonreal parameters simultaneously is needed.

## 3. Deletion and the history-OR union

Deleting the selected restriction on an outside own gap makes its two
recorded endpoint labels equal. Other terms, other pinches and fixed
parity-preserving interventions preserve that outside parity on the gap.
This is a whole-input amplitude-zero identity for every value of the
other scale parameters, including complex values. It is not a probability
estimate after conditioning on the anchor's future event.

Iterating the operator sine lemma using (2) therefore gives, for the
chosen gaps,

    F(1)^*F(1) <= M_A² product_j s(a_jk_j) P_s.        (3)

All history projectors are diagonal in isolated record registers. For
each outside coordinate, history-OR means at least one own gap mismatches.
Thus the all-selected history event is contained in the positive union
over one chosen witness gap per outside coordinate. The union may overlap;
the proof only uses the indicator inequality by the sum of its witnesses.
Summing (3) factorizes the **scalar finite sum**, not the actual error
distribution, and gives M_A² product_j sum_k s(a_jk).

Anchor history projectors and outside gap projectors commute even when
two outside gaps overlap in time or neighboring own gaps share a label.
Their output records are fixed and isolated. Pullback through the common
record isometry preserves the positive operator inequality.

## 4. Individual clipping is justified by dropping before the proof

Let L={j outside A: sum_k s(a_jk)<1}. Drop all other outside constraints
from the **target event first**. The original event is contained in the
event involving all anchors and only L. Apply the same proof to that
smaller selected set. Dropped interactions/pinches preserve all retained
parities, so they can again be treated as baseline/interventions.

The resulting bound is precisely

    M_A² product_(j in L) sum_k s(a_jk)
       = M_A² product_(j outside A) C_j.

This establishes (1). It does not rely on algebraically capping separate
factors in an already proved product inequality. In particular equality
sum s=1 can be placed among the dropped coordinates without ambiguity.

## 5. Degenerate cases and minimizing certificates

- If an anchor factor Q_i is zero, its history event is impossible and
  M_A=0. Equation (2) is identically zero; no division by M_A is used.
- If a chosen outside gap has zero action, its entire type is zero and
  deletion nullness forces its amplitude to be zero. The sine factor is
  exactly zero. A coordinate with all actions zero has C_j=0 and cannot
  have a history mismatch.
- A saturated s=1 makes that outside sum at least one; it may be dropped.
  An anchor Q_i=1 is a harmless factor. No inverse cosine or division by
  a survival probability is used.
- If L is empty, the anchor theorem alone supplies (1); there is no
  outside union or interpolation step.
- The empty anchor gives M_A=1 and recovers the source product-C bound.
  A singleton anchor is always synchronized with itself. The full anchor
  is legal only when the actual node lists synchronize, rather than
  merely their counts or gap actions.

Every anchor certificate is a scalar multiple of the same initial-sector
projector P_s. Taking the minimum over the finite collection of valid
anchor subsets is therefore legitimate. It does not permit choosing the
best factor independently in each coordinate from incompatible anchors.
For two arbitrary schedules the result is exactly

    E_history <= min(Q_1 C_2,C_1 Q_2) P_s.

The general product Q_1Q_2 is smaller and is not established by this step.

## 6. Endpoint/Walsh scope and costs

A terminal wrong binary label requires some own recorded mismatch, so
endpoint inclusion is immediate. Under the exact additive private-sign
common dilation with independent fair refresh bits, the averaged positive
Walsh effects equal the virtual endpoint effects. The anchor inequality
therefore transfers on the whole physical input/reference space. It does
not require reading the latent history flags or adding real syndrome
measurements. The private coefficients, support, completion and controller
privacy conditions remain substantive receiving premises.

Selecting an anchor is a proof operation, not an added physical control.
There is no new acquisition or implementation cost hidden in (1); the
existing ideal protocol's actual random bits, frame updates, wrappers,
reservations, reset, timing and residual costs still need to be paid.

## 7. Exact scalar example

For two staggered own node lists with actions (t,t), sin t=3/5 and
cos t=4/5, Q=369/625 and C=18/25. Direct rational arithmetic gives

    C² = 324/625 = 0.5184,
    Q C = 6642/15625 = 0.425088,
    Q² = 136161/390625 = 0.34857216.

The anchor improvement over C² is 1458/15625, exactly 18 percent of C².
These are certificate comparisons, not actual model probabilities or
sharpness claims. All quoted values in the reviewed example are correct.

No numerical search is used to validate the universal anchor argument.
This review does not certify the reviewed worker's separate optimizer or
its historical originality; neither was needed for the analytic audit.
