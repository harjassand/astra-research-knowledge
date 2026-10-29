# A warranted rank-one response can improve finite-data cancellation accuracy

29 October2026. Optional stronger-interface corollary suggested during review.
Not part of the general finite-data theorem unless root explicitly adopts it.
It is elementary spectral perturbation; no priority claim is made.

Suppose physical structure, independently of the fitted data, guarantees that
one conditional residual Gram has EXACT form

    H=lambda u u^T,  ||u||_2=1,  lambda>0.

For example, all primitive conditional response residuals may have a single
common unknown scalar hidden dependence, with different amplitudes. The
one-factor affine frozen-disorder construction has this property. A small
empirical second eigenvalue does not establish the premise.

Let symmetric Hhat satisfy ||Hhat-H||_op<=eta and eta<lambda/2. Take a unit
largest-eigenvalue eigenvector uhat. Choose an implemented simplex vector p
such that uhat^T p=0, while retaining the prescribed useful-output and resource
constraints. Feasibility must be checked. Opposite response signs with adequate
margin are one simple sufficient setting; a residual nullspace alone does not
provide a useful admissible p.

The actual squared residual obeys

    p^T H p <= lambda eta^2/(lambda-eta)^2 ||p||_2^2
            <= 4 eta^2/lambda.                          (1)

Proof. The top empirical eigenvalue lambdahat>=lambda-eta. Project
Hhat uhat=lambdahat uhat onto the orthogonal complement of u. Since H has no
component there,

    lambdahat ||(I-u u^T)uhat|| <= eta.

The angle between the two one-dimensional subspaces thus has sine at most
eta/(lambda-eta). Since p is orthogonal to uhat, |u^T p| is at most this sine
times ||p||. Finally ||p||<=1 for a simplex vector.

A fully numerical confidence bound can avoid unknown lambda by using
lambda_lower=lambdahat-eta>eta and lambda_upper=lambdahat+eta:

    p^T H p <=lambda_upper eta^2/(lambda_lower-eta)^2.

This bound is conservative but directly checkable. If matrix entry radius is
d, the operator error eta<=s d suffices for s primitives; better matrix
concentration may improve constants but is a separate acquisition claim.

Unlike the generic finite-confidence upper bound O(eta) on squared residual,
this uses the WARRANTED rank-one structure to obtain O(eta^2). Independent
bounded reports typically give eta=O(N^-1/2), so residual norm becomes
O(N^-1/2) rather than O(N^-1/4). The constant deteriorates with the true
nonzero spectral gap, and useful-output feasibility can also be fragile.
The real covariance signal in the example is small, so the asymptotic
improvement does not itself demonstrate an affordable sample count.

Estimated visible means still contribute their own M error to the positive
reference. Implementation probability errors, baseline mass ratios, source
preparations, selector disposal, side records and all calibration/deployment
conditioning requirements remain separate. In particular a data-dependent p
needs the same conditional deployment-H density qualification identified in
ROOT_CANCELLATION_FINITE_ERROR_REVIEW.md.

A higher-rank version replaces the top eigenvector by the estimated range and
requires a known true rank r plus a certified gap lambda_r>eta. A standard
subspace perturbation argument suggests

    p^T H p <=lambda_max [eta/(lambda_r-eta)]^2 ||p||^2

for p in the estimated nullspace. Only the rank-one case is proved directly
in this note. No general numerical implementation or end-to-end acquisition
experiment has been performed for this corollary.
