# Acquired cubic blocks plus phase counting: a raw dense-input theorem

Continuation of Astra P3, 27 October 2026.

This theorem combines a polynomial-time structure compiler with the
previously constructed phase-product counter. It removes the forest
restriction of the preliminary block compiler. The raw input is a cubic
Boolean coefficient list, which may contain Theta(n^3) monomials; no
coordinate change, block decomposition, or contraction order is supplied.

The centroid machinery is established multilinear-form theory. The new
conditional algorithmic consequence here is obtained by feeding its
acquired representation to the phase-product theorem. Neither a new
centroid theorem nor a practical acceleration is claimed.

## 1. Precise result and charged parameters

Let p:F2^n -> F2 be given by its explicit algebraic normal form of degree
at most three, with bit description length L. The task is to compute

    Z(p)=sum_(x in F2^n) (-1)^p(x),
    N0(p)=(2^n+Z(p))/2.

The compiler below either proves Z(p)=0 or produces, in polynomial
time and space:

* an integer e>=0 and a cubic core c on d<=n variables with
  Z(p)=2^e Z(c);
* an invertible F2-linear change of the d core coordinates;
* primitive cubic block dimensions B_1,...,B_t, summing to d;
* a graph G on these blocks, with a pair present precisely when the
  transformed polynomial has nonzero cross-block quadratic coupling;
* an explicit transformed polynomial c' and its actual number M of
  nonconstant monomials.

For d>0 define the certified weight

    W=d+sum_i B_i^3+sum_({i,j} in E(G)) B_i B_j.

The compiler certifies

    M <= sum_i [B_i+binom(B_i,2)+binom(B_i,3)]
           +sum_({i,j} in E(G)) B_i B_j <= W.

**Conditional theorem.** Assuming the governing ETH manuscript and the
proved local phase-product extension, the original exact count is
computable in poly(L+n)2^o(n) bit time and polynomial space whenever

    log(2+M/n)=o(log n).

The sufficient certificate log(2+W/n)=o(log n) may be used instead.
There is no acyclicity, planarity, treewidth, separator, or supplied
decomposition assumption on G. In particular, the sufficient conditions

    max_i B_i=n^o(1),       |E(G)|=n exp(o(log n))

imply W=n exp(o(log n)) and hence subexponential exact counting in the
ORIGINAL n inputs. The blocks may grow; no fixed block size is needed.
The phase engine itself always receives monomial factors of locality
at most three.

With lambda=ceil(log2 n), a suitable explicit parameter is

    h=ceil(log2(2+3M/n))+O(log log n),       a=h/lambda.

In the small-a regime the charged counting bound is

    poly(L+n) * 2^[O(n sqrt(a) [log2(2/a)]^(3/2))],

with absolute constants for binary phases and fixed locality three.
The polynomial-time compiler is added to this cost, not treated as
free preprocessing. The guarded phase algorithm handles the other
parameter ranges by its stated fallback. Independently, exhaustive
counting on the acquired d-bit core gives poly(L+n)2^d time and
polynomial space; this is already subexponential if d=o(n).

These are input-sensitive guarantees with a computed certificate. They
do not say that every dense cubic has small W. If the compiler finds a
single n-dimensional primitive block and a dense polynomial, the theorem
does not supply a subexponential bound.

## 2. Acquiring and eliminating the third-derivative radical

Form T(u,v,w)=D_uD_vD_w p(0), the alternating trilinear form encoded by
the cubic coefficients. Its radical is the kernel of the explicit
binom(n,2)-by-n matrix whose (i,j),k entry is the coefficient of x_i x_j x_k.
Gaussian elimination finds a radical basis R and a complement U.

In coordinates (u,z) with z in R, no cubic monomial contains z. The
remaining z-dependence is quadratic. Eliminate a quadratic pair by

    sum_(s,t) (-1)^[s t+s A+t B+C] = 2 (-1)^[C+A B],

where A,B are affine in the other variables. The new polynomial remains
cubic only in u. Once no z-z terms remain, each remaining z_i enforces
one affine equation A_i(u)=0 and contributes a factor two. Solve those
equations and explicitly substitute their affine parametrization into
the core. Contradictions certify Z(p)=0.

Repeat if the resulting cubic core has a new radical. Each nontrivial
round reduces its variable count. The result is either a constant core
or a core with zero trilinear radical. Its precise identity is

    Z(p)=2^e Z(c),       e+d<=n.

Each equality, affine substitution and power-of-two factor is retained.
No probabilistic rank guess or assumed low-dimensional description is
used. Canonical cubic coefficient expansion costs polynomial time:
each substituted monomial is a product of at most three affine forms.

## 3. Complete centroid extraction over F2

Assume now that c has d variables and its trilinear form T has zero
radical. Compute the vector space

    C={A in Mat_d(F2):
       T(Ax,y,z)=T(x,Ay,z)=T(x,y,Az) for all x,y,z}.

Its d^2 unknown matrix entries satisfy 2d^3 explicit homogeneous linear
equations, obtained by taking x,y,z to be basis vectors. This defines
all of C, not a selected subalgebra.

For A,B in C,

    T(ABx,y,z)=T(Bx,Ay,z)=T(x,Ay,Bz)
             =T(Ax,y,Bz)=T(BAx,y,z).

Zero radical implies AB=BA. Transfers between slots then show that C
is closed under multiplication; it is a commutative F2-algebra with I.
Consequently, for a computed basis A_1,...,A_s,

    (sum_i a_i A_i)^2+sum_i a_i A_i
       =sum_i a_i(A_i^2+A_i),        a_i in F2.

Thus **all F2-rational idempotents** are obtained by one further linear
system in the a_i. No algebraic extension, factorization oracle,
assumed semisimplicity, or enumeration of 2^s elements is required.
Nilpotent elements of C do not invalidate this computation.

Start with the single projector I. For every basis idempotent E, replace
each current P by its nonzero pieces PE and P(I+E). All these matrices
commute and are idempotent. A split yields disjoint nonzero images, so
at most d pieces survive. After all basis idempotents have been used,
each piece is primitive: any further centroid idempotent is a linear
combination of the processed basis, hence acts as either zero or the
identity on that piece. It cannot split it again.

For a centroid idempotent E,

    T(Ex,(I+E)y,z)=T(x,E(I+E)y,z)=0.

Its image and kernel are therefore cubic direct-sum blocks. Conversely,
the projection onto any cubic direct-sum block satisfies the centroid
equations. This proves completeness: the acquired primitive images are
the finest direct-sum blocks over F2, unique up to their order. Choosing
bases in those images yields the required invertible coordinate matrix.

The algorithm uses only polynomial-size binary matrices. For example,
naive elimination of 2d^3 equations in d^2 unknowns costs O(d^7) bit
operations and polynomial space. The remaining matrix products, image
bases, and cubic substitutions also have universal polynomial costs.

## 4. Why the coupling certificate is basis-independent

In acquired block coordinates, every cubic monomial lies within one
primitive block. A monomial crossing blocks can therefore only be
quadratic. For i!=j write that coupling as

    u_i^T Q_ij u_j.

A different choice of bases in the same primitive blocks replaces it
by v_i^T A_i^T Q_ij A_j v_j with A_i,A_j invertible. It is nonzero if
and only if Q_ij is nonzero. Changes in the cubic block polynomial
under Boolean linear substitution can create lower-degree terms, but
only within that same block. Affine translations have the same property;
translations of cross-block quadratics add only affine terms.

Hence for a radical-free input the primitive block dimensions and the
zero/nonzero coupling graph are intrinsic up to block permutation and
are preserved by arbitrary affine changes of the original coordinates.
The actual monomial count within blocks or in a coupling matrix may
depend on the chosen bases, but the upper bound W does not.

After radical elimination, the theorem uses the certificate produced
for the resulting core. It makes no unnecessary claim that every
possible elimination strategy produces the same core polynomial.

## 5. Fixed-arity phase compilation and exact reconstruction

Write the explicit transformed Boolean polynomial as

    c'(y)=c0 + XOR_(S in M) product_(i in S) y_i,
           1<=|S|<=3.

Its phase is (-1)^c0 times M monomial phase factors. For the phase
engine, use

    product_(S in M) (1-2V product_(i in S) Y_i)
       in Q[V]/(V^(n+2)),

padding with n-d unused Boolean variables if necessary. Their only
effect is a known multiplicity. The engine's retained total incidence
degree is at most 3(n+1), independent of M; it manufactures the
replacement forms and shared summaries from these actual scopes.

Let Z_pad denote the signed padded phase sum, including (-1)^c0.
Then

    Z_pad=2^(n-d) Z(c'),
    Z(p)=2^e [Z_pad/2^(n-d)].

Precision n+2 uniquely reconstructs Z_pad in [-2^n,2^n]. Perform the
known exact division AFTER reconstruction, then multiply by 2^e.
No precision is discarded before a multiplicity is removed. All
integers have O(n) bits, and e+d<=n guarantees the final magnitude
bound. Finally return (2^n+Z(p))/2 for the original zero count.

The compiler's raw cost, the phase description, high-incidence
branching, factor evaluation, rational reconstruction and final
arithmetic are all charged. The engine sees degree-three local factors
even when the acquired blocks grow. This is why the weighted W
criterion is stronger than a fixed-size block condition.

## 6. What this adds beyond the earlier representation

The original phase-product theorem applies directly to an explicitly
given n exp(o(log n))-factor local phase program. A raw cubic ANF after
an unknown dense linear change can instead contain Theta(n^3) terms.
Applying the earlier counter to that list gives no subexponential
guarantee. The present algorithm first acquires a new input basis and
proves a much smaller local phase description from the raw coefficients.

Its success does not rely on an easy graph decomposition. For example,
an arbitrary affine disguise of bounded-size cubic blocks connected
by any bounded-degree quadratic interaction graph has W=O(n), whether
that graph is a tree, cyclic, or has large separators. The centroid
stage discovers the blocks; the phase theorem handles the unrestricted
interaction graph. More generally subpolynomial block dimensions and
n exp(o(log n)) block-pair couplings remain in range.

The result is restricted. Scalar-centroid dense cubics typically leave
one full-size block, and arbitrary dense coupling among many blocks can
make W quadratic. The theorem removes the previously assumed block
basis and the forest condition; it does not remove all algebraic or
density restrictions from generic cubic counting.

## 7. Executed non-forest fixtures

The executable `acquired_block_phase_checks.py` compiles four raw dense
polynomials with hidden coordinate changes. It tests a four-cycle,
a four-clique, K3,3, and two six-dimensional primitive blocks whose
centroids are not assumed semisimple.

| Hidden coupling | n | Raw cubic terms | Acquired block sizes | Actual local monomial phases | W | Exact Z |
|---|---:|---:|---|---:|---:|---:|
| Four-cycle | 12 | 114 | 3,3,3,3 | 27 | 156 | 112 |
| Four-clique | 12 | 112 | 3,3,3,3 | 37 | 174 | 112 |
| K3,3 | 18 | 421 | 3,3,3,3,3,3 | 60 | 261 | 832 |
| Two primitive six-dimensional blocks | 12 | 112 | 6,6 | 44 | 480 | 256 |

The K3,3 fixture's exact edge expansion is 5/3, computed by enumerating
all vertex subsets of size at most half the graph. This is a finite
expanding-graph check, not an asymptotic expander-construction claim.
The acquired block images were mapped back to the hidden blocks and
their coupling edges checked exactly.

All three n=12 fixtures were checked pointwise on every assignment.
The n=18 fixture had 4,096 fixed-seed pointwise checks. In addition,
every fixture's phase sum was computed exhaustively, independently
for the raw dense ANF, the original hidden expression, and the acquired
phase polynomial; all agreed. There were 16,384 pointwise checks in
total. Exact binary truth vectors were used for the exhaustive count
checks. The asymptotic replacement counter was NOT executed, and no
practical speed comparison is asserted.

## Sources and dependencies

* Governing source: OpenAI, *The Exponential Time Hypothesis is False*,
  pinned revision 25 October 2026, Definition 3.1, Proposition 3.4,
  Lemma 4.7 and Appendix B:
  https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf
* The local phase-product extension, including precision and uniform
  incidence bounds, is proved in `work_dense_agent/PHASE_PRODUCT_CONSTRUCTION.md`
  and the saved Astra P3 proof report. It is a prerequisite here.
* Hua-Lin Huang, Huajun Lu, Yu Ye and Chi Zhang, *Centers of Multilinear
  Forms and Applications*: https://arxiv.org/abs/2110.07915
* The same authors, *On Centers and Direct Sum Decompositions of Higher
  Degree Forms*: https://arxiv.org/abs/2009.12014

The centroid/primitive-idempotent correspondence is prior machinery.
The full F2 construction above is included to make the algorithm and
its exact admissibility certificate independently inspectable.
