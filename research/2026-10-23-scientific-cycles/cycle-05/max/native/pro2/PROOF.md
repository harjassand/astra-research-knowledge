# Stable coordinate information: exact cut witnesses and four-query operations

PRO 2, 22 October 2026 Australia/Brisbane. Cycle4 owner checkpoint.
This file contains the main argument. All predecessor archives remain unchanged.
Historical originality is not claimed. The full four-versus-five question for
arbitrary real designs on treewidth-two, maximum-degree-four graphs is OPEN here.

## 1. Contract and quantifiers

G is a finite known simple undirected graph on n vertices. S_G consists of all
real symmetric matrices with arbitrary diagonal and off-diagonal support in G.
The graph is supplied before the design. A design X has q columns and satisfies
the total energy cap ||X_i,:||_2<=1 at every vertex. Observations are Y=DX+E,
with arbitrary absolute Frobenius action error E. The objective is a decoder L
with L(DX)=D and ||L(DX+E)-D||_2<=C||E||_F uniformly in n, D and E.

The theorem in Sections2-5 is explicitly for proper coordinate designs
X_i=e_{c(i)}. It characterizes this representation, not all dense real designs.
The positive constructions in Sections6-7 are valid admitted four-column designs.
Their row norms equal one. They do not need probabilistic or independent noise.

For a proper coloring, let K be the largest nontrivial bichromatic component
size (K=1 if there are no edges), Delta the graph maximum degree, and r the
maximum number of distinct neighbor colors at one vertex. Thus
r<=min(Delta,q-1). Let

    rho(G,X)=sup_{0!=D in S_G} ||D||_2/||DX||_F.

The value is infinite when the action map has a nonzero kernel.

## 2. Exact information decomposition

The own-color cell of row i contains exactly D_ii. For each unordered color
pair {a,b}, a connected nontrivial bichromatic component T has one action cell
per vertex: row i, coordinate equal to its opposite color. Its edge coefficients
w act through the unsigned incidence matrix B_T:

    y=B_T w.

These selected cells are disjoint between components, pairs, and diagonals.
This orthogonality is with respect to the actual Frobenius norm on all actions.

Because every such component is bipartite, a cycle is even. Put alternating
weights +1,-1 on its edges and zero elsewhere, including all diagonals. Both
incident cycle weights cancel at every vertex, so DX=0 although D!=0. Chords
cause no difficulty because their matrix coefficients are zero. Consequently
coordinate recovery is impossible if ANY bichromatic component has a cycle.

If every component is a tree, B_T has full column rank. Indeed, successively
removing leaves forces every coefficient of a kernel vector to vanish. The
diagonal readings and these incidence inverses recover all coefficients.
Thus exact coordinate recovery is equivalent to acyclicity of the coloring.
This is the classical sparse-Hessian/acyclic-coloring mechanism; see Section10.

## 3. Exact linear-time least-squares decoder

For a tree T with N vertices, give color a vertices sign +1 and color b
vertices sign -1; call the sign sigma_i. Then A=diag(sigma) B_T is an oriented
incidence matrix: each column has one +1 and one -1. Its range is the
zero-sum subspace. For arbitrary observed y, put f_i=sigma_i y_i and project

    f0=f-(sum_i f_i/N) 1.

Root T at any vertex. For an edge e from a parent to child v, let S_v be the
child-side subtree, a=|S_v|, b=N-a. The unique least-squares edge estimate is

    w_hat_e = sigma_v [ sum_{i in S_v} f_i - (a/N) sum_{i in T} f_i ].     (1)

Its signed boundary sum is sigma_v w_hat_e, which proves the formula.
Postorder subtree sizes and sums compute all estimates in O(N) arithmetic.
The diagonal is read directly. The final matrix is symmetric by construction.

The code src/coordinate_decoder.py implements exactly (1), validates properness
and absence of bichromatic cycles, and returns rational bounds determined by
the graph and coloring before any matrix coefficient is inspected. Preparation
and decoding cost O(nq+m) operations and storage, for fixed q O(n+m). Rational
bit cost and external action acquisition are separate; see COSTS.md.

## 4. Exact cut witness: the lower error mechanism

The row functional in (1) has squared Euclidean norm

    kappa_e^2 = a(1-a/N)^2 + b(a/N)^2 = ab/N.                           (2)

This value is also an explicit information lower bound. Define the oriented
divergence f_i=1/a on S_v and f_i=-1/b on its complement. Its sum is zero.
Solve A w=f using (1), put these edge coefficients in D and all other
coefficients zero. Then |w_e|=1,

    ||D||_2 >= |D_parent,child| = 1,
    ||DX||_F^2 = ||f||_2^2 = 1/a+1/b = N/(ab).

Therefore

    rho(G,X) >= max_e sqrt(a_e b_e/N_e).                              (3)

The proof is not about one chosen decoder. Any estimator satisfying the
required zero-error exactness must return zero at the zero observation.
For true D and action noise E=-DX that observation is again zero, so its
guarantee forces the same lower bound. With a cycle, the exact kernel already
precludes such an estimator.

For a tree of size N>=2 and maximum degree at most Delta, choose a centroid
vertex: every component remaining after its deletion has at most N/2 vertices.
Existence follows by moving toward a component of size>N/2 until none remains;
the oversized side strictly shrinks. The largest of at most Delta components
has size a>=(N-1)/Delta. Its incident edge has b=N-a>=N/2. Equation(3) gives

    rho(G,X) >= sqrt((N-1)/(2 Delta)).                                 (4)

Also rho>=1 from a single free diagonal coefficient. The Delta=0 case has
K=1 and rho=1 and is handled separately.

## 5. Upper error bound and sharp size dependence

Formula(1) is a linear exact decoder for every real input, not only rational
tests. Let E_T be the action noise in a tree's selected cells; signing it and
projecting to zero mean cannot increase its norm.

Fix a vertex v in T and root the tree at v for this argument. The branches
S_e over edges incident to v partition T\{v}. To bound the sum of the absolute
edge errors, choose signs epsilon_e so that this sum is the signed sum of
their subtree expressions. The resulting coefficient vector h equals +1 or
-1 on each branch and zero at v. After the mean projection its norm is at
most ||h||=sqrt(N-1). Thus

    sum_{e incident to v in T} |error_e| <= sqrt(N-1) ||E_T||_2.         (5)

For fixed v, the relevant tree components come from distinct opposite colors;
their action-cell sets are disjoint. There are at most r such components.
Summing(5), applying Cauchy, and including the one independent diagonal cell,
gives an absolute row-sum error bound

    |error_vv|+sum_{u adjacent v}|error_vu|
        <= sqrt(1+r(K-1)) ||E||_F.

A real symmetric matrix has operator norm at most its maximum absolute row
sum. Hence this explicit decoder satisfies

    ||L(DX+E)-D||_2 <= sqrt(1+r(K-1)) ||E||_F.                         (6)

A graph-specific stronger value replaces r(K-1) by
max_v sum_{T containing v}(N_T-1). The source computes this integer certificate.
Another independent Frobenius certificate follows directly from (2): the
squared Hilbert-Schmidt norm of B_T^+ is sum_e a_e b_e/N. Since off-diagonals
are copied twice,

    ||L(E)||_F^2 <= max(1, max_T 2 sum_e a_e b_e/N_T) ||E||_F^2.        (7)

The two estimates may be compared without optimization or a floating solver.

Combining(4) and(6), for Delta>=1 and an acyclic proper coordinate coloring,

 max(1,sqrt((K-1)/(2 Delta))) <= rho(G,X)
       <= ||L||_(F->op) <= sqrt(1+min(Delta,q-1)(K-1)).                (8)

Thus for a uniformly bounded-degree class, a family of proper coordinate
designs has a dimension-independent operator-error inverse IF AND ONLY IF
every bichromatic component is a tree and their sizes are uniformly bounded.
The dependence is of order sqrt(K) at fixed Delta,q. This equivalence is not
true without the degree bound: arbitrary large stars have stable coordinate
recovery. It is not an impossibility theorem for arbitrary real query rows.

Scientific consequence: an acyclic or linear coloring theorem establishing
exact identification does not by itself supply the required noise guarantee.
The missing combinatorial invariant is now explicit and checkable, and a
failed candidate comes with an exact action-noise witness rather than merely
a small floating singular value.

For a numerical implementation, let P be the orthogonal action-space
projection used above: sign, subtract each component mean, sign back; keep
diagonal channels and zero unused channels. If the output D_hat is symmetric
and supported and its rigorously bounded residual is

    R = D_hat X - P Y,

then (6) gives the a posteriori allowance

    ||D_hat-D||_2 <= sqrt(1+r(K-1)) (||E||_F+||R||_F).                 (8a)

One may use the smaller certified constant from(7) or the graph-specific
version of(6). A computed residual must include rounding in its evaluation.
If the physical query is X+deltaX, its extra action error is D deltaX and
needs a bound such as ||D||_2||deltaX||_F; the row cap alone does not supply
that bound. The coordinate seeds here use exactly representable0/1 entries.
The executable tests use exact rational arithmetic, so they do not require
an uncharged floating-solver status or an unproved residual estimate.

## 6. Four queries on every supplied bandwidth-two support

Suppose the supplied vertex ordering has every edge of length at most two.
Repeat colors (0,1,2,0,3,1,0,2,3). All consecutive triples have distinct colors.
Each pair involving color0 induces disjoint paths of at most five vertices;
the other three pairs induce matchings. research/literature/PERIOD9_LEMMA.md
gives the complete periodic gap table and all-size argument. Deleting edges
only shortens these components, so the same operation covers every subpattern.

For a path on ell vertices, B^T B has diagonal2 and adjacent off-diagonal1.
Its eigenvalues are 2+2cos(j pi/ell), j=1,...,ell-1, obtained by sine vectors.
For ell<=5 the minimum is at least alpha=(3-sqrt5)/2. Equation(7), or direct
block singular-value summation, therefore sharpens the generic certificate to

    ||L(DX+E)-D||_2 <= ||L(DX+E)-D||_F
                    <= sqrt(3+sqrt5) ||E||_F.                         (9)

The rational checker uses the slightly weaker squared constant16/3, proved
by positive leading minors of B^T B-(3/8)I, not a numerical eigenvalue status.
The code is an actual O(n) decoder and the data include both a full and an
edge-deleted support.

The unchanged predecessor contains the accepted all-dense-design three-query
lower on P_(8m)^2: the operator inverse diverges at least n^(1/4)/sqrt(24sqrt5).
With that inherited dependency, the worst-case stable query minimum for the
entire bandwidth-two support class is EXACTLY FOUR. We did not replay or
claim a new proof of that lower in this cycle.

The stronger ordinary five-query comparator on this subclass is X_i=e_(i mod5).
Each closed band neighborhood has distinct colors; the action map is a
Frobenius isometry. Reading diagonals and averaging the two readings of each
edge gives ||L(E)||_F<=||E||_F. Thus four saves one action but accepts the
larger error constant in(9). No total runtime advantage is established.

## 7. Four queries on a genuinely branching class

Let T be any supplied rooted forest. Form Q=T Cartesian-product K2 with
vertices(v,0),(v,1), two copies of each forest edge, and the rung(v,0)(v,1).
Let d(v) be depth and a=(0,2,1,3), extended periodically. Set

    c(v,0)=a_(d(v)),    c(v,1)=a_(d(v)+2).

The two rung pairs are01 and23. The other four pairs02,12,13,03 occur only
on forest edges, within a single layer, and at one parent-depth residue
modulo4 in that layer. Consequently a bichromatic component cannot change
layers or cross consecutive level pairs. Every child has one parent, so each
such component is a star. This is a four-star-coloring for every forest T.
The exact pair table and independent argument are in
research/degree4_structure/PRISM_COLORING_REVIEW.md.

For a star with d edges, B^T B=I+11^T, so its minimum eigenvalue is at least1
(it is2 for a single edge). Disjoint action-cell summation yields

    ||L(DX+E)-D||_2 <= ||L(DX+E)-D||_F <= sqrt2 ||E||_F.               (10)

This applies to all known subgraphs of Q too. Constructing the depth colors,
components and decoder costs O(|V(T)|+|E(T)|). No degree restriction is needed
for this positive theorem. If Delta(T)<=3, then Delta(Q)<=4, and Q has
treewidth<=2: each parent-child square has two bags {p0,p1,v0} and
{p1,v0,v1}, attached to a bag containing the parent rung. These bags form a
width-two decomposition. Thus(10) is a receiving use within the current class.

The family is not subsumed by a bounded-bandwidth result. For the complete
binary tree of height h, Q has n=2(2^(h+1)-1) and diameter2h+1. Any ordering
of bandwidth b must satisfy n-1<=b(2h+1), by considering a path between its
first and last labeled vertices. Its bandwidth therefore grows without bound.
The structural counterexample supplied by a contributor became a constructive
receiving use, not a new query lower bound. No all-design q3 lower on prisms
is claimed; no historical originality of this coloring is claimed.

## 8. Actual same-graph failure and repair

The fixed exact experiment uses the complete binary tree on127 vertices,
hence a254-vertex prism. The naive proper four-color design uses colors
d mod2 in layer0 and2+d mod2 in layer1. Its bichromatic components include
the entire127-vertex trees. It is acyclic and exactly identifiable, yet the
cut witness on a63/64 split has

    |D_e|=1,
    ||D X_bad||_F^2=127/4032,
    rho(G,X_bad)>=sqrt(4032/127).

On the SAME matrix D and support, the new prism seed has

    ||D X_good||_F^2=3167639/451584,

and enjoys the global guarantee(10). This is an explicit bad-design mechanism
and a distinct admitted design on that same graph, not a graph hard for every
design. The exact data, complete coefficients, action arrays and noisy outputs
are in results/coordinate_operations.json. The test also includes a four-cycle
alternating exact kernel and the five-query bandwidth comparator. There was no
precision sweep, optimization retuning or external-oracle performance test.

## 9. Retained signed representation and precise remaining gap

The independently developed six-row period-six real design is retained at
research/local_nullspace/PROOF.md. Its local row ambiguity reduces by symmetry
to a scalar signed edge operator Q. An exact SOS proves sigma_min(Q)^2>=7/16
on squared paths, with a four-query Frobenius constant about5.0413 and a
pentadiagonal O(n) decoder. The period-nine coordinate operation has the
better constant on that class, so the signed design is not promoted as the
winning comparator. Its reusable value is the local-kernel/compatibility
representation for query rows beyond an orthonormal palette.

research/degree4_structure/PROOF.md gives a rational local triangle decoder
with constant20 on supplied genuine degree-four 2-tree completions, but proves
these completions comprise only squared paths and two finite exceptions.
General partial2trees can fail to admit degree-preserving completions. That
conditional theorem is not used to infer the full-class result.

The full selected class still has the inherited bounds FOUR<=q_stable<=FIVE.
The lower comes from squared paths; the upper is the admitted 17-color G^2
full-spark R5 construction. A possible route now has an exact obligation:
find a uniform K and an acyclic proper four-coloring with bichromatic
component size<=K for every graph in the class. Theorem(8) says that this is
both necessary and sufficient within proper coordinate designs. A proof that
no such coloring exists would retire that representation, not arbitrary real
four-column designs. The scalar local-kernel representation remains the next
non-coordinate option. No universal four-query obstruction is claimed.

## 10. Closest primary literature and novelty boundary

Gebremedhin, Pothen, Tarafdar and Walther, Efficient Computation of Sparse
Hessians using Coloring and Automatic Differentiation, INFORMS J.Comput.2009,
https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf:
Sections2-3 give the classical star/acyclic compression and tree recovery.
Theorem3.1 bounds substitution error in terms of subtree size. Our argument
uses the stated absolute Frobenius-to-operator contract, exact cut witnesses
and mean-projected least squares; it does not claim discovery of acyclic
recovery or deny the paper's differently scoped stability statement.

Aravind and Subramanian, Bounds on vertex colorings with restrictions on the
union of color classes,2010,
https://people.iith.ac.in/aravind/Files/jgt-gvc.pdf:
Definition1.2 formalizes bounded bichromatic components as(2,K)-colorings.
Acyclicity is an additional needed property for the current coordinate inverse.
Their general degree bounds do not supply four colors for this exact class.

The focused contributor also read Esperet, Montassier and Raspaud, Linear
choosability of graphs, Discrete Math.2008, author report
https://oc.g-scop.grenoble-inp.fr/esperet/publications/RR-1382-06.pdf.
It gives four linear colors for outerplanar maximum-degree-four graphs, but
the inspected statement supplies no uniform bichromatic path-size bound and
does not cover all partial2trees. Root's direct fetch of this PDF timed out;
the contributor's source notes are preserved and this theorem is not a
dependency of any positive or negative result above.

Coleman and Cai's original institutional report, The Cyclic Coloring Problem
and Estimation of Sparse Hessian Matrices, advertises a substitution
characterization and a roundoff bound (DOI10.1137/0607026):
https://ecommons.cornell.edu/entities/publication/9e03cca8-ab7d-406d-a78e-314ecd6b897f.
The focused reviewer could read the landing page but not its PDF. That older
bound must be compared before making a historical stability-priority claim.

These results are new executable/structural consequences relative to the
owner checkpoint. Historical priority of the size criterion, periods or
prism coloring has not been established. Internal proof, executable checking,
historical originality, and practical performance are distinct statuses.
