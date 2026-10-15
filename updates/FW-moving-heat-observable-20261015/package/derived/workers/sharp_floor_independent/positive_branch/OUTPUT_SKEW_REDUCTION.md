# Flat acoustic contact eliminates the surviving output-skew operator

Date: 2026-10-15. This is an append-only extension of the frozen input-diffusion obstruction. `REPORT.md`, `CERTIFICATE.json`, `verify_obstruction.py`, and their verification receipt are unchanged.

For every \(r>0\), let

\[
J_r=\frac{3r}{8(r+2)}H+\frac{r(r-1)}6u^2+j^2+ruj.
\]

**Reduction theorem.** If a constant real strongly parabolic output-matrix operator and a \(C^2\) closed two-form correction give a universally pointwise nonnegative compatible-heat dissipation density for \(J_r\), then a constant positive definite scalar input-diffusion operator and a correction in the same class do so as well. The potential output-skew mixed derivative is forced to vanish by the flat acoustic contact.

For \(r=1\), combining this reduction with the frozen independent input-diffusion obstruction gives a self-contained no-go for the **entire constant real strongly parabolic output-matrix operator plus \(C^2\) closed-two-form class**. This is still a method obstruction. Quasiconvexity remains **UNKNOWN**.

## 1. General constant operators and the exhaustive symmetry reduction

Start with

\[
\mathcal Lu=\sum_{i,j=1}^2 C^{ij}\partial_{ij}u,
\qquad C^{ij}\in\mathbb R^{2\times2}.
\]

We may take \(C^{ij}=C^{ji}\), since mixed partials commute. Strong parabolicity means that the symmetric part of its real principal symbol satisfies

\[
\eta^T\left(\sum_{i,j}C^{ij}\xi_i\xi_j\right)\eta
\ge c|\eta|^2|\xi|^2
\]

for a constant \(c>0\) and all real target and input vectors. The natural integrated energy dissipation is represented by

\[
\sum_{i,j}D^2J_r(A)[B_i,C^{ij}B_j],
\]

up to an allowed exact two-form correction.

Average the certificate over left target rotations, a symmetry of \(J_r\). Each coefficient matrix becomes

\[
C^{ij}=a_{ij}I+b_{ij}\mathsf J,
\qquad \mathsf J=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]

This follows from the commutant of planar rotations; already averaging conjugation by \(\mathsf J\) gives the displayed form. Both input coefficient matrices \(A=(a_{ij})\) and \(B=(b_{ij})\) are symmetric. Strong parabolicity forces \(A\) positive definite, since the output-skew part has zero real quadratic value.

The paired target/input reflection \((S,S)\), with \(S=\operatorname{diag}(1,-1)\), is an energy symmetry. It transforms the coefficient matrices by

\[
A\mapsto SAS,\qquad B\mapsto-SBS,
\]

because \(S^{-1}\mathsf JS=-\mathsf J\). Averaging removes \(a_{12}\), \(b_{11}\), and \(b_{22}\).

There is also an exact energy symmetry

\[
J_r(AT)=J_r(A),\qquad
T=\frac1{\sqrt h}\begin{pmatrix}0&h\\1&0\end{pmatrix},
\quad h=\frac{2r+1}{3}>0.
\]

The checker verifies the polynomial identity \(J_r(AK)=h^2J_r(A)\), where \(K=\sqrt hT\); quartic homogeneity gives the displayed symmetry. Here \(T^2=I\), \(\det T=-1\), and \(STS=-T\). The input transformations generate a finite dihedral group. The paired reflection normalizes the left rotation group, so the averages can be imposed simultaneously.

For arbitrary input matrices, the dihedral averages are

\[
A\longmapsto
\frac12\begin{pmatrix}a_{11}+ha_{22}&0\\0&a_{22}+a_{11}/h\end{pmatrix},
\qquad
B\longmapsto\begin{pmatrix}0&b_{12}\\b_{12}&0\end{pmatrix}.
\]

The first is positive definite and proportional to \(\operatorname{diag}(h,1)\). After positive normalization of its trace to two, the only possible operator is

\[
\boxed{\mathcal L=
\frac{2r+1}{r+2}\partial_{xx}I
+\frac3{r+2}\partial_{yy}I
+2b\mathsf J\partial_{xy}.}
\]

Linear changes of variables pull back closed two-forms. Their correction transforms as \((\det R)\Phi^*\omega\), with \(\Phi(A)=LAR\); thus all symmetry averages preserve the correction class and pointwise positivity. The determinant sign is the same orientation parity checked in the frozen input proof. Nonorthogonality of \(T\) causes no problem: it is invertible, and its covariance sends positive input quadratic forms to positive input quadratic forms.

For the mixed term, integration by parts in one coordinate initially gives \(2bD^2J_r(B_1,\mathsf JB_2)\). We use the symmetric representative

\[
b\big[D^2J_r(B_1,\mathsf JB_2)+D^2J_r(B_2,\mathsf JB_1)\big].
\]

The difference is an exact two-form: with \(\alpha_A(X)=DJ_r(A)[\mathsf JX]\),

\[
d\alpha_A(X,Y)=D^2J_r(A)[X,\mathsf JY]
-D^2J_r(A)[Y,\mathsf JX].
\]

It can therefore be absorbed into the allowed correction.

## 2. A contact identity independent of the correction

In fact, let \(d_1,d_2\) be arbitrary real numbers; the next calculation does not require the averaged ratio. Write

\[
\begin{split}
\mathcal P(A,z)={}&d_1D^2J_r(A)[B_1,B_1]
+d_2D^2J_r(A)[B_2,B_2]\\
&+b\big[D^2J_r(A)[B_1,\mathsf JB_2]
+D^2J_r(A)[B_2,\mathsf JB_1]\big]
+\omega_A(B_1,B_2).
\end{split}
\]

At the contact \((A,z)=(I,e_{z_2})\), \(B_1=0\), \(B_2=e_{12}\), and \(\mathcal P=0\). Use the curve

\[
A_\tau=\begin{pmatrix}1&-(r+1)\tau\\(r+1)\tau&1\end{pmatrix},
\qquad z_\tau=(\tau^2,\tau,1,0,0,0).
\]

Its two derivative matrices are proportional, so its correction is zero for **every** alternating two-form. Exact differentiation yields

\[
\boxed{\mathcal P(A_\tau,z_\tau)=
\frac23r(r+1)(r+2)\tau^4
\big[(r+1)(d_1\tau^2+d_2)-2b\big].}
\]

The tangent at zero is

\[
w=(0,-r-1,r+1,0;\;0,1,0,0,0,0).
\]

If \(\mathcal P\ge0\) everywhere, its full ordinary Hessian at the zero contact is PSD. The curve has zero second derivative of \(\mathcal P\), so \(w\) belongs to the Hessian kernel, exactly as in the frozen input proof.

The correction contributes zero to all four background components of this Hessian-times-tangent vector. This needs neither closedness nor polynomial coefficients. Indeed

\[
\omega_A(B_1,B_2)\big|_{z=e_{z_2}}=0
\quad\text{for every }A,
\]

and its \(z_1\)-derivative there is also zero: that derivative of \(B_1\) is \(e_{12}\), parallel to the base \(B_2=e_{12}\), whereas the base \(B_1\) is zero. Taking background derivatives preserves these identities.

For the uncorrected density, direct calculation gives

\[
\boxed{\big[D^2_{(A,z)}\mathcal P(I,e_{z_2})\,w\big]_{A}
=(0,0,-4b,0).}
\]

This identity is independent of \(r,d_1,d_2\) and the correction. The Hessian kernel condition therefore forces

\[
\boxed{b=0.}
\]

The output-skew term cannot enlarge the feasible heat-certificate class on this sharp acoustic stratum.

## 3. Consequences and scope

At \(r=1\), the normalized input diffusion is \(I\). The independent frozen proof in this directory excludes every \(C^2\) closed two-form correction for that diffusion. The reduction above therefore excludes every constant real strongly parabolic output-matrix operator in the same correction class at \(r=1\).

For general \(r>0\), this workstream proves the operator reduction and the necessary equation \(b=0\). Combining them with a separately audited all-positive-\(r\) input-diffusion no-go would exclude the complete constant-operator class on the whole positive branch. This extension's checker does not read or rely on that other workstream.

The result does not exclude variable-coefficient or nonlinear regularizations, nonlocal certificates, nonquadratic dependence on compatible jets, or direct quasiconvexity arguments. It does not prove failure of quasiconvexity.

Run `../../../.venv/bin/python verify_output_skew.py` here. The receipt is `OUTPUT_SKEW_VERIFICATION.json`; all checks are exact symbolic identities. The prior proof files are treated as immutable dependencies, and their hashes are recorded.
