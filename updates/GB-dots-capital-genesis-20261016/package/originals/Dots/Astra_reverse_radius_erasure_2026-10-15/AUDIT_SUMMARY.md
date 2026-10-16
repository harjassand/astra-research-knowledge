# Mathematical reconstruction and reproducibility scope

The supplied proofs have been internally checked by an independent mathematical reconstruction. This is not external peer review, a priority determination, or a formal proof-assistant verification.

## Classical conditional RLD theorem

The reconstruction checked the small SDP upper certificate, noncommuting factor order, coercive minimax, common-positive-row convention for zero entries, weighted-simplex inverse identity, faithful limits, and same-dimension Hermitian realization. It also checked the active-support bound min(m,n)-1 for nonconstant strictly positive targets and the m-1 sufficient bound for general targets. The free center u must not be normalized to sum one.

The independent exact script verifies the cyclic value 2/11, a physical qubit-reference witness, and a nonuniform prior (1/9,4/9,4/9) whose frame lower value is 1382/8645. A separate Fraction-only test verifies the zero-common-support exclusion value 1. These examples supplement the general proof.

## Classical SLD and MMSE interpretation

The reconstruction explicitly checked the positive-channel signed-lift covariance criterion, operator sum-of-squares argument for arbitrary reference observables, and the one-coherent-flag converse. It checked faithful normalized binary states and equal reference marginals in the finite counterexample. The proof document additionally explains the common-support extension and endpoint conventions.

The threshold equality applies to unrestricted finite references. It neither equates the SLD and RLD metrics nor transfers a fixed-memory RLD formula to fixed-memory SLD. General signed-lift machinery and the measured/SLD-MMSE dictionary are credited precedents.

## Faithful quantum outputs

The reconstruction checked matrix weighted Cauchy, the harmonic minimax, the block Schur complement, same-dimension Hermitian frame realization, min(m,d²)-1 sufficient RLD reference bound, vectorization convention in the small SDP, and product-radius composition. Singular prepared states are excluded.

It separately verified the noncommuting purification orientation in the operator variance bound, the quantum-output observable compiler, and the one-flag Sylvester-limit converse for ordinary, unsmoothed complete SLD/MMSE order. A sufficient strict-violation witness reference dimension is min(m,d²), not a minimality assertion.

An independent rational-complex joint-observable test verifies the Pauli three-state radius 3/11, its center, each reverse chi-square 3/8, and the compiled second-moment inequalities. The constructor's exact frame test independently gives input defect 2/3 and output defect 2/11, hence ratio 3/11.

## Ordinary Pauli coefficients and finite decision witness

The ordinary SLD determinant certificate and positive leading-minor identity were independently checked. The ordinary RLD and SLD values at a=3/5 are respectively 9/41 and 9/50; the complete threshold is 3/11. These distinct values reinforce that ordinary SLD and RLD cannot be interchanged.

A separate independent script solves the full 6-by-6 output Sylvester equation for the three-level-reference finite binary witness, rather than using the constructor's reduced off-diagonal equation. It verifies the exact positive metric margin, all state principal minors, and the finite normalized MMSE gap. The amplitude-1/10000 construction is an existence certificate, not a practical experiment or sensitivity estimate.

The separately conditioned q=1/5 fixture has also passed an independent full-output Sylvester solve and strict principal-minor checks for both state eigenvalue bounds. Its gap is approximately 0.007855003215346228. This fixture establishes ordinary SLD/MMSE dominance at q=1/5 and failure with a reference; q=1/5 does not exceed the ordinary RLD threshold 9/41. The earlier q=6/25 tiny-gap fixture establishes both ordinary dominance statements. Neither fixture is a hardware demonstration or a cross-task performance comparison.

## Bounded loss and computation

The exclusion-family limitation has an all-reference trace-norm proof in COROLLARIES.md, plus exact rational examples for m=3,8,100. Example checks are not substitutes for that general proof.

The optional numerical optimizer is not trusted to certify its own answer. Only exact rational primal and dual evaluations determine its interval. The sample zero-gap certificate is independently checked without SciPy. This package establishes no exact-P complexity claim, no universal polynomial bit bound, and no hardware performance result.

## Fixed receivers and sampling

The independent reconstruction additionally evaluates first and second loss moments directly from each conditional state and the full optimal observable. It confirms the variance sum below 77/200, gap above 157/20000, and certified receiver norms below 43/100 and 53/100. The Bernstein bound uses 2n independent centered arm variables with individual bound 53/25; that number is not used as a paired-difference bound. Rational exponential-series certificates in the package prove the sufficiency of 37,973 and 185,705 trials per arm for the two stated guarantees. Rounded 40,000 and 190,000 counts are conservative.

The separate worst-case bound Delta-4 delta-8 kappa assumes normalized qubit outputs with per-output operator error at most delta, each binary input perturbed by trace distance at most kappa, and the ideal target receiver left unchanged. It is a model-error certificate, not an observed noise tolerance or implementation guarantee.
