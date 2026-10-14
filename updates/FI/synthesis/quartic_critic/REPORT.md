# Independent adversarial audit: FI positive-definite quartic packet

## Verdict and scope

I found no decisive internal counterexample to the stated algebraic claims, and the independent exact checks below reproduce the packet's displayed finite identities. This is scoped internal evidence, not external proof review. In particular, the packet does **not** prove that every rank-one-convex member of the complete nine-coefficient left-\(\mathrm{SO}(2)\u005c)-invariant quartic cone is quasiconvex, and it exhibits no negative compatible Jensen gap. The positive-definite averaged-Hessian sector remains open.

The most delicate proof obligations are the low-rank remainder classification, especially the rank-one distinguished-background reductions and the singular top-block cases, and the contact-shear theorem's elimination of the nonshear branch by an actual nearby rank-one acoustic test. The packet gives the reductions and exact formulas; my scripts independently recompute many identities but do not replace review of the analytic reductions or the source's normalizations.

## Reconstructed moment and nullspace foundation

For a planar homogeneous quartic (F) rank-one convex, reciprocity gives
\[
D^2F(A)[X,X]=D^2F(X)[A,A].
\]
Applying the non-strict one-quadric Finsler decomposition to the right side yields, for each (A),
\[
D^2F(A)[X,X]=P_A(X)+\lambda_A\det X,\qquad P_A\succeq0.
\]
For any finite-fourth-moment determinant-balanced law, (H=\mathbb E D^2F(X)\succeq0). If (A\in\ker H), then \(\mathbb E P_A(X)=0\), so the law is supported on \(U=\ker P_A\). At a null direction \(R\in U\) with \(\det R=0\), nonnegativity of \(D^2F(A+tY)[R,R]\) for both signs of (t) makes its linear coefficient vanish. Quartic tensor symmetry then gives cubic closure \(DF(X)[A]=0\) on the support: for indefinite \(\det|_U\), a quadratic vanishing on its null cone is a scalar multiple of that restriction, and tensor symmetry forces the scalar functional to vanish; for semidefinite restriction, determinant balance forces \(\det X=0\) almost surely and homogeneity gives the same conclusion. Thus \(b=\mathbb E DF(X)\in\operatorname{ran}H\), and the optimized background formula is attained:
\[
\inf_B\mathbb E[F(B+X)-F(B)]=c-\tfrac12 b^T H^\dagger b.
\]
This is a range/attainment result, not positivity of the minimized expression.

## Two-contact rigidity, including singular branches

Given \(C\succeq0\), \(\operatorname{tr}(J_{\det}C)=0\), rank at least two, and singular \(H_F(C)\), choose nonzero \(A\in\ker H_F(C)\). Then \(\operatorname{tr}(P_A C)=0\), so \(\operatorname{ran}C\subseteq\ker P_A\) and \(\operatorname{rank}P_A\le2\).

The rank-at-most-one remainder cases reduce to the exceptional convex/polyconvex class \(\mathcal E\). If the distinguished \(A\) is rank one, reciprocity makes \(D^2F(A)\succeq0\); its determinant multiplier must vanish because a nonzero determinant form has two negative directions on a two-dimensional subspace. Homogeneity and output-rotation covariance put both \(DF(A)\) and \(JDF(A)\) in the Hessian range, so a positive \(F(A)\) would force rank at least two. Hence the convex binary rank-one restriction has a zero direction; its fourth root is a seminorm, and the residual determinant terms are removed by the rank-one Hessian tests at \(e_{12}\) and \(e_{11}\).

If \(A\) is invertible, normalize it to \(I\) and write the PSD remainder in the conformal/anticonformal basis. A rank-at-most-one Schur remainder forces the two mixed first derivatives to vanish. The sign cases \(f<0,f=0,f>0\) are distinct: cubic closure rules out the negative case; in the zero case the rank-one segment gives nonnegativity before the Hessian tests remove the residual terms; the positive case reduces to \(fq^2+g|w|^4+\operatorname{Re}(\eta|w|^2z\bar w)\), and cubic closure removes \(\eta\). These are the rank-at-most-one cases, including a zero remainder.

For rank-two \(P_A\), the range of \(C\) is exactly the two-plane \(U=\ker P_A\), with positive definite covariance on that plane. Since \(\mathbb E\det X=0\), \(\det|_U\) can be indefinite or identically zero; a nonzero semidefinite restriction is impossible under positive definite covariance on \(U\). This is a useful scope restriction: the separate contact-shear theorem's rank-one-semidefinite tangent plane is not itself a balanced rank-two covariance face.

The remaining distinguished-background cases exhaust the two-contact proof:

| Distinguished background | Reconstructed elimination |
|---|---|
| Rank one, \(F(e_{11})=0\) | Degenerate binary seminorm case reduces to \(\mathcal E\). |
| Rank one, \(F(e_{11})>0\) | The positive \((a,c)\) Hessian block has rank two; the Schur complement gives \(q|_{\ker Q}=-L(b^2+d^2)/(4A_c)\). Balanced positive covariance forces \(L=0\); the remaining identities and one rank-one Hessian test reduce to a convex member of \(\mathcal P_2\). |
| Invertible, generic top block \(p,r>0\) and \(\det|_U\) indefinite | The difference of the \(k^3\) and \(kl^2\) coefficients of the closed cubic is \(-4\lambda^3a^3/(r^2p^3)\). Thus \(\lambda a=0\); either the determinant becomes negative definite or semidefinite, contradicting this branch. |
| Invertible, generic top block and \(\det|_U=0\) | The kernel equations force \(p=3a,r=a,\lambda=0\); full cubic closure fixes \(\eta=4f\), and the polynomial becomes \(f|z+w|^4+(g-f)|w|^4\in\mathcal P_2\). |
| Invertible, \(p=0,r>0\) | PSD forces the mixed coefficient to zero; the kernel contains an indefinite determinant plane, contradicting cubic closure and \(DF(I)[I]=4f\). |
| Invertible, \(r=0,p>0\) | The kernel is an indefinite plane. The two actual rank-one tests at \(z=iZ,w=iW\), \((\sigma,1)\), force both residual coefficients \(\tau,h\) to vanish, reducing to \(\mathcal E\), contrary to exact rank two. |
| Invertible, \(p=r=0\) | The kernel is the conformal plane, where determinant is positive definite, incompatible with balanced positive covariance. |

The converse constructs two independent rank-one contacts for each class in \(\mathcal P_2\); their covariance is balanced and their Hessian sum is singular. Thus the theorem's equivalences imply rank-two covariance coercivity outside \(\mathcal P_2\), without classifying every polyconvex quartic.

## Quantitative acoustic consequence

For a balanced covariance \(C\) of trace \(M_2\), a trace-zero congruence of \(J_{\det}\) admits an orthonormal zero-diagonal basis. This decomposes \(C=\sum_{j\le4}R_jR_j^T\) into at most four rank-one atoms. Under weights \(|R_j|^2/M_2\), independent unit atoms satisfy
\[
\mathbb E[1-(R:S)^2]=1-\operatorname{tr}[(C/M_2)^2]\ge\tau,
\quad \tau=1-\lambda_{\max}(C)/M_2.
\]
Since this random variable lies in \([0,1]\), the event that it is at least \(\tau/2\) has probability at least \(\tau/2\). Each individual rank-one Hessian is PSD by reciprocity. Combining the event with the definition of \(\mu_F\) gives
\[
\lambda_{\min}H_F(C)\ge\frac{M_2\tau}{4}\,\mu_F(\sqrt{\tau/2}).
\]
The strict positivity of \(\mu_F(s)\) for \(F\notin\mathcal P_2\) follows from the two-contact theorem plus compactness. It is nonconstructive and supplies no universal power law or efficient coefficient bound.

## Contact shear: exact theorem and limit

The full contact calculation leaves the \(r=a\) branch. The radical is the \(e_{12}\) line; its determinant-preserving condition is \(\operatorname{tr}(A^{-1}R)=0\), and the cubic \(DF(X)[A]\) on \(U\) is independent of the radical coordinate. The competing \(p=3a\) semidefinite branch is excluded by a joint acoustic perturbation. In the basis \(n,U_0\), the Schur coefficient is
\[
-\frac{(p-3r)^4}{324r^2V}<0\quad(p\ne3r,V>0).
\]
I independently checked the first-order coefficient vanishes and that the Schur-corrected background, tested in the nearby actual rank-one direction \(e_1\otimes(t,1)\), has this negative quadratic coefficient. The degenerate \(p=3r\) branch is handled separately as the totally null/polyconvex case.

For the surviving contact shear, \(\Psi_h(x)=x+v h(b\cdot x)\) has the stated exact inverse and determinant one when \(b\cdot v=0\). The change of variables transforms the residual integrand into a spatially varying right transform correlated with the residual. No averaging step follows from the identity. The pure shear has nonnegative gap, but shear straightening alone does not prove quasiconvexity or settle the residual interaction.

## Exact example and concentration sequence

The source's integrand is
\[
G=3(u+v-2q)^2+\tfrac{35}{24}u^2+q^2-\tfrac52qu,
\]
with unequal \(qu,qv\) coefficients, so it is outside the N797 one-parameter slice. The independent checker reconstructs the rank-one-convex SOS Gram block and its six positive leading minors, and reproduces \(G(I)=-1/24\), \(G(\operatorname{diag}(1,-1))=1271/24\), and the balanced nonpolyconvexity witness \(-1350/1297\). Rank-one convexity and nonpolyconvexity are certified in the source's algebraic scope; quasiconvexity is unresolved.

For the compatible pulse \(\rho^{1/2}\psi((x-x_*)/\rho)\), gradients are of size \(\rho^{-1/2}\) on area \(\rho^2\). Thus the pulse contributes \(\rho\), \(\sqrt\rho\), and order one to the second-, third-, and fourth-degree moments. Independent exact integration matches the displayed \(C_\psi,H_\psi,b_\psi,c_\psi\), confirms \(C_\psi,H_\psi\succ0\), and reproduces
\[
\mathcal L_G(D\varphi_\rho)\longrightarrow 80089/21313530>0,
\qquad \sqrt\rho(-H_\rho^{-1}b_\rho)\longrightarrow-566I/3759.
\]
The exact minimized gap is positive for every \(\rho>0\) by its displayed rational expression; there is no negative compatible gap. The sequence's fourth moments are bounded but not equiintegrable, and its Lipschitz constants diverge. Its gradients do not converge strongly in \(L^4\); this construction is not evidence for a uniformly bounded-gradient or equiintegrable extension.

## Distinct comparison with N800 and N797

The N800 integration-derived example fixes the polyconvex integrand \(F=q^2\) and uses smooth, uniformly bounded, fixed-bandwidth compatible gradients converging in every \(C^k\) norm. Its optimized **full Jensen gap** tends to zero while the gap at the limiting field equals \(1/4\); the minimizer escapes at scale \(1/\varepsilon\). Moments converge and there is no concentration. FI instead fixes the nonpolyconvex rank-one-convex \(G\), concentrates gradients, and proves discontinuity of the **minimized cubic loss term** while the full gap stays positive. The two are different quantities and different convergence regimes; neither is a QC counterexample.

N797 proves rank-one-convexity iff quasiconvexity only on \(F_\ell=u^2+v^2+4w^2+\tfrac72q^2+\ell q(u+v)\). Its symmetric coefficients of \(qu,qv\) exclude this FI \(G\), so that theorem cannot be transferred to the complete nine-coefficient cone.

The packet's own Section 8 separately states and proves the noncompatible balanced-law obstruction: determinant balance, rank-two covariance, bounded support, and \(H\succ0\) do not suffice for a Jensen conclusion. Its fixed-\(m\) family includes the later \(m=2\) parameterization audited separately in `delta/DELTA_REPORT.md`; that law remains noncompatible and is not a compatible counterexample.

## Adversarial conclusion

No overbroad transfer from determinant-balanced laws to gradients is justified; the source explicitly isolates the compatibility failure. No inference from nonlinear contact shear to full quasiconvexity is valid without controlling the variable-coefficient residual interaction. Bounded fourth moments do not imply equiintegrability, as the compatible concentration example itself demonstrates. The packet keeps these limits visible. Remaining proof review should focus on the analytic exhaustiveness of the low-rank cases and the coordinate-normalization passages; the finite checks do not certify those arguments or external correctness.
