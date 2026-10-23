# Quantum predicate-mass L-mask tensor-cap qualification — 24 October 2026

## Correction and scope

The exact single-copy comparison remains correct: the quantum $L$-mask witness has balanced cap $4/3$, below the exact classical single-copy cap $3/2$. That separation does **not** yield an asymptotic advantage for the supplied tensor-product quantum witness. Exact classical collective covers of $L^{\otimes t}$ beat its cap $(4/3)^t$ for every tensor length $t\ge2$. The finite predicate-mass theorem and its stated $\kappa$ bound are unchanged; this corrects only an extrapolation from the one-copy comparison.

## Exact classical tensor certificates

Let $C_t$ be the minimum balanced local cap of an exact positive rectangle decomposition of $L^{\otimes t}$, where rectangles may couple all $t$ coordinates jointly. The supplied rational primal/dual certificates give

\[
C_1=\frac32,\qquad C_2=\frac74<\frac{16}{9}=\left(\frac43\right)^2,\qquad C_3=\frac{23}{10}<\frac{64}{27}=\left(\frac43\right)^3.
\]

The certificates expand and check all 37 allowed rectangles at $t=2$ and all 653 at $t=3$, with exact coverage, row/column loads, dual budgets and matching primal/dual values. The supplied source checker uses rational arithmetic rather than a floating-point or NPA optimum. The supplied product covers imply

\[
C_{2k}\le\left(\frac74\right)^k,\qquad
C_{3+2k}\le\frac{23}{10}\left(\frac74\right)^k,
\]

whose ratios to $(4/3)^t$ are $(63/64)^k$ and $(621/640)(63/64)^k$, respectively. Both are strictly below one for all indicated $t\ge2$. Thus the provided quantum product lift has no repetition-rate advantage over these classical collective covers. This does not determine the optimal quantum collective cap; another quantum construction could still improve the comparison.

## Verification record

The producer correction states that an exact `Fraction` checker independently reran the supplied certificate. The user also supplied a separate source-exposed checker; its source is preserved in this packet, and the user reports that it checked all 37 and 653 allowed rectangles and passed the primal/dual comparisons. This integration read both checker sources but ran neither. It is certificate verification, not blind discovery or a full repetition-proof audit.

The [source manifest](source_manifest.json) pins the original receipt and exact selected bytes. This qualification does not establish an optimal quantum cap, an asymptotic theorem for all quantum strategies, or invalidate the finite predicate-mass theorem.
