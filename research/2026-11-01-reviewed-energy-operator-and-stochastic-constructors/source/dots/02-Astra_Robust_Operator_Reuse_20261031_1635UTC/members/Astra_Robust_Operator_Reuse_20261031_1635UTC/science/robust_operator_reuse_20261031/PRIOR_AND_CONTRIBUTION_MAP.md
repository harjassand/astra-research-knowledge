# Prior match versus ingredients proved in this investigation

31 October 2026. This note separates correctness, historical novelty and
consequential performance. None implies either of the others automatically.

## 1. A standard learner can implement a useful new ingredient

The right comparison names are **ordinary retained Krylov/range/spectral
acquisition plus the certificate proved here**, not an exclusive new learner
competing against those algorithms. Sharing a certificate with every strong
method does not erase the certificate's contribution. It prevents attributing
that contribution to a new acquisition algorithm that was not invented.

Conversely, proving a theorem afresh here does not establish historical
priority. The reviews certify the supplied arguments and code, not exhaustive
novelty. The small fixtures and their strongest baselines still do not
establish a consequential acquisition-to-execution advantage.

## 2. Prior mechanisms actually matched

* Stable generalized Arnoldi/weighted-automaton reduction is prior machinery:
  Kiefer--Wachter, https://arxiv.org/abs/1404.6673 . Randomized range acquisition
  is likewise prior machinery, https://arxiv.org/abs/0909.4061 .
* **Quadratic output accuracy from primal and dual residuals is not a new
  principle.** In the directly accessible primary preprint by Klindworth,
  Grepl and Vossen, Section 4.4, equations (54)--(55), the output estimator
  contains the product of primal and dual state-error bounds, plus separately
  paid function-approximation terms. The discussion following equation (59)
  explicitly identifies this product as the superconvergent contribution and
  explains why a linear approximation-error term can dominate it. The PDE,
  coercivity, corrected-output and time-discretization setting is not the
  same as the present arbitrary-word operator interface:
  https://www.igpm.rwth-aachen.de/Download/reports/grepl/KGV_CMAME_preprint_revised.pdf .
* Earlier Grepl--Patera work already combines adjoint output certificates,
  greedy sample acquisition and offline/online repeated evaluation:
  https://numdam.org/articles/10.1051/m2an:2005006/ . This statement is supported
  by its primary abstract; no uninspected equation from that paper is claimed.
* Antoulas--Benner--Feng, *Model reduction by iterative error system
  approximation*, also explicitly relates output error to a product of
  forward and dual residuals. The institutional indexed PDF passage around
  equation (17) exposes the frequency-domain residual-product bound, but a
  full direct fetch returned HTTP 403. Therefore this is a matched mechanism,
  not a completed theorem-by-theorem comparison with that paper:
  https://doi.org/10.1080/13873954.2018.1427116 and
  https://pure.mpg.de/rest/items/item_2506841_10/component/file_2540640/content .
* Stable reduced realizations, common Lyapunov/data consistency reasoning,
  simulation-error telescoping and significant-state exploration have the
  primary antecedents cited in the two finite-observation proofs. Their use
  here is not evidence of a new general learning theory.

## 3. An explicit reduction showing what is already the primal-dual mechanism

In the exact common-contraction setting, let y_t be the lifted reduced
trajectory and r_t=Q A_t P y_(t-1). Then ||r_t||<=e_in||b||, and

    f-f_reduced = sum_t <A_(t+1)^* ... A_l^* c, r_t>.

Subtract the reduced adjoint trajectory, which lies in P and is orthogonal
to r_t. A first-order contraction telescoping bound on the adjoint difference
is (l-t)e_out||c||. Consequently

    |f-f_reduced| <= ||b|| ||c|| e_in e_out l(l-1)/2.

Thus the gapless quadratic result is directly the familiar primal-dual
residual-product mechanism specialized to this discrete word problem. No
output correction is needed in this common-space orthogonal case because
the corresponding reduced-dual/residual pairing already vanishes.

This derivation is included so that a broad resemblance is not mistaken for
an exact published theorem match, and a new derivation is not mistaken for
an historically new quadratic-accuracy principle.

## 4. Particular ingredients derived and checked here

The following are actual proved ingredients of this package, regardless of
which ordinary method implements them:

1. The all-word bound `e_in*e_out*S_l(alpha)`, using a checked complement
   contraction and full-trajectory boundedness, including its sharp leading
   coefficient example and finite local residual/metric acquisition.
2. The capped mixed-norm recurrence with arbitrary acquired positive H and
   separately stabilized replay: `C*M*(l*d + e_out*sum t_j)`. It does not
   infer exact common stationarity from imperfect observations and does not
   introduce an exponential factor from an approximately invariant metric.
3. A composable observation/center-compression/execution admission with
   acquired coefficient denominators and an executed integer backend, plus
   a sparse fresh-validation/Bellman frontend and its explicit coverage cost.

The sources inspected above establish strong antecedents for their component
mechanisms. They do **not**, on the present reading, establish an exact
published match for every hypothesis and constant of items 1--3. Nor has
this investigation established those items' historical novelty. That status
is **unresolved**, not automatically negative because conventional learners
can adopt the ingredients, and not automatically positive because the exact
displayed formulas were derived in this package.

The residual-product certificate demonstrably changes a stopping requirement
in the exact fixture: the same retained basis acquisition stops at rank four
rather than twelve under a first-order state-error rule. That is a real
conditional certification benefit. It is not yet a strong-prior-method or
practical workload advantage.

## 5. What the latest failure does and does not say

The new `finite_observation/MIXING_BASELINE.md` uses an ordinary acquired
minorization and reference-distribution drift certificate. On the chosen
fixture it admits a constant answer for every length 16--30, with paid
full-center fallback for shorter words. All forty length-30 tests therefore
need no matvec. This defeats that proposed online-performance demonstration,
not the correctness or possible scientific usefulness of the two-sided or
mixed-norm certificates.

A consequential next use would need a task whose informative slow directions
cannot already be replaced by forgetting/caching, and an acquisition or
precision saving attributable to the certificate itself. Its prior-theory
comparison should target the exact output/error/observation interface, not
require a novel learner merely to exploit a useful mathematical ingredient.
