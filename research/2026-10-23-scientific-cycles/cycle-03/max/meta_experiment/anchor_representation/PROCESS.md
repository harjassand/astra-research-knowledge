# Public process record

## Scope and timing

First clock: **2026-10-21 17:14:48 UTC**. Hard deadline: **17:26:48 UTC**. Only the named base instructions, representation-method instructions, and anchor seed were read as sources. No web, sibling output, repository search, historical solution, collaboration, or further agent was used.

The representation search was completed before the **17:16:55 UTC** checkpoint, at most 127 seconds from the first clock and within the 180-second allocation. The record below describes mathematical representations, checks, and results; it is not a transcript of private reasoning.

## Representation 1: hyperplane and sign-cone optimization

**Map.** Send the original variable to \(x=N^Tz\). Its image is exactly \(k^\perp\), so all original universal quantifiers are preserved. Write \(a_i=k_i^2\). In a cone with only coordinate \(j\) positive, weighted Cauchy–Schwarz computes the exact minimum cost of its balanced negative coordinates.

**Outcome.** For probability weights with every entry below one, the resulting conditions are
\[
\theta_j\sum_{i\ne j}\frac{a_i}{1-\theta_i}\le a_j.
\]
Their sum, after rearrangement, forces equality in each condition and hence
\(a_i=T\theta_i(1-\theta_i)\). A separate direct Cauchy–Schwarz argument covers the vertex weights where denominators would vanish.

**Preserved or lost.** The hyperplane map is a bijection; nothing is lost. The interior denominator formula initially excludes vertex weights, but these are fully restored by the exact dominance criterion. The final characterization covers the whole probability simplex.

**Load-bearing check.** The minimizer in each single-positive cone has the stated negative signs. Conversely, the proof of the interior certificate handles all mixed-sign cones directly, using the total negative probability mass. This avoids assuming that checks on one family of cones alone automatically suffice.

## Representation 2: weighted-degree factorization

**Map.** The interior equations are equivalent to a complete graph with positive edge weights \(w_{ij}=T\theta_i\theta_j\) and specified weighted degrees \(a_i\). The total vertex mass is normalized by \(\sum_i\theta_i=1\).

**Outcome.** Positive complete-graph degrees in dimension \(n\ge3\) must be strictly nondominant. Solving the quadratic equations for the vertex masses gives square-root branches. The all-lower-branch sum either crosses one, or flipping the branch at a largest degree gives a continuous sign change at a positive parameter. This proves sufficiency for every strictly nondominant degree vector.

**Preserved or lost.** For nonvertex feasible weights, this is equivalent to the original target by Representation 1 and the certificate lemma. The graph representation does not describe vertex certificates; the dominant-coordinate proof covers exactly that remaining class. Thus the combined reformulation has full coverage.

**Boundary check.** The lower-branch sum need not reach one. The exact example \(a=(19/10,1,1)\) requires a flipped branch and has \(\theta=(19/21,1/21,1/21)\). At \(a=(4/3,1,1)\), the two branches meet at \(\theta=(1/2,1/4,1/4)\). At \(a=(2,1,1)\), the singular vertex certificate applies. A method that used only lower roots would therefore have failed.

## Chosen route and final result

The proof uses the weighted-degree equations to construct the weights, followed by a direct sign-balance inequality to certify every original vector. The full finite-inequality characterization is retained as an independent coverage check. No long parameter search was required.

Outcome: **complete affirmative construction and proof**, with explicit handling of arbitrary dimension, unequal column sizes, zero weights, and singular \(S\). No gap or novelty claim is asserted.

## Adversarial validation

After finding the proof, two calculation runs checked load-bearing features:

* Numerical run: 1,408 coefficient vectors, dimensions 2 through 30, including exact and near dominance boundaries. Branch counts: 359 vertex cases, 775 all-lower-root cases, and 274 flipped-root cases. There were 241,491 inequality checks, combining direct samples on \(k^\perp\) with exhaustive negative-face/positive-ray checks for sampled dimensions at most 9. No failure occurred. Maximum recorded scaled equation residual: approximately \(3.50\times10^{-11}\).
* Exact-rational run: 45 assertions checking the branch-transition example, the flipped-branch example, equal coefficients, the two-coordinate equality case, single-positive equality witnesses, and a four-coordinate mixed-sign inequality. All passed.

These computations are supplementary. The final proof does not infer any universal claim from numerical testing.

## Completion

Final record: **2026-10-21 17:20:36 UTC**, approximately **348.73 seconds** elapsed, including source reading, reasoning, calculations and artifact writing. The 720-second cap was respected. All three requested artifacts were saved. The initial artifact heading-count assertion had a bookkeeping error, corrected by a line-prefix check; no mathematical test failed. Token and monetary costs are unknown.
