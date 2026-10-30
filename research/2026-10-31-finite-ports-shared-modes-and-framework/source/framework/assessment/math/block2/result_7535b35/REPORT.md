# A better compatible heat certificate for the exceptional cubic

The central all-ROC-implies-QC question is still open. This continuation constructs a different leading heat correction and proves the following improvement for the explicit open family in the checkpoint:

\[
 P_\nu=2|X|^2|Y|^2+|Y|^4+\operatorname{Re}(\overline X Y^2)
                  +\nu(|X|^2+|Y|^2)
 \quad\text{is QC whenever}\quad
 \nu\ge\nu_*:=\frac{3+\sqrt3}{24}=0.197168783648703\ldots .
\]

The previous sufficient threshold was 1/4. The exact ROC threshold remains 3/16. Thus the concrete unresolved interval is now

\[
 3/16\le\nu<(3+\sqrt3)/24.
\]

The construction is global in the mean and amplitude and uses actual gradient heat flow. It is not a numerical field test. It also yields a rational certificate at \(\nu=1/5\). The optimized threshold is sharp within the complete class of polynomial heat certificates whose corrected density is a sum of squares of expressions affine in the base gradient and linear in the compatible Hessian; the last part of this report specifies and proves that scope. This is a certificate-class result, not a necessary QC condition.

## 1. Normalization and source boundary

As in the earned capsule, put

\[
 X=(a+d)+i(c-b),\qquad Y=(a-d)+i(c+b),\qquad F_0=3F_{1/3}=2|X|^2|Y|^2+|Y|^4.
\]

The whole polynomial is multiplied by three: \(P=3p\). The cubic considered here is \(C=\operatorname{Re}(\overline X Y^2)\). The cubic normal form, exact ROC membership formula and threshold 3/16 are inherited from the checkpoint. The homogeneous heat method and primary primitive retain their Bruno--Pasqualotto credit in the packet. The new ingredient is an adjustable leading primitive, its Gram factorization, and its completion and optimization with the exceptional cubic.

Only the assigned packet, named checkpoint and this continuation's files were read. There was no external lookup, service contact or other continuation access. All numerical probes below are local discovery diagnostics and all retained claims are checked exactly.

## 2. The new one-parameter leading primitive

Let \(f=u_1+iu_2\) be the deformation, and use the compatible Hessian coordinates

\[
 P=f_{zz},\quad Q=f_{z\bar z},\quad R=f_{\bar z\bar z}.
\]

Here \(Q\) denotes a complex Hessian coordinate, not a lower quadratic. Define

\[
\begin{aligned}
 A_1&=\overline X P+2\overline YQ,\\
 A_2&=Y\overline R+X\overline Q+\overline YQ,\\
 A_3&=X\overline Q+2\overline YQ,\\
 L_7&=XQ+2YP.
\end{aligned}
\]

Set \(V=(A_1,A_2,A_3)^T\), and

\[
 G_\rho=\begin{pmatrix}
 1+\rho/2&\rho&-\rho\\
 \rho&2&-\rho\\
 -\rho&-\rho&1+\rho
 \end{pmatrix}.
\]

In original matrix coordinates let \(T=a^2+b^2+c^2+d^2\), \(D=ad-bc\), and

\[
 \theta=-c\,da-d\,db+a\,dc+b\,dd,\qquad
 \zeta=-b\,da+a\,db-d\,dc+c\,dd.
\]

The new cubic one-form is

\[
\boxed{
 \alpha_\rho=
 [(3+9\rho/2)T+(14-7\rho)D]\theta
 +[(9-9\rho/2)T+(7\rho-6)D]\zeta .}
\]

For a function \(H(A)\) and closed two-form \(\Omega\), denote the corrected compatible heat density by

\[
 \mathcal E(H,\Omega)
   =H''(A)[B_1,B_1]+H''(A)[B_2,B_2]+\Omega_A(B_1,B_2),
\]

where \(B_j=\partial_j Du\) are the actual compatible derivatives. Direct polynomial identity gives

\[
\boxed{\quad
 \mathcal E(F_0,d\alpha_\rho)
       =16\left(\frac\rho2|L_7|^2+V^*G_\rho V\right).
 \quad}                                                     \tag{1}
\]

At \(\rho=0\) this is precisely the checkpoint's three-square leading density, with the second and third complex squares conjugated. The additional \(L_7\) term and the nondiagonal Gram matrix are essential to the improvement.

For \(0\le\rho<2\), Sylvester's criterion proves \(G_\rho\) positive definite: the leading minors are

\[
 1+\rho/2,\qquad (2-\rho)(1+\rho),\qquad
 (2-\rho)(2+4\rho-\rho^2)/2.
\]

Thus (1) is a valid global leading heat certificate throughout this interval.

## 3. Completing the exceptional cubic

Retain the checkpoint's closed linear two-form

\[
\begin{aligned}
 \Omega_C={}&-8(a-d)\,da\wedge dc
 +8(b+c)\,da\wedge dd\\
 &+8(b+c)\,db\wedge dc
 +8(a-d)\,db\wedge dd.
\end{aligned}
\]

Its exact density is

\[
 \mathcal E(C,\Omega_C)=32\operatorname{Re}(A_3\overline R).
\]

For the quadratic \(\nu(|X|^2+|Y|^2)=2\nu T\), the constant two-form with coefficients

\[
 \nu(-8,-16,0,0,-16,-8)
\]

in the ordered pairs \((ab,ac,ad,bc,bd,cd)\) gives density \(64\nu|R|^2\). These correcting forms are exact globally: the radial primitives are \(\frac13\iota_E\Omega_C\) and \(\frac12\iota_E\Omega_Q\), respectively.

Let \(e_3=(0,0,1)^T\). Combining the three densities and completing a square gives

\[
\begin{aligned}
 \frac1{16}\mathcal E(P_\nu,\Omega_\rho+\Omega_C+\Omega_Q)
  ={}&\frac\rho2|L_7|^2\\
   &+(V+G_\rho^{-1}e_3R)^*G_\rho(V+G_\rho^{-1}e_3R)\\
   &+\left(4\nu-f(\rho)\right)|R|^2,
\end{aligned}                                                \tag{2}
\]

where

\[
 f(\rho)=e_3^TG_\rho^{-1}e_3
       =\frac{2(\rho+1)}{2+4\rho-\rho^2}.
\]

Consequently \(P_\nu\) is QC whenever \(4\nu\ge f(\rho)\) for some \(0\le\rho<2\). Indeed along ordinary componentwise heat flow, the integral of every exact correction vanishes and the energy derivative is minus the integrated uncorrected density. Formula (2) makes this energy nonincreasing to its affine-mean value. The periodic and compact-support approximation argument is the same compatible argument as in the supplied primary certificate; the forms here are global polynomials, with no selector or incompatible minimization step.

Differentiation yields

\[
 f'(\rho)=\frac{2(\rho^2+2\rho-2)}{(\rho^2-4\rho-2)^2}.
\]

The minimum is at \(\rho_* =\sqrt3-1\), with

\[
 f(\rho_*)=(3+\sqrt3)/6,
 \qquad \nu_*=(3+\sqrt3)/24.
\]

The simpler choice \(\rho=1\) gives \(f=4/5\), hence the entirely rational certificate \(\nu\ge1/5\).

For \(C_\kappa=\operatorname{Re}(\kappa\overline X Y^2)\), rotations transport the construction and scaling gives the sufficient condition

\[
 \nu\ge \frac{3+\sqrt3}{24}|\kappa|^2.
\]

Translations, affine terms, and extra ROC quadratics may be added, using the supplied Fourier fact that a ROC quadratic is QC. This covers the two conformal exceptional cubic modes and their transported quadratic extensions. It does not classify arbitrary \(M\) or arbitrary lower cross terms.

## 4. The optimization is substantive, rather than a chosen Gram matrix

The new leading correction was found by treating the acoustic nulls as constraints on the full 60 coefficients of a quadratic two-form. If a pointwise leading heat density is nonnegative, then at every acoustic zero its six-dimensional Hessian matrix annihilates the corresponding rank-one compatible Hessian. The resulting coefficient system has rank 39. Closure raises its rank to 54. After averaging over the residual circle preserving \(C\) and over conjugation, only two leading parameters remain. This is derived exactly in `leading_null.py` and `leading_symmetry.py`; it does not assume that the primary primitive is unique.

There is also an exact optimality result for a broad, explicitly limited certificate class. Allow any closed two-form polynomial in the base of degree at most two, and require the resulting density to be a sum of squares of expressions affine in the base and linear in the Hessian. The optimum within this class is precisely \(\nu_*\).

Here is the algebraic reduction and dual bound. A leading square must vanish at every acoustic pair. The full real bilinear space has 24 coordinates and its acoustic-null subspace has dimension 12. A complex basis, with six independent real-and-imaginary pairs, is

\[
 L_7,\quad L_5=XR+2YQ,\quad
 L_3=X\overline R+2\overline YP,\quad A_1,A_2,A_3.
\]

Under the residual circle their weights are \(-7,-5,-3,-1,-1,-1\). The constant Hessian terms have weights \(-5,-3,-1\). Averaging a square certificate preserves its sum-of-squares property. Coefficient matching with a closed correction therefore leaves exactly

\[
 \lambda_7|L_7|^2+r|L_5|^2+(t-r)|L_3|^2+V^*G_{t,z,r}V,
\]

with

\[
 \lambda_7=t/4-z/2,\quad
 G_{t,z,r}=\begin{pmatrix}
 1+5t/4-z/2-r&t-z&z-t\\
 t-z&2(1-t)&z\\
 z-t&z&1-t/2-z+r
 \end{pmatrix},                                             \tag{3}
\]

where all scalar square weights are nonnegative and \(G\) is PSD. In particular \(t\ge0\). The linear coefficient matching is performed exactly in `sos_family.py`: the 11 coefficients (two primitive parameters and nine Gram parameters) satisfy a rank-eight linear system, leaving exactly the three parameters in (3). The general primitive underlying (3) is also verified by the final receiver.

Write the cubic square couplings as

\[
 2e\operatorname{Re}(L_5\overline P)
 +2f\operatorname{Re}(L_3\overline Q)
 +2\operatorname{Re}(V^*kR).
\]

The checkpoint's complete closed cubic-correction family forces, and is equivalent to,

\[
 e+k_1=0,\qquad k_2=0,\qquad f+k_3=1.
\]

Its one visible cubic-correction parameter is \(\gamma=4(1-e-f)\). If the constant quadratic block is \(a|P|^2+b|Q|^2+c|R|^2\), closedness and Fourier compatibility give \(a+b+c=4\nu\). Positivity of the square Gram matrices forces

\[
 4\nu\ge e^2/r+f^2/(t-r)+k^TG^+k,
\]

with the usual range conditions at zero weights. For

\[
 v=(1-1/\sqrt3,\ (1-1/\sqrt3)/2,\ 1)^T,
 \qquad T_0=G+\operatorname{diag}(r,0,t-r),
\]

Cauchy--Schwarz and the three coupling constraints imply

\[
 1\le (4\nu) v^TT_0v.
\]

But direct exact calculation gives

\[
 v^TT_0v=3-\sqrt3+(5/6-\sqrt3/2)t\le3-\sqrt3.
\]

Thus \(\nu\ge[4(3-\sqrt3)]^{-1}=\nu_*\). Our certificate attains this bound at \(t=r=0\), \(z=1-\sqrt3\). This proves that further optimization of affine-base bilinear square heat densities cannot close the remaining ROC/QC gap. Nonnegative densities outside this square class, nonpolynomial corrections, and other compatible arguments remain possible.

## 5. An attained local-jet bound, with its proper limitation

For the one-parameter leading family (1) and the fixed cubic correction \(\Omega_C\), the obstruction is even an attained finite-jet test. Put \(m=(3+\sqrt3)/6\), \(a_0=1-1/\sqrt3\), and

\[
 R=1,\quad Q=-3/(1+2\sqrt3),\quad P=-Q/\sqrt3,\qquad
 Y=-m/[2(Q-P)],\quad X=-2YP/Q,
\]

all real. Equivalently, the finite jet is

\[
 X=(6+\sqrt3)/18,\quad Y=(1+2\sqrt3)/12,\quad
 P=(6-\sqrt3)/11,\quad Q=(3-6\sqrt3)/11,\quad R=1.
\]

Then exactly

\[
 L_7=0,\quad (A_1,A_2,A_3)=-m(a_0,a_0/2,1),
 \quad V^*G_\rho V=m
\]

for every \(\rho\). The quartic-plus-cubic corrected density divided by 16 is therefore \(-m\). At \(\nu=\nu_*\) the quadratic correction in (2) supplies exactly \(m\). These are legitimate compatible local Hessian jets because the complex coordinates are an invertible real parameterization of all six Hessian entries.

This finite-jet fact is a test of pointwise heat certificates. It is not an integrated negative-energy gradient field, and does not show non-QC below \(\nu_*\). The numerical `pointwise_probe.py` was only a way to locate the equality jet; the displayed algebraic jet is checked exactly.

## 6. Verification and remaining scope

Run `python3 verify.py`. The captured successful output is `verification.txt`. The receiver independently reconstructs the new primitive, Gram factorization, closed cubic and quadratic corrections, full completion, optimized coefficient, finite equality jet, acoustic-null basis, general square family and exact dual inequality. The auxiliary scripts preserve the construction and local numerical discovery; they do not establish QC by sampling.

This improves a concrete compatible QC theorem and identifies an exact barrier for a larger square-certificate class than the checkpoint considered. It does not establish QC in the remaining interval \([3/16,(3+\sqrt3)/24)\), including its left endpoint. It also leaves the other exceptional cubic directions and sharp arbitrary cross-quadratic classification unresolved. No ROC/non-QC separation, physical claim, novelty claim or general Morrey resolution is asserted.
