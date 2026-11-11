# P1 human continuation: complete available final

Chat https://chatgpt.com/c/6af2bc39-2f58-83ec-b26b-3a99e1d2c0f2; user 23f9d084-1394-4d0d-ab14-64156528b48c: “Please continue from where you left off, solve the full problem”; final 18cbdd63-8aec-56c2-8bfd-13b9ece52839. Full governing question: work/astra-renewed-pro-programmes-20261103/P1_FULL_ORIGINAL_QUARTIC_AFTER_CALIBRATION_AND_NONLINEAR_CORE_PRO_20261111.txt, SHA-256 6d0e3de4a6f6f7d454735b3bc1adcc03b13e81e99672c4e7678f1f6b9e93f816.

The complete native-returned final has no truncation flag; no database-byte identity is claimed. Current expanded activity and three current helper panels were visible but have not yet been saved because the capture application timed out. The linked research packet has the same held library identity and was not collected; individual outputs were not downloaded.

## Complete final

**I have not solved the full problem.** This continuation produced neither a proof for every \(k>1/3\), every affine mean and every compatible gradient, nor an actual compatible field with a negative original gap. I cannot justify an affirmative or negative answer to the universal statement.

I preserved the complete arguments, exact data, code and computation receipts in:

- :chatgpt-content-reference{index="1"}[FULL_ENDPOINT_CONTINUATION_RESULTS.txt](sandbox:/workspace/scratch/21b466b728a1/FULL_ENDPOINT_CONTINUATION_RESULTS.txt)
- [Research packet, version 10](https://chatgpt.com/library?file_id=libfile_6d1aa4e4e9f08191bc79875c2b2752c0&account_id=personal)

The accepted unrestricted large-\(k\) proof remains unchanged. Below are the substantive results of this continuation and the precise reasons they do not complete the original inequality.

## 1. A stronger original-density reserve near the critical mean

There is a new compatible integral estimate at the mean \(I\). Write
\[
G=D\phi=
\begin{pmatrix}a&b\\c&d\end{pmatrix},
\qquad
s=\frac m2a+d,
\qquad
\eta=\frac{\ell n}{4},
\]
and define
\[
q_I(G)=\int_{\mathbb T^2}(s^2+\eta c^2),
\qquad
M=\|G\|_4,
\qquad
\mu_k=\frac{\ell\min(k^2,1)}{4(5k+1)}.
\]

The exact expansion of the **original** density is
\[
\begin{aligned}
\int J_k(I+G)-J_k(I)
={}&q_I(G)+\int J_k(G)\\
&+\int\left\{
-\eta a(a^2+c^2)
+s\left[-\frac{3n}{2}a^2+2as+\frac\ell2c^2-2bc\right]
\right\}.
\end{aligned}
\tag{1}
\]
Only the constant-coefficient determinant term has been integrated out.

Let \(C_*\) be the accepted finite constant in the scalar interpolation estimate, and set
\[
L_k=\frac{2C_*\sqrt{\max(1,\eta)}}{m\sqrt\eta}.
\]
The acoustic Fourier completion and that interpolation give
\[
\|a\|_{8/3}^{\,2}\le L_k M\sqrt{q_I(G)}.
\tag{2}
\]
If \(A_a=\|a\|_\infty<\infty\), then
\[
\|a\|_4
\le L_k^{1/3}A_a^{1/3}M^{1/3}q_I(G)^{1/6}.
\tag{3}
\]
This additional bounded-entry factor allows the critical cubic terms in (1) to be absorbed while retaining both quadratic and quartic reserves.

More explicitly, put
\[
\delta=\max(\|a\|_\infty,\|s\|_\infty),\qquad
B=\|b\|_\infty,\qquad
\nu=1-\frac B{\sqrt\eta}-\left(3+\frac2n\right)\delta.
\]
Whenever \(\nu>0\), the resulting bound is
\[
\boxed{
\begin{aligned}
\int J_k(I+G)-J_k(I)
\ge {}&\frac{\nu}{2}q_I(G)\\
&+\left[
\mu_k-L_k^4\left(
\frac{64\eta^3A_a}{27\nu^2}
+\frac{3125n^6A_a^4}{4\nu^5}
\right)\right]\|G\|_4^4 .
\end{aligned}}
\tag{4}
\]

Thus there are explicit positive \(\varepsilon_a,\delta_0\), given in the report, such that
\[
|b|\le\frac{\sqrt\eta}{2},\qquad
|a|\le\varepsilon_a,\qquad
|s|\le\delta_0
\]
imply
\[
\boxed{
\int J_k(I+G)-J_k(I)
\ge\frac18q_I(G)+\frac{\mu_k}{2}\|G\|_4^4 .
}
\tag{5}
\]
There is no additional pointwise bound on \(c\). All compatible frequencies and concentration are allowed within these entry constraints. The report also gives an exact simultaneous optimization of the two cubic losses that improves (4).

### Why this still does not give a global calibration

The reserve provides a lowered core satisfying constrained Jensen **at \(I\)**. That is enough for a target-specific projection proof, provided the core’s boundary planes lie globally below the normalized original density.

Those global inequalities remain unpaid. For the conservative explicit core, there is a concrete conflict at \(k=1\). Along
\[
D_1=\operatorname{diag}(2,-4),
\]
the normalized original polynomial is
\[
\widehat J_1(tD_1)=194t^4-8t^3.
\]
Its exact scalar convex envelope forces a positive boundary endpoint of the proposed core to satisfy
\[
(G_{11})_{\mathrm{boundary}}>\frac4{97}.
\]
But the explicit slab above has
\[
|G_{11}|\le\varepsilon_a\le\frac9{1024}<\frac4{97}.
\]
This conflict persists even if the entire proved quartic reserve is spent on that core. It excludes this conservative choice of touching data. The sharper extraction and other core constructions remain outside that conclusion.

The complete proof and independent audit are in :chatgpt-content-reference{index="2"}[CRITICAL_SLAB_RESERVE_AND_TARGET_CALIBRATION.md](sandbox:/workspace/scratch/21b466b728a1/projection_full_endpoint_continuation/CRITICAL_SLAB_RESERVE_AND_TARGET_CALIBRATION.md).

## 2. Finite affine Burkholder touching minorants are excluded

I investigated whether the supplied arbitrary-mean Burkholder theorem could give a direct touching minorant for \(J_k\). The quasiconvexity of the Burkholder integrand is used at its established scope. 

Write its \(p=4\) form as
\[
\mathcal U(F)=(3|h|-|p|)(|p|+|h|)^3,
\qquad
F_1=p+h,\quad F_2=i(p-h).
\]
The following obstruction was proved:

For every \(k>1/3\), no finite expression
\[
V(F)=c_0+P:F+\lambda\det F+C(F)
+\sum_{i=1}^{N}\alpha_i
\mathcal U\!\left(M_i+L_i(F-I)R_i\right),
\qquad \alpha_i>0,
\tag{6}
\]
where \(C\) is any finite convex function and all affine shifts and real matrices are arbitrary, can satisfy
\[
V\le J_k\quad\text{near }I,
\qquad
V(I)=J_k(I).
\tag{7}
\]

This includes affine shifts, so it goes beyond the previously excluded homogeneous polynomial representation.

The reason is the original density’s quadratic kernel and cubic behavior. Its quadratic Taylor term at \(I\) has a **unique** positive-semidefinite determinant translation, with kernel
\[
\mathcal P_k
=\operatorname{span}\{\operatorname{diag}(2,-m),E_{12}\}.
\]
On the first of these directions,
\[
\widehat J_k\!\left(t\operatorname{diag}(2,-m)\right)
=-2\ell n\,t^3
+J_k\!\left(\operatorname{diag}(2,-m)\right)t^4.
\tag{8}
\]

A touching positive sum in (6) would force every block’s translated quadratic form to vanish on this entire two-dimensional plane. The possible Burkholder backgrounds then behave as follows:

- At a regular background, the cubic vanishes on the translated quadratic kernel.
- At a nonzero conformal background, the symmetrized cubic is \(16P|h_H|^3\). The touching condition would force an invertible matrix transformation to map \(\mathcal P_k\) into a one-dimensional scalar line.
- A nonzero anticonformal background has a positive first-order cusp, incompatible with touching the smooth \(J_k\) from below.
- A zero background contributes only fourth order.
- Singular target/source transforms are convex and can be replaced by affine supports.

After these cases, no term pays the negative odd cubic in (8), giving the contradiction.

This theorem concerns **finite positive sums with fixed affine transformations**. Infinite concentration limits, unattained suprema and nonlinear graph constructions remain outside it. It supplies no original negative gradient.

The full proof is in :chatgpt-content-reference{index="3"}[AFFINE_BURKHOLDER_TOUCHING_OBSTRUCTION.md](sandbox:/workspace/scratch/21b466b728a1/construction_full_endpoint_continuation/AFFINE_BURKHOLDER_TOUCHING_OBSTRUCTION.md).

## 3. Partial row duality is exact, but the Hessian reduction does not follow

A different route uses the fact that \(J_k\) is strictly convex in either output row. For rows \(x,y\), define the partial conjugate
\[
\mathcal L_k(x,\sigma)
=\sup_y\{\sigma\cdot y-J_k(x,y)\}.
\]

For every fixed first-row gradient \(x=a+Df\), there is an exact attained duality:
\[
\boxed{
\begin{aligned}
\min_{g\in W^{1,4}_{\rm per}}
\int J_k(a+Df,b+Dg)
={}&
\max_{\substack{\sigma_0\in\mathbb R^2\\
v\in W^{1,4/3}_{\rm per}}}
\left\{
\sigma_0\cdot b
-\int\mathcal L_k(a+Df,\sigma_0+RDv)
\right\}.
\end{aligned}}
\tag{9}
\]
Here \(R\) is counterclockwise rotation by \(\pi/2\). Existence follows from row convexity and coercivity; equality follows from the actual minimizing constitutive stress and Fenchel equality. This is an analytic theorem, with no numerical optimizer or PDE solution assumed.

The original weighted minor remains:
\[
\sigma=D_yJ_k(F)
=\ell T_2(F)+\lambda(F)Rx.
\tag{10}
\]
Only the complete divergence-free stress pairing has its prescribed integral.

A simple original row minimizer shows why the conjugate potential cannot automatically be inserted into the adapted-Hessian theorem. At \(k=1\), take
\[
F=
\begin{pmatrix}1&\beta(y)\\0&1\end{pmatrix},
\qquad \int\beta=0.
\]
Its second-row stress is
\[
\sigma=(\beta^3/2-3\beta,\ 3),
\]
which is divergence free. Hence the constant second row is exactly the unique row minimizer for this first row. The full conjugate gradient is
\[
Dv=R^T\sigma=(3,\ 3\beta-\beta^3/2).
\tag{11}
\]

Two difficulties are explicit:

1. If \(\beta\in L^4\setminus L^{12}\), then \(Dv\notin L^4\). The natural \(W^{1,4/3}\) regularity in (9) cannot generally be upgraded to the quartic class.
2. Even for smooth \(\beta=\sin(2\pi y)\),
   \[
   \det D(u,v)=-\frac{\beta^3}{2}.
   \]
   The mixed map changes orientation, and no constant invertible left transformation makes its gradient an adapted Hessian.

A constant determinant translation replaces \(v\) by \(v-\lambda u\) and leaves this mixed Jacobian unchanged.

The constant-stress shortcut also fails: at \(k=1,A=I\),
\[
D^2_{xx}\mathcal L_1(e_1,(0,3))
=\operatorname{diag}(33/2,9/2),
\]
so the hoped-for concave Jensen comparison is absent. A successful use of (9) still needs a nonconstant compatible stress choice with a sufficiently large dual value.

The full derivation is in :chatgpt-content-reference{index="4"}[PARTIAL_ROW_LEGENDRE_ASSESSMENT.md](sandbox:/workspace/scratch/21b466b728a1/moment_full_endpoint_continuation/PARTIAL_ROW_LEGENDRE_ASSESSMENT.md).

## 4. A tempting weighted strengthening is false—with an explicit compatible sequence

I also checked whether the slab argument could be strengthened through
\[
q_I(G)\stackrel{?}{\ge}
c_k\int\frac{G_{11}^4}{|G|^2}.
\tag{12}
\]
This would have allowed a larger lowering along the non-rank-one kernel direction. It is false.

For every integer \(N\ge1\), take the smooth periodic potential
\[
\phi_{1,N}
=\frac{\sin(2\pi x)\sin(2\pi Ny)}{2\pi N},
\qquad
\phi_{2,N}
=\frac{m\cos(2\pi x)\cos(2\pi Ny)}{4\pi N^2}.
\]
Its actual gradient has the form
\[
G_N=
\begin{pmatrix}
a_N&b_N\\
-\dfrac{m}{2N^2}b_N&-\dfrac m2a_N
\end{pmatrix},
\]
where
\[
a_N=\frac{\cos(2\pi x)\sin(2\pi Ny)}N,
\qquad
b_N=\sin(2\pi x)\cos(2\pi Ny).
\]
Exactly,
\[
q_I(G_N)=\frac{\eta m^2}{16N^4}.
\]
Writing \(\kappa=1+m^2/4\), a direct estimate on the explicit set
\[
0\le x\le\frac16,\qquad
|\cos(2\pi Ny)|\le\frac1{2N}
\]
gives
\[
\int\frac{a_N^4}{|G_N|^2}
\ge\frac{3}{640\pi\kappa N^3}.
\]
Thus the ratio in (12) tends to zero.

**These fields have strictly positive original gaps at every affine mean.** Translation by \(1/(2N)\) in \(y\) sends \(G_N\) to \(-G_N\), so
\[
b_{G_N}=\int DJ_k(G_N)=0.
\]
Consequently the accepted exact moment identity gives
\[
\int J_k(A+G_N)-J_k(A)
=c_{G_N}+\frac12A:H_{G_N}A>0.
\]
This sequence decides only the proposed weighted auxiliary estimate. Its complete constants and finite witness threshold are in :chatgpt-content-reference{index="5"}[WEIGHTED_KORN_COUNTERSEQUENCE.md](sandbox:/workspace/scratch/21b466b728a1/projection_full_endpoint_continuation/WEIGHTED_KORN_COUNTERSEQUENCE.md).

## 5. Finite computational work and its limits

The nonlinear-entropy calculation was corrected to retain the first angular null direction at the acoustic degeneracy. Exact symmetry reduction leaves:

- \(16\) invariant closed-form coordinates;
- necessary affine conditions of rank \(7\), leaving \(9\) free parameters;
- a \(44\)-dimensional space in which every proposed square must lie.

Those reductions received an independent algebraic audit. The subsequent finite searches did not produce a certificate.

| Calculation | Declared finite budget | Actual work | Result |
|---|---:|---:|---|
| Restriction of the retained bilinear lift | One exact elimination, 30-second cap | \(0.0046\) seconds | Exact two-coefficient obstruction to the proposed cross-only restriction |
| Exact entropy-face reduction | 60-second cap; no optimizer | \(0.957\) seconds | Consistent necessary reduction |
| Corrected finite-column entropy search | Six LP calls, each capped at 20 seconds and 10,000 iterations | 2,893 iterations; \(4.528\) seconds | No positive nomination |
| Full \(44\times44\) PSD-Gram nomination at \(\sigma=3/8\) | 1,000 iterations; internal 90-second and external 120-second caps | 1,000 iterations; \(0.519\) seconds | No candidate meeting the stated tolerance |

No positivity or infeasibility theorem is inferred from floating residuals, eigenvalues or termination caps. No package, external solver, additional worker or resource was added. The exact inputs, outputs and receipts are preserved.

One further exact resource was obtained at \(k=1\):
\[
\boxed{
|S(F,F)|^2
=13J_1(F)
-\frac{(u-v+8j)^2+4(F_1\cdot F_2)^2}{8}
\le13J_1(F).
}
\]
The coefficient \(13\) is sharp pointwise. The correction and its cross term in the full compatible lift remain unpaid, so this does not establish the required \(18c_G\) bound.

## What remains unresolved

The continuation has not established
\[
\boxed{
b_G^T H_G^\dagger b_G\le2c_G
\quad\text{for every actual compatible }G=D\phi,
}
\]
and it has not constructed a compatible \(G\) violating it.

The stronger slab reserve, exact row duality and pointwise strain saving are available results. The global projection inequalities and the sharp compatible moment estimate are still missing. **The original unrestricted all-\(k\) question therefore remains unresolved in this work.**