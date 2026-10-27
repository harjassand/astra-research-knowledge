# Dense cubic phases: manufactured structure and the affine-compression limit

Continuation research, 27 October 2026. The goal is to extend the exact
phase-product theorem beyond m=n exp(o(log n)). This note records a
completed structural attack, its executable representation compiler,
and the precise point at which it fails on the general dense family.
No generic subexponential dense-cubic algorithm is claimed.

## 1. A polynomial-time compiler for the third-derivative structure

Let p:F2^n -> F2 have algebraic normal form of degree at most three.
The input is its explicit coefficient list, of length L. Define

    T(u,v,w)=D_u D_v D_w p(0).

T is an alternating trilinear form. It depends only on the cubic part.
For i<j, the row indexed by (i,j) has entry c_(i,j,k) in column k.
The kernel of this binom(n,2)-by-n matrix is the radical

    R={v:T(v,u,w)=0 for all u,w}.

This is manufactured by Gaussian elimination, not supplied.

Choose a complement U and a basis x=(u,z) with z in R. Every cubic term
involving z vanishes in these coordinates: its polarization would give
a nonzero value with a radical argument. Thus

    p(u,z)=c(u)+q(u,z),       deg c<=3, deg q<=2.

The Boolean polynomial after this invertible substitution is obtained
explicitly by expanding products of at most three linear forms and
reducing x_i^2=x_i. Its cost is polynomial in L+n; a conservative bound
for one substitution is O(L n^3 log n) bit operations.

### Symbolic Gaussian elimination of every radical direction

If a z_i z_j term is present, write

    p=z_i z_j+z_i A+z_j B+C,

where A and B are affine in the remaining variables. The exact identity

    sum_(z_i,z_j) (-1)^p = 2 (-1)^(C+A B)

eliminates two radical variables and multiplies the sum by two. The new
polynomial remains cubic only in u and at most quadratic in the other
variables. Repeat until no pair of remaining z variables interacts.
Every remaining z_i then appears as z_i A_i(u), where A_i is affine.
Summing z_i produces a factor two and imposes A_i(u)=0. Solve these
affine equations exactly, substitute their affine parametrization into
the cubic core, and retain the known power of two.

The result is either a proved zero sum or

    Z(p)=2^e Z(p_core),

with a cubic p_core on at most rank(T) variables. All factors, pins,
linear constraints, affine offsets and coefficient changes are charged.
If a new radical appears after solving constraints, repeat; each such
round decreases the number of variables. There is no existential
compression assumption.

This recovers hidden low essential dimension, but does not solve dense
generic inputs: their third-derivative radical can be zero. The next
step repairs a second class which has zero radical.

## 2. Extracting unknown cubic blocks by centroid algebra

Assume the current T has zero radical. Define its centroid

    C={A in End(F2^n):
       T(Ax,y,z)=T(x,Ay,z)=T(x,y,Az) for all x,y,z}.

The entries of A are n^2 unknown bits. The displayed identities give
2n^3 homogeneous linear equations, so a basis of C is computable by
ordinary Gaussian elimination. This center/centroid method has prior
ancestry in the multilinear-form literature [1,2]; it is used here as
actual compiler machinery, not presented as a new abstract theorem.

### Why the algebra and its idempotents are constructive

For A,B in C,

    T(ABx,y,z)=T(Bx,Ay,z)=T(x,Ay,Bz)
             =T(Ax,y,Bz)=T(BAx,y,z).

The zero radical implies AB=BA. It follows that C is a commutative
associative algebra containing I. In characteristic two,

    (sum_i a_i A_i)^2=sum_i a_i A_i^2,      a_i in F2.

Therefore the idempotent equation E^2=E is LINEAR in the coefficients
of a computed centroid basis. Solve the corresponding linear system.
Starting with I, split each current projection P by an idempotent E
into PE and P(I+E), discarding zero pieces. All projections commute,
remain idempotent, and have orthogonal images. After all basis
idempotents are processed, their nonzero pieces are primitive. There
are at most n pieces.

If E is a centroid idempotent, then

    T(Ex,(I+E)y,z)=T(x,E(I+E)y,z)=0.

Thus its image and kernel are direct-sum blocks of T. Conversely any
direct-sum block projection satisfies the centroid identities. The
primitive projections therefore manufacture the finest cubic direct
sum decomposition. No block basis or decomposition oracle is assumed.

A conservative total bound for the linear-algebra and polynomial
substitution part is n^O(1)+poly(L), with O(n^7) elementary bit work
sufficient for the displayed centroid equations in a naive dense
implementation; storage is polynomial. The executable uses integer
bitsets for F2 rows and matrices.

## 3. The remaining quadratic interaction graph

In the resulting block coordinates the cubic monomials lie within
individual blocks. Lower-degree terms may still couple different
blocks. Put an edge between two blocks when a quadratic monomial
uses one variable from each. Linear terms and within-block quadratic
terms stay local; constants contribute a known sign.

If this discovered graph is a forest, exact tree messages evaluate
the full phase sum. For block sizes B_i and edge bilinear phases q_ij,

    M_(i->j)(x_j)=sum_(x_i)
       (-1)^[p_i(x_i)+q_ij(x_i,x_j)]
       product_(a in children(i)) M_(a->i)(x_i).

This costs poly(L+n) plus

    poly(n) * sum_(edges i,j) 2^(B_i+B_j)

bit operations, including exact integer arithmetic. Storing messages
costs poly(L+n)+poly(n)2^B bits for B=max B_i. In particular, for
B=O(log n) this is polynomial time and polynomial space. The forest
test and all tables are constructed from the original polynomial.
For larger blocks the space cost is stated explicitly; it is not
silently called polynomial.

A concrete raw family covered in polynomial time consists of arbitrary
invertible affine changes of

    sum_i u_(i,1)u_(i,2)u_(i,3)
      + sum_(forest edges i,j) q_ij(u_i,u_j)
      + sum_i q_i(u_i),

where each block u_i has three bits and the q terms are quadratic.
The hidden affine transformation, block partition, and forest are
not provided. These polynomials may have Theta(n^3) canonical cubic
monomials, yet the compiler recovers the three-bit primitive blocks
and their quadratic interaction graph. This is a real constructed
representation, although its center-algebra and tree-summation
ingredients are established machinery rather than a claimed new
complexity breakthrough.

### Why arbitrary quadratic coupling is substantive

A primitive cubic block is intrinsic up to changes of basis within
blocks and permutation. Any full affine direct-sum decomposition
would induce a centroid idempotent for T, hence would partition the
primitive cubic blocks. A nonzero cross-block quadratic bilinear form
cannot be eliminated by invertible changes within those blocks;
translations of cubic block coordinates affect only within-block
quadratic terms. Thus a connected quadratic coupling graph prevents
further full-polynomial direct-sum splitting. Its being a forest can
still enable messages, but a dense graph need not do so.

The uncompleted frontier is therefore concrete: evaluate these
quadratically coupled nonlinear block factors without assuming the
coupling graph has an easy contraction. A Gaussian-moment oracle
for the quadratic part alone does not establish that ability.

## 4. Why one small affine-phase representation cannot cover dense cubics

Fix k,b. Consider a proposed exact representation of a binary cubic
phase as a product of at most m fixed-2^b-order phase gates. Each gate
reads at most k arbitrary affine forms in the original n bits and
has an arbitrary truth table on those k bits. Permit an arbitrary
quadratic correction for free. This includes any one global
invertible affine change of variables, since every affine gate input
is already arbitrary.

One gate has at most

    A=k(n+1)+b*2^k

bits of choices. Consequently at most 2^(mA) cubic coefficient vectors
can be represented. There are 2^binom(n,3) possible cubic parts.
Free quadratic corrections do not change that vector. Thus the
fraction representable by m such gates is at most

    min(1, 2^[m A-binom(n,3)]).

In particular, covering every cubic requires

    m >= binom(n,3)/(k(n+1)+b*2^k)=Omega_(k,b)(n^2).

For m=n^(1+o(1)), the representable fraction tends to zero as
2^[-Theta(n^3)]. This is a failure of the proposed SINGLE compressed
affine-phase representation. It is not a lower bound against exact
counting, general arithmetic circuits, signed sums of many easier
representations, or the source's interpolation families. Adding
nonlinear intermediate gates changes the representation class and
is not covered by this counting argument.

## 5. A small exact counterexample, with an invariant proof

The six-variable cubic

    p=x1*x2*x6+x1*x3*x5+x2*x3*x4

cannot be expressed, even modulo an arbitrary quadratic polynomial,
as a sum of two products of three affine forms. Its alternating rank
is exactly three.

The cubic part of a product of three affine forms is the exterior
product of their linear coefficient vectors. If a sum of two such
products has a zero radical on six variables, the two three-dimensional
coefficient spaces must span all six dimensions and be disjoint.
After an invertible change of basis the cubic tensor is then the
direct sum of two three-dimensional volume forms. Among its 63 nonzero
directional contractions, 14 have alternating-matrix rank two and
49 have rank four.

For p, write the first three coordinates as u and the last three as
v, reversing their order to match the displayed expression. For a
direction (a,b), a=0 and b!=0 gives contraction rank two: there are
7 such directions. If a!=0, the off-diagonal three-by-three cross
matrix has rank two, giving contraction rank at least four. The
direction itself is in the contraction radical, so an alternating
six-by-six matrix can have rank at most four. Thus the remaining
56 directions have rank four. No nonzero direction has zero
contraction, so the full trilinear radical is zero. The rank
distribution differs from that of two disjoint volume forms and is
invariant under invertible coordinate change. Two products are
therefore impossible; the displayed three products attain rank three.

The exhaustive certificate independently enumerated all 1,395 nonzero
decomposable cubic tensors in six variables. Their sums of at most two
cover exactly 413,200 of the 1,048,576 cubic parts. The first missing
binary coefficient vector is the polynomial above. These are exact
F2 computations, not numerical tensor-rank estimates.

## 6. Executed evidence and limitations

`cubic_structure_compiler.py` passed 37 fixtures: 28 random cubics,
six hidden independent-block or hidden-chain polynomials, and three
hidden cubic cores with quadratic directions. The hidden fixtures
were checked both against their original block forms and by direct
enumeration of their transformed dense ANFs. At n=12, 100 and 105
cubic monomials were transformed back into four three-bit blocks;
the hidden chain's exact phase sum was 496. The Gaussian-radical
fixtures on 8,10,12 variables reduced to a three-variable core with
the required exact power-of-two multiplicities.

This does not turn a typical dense cubic into a small core. All
twelve random fixtures on 7,8,9 variables had zero radical and a
scalar centroid. The compiler then retained the full variable set.
This finite evidence illustrates the obstruction; it is not offered
as an asymptotic average-case theorem.

The new branch has therefore produced an executable, source-aware
structure compiler and a decisive obstruction to the obvious affine
compression cure. It has not removed the general dense-incidence
cost in the earlier constructive phase theorem.

## Primary literature checked

1. Hua-Lin Huang, Huajun Lu, Yu Ye and Chi Zhang, *Centers of Multilinear
   Forms and Applications*, arXiv:2110.07915; published in Linear Algebra
   and its Applications. The center-algebra/direct-sum correspondence
   is prior machinery: https://arxiv.org/abs/2110.07915
2. *On Centers and Direct Sum Decompositions of Higher Degree Forms*,
   arXiv:2009.12014: https://arxiv.org/abs/2009.12014
3. Augustine Musukwa, Massimiliano Sala, Irene Villa and Marco Zaninelli,
   *On cryptographic properties of cubic and splitting Boolean functions*,
   published online 2022. Section 3.1 supplies the established recursive
   cubic-to-quadratic counting procedure and its explicit exponential
   branching cost: https://link.springer.com/article/10.1007/s00200-022-00575-2
4. Kirill Khoruzhii, Patrick Gelss and Sebastian Pokutta, *Classification
   of Boolean Cubic Forms in Ten Variables*, 26 June 2026. Its verified
   abstract reports complete cubic/alternating-trilinear classification
   and explicit alternating-rank decompositions. The full paper was
   not retrieved here, so no unverified internal result is used:
   https://arxiv.org/abs/2606.28473

The algebraic proofs above are included so that the executed compiler's
correctness does not depend on extrapolating any inaccessible source.
