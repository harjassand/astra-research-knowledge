# Why arbitrary parity-constrained leaves are not a free exponent improvement

This note proves two precise limitations of the proposed shortcut from
`2^r` Walsh leaves for a rank-`r` quadratic defect to `2^(r/2)` conditioned
leaves. It does **not** prove that `2^r` time is necessary, or that a stronger
joint algorithm is impossible. It identifies the new problem that conditioning
would have to solve and proves optimality only inside a stated shift-only
representation model.

## 1. Every cubic Boolean polynomial occurs on a linear section of one field product

Let `p:F_2^m -> F_2` have Boolean ANF degree at most three and constant term
zero. Choose `d>=m^2`, a degree-`d` irreducible polynomial over `F_2`, and let
`F=F_(2^d)=F_2[alpha]`. Define

\[
 a_i=\alpha^i,\qquad b_j=\alpha^{mj},\qquad 0\le i,j<m.
\]

All `m^2` products `a_i b_j=alpha^(i+mj)` are linearly independent: their
exponents are exactly `0,...,m^2-1`, which are below `d`.

Manufacture a binary tensor `T_ijk` by assigning each nonzero ANF monomial to
one ordered triple. For a unary term `u_i`, use `(i,i,i)`; for a quadratic
term `u_i u_j` with `i<j`, use `(i,i,j)`; for a cubic with distinct sorted
indices use its sorted triple. All other tensor entries are zero. Boolean
idempotence then gives

\[
 p(u)=\sum_{i,j,k}T_{ijk}u_i u_j u_k.
\tag{1}
\]

For each `k`, solve the linear equations

\[
 \operatorname{Tr}_{F/F_2}(a_i b_j c_k)=T_{ijk}\quad(0\le i,j<m).
\tag{2}
\]

The trace pairing on a finite field is nondegenerate. Since the products are
independent, (2) consists of `m^2` independent binary equations in `d`
unknown bits and is solvable. This manufactures the `c_k`; no tensor
factorization or compressible representation is assumed.

Set

\[
 J(u)=\left(\sum_i a_i u_i,\sum_j b_j u_j,\sum_k c_k u_k\right).
\]

Then

\[
 \operatorname{Tr}(XYZ)\big|_{(X,Y,Z)=J(u)}=p(u).
\tag{3}
\]

The embedding `J` is injective because its first coordinate has independent
coefficients `a_i`. Its image is an `m`-dimensional binary linear subspace of
`F^3`, given by a matrix of `3d-m` independent binary parity equations.
Gaussian elimination constructs those equations in polynomial time. Therefore

\[
 \sum_{u\in F_2^m}(-1)^{p(u)}
 =\sum_{(X,Y,Z)\in\ker H}(-1)^{\operatorname{Tr}(XYZ)}.
\tag{4}
\]

A nonzero constant term in `p` changes only the overall known sign. It can
also be represented by an affine shift/extra fixed coordinate when that
format is desired.

### Description and construction costs

Take `d=m^2`. The field modulus has `d+1` bits, the embedding matrix has
`3dm=O(m^3)` bits, and an explicit independent constraint matrix has
`(3d-m)3d=O(m^4)` bits. All trace-pairing solves and basis computations are
polynomial in `m`. Deterministic polynomial-time construction of a prescribed
field degree over fixed characteristic two is established: Victor Shoup,
*New Algorithms for Finding Irreducible Polynomials over Finite Fields*,
Mathematics of Computation 54 (1990), 435–447; author's full paper
https://www.shoup.net/papers/detirred.pdf. Its abstract explicitly states the
deterministic polynomial-time bound for small characteristic. This is the
field-construction dependency of the complexity reduction. The small executed
fixtures use simple trial construction and label that choice; they do not
pretend trial search establishes the worst-case bound.

The constrained instance has `3m^2` ambient Boolean coordinates but only `m`
independent free bits. This distinction is exactly the original-input issue:
solving the ambient unconstrained field product is easy, but an arbitrary
binary restriction can encode any cubic computation on the independent bits.

## 2. Exact cubic phase sums already encode circuit counting

Let a Boolean circuit have `n` independent inputs, `s` internal gate outputs,
and one designated output. Gates AND, XOR, NOT suffice. Introduce one binary
variable for each internal wire, and write its gate equation over `F_2`:

\[
 y+ab=0\ (\text{AND}),\quad y+a+b=0\ (\text{XOR}),\quad
 y+a+1=0\ (\text{NOT}).
\]

Add the equation `output+1=0`. There are `g=s+1` equations `f_j`, each of
Boolean degree at most two. Every assignment of the `n` original inputs has
exactly one assignment of the internal wire variables satisfying all gate
equations. It satisfies the additional output equation precisely when the
circuit accepts.

Introduce `g` fresh binary multiplier variables and form the explicit
zero-constant cubic polynomial

\[
 P(x,y,z)=\sum_{j=1}^g z_j f_j(x,y).
\]

There are `M=n+s+g=n+2s+1` variables. Character orthogonality yields

\[
 \sum_{x,y,z}(-1)^{P(x,y,z)}
 =2^g\#\{x:C(x)=1\}.
\tag{5}
\]

All intermediate witnesses are unique; the factor `2^g` comes solely from
summing the multipliers. Thus exact cubic phase sums are #P-hard under a
polynomial-time metric reduction from #CIRCUIT-SAT. If the supplied oracle
returns zero counts instead of signed sums, use `Z=2N_0-2^M` before dividing
by `2^g`. Combining (4) and (5), exact counting for the fixed-form field
product `Tr(XYZ)` under arbitrary binary linear constraints is #P-hard.
A polynomial-time algorithm for all those constrained leaves would imply
`FP=#P`. No assumption that these classes differ is needed to establish the
reduction.

This does not prevent efficient counting under special compatible constraints,
or with cost exponential in the number of constraints. It rules out treating
arbitrary binary parity constraints as a free feature of the existing
unconstrained ring/field counter.

## 3. Shift-only quadratic reconstruction has exactly 2^r support

Let `Q:F_2^n -> F_2` be quadratic, with alternating polar matrix `B` of rank
`r`. Let

\[
 W_Q(a)=\sum_x(-1)^{Q(x)+a\cdot x}.
\]

Squaring and putting the second argument equal to `x+y` gives

\[
 |W_Q(a)|^2=2^n\sum_{y\in\ker B}
 (-1)^{Q(y)+Q(0)+a\cdot y}.
\tag{6}
\]

On the radical `ker B`, the function `Q(y)+Q(0)` is linear. Therefore (6)
is either zero or `2^(2n-r)`. Parseval gives
`sum_a |W_Q(a)|^2=2^(2n)`, so exactly `2^r` coefficients are nonzero, and
all nonzero normalized Fourier coefficients have magnitude `2^(-r/2)`.

The characters `(-1)^(a dot x)` are a basis. Hence any exact pointwise
identity

\[
 (-1)^{Q(x)}=\sum_{j=1}^M c_j(-1)^{a_j\cdot x}
\tag{7}
\]

with arbitrary real or complex coefficients must use at least `2^r`
distinct shifts. The usual Walsh decomposition attains this bound.

The same conclusion applies to a reconstruction identity that only claims to
preserve counts, provided it uses a **single fixed set of shifts and weights
uniformly over all affine perturbations of a fixed base function**. Suppose
for some fixed Boolean base `b`, all `l in F_2^n` satisfy

\[
 \sum_x(-1)^{b(x)+Q(x)+l\cdot x}
 =\sum_{j=1}^M c_j\sum_x(-1)^{b(x)+(l+a_j)\cdot x}.
\tag{8}
\]

Fourier inversion in `l` gives (7) after division by the nonzero sign
`(-1)^b(x)`. Thus `M>=2^r` even if the base function is a fixed ring product
and every query only changes its linear terms.

This is a representation lower bound for universal shift-only identities.
It is not a counting-time lower bound; it does not apply to instance-adaptive
identities whose coefficients themselves require count information, or to
an algorithm that contracts the whole family jointly by a different method.

## 4. What the 2^(r/2) conditioning proposal still requires

Write `r=2k` and put the quadratic defect into symplectic form
`Q=sum_(i=1)^k ell_i m_i + ell_0`. Conditioning on the `k` values `ell_i=a_i`
leaves `2^k` branches, but branch `a` asks for the base count under `k`
binary parity constraints and an added linear phase `sum a_i m_i+ell_0`.
Expanding those constraints by binary character orthogonality introduces
another `2^k` terms and recovers the original `2^r` construction. A net
improvement must therefore solve those constrained sums more efficiently
using a proved compatibility property or a new joint mechanism. Equations
(4)–(5) show why that work cannot be omitted.

## Executed checks

`parity_constraint_obstruction.py` and its JSON save the full embeddings,
constraint matrices, reconstructed nullspace bases, and exact count results.
The constrained oracle enumerates only the independently recovered `m`-bit
nullspace, rather than reusing the original embedding basis.

The executed suite has 40 cubic embeddings on `m=3,4,5,6` variables, checks
all `1,200` pointwise identities, four complete gate/multiplier reductions,
and 34 quadratic Fourier-support cases up to ten bits. All comparisons agree.

