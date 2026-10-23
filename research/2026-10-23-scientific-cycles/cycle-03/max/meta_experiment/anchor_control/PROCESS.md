# Public process record

Only the supplied base instructions, control method, and anchor seed were read. No web, unrelated files, sibling outputs, collaborators, or subagents were used. The output directory contains only the three requested deliverables.

1. Reexpressed the problem on the hyperplane $k^\perp$ using $x=N^Tz$. This removed the irrelevant choice of coordinates in $\mathbb R^r$.
2. Identified the rank-one construction when one squared kernel entry is at least the sum of the others. This directly handles the singular boundary instead of assuming positive definiteness.
3. Reduced the arbitrary sign-pattern inequality to finitely many singleton-positive conditions by a nonnegative-square estimate and weighted Cauchy–Schwarz. Summing those conditions under the probability normalization forced an exact quadratic identity for every nonvertex solution.
4. Constructed solutions of that identity by scalar square-root branches and the intermediate value theorem. The all-smaller-root prescription alone fails for $a=(4,3,2)$; flipping the maximal coordinate to the larger root resolves that case and, by the endpoint argument, every remaining nondominant case.
5. Checked the construction numerically on 650 positive coefficient lists and 32,500 hyperplane vectors. The three branches occurred 289, 194, and 167 times, respectively (vertex, all smaller roots, one larger root). No positive normalized violation was observed.
6. Performed adversarial exact checks of the unequal-coefficient branch and every ternary sign pattern in two three-coordinate examples. Also checked dominance equality. A first uniform-weight probe used a nonbinding sign pattern and did not produce a violation; the corrected probe with weighted coordinates $(-4,-3,7)$ gives the exact failure $21/2>7$. The final proof does not rely on these calculations.
7. Wrote a self-contained proof, including the necessity and sufficiency characterization, dimension-one case, zero weights, and possibly singular $S$.

## Limit and result

The 12-minute cap began at the first clock reading, 2026-10-21 17:14:43 UTC. Work was completed before the cap. Exact elapsed and code accounting appear in COSTS.json. Token costs are unavailable and are explicitly recorded as unknown.

Result: full affirmative resolution, with a construction for every stated input. There is no remaining gap and no claim of novelty.
