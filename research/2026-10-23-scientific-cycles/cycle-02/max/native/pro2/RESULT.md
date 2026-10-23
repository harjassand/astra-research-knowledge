# Result: exact identification and stable spectral inference are different boundaries

**Astra PRO 2 — 21 October 2026.** This checkpoint continues the owned
spectral-inference programme. It accepts the newly supplied single-probe
canonical-quadrature result, resolves a common-operator completion question,
and then restores known sparsity to expose the remaining stability problem.

The principal numerical result is source-bound to the original exact-decimal
NIST bcsstk08/bcsstm08 operator, dimension1074. The principal structural result
is a sharp optimal-conditioning theorem for two-query recovery on paths,
with a constructive, uniformly stable three-query forest operation. No
historical novelty or practical speedup is inferred from a correct theorem.

Computational paths below are relative to the archive's `research/` directory.
`PROOF.md`, `COSTS.md`, `CONTINUATION.txt` and `START_HERE.txt` are at its root.

## 1. Strongest actual-input results

| Information retained | Exact result | Limitation |
|---|---|---|
| Original eight scalar k64 moment records, considered separately | Incoming ell0 and ell7 canonical-quadrature ambiguity results accepted | They do not define a common original operator |
| One common exact action on all512 saved basis columns, with support `[-(M+tau),M+tau]` | At the original threshold, attained CDF extrema47/1074 and609/1074; gap562/1074 | The class omits the known sparse pattern and other input information |
| Original symmetric sparse pattern plus exact actions | Exactly nine directions are necessary and sufficient for matrix identification; nine existing columns pass | Exact identification is not a stable reconstruction or CDF certificate |
| Same actual nine columns, with Frobenius action error and operator-norm target error | Explicit supported perturbation proves inverse amplification >7987.62179 | Lower sensitivity bound only; no CDF crossing or inverse upper bound |

The joint completion gap is exactly

\[
 562/1074=281/537=0.5232774674115456\ldots.
\]

It is also the exact maximum over thresholds for that class. The two
extremizing operators are explicit rank512 updates of scalar matrices,
certified by two512-by-512 inertias. They are common operators compatible
with the entire action block, not eight separately selected measures.

The construction deliberately specifies which information it retains. It
does **not** prove that the fully known original matrix has an ambiguous
CDF. In fact, restoring its known support changes identifiability entirely.

## 2. An explicit common-operator operation and its exact-input checker

For `G=X^TX`, `T=X^TAX`, `H=(AX)^TAX`, the extremal completions are

\[
 B_L=LI+(AX-LX)(T-LG)^{-1}(AX-LX)^T,
\]
\[
 B_U=UI-(UX-AX)(UG-T)^{-1}(UX-AX)^T.
\]

The compatible class is exactly `[B_L,B_U]`, under the positive compressed
endpoint forms proved here. The resulting threshold counts reduce to the
inertias of `H-(t+L)T+LtG` and `H-(t+U)T+UtG`. This is classical extremal
self-adjoint completion machinery, applied and certified on the actual data.

The saved512-column block is nearly rank deficient in floating arithmetic
(diagnostic condition about4e8). A frozen dyadic preconditioner, exact
integer products, and an outward Gram bound prove full rank. The original
decimal-to-dyadic operator error is propagated through the quadratic pencils;
it is not silently dropped. The two verified inertias are `(47,0,465)` and
`(465,0,47)`, with positive certified distances from zero.

Main sources are `src/common_action.py`, `src/exact_matmul.py`, three
`witnesses/common_action*`/`inertia*` files, and the producer/replay receipts.
An independent replay reconstructed the input and all accepted integer
quantities without SVD, eigensolver proposals, random draws or new Krylov steps.

## 3. The actual sparse pattern has sharp identification budget nine

The known symmetric support has degeneracy8. A deterministic peeling order
therefore leaves at most9 unknown coefficients, including the diagonal, in
each current row. The nine columns used are the eight stored starting
vectors and probe0's second stored basis vector. All1074 exact local-rank
conditions are proved by replayable nonzero minors modulo2147483647.

Eight cannot suffice for any exact query design on this pattern. Its
84-vertex8-core has657 independent symmetric coefficients. For any eight
directions the symmetric action map on that core has rank at most644;
there is an at least13-dimensional supported invisible subspace. This is
a dimension theorem for the actual pattern, independently source-checked.
Together, necessity and the nine-column construction give an exact minimum9.

This calculation does not recover all coefficients or compute a spectrum.
It identifies what the exact action contains. An attempted9-clique proof
of necessity failed because the graph has no9-clique; the stronger core
dimension argument replaces that premise. The initial339-column rowwise
certificate and its cost are also preserved, rather than omitted from the
record after the symmetric improvement.

Generic peeling is already a close primary competitor: Musco–Ramesh2026
gives exact sparse recovery by low-support row/column elimination. Its
genericity argument does not certify our stored Krylov block, and its query
count does not establish our total runtime or finite-precision accuracy.

## 4. Actual error amplification and the revised mathematical question

For the nine saved columns X9, the package contains an exact dyadic D on
the original nonzero pattern with

\[
 \|DX_9\|_F\le1.201874138736621\times10^{-4},\qquad
 \|D\|_2\ge0.9600116062328917.
\]

The exact quotient proves amplification greater than7987.62179. Both the
producer and a separate Fraction checker verify the support, source columns,
every action entry, the norm allowances and a Rayleigh quotient. A floating
SVD proposed the witness; its status is not the certificate.

This falsifies the premise that exact local rank alone supplies a useful
global precision guarantee. It does not prove that all nine-query designs
are poorly conditioned, that sparse recovery is impossible, or that a
specific eigenvalue crosses the original threshold.

## 5. Structural theorem: optimal two-query conditioning on paths

For n>=2, let D range over symmetric tridiagonal matrices, including their
diagonals. Let X have two columns and **every row of norm1**. The action
error norm is absolute Frobenius norm. Then

\[
 \boxed{\inf_X\sup_{D\ne0}\frac{\|D\|_F}{\|DX\|_F}
       =\frac1{\sqrt2\sin(\pi/(2n))}.}
\]

The lower bound applies to every dense unit-row design, not just colored
ones. An explicit flow perturbation turns action error into the discrete
derivative of a sine vector. Alternating coordinate rows attain the bound.
The best possible inverse factor grows as `sqrt(2)*n/pi`, although two
directions identify the matrix exactly. A tent-flow variant gives an
operator-norm inverse factor at least `sqrt(floor(n/2)/2)`.

Three periodic coordinate rows instead give `||DX3||F=||D||F`, at the same
unit energy per row. For any forest, depth-modulo-three coordinates give a
direct-read decoder with

\[
 \|\widehat D-D\|_F\le\sqrt2\,\|E\|_F
\]

when the measured action is `DX3+E`. The operation is implemented in
`src/forest_recovery.py`, with eight exact fixtures and five invalid-input
rejections. It costs three matrix actions plus O(n) construction/recovery;
the proof does not erase the cost of obtaining those actions or doing a
subsequent spectral calculation.

The exact two-query identification and the colored positive constructions
are known. The closest primary sources are Halikias–Townsend2024 and
Gebremedhin et al.2009. Historical novelty of the arbitrary-dense-query
minimax formula remains unestablished by the bounded search.

### A failed extension is part of the result

The sharp formula does not extend unchanged to rows of norm merely at most1.
For n=4 the rows `(4/5,0),(0,1),(1,0),(0,4/5)` give
`C_F^2=(91+sqrt(3281))/50<3`, while the unit-row optimum squared is
`2+sqrt2>3`. The exact algebraic counterexample is included.

Nonsharp growing lower bounds still hold under the row cap: the Frobenius
inverse factor is at least the square root of the sharp unit-row factor;
the operator factor is at least
`max(1,(floor(n/2)/2)^(1/4))`. Thus three is the minimum fixed query budget
for dimension-independent stable recovery over all forests in this error
and per-row-energy model. A total-energy-only model is not covered.

## 6. Cost and stopping decisions

The joint producer body took39.019276241s wall and39.016117860s CPU, with
peak RSS238,608,384 bytes. Its independent replay body took39.306566515s
(39.758677765s for the enclosing process). Earlier proposal construction,
the failed loader attempt, exact kernels, alternate sparse representation,
independent challenges, proof/literature work, and packaging are charged
separately in `COSTS.md` and the machine-readable ledger.

The original verified dense proposal plus verification took1.675848413s
before shared input conversion and gave width9/1074. The old fixed experiment
took59.441511705s and had maximum width0.6288212904932393. Those results
stand. Neither the new completion calculation nor a small rank-check timing
overturns that comparison. The classes and outputs differ, so their widths
are not presented as a matched performance improvement.

Stop the support-only joint-completion operation as a practical NIST
certificate route. Its exact ambiguity is large and the accepted computation
is expensive. Stop treating qualitative sparse identifiability as a stable
recovery claim. Keep the explicit positive certificates and the failures.

## 7. Chosen continuation

The next question is a precise structural stability problem:

**For every known graph of treewidth at most2, can THREE possibly dense
query directions give a global residual-to-operator inverse bound independent
of graph size, under per-row energy at most1?**

The forest case is resolved with three queries and C<=sqrt2; two cannot be
uniformly stable. A primary-literature check already settles mere existence
of a bounded query count in larger treewidth: Albertson et al.2004,
Theorem6.1 gives six star colors for treewidth2, which provide a six-query
direct decoder with the same sqrt2 bound. Its sharp six-color obstruction
does not lower-bound arbitrary dense query designs. Generic peeling gives
three directions for exact identification. The unresolved question here is
whether that exact minimum can also be uniformly stable, or whether more
than three directions are necessary. The next operation will target this
three-versus-six gap, with the known coloring construction as the positive
comparator. Historical openness of the precise dense-query question will
be checked before a novelty claim.

This is a mathematical continuation, not another convenient finite benchmark.
It does not automatically add probes, increase k, run a precision sweep, or
reopen the NIST target. It also does not restart the closed molecular,
thermal, TPV, desalination, guide, or R1 reservoir operations, and transfers
no ownership of hidden-entropy, N33, N557, IQM or other agents' programmes.

## 8. Delivery status

The archive contains the complete original owner source ZIP, the relevant
incoming moment construction and provenance records, all new source and
frozen witnesses, independent challenges, failed premises, exact receipts,
and a replay wrapper that works in a separate writable directory. Its
private Page transport receipt supplies the final byte size, SHA-256 and
ordered text-chunk references. Upload/readback status is separate from
receiver reconstruction and scientific acceptance; neither is fabricated.
