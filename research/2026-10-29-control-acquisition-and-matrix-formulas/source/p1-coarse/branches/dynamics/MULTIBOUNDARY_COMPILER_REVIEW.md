# Independent review of the multiboundary positive-event compiler

28 October 2026. No fatal error found in the reviewed construction or
executed receipt. This review covers the new acquisition, matrix uncertainty,
bilinear endpoints, confidence calculations, cost ledger and same-data
Galerkin comparator. It does not re-prove the previously reviewed Julia
colligation theorem.

Reviewed result SHA256:
3a3614205db7ebd8f4f748f00af2f0675c5b4bf70edba4af6e95872647e79dbc.

## Positive physical event and matrix residual

Let V contain the distinguished boundary basis vectors, P=VV^T,
B=V^TAV and D_gal=(I-P)AV. For each boundary j,

\[
e_j^TD_{\rm gal}^TA^{2k}D_{\rm gal}e_j
=\Pr_j(X_1\notin\mathcal B,\ X_{2k+1}\notin\mathcal B,\
X_{2k+2}=j).
\]

The deleted set is the entire boundary, not just the starting state.
The instrument implements precisely these conditions. It may stop as soon
as the first or penultimate boundary report proves that the event is false.
At k=0 the first and penultimate reports coincide; no extra condition is
silently imposed.

For self-adjoint ||A||<=a<1, the acquired mixture
sum_(k<K) D_gal^T A^(2k) D_gal plus
D_gal^T A^(2K) D_gal/(1-a^2) dominates
Q_gal=D_gal^T(I-A^2)^-1D_gal in Loewner order.
Diagonal positive-event upper bounds therefore bound its trace, and a PSD
matrix is at most its trace times the identity. No hidden-rank bound is
used by this argument.

## Proposed model, row-mass refinement and endpoints

Writing E=B-T_hat, the proposed defect is D_prop=D_gal+VE. Thus

\[
\|(I-A^2)^{-1/2}D_{\rm prop}\|
\le\sqrt{\operatorname{tr}Q_{\rm gal}}
+\|E\|/\sqrt{1-a^2}.
\]

The code's row-sum bound on the symmetric entry-error matrix controls
||E||, and its rational PSD checks establish both Q_prop<=theta^2 R
and delta_op I<=zeta R, with R=I-T_hat^2.

The structured correction form is also valid. If e_j=sum_k E_jk,
then

\[
E=\operatorname{diag}(e)-\sum_{j<k}E_{jk}
(e_j^{\rm basis}-e_k^{\rm basis})(e_j^{\rm basis}-e_k^{\rm basis})^T.
\]

Observed row-mass radii and symmetric off-diagonal radii consequently
construct Pi with -Pi<=E<=Pi. Checking Pi<=zeta_struct R yields the
sharper bilinear correction bound by Cauchy-Schwarz in the R metric.

Different initial and terminal boundary basis vectors each have norm one.
The forward and backward coefficient energy budgets therefore give the
same uniform factor 2 theta^2; matching the two endpoints is unnecessary.
The checked backward recursion and signed-correction coefficient
orientation are correct. Aggregating coefficients across repeated uses
of one unknown E, and across a difference of two programs, preserves the
shared-data correlation.

## Strongest saved route: true-Galerkin interval propagation

The same data enclose the true nonnegative symmetric B entrywise and
bound its row sums by rho<1. Hence
I-B^2>=(1-rho^2)I and
Q_gal<=tr(Q_gal) I certify a true-Galerkin dynamical error without the
proposal's Minkowski penalty.

For nonnegative boundary preparation and receiver coordinates, boundary-only
paths are a subset of all source paths, so the true Galerkin response is
a lower bound on the full response. Multiplying the nonnegative lower
and upper entry matrices yields a valid word interval. Adding the
dynamical envelope only to the upper endpoint is justified. This
one-sided argument is not licensed for arbitrary signed endpoint vectors.

On the main 0-to-2 transport pair, the saved intervals are:

| Route | Certified source difference |
|---|---|
| Proposed model plus signed correction bounds | [.06641027, .17415187] |
| Same-data true-Galerkin interval propagation | [.10119065, .13943585] |

The exact source difference is .12046629285052089. The true-Galerkin
route also resolves all five tested transport pairs of lengths 20 through
60; the proposed-model interval ceases to resolve the pair at length 40.
The global proposed-model bounds are .0602079226 with the operator-error
correction and .0399340295 with the row-mass refinement. The true-Galerkin
uniform dynamical component is .01387442542000554, with word-dependent
entry-interval propagation added separately.

The stronger comparator must receive credit. It uses the same acquired
physical residual certificate, so its success does not remove that
construction's contribution. It does show that the proposal/correction
route is not the strongest implementation on this positive-source fixture.

## Confidence and completed independent replay

Pooling opposite-direction boundary counts is valid because the access
contract warrants symmetric transition probabilities. Ordinary reversibility
under an unknown nonuniform measure would not justify this unweighted pool.
Each row-mass count is binomial, even though different statistics computed
from the same categorical data are correlated. The union bound needs no
independence between those intervals.

The two predeclared inference checkpoints require 84 one-sided confidence
tails: 12 distinct symmetric kernel entries with two tails, six row masses
with two tails, and six one-sided positive-event probabilities, at each
checkpoint. A data-dependent choice between these checkpoints is covered.
The four direct-comparator tails can also be included while keeping the
total below .001, since 88 exp(-12)<.001.

The independent replay used its own 40-term rational logarithm enclosures,
rather than accepting the fitting routine's floating proposals. It checked
42 saved inference endpoints and all four direct endpoints. Degenerate
zero/all-success cases have conservative analytic endpoints. It also
recomputed all relevant 3-by-3 principal-minor PSD tests, proposal triangle
inequalities, structured forms and true-Galerkin denominators.

Using the hidden fixture only as a separate validation source, it checked
30 positive event/path identities and ten bilinear programs, including
their signed-correction orientation and their true-Galerkin intervals.
No source trajectories were regenerated. The executable and receipt are
replay_multiboundary_review.py and MULTIBOUNDARY_COMPILER_REVIEW_RESULTS.json.
The completed checks are at this actual scope, not a new audit of the
underlying all-word Julia theorem.

## Complete cost and access scope

The instrument's early rejections correctly save one final transition when
the penultimate report enters the boundary. It computationally skips
absorbed updates but continues to charge their scheduled time and reads.
Known terminal reports equal to the requested preparation state are reused
without a physical reset. The new final-report metadata makes
N-minus-known_returns-plus-last_equals_requested exactly replayable for
each sampling group; the corrected counts include group initialization.

The executed reusable acquisition used 60,000,000 logical trials,
70,353,830 primitive applications, 62,376,821 categorical observations,
and 8,801,332 physical preparations. The independently executed direct
0-to-2 comparator used 20,000 logical trials, 400,000 applications,
20,000 observations and 13,708 preparations, and resolved the one pair.
Thus this receipt establishes reusable certification, not a one-pair
acquisition advantage. Neither cost is claimed optimal.

The warranted global source norm cap, accurate nonintrusive categorical
boundary readout, controllable boundary preparations, and Markov/reset
semantics remain premises. The six hidden-state fixture validates the
software but does not supply hidden rank to the learner. Counting a
categorical observation does not acquire its precision or physical
noninvasiveness. No physical apparatus was operated.
