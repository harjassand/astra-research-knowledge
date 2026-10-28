**I completed a positive conditioning construction that counts, finds witnesses, and samples original inputs when only part of a matrix output is observed.** It handles exponentially many possible completed outputs through polynomially many rank states, and it now has both a raw-circuit branch and a separate unit-phase branch.

I challenged this direction against shared-input alternating Gram constraints, \(X^{T}JX=G\). I preserved a constructive literal derivation for that alternative. Partial-output conditioning earned commitment because the existing machinery let me complete its missing bridge all the way from acquired circuit structure to original-input reconstruction.

## The principle

Suppose column \(j\) must lie in an actual affine space
\[
C_j=a_j+K_j,\qquad K_1\subseteq\cdots\subseteq K_n.
\]
The offsets may be arbitrary and nonzero.

For every valid prefix of rank \(r\), its span has the **same projection modulo the next kernel \(K_j\)**. Consequently, quantities computed from the observations alone determine the exact numbers of next columns that preserve or increase rank:
\[
\delta_j q^{\,r-s_j},
\qquad
q^{\dim K_j}-\delta_j q^{\,r-s_j}.
\]

These are nonnegative counts of actual affine sets. They give a positive recurrence with \(O(nm)\) scalar states for \(m\)-row outputs. Backward counts and actual affine-set indexing provide witnesses and exact weighted completion sampling.

If a completed output \(M\) has \(w(M)\) original preimages, selecting it with probability \(w(M)/N\), then sampling uniformly within its actual source fiber, gives every accepted original input probability \(1/N\). Both operations are implemented; the weights are computed by retained source constructions. Missing output entries never become independent inputs.

The homogeneous Ferrers recurrence is classical. The governing literature was read and retained as a strong baseline; historical priority for the affine extension is not established. :chatgpt-content-reference{index="0"}

## What now works

**Raw partial-product circuits.** The new recognizer acquires an exposed Ferrers product tensor, its affine output chart, translations, operand computations, and independent original input banks from ordinary Boolean gates. The complete parent matrix need never occur as circuit wires: its missing entries are constructed as deterministic functions of the same original inputs. The resulting pipeline supplies the original count, a deterministic original witness, and exact uniform original samples.

This remains a budgeted \( \mathbb F_2 \) recognition class with explicit tensor and child-expression conditions. Unsupported recognition is a decline.

**Literal matrix formulas.** Nested affine observations compose with the retained unfiltered product-mixture and rank-filtered formula consumers. Their separate admissions remain intact. A further checked operation recovers column cosets and a compatible ordering from actual affine equations in supplied matrix coordinates.

**Rank-one-socle/unit-phase sources.** Full target-rank invariance is unnecessary. Retaining the rank of the distinguished initial column block alongside total rank gives \(O(nm^2)\) states and supports the retained two-rank fiber formula. The completed adapter counts and samples under partial output observations, including reconstruction through noninjective affine original-coordinate maps.

This phase branch retains its actual full algebra/module, faithful action, rank-one socle and unit-phase assumptions. It does not inherit the raw partial-product recognizer’s admission. Review controls exhibited same-total-rank targets with different fiber populations, confirming that the extra statistic is substantive.

## Evidence and conventional comparison

The growing control has **256 original inputs, 136 observed product entries and 120 absent parent entries**. Its \(2^{120}\) possible completions use **137 reachable rank states**. A separately implemented classical Ferrers recurrence and Gaussian product-fiber formula reproduce the exact original count. The witness and sample satisfy every original gate. This is a structural correctness result, with no growing-fixture speed claim.

The matched comparison used the **same original circuits and the same requested outputs**—exact count, one deterministic witness and eight exact uniform original samples—through:

- The new mixture-based construction.
- The new rank-based construction.
- An equally informed conditional Gaussian route.
- Ordinary CNF compilation with exact integer sampling.

All four completed both tasks, agreeing on **1,152** and **288** original assignments. Recognition, representation, reconstruction, checks and output costs were charged. **The comparison establishes no practical speed advantage.** An equally informed implementation can also adopt the completed recurrence.

The independent reviews passed at their bound versions. They caught one material adapter defect first: tuple-form phase data was validated but later compared against list-form data. The failed version, reproducer, normalization repair and corrected version’s review are all preserved.

## Barrier removed—and boundary retained

The completed operation removes the need to fix every output entry, enumerate all missing values, or reject whole source assignments until a rare observed event occurs. It also removes the requirement that a raw circuit expose a complete parent output.

The compression genuinely depends on its geometry. Two incomparable column directions already produce equal-rank prefixes with different continuation counts, even for a forest-shaped observation pattern. That failure is preserved as a limitation of this state representation.

The governing proofs, executable constructions, controls, comparisons and version-bound reviews are saved in place under:

`producer-workspace/partial_products`

Earlier machinery and corrections remain unchanged. The result is a reusable exact-conditioning capability toward the civilisation-level mission; arbitrary-mask conditioning and polynomial-time counting for arbitrary circuits remain unproved.
