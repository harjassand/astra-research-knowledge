# A movable leading heat primitive improves the exceptional QC frontier

The central all-ROC-implies-QC question remains unresolved. This continuation establishes a stronger compatible positive result for the checkpoint's concrete open family:

\[
P_\nu=F_0+\operatorname{Re}(\overline X Y^2)
                   +\nu(|X|^2+|Y|^2)
\quad\text{is QC whenever}\quad
\nu\ge\nu_*:=\frac{3+\sqrt3}{24}=0.197168783648703\ldots .
\]

The preceding sufficient coefficient was 1/4. The exact ROC coefficient, inherited from the checkpoint, is 3/16. Thus this is a proved improvement within the previously unresolved ROC interval, with a remaining gap; it is not a separation or a full resolution of the exceptional face.

`verify.py` is a standalone exact receiver. It verifies the correcting forms, their polynomial primitives, the full compatible density identity in all base and Hessian coordinates, positivity of its Gram matrix, and the exact coefficient optimization. Its complete passing output is `verification.txt`. No numerical feasibility output is used to establish the theorem.

## 1. Target, inherited representation, and the contingent failure

The scientific contract concerns actual compatible gradients, all affine means, and arbitrary admissible lower quadratics in the entire four-extra-mode face. It does not prescribe a particular heat primitive. I retain the coordinate normalization

\[
x=(a+d,c-b),\quad y=(a-d,c+b),\quad
X=x_1+ix_2,\quad Y=y_1+iy_2,
\]

so that

\[
F_0=3F_{1/3}=2|X|^2|Y|^2+|Y|^4.
\]

The checkpoint's strongest informative failure was a 1/4 obstruction for **a fixed primary leading correction**, even after all closed linear cubic corrections and all constant quadratic corrections were allowed. Its degenerating compatible jets make the primary leading squares nearly singular in precisely the channel used by the cubic. This does not discard compatibility: it discards the freedom to move dissipation between different exact leading null Lagrangians.

Here the leading primitive itself varies. A new joint Gram representation then completes the cubic and quadratic simultaneously. All forms remain global polynomial forms; there is no correction selector, pointwise gradient assumption, replacement by matrix distributions, or change of the leading polynomial.

## 2. A one-parameter family of leading primitives

Write \(T=a^2+b^2+c^2+d^2\), \(D=ad-bc\), and use the inherited one-forms

\[
\theta=-c\,da-d\,db+a\,dc+b\,dd,
\qquad
\zeta=-b\,da+a\,db-d\,dc+c\,dd.
\]

For a parameter \(0\le k<1\), define

\[
\boxed{\alpha_k=
 [(3+9k)T+(14-14k)D]\,\theta
 +[(9-9k)T+(-6+14k)D]\,\zeta.}
\tag{1}
\]

At \(k=0\) this is exactly the checkpoint's leading primitive, the s=1/3 specialization of the supplied Bruno--Pasqualotto Appendix A primitive, scaled by three. The new deformation is

\[
\alpha_k-\alpha_0=k(9T-14D)(\theta-\zeta).
\]

Consequently \(d\alpha_k\) is a globally exact homogeneous quadratic two-form for every k. This changes no integrated heat derivative on periodic gradients.

The discovery calculation first allowed **all** homogeneous quadratic closed two-forms. Requiring their leading compatible density to annihilate the continuous acoustic null jets gives a consistent 136-by-60 rational linear system of rank 54. The circle symmetry of the cubic and simultaneous conjugation leave two parameters. The one-parameter subfamily (1) is enough for the positive result. The rank calculation explains how the family was obtained, but the final theorem needs only the explicit identity verified below, not any completeness claim about that exploratory elimination.

## 3. The joint compatible Gram identity

For an actual complex deformation \(f=f_1+if_2\), put

\[
P=f_{zz},\qquad Q=f_{z\bar z},\qquad R=f_{\bar z\bar z}.
\]

Here Q denotes a complex Hessian coordinate. It is not the lower quadratic polynomial. The corresponding six real compatible Hessian coordinates are

\[
(h_0,h_1,h_2,h_3,h_4,h_5)=
(\operatorname{Re}(P+2Q+R),\ -\operatorname{Im}P+\operatorname{Im}R,
\operatorname{Re}(-P+2Q-R),
\operatorname{Im}(P+2Q+R),\ \operatorname{Re}(P-R),
\operatorname{Im}(-P+2Q-R)).
\]

They give
\(B_1=(h_0,h_1,h_3,h_4)^T\) and
\(B_2=(h_1,h_2,h_4,h_5)^T\), the two derivatives of the matrix gradient. Define

\[
\begin{aligned}
W_1&=\overline X P+2Y\overline R,\\
W_2&=\overline Y Q-Y\overline R,\\
W_3&=X\overline Q+2Y\overline R,\\
N&=XQ+2YP,
\end{aligned}
\quad
K_k=\begin{pmatrix}
1+k&2&0\\
2&10-4k&4-2k\\
0&4-2k&3-2k
\end{pmatrix}.
\tag{2}
\]

With \(\Omega_F=d\alpha_k\), the exact leading identity is

\[
\frac1{16}\left(
F_0''(A)[B_1,B_1]+F_0''(A)[B_2,B_2]
                         +\Omega_F(A)[B_1,B_2]\right)
=W^*K_kW+k|N|^2.
\tag{3}
\]

This is a polynomial identity for **every** real base A and every compatible real Hessian. It does not require a rank-one Hessian, a diagonal base, a phase restriction, or an integration ansatz.

Retain the checkpoint's closed linear cubic form

\[
\Omega_C=-8(a-d)\,da\wedge dc+8(b+c)\,da\wedge dd
            +8(b+c)\,db\wedge dc+8(a-d)\,db\wedge dd
\tag{4}
\]

and the constant form \(\Omega_Q\) whose coefficients in the ordered pairs
\((ab,ac,ad,bc,bd,cd)\) are \((-8,-16,0,0,-16,-8)\).
Both are exact: their primitives are respectively
\(\alpha_C=(1/3)\iota_E\Omega_C\) and
\(\alpha_Q=(1/2)\iota_E\Omega_Q\), with E the radial vector field.

For \(C=\operatorname{Re}(\overline X Y^2)\), their compatible densities, divided by 16, are

\[
2\operatorname{Re}\big(\overline{2W_2+W_3}\,R\big),
\qquad 4|R|^2,
\tag{5}
\]

for C and \(|X|^2+|Y|^2=2T\), respectively. The identities in (5) agree with the inherited correction; only the leading primitive has changed.

Let

\[
\delta_k=1+4k-2k^2,\qquad
v=(0,2,1)^T,\qquad
u_k=\frac{(-2,1+k,-1)^T}{\delta_k}.
\]

Direct multiplication gives

\[
K_ku_k=v,\qquad v^Tu_k=\frac{2k+1}{\delta_k}.
\tag{6}
\]

For any real cubic amplitude \(\lambda\), the corrected heat density of

\[
F_0+\lambda C+\nu(|X|^2+|Y|^2),
\quad \Omega=\Omega_F+\lambda\Omega_C+\nu\Omega_Q,
\]

is therefore exactly

\[
\boxed{
16\left[
(W+\lambda Ru_k)^*K_k(W+\lambda Ru_k)
+k|N|^2+
\left(4\nu-\lambda^2\frac{2k+1}{\delta_k}\right)|R|^2
\right].}
\tag{7}
\]

This is the construction's hardest step: one polynomial primitive supplies a nonnegative density for all compatible jets and all bases after a single explicit completion. Every coefficient and the full identity are checked symbolically by `verify.py`.

## 4. Positivity and the improved coefficient

The leading principal minors of K are

\[
1+k,\qquad 6+6k-4k^2,\qquad
2(1-k)(1+4k-2k^2).
\]

All are strictly positive for \(0\le k<1\). Thus (7) is nonnegative under

\[
\nu\ge \lambda^2\rho(k),\qquad
\rho(k)=\frac{2k+1}{4(1+4k-2k^2)}.
\tag{8}
\]

Its derivative has the sign of \(2k^2+2k-1\), so this sufficient coefficient is minimized at

\[
k_*=(\sqrt3-1)/2,\qquad
\rho(k_*)=\frac{3+\sqrt3}{24}.
\tag{9}
\]

This is optimal within the displayed one-parameter **Gram completion bound**. I do not claim that it is the optimal pointwise heat certificate over every primitive, or the sharp QC coefficient. A completely rational alternative is \(k=1/3\), giving \(\nu\ge15/76=0.197368421\ldots\).

The checkpoint's old obstructing jets have normalized corrected leading density tending to 1 at k=0. Under (1), it tends to \(1+3k\). This exact limit, checked in the receiver, shows specifically why the fixed-primitive obstruction does not survive this deformation. No jet has been promoted to an integrated negative-energy field.

## 5. Why the construction proves QC at every mean

Take an affine mean plus a smooth periodic perturbation and evolve the perturbation by ordinary componentwise heat flow. For its gradient A(t), integration by parts gives

\[
\frac{d}{dt}\int P(A(t))
=-\int\left(P''(A)[B_1,B_1]+P''(A)[B_2,B_2]\right).
\]

The pullback of each exact polynomial two-form in (7) integrates to zero on the periodic cell. Consequently the right side equals minus the integral of (7), and is nonpositive under (8). Heat flow converges smoothly to the affine mean, proving the quasiconvex inequality. Smooth periodic tests and the ordinary compact-support approximation give the usual gradient-test definition, as in the supplied primary heat construction. Polynomial degree and smooth compact tests make the energy integrations finite. All means are permitted in the pointwise identity, including means outside the coordinate axes.

For a complex coefficient \(\kappa\), proper domain/output rotations can remove its phase while preserving F0 and the isotropic quadratic. Hence the theorem also proves

\[
F_0+\operatorname{Re}(\kappa\overline X Y^2)
                 +\nu(|X|^2+|Y|^2)\quad\text{QC if}\quad
\nu\ge \nu_*|\kappa|^2.
\]

Argument translations, affine terms, and addition of an arbitrary ROC quadratic preserve this QC conclusion. The last assertion uses the ordinary compatible Fourier proof of QC for a quadratic nonnegative on rank-one amplitudes.

## 6. Exact remaining scope and preserved failed attack

For \(\kappa=1\), the retained exact ROC threshold is 3/16. What remains undecided by this continuation is

\[
3/16\le\nu<(3+\sqrt3)/24.
\]

The entire exceptional face additionally contains the other two real M directions and all cross quadratic terms. This continuation supplies no classification or QC proof for those missing directions and does not solve general Morrey.

The exploratory finite Gram search at \(\nu=3/16\) did not converge to a feasible certificate; its residual was approximately 0.01439. A search at \(\nu=0.195\) likewise retained a residual near 0.00243. These are failures of a numerical SOS search only. They do not prove infeasibility of that certificate class, non-QC, or sharpness of (9). A search at \(\nu=1/5\) yielded a feasible matrix; `exactify_certificate.json` records a rational PSD certificate for that intermediate result. The much shorter analytic family (1)--(9) supersedes it and is independently verified without relying on the numerical solver.

## 7. Artifacts and provenance

Run `python3 verify.py` in this directory. The receiver imports no exploratory files and makes no network or service calls.

`leading_rigidity.py` retains the all-quadratic-form acoustic elimination; `optimize_primitive.py` retains the two-parameter symmetry reduction; `sos_search.py` and `cached_search.py` retain the local NumPy feasibility searches; `exactify.py` retains rational reconstruction; and `derive_family.py` recovers the short primitive (1). Their output files preserve successful and failed steps. The final proof is `verify.py` plus (1)--(9), not a passing finite field list.

Scientific source rights used were the named `SECOND_PHASE.txt`, `CONTEXT_PROCEDURE.txt`, frozen packet task/provenance, the named m02 checkpoint capsule/report/receiver, and `packet/math/rotational_faces/PROOF.txt`. The homogeneous heat method and primary k=0 primitive retain their supplied Bruno--Pasqualotto credit; the rank-one lower boundary is inherited from the checkpoint. No sibling continuation, evaluation/design material, memory, unrelated repository, external source, provider feedback, or nested agent was used. Writes were confined to this assigned continuation directory.
