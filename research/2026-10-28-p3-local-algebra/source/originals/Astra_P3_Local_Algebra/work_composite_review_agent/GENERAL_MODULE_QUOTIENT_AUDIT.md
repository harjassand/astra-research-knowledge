# General-module quotient acquisition and transverse counting

The proposed acquisition theorem is correct, including the need to solve
for the center only modulo `J^(e-h)`. The proposed weighted transverse
factor is also correct for odd module dimension and a nondegenerate
transverse residue Hessian. A separate geometric obstruction prevents
deducing this counting condition from radical-freeness of the third tensor.

## 1. Acquired data and coefficient fitting

Let `A=F_(2^d)[t]/(t^e)`, `d>=3`, `J=(t)`, and `V=A^b`. Assume the full
centroid and a free module basis have been acquired and verified. Let the
third tensor be represented by the alternating coefficients `C_ijk`, and
freeze the complete squarefree cubic

\[
H_{sf}(X)=\sum_{i<j<k}C_{ijk}X_iX_jX_k.
\]

The difference from the raw Boolean phase is binary quadratic. Fit the
traces of the remaining ordinary monomials to all binary linear and
quadratic coefficients outside the quotient of height `h`. The monomials
are the `b^2` repeated-variable cubics `X_i^2X_j` (including `X_i^3`),
the `binom(b,2)` cross pairs, the `b` linears, and a constant. Ordinary
pure squares can be absorbed into linears under the Frobenius functional.

Put

\[
K=b^2+\binom b2+b=\frac{3b^2+b}{2},\qquad m=de,\qquad n=bm.
\]

There are `(K+1)m` binary coefficient columns and at most `n(n+1)/2`
protected rows. Each model is exactly binary quadratic. The ordinary
squarefree cubic was frozen, so no untested binary cubic ambiguity enters
this linear fit.

The coefficient-invisibility lemma from `WEIGHTED_QUOTIENT_AUDIT.md`
extends verbatim to every `b`: if the trace of such a polynomial is
supported on the height-`h` quotient, every nonconstant ordinary coefficient
belongs to `J^(e-h)`. Simultaneous scaling of the input and a high variation
separates trace exponent three from exponents one and two. Variations in
odd-exponent coordinates isolate the cubic coefficients; nondegeneracy of
the Frobenius pairing then isolates cross and linear coefficients.

Thus the complete coefficient kernel is

\[
A\;\oplus\;(J^{e-h})^K,
\]

with binary dimension `de+Kdh`. The protected matrix has exact rank
`Kd(e-h)`. This holds for **all** heights `0<=h<=e` and requires no counting
height restriction.

All matrix dimensions are explicit and polynomial. A direct binary solve
uses at most `O(n^2 (bn)^2)=O(b^2 n^4)` bit operations and `O(b n^3)`
bits of matrix storage, in addition to polynomial model construction and
the already separate centroid acquisition. These are conservative dense
bounds; bit packing reduces practical work. The ordinary cubic output has
`binom(b,3)+b^2` ring coefficients, hence `O(b^3 de)` bits.

## 2. Center acquisition at the necessary precision

Translation of repeated-variable cubics creates pure squares and linears,
but no ordinary cross pairs. Therefore the cross coefficients of a
translated homogeneous cubic satisfy

\[
B_{ij}=\sum_k C_{ijk}a_k.
\]

Let `L_C:A^b -> A^binom(b,2)` be this contraction map. Radical-freeness of
the residue third tensor says exactly that its residue matrix has column
rank `b`. A `b`-row minor has unit determinant. Consequently the map is
injective, has a left inverse over `A`, and remains injective over every
truncated ring `A/J^s`.

For a height-`h` fit, set `s=e-h`. Solve

\[
L_C a=B\pmod{J^s}.
\]

The solution modulo `J^s` is unique when it exists. Verify **every** cross
pair equation at this precision, not only the selected invertible minor.
Then take any lift to `A^b`, for example by setting the remaining digits
to zero. At `s=0`, the quotient is zero and the center may simply be chosen
zero; do not instantiate a positive-length chain-ring routine at length
zero.

A digit-lifted linear solve or an explicit binary solve gives polynomial
cost. The latter has `bds` unknown bits, `binom(b,2)ds` equation bits, and
rank `bds`.

It would be incorrect to require the fitted full-precision vector `B` to
lie in the image of `L_C`. For `b>3`, that image need not be the entire
cross-coefficient space, while the fit leaves arbitrary coefficients in
`J^s` unconstrained. An executed five-coordinate example has no full-
precision center but has the required unique center modulo `J^s`.

## 3. Completeness and minimum height

Suppose the raw phase has a promised representation

\[
p(X)=\lambda(H_*(X+a_*))+Q_*(X\bmod J^h).
\]

Expand its ordinary translated polynomial, absorbing pure-square trace
terms into linears. Compare it with any solution of the protected linear
fit. The coefficient lemma gives

\[
H-H_*\in J^s[X]_3,\qquad B-L_Ca_*\in(J^s)^{\binom b2}.
\]

The modular center solve is therefore consistent and returns
`a=a_* mod J^s`. Replacing the homogeneous polynomial or its translation
by these fitted values changes the scalar function only on the height-`h`
quotient. Every new nonconstant term in a translation difference contains
a factor from `a-a_* in J^s`; its square or cube need not vanish, but it
still lies in the same ideal. The exact final discrepancy is binary
quadratic and has the required quotient support.

Conversely, the final identity and support checks certify any accepted
representation. Hence fitting plus the modular center solve and final
support check is complete for every height. Existence is monotone in `h`,
and `h=e` always works with the canonical squarefree cubic and the entire
quadratic remainder. Binary search therefore acquires the minimum height
without assuming a useful decomposition. Semilinear ring-coordinate
changes preserve this minimum for the same reasons as in the ternary
proof: they preserve `J^h`, homogeneous degree, and the Frobenius functional
up to a unit.

## 4. Weighted transverse factor for odd b

Let `b` be odd and `m_t=b-1` be the transverse dimension. At an acquired
projective singular residue point, require its transverse Hessian to be
invertible over the residue field. The critical point lifts uniquely by
Hensel corrections. After translating to that exact lift, the chart phase
is

\[
c+q_2(u)+C_3(u),\qquad u\in(tA_e)^{m_t},
\]

where the polar form of `q_2` is nonsingular. Cubic squarefree terms are now
allowed in `C_3`; the initial transverse phase need not be binary quadratic.

The same exact digit elimination applies. After writing `u=tU`, the
residual cubic has a factor `t`. Highest-digit orthogonality forces all
residue coordinates of `U` to zero, reducing depth by two and contributing
`q^m_t`. The field terminal is a nonsingular even-dimensional quadratic
Gaussian sum

\[
\kappa q^{m_t/2},\qquad\kappa\in\{-1,1\}.
\]

Its sign is unchanged by multiplying the quadratic form by a nonzero
field scalar. To verify this, put its polar form into symplectic pairs;
the sign is the trace of the sum of pairwise Arf ratios, each unchanged
when both diagonal coefficients and the polar coefficient are scaled.
In particular the radial factor `r^3` does not change `kappa`.

For a quotient weight of height `h<=floor(e/2)`, the high-digit operations
do not see the weight and force `u=0 mod J^h`. Thus the exact transverse
factor is

\[
\boxed{
q^{m_t e/2}\kappa^{e\bmod2}
 (-1)^{\lambda(c r^3)+Q(r v)}.
}
\]

The radial sum remains the difference of two binary Gaussian sums, because
there is still only one ring-valued radial variable. The origin factor is
`q^(2b)` for a depth-three reduction. Its small-depth values are `q^b` at
depth two and `q^(2b)` at depth three. The polynomial quotient-height
schedule and the adaptive residual-depth calculation are unchanged, with
`3d` replaced by `bd` in the number of residual binary variables.

## 5. Decisive geometric obstruction to a generic higher-b counter

Radical-freeness of the third tensor does **not** imply a finite collection
of nondegenerate critical rays. Consider

\[
H=X_1(X_2X_3+X_4X_5).
\]

Its third-form contraction map has rank five. The full scalar centroid is
the base ring, as also verified by raw acquisition in the executed test.
For the algebraic check, write the form as `e1 wedge omega` on
`A e1 direct-sum W`, where `omega` is nonsingular alternating on `A^4`.
The radical-free centroid commutes with the known scalar multiplications,
so its elements are `A`-linear. Repeated `e1` arguments kill the block
from `e1` into `W`; an `e1` argument and two `W` arguments force the `W`
block to be the same scalar. Three `W` arguments, choosing the other
symplectic pair, kill the remaining block into `e1`. Only scalar
multiplications remain.
Nevertheless its projective singular locus contains

\[
X_1=0,\qquad X_2X_3+X_4X_5=0,
\]

a positive-dimensional quadric. There is also the isolated vertex
`[1:0:0:0:0]`. Over `F_q` there are `(q+1)^2+1` singular points: the vertex
has transverse Hessian rank four, while the other `(q+1)^2` points have
rank two. Over `F_8`, the program found all **82** points, including **81**
degenerate ones, while acquiring a six-dimensional centroid and a free
rank-five module over `F_8[t]/t^2`.

Furthermore, dehomogenized gradients in more than two transverse variables
contain mixed quadratic terms. The ternary affine-`F_2` gradient solver
cannot be reused unchanged. The higher-dimensional counting theorem must
include a separate constructive critical-locus acquisition and its cost,
and must reject or separately handle degenerate/positive-dimensional
critical loci. The local Gaussian formula is correct under the stated
nondegeneracy condition; it does not remove this global obstruction.
If `b` varies, neither the number of rays nor the generic finite-field
terminal cost is automatically polynomial in the original input length.
The cited fixed-variable point-counting closure applies for fixed `b`;
dependence on `b` must remain explicit in a varying-dimension theorem.

## 6. Executed checks

`general_module_audit.py` and `general_module_audit_results.json` preserve:

- complete coefficient-kernel checks for `b=5,d=3,e=2` at heights zero,
  one, and two, with ranks `240`, `120`, and `0`;
- a center-precision example where a full-ring solve rejects but the
  required quotient-ring solve succeeds uniquely;
- the raw-centroid and exhaustive projective verification of the
  positive-dimensional critical-locus obstruction above;
- twelve weighted four-transverse-variable truth tables, including
  squarefree transverse cubic terms and maximal allowed quotient weights.

Every exact assertion passed. No root file was modified.
