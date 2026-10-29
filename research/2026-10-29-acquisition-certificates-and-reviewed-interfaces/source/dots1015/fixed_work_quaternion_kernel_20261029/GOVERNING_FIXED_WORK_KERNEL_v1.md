# Bounded proposal work with an always-sound quaternion gap

2026-10-29 — receiving review requested. This is an executed classical kernel in a fixed-size arithmetic model, not a measured physical source-clock or universal tight-optimization guarantee.

## Contract
Input: a valid rational homogeneous four-variable quartic F. Output: an exactly rational unit quaternion q, an exactly checkable global lower bound ell, and visible nonnegative gap e=F(q)−ell. No target-gap test aborts the controller. Always retain ell>=−A, A=sum absolute coefficients, so e<=2A. Bad quality is recorded rather than called success at a requested accuracy. Under the stated floating primitives, all proposal loops have fixed declared finite caps; exact verification does not trust numerical optimality/eigenvectors. Input validation errors and physical/computational faults are not declared successful oracle outputs.

## Fixed proposal budgets
Normalize by scale=max(1,A). Thirty-one deterministic starts (four coordinate vectors and27 rational stereographic grid points) each receive32 tangent Newton iterations with8 tested line-search slots. Directions are projected/clipped; singular/non-descent Newton solves use bounded gradient directions. The best feasible numerical direction is rounded by an exact stereographic formula at24bits.

The affine10×10 Gram family has20 free coordinates and scalar lambda. A floating barrier proposal uses9 declared barrier levels,16 Newton iterations each and16 line-search slots each, all slots processed even if an earlier trial passes. There are2304 line-search Cholesky slots, plus bounded current-matrix factorizations/reset checks. Invalid/non-descent directions fall back conservatively; all accepted proposal coordinates are capped in absolute value by2^16. Rational lambda/free coordinates use40bit dyadic rounding.

Twelve full Jacobi sweeps over45 index pairs propose a generalized-eigenvector basis, rounded to32bits. A nonfinite/out-of-range basis proposal falls back to the identity. These are NOT trusted eigendecompositions and do not establish a global minimum. Matrix primitives have fixed dimensions; rational work is bounded in bit length by the public input-bit bound plus fixed precision budgets. Runtime measurements do not prove hardware timing isolation. The implementation still needs an external release/padding interface if the source can observe computation time.

## One-pass exact congruence repair
Let z contain the10 degree2 monomials. The exact affine Gram G satisfies F/scale−lambda Q²=z^T Gz, Q=sum q_i². Let D=diag(1 on q_i² monomials,2 on q_iq_j monomials), so Q²=z^T Dz and D is positive definite.

For ANY rational proposed basis V compute A0=V^T G V and B=V^T D V. If b_i=B_ii−sum_{j!=i}|B_ij| is not strictly positive for every row, replace V by I, which always makes B=D and b_i>0. Define

 delta=max(0,max_i [sum_{j!=i}|A0_ij|−A0_ii]/b_i).

Triangle inequalities show A0+delta B is diagonally dominant with nonnegative diagonal, hence PSD. Strict diagonal dominance makes B positive definite, which proves V invertible (otherwise V^T D V would be singular). Therefore G+delta D is PSD, and (lambda−delta)*scale is a global lower bound on F over the sphere. Take the maximum with−A. There is no iterative rational repair search or assumption that the floating basis is orthogonal.

The exact verifier checks the polynomial identity, rational unit norm, strict DD of B, weak DD of A0+delta B, exact upper/lower/gap and coefficient-range cap. A singular all-zero basis fixture correctly falls back to I. Gram positivity is certified by a change of basis, not by extracting a physical encoder from a relaxed PSD matrix; q is separately feasible.

## Executed evidence
- The pure rational coordinate-search/DD prototype uses100 objective evaluations and541 Gram scores. Six retained-bank mean-loss gaps are0.175–0.321: poor lower bounds, preserved as a useful failed baseline rather than hidden.
- The bounded full-Gram/Jacobi kernel exactly verifies all six retained banks. Mean-loss gaps are5.16e−8–9.61e−8, and its rational candidates equal the earlier ordinary SLSQP candidates on all six cases. Measured total times are0.41–0.55s per case including verification, not a worst-case clock claim.
- OFFLINE replay of360 old FTPL queries exactly verifies all returned certificates. Gaps range0.00013949–0.00029445, median0.00021439. Per-edge realized gap sums divided by T R are9.24e−8–9.39e−8; this is NOT an expected-gap estimate or a new quantum history. Full replay/cache/verification took188s. A first run completed numerical work but failed while serializing enormous exact aggregate fractions; the durable-cache rerun completed. Raw exact per-query certificates are retained, while a separately verified dyadic counter avoids LCM-denominator growth.
- Zero polynomial returns exact gap0. Negative constant and deliberately singular-basis cases verify. The known non-SOS Choi–Lam quartic returns gap0.0341885, visibly failing a small target; no tightness is asserted there.

The newly running actual three-role simulation is a separate artifact/receipt scope; this contract and offline evidence do not certify it or any outer-code readiness event.

## Prior machinery and limitations
Diagonal-dominant Gram certificates are standard DSOS-type sufficient conditions, not an Astra invention: Ahmadi–Majumdar, arXiv:1706.02586 (primary abstract retrieved). Our weak DD coordinate search is not a proof of the optimal DSOS relaxation value. The stronger candidate/global-SOS methods already reproduce the same encoders. No unique quantum protection advantage or historical novelty is inferred.

The accepted variable-gap and observable-gap theorems may consume sound reported gaps under their source/probe/privacy assumptions. Candidate-dependent timing leakage can invalidate learning/readiness even if the original guard remains sound with hidden role/key choices. No one should conflate those privacy requirements. The fixed-budget solver need not be uniformly accurate; small gaps on all future queries, physical calibration, trusted buffers and a complete release-clock architecture remain unresolved. The theoretical complete algebraic/grid solvers remain separate fallbacks, not silently invoked here.
