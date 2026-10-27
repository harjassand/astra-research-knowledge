# An executed field terminal counter closed under linear shifts

For every field `F=F_(2^d)` and coefficients `a,rho,sigma,tau,g`, the program
computes

\[
 S=\sum_{X,Y,Z\in F}(-1)^{\operatorname{Tr}(
 X^2Y+XY^2+Z^3+aXYZ+\rho X+\sigma Y+\tau Z+g)}
\tag{1}
\]

in deterministic polynomial time and space in `d`, without enumerating field
elements. At `a=0` this is already a binary quadratic on `3d` bits. At
`a!=0` it reduces to one binary Gaussian and one bounded Laurent phase.
The latter is an exact specialization of the earlier established finite
Dwork machinery, not a new point-counting principle.

This removes the odd-extension-degree restriction of the simpler elliptic
formula and closes this explicit field family under all linear Walsh shifts.
It does not supply an executed generic smooth-ternary-cubic counter, and does
not establish closure under arbitrary ring-level shifts.

## Derivation of the Laurent phase

The identity `Tr(X^2Y)=Tr(X sqrt(Y))` lets us sum `X` exactly. The sum is zero
unless

\[
 \sqrt Y+Y^2+aYZ+\rho=0,
\]

and otherwise contributes `q`. If `Y=0`, this requires `rho=0`, leaving the
binary quadratic Gaussian

\[
 G(\tau)=\sum_Z(-1)^{\operatorname{Tr}(Z^3+\tau Z)}.
\]

For `Y!=0`, substitute the bijection `Y=w^2`; the constraint determines

\[
 z(w)=a^{-1}(w^2+w^{-1}+\rho w^{-2}).
\]

Therefore

\[
 S=q(-1)^{\operatorname{Tr}(g)}
 \left[1_{\rho=0}G(\tau)+
 \sum_{w\ne0}(-1)^{\operatorname{Tr}(z(w)^3+\sigma w^2+\tau z(w))}\right].
\tag{2}
\]

Expanding the cube and repeatedly folding
`Tr(cw^(2j))=Tr(sqrt(c)w^j)`, including negative `j`, leaves only the
nonconstant exponents `{3,1,-1,-3,-5}`. The implementation manufactures these
coefficients by exact sparse multiplication and Frobenius folding.

Explicitly, with `b=a^(-1)`, the constant is `b^3` and the coefficients are

\[
\begin{aligned}
 c_3&=b^3+\sqrt{b^3},\\
 c_1&=\sqrt{b^3\rho}+\sqrt\sigma+\sqrt{\tau b},\\
 c_{-1}&=\sqrt[4]{b^3\rho}+\sqrt{b^3\rho^2}
                    +\tau b+\sqrt{\tau b\rho},\\
 c_{-3}&=b^3+\sqrt{b^3\rho^3},\\
 c_{-5}&=b^3\rho^2.
\end{aligned}
\]

All roots are unique field Frobenius inverses. Formula (2) holds for all
extension degrees and even when the homogeneous cubic is singular.

## Bounded-Laurent finite Dwork matrix

Let `f(w)=sum c_j w^j` have no constant term. Let `m_+` be its largest
positive exponent and `m_-` the largest absolute negative exponent, setting
an absent side to zero. Choose `N=d+2`. Since the torus sum has absolute
value at most `q-1`, its residue modulo `2^N` determines it uniquely.

Use the prior exact unramified ring
`A=(Z/2^N Z)[T]/lift(h)` and splitting series

\[
 \theta(U)=\exp(-2U+2U^2)=\sum_{k\ge0}\lambda_kU^k,
 \qquad v_2(\lambda_k)\ge k/4.
\]

For Teichmüller coefficients `C_j`, form
`F_i(w)=product_j theta(C_j^(2^i) w^j)`. A coefficient at positive exponent
`r` has valuation at least `r/(4m_+)`, and the negative counterpart has
valuation at least `|r|/(4m_-)`: each contributing term has valuation at least
`sum k_j/4`, while its exponent is bounded on either side by the corresponding
maximum exponent times `sum k_j`.

Thus truncate each theta factor at `k<4N`, and all intermediate convolutions
to

\[
 I=[-4m_-N+1,\ 4m_+N-1],
\]

replacing an absent endpoint by zero. Every discarded coefficient already
vanishes modulo `2^N`; later products cannot restore it. Define

\[
 M_i[u,v]=[w^{2u-v}]F_i(w)\quad(u,v\in I).
\]

The finite Dwork trace identity gives

\[
 \sum_{w\ne0}(-1)^{\operatorname{Tr}(f(w))}
 \equiv(q-1)\operatorname{Tr}(M_{d-1}\cdots M_0)\pmod{2^N}.
\tag{3}
\]

The finite state interval suffices: any omitted closed path has either a
maximal positive or minimal negative state outside the interval. An incident
exponent `2u-v` has at least that magnitude on the same side, forcing the
associated coefficient to vanish modulo `2^N`. Every omitted closed-path
contribution is therefore zero.

The implementation checks that the nonconstant unramified-ring coefficients
of the answer vanish, then performs exact centered reconstruction. The
constant phase of `f` is restored separately. At support `{3,1,-1,-3,-5}`,
the matrix dimension is at most `32N-1`. Direct schoolbook arithmetic gives
a conservative `O(d^8)` bit-time and `O(d^4)` bit-space bound. General bounded
Laurent input is polynomial in `d`, its number of terms, and the exponent
magnitudes; those magnitudes are not treated as free when encoded in binary.
All final answers in (1) have at most `3d+1` bits.

## Executed evidence and API

`laurent_field_counter.py` exports:

- `laurent_dwork(poly,h,details=False)`: `poly` maps integer Laurent exponents
  to polynomial-basis field coefficients. Returns the exact torus sum.
- `shifted_hesse_sum(h,a,rho=0,sigma=0,tau=0,constant=0,details=False)`:
  returns (1). The `a=0` branch uses exact binary quadratic elimination.

`laurent_field_checks.py` and `laurent_field_results.json` contain twenty
general Laurent cases and twenty-four shifted three-variable cases over
extension degrees one through four, all checked against complete field
enumeration. Four cases explicitly cover the `a=0` branch. All pass.
These are correctness checks, not comparative performance benchmarks.

`smooth_ring_counter.py` uses this backend for even-degree leaves of the
explicit homogeneous family. Odd-degree leaves retain the faster single
Kloosterman formula. A generic residue cubic outside this family is still
rejected at chain lengths congruent to one modulo three.

## Generic terminal theorem versus implementation

For an arbitrary ternary field cubic `H`, introduce one Artin–Schreier
variable:

\[
 W^2+W=H(X,Y,Z).
\]

Every trace-zero right hand side has exactly two `W` solutions and every
trace-one right hand side has none. Therefore, with `N_AS` the affine point
count, the desired signed sum is `N_AS-q^3`.

Lauder–Wan, *Counting points on varieties over finite fields of small
characteristic*, https://arxiv.org/pdf/math/0612147, Proposition 36 and the
affine torus decomposition in Section 6.4, provide an unconditional
**first-point-count** bound. With characteristic two, four variables, total
degree three, and extension degree `d`, this is soft-O(`d^19`) **bit time**
and soft-O(`d^12`) **bits of space**. These are not unit-cost field-operation
bounds, and no full zeta-function computation is needed.

That theorem gives a complete theoretical generic terminal. It has not been
executed as a generic engine here. A direct unreduced multivariate Dwork
implementation has polynomially many states but very large dense matrices:
roughly cubic state growth and sixth-power dense storage in precision for a
three-variable additive phase. The current runtime has no installed Sage,
PARI/cypari, FLINT, or similar point-counting package. An efficient generic
implementation would require additional cohomological reduction or a proved
acquisition of a suitable elliptic/projective model. No acquired Hesse normal
form is assumed, and the explicit Laurent backend is not relabelled generic.
