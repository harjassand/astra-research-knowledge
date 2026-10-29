**I changed the target from recovering a smaller linear state to discovering a reversible information decomposition of a nonlinear computation.** The completed construction acquires both the observable information and the minimum additional information needed to reconstruct every original input. I then extended its acquisition path so that it can operate directly on ordinary Boolean gate DAGs without expanding their ANFs.

The larger consequence sought is automatic, exact inference through nonlinear computations: discovering coordinates in which conditioning, reconstruction and sampling become tractable. This turn establishes a restricted but constructive instance of that principle.

## The completed principle

For an admitted observation \(G:\mathbb F_2^n\to\mathbb F_2^m\), the algorithm discovers its actual affine image, of dimension \(r\), and a linear map \(J\) on the **original inputs** such that

\[
\Psi(x)=\bigl(\text{coordinates of }G(x)+G(0),\;Jx\bigr)
\]

is a bijection on \(n\) bits.

The \(n-r\) bits in \(Jx\) attain the minimum possible fixed-length reconstruction information: each observed output has exactly \(2^{n-r}\) originals. The algorithm acquires a decoder through successive linear solves and evaluations of the actual source; it does not expand an inverse polynomial.

This gives distinct, implemented operations:

- **Count:** solve affine conditions in the acquired completion coordinates.
- **Witness:** decode a deterministic affine solution.
- **Rank and unrank:** enumerate accepted original inputs bijectively.
- **Exact uniform sampling:** choose one uniform ticket and decode it, giving every accepted original exactly the same probability.

Arbitrary codimension is supported in those completion coordinates. Arbitrary additional original-input conditions still require their own admission. A failed certificate remains “not acquired,” rather than becoming an empty-count answer.

The integrated argument is preserved in :chatgpt-content-reference{index="2"}[ACQUIRED_NONLINEAR_COORDINATES_CONSTRUCTION.tex](producer-workspace/ACQUIRED_NONLINEAR_COORDINATES_CONSTRUCTION.tex).

## The acquisition barrier removed

The first construction worked from sparse Boolean ANFs. I continued past that result because it retained the expansion barrier you identified.

The new route compiles each ordinary gate into a **binary matrix branching program**, processes shared gates once, and removes states that cannot affect any output. It discovers finite-difference relations directly in these matrices, without enumerating monomials or original assignments. Those relations supply the nonlinear completion construction.

Its polynomial bound depends on the **actual intermediate widths in the chosen variable order**, together with circuit size and input/output dimensions. It does not infer cheap acquisition from a small final representation or assume a favorable hidden order.

This representation is not already a general counting algorithm: polynomial-width programs include sparse cubic Boolean counting, with the retained reduction showing its counting hardness. Successful completion of the acquired geometric certificate is a substantive additional condition.

The matrix minimization and coefficient-rank machinery have established ancestry. The construction uses them explicitly; I am not claiming their invention or settled historical priority for the combined discovery operation. :chatgpt-content-reference{index="0"}

The executable raw interface is :chatgpt-content-reference{index="3"}[certified_roabp_submersion.py](producer-workspace/certified_roabp_submersion.py).

## What the execution established

The raw pipeline acquired width-three programs for a retained circuit whose reduced ANF has **16,777,217 distinct terms**, then counted and reconstructed originals without materializing that ANF. This demonstrates an actual expansion separation.

I also executed the strong ordinary alternative on the **same original conditioned task**, including fresh source acquisition, counting, witness construction, exact sampling paths, verification and output writing. Exclusive-input elimination returned the same count, witness and two-point uniform law, and was cheaper in the recorded run. The comparison therefore establishes **no practical superiority**. Its scope and results are preserved in :chatgpt-content-reference{index="4"}[ROABP_SCOPE_AND_SAME_TASK_COMPARISON.tex](producer-workspace/ROABP_SCOPE_AND_SAME_TASK_COMPARISON.tex).

Independent reviews passed separately for the compressed discovery engine and the raw reconstruction pipeline. Among the decisive controls were exact minimum-width checks, original-input rank/unrank and sampling checks, and a whole-source failure whose requested observation nevertheless acquired successfully. They also preserved a circuit that ends in constant zero but exceeds the width budget earlier—an explicit counterexample to treating final size as acquisition cost. The raw review is :chatgpt-content-reference{index="5"}[RAW_ROABP_STRUCTURE_INDEPENDENT_REVIEW.tex](producer-workspace/RAW_ROABP_STRUCTURE_INDEPENDENT_REVIEW.tex).

## A failure that changes the next scientific question

The work also established an intrinsic obstruction to linear reconstruction information.

For every odd \(n\ge5\), a codimension-one linear projection of the field cube,
\[
Q(x)=P(x^3),\qquad x\in\mathbb F_{2^n},
\]
has exactly two originals per output, yet **no one-bit affine function of the original input distinguishes every pair**. One quadratic bit does.

Thus minimum information length and minimum algebraic complexity of that information are different quantities. In dimension three, a linear bit exists even though the current flag fails; in higher odd dimensions, linearity itself is insufficient. The proof and executable controls are preserved in :chatgpt-content-reference{index="6"}[LINEAR_NOISE_OBSTRUCTION_GOLD_FAMILY.tex](producer-workspace/LINEAR_NOISE_OBSTRUCTION_GOLD_FAMILY.tex).

That gives the broader programme a sharper destination: **discover efficiently decodable nonlinear reconstruction coordinates, with both their information length and their acquisition cost controlled**. The supplied-field decoder is straightforward; recovering its hidden structure from unrelated equations remains unresolved. The completed machinery removes a real expansion barrier and acquires a reusable conditional-inference class, while unrestricted polynomial-time circuit counting and the civilisation-level objective remain unproved.

All proofs, executable work, comparisons and failures were retained in place. No upload, export or repackaging was performed.