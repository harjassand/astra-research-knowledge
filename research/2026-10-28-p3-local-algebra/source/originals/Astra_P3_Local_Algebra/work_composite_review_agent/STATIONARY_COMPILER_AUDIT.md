# Stationary chain compiler: independent audit and uniform closure

The actual implementation reviewed was
`work_chain_root/stationary_chain_counter.py`. The common-center readout,
trace-dual derivative extraction, Macaulay certificate, restriction,
manufactured cubic subtraction, and `q^6` multiplier agree with the proof
below. No incorrect multiplicity was found. This audit also supplies an
independent all-coefficient field-terminal fitter.

## 1. The recursive interface and center certificate

Let `F=F_(2^d)`, `q=2^d`, `A_e=F[t]/(t^e)`, and
`lambda_e(a)=Tr_F/F2([t^(e-1)]a)`. At a recursive node the exact phase is

\[
p(X)=\lambda_e(\mu X_1X_2X_3)+Q(X),
\]

where `mu` is a unit and `Q` is an explicit binary quadratic including affine
terms. The initial centroid compiler acquires this representation from the
raw cubic. No quadratic rank assumption is used here.

For `e>=2`, compute all derivatives along the highest digits and check that
they depend only on the three residue coordinates `x`. Trace duality gives
unique functions `g_i:F^3 -> F` with

\[
D_{t^{e-1}\eta e_i}p(X)=\operatorname{Tr}(\eta g_i(x)).
\]

For `d>=2`, fit and verify the complete identities

\[
g_i(x)=\mu_0x_jx_k+\sum_\ell M_{i\ell}x_\ell^2
                    +\sum_\ell B_{i\ell}x_\ell+c_i.
\]

The field-linearized monomials `x` and `x^2` are independent when `q>=4`.
Let `G_i` be the homogeneous part. The center conditions are

\[
B_{ii}=0,\quad B_{ij}=\mu_0a_k\quad(i\ne j),\quad g(a)=0.
\]

All off-diagonal entries must be checked. Since `Ba=0` in characteristic
two, these conditions give exactly `c=G(a)` and `g(x)=G(x+a)`.

The homogeneous vector `G` is the gradient of

\[
H_0=\mu_0x_1x_2x_3+
\sum_iM_{ii}x_i^3+\sum_{i\ne j}M_{ij}x_ix_j^2.
\]

If its three quadrics generate all degree-four monomials, they have no
nonzero common zero over the algebraic closure. This is the rank-15 test
on the 18-by-15 Macaulay matrix. It is also necessary for a smooth residue:
three projectively zero-free quadrics in three variables form a regular
sequence, whose quotient has Hilbert series `(1+z)^3`. Euler's identity has
coefficient `3=1` in characteristic two, so projective gradient zeros are
precisely singular points of this cubic. The sole affine zero of `g` is
therefore `a`.

For `d=1`, coefficient separation is ambiguous because `x^2=x` as functions.
Eight exact evaluations of `g` instead certify its unique residue zero.
This suffices for counting and is guaranteed by the smooth translated
promise. The new mechanism therefore need not inherit the old `d>=3`
ordinary-cubic-uniqueness restriction.

## 2. Orthogonality and exact depth reduction

Summing the three highest field digits gives zero unless `g(x)=0`. Hence

\[
Z_e(p)=\sum_{Y\in A_{e-1}^3}(-1)^{p(a+tY)}.
\]

There is **no additional `q^3` factor outside this full restriction**. The
domain on the right still includes the old highest digits and already
contains their multiplicity.

The cubic part of the restricted phase is
`lambda_e(mu t^3 Y_1Y_2Y_3)`. For `e=2` or `3` it vanishes, so the entire
restriction is a binary quadratic and exact Gaussian elimination finishes
the count. For `e>=4`, manufacture

\[
\lambda_{e-3}((\mu\bmod t^{e-3})Y_1Y_2Y_3)
\]

and subtract it. The discrepancy is mathematically quadratic, so evaluating
it on inputs of binary Hamming weight at most two recovers it exactly; this
justifies `quadratic_coefficients` in the code. Check that the discrepancy
uses neither of the highest two digits of any `Y_i`. The manufactured cubic
also omits those digits. Removing these six free field coordinates gives

\[
Z_e(p)=q^6Z_{e-3}(p').
\]

The mask compression is injective on monomials in retained variables, so
the implementation's compressed set preserves the exact ANF, including its
constant. The retained cubic coefficient is still a unit.

## 3. Guaranteed family with arbitrary quotient-quadratic noise

Suppose in hidden ring-affine coordinates

\[
p(X)=\lambda_e(H(X+A))+R(X\bmod t^h),\qquad
h\le\lfloor(e+1)/3\rfloor,
\]

where `H` is homogeneous cubic with unit mixed coefficient and smooth
projective residue, while `R` is an arbitrary binary quadratic on the
quotient. The top derivative is `grad H_0(x+A_0)`, because `h<e`. The
acquired center is `a=A_0`. Write `A=a+tA_1`. Then

\[
H(a+tY+A)=t^3H(Y+A_1).
\]

After restriction, the perturbation lives on the quotient of depth `h-1`
when `h>0`, and is constant when `h=0`. For `e>=4`,

\[
h-1\le\left\lfloor\frac{(e-3)+1}{3}\right\rfloor.
\]

Both discarded layers are absent and the promise recurs. At depths two and
three the restricted homogeneous cubic vanishes and the allowed quotient
noise becomes constant. This proves acceptance inductively. Its rank may
be of order `3dh`, hence of order `n/3`; no rank enumeration occurs.

## 4. Full semilinear and Frobenius-functional invariance

This step is needed to pass from a hidden presentation to the presentation
actually acquired from the raw tensor.

Two coordinate systems identify the same full centroid algebra. Their
linear transition intertwines its multiplication action and therefore has
the form

\[
x=M\sigma(y)+a,
\]

where `sigma:A' -> A` is a ring isomorphism and `M` is invertible over `A`.
To see this, apply the transition to each ring basis vector: semilinearity
determines its value on all scalar multiples, and its three images give
the columns of `M`. Bijectivity makes `M` invertible.

Consider a hidden phase `lambda_old(H(x+b))+R(x mod J^h)`. Set

\[
b'=\sigma^{-1}(M^{-1}(a+b)),\qquad H_M=H\circ M.
\]

The functional `lambda_old o sigma` is nondegenerate. By the nondegenerate
pairing on `A'`, it uniquely has the form `lambda_new(c·)`. The multiplier
`c` is a **unit**: a nonunit in this finite local ring has a nonzero
annihilator, which would make the functional pairing degenerate. Thus put

\[
H'=c\,\sigma^{-1}(H_M),
\]

with `sigma^{-1}` acting coefficientwise. The phase becomes exactly

\[
\lambda_{new}(H'(y+b'))+R'(y\bmod (J')^h).
\]

The new cubic remains homogeneous. If `sigma_0` is the induced residue-field
isomorphism, then

\[
H'_0(y)=c_0\,\sigma_0^{-1}(H_0)
                   (\sigma_0^{-1}(M_0)y).
\]

Coefficient Frobenius commutes with formal differentiation. The gradient
therefore changes by coefficient Frobenius, a nonzero scalar, and the
transpose of an invertible residue matrix. Its projective zero set is
empty exactly when the original gradient's is empty. This explicitly
establishes smoothness invariance, including a noncanonical Frobenius.

The mixed coefficient changes to

\[
c_0\,\sigma_0^{-1}(\mu_0\det M_0),
\]

which is nonzero. A repeated-variable cubic cannot contribute `Y_1Y_2Y_3`
after a linear substitution in characteristic two, since the squared
linear factor has no cross terms. Higher terms of the uniformizer image
change higher coefficients and the functional unit; they do not introduce
inhomogeneous dependence on `y`.

Finally `sigma((J')^h)=J^h`, and `M` preserves `J^h A^3`. Thus the new
perturbation still factors through the same-depth quotient. Its binary
quadratic degree is preserved by the binary affine transition. All parts
of the promise survive acquisition.

## 5. Closing every depth class in uniform polynomial time

The current executable uses a bounded explicit field enumeration when
depth one is reached. The uniform theorem can instead use a known exact
fixed-degree point counter, after manufacturing the necessary field leaf.

At depth one, fit the actual Boolean phase to `Tr(P(X,Y,Z))` with ordinary
`degree(P)<=3`. There are 20 ordinary monomials and `d` coefficient bits
per monomial. Build their exact Boolean ANFs and solve the resulting binary
linear system with **20d columns**. Check the complete ANF identity. No
coefficient uniqueness is required, so the construction works for all `d`.

The promised quotient perturbation is constant by this stage, so a fit
always exists. A more general input passing earlier deflation gates need
not have such a fit; rejection here is essential for the uniform theorem.

Given the manufactured polynomial, form the four-variable hypersurface

\[
V:\quad W^2+W+P(X,Y,Z)=0.
\]

For each `(X,Y,Z)`, the number of `W` solutions is `1+(-1)^Tr(P)`, so

\[
Z_1=\#V(F)-q^3.
\]

Lauder and Wan's Theorem 1 gives deterministic point counting in fixed
characteristic and fixed number of variables, without a nonsingularity
assumption. Their Proposition 36, with characteristic two, four variables,
total degree three, and extension degree `d`, yields conservative bounds
`O-tilde(d^19)` bit time and `O-tilde(d^12)` bit space. The 16 torus strata
are constant in number. See [Lauder–Wan, MSRI 44 (2008), Theorem 1 and
Proposition 36](https://library.slmath.org/books/Book44/files/18lauder.pdf).

Thus the promised raw family has a deterministic polynomial-time exact
counting algorithm for every `d,e`, by this explicit reduction to that
existing algorithm. This does not say the generic point-count backend has
been implemented here. The executable currently realizes the quadratic
terminal classes and bounded field enumeration; the new leaf compiler
realizes the exact reduction interface.

## 6. Executed evidence and decisive failures

The independent top-digit checker uses chart Groebner smoothness rather
than the production Macaulay certificate and compares against full Boolean
truth tables computed by an exact Mobius transform.

- Twelve cases passed at `(d,e)=(2,2),(2,3),(2,4),(3,2)`, three each.
  They include arbitrary full translations, randomized higher cubic
  coefficients, dense quotient quadratics, and 24-bit `q^6` checks.
- Nine more passed for `d=1`, depths five, seven, and eight. The 21- and
  24-bit cases include two successive depth-three reductions and use the
  exact eight-point residue certificate.
- Three semilinear tests called the actual `compile_stationary` on raw
  ANF at `(d,e,n)=(3,2,18),(4,2,24),(3,3,27)`. All matched full exhaustive
  counts: `512`, `-4096`, and `262144`. Nontrivial field Frobenius,
  nonlinear uniformizer substitution, arbitrary invertible ring matrices,
  and two translations were included. A further 768 pointwise identities
  verified the functional-unit formula.

The unused-layer failure is explicit. At `d=2,e=4`, take

\[
H=X^2Z+Y^3+Z^3+XYZ.
\]

Its projective gradient is zero-free. Adding one linear bit from the `t^2`
coefficient of `X` leaves the top derivative and center unchanged, but
changes the signed count from `114688` to zero. The restriction activates a
discarded layer and is correctly rejected. Center forcing alone would
therefore be insufficient.

The field-terminal failure is also explicit: over `F_16`, add the product
of the first binary coordinate of `X` and the first binary coordinate of
`Y` to `Tr(XYZ)`. This field phase need not lie in the traced ordinary
degree-three space. The independent fitter checks and records its rejection;
an arbitrary binary quadratic must not be silently treated as an ordinary
quadratic over the extension field.

Programs and data are in this directory: `top_digit_deflation_audit.py`,
its two result files, `top_digit_failure_check.py`,
`top_digit_compression_failure.json`, `stationary_semilinear_audit.py`,
`stationary_semilinear_audit_results.json`, `field_leaf_compiler.py`, and
`field_leaf_compiler_results.json`.
