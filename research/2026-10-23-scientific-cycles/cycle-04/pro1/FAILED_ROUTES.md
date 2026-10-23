# Failures and counterexamples that affect the continuation

## A direct iid extension would miss a real gain

The block entropy identity is `D(varrho||rho_c^tensor2)=2delta-epsilon`.
It bounds c squared by a constant times delta, not c by delta. A family with
c proportional to sqrt(delta) has entropy above3. Thus the bulk term
`2 alpha^2 beta^2 c` cannot be absorbed into a presumed `O(beta^2 delta)`
loss by the previous iid spectral argument. The exact block map, rather than
iteration of one-site maps through a correlated input, reveals the stabilizing
term. This was a falsified extension premise, not a failure of the old theorem.

## Same entropy with the opposite phase does not stabilize

Changing only c from -b/128 to +b/128 preserves the entire input spectrum but
changes bulk drift from -kappa to +3kappa. All boundary corrections are positive.
At beta<=1/8 the actual bath entropy then grows at least linearly and the pair
coherent-information rate is strictly below3/2. Complete inequalities are in
equation38. This counterexample uses the same device and actual initializer.
It demonstrates why input entropy alone cannot prove the new capacity gain.

## A global strict exponential contraction without a boundary is false

At beta0 and the critical product input the true root transitions are
(1/2,1/4,1/4) to depths0,1,2, whereas the bulk drift is zero. The root drift is
3/4. In general Phi*exp(tL)<=lambda exp(tL) with lambda<1 and no boundary
remainder contradicts exp(tL)>=I after iteration. The proof uses the actual
finite boundary remainder to obtain a bounded moment, not vanishing total mass.

## Arbitrary spectral types lose the compression implication

A type consisting only of a least-probable eigenvector has exponentially small
mass, not polynomial mass. Dividing an average tail bound by that mass can force
a linear cutoff and destroy the coding rate. The new proof uses a maximum-
probability type; a rounded near-eigenvalue type is separately proved as an
explicit alternative. Ordinary within-pair coherence does not invalidate this
operator type construction.

## Average overflow is still not arbitrary-reference recovery

The inherited examples remain decisive: one bad logical basis vector has mean
failure1/D and worst-case failure1; a maximally entangled logical-bath projector
has tiny bath average and unit joint norm. The r^2 positivity factor, spectral
expurgation, auxiliary CPTP normalization, and polar repair are retained.
No physical implementation of the auxiliary normalizer is permitted.

## Routes already closed stay closed

The unchanged parent preserves the balanced-only dimension ceiling, diagonal
bias obstruction, stronger product-stationarity entropy ceiling, finite-reflecting-
cutoff limitation, and exact high-entropy single-site iid escape/information
theorem. Depth growth alone and entropy alone remain insufficient for arbitrary-
rank claims. The new theorem avoids these failures through a different actual
input operation and a complete infinite-bath tail plus coding proof.

No long-time finite-cutoff simulation or efficient encoder was attempted. At the
fixed tiny drift, honest simulated mixing horizons or explicit code construction
would be far beyond the finite symbolic evidence used here. The proof does not
claim such simulations or hide them in replay time.
