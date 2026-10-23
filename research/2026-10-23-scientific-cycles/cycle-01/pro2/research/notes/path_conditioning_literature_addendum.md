# Bounded primary-literature check: optimal two-query path conditioning

Contributor: `/root/completion_literature`, 21 October 2026.
Scope: one bounded literature check for the root's concrete conditioning theorem.
No proof ownership transfer, numerical sweep, new benchmark or new subagent.

## Exact claim being checked

For n>=2, let T_n be the vector space of real symmetric tridiagonal matrices.
For X in R^(n by 2) with every row of Euclidean norm one, set

    C(X) = sup_{0 != D in T_n} ||D||_F / ||DX||_F,

with C(X)=infinity when the measurement map is not injective. The root's proposed
result is

    inf_X C(X) = 1/(sqrt(2) sin(pi/(2n))).

The load-bearing distinction is optimization over **all dense two-query designs
with the stated row normalization**, rather than analysis of one fixed coloring.
The root reports a universal sine-flow obstruction and attainment by alternating
coordinate rows. This literature note does not independently verify that proof.
For n=1 the inverse constant is one, so that degenerate case must be excluded
from the displayed formula. Without a normalization, scaling X changes C(X) and
the minimization would not express the intended stability question.

## Closest exact-recovery source

Diana Halikias and Alex Townsend, “Structured matrix recovery from matrix-vector
products.” *Numerical Linear Algebra with Applications* 31(1), e2531 (2024),
DOI <https://doi.org/10.1002/nla.2531>; published online 22 September 2023.
Primary preprint inspected: arXiv:2212.09841v2, 29 May 2023,
<https://arxiv.org/pdf/2212.09841>.

Section 2.1.3, equation (2.2), explicitly recovers symmetric tridiagonal matrices
from the two alternating coordinate-indicator vectors. It also describes the
three periodic coordinate-indicator vectors for direct recovery. Thus two-query
identifiability and both attaining/positive seed designs already have close
primary predecessors. The inspected section establishes query counts and a
recursive reconstruction, not the stated optimal inverse Frobenius constant over
arbitrary dense row-normalized two-query designs. The paper's explicit
conditioning discussion concerns a later HSS recovery system.

## Closest stability and coloring comparison

The primary sparse-Hessian source already inspected for the preceding obligation
is Gebremedhin, Tarafdar, Pothen and Walther, “Efficient Computation of Sparse
Hessians Using Coloring and Automatic Differentiation,” *INFORMS Journal on
Computing* 21(2) (2009), 209–223,
DOI <https://doi.org/10.1287/ijoc.1080.0286>.
Author-hosted manuscript:
<https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf>.

Section 3.3 and Theorem 3.1 bound the errors in a fixed acyclic-coloring
substitution routine in terms of two-colored tree sizes. Direct recovery under
star coloring is the special case without that chain of substitutions. This is
a meaningful stability comparator; it does not state a lower bound against every
dense two-query design under the root's normalization.

For a rooted forest, depth modulo three is a star coloring: within any two color
classes each connected component consists of a parent and its children. Therefore
the root's three-query forest construction is within classical direct sparse
Hessian recovery. Its explicit Frobenius inequality can be proved for the chosen
normalization, but the coloring construction itself should not be claimed new.
For a path, periodic three-color rows separate all entries in each row, explaining
the isometry directly. The general two-query minimax obstruction is a different
claim from these positive coloring constructions.

## Verdict and scope

**Historical novelty of the exact optimal conditioning formula is unestablished.**
The bounded search did not locate that formula or its arbitrary-dense-two-query
lower bound. This is not an exhaustive priority search and is not evidence of
originality by itself. The defensible checkpoint description is a self-contained
proved optimal conditioning result, with independent proof challenge, placed
beside the known two-query recovery and three-color constructions. A proof of
this normalized linear inverse problem does not establish a spectral-CDF speedup
on the NIST matrix or any other application.

If used as a continuation seed, retain: real symmetric tridiagonal domain;
Frobenius norm counts each off-diagonal entry twice; unit Euclidean norm of every
query row; n>=2; extended infinite constant for a noninjective design; full lower
bound for arbitrary dense designs; and separate attainment proof. These are the
specific obligations distinguishing the claim from existing query-count results.

## Observed source-access costs

Four web-tool batches, with returned wall latencies approximately 2.3, 6.3, 2.8
and 5.1 seconds: **16.5 seconds total observed tool latency**. The batches used
one routine search and two stronger-coverage searches, plus primary opens and
finds. The unversioned arXiv HTML route failed with DisabledError; the primary
PDF succeeded. No numerical run or external full-paper download was performed.
Reading, analysis, writing, model inference, energy and monetary cost remain
unmetered. The earlier sparse-recovery literature task is separately charged.

Root citation references: `turn65view1` is the primary Halikias–Townsend PDF;
`turn67view0` identifies Section2.1.3; `turn67view1` contains its HSS-conditioning
passage. `turn65view2` is the publisher record. The prior Hessian stability
source is `turn54view1` / `turn56view7`. Root must open a source before citing it
in the final response.
