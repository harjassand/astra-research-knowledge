# Primary-literature boundary: dense compression and stable sparse recovery

Investigator: `/root/stable_design_literature`, scoped contributor to Astra PRO 2.
Read and searched 21 October 2026 UTC / 22 October 2026 Australia/Brisbane.
This is a bounded primary-source check, not a systematic priority review.

## Main finding

Dense compression of a coloring seed is an established idea. A claim that
replaces coordinate colors by vectors in fewer dimensions must therefore
identify its new **global inverse estimate**, graph hypothesis, and noise/energy
normalization, rather than claim seed compression itself as new.

I found no matched published four- or five-query theorem for **every**
treewidth-two symmetric support with diagonal, a per-row Euclidean energy cap,
and a dimension-independent inverse from absolute Frobenius action error.
This search failure does not establish historical novelty or openness.

## Closest compression predecessors

### [C1] Griewank and Strogies, 2014, Part I

Andreas Griewank and Nikolai Strogies, *Efficient Evaluation of Sparse Jacobians
by Matrix Compression, Part I: Motivation and Theory*, Advances in Applied and
Pure Mathematics, 2014, pp. 33–40.

Primary PDF: <https://wseas.us/e-library/conferences/2014/Gdansk/MATH/MATH-01.pdf>

Section 2 explicitly factors the seed as `S = G C`, where `G` is a coordinate
grouping seed and `C` compresses the groups. Distinct colors receive interpolation
abscissae; Lagrange generalized-Vandermonde rows give local invertibility with
`rho = max_i row_nnz(i)` columns. Section 3 treats evaluation/reconstruction
accuracy and normalization. The paper discusses a worst-case bound depending
only on `rho` and the number of colors, while emphasizing practical conditioning.

**Boundary for our question:** their row systems are individually invertible;
they do not allow a row with more independent unknown aggregates than query
coordinates and then use global symmetry/graph structure to restore a uniform
inverse. Such a global argument is the obligation in a six-color to five-query
construction on unbounded-degree graphs.

### [C2] Strogies and Griewank, 2014, Part II

Nikolai Strogies and Andreas Griewank, *Efficient Evaluation of Sparse Jacobians
by Matrix Compression Part II: Implementation and Experiments*, WSEAS
Transactions on Mathematics 13 (2014), pp. 646–653.

Primary PDF: <https://wseas.com/journals/mathematics/2014/a545706-088.pdf>

Equations (1)–(5) give the seed and explicit local inverse. Section 3 explains
that both large seed entries and large inverse entries matter for accuracy;
it discusses scaled inverse norms and choices of interpolation nodes. A worked
example compresses six groups to four coordinates because each row has at most
four unknowns. The choices of node ordering and Cartesian colors use heuristics.

**Boundary:** this is a concrete earlier color-to-dense-vector compression
operation with a numerical sensitivity discussion, not just an abstract
generic-rank observation. No total row-energy cap or our uniform operator/Frobenius
action bound should be attributed to it without deriving the conversion.

### [C3] Hossain and Steihaug, 2001 preprint / 2002 chapter

Shahadat Hossain and Trond Steihaug, *Reducing the Number of AD Passes for
Computing a Sparse Jacobian Matrix*, in *Automatic Differentiation of
Algorithms: From Simulation to Optimization*, 2002. Preprint posted January 2001.

Primary PDF: <https://optimization-online.org/wp-content/uploads/2001/01/255.pdf>

Starting from a consistent column/row partition, this paper combines groups and
uses substitution to reduce the number of derivative passes. Section 2 shows
how a grouping with more than `rho` groups can lose at least one pass, with
`rho` the relevant maximum row support. Its concluding discussion compares
Vandermonde and Chebyshev versions of the earlier Newsam–Ramsdell construction,
including conditioning concerns.

**Boundary:** a reduction below the color count is old. A symmetric sparse
support with unbounded maximum degree is outside the fixed-row-support benefit
that would automatically follow here.

## Strongest established comparisons relevant to the owned problem

### [G1] Albertson et al., 2004: six star colors

Michael O. Albertson, Glenn G. Chappell, H. A. Kierstead, André Kündgen and
Radhika Ramamurthi, *Coloring with no 2-colored P4's*, Electronic Journal of
Combinatorics 11 (2004), R26.

Primary PDF: <https://www.combinatorics.org/ojs/index.php/eljc/article/viewFile/v11i1r26/pdf/>

Theorem 6.1 proves a star-list-coloring bound `binom(t+2,2)` for treewidth `t`,
attributed there to Fertin–Raspaud–Reed. Theorem 6.3 proves sharpness in that
coloring class; the clique-number-three example is outerplanar. Thus six is
the established treewidth-two star-coloring bound, while a six-color lower
bound says nothing by itself about arbitrary real vector seeds.

**Our direct consequence, not a separately quoted theorem:** leaf-side reads
of bichromatic stars use distinct action cells. Copying an off-diagonal error
to its symmetric position costs at most `sqrt(2)` in Frobenius norm. Coordinate
seeds satisfy the per-row energy cap exactly.

### [G2] Gebremedhin et al., 2009: recovery and error propagation

Assefaw H. Gebremedhin, Arijit Tarafdar, Alex Pothen and Andrea Walther,
*Efficient Computation of Sparse Hessians Using Coloring and Automatic
Differentiation*, INFORMS Journal on Computing 21(2) (2009), 209–223.
DOI: <https://doi.org/10.1287/ijoc.1080.0286>.

Primary author PDF: <https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf>

This source explicitly distinguishes direct star-color recovery from indirect
acyclic-color recovery and gives linear-time implementations. Section 3.3,
Theorem 3.1 bounds a recovered edge's error by a subtree-size factor times an
error allowance. For stars that propagation length collapses. Its favorable
empirical stability conclusions do not convert that size-dependent bound to
our dimension-independent adversarial action-noise bound.

### [M1] Halikias and Townsend, 2024: exact query complexity

Diana Halikias and Alex Townsend, *Structured matrix recovery from matrix-vector
products*, Numerical Linear Algebra with Applications 31(1) (2024), e2531.
DOI: <https://doi.org/10.1002/nla.2531>.

Primary manuscript: <https://arxiv.org/pdf/2212.09841>, version 2, 29 May 2023.

Section 2.1.3 gives two-query exact recovery for symmetric tridiagonal matrices,
including the alternating coordinate construction, and discusses three periodic
coordinate queries for tridiagonal recovery. Query complexity primarily means
exact identifiability here. The paper treats approximation and stability for
other structured families, especially hierarchical low rank; those do not
supply the missing stable treewidth-two theorem.

### [M2] Chiu and Demanet, 2012: conditioning of general matrix probing

Jiawei Chiu and Laurent Demanet, *Matrix Probing and its Conditioning*, SIAM
Journal on Numerical Analysis 50(1) (2012), 171–193.
DOI: <https://doi.org/10.1137/110825972>.

Primary author manuscript: <https://math.mit.edu/icg/papers/matrix-probing-theory.pdf>.

For a known basis `B_j`, their action design matrix has columns `B_j u`.
Theorem 1.3 controls conditioning from a basis Gram condition `kappa` and
`lambda=max_j sqrt(n)||B_j||_2/||B_j||_F`, provided
`n >= p(C kappa lambda log n)^2`. Section 1.3 extends the construction to
multiple random probes; Proposition 1.5 handles approximation error.

**Inference for this model:** the natural diagonal/edge basis contains rank-one
diagonal units, giving `lambda=sqrt(n)`. The displayed sufficient theorem is
therefore not a fixed-query stable construction for arbitrary sparse supports.
It is an important general conditioning comparator, not an impossibility
result. Gaussian seeds also need explicit normalization before satisfying the
row cap. Scaled Rademacher blocks satisfy it, but this alone does not supply
the missing dimension-independent lower singular-value estimate.

## What the bounded search permits us to claim

1. A new theorem relative to our checkpoint may compress a classical seed or
   combine classical ingredients. Its contribution must be the resulting
   proven guarantee, not a claim that dense seeds, coloring, least squares, or
   interpolation were previously unknown.
2. Six stable coordinate queries remain the applicable general comparator
   until a stronger all-graph operation is actually proved.
3. A local-rank argument, an exact algebraic recovery count, or samples of
   well-conditioned query blocks do not prove the desired global stability.
4. No historical originality claim is justified by this search. I found no
   matching four/five-query all-treewidth-two stable result, but unindexed or
   differently phrased prior literature remains possible.

## Search and resource record

The searches used both routine and stronger search engines, followed by primary
PDF inspection. Main phrases included dense Hessian seeds, Vandermonde/Pascal
seeding, star-color compression, treewidth and matrix-vector recovery, and
matrix probing conditioning. Secondary search hits were used only to locate
primary papers. No old benchmark, incoming obstruction replay, new numerical
experiment, package installation, or other owner's programme was performed.

Nine completed web tool calls were made, with reported wall times 2.5, 5.3,
2.3, 2.8, 2.4, 6.7, 2.6, 2.8, 2.3 seconds (29.7 seconds in total).
Tool-reported latency is a
partial cost, not total research time or model cost. A current structured-learning
PDF and the ESA2026 author PDF failed retrieval on attempted direct URLs; the
failures did not change any theorem or comparator conclusion here.

Useful web references for the parent to open before final citation:
`turn85view0` (C1), `turn80view0` / `turn82view0` (C2), `turn76view1` / `turn77view1`
(C3), `turn78view2` / `turn79view3` (G1), `turn78view1` / `turn79view2` (G2),
`turn76view2` / `turn77view2` (M1), `turn78view0` / `turn80view1` (M2).

## Addendum: revised separator-and-forest operation

Root reported decisive palette-compression counterexamples and revised the
construction. The new positive operation assumes an explicitly supplied set
`S` of `s` vertices such that `G - S` is a forest. The proposed query count is
`s+3`; separator vertices receive individual coordinate rows and the forest
receives three depth colors in orthogonal coordinates. The proposed sharpness
family is `K_s join P_m`, with an all-dense capped-row obstruction for `s+2`
queries. This addendum is a literature check, not an independent acceptance
of the root's still-developing proof.

### What is already classical in the positive construction

The positive seed is an immediate composition of known star coloring:
give `S` unique colors disjoint from a star coloring of `G-S`. Any bichromatic
component involving a separator color has at most one vertex in that color,
so is a star; the remaining bichromatic components lie in the forest coloring.
This deduction uses the standard definition and direct-recovery mechanism in
[G1,G2]. It is not a claim of a new coloring theorem or new separator-coloring
operation. Consequently, merely observing `s+3` queries for this class does
not outperform its strongest directly applicable classical construction.

The possible new result relative to the checkpoint is the **sharp uniform
necessity against arbitrary real, row-capped directions**, obtained by lifting
path flows through a separator and cancelling all separator action constraints.
Its nearest supplied mathematical predecessor is the incoming fan proof
(`s=1`), and the prior owned two-query path obstruction (`s=0`). The general
extension should be credited as reuse of that mechanism. This bounded search
did not find a published theorem matching that full norm/energy/quantifier
contract; historical originality remains unestablished.

### [S1] Musco–Ramesh, 2026: general sparse recovery/approximation

Christopher Musco and Indu Ramesh, *Nearly Instance Optimal Sparse Matrix
Approximation from Matrix-Vector Products*, arXiv:2606.12179v1 (10 June 2026).
The preceding owner checkpoint also records its ESA2026 publication.

Primary accessible PDF: <https://arxiv.org/pdf/2606.12179>.

Theorem 2 obtains, from exact actions with `A` and `A^T`, a near-optimal
Frobenius approximation of a fixed sparsity pattern using
`O(degen(S) log(n+m)/(epsilon delta))` queries, with success probability
`1-delta`. Its exact sparse-recovery specialization uses `2 degen(S)` Gaussian
queries. The paper explicitly includes arrowhead patterns among the motivating
families and distinguishes support recovery from approximation.

**Comparison:** this is stronger in generality and in allowing arbitrary input
matrices approximated by a known support. Its guarantee measures approximation
error relative to the best supported matrix, using uncorrupted actions. It does
not by itself state our absolute adversarial action-noise bound under a total
per-row energy cap. Exact recovery and near-optimal approximation therefore do
not invalidate a distinct query-stability lower bound.

### [S2] Xia, 2013: separator-based sparse probing

Jianlin Xia, *Matrix-Free Sparse Direct Solvers*, Proceedings of the Project
Review, Geo-Mathematical Imaging Group, Purdue University, Vol. 1 (2013),
pp. 171–183.

Primary author/institution PDF: <https://gmig.science.purdue.edu/pdfs/2013/11Xia2013.pdf>.

This report reconstructs sparse matrices via multi-nested dissection and
compact probing before structured factorization. It uses separator organization
to recover several disjoint blocks simultaneously, and obtains polylogarithmic
probe counts for specified locally connected mesh assumptions. It is a direct
predecessor for the broad idea of sparse probing organized by separators.
The inspected reconstruction results do not provide a matched `s+3` sharp
uniform theorem for arbitrary forest complements and absolute action noise.
Do not equate nested-dissection recovery or linear-system factorization with
our inverse sensitivity contract.

### Scope and additional resource record

The additional search was limited to arrowhead/bordered-tridiagonal recovery,
separator probing, dense-row Hessian recovery, and feedback-vertex-set coloring.
No original matrix calculation or new scientific experiment was performed.
Four further web calls had reported wall latencies 2.4, 4.6, 2.7, and 2.5
seconds, summing to 12.2 seconds. Together with the first stage this is
**13 web calls, 41.9 reported latency seconds**, exclusive of reading,
reasoning, authoring, and parent integration. An accidentally queried arXiv
identifier returned an unrelated multimodal-model paper; it was discarded and
used for no conclusion. The correct Musco–Ramesh source above was then located
through the primary search result.

Additional primary references for parent retrieval before citation:
`turn89view0` / `turn90view0` (S1), `turn88view0` (S2).
