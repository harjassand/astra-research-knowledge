# Known bounded-treewidth comparator for stable query design

Contributor: `/root/completion_literature`, 21 October 2026.
One final bounded source check; no numerical experiment or programme launched.

## Secure primary theorem

Michael O. Albertson, Glenn G. Chappell, H. A. Kierstead, André Kündgen and
Radhika Ramamurthi, “Coloring with no 2-colored P4's,” *Electronic Journal of
Combinatorics* 11 (2004), R26, DOI <https://doi.org/10.37236/1779>.
Primary full text:
<https://www.combinatorics.org/ojs/index.php/eljc/article/viewFile/v11i1r26/pdf/>.

Theorem 6.1 states that every graph of treewidth t has a star coloring from lists
of size binomial(t+2,2). Its proof uses a chordal supergraph and a perfect
elimination ordering. Theorem 6.3 establishes sharpness of this star-coloring
bound; Corollary 6.4 gives the sharp six-color bound for outerplanar graphs.
Thus treewidth at most two has an established six-color upper bound, and some
such graphs actually require six star colors. The paper attributes the earlier
upper bound to Fertin, Raspaud and Reed and supplies its own proof.

## Consequence for the root's inverse problem

The following elementary consequence is our explicit connection to query design.
Let the permitted off-diagonal support graph have a star coloring c with q colors,
and set the i-th query row equal to the coordinate vector e_{c(i)} in R^q.
Every row has Euclidean norm one. For a symmetric supported matrix D, put Y=DX.

Proper coloring gives Y[i,c(i)]=D[i,i]. Within the subgraph induced by any two
colors, every nontrivial component is a star. Each edge is therefore isolated
in the measurement at a leaf and the other endpoint's color. Choose one such
cell per edge. The chosen edge cells are distinct from each other and from the
diagonal cells. Hence

    ||DX||_F^2 >= sum_i D[i,i]^2 + sum_{edges {i,j}} D[i,j]^2
               >= (1/2) ||D||_F^2.

Consequently the **known six-query design** for treewidth<=2 satisfies

    ||D||_2 <= ||D||_F <= sqrt(2) ||DX||_F

uniformly in dimension and maximum degree. More generally, this proof gives
q=binomial(t+2,2) with the same displayed constant. It is a mathematical upper
bound, not a claim about the complete computational cost of obtaining the
support decomposition/coloring, querying a physical operator, or certifying
noisy data.

## Precise continuation boundary

Existence of some bounded query count q(t) with uniform inverse control is already
settled by this classical construction. The sharp star-coloring lower bound of
six at treewidth two does **not** imply that six arbitrary real dense queries
are necessary, because dense designs need not represent color classes.

A distinct programme question can ask whether **three** real query coordinates,
with each row norm at most one, suffice for a dimension-independent constant in
`||D||_2 <= C ||DX||_F` uniformly over all symmetric matrices on each known graph
of treewidth at most two. The theorem above provides an explicit six-query
comparator but does not answer that three-query question. This source check does
not establish that the latter question is historically open; it is the unresolved
boundary identified within the present programme.

## Source costs

Two web batches, each reporting about2.6 seconds wall latency: **5.2 seconds**
total observed source-access time. No failed retrievals, numerical calls or new
probes. Interpretation, source writing, inference, monetary cost and energy are
not metered. Root citation refs: `turn72view0` is the primary full paper;
`turn72view1` supplies Theorems6.1 and6.3; `turn72view3` includes Corollary6.4.
Root must open the primary source before using a final citation.
