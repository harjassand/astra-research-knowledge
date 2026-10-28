# Independent review: dissipation-normalized correction noise

28 October 2026. Scope: core/dissipation_noise.py and its refinement of the
12 existing acquisition receipts. The completed source-tail acquisition
and physical energy theorem are not re-audited.

## Finding and reviewed hashes

The new noise bound is valid. The implementation computes the correct
native weak-defect uncertainty, uses the required row/column domination,
and certifies the normalizations exactly. Its midpoint is the same
native-word midpoint predictor already used by the compiler.

Reviewed SHA256:

- core/dissipation_noise.py:
  265018896239eb5131afbd4bedfb2d98a56c4936c6a5f55d8d57419406a161ed
- results/DISSIPATION_NOISE_REFINEMENT.json:
  33b3c635be77907cfb8f7b133c473d9467184189a4a724070d4efd436156b447
- Unmodified input results/DISSIPATION_EXPERIMENT.json:
  e72d9b712284db24dcefd71bc4d744aa56bca58052f2e94ba92192c7858d5850

The finite-noise theorem needs no separately supplied strict contraction
factor rho. It does require the uncertainty to be dominated by computational
dissipation. The current numerical routine requires strictly positive
dissipation to propose its rational dominations; the theorem itself permits
positive semidefinite dissipation when the stated domination holds.

## 1. Nonsymmetric weak-defect intervals

Fix the realized transcript and its chosen coefficient maps T_i. Let

    F_i=M_i-G T_i,     R_i=W-T_i* W T_i.

Let Fhat_i be the matrix obtained by evaluating the combined native
expressions at the raw interval centers. Because interval midpoint is
linear under a fixed linear expression, Fhat_i=Mhat_i-Ghat T_i. Selecting
T_i from the same transcript does not invalidate this pointwise statement:
the observed T_i is fixed while testing sources consistent with the
observed intervals.

Write Delta_i=F_i-Fhat_i and assume |Delta_i[j,k]|<=r_i[j,k]. Define row and
column sums u_j=sum_k r_i[j,k] and v_k=sum_j r_i[j,k]. Weighted
Cauchy-Schwarz gives

    |x*Delta_i y|
      <= sum_jk r_i[j,k] |x_j| |y_k|
      <= sqrt(sum_j u_j |x_j|^2) sqrt(sum_k v_k |y_k|^2).

Consequently, with D_i=diag(max(u_j,v_j)) and D_i<=zeta_i R_i,

    |x*Delta_i y|
      <= zeta_i sqrt(x*R_i x) sqrt(y*R_i y).

The weak-defect matrix need not be symmetric; using both row and column
sums is essential. For example, an uncertainty matrix with only entry
(1,2) nonzero has zero second row sum. A row-only diagonal would falsely
give a zero bound for x=e_1,y=e_2. The implementation's maximum correctly
covers this case.

No independence of entry errors, calibration errors or repeated observations
is assumed. Native coefficients are combined before each interval radius
is evaluated.

## 2. Both temporal energy sums telescope

For a word i_1,...,i_H define

    alpha_t=T_{i_(t-1)} ... T_{i_1} c,
    beta_t=T_{i_(t+1)} ... T_{i_H} c,

with empty products equal to the identity. Alpha is the forward prefix
state immediately before operation t. Beta is the state reached by
applying the suffix in reverse chronological order, also immediately
before its reverse traversal would apply operation t.

Assume W>0 and R_i>=0 for each i. Forward telescoping gives

    sum_{t=1}^H alpha_t* R_{i_t} alpha_t
      = ||c||_W^2 - ||T_{i_H}...T_{i_1}c||_W^2
      <= ||c||_W^2.

The reversed path gives a distinct telescope,

    sum_{t=1}^H beta_t* R_{i_t} beta_t
      = ||c||_W^2 - ||T_{i_1}...T_{i_H}c||_W^2
      <= ||c||_W^2.

These identities do not require commuting or selfadjoint T_i. They do use
the same T_i on the forward and reversed paths, as stipulated in this
construction. Separately learned forward and dual maps require their own
two-budget normalization.

Let zeta=max_i zeta_i. Applying the preceding bilinear bound and then
Cauchy-Schwarz across temporal positions yields

    |sum_t beta_t* Delta_{i_t} alpha_t|
      <= zeta sqrt(sum_t beta_t*R_{i_t}beta_t)
               sqrt(sum_t alpha_t*R_{i_t}alpha_t)
      <= zeta ||c||_W^2.

There is no horizon factor or geometric-series factor in this conclusion.

## 3. Gram uncertainty and the complete midpoint allowance

Suppose the symmetric Gram uncertainty satisfies

    -gamma_G W <= Delta_G <= gamma_G W.

Every T_i is nonexpansive in W because R_i>=0. Therefore, writing
alpha_final=T_{i_H}...T_{i_1}c,

    |c*Delta_G alpha_final|
       <= gamma_G ||c||_W ||alpha_final||_W
       <= gamma_G ||c||_W^2.

Together, the true-moment signed predictor and its observed midpoint differ
by at most

    (gamma_G+max_i zeta_i) ||c||_W^2.

For H=0 the correction sum is empty and the same bound is conservative.
For H=1 native Gram terms cancel against their correction terms. The bound
does not rely on capturing every such additional cancellation, but the
code's midpoint agrees exactly with the fully combined native expression.

Conditional on the separately checked energy-remainder theorem, the total
all-word error bound becomes

    [2 theta^2 + gamma_G + max_i zeta_i] ||c||_W^2.

The noise proof itself does not require access to the physical operator or
a physical norm bound. The acquisition of theta^2 retains all of its own
previously stated premises.

## 4. Exact implementation and receipt checks

The code constructs each F_i entry through the established native defect
expression M_i-G T_i, then computes row and column radius sums. Its
dominate call accepts zeta_i only after the exact rational inequality
zeta_i R_i-D_i>=0 passes. Gram row-radius domination is valid because its
native expressions and radius matrix are symmetric. The numerical
eigenvalue calculation remains a proposal, not the proof.

The independent checker rebuilt every Gram and F_i expression directly
from dictionary state words and entries of T_i. For all 12 existing
receipts it verified the Gram domination, each computational budget, each
row/column diagonal, each rational zeta domination, and the revised total.
It did not rerun the completed inverse-dissipation acquisition review.

An additional two-column case used nonsymmetric coefficient maps, a
nonidentity W, and a genuinely nonsymmetric F_i radius matrix. Across 130
words, the checker verified both energy telescopes exactly, equality of the
matrix midpoint with the fully combined native midpoint, and that the
entire native interval radius was below the proposed uniform noise bound.
This is a synthetic implementation check, not additional physical source
acquisition.

The main g=0.001, eta=10^(-14) case has

    new uniform noise allowance = 3.2e-11,
    refined total bound = 0.001069081794.

All 12 refined receipts use zero additional source queries. Their previously
reviewed raw records, maps, dissipation acquisition and tail bounds remain
unchanged.

## 5. Precision and strict-gap interpretation

This theorem removes the explicit rho-based summation. It does not grant
bounded noise at arbitrarily weak dissipation without a corresponding
uncertainty condition. Already in one dimension,

    T=1-g,   R=2g-g^2,   uncertainty radius delta

requires zeta>=delta/(2g-g^2). Thus fixed instrument uncertainty becomes
expensive as g tends to zero. With T=1 and nonzero F uncertainty delta,
the H correction terms can accumulate to H delta; the required domination
fails because R=0.

Conversely, the mathematical theorem can cover nondecaying computational
directions when uncertainty vanishes in those directions and the remaining
noise satisfies its dissipation budget. The current implementation requests
R_i>0 and therefore does not implement every such semidefinite case.

The fixed denominator in the rational proposal routine introduces safe
conservative padding for very small bounds. For example, the main case's
Gram gamma is 2e-12 despite smaller decoded Gram uncertainty. This is a
computational rounding choice, not an instrument precision assumption.
The recorded decrease in the total bound should not be represented as a
large physical cost advantage.

The proof and exact checks support the new normalization and its reuse of
existing data. No new general energy-inequality principle, hardware
precision acquisition or physical cost claim is established by this review.
