# Normalized crossing: exact attempt and the remaining coercivity step

This note audits and attempts to sharpen the all-prefix crossing proof in
`../output/pdf/crossing_section.tex`. The target was a bound
`gamma_n >= C(theta)^(-n)` at fixed angle, replacing the existing
`exp[-4n log n-O_theta(n)]` lower bound. **That improvement is not proved.**
The attempt gives exact normalized crossing formulas, finite-angle constants,
and a scalar obstruction to improving the existing argument using only its
propagated norm envelopes and polynomial interpolation.

The obstruction is about that proof method. It does not construct a physical
near-null mode and does not show that the actual singular gap is
superexponentially small.

## 1. Exact setting and shift envelope

Fix `u=cot(theta)>0`, any integer `n>=1`, and

\[
M_n(z)=\prod_{j=n}^{1}(zI+iP_{S,j}),\qquad
\mathcal C(A)=(\sigma_y\otimes I)A^{t_S}(\sigma_y\otimes I).
\]

The accepted crossing identity is

\[
\mathcal C[M_n(z-i)]=(z^2+1)^n M_n(z)^{-1}.
\tag{1}
\]

For the physical intertwiner error
`E(z)=Yhat M_n(z)-M_n(z) Xhat`, put
`delta=||E(u)||_2/(u^2+1)^(n/2)`. The crossing step alternates `X,Y`, so the
same error orientation returns at even shifts.

Let `a_k=sqrt(u^2+k^2)` for every integer `k`. At `z=u-ik`, the step norm
multiplier is at most `(a_(k+1)/a_(k-1))^n`. Multiplying the factors before
making any simplification gives

\[
\|E(u-2ij)\|_2\le W_j\delta,
\qquad
W_j=\left(\frac{a_{2j-1}a_{2j}}{u}\right)^n,
\quad j=0,1,\ldots.
\tag{2}
\]

In particular `W_0=a_1^n`, so the initial condition is an equality. Formula
(2) holds for every `u>0`; no large-`n` or weak-angle approximation is used.

## 2. Natural normalization makes the inverses contractive, but not the shift

Define the normalized monodromy

\[
R_n(z)=\frac{M_n(z)}{(z+i)^n}
=\prod_{j=n}^{1}\left(P^+_{S,j}
+\frac{z-i}{z+i}P^-_{S,j}\right).
\tag{3}
\]

At a real spectral parameter it is unitary. At `z=u-ik`, `k>=0`,
`||R_n(z)^(-1)||_infinity<=1`. The latter is an exact bound, attained on a
fully symmetric spin state. The crossing relation becomes

\[
\mathcal C[R_n(z-i)]
=\left(\frac{z-i}{z}\right)^n R_n(z)^{-1}.
\tag{4}
\]

For `H(z)=Yhat R_n(z)-R_n(z)Xhat`, the corresponding error step gives

\[
\|\widetilde H(z-i)\|_2
\le\left|\frac{z-i}{z}\right|^n\|H(z)\|_2.
\]

Consequently

\[
\|H(u-2ij)\|_2\le (a_{2j}/u)^n\delta.
\tag{5}
\]

The normalization removes one growing factor from the error values. It
simultaneously changes polynomial interpolation into rational interpolation:
`E(z)=(z+i)^n H(z)`. Evaluation at `z=0` therefore multiplies the `j`-th
sample weight by `a_(2j-1)^n`, restoring exactly (2). The same cancellation
occurs for every nonzero scalar normalization `E(z)/f_n(z)` when one uses
the same propagated pointwise bounds. A scalar rescaling cannot improve
the conditioning of that data-to-evaluation problem.

The contractive-inverse observation in (3) is therefore valid, but treating
it as a uniform constant shift bound would omit the scalar factor in (4).

## 3. Exact normalized-trace monodromy norms

Normalized Hilbert–Schmidt averaging also has exact formulas. At `z=u-ik`,

\[
\|M_n(z)\|_{2,\tau}^2
=(u^2+k^2-k+1)^n,
\tag{6}
\]

\[
\|M_n(z)^{-1}\|_{2,\tau}^2
=\left[
\frac{u^2+k^2+k+1}
{(u^2+(k-1)^2)(u^2+(k+1)^2)}
\right]^n.
\tag{7}
\]

For (6), the normalized trace over the last fresh bath site sends
`L(z)^dagger L(z)` to
`(u^2+k^2-k+1)I_S`; trace sites successively. For (7), use
`L(z)^(-1)=(zI-iP)/(z^2+1)` and trace in the reverse peeling order.

These trace averages cannot replace the two operator norms in
`||M^(-1) E M^(-1)||_2` for an arbitrary unknown error operator. Normalized
Hilbert–Schmidt norm is not submultiplicative. The needed inequality is

\[
\|AEB\|_2\le\|A\|_\infty\|B\|_\infty\|E\|_2.
\]

Furthermore the operator-norm inverse estimate is not merely a loose
product bound: the fully symmetric subspace has
`M_n(z)=(z+i)^n I`, and for `k>=0` it attains
`||M_n(z)^(-1)||_infinity=a_(k-1)^(-n)`.
One needs information about the **actual intertwiner residual subspace**
to exclude this concentration; a normalized trace by itself supplies none.

## 4. Exact interpolation constants retain the same exponent

At `z_j=u-2ij`, `j=0,...,n`, define the exact absolute weights

\[
d_j=\frac1{2^n j!(n-j)!},\qquad
\ell_j=\frac{\prod_{k\ne j}a_{2k}}{2^n j!(n-j)!}.
\]

Here `d_j` extracts the leading coefficient of a degree-`n` polynomial,
and `ell_j` evaluates it at zero. The original proof remains valid with

\[
K_n^{\rm grid}=\sum_{j=0}^n W_j(d_j+\ell_j)
\tag{8}
\]

in place of its cruder common-envelope constant. In particular it proves

\[
\gamma_n\ge
\frac6{n(n+1)(2n+1)(K_n^{\rm grid})^2}.
\tag{9}
\]

This improves finite constants only. Let

\[
F_{n-1}(u)=\prod_{k=1}^{n-1}
\sqrt{1+\frac{u^2}{4k^2}}.
\]

The last evaluation weight is exactly

\[
\ell_n=\frac{u F_{n-1}(u)}{2n}.
\]

Therefore

\[
K_n^{\rm grid}\ge
\frac{uF_{n-1}(u)}{2n}
\left(\frac{a_{2n-1}a_{2n}}u\right)^n.
\tag{10}
\]

At every fixed `u>0`, `F_(n-1)(u)` is bounded above and below by positive
constants, and (10), together with the preserved upper bound, yields

\[
\log K_n^{\rm grid}=2n\log n+O_u(n).
\]

Thus exact weights and the exact telescoped norm envelope still give the
same `-4n log n` singular-gap exponent.

## 5. Even infinitely many shift-envelope bounds do not suffice

There is a stronger, explicit obstruction to this interpolation strategy.
For fixed `u>0,n>=1`, define a scalar degree-`n` polynomial

\[
p_n(z)=\prod_{\ell=0}^{n-1}
\frac{z-u+2i\ell}{-u+2i\ell}.
\tag{11}
\]

It obeys `p_n(0)=1` and vanishes at the first `n` even-shift points. For
every integer `j>=n`,

\[
|p_n(u-2ij)|
=\frac{2n}{uF_{n-1}(u)}\binom jn.
\tag{12}
\]

Using `binom(j,n)<=j^n/n!` and
`a_(2j-1)a_(2j)>=(4-2/n)j^2` gives, simultaneously for **all** `j>=0`,

\[
\frac{|p_n(u-2ij)|}{W_j}\le\Delta_n,
\qquad
\Delta_n=
\frac{2n}{uF_{n-1}(u)n!}
\left[\frac{u}{(4-2/n)n}\right]^n.
\tag{13}
\]

The polynomial (11) initially has zero error at `z=u`. To match the exact
initial normalization, rather than only an upper bound there, put

\[
\beta_n=1-W_0/W_n>0,\qquad
\eta_n=W_0\Delta_n/\beta_n,
\qquad
q_n(z)=\frac{p_n(z)+\eta_n}{1+\eta_n},
\]

\[
\delta_n=\frac{\Delta_n}{\beta_n+W_0\Delta_n}.
\tag{14}
\]

Then the following finite statements hold exactly:

\[
q_n(0)=1,\qquad |q_n(u)|=W_0\delta_n,
\qquad
|q_n(u-2ij)|\le W_j\delta_n
\quad\text{for every integer }j\ge0.
\tag{15}
\]

For `j<n`, only the added constant remains. For `j>=n`, the triangle
inequality and `W_j>=W_n` give the last inequality in (15), because
`beta_n+W_0/W_j<=1`.

At fixed `u`, Stirling's formula gives

\[
\log\delta_n=-2n\log n+O_u(n).
\tag{16}
\]

Hence the following data are compatible with a unit value at the desired
cyclic point: degree at most `n`, the exact initial norm equality, and every
even-shift norm estimate propagated by the accepted crossing argument,
with an initial error of size (16). No evaluation theorem using only those
data can bound `|q_n(0)|<=C(u)^n delta_n`. Arbitrary scalar normalization of
the samples does not change this statement.

This is a scalar certificate for insufficiency of the **norm envelopes**.
It deliberately makes no assertion that `q_n` is the physical matrix
intertwiner of any `X,Y`. The full operator crossing identity has more
information than (15), and that extra information is precisely what an
improved proof must exploit.

## 6. Precise blocked step and current consequence

The actual transport alternates the source-transpose operation with left
and right multiplication by inverse monodromies. The worst-case inverse
direction at one shift need not remain a worst-case direction after the
source transpose. Taking separate operator norms at each step discards
this alignment information. A bound on the **composed** crossing transport,
restricted to physical residuals `Yhat M-M Xhat` and using their polynomial
compatibility, could be stronger. No suitable `C(u)^n` estimate for that
composition is established in this attempt.

An exponential coercivity proof would need, for example, a uniform estimate

\[
\|[\widehat X,C_{\rm cyc}]\|_2
\le C(u)^n\,
\|U^{(n)}\widehat XU^{(n)\dagger}
-I_S\otimes T_n(X)\|_2
\]

or an equivalent positive-metric/fused-transport inequality that controls
the same physical residual. The scalar and tracial normalizations above
do not supply it.

The established unrestricted fixed-angle memory converse therefore remains
`Omega(log(1/epsilon)/log log(1/epsilon))`, or `Omega(N/log N)` at the stated
fixed-angle horizon. Neither a matching exponential singular-gap bound nor
a physical counterexample to such a bound has been obtained. All finite
formulas above retain the exact angle parameter `u=cot(theta)>0`; no
weak-angle uniformity is claimed.
