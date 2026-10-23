# A sharp convergence boundary and a cost obstruction for vanishing screens

Astra PRO3 accepted both received proofs closing the fixed-positive-eta gap,
then established a new result for screens selected before a run but weakened
across requested accuracies. The exact condition for uniform convergence is
eta_n log n->infinity. Preserving the stronger K/log n minimax rate requires
more screening, and an admitted growing path disproves the single-trap
multiplier-one prediction. The precise finite-constant crossover is open.

## Result and why it matters

The class remains finite positive pi,q, D(pi||q)<=K, fixed symmetric Q,
fixed alpha in (0,1), q initialization, and the lazy global/local mixture.
Only eta may change between separately specified runs. Ratios cancel the
unknown target normalizer. This is a robustness question for an established
delayed-acceptance algorithm, not a new acceptance rule or a downstream
application claim.

A theorem holding for each fixed positive eta does not justify decreasing
eta with a requested error. The new finite bound resolves that quantifier
gap. Weakening the screen makes each individual local proposal easier to
accept, yet can worsen the proposal-start minimax error. This gives a
concrete limit on reading finite-time robustness from acceptance comparisons.

Write R_eta(n) for the class supremum TV error. We prove:

1. For deterministic eta_n in (0,1], R_{eta_n}(n)->0 exactly when
   eta_n log n->infinity.
2. If liminf eta_n log n/loglog n exceeds the explicit sufficient constant
   Lambda_*=1+log(1+beta/2)/[-log(1-alpha exp(-K)/2)], then
   log n R_{eta_n}(n)->K.
3. Let chi be defined in the continuation seed by the path variational
   equation. If eta_n log n/loglog n tends to a positive constant below
   1/chi, then log n R_{eta_n}(n)->infinity.

The second and third constants do not match and are not called sharp.
For K=1,alpha=1/2 they are 3.31290271377... and 1.08848276574....

## The new proof operation

The received conjugation retains a fixed exponent in an Lp(q) moment bound.
The received reset representation sharpens its growth to an affine recurrence.
Our new step combines this moment bound with the geometrically decreasing
mass of each unconditioned first-hit submeasure. Interpolating these two
bounds gives a summable sequence of norms with a constant independent of eta.
Smoothing each submeasure at its own remaining horizon then pays the target
high-weight tail only once and preserves every subsequent return path.

The full finite inequality and its proof are in VANISHING_SCREEN_THEOREM.md.
An independent challenge accepted the actual upper source without repair.
The chosen first-hit thresholds are proof devices, not additional target
queries or knowledge of normalized weights made available to the sampler.

## The decisive failed conjecture

A single trap supplies capture roughly exp(-eta log n). It therefore suggests
that eta log n slightly above loglog n might suffice for the K rate. A path
of individually screened local moves defeats that universal conclusion.
The path's pi masses rise by n^2 on each edge, q masses decrease geometrically,
and its terminal state has weight n(log n)^2. Global escapes compete at
every intermediate state. Marked-exit probabilities and terminal retention
give an actual finite event lower bound; no adverse conclusion is inferred
from failure of a norm estimate.

At K=1,alpha=1/2, the fixed choices b=0.63, v=log16 and
eta_n=1.08 loglog n/log n yield a capture exponent

    27 log(321/25)/(25 log16)=0.994294790283846...<1.

The strict inequality has an exact integer certificate. Thus log n times
worst-case TV diverges even above multiplier one. Finite diagnostics do not
reach that very slow divergence; the source says so explicitly.

## Accuracy policy and ordinary comparator

For eta(epsilon)~d epsilon log(1/epsilon), d>0, the new theorem gives

    max(K,1/(d chi)) <= liminf epsilon log T
       <=limsup epsilon log T <=max(K,Lambda_*/d).

For d tending to infinity the exact coefficient is K; for d tending to zero
it diverges. A finite d>Lambda_*/K already suffices for K. Every run keeps
its chosen eta fixed. The argument evaluates actual fixed-kernel risks at
exp(A/epsilon); it does not invert a varying-kernel risk as if monotone.

At K=1,alpha=1/2,d=1, the resulting coefficient interval is
[1.0884827657...,3.3129027138...]. Pure IMH already has coefficient 1.
This supplies a strict worst-class penalty relative to that ordinary method.
It is not a claim that a particular applied target behaves adversely.

All 24 evaluated finite certificate comparisons favor ordinary IMH. Both
sides use the same target oracle, complete caching, forward-KL assumption
and error margin. The bounds are sufficient and conservative; they do not
measure a runtime ratio. NUMERICS.md gives the comparator's coupling proof,
the exact evaluated cutoff choices and every numerical limitation.

## Actual evidence and resources

The principal's two final standard-library Decimal runs evaluate 30 horizon
rows, 24 policy rows and 516 scalar certificates each. Their 980 reported
numeric comparisons agree to the retained 50 digits, apart from deliberately
excluded negligible optimization residuals. Final measured calculation times
are approximately 0.346 and 0.465 seconds. Earlier dependency failures and
the timing-record correction are recorded; no external package was installed.

The lower contributor computed 16 finite-chain laws at two reserved
precisions, with 3100 matrix products each. Largest working precisions are
392 and 422 digits; measured replay times were about 0.412 and 0.608 seconds.
The maximum TV discrepancy is approximately 1.073e-91. Those are direct
matrix-power calculations, not n-step trajectory runs. The initial precision
assertion failure and its correct repair remain visible.

These short computations are not the discovery cost. The source records
the observed principal interval, distinct contributors' intervals and search
calls, and unknown model/token/monetary and programme-wide totals. No spending,
hardware, intervention or outreach was used. A relocated source replay checks
portability; it is not an independent scientific review.

## Scientific status and next decision

The upper theorem has a source-bound independent challenge. The principal
directly accepted the separate lower construction and checked its admission,
branches, timing and retention. The upper challenger also verified its
accuracy-policy conversion without claiming a second full lower review.

A focused primary-literature search found relevant delayed-acceptance,
tempered-surrogate, weak-Poincare and hitting-time precedents. It did not
establish historical originality. Pure IMH remains the coefficient-K
comparator; there is no new useful implementation or physical speedup claim.
Ideal-real proofs and finite-precision diagnostics are kept distinct.

The next selected step is to study the killed transport operator before the
first safe hit, retaining the global escape term inside its weighted norm.
The goal is to decide whether that sharp transport exponent matches the
admitted path exponent chi, or whether another complete mechanism is needed.
This targets the finite-d gap, not the settled fixed-eta theorem. It is the
next question, not an unreported completed construction or background job.

The original Cycle2 owner archive, accepted incoming contributions, B3 pISO
correction and failed halo gate, metadata rejection and R3/anMC rejection
are preserved. Other owners' programmes and closed campaigns were not reopened.
Private delivery does not imply Max has read, accepted or integrated this return.
