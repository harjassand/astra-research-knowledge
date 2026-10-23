# Sparse common-operator recovery: closest primary mechanisms

Contributor: `/root/completion_literature`, 21 October 2026.
This is a scoped literature follow-up to the root's concrete sparse-support pivot.
No new numerical experiment, probe, or independent research programme was run.

## Decisive novelty boundary

The generic dense-probe plus support-peeling mechanism is already explicitly in
**Musco and Ramesh, ESA 2026, Lemma 10 and Algorithm 1**. This primary result is
substantially closer than a broad analogy with Hessian coloring. The correct claim
for the present work is an exact, source-bound receiving use on the saved matrix
and saved directions, together with its proof/checker and conditioning boundary.
Neither generic degeneracy-based identifiability nor iterative subtraction should
be described as a new general theorem.

### Direct contemporary comparator

Christopher Musco and Indu Ramesh, “Nearly Instance Optimal Sparse Matrix
Approximation from Matrix-Vector Products.” *34th Annual European Symposium on
Algorithms (ESA 2026)*, LIPIcs 388, 85:1–85:14. Published 25 August 2026.
DOI: <https://doi.org/10.4230/LIPIcs.ESA.2026.85>.
Primary PDF:
<https://drops.dagstuhl.de/storage/00lipics/lipics-vol388-esa2026/LIPIcs.ESA.2026.85/LIPIcs.ESA.2026.85.pdf>.

Definition 1 uses repeated deletion of low-support rows and columns to define
support degeneracy. Lemma 10 recovers an exactly supported rectangular matrix
using two Gaussian blocks, one for each action direction, with twice that
many queries. Algorithm 1 solves rows or columns with sufficiently few remaining
unknowns, subtracts recovered action, and repeats. Its proof needs full rank of a
finite family of row submatrices. Section 4 separately addresses off-pattern
approximation: residuals depend on reused random queries, so the exact-recovery
argument does not establish their approximate guarantee. This is not a certified
floating-point error analysis for the saved Krylov directions.

The theorem's operator access is to both `A x` and `A^T x`. It counts queries,
with polynomial computation outside them. It therefore supplies neither an
end-to-end runtime advantage nor a sharp cost prediction for the actual NIST
problem, whose full coefficients are already available.

## Symmetric specialization and what must be checked locally

The following is our interpretation of the root's stated object, not an additional
attributed theorem. Let `G` be a known undirected support graph, with the diagonal
also allowed. In an elimination ordering, let `N_i^+` be the neighbors still
present when vertex `i` is removed. Suppose a fixed `n by q` query matrix `X`
satisfies full row rank for every

    X[{i} union N_i^+, :].

For two symmetric matrices with this support and the same action on `X`, write
their difference as `D`. At the first vertex, the row equation `(DX)[i,:]=0`
and the rank condition force every still-unknown entry in row `i` to vanish.
Symmetry removes the corresponding column. The same argument then applies
inductively at every subsequent vertex. Hence `D=0`.

A degeneracy ordering with maximum remaining degree `d` requires at most `d+1`
rows in each test, including the diagonal. Generic continuous entries in a query
matrix with `q=d+1` make this finite family full rank. In the symmetric setting,
one may reuse a single block for both row and column information because
`A^T=A`; the rank argument needs no independence between two copies of that
block. This is a direct specialization of the exact peeling mechanism above.
For the actual saved Krylov columns, the correct premise is an **exact check of
those row ranks**. They are not a fresh iid Gaussian block, and a genericity
argument must not substitute for the finite input check.

A `q+1` clique gives an elementary matching obstruction for `q` directions:
choose nonzero `w` supported on that clique with `X^T w=0`. Then `D=ww^T` is a
nonzero symmetric matrix on the permitted support and `DX=0`. If the root verifies
an actual 9-clique and all local 9-column rank conditions, it can establish a
sharp 8-versus-9 identification boundary for that support class. This is an
identification result. To claim eigenvalue-count ambiguity at a specific
threshold requires a separate argument; a nonzero invisible perturbation need
not move an eigenvalue across that threshold.

Full row rank is also only a qualitative uniqueness statement. It does not give
a useful numerical error bound. Solving the local systems can amplify errors
through inverse singular values; subtracting previously reconstructed action can
propagate the errors along the elimination chain. An accepted finite-precision
operation needs a bound on the resulting full recovery map (or a correctly
accounted residual-to-operator certificate). Maximum local condition number alone
is not a complete error-propagation bound.

## Classical sparse-Hessian comparators

Thomas F. Coleman and Jin-Yi Cai, “The Cyclic Coloring Problem and Estimation of
Sparse Hessian Matrices.” *SIAM Journal on Algebraic and Discrete Methods* 7(2)
(1986), 221–235. DOI: <https://doi.org/10.1137/0607026>.
Cornell's original 1984 technical-report record:
<https://ecommons.cornell.edu/entities/publication/9e03cca8-ab7d-406d-a78e-314ecd6b897f>.
Its primary abstract describes graph characterizations of substitution methods
and a roundoff bound. The full report endpoint returned HTTP429 in this search;
I do not claim to have checked its complete proof. The concrete modern primary
implementation below was read instead.

Assefaw H. Gebremedhin, Arijit Tarafdar, Alex Pothen, Andrea Walther,
“Efficient Computation of Sparse Hessians Using Coloring and Automatic
Differentiation.” *INFORMS Journal on Computing* 21(2) (2009), 209–223;
online 15 September 2008. DOI: <https://doi.org/10.1287/ijoc.1080.0286>.
Author-hosted primary manuscript:
<https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf>.

Their seed matrix has one unit entry per row, representing a column coloring.
Star coloring permits direct recovery; acyclic coloring permits recovery through
substitutions on two-colored trees. The indirect routine is linear in the number
of graph edges. Section 3.3 and Theorem 3.1 analyze error accumulated in these
tree substitutions. This mechanism uses additions and subtractions and does not
require inversion of arbitrary dense local query submatrices. Its stability
analysis therefore cannot simply be applied to the generic saved-probe method.

Also inspected: Gebremedhin, Tarafdar, Manne and Pothen, “New Acyclic and Star
Coloring Algorithms with Application to Computing Hessians,” *SIAM Journal on
Scientific Computing* 29(3) (2007), 1042–1072,
DOI <https://doi.org/10.1137/050639879>, primary PDF
<https://www.cs.purdue.edu/homes/apothen/Papers/acyclic-SISC.pdf>.
It develops practical coloring heuristics and distinguishes star, acyclic and
triangular coloring. This supports a conventional comparator, not a claim that
our generic probes already implement an acyclic coloring.

The comparison is therefore between different representations of the same
known-support inverse problem: a discrete coloring seed with structured
substitution, versus dense query rows with local full-rank solves and peeling.
A smaller probe count need not mean a faster or more stable complete computation.
No experiment comparing these alternatives was assigned to this contributor.

## Sources and resources

Six web-tool batches were executed for this follow-up. Observed returned wall
latencies were approximately 2.3, 2.9, 2.6, 3.1, 2.8 and 5.3 seconds, totaling
about **19.0 seconds**. These are source-access latencies only. Reasoning,
interpretation, source writing, inference tokens, monetary cost and energy remain
unmetered. There was one failed Cornell full-report access (HTTP429), no numerical
work and no new Gaussian probes. The earlier completion-theory search is a
separate task with its own receipt in `completion_literature.md`.

Primary web refs, for the root to open before using final citations:
- `turn55view1`: full Musco–Ramesh ESA2026 paper; `turn56view4` is the exact
  Algorithm1/Lemma10 passage, `turn57view1` its approximation caveat.
- `turn54view1`: author-hosted sparse-Hessian manuscript; `turn56view7` and
  `turn57view2` are the stability section.
- `turn55view0`: 2007 coloring algorithm paper.
- `turn58search0`: publisher bibliographic metadata for the 2009 paper.
- `turn53search0`: original Coleman–Cai primary abstract only.
