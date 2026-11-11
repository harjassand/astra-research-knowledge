# P1; chat https://chatgpt.com/c/6af2bc39-2f58-83ec-b26b-3a99e1d2c0f2; user a92a0a27-ac3f-42cc-908f-ee838c12a798; assistant 22c8b212-5c57-580f-8632-dbd112beb322; question P1_FULL_ORIGINAL_QUARTIC_AFTER_MIXED_CURVATURE_PRO_20261111.txt.

Native final returned without truncation flag. Current expanded activity and full helper panels are unsaved. Individual linked files were not collected; no ZIP visible in the inspected response, other availability unknown. Native reader text is not a database-byte identity claim.

## Full final

**I have not resolved the full original inequality.** This continuation produced an attained nonlinear compatible stress projection and a geometric convergence theorem for conditional row minimization. It also produced an exact counterexample to convexity of the reduced first-row functional. The bounded compatible search found no negative candidate to certify.

The complete proofs, independent audits, exact identities, and computation records are saved in:

- :chatgpt-content-reference{index="0"}[MIXED_CURVATURE_CONTINUATION_RESULTS.txt](sandbox:/workspace/scratch/21b466b728a1/quartic_research_packet/MIXED_CURVATURE_CONTINUATION_RESULTS.txt)
- [Updated complete research packet](https://chatgpt.com/library?file_id=libfile_6d1aa4e4e9f08191bc79875c2b2752c0&account_id=personal)

The accepted unrestricted large-\(k\) theorem remains unchanged.

## 1. The mixed remainder now gives an attained nonlinear stress selection

Fix an actual first gradient row
\[
x=a+Df
\]
and an actual candidate second row
\[
y=b+Dg_0.
\]
Throughout this construction, the first row stays fixed. Define
\[
H=D_y^2J_k(x,y),\qquad s=D_yJ_k(x,y),
\]
and write
\[
\gamma_k=\frac{\ell\min(k^2,1)}{24n},
\qquad
g_k=\frac{3\gamma_k}{5},
\qquad
\mathcal F_H(u)=\frac1{12}u^THu+g_k|u|^4.
\]
The supplied mixed-curvature estimate says that \(\mathcal F_H\) is a lower bound for the **original** row Bregman remainder.

Consider the compatible scalar variational problem
\[
\min_{\substack{\psi\in W^{1,4}_{\rm per}\\ \int\psi=0}}
\int_{\mathbb T^2}
\left[\mathcal F_H(D\psi)+s\cdot D\psi\right].
\tag{1}
\]
It has a unique minimizer. If \(u_*=D\psi_*\), its Euler equation gives
\[
\boxed{
\tau_*
=s+\frac16Hu_*+4g_k|u_*|^2u_*,
\qquad \operatorname{div}\tau_*=0.
}
\tag{2}
\]

This is a compatible nonlinear selection of the stress. Its mean is retained.

The construction works for the natural rough coefficients
\[
H\in L^2,\qquad H\ge0,\qquad s\in L^{4/3}.
\]
For existence, the quartic term is coercive, and the quadratic term is the squared norm of the bounded map
\[
L^4\ni u\longmapsto H^{1/2}u\in L^2.
\]
Strict quartic convexity gives uniqueness. No positive lower bound on the eigenvalues of \(H(x)\) is needed.

Moreover, this stress solves the complete dual minimization for the chosen lower model:
\[
\boxed{
\begin{aligned}
\mathfrak D(H,s)
&:=\min_{\operatorname{div}\tau=0}
  \int\mathcal F_H^*(s-\tau)\\
&=-\min_\psi\int\left[\mathcal F_H(D\psi)+s\cdot D\psi\right]\\
&=\int\left[\frac1{12}u_*^THu_*+3g_k|u_*|^4\right].
\end{aligned}}
\tag{3}
\]

The proof uses Fenchel equality at \(-u_*\), together with the solenoidal-gradient pairing. In particular, the signs in (3) account for the fact that the model lies **below** the original Bregman remainder.

### Finite trials certify the optimal defect

For any actual trial gradient \(u=D\psi\), set
\[
r=P_{\rm grad}\left(s+\frac16Hu+4g_k|u|^2u\right),
\]
and
\[
L(u)=-\int\left[\mathcal F_H(u)+s\cdot u\right].
\]
Then
\[
\boxed{
\max\{0,L(u)\}
\le\mathfrak D(H,s)
\le L(u)+C_{g_k/3}\int|r|^{4/3}.
}
\tag{4}
\]
Thus the optimal nonlinear stress defect can be enclosed using compatible trial potentials and a certified natural-exponent residual.

For rational finite Fourier data, \(r\) is finite Fourier, \(L(u)\) is an exact rational Laurent constant coefficient, and the last integral is bounded by the supplied Bernstein/cube-bisection procedure. No pointwise conjugate optimizer is required. The full proof and cost accounting are in :chatgpt-content-reference{index="1"}[NONLINEAR_MIXED_STRESS_PROJECTION.md](sandbox:/workspace/scratch/21b466b728a1/projection_mixed_curvature_continuation/NONLINEAR_MIXED_STRESS_PROJECTION.md).

## 2. The projection gives paid descent of the original energy, with a geometric conditional rate

The lower model alone would not justify taking a full update \(y\mapsto y+u_*\). A separate upper estimate on the original remainder pays a smaller step.

Put
\[
\Gamma_k=\frac{\ell\max(k^2,1)}{8n}.
\]
Along a row line,
\[
B_F(tu)=\frac12t^2h_F(u)+t^3C_F(u)+t^4q_k(u).
\]
Convexity of that quartic line gives the discriminant bound
\[
|C_F(u)|^2\le\frac43h_F(u)q_k(u).
\]
Consequently,
\[
B_F(tu)\le t^2h_F(u)+\frac53t^4\Gamma_k|u|^4.
\]
For
\[
0<t\le
\min\left\{\frac1{12},
\left(\frac{3g_k}{5\Gamma_k}\right)^{1/3}\right\},
\]
this implies the useful inequality
\[
\boxed{B_F(tu)\le t\mathcal F_H(u)}
\tag{5}
\]
for **every** trial \(u\).

Let
\[
E=\int J_k(x,y),\qquad
m=\min_g\int J_k(x,b+Dg),\qquad
\Delta=E-m.
\]
The compatible update \(y_{\rm next}=y+tu\) therefore satisfies
\[
E_{\rm next}\le E-tL(u).
\tag{6}
\]
The original lower-model certificate gives
\[
\Delta\le\mathfrak D(H,s).
\]
If the finite residual certificate pays
\[
\mathfrak D(H,s)-L(u)\le\eta,
\]
then (6) yields
\[
\boxed{
\Delta_{\rm next}\le(1-t)\Delta+t\eta.
}
\tag{7}
\]

For exact model steps,
\[
E_n-m\le(1-t)^nE_0.
\tag{8}
\]
The original row Bregman inequality at the conditional minimizer \(y_*\) also gives
\[
\gamma_k\|y_n-y_*\|_4^4\le E_n-m,
\]
and hence
\[
\boxed{
\|y_n-y_*\|_4
\le
\left(\frac{E_0}{\gamma_k}\right)^{1/4}(1-t)^{n/4}.
}
\tag{9}
\]

This is global in the amplitude of the fixed first row and the initial second row. It is a convergence theorem to the **conditional row minimizer**.

### A finite implementation with an explicit outer count

For rational data, one admissible rational choice is
\[
t=\min\left\{\frac1{12},\frac{3g_k}{5\Gamma_k}\right\}.
\]
Indeed,
\[
0<\frac{3g_k}{5\Gamma_k}\le\frac3{25}<1,
\]
so this choice satisfies the required cubic inequality.

To achieve a requested rational \(L^4\) row accuracy \(\varepsilon>0\), use the fixed inner model-gap tolerance
\[
\eta=\frac{\gamma_k\varepsilon^4}{2},
\]
and choose an integer \(N\) by rational power comparisons so that
\[
(1-t)^NE_0\le\frac{\gamma_k\varepsilon^4}{2}.
\]
Iteration of (7) then proves
\[
\|y_N-y_*\|_4\le\varepsilon.
\]

Each inner model gap is certified using (4). Rational Fourier density and strong \(L^4\) continuity of the model stress prove that its finite enumeration terminates. The Bernstein construction supplies explicit operation and bit bounds for every attempted certificate. The number of outer steps is known before the inner searches begin; **no a priori bound on their successful enumeration stages is supplied**.

No such iteration was executed in this continuation. This is a proved finite procedure, not a reported PDE solve. Its attainment, residual signs, rough-space passages, descent constants, and geometric recurrence passed an independent :chatgpt-content-reference{index="2"}[analytic audit](sandbox:/workspace/scratch/21b466b728a1/projection_mixed_curvature_continuation/CONSTRUCTION_NONLINEAR_STRESS_AUDIT.md).

The remaining issue is that the limiting value \(m\) has not been shown to satisfy
\[
m\ge J_k(a;b)
\]
for every first row.

## 3. The reduced first-row energy is rigorously nonconvex

I investigated whether the exact row minimization might leave a convex scalar functional, which would close the remaining comparison by a further Jensen argument. That proposed route fails.

At \(k=1\), define
\[
m(f)=\min_g\int_{\mathbb T^2}
J_1(e_1+Df,e_2+Dg).
\]
Take
\[
f_0(x,y)=\frac{\sin(4\pi x)}{8\pi},
\]
so that
\[
F_0=I+D(f_0,0)
=\begin{pmatrix}
1+\frac12\cos(4\pi x)&0\\
0&1
\end{pmatrix}.
\]
Its second-row constitutive stress has first component zero and second component depending only on \(x\). It is therefore exactly solenoidal. Row convexity proves that the constant second row is the actual conditional minimizer.

Thus its value is known exactly:
\[
m(f_0)-J_1(I)=\frac{515}{1024}.
\tag{10}
\]

Now define the actual periodic variations
\[
\eta(y)=\frac{\sin(2\pi y)}{2\pi},
\qquad
\zeta(x,y)=\frac{\sin(4\pi x)\cos(2\pi y)}{4\pi},
\qquad
Z=D(\eta,\zeta).
\]
Direct integration of the original Hessian gives
\[
\boxed{
\int D^2J_1(F_0)[Z,Z]=-\frac{157}{512}.
}
\tag{11}
\]
This concerns a nonconstant compatible background; it does not contradict the accepted local result at constant affine backgrounds.

The finite-amplitude calculation is also exact. For
\[
F_\pm=F_0\pm\frac12Z,
\]
one has
\[
\int J_1(F_\pm)-J_1(I)
=\frac{64161}{131072}>0,
\tag{12}
\]
while
\[
\int J_1(F_+)+\int J_1(F_-)-2m(f_0)
=-\frac{1759}{65536}.
\]
Since these second rows are admissible competitors for their respective conditional problems,
\[
\boxed{
m(f_0+\eta/2)+m(f_0-\eta/2)-2m(f_0)
\le-\frac{1759}{65536}<0.
}
\tag{13}
\]

Therefore **the functional obtained by actual conditional row minimization is not convex in the first potential**.

The proof also establishes strong \(L^4\) continuity of the minimizing rows along this line and the corresponding envelope derivative. Consequently, the proposed integrated monotonicity between arbitrary conditional minimizers is false. For some actual pair of such minimizers, the signed constitutive weighted-minor secant outweighs the positive monotone-companion secant.

This does not decide the weaker comparison with the affine mean. In particular, (12) gives positive gaps for the explicit competitors, while the signs of the two unknown conditional minima in (13) were not computed.

### Mean elimination does not turn this explicit family into a counterexample

The construction was checked for the complete family
\[
\begin{aligned}
f_0(x)&=\frac{t\sin(2\pi Nx)}{2\pi N},\\
\eta(y)&=\frac{\sin(2\pi y)}{2\pi},\\
\zeta_{t,N}(x,y)&=\frac{t\sin(2\pi Nx)\cos(2\pi y)}{\pi N},\\
G&=D(f_0+\varepsilon\eta,\varepsilon\zeta_{t,N}),
\end{aligned}
\]
with arbitrary real \(t,\varepsilon\) and positive integer \(N\).

At \(k=1\), every nonzero field in this family has a **strictly positive original gap for every affine mean**.

The proof eliminates the mean exactly. With
\[
T=t^2,\qquad E=\varepsilon^2,\qquad L=N^{-2},
\]
the minimized gap is a rational expression with positive denominator. Its numerator has nonnegative coefficients; the only three coefficient groups altered by the Schur subtraction are
\[
\begin{array}{c|l}
T^3E^2&744+1128L\\
T^2E^3&888+552L\\
T^3E^3&800+8064L+1312L^2,
\end{array}
\]
and the \(T^4\) coefficient is \(36\). Boundary cases are scalar shears.

This was an analytic polynomial calculation, with no numerical or symbolic search. The complete proof is in :chatgpt-content-reference{index="3"}[REDUCED_ROW_NONCONVEXITY_AND_EXACT_MEAN_TEST.md](sandbox:/workspace/scratch/21b466b728a1/moment_mixed_curvature_continuation/REDUCED_ROW_NONCONVEXITY_AND_EXACT_MEAN_TEST.md). Its family certificate does not include the unknown minimizing second rows defining \(m(f_0\pm\eta/2)\).

## 4. The lower endpoint has an exact mean-regression expansion

For an actual compatible \(G\), let
\[
q=\operatorname{cof}G,\qquad
C=\int q\otimes q,\qquad
r=\int(\det G)q,\qquad
d=\int(\det G)^2.
\]
At \(k=1/3\), the original density is \((\det F)^2\). Its gap is exactly
\[
V(A)=d+2r:A+A:CA.
\]
The range condition is immediate: \(Z\in\ker C\) implies \(Z:q=0\) almost everywhere, hence \(r:Z=0\). Therefore
\[
\boxed{
V_*=\min_A V(A)=d-r:C^\dagger r\ge0.
}
\tag{14}
\]
Equality means that a minimizing mean makes the **total determinant** constant.

When \(C>0\), set
\[
A_0=-C^{-1}r,\qquad
q_0(A)=\Delta Q_0(A,G),\qquad
z=\nabla_Aq_0(A_0).
\]
The mean minimizing the original gap is analytic near the endpoint and satisfies
\[
A(h)=A_0-\frac32hC^{-1}z+O(h^2),
\qquad h=k-\frac13.
\]
The optimized gap has the expansion
\[
\boxed{
\begin{aligned}
\min_A\Delta J_{1/3+h}(A,G)
={}&V_*+3h\,q_0(A_0)\\
&+h^2\left[
\frac38X(A_0)-\frac{27}{128}D(A_0)
-\frac94z:C^{-1}z
\right]+O(h^3).
\end{aligned}}
\tag{15}
\]

The last term records the benefit of changing the affine mean. Its derivation retains the determinant-variance cost: the mean displacement contributes \(+\frac94z:C^{-1}z\) through \(V\) and \(-\frac92z:C^{-1}z\) through the first-order endpoint term, leaving the displayed negative correction.

This is a fixed-field expansion, with no uniformity as \(C\) degenerates. No actual field satisfying a resulting negative criterion has been supplied. The derivation and independent check are in :chatgpt-content-reference{index="4"}[ENDPOINT_MEAN_REGRESSION.md](sandbox:/workspace/scratch/21b466b728a1/construction_mixed_curvature_continuation/ENDPOINT_MEAN_REGRESSION.md) and its :chatgpt-content-reference{index="5"}[audit](sandbox:/workspace/scratch/21b466b728a1/moment_mixed_curvature_continuation/ENDPOINT_MEAN_REGRESSION_AUDIT.md).

## 5. The new compatible search produced no negative nomination

The single bounded investigation used actual continuous periodic quadratic finite-element potentials:

| Item | Actual specification or outcome |
|---|---|
| Coarse torus mesh | \(4\times4\) squares, 32 triangles |
| Degrees of freedom | 64 scalar nodes; 128 free vector nodal values |
| Gradient within each triangle | Affine |
| Integration rule | Rational 12-point rule, exact through degree four |
| Exact integration preflight | All 15 monomial checks passed |
| Parameter interval | \(1/3+2^{-16}\le k\le4\) |
| Starts | Six deterministic fresh starts |
| Objective evaluations | 1,524, including three preflight calls |
| Termination | Every start reached its 250-iteration cap |
| Conditioning or solve rejections | None |
| Negative nominations below \(-10^{-7}\) | None |
| Exact rational certification attempts | Zero |
| Nomination time | 2.0649 seconds |
| Total bounded execution time | 2.6804 seconds |

The affine mean was eliminated analytically at each evaluation. All nodal values were free; the fields were not constrained to remain in the initial shear or streamfunction classes.

The smallest floating gap ratio was approximately \(0.0001802003\), and every best record used the lower parameter bound. **Those values are not exact positive signs or certificates of optimality.** No universal conclusion follows from the absence of a negative nomination.

The actual compatible realization, finite caps, precision, code, records, and unused rational-certification contingency are retained in :chatgpt-content-reference{index="6"}[P2_REALIZATION_AND_SEARCH_SCOPE.md](sandbox:/workspace/scratch/21b466b728a1/construction_mixed_curvature_continuation/P2_REALIZATION_AND_SEARCH_SCOPE.md) and the packet.

## 6. Potential-dependent compensation is valid, but leaves the missing work unchanged

There is also an exact nonlinear stress freedom. At mean \(I\), write
\[
u=x_1+f,\qquad v=x_2+g.
\]
For a smooth one-periodic \(\Lambda\), its primitive shows that
\[
\tau_\Lambda=\Lambda(u)RDu
\]
is periodic and solenoidal, with mean \(\overline\Lambda e_2\). Hence
\[
\int\Lambda(u)\det D(u,v)=\overline\Lambda.
\tag{16}
\]
At a conditional row minimizer with stress \(s\),
\[
\int\Lambda(u)s\cdot Du
=\overline\Lambda\int s\cdot Du.
\tag{17}
\]
These identities do not require \(u\) to be invertible or its level sets to form a regular foliation.

The literal period contract can also be arranged for any invertible real mean by a constant left rotation: the first mean row becomes \((a,0)\), and one uses \(\Lambda_0(u/a)\). This changes no source lattice.

However, the constitutive coefficient \(\lambda(F)\) is gradient dependent. The exact identity
\[
\int[\lambda(F)-\Lambda(u)]RDu\cdot Dg
=
\int\lambda(F)RDu\cdot Dg
\tag{18}
\]
shows that this gauge leaves the missing Euler work unchanged. Its subtracted part is precisely a solenoidal-gradient pairing. The complete scope is recorded in :chatgpt-content-reference{index="7"}[POTENTIAL_DEPENDENT_EULER_IDENTITIES.md](sandbox:/workspace/scratch/21b466b728a1/moment_mixed_curvature_continuation/POTENTIAL_DEPENDENT_EULER_IDENTITIES.md).

## What remains unresolved

The new stress selection optimizes a valid lower model, and the damped updates converge geometrically to each conditional row minimum. The exact nonconvexity result shows that this reduction cannot be followed by an unrestricted convexity argument in the first row.

The required weaker statement remains
\[
\min_g\int J_k(a+Df,b+Dg)\ge J_k(a;b)
\]
for every first-row potential, every affine mean, and every \(k>1/3\). Equivalently, the full shared moment inequality is still
\[
\boxed{
b_G^T H_G^\dagger b_G\le2c_G
\qquad\text{for every actual compatible }G.
}
\]

Neither that universal comparison nor a rigorously negative compatible original gap was obtained in this continuation.