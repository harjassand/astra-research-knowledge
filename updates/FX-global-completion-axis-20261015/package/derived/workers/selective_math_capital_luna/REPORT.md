# Selective mathematical capital retrieval: openai/math

**Status:** source-derived bounded review; no theorem transfer established.

## Pin and selection

At retrieval time, `git ls-remote https://github.com/openai/math.git HEAD` returned commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a`. This is the same pin named in the task, so no repository update was detected. The pinned catalogue says 719 manuscripts in 372 families. The repository README also says that results have mixed verification status and that not every manuscript has a Lean formalization. Catalogue presence is navigation evidence only.

The catalogue map was filtered for quasiconvexity, rank-one convexity, SOS or positive-polynomial representations, semidefinite moment matrices, matrix convexity, and PSD rank. It contains no direct proof for either current interface. I inspected three nearby proofs: one no-lift theorem for a specially constructed hyperbolicity cone, one direct-LMI obstruction for another hyperbolicity cone, and one PSD-rank lower bound for matching slack matrices. The earlier critical-Ising and inverse-boundary proofs at this pin were not repeated.

## Proofs inspected

### 1. No finite semidefinite lift for a constructed hyperbolicity cone

Theorem 1.1 of [Hyperbolicity Cones Without Semidefinite Lifts](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Hyperbolicity-Cones-Without-Semidefinite-Lifts-October-5-2026/nonliftable-hyperbolicity.pdf) asserts existence of a real homogeneous hyperbolic polynomial whose entire closed hyperbolicity cone has no exact finite affine semidefinite lift, allowing arbitrary real coefficients and any finite number of auxiliary variables. The theorem is existential and does not give a lower bound for a particular fixed-size representation.

The construction starts with a homogeneous quadratic matrix map Q from a 330-dimensional space of quartic functionals to symmetric matrices, with Q(y) positive semidefinite for every real y. It uses a rank-20 Hankel seed on the 36-dimensional space of quadratic forms in eight variables. A finite inverse-limit argument produces a positive matrix-valued quadratic map; a degree-four polynomial patch and a positive truncated-moment functional then yield a negative order-epsilon-four trace gap. A hypothetical lift gives local analytic Gram factors and feasible approximants within order-epsilon-sixteen; the resulting inverse perturbation is order-epsilon-eight, too small to remove the order-epsilon-four gap.

The construction chooses N greater than 10 times 36 squared and sets r = 20N - 1. The smallest integer meeting that strict bound is N = 12,961, hence r = 259,219 and determinant block size n = r + 1 = 259,220. The associated determinant polynomial has degree n(n + 1) = 67,195,267,620 and ambient dimension n(n + 1) + 330 = 67,195,267,950. These dimensions make the result a structural existence theorem, not a tractable candidate representation for the present nine-coefficient problem. Its seed proof uses exact rank checks over F7 on small blocks (at most 35 quartic rows per weight). The paper describes a reproducing script, verify_certificate.py, but that script was not listed in the pinned preprint directory and was not replayed here.

**Applicability.** For compatible positivity, this is at most a template for an adversarial representation argument: one would need to encode the target coefficient cone as an appropriate section or image of the constructed epigraph interface, or independently reproduce its local moment and Gram-factor obstruction. No such embedding or implication is established. It does not turn a failed Gram search into a quasiconvexity counterexample. For the axis tensors, its positive functionals are truncated algebraic moment functionals and need not come from measures; the proof does not identify a physical volume-weighted tensor M from an order-weighted tensor W.

The linked [Lean scope note](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/docs/095.md) concerns the separate degree-20, 23-variable direct-LMI example below. It does not formalize this October 5 no-lift theorem.

### 2. A direct-LMI obstruction from a positive biquadratic form

Theorem 1.1 of [A nonspectrahedral hyperbolicity cone](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/A-Nonspectrahedral-Hyperbolicity-Cone-September-24-2026/nonspectrahedral-hyperbolicity-cone.pdf) constructs a hyperbolicity cone in 23 variables that is not representable by a homogeneous real symmetric LMI in those same variables. Its degree-20 determinant has a degree-16 quotient defining the same cone. The proof takes the coefficient-one Choi–Lam nonnegative biquadratic form b(z,y), whose only bilinear square dominated by b is zero, and builds a positive map from it. Any putative pencil yields an exact operator-norm identity for moving kernel projections; differentiating one projection on a constant-rank neighborhood forces a bilinear square dominated by b, a contradiction.

The local interface is small: z and y each lie in R3, the auxiliary positive map acts on 4-by-4 symmetric matrices, and the proof uses finite-dimensional pencil blocks. The paper is 14 pages and gives explicit formulas. The result only excludes a direct pencil in the original coordinates. The pinned catalogue describes a [companion exact lift](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/An-Exact-Semidefinite-Lift-of-a-Nonspectrahedral-Hyperbolicity-Cone-October-5-2026/Exact-Semidefinite-Lift-of-a-Nonspectrahedral-Hyperbolicity-Cone.pdf) of this same nonspectrahedral cone using a 100-by-100 pencil and 307 auxiliary variables. Thus this proof cannot be read as a no-lift result.

**Applicability.** The proof offers a concrete obstruction pattern if the target acoustic or positivity structure can be shown to force a nonzero bilinear square beneath a weakly extremal positive biquadratic form. The present quartic cone has not been mapped to this Choi–Lam form, and the needed pencil-to-kernel identity is absent. The theorem gives no bound or certificate for the current quartics. The separate lift result also cautions against promoting failure of a same-coordinate LMI to failure of all finite lifts.

### 3. Exponential PSD rank for shifted matching slack matrices

Theorem 1.1 of [Exponential PSD rank of positively shifted matching matrices](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Exponential-PSD-rank-of-positively-shifted-matching-matrices-October-5-2026/shifted-matching-psd.pdf) considers even n, rows indexed by odd vertex subsets U, columns by perfect matchings M of the complete graph, and exact entries |M intersect delta(U)| - 1 + rho. For each fixed 0 < rho < 1, its real PSD rank is at least 2 to the power c n for all sufficiently large even n. The matching-polytope lift consequence is also exponential. Factors are arbitrary real PSD matrices with exact trace pairings; the theorem imposes no symmetry or precision restriction.

The proof encodes a parity contradiction on a fixed-degree expanding bipartite multigraph, uses constant-size cells and local averaging, and converts a small PSD factorization into low-degree matrix sums of squares. A signed separating functional then contradicts the factorization. The proof fixes d = 100, beta = 1/100, tau = 1/1000, then chooses a sufficiently large fixed cell size k; it states the exponent c = 1/(2k), independent of rho, while the threshold n0 may depend on rho. This is an asymptotic exact-factorization proof, not a numerical algorithm for 3-by-3 moment tensors.

**Applicability.** PSD rank here is the minimum common factor size reproducing a combinatorial slack matrix by trace inner products. It is not the ordinary matrix rank or support-identification problem for M and W. No reduction from those tensors or from the invariant quartic cone is supplied. The linked [Lean scope note](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/docs/126.md) records selected superpolynomial lower bounds for an unshifted slack matrix; it explicitly does not claim the paper’s exponential theorem for every fixed positive shift. No Lean code was checked in this retrieval.

## Outcome for the two active interfaces

For compatible positivity in invariant 2-by-2 quartics, the only potentially useful item is the method pattern in proof 2: a positive biquadratic form can obstruct a proposed LMI when the geometry of every hypothetical representation forces a dominated square. There is no justified transfer to the current nine-coefficient quartic cone, and no new necessity, sufficiency, or coefficient bound follows.

For W = integral S-squared n n-transpose and M = integral n n-transpose, no inspected proof identifies volume-weighted M from order-weighted W. Proofs 1 and 3 use algebraic or combinatorial factorization objects with different quantifiers and inputs. They do not modify the current identified set or its acquisition assumptions.

All theorem statements above remain claims made in the pinned released sources. This retrieval did not independently verify the proofs, reproduce the F7 certificate, or validate historical priority.
