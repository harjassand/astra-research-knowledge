# Smooth residue cubics, invisible quotient perturbations, and raw affine-center audit

## Result and scope

Let `R_e=F_q[t]/t^e`, `q=2^d`, and
`psi_e(v)=(-1)^Tr([t^(e-1)]v)`. Let `H` be an ordinary homogeneous cubic in
three ring variables whose residue `H_0` defines a smooth projective plane
curve. If `h<=floor((e+1)/3)`, then every Boolean function `Q` of the quotient
coordinates `X mod t^h` satisfies

\[
 \sum_{X\in R_e^3}\psi_e(H(X))(-1)^{Q(X\bmod t^h)}
 =(-1)^{Q(0)}Z_e(H),\qquad Z_e(H)=\sum_X\psi_e(H(X)).
\tag{1}
\]

No low-rank condition on `Q` is needed for this identity. For algorithmic
acquisition from an explicit cubic ANF, restrict `Q` to an arbitrary binary
quadratic on the quotient; then a polynomial-size linear solve acquires
`H+Q`, and the smooth residue cubic is uniquely determined by every solution.
This is a checked representation class. It does not claim efficient
recognition of dependency on hidden variables for an unrestricted program.

The homogeneous sum itself satisfies

\[
 Z_2=q^3,\quad Z_3=q^6,\quad Z_e=q^6 Z_{e-3}\quad(e\ge4).
\tag{2}
\]

Consequently all smooth residue cubics have the explicit counts

\[
 Z_e=\begin{cases}
 q^{2e},&e\equiv0\pmod3,\\
 q^{2e-1},&e\equiv2\pmod3,\\
 q^{2e-2}Z_1(H_0),&e\equiv1\pmod3.
 \end{cases}
\tag{3}
\]

Thus two out of the three chain-length classes need no finite-field point
counter at all. For the last class, the only remaining computation is on
three field variables, regardless of the nilpotent depth `e`.

For quadratic `Q`, its allowed polar rank can be as large as the largest even
integer below `3dh`, about one third of the original `n=3de` input count
(and one half when `e=2`). Equation (1) evaluates that perturbation without
Walsh branching or rank decoding. The coordinate quotient is intrinsic to
`J^h R_e^3`, where `J=(t)` is the recovered radical; arbitrary invertible
ring-linear changes preserve it.

These are local stationary-phase constructions. The broad method has
established ancestry, including Fisher's stationary-phase work and Sawin's
local-ring Kloosterman work already examined in CHAIN_RING_COUNTER.md. No
historical-priority claim is made for the homogeneous recurrence or the
orthogonality identity. The useful compiler extension is their acquisition,
exact closure checks, and use with the original independent inputs.

## Proof of the recurrence and perturbation identity

Euler's identity in characteristic two gives
`H_0=sum_i X_i partial_i H_0`, because the degree three equals one in the
field. Smoothness therefore implies that the three partial derivatives have
no common nonzero point over the algebraic closure, and in particular no
common nonzero point over `F_q`.

For `e>=2`, translating a variable by its highest digit gives

\[
 H(X+t^{e-1}U)-H(X)
 =t^{e-1}\nabla H_0(X\bmod t)\cdot U.
\tag{4}
\]

Summing that digit cancels unless `X mod t=0`. The remaining points are
exactly `X=tY`, with `Y in R_(e-1)^3`. Homogeneity gives `H(tY)=t^3H(Y)`.
If `e=2` or `e=3`, this phase vanishes, proving the first two formulas.
If `e>=4`, the phase depends only on `Y mod t^(e-3)`. The two unused digit
layers in each of three coordinates contribute `q^6`, proving (2).

Now include `Q(X mod t^h)`. It does not involve the highest digit whenever
`h<=e-1`, so (4) still forces `X mod t=0`. After restriction `X=tY`, the
perturbation depends on only `h-1` digits, while the cubic depth decreases
by three. Repeat. At stage `j<h`, the condition needed to sum the highest
digit without changing the perturbation is

\[
 h-j\le e-3j-1.
\]

Its strongest instance is `j=h-1`, namely `3h<=e+1`. This is exactly the
stated range. Thus all the digits seen by `Q` are forced to zero before a
terminal field computation can occur. The remaining factor is `(-1)^Q(0)`.
The `e=2,3` terminal steps are included in the same argument.

### More general reusable identity

For an ordinary homogeneous polynomial of degree `D` prime to the residue
characteristic, in `b` ring variables, with smooth projective reduction,
the same proof gives

\[
 Z_e=q^{b(D-1)}Z_{e-D}\quad(e>D),\qquad
 Z_e=q^{b(e-1)}\quad(2\le e\le D).
\]

A perturbation depending on the first `h` digits is invisible up to its value
at zero whenever

\[
 Dh\le e+D-2.
\]

This is an identity, not an assertion that the representation or arbitrary
perturbation dependency is automatically recoverable. The cubic/quadratic
case above supplies an explicit acquisition method.

## Manufacture the cubic plus quotient quadratic from raw ANF

Assume the preceding centroid stage has acquired coordinates of `R_e^3`.
There are ten ordinary homogeneous cubic monomials in three variables. Form
the binary ANF of each such monomial with each of the `ed` binary coefficient
basis elements of `R_e`, followed by `Tr([t^(e-1)] . )`. These `10ed` ANFs
are available by evaluation on subsets of at most three coordinate basis
vectors; no truth table is needed.

Let `U` be the span of all binary monomials of degree at most two supported
on the `3dh` quotient bits. Solve the linear equation

\[
 p\in \operatorname{span}\{\text{the }10ed\text{ ring-cubic ANFs}\}+U.
\tag{5}
\]

Implementation need not explicitly include all columns of `U`: retain only
ANF rows that are cubic or involve at least one non-quotient bit, solve for
`H` there, and then reconstruct the exact remainder `Q=p+psi(H)`. Verify
that remainder has degree at most two and uses only quotient bits.

### The smooth residue is independent of which linear solution is chosen

Suppose `psi(D_H)` depends only on the quotient, for a homogeneous ring cubic
`D_H`. Its derivative under every shift in the highest digit is zero because
`h<=e-1`. By (4) and nondegeneracy of the field trace pairing,

\[
 \partial_i(D_H)_0(X_0)=0
 \quad\text{for every }X_0\in F_q^3,\ i=1,2,3.
\]

A homogeneous quadratic in three variables that vanishes everywhere on
`F_q^3` is zero. For `q>2`, its degree in every variable is below `q`. For
`q=2`, its square terms become the three distinct unary Boolean monomials
and its mixed terms become the three distinct quadratic Boolean monomials,
which are still independent. Euler's identity then forces `(D_H)_0=0`.
Thus every solution to (5) has exactly the same `H_0`. If one admissible
smooth fit exists, arbitrary linear solution selection cannot lose it.

Projective smoothness can be checked by the constant-size Macaulay test below
or by a Gröbner-basis computation in the three affine charts. The independent
implementation uses the latter. Once a fit is acquired and checked, (1)–(3)
give the exact count. The original independent bit count is always `3ed`;
there are no additional internal-state assignments in the result.

The fit has `O(n)` unknown cubic coefficients and `O(n^3)` ANF rows. A direct
schoolbook construction and solve is polynomial in the explicit description
length `L` and `n`. A conservative bound for the implementation is
`O(L+n^7)` bit operations and `O(L+n^4)` bits of space before an optional
finite-field leaf; this includes naive field traces, ring products, and
packed binary elimination. More efficient coefficient construction is
possible, but is unnecessary for the theorem. Generic depths zero and two
modulo three require no further counting engine.

## Exact terminal field formula for an ordinary elliptic family

Suppose `d` is odd and

\[
 H_0(X,Y,Z)=X^2Y+XY^2+Z^3+aXYZ.
\]

Its projective curve is smooth precisely when `a^3!=1`. This follows from
its gradient

\[
 (Y^2+aYZ,\ X^2+aXZ,\ Z^2+aXY).
\]

A nonzero critical point must have `Z!=0`; setting `Z=1` shows that the only
possible case is `X=Y=a` with `a^3=1`.

For any homogeneous cubic and odd `d`, cubing permutes `F_q^*`. Sum first
along each projective line to obtain

\[
 Z_1=q\bigl(\#\{H_0=0\}\subset\mathbb P^2(F_q)-q-1\bigr).
\tag{6}
\]

For the displayed family, the chart `Y=1` is the elliptic curve
`y^2+a x y+y=x^3`, with one point at infinity. When `a!=0`, set
`u=a^(-3)` and scale `x=a^2x'`, `y=a^3y'`, then translate
`x'=X+u`, `y'=Y+u^2`. The resulting curve is

\[
 Y^2+XY=X^3+uX^2+c,\qquad c=u^3+u^4=(a^3+1)/a^{12}.
\]

At nonzero `X`, dividing by `X^2` and using trace orthogonality gives
`1+(-1)^Tr(X+u+c/X^2)` solutions. The `X=0` fiber has one point. Hence

\[
 \#E(F_q)=q+1+(-1)^{\operatorname{Tr}(u)}K(c),
\]

where `K(c)=sum_(x!=0)(-1)^Tr(x+c/x)`; replacing `sqrt(c)` by `c` is valid
by Frobenius invariance of Kloosterman sums. Combining with (6),

\[
 Z_1=q(-1)^{\operatorname{Tr}(a^{-3})}
         K\bigl((a^3+1)/a^{12}\bigr).
\tag{7}
\]

The existing exact Dwork implementation executes this field sum. When `a=0`
and `d` is odd, the curve `y^2+y=x^3` has `q+1` points because cubing
permutes the field, so `Z_1=0`.

The implementation rejects a depth-one residue outside this explicit family.
For even `d` it now uses the separately executed bounded-Laurent counter
proved in LAURENT_TERMINAL_EXTENSION.md; that backend also supports arbitrary
linear shifts of the explicit family. General fixed-variable finite-field
point counting supplies a broader theoretical leaf but has not been
implemented here. Formula (6) itself must not be used for even `d`: cubing is
then three-to-one on its image.

## Why unrestricted linear Walsh shifts are not closed

For the smooth binary cubic

\[
 H=XYZ+Z^3+Y^3+X^2Z,
\]

adding a single linear bit beyond the allowable quotient changes the count:

| Ring length | Allowed quotient depth | Added X digit | Base signed sum | Shifted signed sum |
|---|---:|---:|---:|---:|
| 2 | 1 | 1 | 8 | 0 |
| 3 | 1 | 1 | 64 | 0 |
| 5 | 2 | 2 | 512 | 0 |

Digits are numbered from zero. All three examples were fully enumerated and
rejected by the acquired quotient-fit compiler. This is why the homogeneous
recurrence cannot simply be attached to arbitrary Walsh leaves. The parent
compiler repairs a larger affine class by acquiring stationary centers and
checking actual unused coordinates at every recursive step.

## Independent audit of the parent's affine-center mechanism

### Degree-four Macaulay criterion

For the three homogeneous quadratics `g_i=partial_i H_0`, multiply each by
all six degree-two monomials. Their coefficients in the fifteen degree-four
monomials form an `18 by 15` matrix. The matrix has rank fifteen if and only
if the gradient has no projective zero over the algebraic closure.

One direction follows by evaluation: if all degree-four monomials lie in
the gradient ideal, a projective common zero would annihilate every fourth
power of a coordinate, which is impossible. Conversely, no projective zero
makes the three quadratics a homogeneous regular sequence in the polynomial
ring in three variables. Its quotient has Hilbert series `(1+s)^3`, so its
degree-four part vanishes. This proves the rank condition, including
characteristic two.

### Acquiring an undisclosed affine residue center

If the highest-digit derivative yields the vector polynomial

\[
 g_i(X)=\mu_0X_jX_k+\sum_lM_{il}X_l^2+
                       \sum_lB_{il}X_l+c_i,
\]

and this comes from the gradient of `H_0(X+a)`, its linear coefficients obey
`B_ii=0`, `B_ij=B_ji=mu_0 a_k` for the complementary index `k`. When
`mu_0!=0`, these manufacture `a`. Verify those relations and `g(a)=0`;
the homogeneous quadratic part and the Macaulay test then certify that
`a` is the only residue critical point. No search over field elements is
needed.

The coefficient fit distinguishes `X_l^2` from `X_l` when `d>=2`. At `d=1`
those functions coincide: the ten-feature space has rank seven. A compiler
must handle that small field separately, for example by checking its eight
residue vectors, or state a `d>=2` restriction. Treating the ten features as
independent for `d=1` would be incorrect.

After summing highest digits, restrict to `X=a+tY`. The parent checks the
actual resulting quadratic remainder and verifies that the top two digit
layers of `Y` are unused before multiplying by `q^6` and recursing. This
check is required; the smooth gradient alone does not justify dropping a
general lower-degree perturbation. At terminal depth two or three, the
restricted cubic part vanishes and exact binary quadratic elimination is
valid.

## Executed files and evidence

- `smooth_ring_counter.py`: independent generic smoothness check, homogeneous
  and explicit field-family counts, and raw-coordinate linear acquisition
  of a cubic plus unrestricted quotient quadratic.
- `smooth_ring_checks.py`, `smooth_ring_results.json`: five complete acquired
  ANF counts on 6,9,12,15,18 bits, with noise ranks 0,2,4,8; all agree with
  full Boolean enumeration. Thirty residue-family smoothness checks and ten
  full finite-field counts verify (7). The three incompatible shifts above
  are preserved.
- `macaulay_gradient_audit.py`, `macaulay_gradient_results.json`: 752 exact
  Macaulay-versus-independent-Buchberger comparisons (all 512 binary cubics
  with XYZ coefficient one, plus 240 random cubics over F4,F8,F16), and
  202 recovered affine gradient centers with all coefficient identities
  checked. The d=1 feature-rank failure is explicitly executed.

These are correctness demonstrations and algebraic audits, not timing
comparisons against specialist stationary-phase or elliptic-curve software.
