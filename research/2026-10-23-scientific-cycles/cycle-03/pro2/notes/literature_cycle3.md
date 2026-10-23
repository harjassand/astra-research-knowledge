# Cycle3 primary-literature boundary: fan-block gluing and direct covers

Contributor: `/root/block_stability_literature`, 22 October 2026 Brisbane.
Scope: a bounded source obligation for the owner's five-direction question,
not a second investigation or an acceptance of a new global construction.

## Finding

I found no source establishing a matched four/five-query, dimension-independent
inverse for arbitrary vertex-glued trees of fan blocks under the total row-energy
cap and absolute Frobenius action-noise contract. This limited search does not
establish historical novelty or that the problem is open in the literature.

Two distinctions matter for the next construction: five-color results on
serial overlapping fans do not extend automatically across arbitrary cut
vertices, and binary multicolor direct covers are a known alternative to
one-coordinate-per-color seeds. A new global inverse must be assessed against
that stronger direct-recovery operation class, not only star colorings.

## 1. Newer five-color theorem on 2-paths, with a different gluing rule

G. Benitez-Bobadilla, F. E. Contreras-Mendoza, C. Hernandez-Cruz, C. Linhares Sales,
A. Trujillo-Negrete, *Star Coloring on Some Subclasses of Chordal Graphs*,
arXiv:2606.25168, June 2026.
Primary PDF: https://arxiv.org/pdf/2606.25168

Theorem 4.10 (printed page33) states that every 2-path is star5-colorable.
Section4.4 constructs the coloring by processing overlapping maximal fans.
Theorem4.6 characterizes star4-colorable 2-paths using two forbidden induced
subgraphs. The canonical construction adds a new vertex on an edge incident
with the last added vertex; it is not arbitrary fan attachment at one vertex.

For this owner's noise contract, a valid five-star-coloring would immediately
give five unit-row coordinate queries and the ordinary sqrt(2) Frobenius
direct-read guarantee. This is our elementary consequence of the coloring
theorem. It does not settle the current fan-tree family: its already accepted
41-vertex member requires six star colors. In particular, do not replace
vertex-glued fan trees by the paper's serial edge-overlap class without stating
the changed question.

The definition paragraph on printed page21 says nonconsecutive triangles have
no common vertices, whereas later canonical/fan descriptions allow repeated
apices. I did not resolve that wording inconsistency or independently validate
the complete new paper. It is a relevant comparator to inspect, not a theorem
dependency silently accepted by this note.

## 2. Binary multicolor direct covers are established

S. Hossain and N. H. Mithila, *Pattern graph for sparse Hessian matrix
determination*, Optimization Methods and Software33(4-6) (2018),1250-1263.
DOI https://doi.org/10.1080/10556788.2018.1458849
Primary journal record:
https://www.tandfonline.com/doi/full/10.1080/10556788.2018.1458849

The paper's abstract gives a direct-cover formulation and multicoloring
interpretation. The author's preceding thesis supplies accessible detailed
source: N. H. Mithila, *On the determination of sparse Hessian matrices using
multi-coloring*, University of Lethbridge,2016, Section4.1.2, Theorem4.5,
printed pages31-36.
https://opus.uleth.ca/bitstreams/2e847d06-b3f9-459f-beb4-a13df9596fef/download

A seed may put one column in several groups. Every allowed symmetric
coefficient must have an isolated reading at one endpoint. The thesis's
six-by-six example has all diagonal positions allowed and a four-column binary
seed; it is presented as improving the star-color count for that example.
Thus multiple nonzero query coordinates per row and selected endpoint reads
are prior art, including the free-diagonal setting. No uniform theorem for
the owner's fan-tree family was found in this source.

### Direct-cover conversion to the owner's error model (self-contained deduction)

Let S be a binary n-by-q seed. Suppose every diagonal and permitted edge
coefficient has a selected cell (i,k) of DS that contains that coefficient alone,
at either endpoint for an edge. This is a property to verify on the actual
seed; arbitrary element labels in an intermediate graph model do not suffice.
Let r be the largest number of ones in a row of S, so1<=r<=q. Set X=S/sqrt(r).
Then each row of X has norm<=1. Recover each chosen coefficient by multiplying
the corresponding Y cell bysqrt(r), and copy each edge value symmetrically.
The selected cells are distinct: a single cell cannot contain two distinct
independent coefficients alone. Consequently,

    ||Dhat-D||F^2 <= 2 r ||E||F^2,
    ||Dhat-D||2 <= sqrt(2r) ||E||F.

This charges total row energy and allows arbitrary correlated action noise.
It proves no existence of a five-column cover. A concrete five-column cover
would, however, be a valid construction without needing global substitution.
This deduction and its normalization are elementary; no historical novelty
is claimed. Query acquisition and seed/cover validation still cost work.

## 3. Acyclic substitution does not supply the missing uniform estimate

A. H. Gebremedhin, A. Tarafdar, A. Pothen, A. Walther, *Efficient Computation of
Sparse Hessians Using Coloring and Automatic Differentiation*, INFORMS Journal
on Computing21(2) (2009),209-223.
https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf

The direct star-color versus indirect acyclic-color distinction is explicit.
Theorem3.1, printed page13, bounds an indirectly recovered edge's error by the
number of vertices in a relevant two-color subtree times an error allowance.
For star components that subtree contribution collapses. The numerical
stability discussion does not establish a dimension-independent inverse under
our adversarial whole-action Frobenius norm. A proposed repeated-interface
decoder therefore cannot cite acyclic exact recovery as its global stability
proof.

## 4. Global least squares is an established implementation route

J. M. Fowkes, N. I. M. Gould, J. A. Scott, *Approximating sparse Hessian matrices
using large-scale linear least squares*, Numerical Algorithms96 (2024),1675-1698,
published online2023. DOI10.1007/s11075-023-01681-z.
https://link.springer.com/article/10.1007/s11075-023-01681-z

Section2 formulates fitting multiple secant equations while enforcing symmetry
and a known sparsity pattern. Section3 discusses normal-equation conditioning
and near rank degeneracy. This is a primary predecessor for solving the global
symmetric constrained least-squares system. It does not provide a fixed
five-query design with the owner's dimension-free noise bound. Calling a
numerically successful global least-squares solve a certificate would omit
the required singular-value/inverse estimate.

## Search and cost boundary

Seven web calls were made, with reported outer-call wall latencies2.5,4.5,2.3,
2.2,1.9,2.4,2.7seconds: **18.5seconds** in those observed scopes. The first
call also included a small local read. These are not total research times.
Search phrases concerned sparse symmetric matrix recovery, star coloring on
fan/amalgamation graphs, pattern-graph Hessian determination, and sparse
Hessian least squares. Routine search was supplemented by the stronger engine
when primary coverage was incomplete. Several search hits concerned star EDGE
coloring, ordinary coloring, or unrelated material; none is used as evidence.
The STFC PDF-link click failed with Internal Error; the publisher full text was
then read. No package installation, simulation, benchmark, proof replay,
optimization, paid compute, or external communication was performed.
Reading, mathematical interpretation, authoring, inference, money and energy
are additional/unmetered, not zero.

Parent must personally open a source before citing its web reference in a
root answer. Useful refs: turn95view0/turn96view1 (2-path paper), turn97search0
(journal direct-cover record), turn98view1/turn99view0/turn99view1 (thesis),
turn95view2/turn96view3 (Hessian recovery), turn98view2/turn99view3 (least squares).

The preceding checkpoint's six-query treewidth-two comparator, fixed-palette
obstruction, and local all-aggregate obstruction remain unchanged.

## Addendum: calibration for the owner's new all-design lower-bound claim

Root subsequently reported a covariance-dichotomy construction that would
exclude five uniformly stable queries already for a two-level tree of fans,
and would give a necessary2t+2-query threshold on selected treewidth-t graphs.
This addendum is a narrow comparison search, not an independent proof review
or acceptance of that reported construction. In particular, cone adjacency
needed for its cheap cancellation operation must remain an explicit hypothesis.

### Closest numerical query count:2t+2 is already an exact-action upper bound

C. Musco and I. Ramesh, *Nearly Instance Optimal Sparse Matrix Approximation
from Matrix-Vector Products*, arXiv:2606.12179 / ESA2026.
https://arxiv.org/pdf/2606.12179

Theorem2 gives near-optimal fixed-pattern Frobenius approximation with query
count O(degen(S) log(n+m)/(epsilon delta)). Its exact-recovery specialization
(Lemma8) uses2 degen(S) Gaussian queries with A and A^T. Theorem3 gives a
degen(S) lower bound for exact/relative-approximation recovery. These are exact
action results; approximation error is measured relative to the best
supported matrix. They do not state an arbitrary additive action-noise
guarantee with the owner's row-energy normalization.

For the support of a treewidth-t graph INCLUDING every diagonal, degen(S)<=t+1,
so the exact theorem already supplies the number2t+2. This is our direct
conversion of the graph parameter, not a noisy recovery corollary. An all-design
necessity of2t+2 under the owner's uniform absolute-noise contract would
therefore be a different result, despite the numerical coincidence. The
reported five-query obstruction is not contradicted by noiseless Gaussian
identification or by the paper's logarithmic-query approximation theorem.

### General probing conditioning does not supply a contradictory small-q bound

J. Chiu and L. Demanet, *Matrix probing and its conditioning*, SIAM Journal on
Numerical Analysis50(1) (2012),171-193.
https://math.mit.edu/icg/papers/matrix-probing-theory.pdf

Theorem1.3 and Section1.3 give a high-probability conditioning condition of
the form nq proportional to p(kappa lambda log n)^2, where p is basis size,
kappa measures the basis Gram condition and lambda measures basis numerical
rank. Proposition1.5 treats approximation error. For the natural free-diagonal
and edge basis, rank-one diagonal units give lambda=sqrt(n). Thus the displayed
sufficient condition is not a constant-query guarantee for our graphs. This
is an applicability calculation, not a claim that their sufficient condition
is necessary. Their theorem does not preempt a sharper lower bound in the
owner's graph-specific, row-capped action-noise model.

### Other recent structured-learning work and bounded-search conclusion

Amsel et al., *Query Efficient Structured Matrix Learning*, COLT2026,
PMLR336:158-194, studies near-optimal approximation from general matrix families.
The primary abstract gives a query bound of order square root of the linear
family dimension up to logarithmic factors. This is not a five-query noisy
fan-tree result. The PDF linked from PMLR failed retrieval as an unsupported
application/octet-stream object; only the primary abstract is used here.
https://proceedings.mlr.press/v336/amsel26a.html

The targeted searches combined treewidth, matrix probing, matrix-vector
recovery, additive/adversarial noise, stability and lower bounds. I found no
primary theorem matching a2t+2 uniform noisy lower threshold, nor a published
uniform q<=2t+1 theorem that contradicts the owner's reported construction.
This is insufficient to claim historical originality. The sensible language
remains a new result relative to the checkpoint with historical priority
unestablished. Exact identification, sparse approximation of a different
operator and arbitrary action-noise inversion must remain separate.

Four additional web calls had reported outer latencies2.2,4.3,2.3,5.8seconds,
total14.6seconds. Cumulative scoped source work is11calls and33.1seconds in
these measured access scopes, excluding reasoning, reading, authoring and
inference. No numerical experiment, old replay or parameter sweep was added.
Further root-open refs: turn101view0/turn102view3 (Musco-Ramesh),
turn102view1/turn103view0/turn103view1 (Chiu-Demanet), turn101view1 (PMLR).

## Final addendum: reported triangular sharp bound for all fixed treewidth

Root subsequently strengthened the reported claim to the sharp worst-case
uniform stable budget K_t=binom(t+2,2), with exact identification budget t+1.
The reported new lower induction uses coning, repeated copies, low/high
covariance alternatives and a coefficient-dimension excess on a core. This
literature addendum does not certify that proof. It checks the changed
comparison and attribution boundary only.

### Exact classical upper theorem and its applicability

M. O. Albertson, G. G. Chappell, H. A. Kierstead, A. Kundgen, R. Ramamurthi,
*Coloring with no2-colored P4's*, EJC11(2004),R26, Section6, printed pp9-10.
https://www.combinatorics.org/ojs/index.php/eljc/article/viewFile/v11i1r26/pdf/

Theorem6.1 states: a graph of treewidth t has a star coloring from arbitrary
lists of size binom(t+2,2). The paper attributes the result to Fertin,
Raspaud and Reed and supplies a chordal-completion proof. The proof restates
the parameter as clique number: a chordal graph of clique number w needs at
most binom(w+1,2). Thus there is no missing chordality hypothesis in the
treewidth statement. Theorem6.3 constructs chordal graphs attaining that count
within star colorings, by a clique joined to a path and recursive attachments.

The transfer to the current model is elementary: use coordinate rows for the
colors, recover free diagonals at their own color and each edge from a leaf
endpoint of its bichromatic star. Distinct selected action cells give
||Dhat-D||F<=sqrt(2)||E||F. This applies to arbitrary real action noise and
meets the total row cap exactly. A supplied tree decomposition can be completed
to a chordal supergraph and its coloring restricted to the original support.

**Attribution consequence.** The upper budget, the coloring sharpness, and
the broad clique/path/recursive-attachment graph architecture are classical.
A genuinely new contribution relative to the checkpoint would be proving
that arbitrary dense row-capped designs also fail below that budget in the
uniform action-noise model. Theorem6.3 alone does not make that extension:
its quantifier is over colorings. The new lower mechanism must carry its
own covariance, support, error and norm arguments, without substituting the
classical coloring obstruction for them.

### Further check against broader compression formulations

A. Montoison and coauthors, *Revisiting sparse matrix coloring and bicoloring*,
arXiv:2505.07308v1 (2025), Sections3-4.
https://arxiv.org/html/2505.07308v1

This work discusses removing unnecessary colors and an extended direct
decompression formulation. Its neutral-color improvement uses structurally
zero diagonal entries; it explicitly explains why fully free/nonzero
diagonals prevent that neutralization. It supplies no dense robust probing
lower theorem or contradictory fixed-treewidth uniform guarantee in the
inspected sections. It reinforces the need to retain the diagonal contract
when comparing query counts.

The classical survey Gebremedhin-Manne-Pothen, *What Color Is Your Jacobian?*,
SIAM Review47(4)(2005),629-705, was also inspected for relevant terminology:
https://cscapes.cs.purdue.edu/coloringpage/abstracts/sirev.pdf
Its graph-coloring matrix-partition formulations do not establish the new
all-dense noisy lower claim. Earlier notes in this file cover the stronger
multicolor direct-cover and Gaussian exact-query comparators.

### Calibration and costs

Three additional targeted calls combined the exact treewidth/star-color
primary theorem with searches for treewidth/stable matrix recovery and
robust sparse-Hessian lower bounds. No primary source matching the reported
triangular all-dense uniform threshold was found. No claim of historical
priority follows from this search. The accurate status remains new relative
to the owner's checkpoint, subject to its separate proof checking, with the
classical upper bound and graph-construction ancestry explicitly credited.

Observed outer-call latencies were4.8,3.2,2.9seconds, total10.9seconds. The
cumulative scoped source record is now **14calls,44.0seconds** of access
latency; all reading, reasoning, authoring and inference costs remain
additional. No additional numerical experiment or old replay was performed.
Parent-open refs: turn105view0/turn106view2/turn106view3 (exact classical
upper and coloring lower); turn106view0/turn107view2 (neutral colors);
turn106view1 (survey).
