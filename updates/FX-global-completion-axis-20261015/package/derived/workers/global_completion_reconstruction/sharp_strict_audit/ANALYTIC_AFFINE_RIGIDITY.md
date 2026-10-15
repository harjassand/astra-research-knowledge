# Analytic zero-density fields are affine

15 October 2026. Same-team independent deduction from actual rows of the
pinned sharp negative-branch Gram support. External review, formal proof
verification, and historical novelty remain UNKNOWN.

Fix r<-2. Let U be a connected open subset of the plane and let
Psi:U->R² be real analytic. If the full corrected sharp heat density

\[
\mathcal D_r(D\Psi,D^2\Psi)
=\ell^TS_r\ell,\qquad
\ell=C_r^T(\operatorname{vec}D\Psi\otimes D^2\Psi),
\]

vanishes identically, then Psi is affine on U. No boundary or growth
hypothesis is needed for this conclusion.

Because S_r is positive definite, every entry of ell vanishes. The eight
rows independently regenerated in `check_kernel_and_scaling.py` imply

\[
X_i(D\Psi)\Psi_{j,yy}=0,\qquad
Y_i(D\Psi)\Psi_{j,xx}=0\quad(i,j=1,2),
\]

where X=(a-d,b+c) and Y=(-3b+(2r+1)c,(2r+1)a+3d).
All four products in each family are meant.

If neither X nor Y is identically zero, analyticity and these product
equations give Psi_xx=Psi_yy=0 throughout U. If X is identically zero but
Y is not, the Y products give Psi_xx=0. The Cauchy-Riemann equations X=0
make each component harmonic, so Psi_yy=0 as well. If Y is identically zero
but X is not, the X products give Psi_yy=0. The anisotropic Cauchy-Riemann
equations Y=0 give k² Psi_xx+Psi_yy=0 with k=-(2r+1)/3>1, so Psi_xx=0.
If both X and Y vanish identically, their combined linear coefficient
matrix has determinant 4(r+2)², hence D Psi=0.

Thus, in every case, both pure second derivatives vanish. On a connected
open set Psi_xy is a constant vector v, giving

\[
\Psi(x,y)=A x+B y+vxy+c.
\]

The actual fourth zero-based row of C_r^TZ is

\[
\ell_4=
\frac{a(r+1)z_1+a z_5+b z_2+c(r+1)z_4}{r+1}.
\]

For this bilinear map, z_2=z_5=0, z_1=v_1, z_4=v_2,
a=A_1+v_1y and c=A_2+v_2y. Therefore

\[
\ell_4=A\cdot v+|v|^2y.
\]

Its vanishing on the open set forces |v|²=0. Hence v=0 and Psi is affine.
Every identity used here is reconstructed from the actual kernel rows;
the analyticity argument is an explicit written proof, not an inference
from finite sampled positivity.

For the construction's compact-data application, an affine map Bx+eta
with eta Schwartz has D eta=0. For its angular heat application, a
sublinearly growing affine map has zero gradient. On a torus, an affine
periodic perturbation is constant. These consequences supply the required
rigidity without a separate quantitative estimate. They do not imply a
uniform fourth-order Jensen margin.
