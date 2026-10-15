# Independent scaffold audit

## Verdict

The conditional identification certificate is mathematically sound under its stated exact-data and promised-model premises, with implementation qualifications below. Its completeness proof is substantive: finite real root enumeration, unique pair completion, and the star condition together cover every admissible model without enumerating an exponential product. This is not a completed generic acquisition theorem or an implemented practical learner. The documents supply no exhaustively solved nontrivial instance that passes all gates, and do not establish that the joint pass gate is nonempty for arbitrarily large m. The existing numerical extension experiments cannot fill that gap.

I independently checked the modular Jacobian receipt, the symbolic pair equation, weighted-transpose invariance, and a positivity counterexample. Replay: `python audit_scaffold_checks.py`. The script does not import the original witness generators and does not overwrite their receipts.

## 1. Exact algebraic enumeration

For a subset S the correct polynomial equation is

`g(S) det(I+B_SS) - a_S^T adj(I+B_SS) 1 = 0`,

accompanied by `det(I+B_SS) != 0`. Clearing denominators alone is not sufficient. One may use real semialgebraic solving with these inequations, or saturation followed by the original inequation checks. Merely solving the Zariski closure of the rational fiber and retaining its boundary would be incorrect. Conversely, silently discarding a positive-dimensional component because an optimizer did not find points on it would be incorrect.

The seed has fixed dimension 20 and maximum polynomial degree 5. When the complex saturated fiber is zero dimensional, a coarse isolated-root Bezout bound is 5^20 = 95,367,431,640,625. This is independent of m but already illustrates how misleading “constant-size” can be as a practical claim. It is a bound, not a prediction of the actual number of roots. If only the real valid fiber is finite while the complex fiber has positive dimension, use real algebraic decomposition; the same simple complex zero-dimensional argument cannot be invoked without qualification. Fixed-size semialgebraic bounds still give a constant bound on the finite real solution count.

For a fixed seed C, the extension equations can actually be written with degree at most two in the ten new entries using the displayed Schur formula. All seed-context inverses are constants at this stage. Thus the stated degree-at-most-six bound is safe but loose. A complex isolated-root Bezout bound of 2^10 applies to this quadratic formulation under the corresponding zero-dimensional hypotheses. Real root isolation must distinguish every root and verify all original rational equations and denominator inequations.

Positive-dimensional real fibers correctly cause an inconclusive result unless the entire branch is rigorously eliminated. A finite list discovered numerically is not a substitute. There is no requirement that finite roots be nonsingular: multiplicity or a singular Jacobian at an isolated root must not cause that root to be dropped.

The full-rank witness proves generic finiteness in the joint parameter domain. It does not prove finite fibers at every instance, nor automatically at every individually prescribed nonzero vector a. The step-1 gate handles exceptions. The generic finite-extension statement for the true generic seed can also be justified from the six-node full-rank result: seed-only rows fix twenty seed directions, so the remaining ten attachment directions have full rank generically. This does not control spurious seed branches.

## 2. Singular branches and completeness

The pair linear equation is correct: symbolic expansion gives exactly `h D - N = 0` for the numerator N and denominator D in RESULTS.md. For a nonsingular 3-by-3 coefficient matrix, every true completion must equal its unique solution in `(x,y,xy)`. The additional `z=xy` and all-context rational checks are essential and sufficient for the queried pair observations.

The conservative requirement that *every* candidate pair have nonsingular coefficient matrix is safe. A singular matrix is not proof that the candidate pair is impossible; reporting inconclusive preserves completeness. This conservatism can greatly reduce success, because even a spurious combination that could eventually be eliminated elsewhere triggers failure. No evidence establishes that all such spurious combinations avoid singularity generically.

No unhandled singular branch was found in the mathematical specification, provided “enumerate ALL real solutions” is implemented literally and dimension is tested on the valid real locus or treated conservatively on the complex locus. At the end, an empty retained list must be reported as inconsistency with the promised model, rather than attempting to choose B*. This case should be explicit. For m<=5 the full-table fallback is sufficient for map prediction without reconstructing B. For one outside node star rigidity is vacuous and its finite candidates can simply be checked. With at most two outside nodes the acquisition schedule itself is the entire binary table.

## 3. Star rigidity really is sufficient

Fix a seed and a reference r satisfying the stated property. Every complete compatible assignment has a value c at r. Each other value must be in the compatibility set for `(r,c)`; this set has size at most one. If it is empty there is no such assignment. Otherwise there is exactly one possible whole assignment for c, which is accepted only if every pair relation passes. Therefore no compatible assignment is lost and there are at most D retained assignments per seed.

This proof does not assume that the relations are equivalence relations, that compatibility is transitive, or that the reference edges alone are enough. The all-pairs check is indispensable. Searching all references does remain polynomial. Constant alphabet without star rigidity would not imply polynomial enumeration or a polynomial-time solution to an arbitrary binary constraint problem.

## 4. Entire-map certification and positivity

Put A=diag(a) with all a_i nonzero, and B'=A^-1 B^T A. For each S,

`I+B'_SS = A_S^-1 (I+B_SS)^T A_S`.

Consequently the determinants agree, and

`a_S^T (I+B'_SS)^-1 1 = 1^T (I+B_SS)^-T a_S = a_S^T (I+B_SS)^-1 1`.

The final equality-or-weighted-transpose check is therefore sufficient for equality of every response and for transferring all-subset nonsingularity from the true promised model. It must be a single global transpose choice for each retained matrix, not a separately chosen transpose for each edge or block. The text correctly requires the global version.

The promise that a valid true model exists is important. Without it, nonsingularity on measured subsets alone does not certify nonsingularity on unmeasured subsets. No standalone feasibility certificate for arbitrary data has been established.

The documents state no additional physical positivity domain. Enumerating an unrestricted real superset is safe for identifying the response map: it includes every positive physical model, and may only cause unnecessary rejection. If the intended output is itself required to be physically feasible, that requirement needs to be specified and checked.

- If a_i>0 and B is entrywise nonnegative, weighted transpose preserves entrywise nonnegativity. For mixed-sign a this is not automatic.
- Positivity of each internal vector `(I+B_SS)^-1 1` is *not* preserved. For a=(1,10) and B_12=B_21=1/5, the full-state internal vector is (5/6,5/6). The weighted transpose has entries B'_12=2 and B'_21=1/50 and internal vector (-25/24,49/48). Both matrices are entrywise nonnegative, nonsingular on every subset, and have the same response map.
- Positivity constraints on the scalar response itself are preserved by map equality; positivity of hidden states or other unmentioned physical parameters is a separate question.

Thus the claimed map certificate is sound, but it cannot be relabeled a positivity/physical-realizability certificate without specifying which positivity notion is intended.

## 5. Polynomial dependence and exact-number representations

For rational readings with maximum input bit length L, local seed and attachment algebraic solving has fixed numbers of variables, equations and degrees. Standard exact fixed-dimensional algorithms give polynomial bit dependence on L, with potentially enormous fixed constants. A bounded-degree algebraic representation with isolating data is needed; arbitrary real oracles do not give this finite-bit statement. More general exact input formats must explicitly bound their representation size and degree.

There is no need to build one number field containing every node's coordinates merely to verify the certificate. Each pair test involves the seed and two attachment candidates, hence only a bounded number of bounded-degree algebraic numbers. Each entrywise comparison between retained global matrices also involves a bounded number of such local fields. Keeping these operations local avoids an artificial exponential compositum in the acquisition/certification phase. Subject to this implementation choice, the claimed O(m^2) or naive O(m^3) constant-size arithmetic bounds have a credible polynomial-bit counterpart for rational inputs.

Prediction is more nuanced. A complete candidate matrix has O(m^2) locally represented algebraic entries. A generic m-dimensional exact inversion can combine all these fields. If each successive attachment contributes degree at most d over the seed field, the naive compositum degree bound is C0*d^(m-5), exponential in m. Constant degree *per entry* does not prevent this. A finite number of real global candidates also does not itself bound complex algebraic degree. The documents prove no special field-collapse theorem for this model.

This is an upper-bound warning, not a demonstrated exponential-degree example satisfying every scaffold gate. A prediction may be kept as the original matrix solve or a polynomial-size arithmetic circuit (for example a division-free determinant/adjugate circuit and one final division), avoiding a dense minimal-polynomial expansion. Converting that representation to a canonical isolated algebraic root, or proving uniformly efficient correctly rounded evaluation near a pole, is not covered by the stated operation count. If the true B is additionally promised rational and the final orbit test succeeds, both orbit members are rational for rational a, which removes this particular algebraic-extension issue; that is an extra promise.

There is also an unavoidable output-size distinction: answering a requested subset via a solve is different from printing the entire 2^m-row response table. The latter has exponential output length.

## 6. What the evidence establishes

Independent exact replay confirmed the receipt's prime and the 20-by-20 modular determinant 473745, reconstructing the rational Jacobian entries before reduction. It confirms the generic full-rank premise and the associated one-anchor obstruction, subject to the open-domain assumptions in RESULTS.md. These are not conditioning guarantees.

The two-anchor local-identifiability theorem and one-anchor dimension obstruction are sound in the stated generic real model. If physical constraints contain a nonempty open parameter region, the generic argument intersects that region; it need not apply unchanged to a lower-dimensional physical constraint family.

Neither the rank receipt nor the pair witness supplies an exhaustive seed inverse or verifies the joint scaffold pass gate. The multistart extension experiment is only a search result. The next decisive mathematical or computational deliverable is an exhaustive certificate for a nontrivial growing-m family, or a theorem establishing generic uniqueness/alignment and eliminating all spurious and singular branch failures. Until then the proper claim is “conditional sufficient identification certificate with polynomial m-dependence,” not “complete generic polynomial-time learner” or “practical acquisition method.”
