# A sharp section of the quadratic compatible-heat cone

Write `A=[[a,b],[c,d]]`, `s=|A|^2`, `j=det A`, and

\[
 F_{\alpha,\beta}=\alpha s^2+\beta j^2.
\]

A compatible second jet is

\[
 B_1=(z_0,z_1,z_3,z_4),\qquad B_2=(z_1,z_2,z_4,z_5)
\]

in row-major order. The certificate class in this note is a positive constant
scalar input matrix D and a closed two-form omega with homogeneous quadratic
coefficients, such that

\[
 \sum_{i,k}D_{ik}D^2F(A)[B_i,B_k]
                       +\omega_A(B_1,B_2)\ge0              \tag{1}
\]

for every A and every compatible second jet. A bilinear SOS is a special
case. Exactness of omega follows from closedness by the polynomial Euler
primitive `(1/4)i_E omega`.

**Theorem.** Such a certificate exists exactly for

\[
 \alpha\ge0,\qquad -2\alpha\le\beta\le(12+8\sqrt3)\alpha.
                                                               \tag{2}
\]

Every member of this interval has a bilinear SOS certificate.

## 1. Symmetry gives the complete two-parameter correction

F is invariant under left and right O(2). If (1) holds, transform it by these
orthogonal symmetries and average. The transformed metric is `R^T D R`;
its right-rotation average is `(tr D/2)I`. The pullback correction transforms
as a two-form; an input reflection reverses the two spatial derivative
directions and contributes its determinant sign. Therefore, after dividing
by the positive number `tr D/2`, there is an isotropic certificate whose
correction is left O(2)-invariant, right SO(2)-invariant, and odd under a right
reflection. Averaging preserves pointwise nonnegativity, closedness and
homogeneous degree. The same argument preserves existence of an SOS Gram.

The complete averaged correction space is

\[
 \omega=d\{k s\zeta+\ell j\theta\},                    \tag{3}
\]

where

\[
 \theta=a\,dc-c\,da+b\,dd-d\,db,
 \qquad\zeta=a\,db-b\,da+c\,dd-d\,dc.
\]

For completeness, use conformal complex coordinates

\[
 z=(a+d+i(c-b))/2,\qquad w=(a-d+i(c+b))/2.
\]

Left and right rotations give independent phase rotations of z and w.
Put `rho_z=|z|^2`, `rho_w=|w|^2`, and
`tau_z=Im(conj(z)dz)`, `tau_w=Im(conj(w)dw)`.
Invariant cubic one-forms are the eight products of either rho with either
radial differential `d rho` or either angular form tau. Modulo exact radial
one-forms, their derivatives span four angular derivatives and
`d rho_z wedge d rho_w`. An output reflection sends `(z,w)` to
`(conj(w),conj(z))`; an input reflection interchanges z and w. The required
parities eliminate the radial cross term and leave precisely the two angular
combinations `rho_z tau_z-rho_w tau_w` and
`rho_z tau_w-rho_w tau_z`. Their span equals (3). The Euler primitive ensures
that starting from an arbitrary closed quadratic two-form loses no forms.

`invariant_space.py` separately verifies completeness by exact linear algebra:
there are 60 quadratic two-form coefficients, and closedness, the two rotation
Lie equations and the two reflection conditions have rank 58.

## 2. Three point evaluations give the exact upper obstruction

Set `h=sqrt(3)`. Evaluate the corrected isotropic density from (3) at these
three compatible jets:

1. `A=diag(1,0)`, `(z0,z2,z4)=(1,h,0)`, other jets zero;
2. `A=diag(1,0)`, `(z1,z3,z5)=(0,-(2+h),1)`, other jets zero;
3. `A=I`, `(z0,z2,z4)=(1,-1,-1)`, other jets zero.

Their values are

\[
\begin{aligned}
 q_0&=24\alpha+4h k,\\
 q_1&=(32+16h)\alpha+2\beta-(4+2h)k+(2+h)\ell,\\
 q_2&=32\alpha-8\beta-8k-4\ell.
\end{aligned}                                                \tag{4}
\]

All three must be nonnegative. The positive linear combination

\[
 (1+2h/3)q_0+q_1+\frac{2+h}{4}q_2
 =2(1+h)\big[(12+8h)\alpha-\beta\big]                 \tag{5}
\]

eliminates every correction parameter. This proves the upper bound in (2)
for the entire correction class, not just a numerically selected ansatz.

These point jets are not a periodic negative field. Equation (5) separates
the pointwise certificate class and does not refute an integrated inequality.

## 3. A four-square exact endpoint certificate

Take `alpha=1`, `beta=12+8h`,

\[
 k=-2h,\qquad\ell=-16-12h.
\]

Define four bilinear forms:

\[
\begin{aligned}
 L_1={}&\tfrac{h-1}{2}az_3+\tfrac{h+1}{2}az_5-bz_4
       +\tfrac{1-h}{2}cz_0-\tfrac{1+h}{2}cz_2+dz_1,\\
 L_2={}&(1+h)az_4-(2+h)bz_3-bz_5
       -(1+h)cz_1+(2+h)dz_0+dz_2,\\
 L_3={}&\tfrac{3-h}{2}az_0+\tfrac{1-h}{2}az_2+bz_1
       +\tfrac{3-h}{2}cz_3+\tfrac{1-h}{2}cz_5+dz_4,\\
 L_4={}&\tfrac{3+h}{3}az_1-\tfrac h3 bz_0+bz_2
       +\tfrac{3+h}{3}cz_4-\tfrac h3 dz_3+dz_5.
\end{aligned}                                                \tag{6}
\]

Direct polynomial expansion gives the universal identity

\[
 D^2F(A)[B_1,B_1]+D^2F(A)[B_2,B_2]+\omega_A(B_1,B_2)
 =(16+8h)(L_1^2+L_3^2)+4L_2^2+12L_4^2.                 \tag{7}
\]

Every weight is positive. This is an algebraic exact certificate for all A
and compatible jets, with no diagonal-matrix restriction in (7).

Conjugating `h -> -h` also gives a positive certificate, because
`16-8h>0`, at `beta=12-8h`. Let `Q_+ = Q_0+h Q_1` be the 24 by 24 rational-field
Gram of (7). Its conjugate is `Q_- = Q_0-h Q_1`. For rational beta between
these endpoints,

\[
 Q_\beta=Q_0+\frac{\beta-12}{8}Q_1                    \tag{8}
\]

is rational and is a positive convex combination of `Q_+` and `Q_-`.
The corresponding primitive has rational coefficients

\[
 k=(12-\beta)/4,\qquad \ell=2-3\beta/2.
\]

At beta=25, `F25_EXACT_HEAT_CERTIFICATE.json` contains the full rational Gram,
an exact rank-eight rational LDL factor, and the primitive. Positivity is
checked directly from its positive rational pivots, independently of (8).

## 4. The lower endpoint and the full interval

For rank-one `R=e11` at `A=e22`,

\[
 D^2F(A)[R,R]=4\alpha+2\beta.
\]

At a rank-one-compatible jet `B_i=b_i R`, the two-form term vanishes because
its arguments are proportional. Thus any certificate implies ROC. Testing
the other rank-one directions gives `alpha>=0`; the displayed test gives
`beta>=-2alpha`.

At the lower endpoint,

\[
 |A|^4-2(\det A)^2=\operatorname{tr}((A^T A)^2)
\]

is convex. Indeed its Hessian in a direction H is

\[
 2\operatorname{tr}((H^T A+A^T H)^2)
       +4\operatorname{tr}(A^T A H^T H)\ge0.
\]

Both terms are explicit sums of bilinear squares, so no correction is needed.
Positive interpolation between this certificate and (7) proves every beta
in (2). When alpha=0, the lower and upper bounds force beta=0.

Every form in the entire ROC half-sector `alpha>=0, beta>=-2alpha` is already
polyconvex, since

\[
 F_{\alpha,\beta}=
 \alpha\operatorname{tr}((A^T A)^2)+(\beta+2\alpha)(\det A)^2.
                                                               \tag{9}
\]

This is exactly why the sharp certificate exclusion does not address the
remaining heat-plus-polyconvex inclusion.

## 5. A separating functional on the full isotropic-heat cone

For a general invariant quartic in the coefficient order of
`ROC_CLASSIFIER.md`, average over both O(2) actions. The result is
`alpha s^2+beta j^2`, with

\[
 \alpha=[3(p_0+p_1)+p_2+p_3]/8,\qquad
 \beta=[-p_0-p_1+p_2-p_3]/2.
\]

If the original certificate has isotropic heat, averaging preserves that
same heat. Substitution in `(12+8h)alpha-beta>=0` yields

\[
 (5+3h)(p_0+p_1)+(1+h)p_2+(2+h)p_3\ge0.                \tag{10}
\]

For a general anisotropic integrand and a variable metric, averaging F and D
together does not factor their product. Equation (10) is not asserted for
that larger class.
