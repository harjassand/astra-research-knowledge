# Four stable actions on chordless width two atoms

Pro2, 22 October 2026. This is a constructive result relative to the Cycle7
checkpoint. Historical priority and external acceptance are not claimed.
The literal finite certificate, independent checker and structural proofs are
parts of the proof, not optional numerical illustrations.

## 1. Contract and strongest theorem

Let G=(V,E) be a known finite simple graph. Let S_G be the real vector space
of symmetric matrices with arbitrary diagonal and arbitrary entries on E,
zero elsewhere. The graph is supplied before the design. Choose a real
n-by-q matrix X with Euclidean norm at most one in EACH whole row. All q
original actions are observed as Y=DX+E_noise; the noise is arbitrary and
its norm is the absolute Frobenius norm. The required output is the original
supported symmetric matrix, with exact noiseless recovery and a uniform
operator-norm error bound. There is no known coefficient, relative noise,
reduced-action oracle, spectrum normalization or favorable noise law.

**Theorem A.** Every finite simple two-connected chordless graph G with
treewidth at most two and maximum degree at most four has a graph-adapted
coordinate design with at most four columns and an exact linear inverse R
such that, for every D in S_G and every real action error E_noise,

    ||R(DX+E_noise)-D||op <= sqrt(3/2) ||E_noise||F,
    ||R(DX+E_noise)-D||F  <= sqrt(2)   ||E_noise||F.

Every design row has norm exactly one. For G=C3 the three-coordinate identity
design and symmetrization have the stronger constant one. The other supports
are triangle-free. Preparation uses the original graph; it preserves every
vertex and edge. An explicit graph reduction and coloring algorithm are
supplied below. This is an intrinsic graph class, not merely an existential
promise that a convenient recursive expression happens to be available.

The constructive theorem has two independently checkable parts:

* Theorem B: a nonempty finite guarantee system colors every expression in a
  loaded two-terminal grammar, at every finite depth, with four star colors.
* Theorem C: every nontriangle graph in Theorem A has such an expression
  without any support change.

Four is necessary for star-coordinate coloring on this class because C5 is
included and is not star-three-colorable. This is NOT an arbitrary-real
three-query lower bound for this class. The full class of all width-two,
degree-four supports still has the inherited lower q>=4 and upper q<=5;
arbitrary-real q4 for that full class remains open.

## 2. The exact loaded grammar

A module has two distinct ordered, nonadjacent terminals s,t, each with
positive actual degree. Every vertex has degree at most four. Copies of
children are disjoint before only the stated identifications. Productions:

1. A path of length at least two, with its endpoints as terminals.
2. S(G1,G2): identify the right terminal of G1 and the left terminal of G2;
   retain the other two terminals. Require the sum of the joined degrees<=4.
3. P(G1,G2): identify corresponding terminal pairs. Require BOTH sums of
   actual terminal degrees<=4.
4. L(G), respectively R(G): add one fresh leaf and its edge at the left,
   respectively right, terminal, making that leaf the new terminal. The old
   terminal must have degree<=3.

Every added leaf/edge is an actual part of the graph described by the input.
These rules do not authorize adding stubs to a support that lacks them.
Arbitrary path lengths normalize to path2 plus endpoint extensions. Higher
series/parallel arities associate to binary nodes; positive loads ensure
intermediate sums obey the same cap when the final sum does.

These expressions are simple, triangle-free, chordless, series-parallel and
degree<=4. They also have every simple terminal-to-terminal path induced and
every edge on some terminal path. The structural induction is in
research/structural_scope/PROOF.md. In a parallel composition a cycle is either
inside one child or consists of induced paths in two different children;
their interiors are disjoint and there is no terminal edge. In series no
cycle crosses the joined cut vertex. Extensions create no cycle. These facts
prove chordlessness and the terminal-path invariant, not just a diameter or
local-rank condition.

The grammar contains the full Cycle7 grammar: its stubbed parallel operation
is ordinary parallel followed by L and R, retaining the original stubs. It
also includes the previously excluded A_L atoms at loads (4,3), including
intermediate loads (2,1). The grammar alone still excludes a C4 with leaves
attached to adjacent cycle vertices: its only possible terminals are the
leaves, and their longer connecting path has a chord. This is a remaining
representation boundary, not a recovery lower bound.

## 3. Exact boundary information and the star condition

A proper coloring is a star coloring if it has no two-colored path on four
distinct vertices. For an edge uv, such a path has uv as its middle edge iff
u has another neighbor of color c(v) AND v has another neighbor of color
c(u). The two extra vertices are distinct because their colors differ.
Thus the following edge test is exact:

    not [n_u(c(v))>=2 and n_v(c(u))>=2] for every edge uv.

For a terminal v of an already star-colored module, retain its color a,
the actual counts n(c) of neighbors of each color c, and a far-end flag

    F(c)=1 iff some neighbor u of color c has another neighbor of color a.

Validity implies n(c)>=2 => F(c)=0. On a merge of equally colored ports,
counts add and flags OR. The exact acceptance test is that no resulting
count>=2 has flag one, and the actual degree sum is at most four. A series
join retains the other two port records. Parallel tests both pairs.

For a left extension giving the new leaf color A, acceptance is exactly
A!=a, old degree<=3, and F(A)=0. The new terminal has degree one, neighbor
color a, and its flag at a is [n(A)>0]. The other terminal record is unchanged.

Why are there no missing remote flags? Only a joined terminal acquires
neighbors. Every old neighbor of it is an interior vertex, since terminals
are nonadjacent. That vertex retains its color-labelled adjacency list.
Even a common neighbor of the two terminals retains two distinct neighbors
with the same colors as before. Child interiors are disjoint, so counts are
real sums and no duplicate edge is concealed. Necessity follows by restriction
of any valid parent coloring; sufficiency follows from the exact bad-edge
test. These are all-size statements; the actual finite graph enumerations
in verification/port_lemma supplement their implementation only.

Adjacent ports would invalidate the formulas: concatenating single edges
colored 0-1 and 1-0 creates new outer flags not retained by the nonadjacent
series rule. The hypotheses are therefore essential.

## 4. Two proved reductions of the state space

### 4.1 Saturated ports

A degree-four terminal cannot ever be merged with a positive-load child or
extended under this degree cap. It can only persist untouched as an outer
port. Its entire exposed record can therefore be replaced by SAT4. Its
actual graph vertex and actual color still exist. SAT4 means existentially
unspecified color, not a fifth color and not arbitrary future color control.
The merge that CREATES degree four is checked before projection. This is a
contextual congruence for the admitted operations; see
verification/port_lemma/SATURATION_QUOTIENT.md.

### 4.2 Exact occupancy quotient

For an active port retain (a,d,N,F), where d=sum n(c) is the exact actual
degree and N={c:n(c)>0}. Actual multiplicities remain in the realizing
coloring. They need not be prescribed in the continuation state.

For two already valid children of the same port color, merging is accepted iff

    d1+d2<=4 and N1 intersect N2 intersect (F1 union F2) is empty.

The output is (a,d1+d2,N1 union N2,F1 union F2). If c occurs on both sides,
the combined count is at least two and a flag on either side is exactly the
new danger. If c occurs on one side only, its count and flags are unchanged
from an already-valid child. These exhaustive alternatives prove the quotient
exact for all admitted continuations. Extension uses only A in N and A in F.

The already-valid-child premise is essential. A syntactic state does not
prove its own internal validity. Concentrating multiplicity in one color is
safe in a replacement only when an actual star realization is supplied.
The full proof is verification/port_lemma/SUPPORT_QUOTIENT.md.

### 4.3 Monotone upper-bound guarantees

At fixed visible terminal colors, actual degree pair and SAT4 positions,
write sigma<=tau if sigma has subsets of tau's neighbor-support and flag
sets at both active ports. The merge rejection predicate and its unions are
monotone; extension's rejection flag and new membership flag are monotone.
Replacing realizing children by smaller profiles preserves acceptance and
produces a smaller output profile. Actual total degrees stay exact.

A guarantee family is a nonempty finite list of target profiles. It promises
that EVERY target has some actual star realization with those exact visible
colors and degrees, and supports/flags contained in the target bounds. It
does not promise equality of those sets or of discarded count vectors.
Global color permutations preserve the guarantee. One permutation applies
to BOTH ports of a child; their colors cannot be relabelled independently.

## 5. Literal finite certificate and complete induction

The proof object is results/loaded_star_certificate.json:

* 982625 bytes;
* SHA256 63f4cdfd7ccc3b3159782a28a144a199422a315975aa207e5d144e8659e53525;
* 73 nonempty degree-homogeneous families;
* 608 canonical target profiles;
* 3225 degree-admissible operation/family cases;
* 11142 literal child witnesses, plus two actual path2 leaf witnesses.

The eight entries of a profile are (a,b,dL,NL,FL,dR,NR,FR); sets are masks on
the actual color labels 0,1,2,3. SAT4 uses degree4, color -1 and zero masks.
The finite table covers 69 L cases, 69 R cases, 2521 ordered S cases and
566 unordered P cases. Every parent target has an explicit witness in every
case assigning child targets in the children’s global color orbits. The
result of the exact transition is below that parent target.

verification/finite_gate/verify_certificate.py imports no producer module.
Its independent set-valued algebra demands every admissible case exactly
once, checks actual degrees, all output targets, global relabelings, every
merge before saturation, both extensions and the path2 leaf enumeration.
All 11142 witnesses passed on the first check. This is not a solver's status,
an extrapolation from sampled depths or an assumed nonempty interface.

Induct over a finite expression. The leaf witnesses establish their family
guarantee. At a node, classify the child families and use the corresponding
literal case to select the parent family. For each requested parent target,
its witness chooses child target profiles. Their guarantees realize profiles
no larger than those targets. The exact transition and monotonicity lemmas
glue those real colorings to a valid parent coloring below its target. The
parent family is nonempty. Thus every finite expression has a star-four
coloring. No depth-, mass- or component-growth term remains unproved.

Construction labels nodes bottom-up, then follows witnesses top-down using
explicit stacks. At most 24 color relabelings per node are a fixed constant.
src/loaded_recovery.py expands disjoint occurrences, resolves actual colors
of saturated vertices, and checks actual multiplicities on the whole original
graph. The finite certificate is sufficient to run construction; discovery
need not be rerun. The search that found it and all bounded unsuccessful
attempts remain archived and charged.

## 6. Intrinsic atom coverage without changing support

The full proof is research/structural_scope/ALL_CHORDLESS_ATOMS.md. Its new
load-bearing scope was challenged independently in verification/atom_scope/.
Here is the complete mechanism.

Protect any actual edge uv of a two-connected width-two graph. A width-two
decomposition rooted at a bag containing uv has a degree-two vertex w outside
{u,v}: after contracting contained neighboring bags, an exclusive vertex of
a nonroot leaf bag has degree<=2; two-connectivity gives equality. If only
one bag remains the same conclusion is immediate. Suppressing w replaces
its two incident edge labels by their series composition, put in parallel
with an existing edge label when necessary. The simple reduced graph is a
minor, stays two-connected while it has at least three vertices, and retains
uv. Labels partition the original edges, with disjoint interiors. Continue
until only uv remains. This produces an ordinary edge-based TTSP expression.

The protected original uv edge has only parallel ancestors. Chordlessness
allows only one other branch H; two others would form a cycle chorded by uv.
Thus G=P(edge uv,H). If H has no parallel node, G is a cycle. For a cycle of
length>=4 choose two nonadjacent vertices and use its two original arcs.

Otherwise choose an internal parallel node N. Its complement is a nonempty
TTSP network between the same terminals. This is constructive: at a series
ancestor with prefix A and suffix B, the new complement is
S(reverse(A),old_complement,reverse(B)); at a parallel ancestor it is the
parallel of the old complement and the other children. Empty prefixes/suffixes
are omitted. Orientation flags and node references avoid copying expanded
subgraphs. The whole graph is now parallel on N's children and its complement,
at least three genuine branches. Its new terminals x,y are nonadjacent: an
xy edge would chord the cycle through two other branches.

Every simple x-y path is contained in one branch and closes to a cycle with
a path in another. A chord of that path would chord the cycle. Thus every
terminal path is induced. Every submodule terminal path extends to an outer
terminal path, so a parallel node cannot have a single-edge child: that edge
would chord a path through another child. Binary normalization is exhaustive:

| Ordinary series children | Loaded production |
| --- | --- |
| edge, edge | path2 on those same three vertices |
| edge, module | left extension by that existing edge |
| module, edge | right extension by that existing edge |
| module, module | series |

Every parallel child is a module, so ordinary parallel remains admitted.
Every intermediate module is an actual edge-subgraph of G; consequently its
degree sums and extension budgets are at most the final degree four. There
is no subdivision, deletion, duplicate coefficient or reduced action.

A two-connected chordless graph containing a triangle is that triangle:
otherwise an outside connected component has neighbors at two triangle
vertices, giving an outside path and a cycle chorded by their triangle edge.
This proves the stated C3 exception and triangle-freeness of all other atoms.
It also completes Theorem C and the graph-class part of Theorem A.

src/atom_normal_form.py implements protected-edge suppression, complement
rerooting, binary normalization, and coloring directly on original vertex IDs.
Its returned normal form has exact original-edge binding. The native receiving
input is just inputs/native_atom_9.json, not a supplied decomposition oracle.

The bounded-degree structural algorithm can use O(n+m) combinatorial work
and storage: suppression never increases reduced degree and every update
inspects at most four neighbors. The current Python native implementation
also sorts canonical edge lists for reproducibility/support comparison and
therefore has the conservative O(n+m log m) comparison-work bound. Its cycle
walks, suppression, reference rerooting and witness decoding are linear.
Dictionary/set bounds use the usual word-RAM convention. Neither statement
is a free recognition promise for arbitrary inputs outside the stated class.

## 7. Full original action inverse and all-noise proof

For the actual star coloring set X_i=e_c(i). The own-color action cell at i
contains D_ii alone. Each unordered color pair decomposes into stars; its
edge coefficients map to the selected action cells by unsigned incidence.
Different components, pairs and diagonal cells are disjoint.

For a k-edge star the Gram matrix is I_k+11^T. Its least singular value is
at least one. Thus least-squares edge error squared is at most the squared
norm of its selected input error. A symmetric off-diagonal entry is counted
twice in the matrix Frobenius norm. Summing disjoint input cells proves
||Dhat-D||F^2<=2||E_noise||F^2. Equivalently, with center observation y0 and
leaf observations yi, the edge estimate is

    d_i_hat = y_i + (y0-sum_j y_j)/(k+1).

The actual inherited coordinate_decoder.py computes the same canonical LS
inverse by signed divergence projection and subtree sums. It remains unchanged
from Cycle7. Independent receiving checkers instead use the analytic star
formula above and check all normal equations, so they do not merely import
and repeat the producer decoder.

For the stronger operator bound, choose a direct exact inverse T reading each
edge from one leaf's isolated action cell and each diagonal from its own cell.
These input cells are distinct. For a unit z put w_i=z_i^2. The squared dual
norm of E_noise -> z^T T(E_noise)z is

    Q_G(w)=sum_i w_i^2 + 4 sum_{ij in E} w_i w_j,  sum_i w_i=1.

Move mass between two nonadjacent positive-weight vertices while fixing their
sum. This quadratic is convex in the moved mass, so one endpoint does not
decrease Q and removes one positive vertex. Repeating leaves clique support.
In a triangle-free graph that clique has size<=2; its value is
a^2+b^2+4ab=1+2ab<=3/2. Therefore ||T||_(F->op)<=sqrt(3/2).

Let Pi be the orthogonal projection onto the range of the full supported
action map L:D->DX. Its canonical LS inverse R equals T Pi because T is
exact on the range and PiY has a unique supported preimage. Pi is a contraction,
so ||R||_(F->op)<=sqrt(3/2). This uses the actual Cycle2/Cycle7 operator proof
on the new colorings, not a new asserted sharp constant. LS sharpness is not
claimed. C3 uses X=I3 and symmetrization, with constant<=1.

For an inexact supported symmetric candidate, independently bound its
projected-action residual R_num=Dhat X-PiY. Then

    ||Dhat-D||op <= sqrt(3/2)(||E_noise||F+||R_num||F).

Acquisition and assembly errors belong in E_noise or require separate bounds.
If the actual probe is X+deltaX, D deltaX must also be paid; the row cap alone
does not bound it. Saved operations use exact rational inputs/outputs and
have R_num=0. Their raw Y-minus-recovered-action residual need not be zero.

Color/witness preparation on a supplied expression costs O(p+nq+m) arithmetic
and storage, including expanded output. Native preparation has the conservative
sorting cost above. The four full matrix actions must actually be acquired.
Explicit sparse fixtures charge their accumulation; another action source
must supply its own acquisition cost. Rational operation counts do not bound
bit complexity. Fixed certificate loading, graph checks and residual work
are included, and no application speedup follows from one fewer action.

## 8. Stronger control on A_L and actual receiving evidence

The new grammar includes every previously excluded A_L, but that family has
an explicit stronger three-query control. Color a=0,b=c=1 and the four doubled
path interiors by2. On the b-c path of length L choose k=2+(L-2) mod3, start
with 101,1021,10201 for k=2,3,4 respectively, and append 201 (L-k)/3 times.
The finite suffix argument and hub-edge check in
research/structural_scope/STRONG_CONTROL_A_L.md prove star coloring for all L.
Since n=L+6 and m=n+2, dim S_G=n+m=2n+2>2n. Every real two-column action map
is noninjective. Hence q3 is both exact- and stable-optimal for A_L, with the
same operator/Frobenius guarantees as a star-four design. A four-query A_L
demonstration alone would not be a query advance.

Three actual receiving operations have saved original D, full DX, nonzero
rational E_noise, Y, output coefficients and projected actions:

| Operation | Vertices | Edges | Queries | Receiving role |
| --- | ---: | ---: | ---: | --- |
| A5 three-action control | 11 | 13 | 3 | Stronger matched control for the new atom family |
| Mixed loaded expression | 16 | 20 | 4 | Higher-load P/S/extensions, saturation, and original five-cycle |
| Native asymmetric atom | 9 | 11 | 4 | Edge-list-to-normal-form-to-original-action operation |

Exact noiseless reconstruction and zero projected-action residual hold.
Each record also saves rational positive-semidefinite pivots certifying
(3/2)||E_noise||F^2 I-(Dhat-D)^2>=0 for its actual error. These dense diagnostics
are additional verification cost, not part of the linear sparse decoder.
Independent checkers import no producer; they bind exact original supports,
recompute actions, use analytic star LS, and check rational matrix factorization.
The universal theorem above supplies all-noise validity beyond those examples.

The mixed graph and native atom contain actual C5 subgraphs. A proper
three-coloring of C5 has class sizes2,2,1; deleting the singleton leaves a
bichromatic P4. Thus these four-color designs are optimal within star-coordinate
coloring. This says nothing about arbitrary-real q3, or other acyclic q3 designs.

## 9. Comparators, significance and remaining gap

Star/Hessian compression, acyclic substitution and linear sparse recovery are
established: Gebremedhin, Pothen, Tarafdar and Walther, Efficient Computation
of Sparse Hessians using Coloring and Automatic Differentiation,
https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf.
Fixed-k star-colorability is expressible in MSO1 and is FPT on bounded
treewidth; see Shalu and Antony, https://arxiv.org/html/2309.04291v1.
Therefore finite decidability or using a coloring is not the advance here.

The closest inspected chordless structure result decomposes a two-connected
chordless graph into 2-sparse pieces through proper two-cutsets: Machado,
de Figueiredo and Trotignon, https://arxiv.org/pdf/1309.1842, Theorems2–3.
That established decomposition does not itself prove compatible star-four
boundary guarantees. The bounded primary search found no matched theorem
covering the strongest new class; that is not a historical priority proof.

The actual advance relative to the owned checkpoint is a realizable
higher-load interface, explicit nonempty all-depth closure, and the
support-preserving structural theorem extending its consequence to ALL
two-connected chordless width-two degree-four atoms. This removes a real
coverage obstruction, including every A_L, without assuming arbitrary colors,
retuning the old constant or replacing full original actions.

Ordinary three-query forests remain the appropriate forest control, and the
five-query full-spark construction remains a uniform control for the full
width-two degree-four class. The full class includes triangle-containing
supports and compositions not covered here. Independent atom colorings do
not automatically compose at cut vertices or clique separators. Existing
P7-squared evidence already makes universal star-four too strong for the
full class; bounded larger bichromatic trees or noncoordinate designs remain
distinct options. No NIST, molecular or physical-performance claim is made.

The chosen next question is a ROOTED atom interface at an actually specified
attachment vertex with residual degree budget, followed by compatible
composition across cut vertices. The current normalizer chooses its own
terminal pair, so it does not silently provide arbitrary prescribed root
states. The next proof must keep realizability, far-end hazards and actual
combined degree, and produce a complete full-action inverse. Its failure
would close that representation only. Full arbitrary-real q4 remains open.
