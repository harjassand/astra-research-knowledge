**Completed a positive representation for conditioning independent matrix formulas, with exact counting, deterministic witnesses and exact uniform sampling of the original inputs.** The comparison changed the attack: a simpler representation handles the entire admitted class without internal rank filters, while the new rank-sum construction supplies a complementary, broader operation.

### Positive closure under addition and multiplication

Let \(D_h^{m,n}\) be the output law of two independent uniform matrices of shapes \(m\times h\) and \(h\times n\), and let \(U^{m,n}\) be the uniform matrix law. Independent addition satisfies

\[
D_h+D_k=D_{h+k}.
\]

Ordered multiplication also closes positively:

\[
D_h^{m,d}D_k^{d,n}
=\sum_r\left(\sum_j\rho_{h,d}(j)\rho_{j,k}(r)\right)D_r^{m,n},
\]

where \(\rho_{a,b}(r)\) is the explicitly computed rank distribution of a uniform \(a\times b\) matrix. Uniform components have corresponding closed rules.

The resulting mixture has polynomial support: every finite label \(h\) is bounded by the sum of multiplication inner dimensions in the formula. Exact conditioning reduces to retained complete-product samplers on chains of two to four factors, followed by actual affine reconstruction of the original inputs.

The multiplicity issue is resolved explicitly. **Auxiliary factors describe output distributions; they never become additional counted inputs.** Counts are \(2^N P(Z)\), with original affine kernels and unused bits retained. After choosing an auxiliary component and actual child outputs, the algorithm samples each child’s *full original fiber*. The proof establishes that this produces the correct uniform original-input measure.

This removes the product-only restriction for complete-output conditioning through independent sums and products, including arbitrary alternation of those operations.

### Distinct admissions remain explicit

| Construction | Information required | Completed operations |
|---|---|---|
| Positive product mixtures | Supplied characteristic-two field coordinates, independent formula, full affine leaf maps; no internal rank filters | Count, witness, exact uniform original-input sampling |
| Rank-convolution formulas | Supplied formula and maps, with explicit rank predicates permitted | Count, witness, exact uniform original-input sampling |
| Raw compiler | Ordinary Boolean gates within the proved partial \(\mathbb F_2\) recognition class | Acquires local matrix charts, banks, gauges and targets, then performs the corresponding construction |

The raw compiler reads no hidden dimensions or decomposition annotations. Its exposed-cut admission and acquisition budgets remain material. Failed recognition is a decline; an inconsistent recovered target is a certified empty fiber.

The rank-filter boundary is mathematical. Every positive mixture of \(D_h\) and \(U\) assigns positive probability to zero. A nonempty source constrained to positive exact rank cannot belong to that representation.

I instantiated the separating case

\[
X+Y=\operatorname{diag}(1,1,0,0),\qquad
\operatorname{rank}X=\operatorname{rank}Y=2
\]

over \(\mathbb F_2\). An independent census of all \(65{,}536\) possible \(X\) established **1,418 decompositions**. The rank-sum construction counts and constructs this fiber; the mixture consumer correctly declines its rank predicates. This is a literal rank-predicate result, separate from raw acquisition.

The rank-sum branch also now has a reviewed complete-pair rank/unrank bijection. Its conditioning admission covers whole initial matrix rows and coordinate pins in the next row; arbitrary original-input prefixes remain outside that claim.

### Verification and equally informed comparison

The mixture implementation passed producer controls covering **71,432 original assignments and 124 targets**. A separate independent review checked **4,576 assignments, 44 targets and 12,165 exact rational sampling paths**, including overlapping auxiliary components. Guards confirmed that it called neither the new rank-sum machinery nor the original rank-convolution constructor.

On the **same original circuits and output task**—exact count, one witness and eight exact uniform assignments—the positive rank route, classical signed rank route, product-mixture route and ordinary CNF compilation route all completed. They agreed on counts **1,144** and **9,152**. Acquisition, representation, reconstruction, gate checks and output encoding were charged. These results establish no speed advantage. Classical rank-intersection formulas remain a valid counting alternative. :chatgpt-content-reference{index="0"}

The literature check also identified clear antecedents for the mixture atoms: reducing Bufetov–Qiu’s outer-product and Haar constructions to the residue field gives these families. Their atom family and Fourier fingerprint are therefore prior machinery. Historical priority for the complete conditional compiler is not claimed. :chatgpt-content-reference{index="1"}

Proofs, executable constructions, exact controls, failed admissions, the control-setup correction and version-bound reviews are preserved in place under:

`producer-workspace/rank_composition`

The substantive gain is a reusable method for **constructing original inputs under complete matrix-output conditions across independent additive and multiplicative structure**. Earlier shared-prefix product trees and other complementary constructions retain their separate admissions. Arbitrary shared-input circuits and unrestricted polynomial counting remain unresolved; the civilisation-level mission remains the larger objective.
