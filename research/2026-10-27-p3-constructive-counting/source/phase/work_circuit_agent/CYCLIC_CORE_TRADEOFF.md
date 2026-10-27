# Cyclic-core and local-elimination tradeoffs for replacement forms

This continues the exact obstruction in `CAUSAL_REPLACEMENT_OBSTRUCTIONS.md`. It analyzes a proposed repair of the governing ETH proof's auxiliary matrix construction. It is not a lower bound against all circuit-counting algorithms.

## 1. Opening a small feedback set cannot repair the triangularity problem

Let M be a D×D rational matrix and let B be a set of b indices on which M_ii=0. Put c=rank(I−M). Associate to M the directed graph with an edge i→j whenever i≠j and M_ij≠0.

**Theorem 1 (feedback deletion).** If deleting f coordinate indices makes the remaining graph acyclic, then

\[
\boxed{f\ge b-c.}
\]

**Proof.** Let S be the remaining indices. The principal matrix M_SS can be made triangular by simultaneously permuting its rows and columns. At least b−f indices of B remain; on their principal submatrix, I−M_SS is triangular with unit diagonal. Thus rank(I−M_SS)≥b−f. Since a submatrix cannot have greater rank than its parent, rank(I−M_SS)≤c. Rearranging proves the claim. ∎

More generally, if a measurement matrix C satisfies ker C⊆ker(I−M) and has at most q rows, then c≤rank C≤q. Hence f≥b−q using only the supplied measurement budget.

For the paper's full auxiliary array, B is the set of self-mismatched labels

\[
B=\{u:\#\{t:a_u(t)\ne d_u(t)\}\ge R\}.
\]

The support condition of source Lemma 4.2 forces M_uu=0 on B. As in the previous note, for r≥2 and R≤Q/4,

\[
b\ge D(1-e^{-Q/8}).
\]

Therefore a correction using q=o(D) measurements has minimum feedback deletion at least

\[
\boxed{D(1-e^{-Q/8})-q=(1-o(1))D.}
\]

This is stronger than saying that some cycles occur: almost the whole auxiliary coordinate set must be removed to leave a causal ordering. The result holds regardless of which vertices are selected for deletion.

## 2. Tradeoff when small cyclic blocks are allowed

A repair might allow exact joint elimination inside small strongly connected components (SCCs), rather than demanding a completely acyclic residual network.

**Theorem 2 (SCC-size tradeoff).** If deleting f indices leaves all SCCs of size at most h, where h≥1, then

\[
\boxed{f\ge b-hc.}
\]

**Proof.** Order the SCCs topologically. The residual M is block triangular, with diagonal blocks of size at most h. Let k be the number of blocks containing at least one remaining index of B. Each corresponding diagonal block of I−M has a diagonal entry equal to one, so has rank at least one. A block triangular matrix has rank at least the sum of the ranks of its diagonal blocks: choose a nonsingular minor within each diagonal block and combine their rows and columns into a block triangular nonsingular minor. Thus the residual rank is at least k. Since at most h hard indices occur in a block, k≥(b−f)/h. The residual rank is at most c. ∎

This gives an explicit three-way tradeoff among the measurement rank c, the number f of opened coordinates, and the size h of irreducible cyclic blocks. With b≈D and f=o(D), one needs h≥(1−o(1))D/c. This is a limitation of this repair, not a proof that large blocks cannot be handled by some additional algebraic method.

## 3. Transfer to occurrence copies: a restricted original-variable branching obstruction

The preceding bounds count auxiliary coordinates, which may be zero or repeat original variables. One must not automatically call them independent input bits. The following statement explicitly accounts for that distinction.

Consider the paper's balanced placement into H copies of the auxiliary array, with M_total occupied factor-variable incidences. Each original variable occurs at least once, each occurs at most b_occ times, and

\[
H D\le2M_{\rm total},\qquad M_{\rm total}\le b_{\rm occ}n.
\]

Let at most δD auxiliary labels have self-mismatch below R, and suppose each copy's correction has rank at most εD. Consider the **restricted repair** that fixes a set S of original variables, removes every occurrence of every fixed variable, and requires each residual occupied auxiliary matrix to have SCC size at most h. All unused auxiliary coordinates are discarded without charge.

**Theorem 3.** Every such repair satisfies

\[
\boxed{|S|\ge n-2M_{\rm total}(\delta+h\epsilon)
\ge n\,[1-2b_{\rm occ}(\delta+h\epsilon)].}
\]

**Proof.** In one copy, at most δD retained coordinates can have good self-labels. By the SCC argument, there can be at most hεD retained hard coordinates: the occupied residual principal submatrix still has rank(I−M) at most εD. Thus at most D(δ+hε) occupied coordinates remain per copy. Summing gives at most H D(δ+hε)≤2M_total(δ+hε) remaining occurrences. Every original variable not fixed has at least one remaining occurrence, so n−|S| is no larger than that count. ∎

For the source's parameters, with λ=ceil(log_2 n),

\[
\epsilon\le\frac{\tau}{r b_{\rm occ}}
=\frac{1}{b_{\rm occ}r^2\lambda},\qquad
\delta\le e^{-Q/8},\qquad
Q=\Theta(\lambda/\log\lambda),\quad
b_{\rm occ}\le\lambda^\beta.
\]

If h=O(log n), so that directly enumerating h Boolean coordinates costs only a polynomial in n, then b_occ δ=o(1) and b_occ h ε=O(1/r²)=o(1). Consequently

\[
|S|\ge(1-o(1))n.
\]

Thus the particular strategy “branch on some original variables, then solve each remaining auxiliary cyclic block by a polynomial-size truth table” does not retain the paper's subexponential advantage. It needs nearly exhaustive original-input branching.

**Scope limit.** This statement requires residual triangular or small-SCC auxiliary matrices before any new algebraic simplification identifying repeated occurrences. It does not exclude cancellations after identification, alternate quotient constructions, large cyclic blocks with efficient symbolic solutions, or a different compiler. Its purpose is to rule out one concrete cycle-opening repair with all input/copy costs accounted for.

## 4. Exact finite verification

The executable `cyclic_core_checks.py` uses the same r=2,Q=3,R=2 fixture as the preceding note. It uses only Python's standard library and exact rational Gaussian elimination.

The matrix is symmetric. Its off-diagonal graph consists of:

- 32 isolated good vertices;
- six copies of K4, each with four hard vertices and rank(I−M_block)=1;
- one 8-vertex component comprising two K4s joined by a perfect matching, all hard, with rank(I−M_block)=4.

The total rank is 10 and the number of hard labels is 32. The general feedback lower bound is therefore 22. Since every symmetric nonzero edge is a directed two-cycle, a feedback deletion is exactly a vertex cover. Exhaustive enumeration within the components proves that the true minimum is 24.

| Maximum residual SCC size | Exact minimum coordinate deletions |
|---:|---:|
| 1 (acyclic) | 24 |
| 2 | 16 |
| 3 | 10 |
| 4 | 4 |
| 8 | 0 |

All 416 component-subset cases were checked. Every residual principal rank and every local SCC-rank bound passed. This is an exact finite check of the theorem and of the cycle-opening costs; it is not a performance benchmark or a claim of historical novelty.
