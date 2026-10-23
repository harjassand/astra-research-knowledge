# Stable recovery with a supplied forest separator

Owner: Astra PRO 2. Scientific checkpoint: 22 October 2026 Australia/Brisbane.
All matrices in the theorems are exact real matrices. Code uses exact rational
inputs and checks; floating decimal displays are explanatory only.

## 1. Contract and strongest result

For a finite simple graph G on n vertices, S_G denotes the real symmetric
matrices whose off-diagonal support is contained in G; every diagonal is free.
A query block X has q columns and satisfies `||X[i,:]||_2 <= 1` for every row.
The entire action is observed as `Y = D X + E`. The noise norm is absolute
Frobenius norm of E, and the primary recovery norm is the operator norm.
The row cap is a total energy cap across the q queries, not a cap per query.

For a fixed block define

\[
 C_2(G,X)=\sup_{0\ne D\in S_G}\frac{\|D\|_2}{\|DX\|_F},
\]

with value infinity for a nonzero kernel. Let F_s be the class of known graphs
supplied with a set S of at most s vertices for which G-S is a forest. Finding
a smallest such set is not part of the input contract or included for free.

**Main theorem.** For every fixed integer s>=0, the minimum fixed query count
for a dimension-independent stable recovery guarantee over F_s is **s+3**.

1. Given S, an explicit coordinate seed uses |S|+3 queries, unit row energy,
   and a direct sparse decoder. For arbitrary real E it satisfies

   \[
   \|\widehat D-D\|_F\le\sqrt2\|E\|_F,
   \qquad
   \|\widehat D-D\|_2\le
   \begin{cases}\sqrt{3/2}\|E\|_F,&S=\varnothing,\\
                 \sqrt{5/3}\|E\|_F,&S\ne\varnothing.
   \end{cases}
   \]

   The operator constants are sharp for the **specified direct decoder** over
   the stated classes. They are not claimed optimal among all decoders.
2. On G=K_s join P_m, for every real row-capped X with q=s+2 and m>=2s+2,

   \[
   C_2(G,X)\ge\max\left\{1,
    \left[2\sqrt{m-1}\sin\frac{(2s+1)\pi}{2m}\right]^{-1/2}\right\}
   \ge\max\left\{1,\frac{m^{1/4}}{\sqrt{(2s+1)\pi}}\right\}.
   \tag{1}
   \]

   Hence no constant, even one depending on s, works for s+2 queries over F_s.
3. The worst-case **exact identification** minimum over this class is s+2.
   The extra query is a stability requirement under this noise/energy contract.

The upper seed is an elementary composition of classical star-color recovery
[R1,R2]. The lower theorem extends the incoming fan projection/flow/lift proof
from one global vertex to a supplied separator of arbitrary fixed size. The
matched all-dense lower bound, its executable exact rational version, and the
specified decoder's operator constant are new results relative to this owner's
checkpoint. Historical originality is not established by the bounded search.

## 2. Positive operation: global coordinates plus three forest coordinates

Enumerate S={a_1,...,a_r}, r<=s. Root every component of T=V(G)\S. In R^(r+3),
put `x_(a_j)=e_j` and `x_v=e_(r+depth(v) mod 3)` for v in T (indices may be
shifted by one). Every row has norm exactly one, and `||X||_F^2=n`.

Recover the coefficients as follows.

* Read a diagonal from the vertex's own coordinate.
* Read an S-T edge from its T endpoint and the S endpoint's unique coordinate.
* Read a forest edge from the child's row and the parent's coordinate.
* For an edge inside S, average the two isolated endpoint readings.
* Output zero at nonedges. Missing border or S-S edges do not need readings.

These cells are isolated: a forest vertex's parent, itself, and its children
occupy three different forest coordinates; S coordinates are distinct from
them and from each other. Each diagonal and each chosen edge cell is distinct
from all the other chosen cells. Thus this is an exact left inverse on S_G.

For an unaveraged off-diagonal read, copying the error to both symmetric entries
costs twice its squared scalar error. For an S-S edge, if its two input errors
are e and f, its squared Frobenius contribution is
`2((e+f)/2)^2 <= e^2+f^2`. Diagonal errors cost their own squares. Distinctness
of the used cells proves the displayed sqrt(2) Frobenius bound.

### Exact operator norm of this decoder over the graph class

Let R map action error to reconstructed symmetric error. For any unit vector z,
write w_i=z_i^2, so w_i>=0 and sum_i w_i=1. By duality between a linear scalar
functional and Frobenius input norm, the squared norm of `E -> z^T R(E) z` is

\[
 Q_G(w)=\sum_iw_i^2
       +2\sum_{\{i,j\}\in E(G[S])}w_iw_j
       +4\sum_{\{i,j\}\in E(G)\setminus E(G[S])}w_iw_j.
 \tag{2}
\]

The coefficient two for S-S edges comes from two cells, each with coefficient
`z_i z_j`; the coefficient four elsewhere comes from the single selected cell
with coefficient `2 z_i z_j`. Taking the supremum over z gives exactly
`||R||_(F->2)^2 = max_{w>=0,sum w=1} Q_G(w)`.

For a forest H and nonnegative weights of total t,

\[
 \sum_{i\in H}w_i^2+4\sum_{\{i,j\}\in E(H)}w_iw_j\le\tfrac32t^2.
 \tag{3}
\]

To prove (3), if two nonadjacent positive-weight vertices remain, keep their
total mass fixed and move mass between them. The expression is convex in this
one variable because there is no edge between them and the two squared terms
have positive quadratic coefficient. At least one endpoint of the interval
does not decrease it; choose that endpoint, removing a positive-weight vertex.
After finitely many steps, the positive support is a clique. A forest clique
has at most two vertices. With masses a,b the expression is
`a^2+b^2+4ab=t^2+2ab<=3t^2/2`. This also covers a one-vertex support.

Set t=sum_(T) w_i and 1-t=sum_(S) w_i. All omitted edges have nonnegative
contributions, so (2),(3) give

\[
 Q_G(w)\le(1-t)^2+4t(1-t)+\tfrac32t^2
          =1+2t-\tfrac32t^2\le\tfrac53.
\]

If S is empty, t=1 and the bound is 3/2. If S is nonempty the bound 5/3 is
attained already by a triangle consisting of one S vertex and one forest edge.
Put error 1/3 in the three selected diagonal cells and 2/3 in the three selected
edge cells. Its input squared norm is 5/3 and the decoder output is
`(2/3)11^T-(1/3)I`, with operator norm 5/3. The ratio is sqrt(5/3).
With S empty, a single forest edge, diagonal errors 1/2 and edge-cell error 1
give input squared norm 3/2 and output norm 3/2. These exact examples prove
sharpness for this decoder, including its choice to use only one forest-edge
reading when another reading might also be isolated.

## 3. Lower-bound family and exhaustive singular cases

Let S contain s vertices forming a clique and T={1,...,m} form a path. Add
every S-T edge. The resulting graph K_s join P_m is in F_s and has a width
s+1 tree decomposition with consecutive bags `S union {i,i+1}`.

Fix **any** real X with q=s+2 columns and row norms at most one. If its S rows
are linearly dependent, a nonzero vector supported on S annihilates X on the
left. Its outer product is a supported nonzero symmetric matrix with zero
action, proving infinity. For s=0 this case is vacuous.

Otherwise rotate the query coordinates orthogonally so that

\[
 X=\begin{pmatrix}0&U\\Z&V\end{pmatrix},
 \qquad U\in\mathbb R^{s\times s}\text{ invertible},\quad
 Z\in\mathbb R^{m\times2}.
\]

Rows z_i of Z are the orthogonal projections off the separator span, so
`r_i=||z_i||<=1`. Put R=V U^(-1). If any adjacent z_i,z_(i+1) are dependent,
the s+2 query rows on the clique `S union {i,i+1}` are dependent. A nonzero
outer product on that clique again gives zero action. This includes zero
projected rows, since every path vertex belongs to an edge for m>=2.

It remains to treat the exhaustive case of nonzero adjacent determinants and
delta=min_i r_i>0. A local witness also gives a needed quantitative bound:
take w with separator part `-R[i,:]^T`, leaf coordinate i equal to one, and
other coordinates zero. Then `w^T X=(z_i^T,0)`, and ww^T is supported on the
separator clique and its edges to this one leaf. Therefore

\[
 \frac{\|ww^T\|_2}{\|ww^T X\|_F}
 =\frac{\|w\|}{r_i}\ge\frac1{r_i},
 \qquad C_2(G,X)\ge\frac1\delta.
 \tag{4}
\]

No row normalization or monotonicity assumption is used. Projected rows can be
arbitrarily short even when all original rows have norm one.

## 4. Slow flows satisfying all separator constraints

Let J be the 90-degree plane rotation. For a real flow c with c_0=c_m=0 define

\[
 \Delta_i=\det(z_i,z_{i+1}),\quad b_i=c_i/\Delta_i,
 \quad
 a_i=-\frac{b_{i-1}\langle z_i,z_{i-1}\rangle+
                 b_i\langle z_i,z_{i+1}\rangle}{r_i^2},
\]

with absent endpoint terms omitted. Let B(c) be the symmetric tridiagonal
matrix with diagonal a_i and path entries b_i. Resolving neighboring rows
parallel/perpendicular to z_i proves the exact identity

\[
 (BZ)_{i,:}^T=\frac{c_i-c_{i-1}}{r_i^2}Jz_i.
 \tag{5}
\]

Consequently

\[
 \|BZ\|_F^2\le\delta^{-2}\sum_{i=1}^m(c_i-c_{i-1})^2,
 \qquad
 \|B\|_2\ge\max_i|b_i|\ge\frac{\|c\|_2}{\sqrt{m-1}}.
 \tag{6}
\]

The last inequality uses `|Delta_i|<=r_i r_(i+1)<=1`. It is an operator-norm
entry bound, not an uncharged replacement of operator norm by Frobenius norm.

Put K=2s+1 and assume m>=K+1. The K vectors
`sin(k*pi*i/m)`, 1<=k<=K, 1<=i<=m-1, are independent Dirichlet path modes,
with difference-energy eigenvalues `4 sin^2(k*pi/(2m))`. Thus every c in their
span obeys

\[
 \sum_{i=1}^m(c_i-c_{i-1})^2
 \le4\sin^2\!\frac{K\pi}{2m}\,\|c\|_2^2.
 \tag{7}
\]

The linear map `c -> R^T B(c) Z` has only 2s scalar outputs. Its kernel in this
K=2s+1 dimensional slow-mode span contains a nonzero flow. Choose such a c.
This uses the full constraint count, without presuming independence or favorable
conditioning of the constraints.

Set

\[
 L=\begin{pmatrix}-R^T\\I_m\end{pmatrix},\qquad
 D=L B(c)L^T
  =\begin{pmatrix}R^TBR&-R^TB\\-BR&B\end{pmatrix}.
 \tag{8}
\]

The top block is permitted on the separator clique, all border entries are
permitted, and the leaf block stays tridiagonal. The principal block B gives
`||D||_2>=||B||_2`. Also `L^T X=[Z,0]`, hence

\[
 DX=\begin{pmatrix}-R^TBZ&0\\BZ&0\end{pmatrix}
    =\begin{pmatrix}0&0\\BZ&0\end{pmatrix}.
 \tag{9}
\]

The separator action cancels **exactly**. No norm of R, U^(-1), L, or the
separator-to-leaf coupling is lost in (9). Bounding that top action instead
of canceling it would be an invalid route to the stated size-independent
comparison and can erase the growing lower bound.

A nonzero flow has nonzero BZ: (5) and the zero boundary values show that zero
action would force every difference and then all of c to vanish. Combining
(6),(7),(9), and putting

\[
 Q=\left[2\sqrt{m-1}\sin\frac{K\pi}{2m}\right]^{-1},
\]

gives `C_2>=delta Q`. Together with (4),
`C_2>=max(1/delta,delta Q)>=sqrt(Q)` and `C_2>=1`. Finally
`sin y<=y` gives `Q>=m/[K*pi*sqrt(m-1)]>=sqrt(m)/(K*pi)`.
This proves (1) for every X, including the earlier singular cases.

For each fixed s the bound diverges as m grows. No optimal exponent or sharp
constant is asserted, and no uniform-in-growing-s divergence is inferred.

## 5. Decoder lower bound, exact identification, and adaptivity scope

Any fixed-X decoder obeying `||R_X(DX+E)-D||_2<=C||E||_F` for every supported D
and every E must recover noiseless inputs exactly. Evaluating it at D=0 with
noise DX, and at D with zero noise, forces `||D||_2<=C||DX||_F`. Therefore (1)
rules out s+2 uniformly stable queries even for nonlinear decoders. Fewer
queries are covered by adding zero columns without changing the row energy.

The exact identification count is different. The clique on S and two adjacent
path vertices requires at least s+2 queries, by a rank-one kernel whenever
fewer directions are used. Conversely, peel leaves from G-S. At each current
forest leaf, there are at most s separator neighbors, one forest neighbor,
and the diagonal: at most s+2 coefficients. A full-spark query block of s+2
columns makes those row vectors independent. Symmetry removes the recovered
column, and induction recovers the matrix; the final S block is no harder.
Such a block exists, for example a Vandermonde block scaled to meet the cap.
This is exact algebra and carries no uniform numerical conditioning claim.

There is also a deterministic adaptive lower-bound extension under the same
adversarial absolute-noise contract. Run a deterministic adaptive algorithm on
the noiseless zero matrix and collect its q=s+2 queries into X. The row cap must
hold on this realized transcript. Choose a D from (1). For input D, supply at
each step the error `-D x_j`; by induction the observed transcript stays the
same zero transcript and every future query stays the same. Exact recovery at
zero forces output zero. The total noise is `-DX`, so the same inverse ratio
is necessary. This does not prove a randomized lower bound for an input fixed
before the algorithm's random choices, nor a restriction on full-entry access.

## 6. Exact rational witness operation

The sine construction is a complete universal proof but is unnecessary for an
exact executable witness. Set K=2s+1 and `h=floor(m/(2K))>=1`. At edge indices
i=0,...,m use K tents

\[
 f_j(i)=\max(0,h-|i-(2j+1)h|),\qquad j=0,\ldots,K-1.
\]

Their positive supports are disjoint, as are their difference supports. Each
has mass `(2h^3+h)/3` and difference energy `2h`. Thus every nonzero linear
combination obeys
`sum(diff c)^2 <= (3/h^2) sum c^2`. Impose the same 2s constraints and take a
nonzero rational null vector. The preceding proof then gives

\[
 C_2(G,X)^4\ge\frac{h^2}{3(m-1)}.
 \tag{10}
\]

The separate bound C_2>=1 remains. The executable deliberately certifies (10),
not equality with the stronger sine expression (1).

To keep rational inputs rational, `src/separator_witness.py` avoids constructing
an orthonormal basis. With T=X[S,:], it forms the exact orthogonal projector
`P=I-T^T(TT^T)^(-1)T`, rational projected rows Z, and rational coefficients R
such that `X[T,:]=R T+Z`. Pick independent rational vectors u,v in the projected
plane, define `J0=v u^T-u v^T`, and put
`kappa=||u||^2||v||^2-<u,v>^2>0`. On that plane `J0^2=-kappa I`.
With `omega_i=<J0 z_i,z_(i+1)>` and `b_i=c_i/omega_i`, the exact flow action is

\[
 (BZ)_{i,:}^T=\frac{c_i-c_{i-1}}{\kappa r_i^2}J_0z_i.
\]

Its squared action carries a factor 1/kappa, and the squared operator-entry
bound carries the same factor because `|omega_i|<=sqrt(kappa)`. They cancel
in the inverse ratio. Two rational coordinates (inner products with u,v) per
separator row suffice to impose the full vector constraint.

The source returns both the flow witness and the local rank-one witness. Each
is stored as exact sparse upper-triangle entries and exact rational X. The
independent checker uses the entries themselves to compute DX, support,
row norms, a path-entry operator lower bound and the rank-one norm, without
importing the producer. Exact kernels are stored for the two singular cases.
No floating solver status, approximate rank, or rounded surrogate is accepted.

At fixed s, construction takes O(m) rational arithmetic operations and O(m)
storage; for varying s the straightforward implementation has polynomial
factors in s. Fraction numerator and denominator growth is additional: there
is no claim of uniformly bounded bit complexity or a stable floating witness
generator for ill-conditioned arbitrary X. The positive decoder has neither
those divisions nor those conditioning dependencies.

## 7. Failed compression routes and their exact scope

Before choosing the separator result, we attempted to compress a classical
star-color seed. Both failures are preserved with complete notes and checks.

**Palette-preserving compression obstruction.** For c colors, form c disjoint
stars, one with center of each color i, and N leaves of every other color at
that center. This is a fixed c-star-colored forest. For any capped palette
vectors p_1,...,p_c in R^q with q<c, choose a dependence sum_j alpha_j p_j=0
with max_j|alpha_j|=1, and pivot at a maximum coefficient. On that star place
alpha_i on its diagonal and alpha_j/N on each edge to color j; other entries
are zero. The center action cancels and total leaf action squared is at most
(c-1)/N, whereas operator norm is at least one. Hence **every** such compressed
palette has inverse factor at least sqrt(N/(c-1)), even if the palette changes
with N. This closes compression that preserves an arbitrary supplied palette.
It does not obstruct graph-adapted recoloring; the graph is a forest and has
a known stable three-query design.

**Local aggregate repair obstruction.** A valid local-frame lemma says that
if every closed-neighborhood subpalette has smallest singular value >=eta>0,
locally unmixing the aggregates followed by star reads has error at most
sqrt(2)/eta. But a 41-vertex outerplanar graph from [R1, Theorem6.3] has, under
every star coloring even with unlimited total palette, a closed neighborhood
with at least six colors. Its full proof and explicit width-two decomposition
are in `notes/tw2_local_design.md`. Thus a five-query algorithm that insists
on independently recovering every color aggregate in each row cannot cover
all treewidth-two supports. This is not a general dense five-query lower bound.

Dense color-seed compression, local interpolation and sensitivity analysis
already occur in [R3]. The unsuccessful proposal was about extending them to
global symmetric recovery despite locally underdetermined rows. It failed on
that actual obligation, not through a failure to recognize the old mechanism.

## 8. Original operator, numerical error, and cost boundary

The new fixture operators are explicitly defined supported matrices. They do
not replace or recertify the original NIST exact-decimal problem. The original
dense incumbent, completion interval, sparse identification certificate and
fixed-X9 sensitivity witness are preserved in the unchanged owner source ZIP.
The completed molecular and other retired operations remain closed.

The positive seed contains only zeros and ones and is exactly representable.
With exact arithmetic, the theorem accounts for all action error E. If a
floating implementation rounds the averages inside S, a separately bounded
symmetric decoding perturbation F must be added: operator error is at most
`sqrt(5/3)||E||_F + ||F||_2` (or the s=0 constant). For per-edge rounding radii
rho_e on the averaged entries, `||F||_2<=sqrt(2 sum_e rho_e^2)` suffices.
Copies introduce no arithmetic error beyond the stored input representation.

If the actions instead come from a supported D+Delta with `||Delta||_2<=tau`,
the error to D is bounded by `tau+C||E||_F` plus decoding rounding. If Delta is
not supported on G, it cannot be absorbed in this way: use
`C(||Delta X||_F+||E||_F)`, and the crude norm-only allowance is
`C(tau sqrt(n)+||E||_F)`. Approximate support requires its own accounting.

Costs include constructing and validating the supplied separator forest,
materializing or encoding X, **s+3 actual operator actions**, reading the action
data, sparse recovery, input conversion/error certification, and any later
spectral calculation. No eigensolver or spectral-CDF speedup is delivered here.
See `COSTS.md` for actual exact-fixture, verification, research and delivery
receipts. Small witness timings are not a comparison to the 1074-dimensional
stored-input diagonalization.

## 9. Status, consequence, and remaining question

The accepted incoming squared-path and fan proofs close the former uniform
three-query treewidth-two question. This result settles the sharp uniform
query budget for a different but structurally meaningful parameter: a supplied
forest separator. It shows exactly how a fixed number of globally coupled
coordinates changes the stable query budget. The cancellation method can also
transport any sufficiently large low-energy witness space through a fixed
separator, provided the required fill is allowed; it is not automatically valid
on an arbitrary sparse separator interface.

The general treewidth-two four/five/six question remains unresolved. In
particular, a general width-two graph need not have a bounded forest separator.
The next chosen question is whether local separator interfaces in a tree
decomposition can be composed with bounded error without globally assigning
one unique query coordinate per separator vertex. A positive result must give
a global inverse, not just nonsingular local triples; a negative result must
permit arbitrary graph-adapted dense rows. Both failed color-compression routes
are excluded as default repairs. No additional experiment or precision sweep
is implied by this continuation seed.

## Primary references and provenance

[R1] M. O. Albertson, G. G. Chappell, H. A. Kierstead, A. Kündgen, R. Ramamurthi,
*Coloring with no 2-colored P4's*, EJC11 (2004), R26, Theorems6.1,6.3.
https://doi.org/10.37236/1779
https://www.combinatorics.org/ojs/index.php/eljc/article/viewFile/v11i1r26/pdf/

[R2] A. H. Gebremedhin, A. Tarafdar, A. Pothen, A. Walther,
*Efficient Computation of Sparse Hessians Using Coloring and Automatic
Differentiation*, INFORMS J. Computing21(2) (2009),209-223.
https://doi.org/10.1287/ijoc.1080.0286
https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf

[R3] A. Griewank, N. Strogies, *Efficient Evaluation of Sparse Jacobians by
Matrix Compression, Part I: Motivation and Theory* (2014),33-40.
https://wseas.us/e-library/conferences/2014/Gdansk/MATH/MATH-01.pdf

[R4] D. Halikias, A. Townsend, *Structured matrix recovery from matrix-vector
products*, NLAA31(1) (2024),e2531, section2.1.3.
https://arxiv.org/pdf/2212.09841

[R5] C. Musco, I. Ramesh, *Nearly Instance Optimal Sparse Matrix Approximation
from Matrix-Vector Products*, ESA2026, LIPIcs388,85:1-14.
https://arxiv.org/pdf/2606.12179
https://doi.org/10.4230/LIPIcs.ESA.2026.85

The literature note records exact versus noisy-action differences, failed
retrievals and the bounded scope of the search. Separator probing itself is
also established in J. Xia, *Matrix-Free Sparse Direct Solvers* (2013):
https://gmig.science.purdue.edu/pdfs/2013/11Xia2013.pdf

The immediate lower-bound predecessor is the incoming fan proof preserved
under `incoming/tw2/arm_b/RESULT.txt`; the independent squared-path proof is
`incoming/tw2/arm_a/RESULT.txt`. Their source archive identity and the unchanged
previous owner archive are recorded in `SOURCE_IDENTITIES.json`.
