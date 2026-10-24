# Multiple intercell rails: an exact spectrum and a range obstruction

Status: independent bounded derivation. This tests the one-intercell-link scalar model with multiple parallel same-site rails. It does not establish an advantage for a material or a new transport operation.

## 1. Exact two-rail ladder

Use two equal masses (m=M/2) per cell, a positive same-cell rung spring \(\kappa\), and positive intercell springs \(K_1,K_2\) on the two rails. Fix their sum \(K_1+K_2=K\), so the locked-cell mass and affine intercell stiffness match the rigid scalar comparator. Let \(\Delta=K_1-K_2\), \(s=\sin^2(q/2)\), and take the physical-coordinate Bloch stiffness matrix

\[
H(s)=\begin{pmatrix}\kappa+4K_1s&-\kappa\\-\kappa&\kappa+4K_2s\end{pmatrix}.
\]

The two squared frequencies are exactly

\[
\lambda_\pm(s)=\omega_\pm(s)^2
 =\frac{\kappa+2Ks\pm\sqrt{\kappa^2+4\Delta^2s^2}}{m}.
\]

Both increase with \(s\):
\[
\frac{d\lambda_-}{ds}
=\frac{2K-4\Delta^2s/\sqrt{\kappa^2+4\Delta^2s^2}}{m}
\ge \frac{2(K-|\Delta|)}m>0,
\]
and \(d\lambda_+/ds>0\). If \(\kappa>K\), the bands are separated and the full propagating-channel indicator is
\[
\chi_{\rm lad}=1_{[0,\Omega_a]}+1_{[\Omega_{o0},\Omega_{o\pi}]},
\]
where
\[
\Omega_a^2=\frac{\kappa+2K-\sqrt{\kappa^2+4\Delta^2}}m,
\quad \Omega_{o0}^2=\frac{2\kappa}m,
\quad \Omega_{o\pi}^2=\frac{\kappa+2K+\sqrt{\kappa^2+4\Delta^2}}m.
\]

The rigid locked-rail frequency is \(\Omega^2=4K/M=2K/m\). Since \(\lambda_-(s)=2Ks/m+O(s^2)\) as \(s\to0\), the long-wave acoustic stiffness depends on \(K_1,K_2\) only through their sum \(K\). For \(\Delta\ne0\), \(\Omega_a<\Omega\); the high optical band is exponentially Bose-suppressed when \(\kappa\) is large at fixed temperature. In particular,
\[
J_{\rm lad}-J_{\rm rigid}
=-\int_{\Omega_a}^{\Omega}g_\theta(\omega)\,d\omega
 +\int_{\Omega_{o0}}^{\Omega_{o\pi}}g_\theta(\omega)\,d\omega,
\]
and as \(\kappa\to\infty\) with \(K_1,K_2,m,\theta\) fixed and \(\Delta\ne0\),
\[
J_{\rm lad}-J_{\rm rigid}
=-g_\theta(\Omega)\frac{\Delta^2}{m\kappa\Omega}
 +O(\kappa^{-2})+O\!\left(\sqrt\kappa\,e^{-\sqrt{2\kappa/m}/\theta}\right)<0
\]
for all sufficiently large finite \(\kappa\). The matched symmetric ladder \(K_1=K_2=K/2\), with the same \(M,K,\kappa\), has acoustic band \([0,\Omega]\) and a separated positive optical band when \(\kappa>K\); hence its conductance is strictly above the rigid value. The asymmetric ladder therefore beats that conventional equal-rail split in this regime. This is a band-redistribution effect, not evidence that a multichannel device beats the scalar optimum.

## 2. The rank-one log moment changes, but the scalar optimum still dominates

The ladder's two ordinary band moments can be computed without approximation. Its trace moment is
\[
T_{\rm lad}=\int_0^\infty 2\omega\chi_{\rm lad}(\omega)\,d\omega
=\lambda_-(1)-\lambda_-(0)+\lambda_+(1)-\lambda_+(0)
=\frac{4K}{m}=\frac{8K}{M}.
\]
Its renormalized log moment relative to the rigid band is
\[
L_{\rm lad}=\int_0^\infty\frac{\chi_{\rm lad}(\omega)-1_{[0,\Omega]}(\omega)}{\omega}\,d\omega
=\frac12\log\!\left(\frac{\lambda_-(1)\lambda_+(1)}{\lambda_+(0)\Omega^2}\right)
=\frac12\log\!\left(1+\frac{4K_1K_2}{\kappa K}\right)>0.
\]
Thus the scalar rank-one null log moment does not extend unchanged to this genuine two-link spectrum. Its determinant has a nonzero \(s^2\) term:
\[
\det H(s)=4\kappa Ks+16K_1K_2s^2.
\]

Nevertheless, for \(\kappa>K\) the bands are disjoint, so \(\chi_{\rm lad}\) is still a \(0/1\) indicator. Compare it to the already-proved scalar one-link optimum \(\chi_*\) with backbone mass \(m_0=m=M/2\), total mass \(M\), and intercell spring \(K\). It has the same trace moment \(T_*=4K/m_0=8K/M=T_{\rm lad}\), and its dual \(R(\omega)=g_\theta(\omega)+\lambda/\omega+2\mu\omega\) has \(\lambda<0,\mu>0\), with \(\chi_*=1\) precisely where \(R<0\). Pointwise,
\[
\int R(\chi_{\rm lad}-\chi_*)\,d\omega\ge0.
\]
Using \(R=g+\lambda/\omega+2\mu\omega\), equal trace moments, and \(L_*=0\),
\[
J_{\rm lad}-J_*
=\int R(\chi_{\rm lad}-\chi_*)\,d\omega-\lambda L_{\rm lad}>0.
\]
So this exact ladder violates the rank-one spectral identity but does not beat the full rank-one optimum in the separated-band regime. The rank-one comparison fixes \(M,K,m_0\) and lets the one-link design choose its own internal spring; it is an unconstrained performance benchmark, not a matched total internal-spring budget. No conclusion is made for overlapping bands, where the ladder's channel multiplicity can be two and the pointwise \(0/1\)-indicator comparison no longer applies.

## 3. Static compliance is visible in the same construction

For the same-cell rail difference \(Y=x_1-x_2\), the force pair is \((1,-1)\). Direct inversion of \(H(s)\) gives
\[
(1,-1)H(s)^{-1}(1,-1)^T
=\frac1{\kappa+4K_1K_2s/K}.
\]
The cell-averaged static compliance is therefore
\[
C_Y=\frac1{2\pi}\int_{-\pi}^{\pi}
\frac{dq}{\kappa+(4K_1K_2/K)\sin^2(q/2)}
=\frac1{\sqrt{\kappa(\kappa+4K_1K_2/K)}}.
\]
For large \(\kappa\), \(C_Y\sim1/\kappa\), while the conductance gain relative to the rigid comparator above is also only order \(1/\kappa\). Their leading ratio is finite:
\[
\frac{J_{\rm rigid}-J_{\rm lad}}{C_Y}\longrightarrow
g_\theta(\Omega)\frac{\Delta^2}{m\Omega}.
\]
The Gibbs inequality gives \(\operatorname{Var}(Y)\ge k_BT C_Y\). Thus the large-rung limit does not create a finite transport improvement at vanishing compliance.

## 4. Uniform low-temperature range bound for any number of parallel rails

There is also a direct bound that does not use a rank-one band indicator. Consider any finite cell with positive masses \(m_j\), total \(M\), connected positive internal springs, and same-site nearest-cell rail springs \(K_j\ge0\) with \(\sum_jK_j=K>0\). Let
\[
D(q)=D_0+4s(q)B,\qquad B=\operatorname{diag}(K_j/m_j),\qquad
\Omega^2=4K/M.
\]
Write \(a=\sqrt{\lambda_{\min}(D(\pi))}\). For a normalized lowest-mode polarization \(x_j(q)\), use the normalization \(\sum_jm_j|x_j|^2=1\). Since \(D_0\ge0\) and \(D(q)\preceq D(\pi)\),
\[
4s\sum_jK_j|x_j(q)|^2\le\omega_0(q)^2\le a^2.
\]
Define the rail-weighted displacement \(X_K(q)=\sum_jK_jx_j(q)/K\). Jensen's inequality yields
\[
\sqrt M|X_K(q)|\le\frac{a}{\Omega\sqrt{s}}.
\]
For \(s\ge1/2\), if \(a\le\Omega/(2\sqrt2)\), this is at most \(1/2\). The normalized mode then has
\[
\left(\sum_jm_j|x_j-X_K|^2\right)^{1/2}
\ge \left(\sum_jm_j|x_j|^2\right)^{1/2}-\sqrt M|X_K|
\ge\frac12.
\]
The half-zone \(s\ge1/2\) occupies half the Brillouin zone. Summing the quantum Gibbs covariance over the lowest branch there, and using \(\hbar\coth(\hbar\omega/(2k_BT))/(2\omega)\ge k_BT/\omega^2\), gives the per-cell bound
\[
\mathcal V_K:=\sum_jm_j\operatorname{Var}(x_j-X_K)\ge\frac{k_BT}{8a^2}.
\]
If every site's RMS displacement relative to a chosen backbone site is at most \(d\), the rail average is a convex combination of the site displacements, so \(\|x_j-X_K\|_2\le2d\) and \(\mathcal V_K\le4Md^2\). Consequently,
\[
a\ge\min\!\left\{\frac{\Omega}{2\sqrt2},
\sqrt{\frac{k_BT}{32Md^2}}\right\}.
\]

The lowest Bloch branch is continuous from zero at \(q=0\) to \(a\) at \(q=\pi\); hence the bulk has at least one propagating channel throughout \([0,a]\) (isolated band-edge velocities do not affect the conductance integral). Therefore
\[
J\ge\int_0^a g_\theta(\omega)\,d\omega,
\qquad
J_{\rm rigid}-J\le\int_a^\Omega g_\theta(\omega)\,d\omega.
\]
At fixed \(M,K,d\) and low temperature, the lower cutoff is at least order \(\sqrt{T}\), while \(\theta=k_BT/\hbar\) is order \(T\). Using \(g_\theta(\omega)\le4(\omega/\theta)^2e^{-\omega/\theta}\) once \(\omega/\theta\) is large, the normalized deficit is bounded by a polynomial in \(T^{-1/2}\) times \(\exp[-c/\sqrt T]\). This is uniform in the number of rails, their positive mass allocation, and their retuning, under the stated same-site rail topology and uniform relative-displacement cap.

## 5. Nearest-cell cross-node springs: an affine-resource extension

The diagonal-rail step above is not needed if one counts the total positive
spring constant crossing a cell boundary. Assume the internal cell springs
connect every node, so the only zero-frequency mode is the uniform translation
at \(q=0\). Let an edge \(e=(j,k)\) join node
\(j\) in cell \(n\) to node \(k\) in cell \(n+1\), with stiffness
\(\kappa_e>0\), and assume only nearest-cell edges. Set
\[
K_{\rm aff}=\sum_e\kappa_e,\qquad
\Omega_{\rm aff}^2=4K_{\rm aff}/M.
\]
This is the affine (unrelaxed) spring-sum resource: if all cell displacements
are equal to \(X\), a Bloch phase \(q\) puts edge energy
\(4sK_{\rm aff}|X|^2\). It need not equal the relaxed long-wave stiffness.

For a normalized Bloch mode \(x_j(q)\), let
\[
E_q(x)=\sum_e\kappa_e|x_j-e^{iq}x_k|^2.
\]
Let \(a=\max_q\sqrt{\lambda_{\min}(D(q))}\), the maximum of the lowest
frequency branch. On every \(q\), the lowest mode has total energy at most
\(a^2\); since the cell-internal energy is nonnegative, \(E_q(x)\le a^2\).
The translation trial vector gives \(a\le\Omega_{\rm aff}\). Write the
normalized polarization as \(x_j=X+y_j\), where
\(X=\sum_jm_jx_j/M\), so that
\[
h^2+V=1,\quad h=\sqrt M|X|,\quad
V=\sum_jm_j|y_j|^2.
\]
For the edge vector of the uniform part,
\(\|E_q(X)\|_\kappa=2\sqrt{sK_{\rm aff}}|X|\). The triangle inequality
and \(|y_j-e^{iq}y_k|^2\le2(|y_j|^2+|y_k|^2)\) imply
\[
2\sqrt{s}\,h\le \frac{2a}{\Omega_{\rm aff}}+\sqrt{2E},
\qquad
E=\frac M{K_{\rm aff}}\sum_e\kappa_e(|y_j|^2+|y_k|^2).
\]
On the half-zone \(s\ge1/2\), if
\(a\le\Omega_{\rm aff}/(2\sqrt2)\), this gives
\(h\le1/2+\sqrt E\). Were both \(V<1/8\) and \(E<1/8\), normalization
would require \(h>\sqrt{7/8}\), while the last inequality gives
\(h<1/2+\sqrt{1/8}\), a contradiction. Thus
\[
V+E\ge1/8
\]
for the lowest mode throughout that half-zone.

Integrating its Gibbs covariance over half the Brillouin zone gives
\[
\mathcal F:=\sum_jm_j\operatorname{Var}(x_j-X)
+\frac M{K_{\rm aff}}\sum_e\kappa_e\big(\operatorname{Var}(y_j)+\operatorname{Var}(y_k)\big)
\ge\frac{k_BT}{16a^2}.
\]
If every site is within RMS distance \(d\) of a chosen backbone site, then
each \(y_j=x_j-X\) has RMS at most \(2d\). Hence the first term is at most
\(4Md^2\), while the edge term is at most \(8Md^2\), and
\[
a\ge\min\!\left\{\frac{\Omega_{\rm aff}}{2\sqrt2},
\sqrt{\frac{k_BT}{192Md^2}}\right\}.
\]
The lowest branch is continuous, includes zero at \(q=0\), and reaches its
maximum \(a\); its bulk passband therefore covers \([0,a]\), up to isolated
zero-velocity band edges. This gives \(J\ge\int_0^a g_\theta\) and the same
exponentially small low-temperature bound on a fixed-range conductance deficit.

This cross-node extension is conditional on positive nearest-cell springs and
a fixed \(K_{\rm aff}\). Because internal relaxation can make effective
long-wave stiffness strictly smaller than \(K_{\rm aff}\), it does not by
itself prove the same bound under an effective-stiffness budget alone.

## 6. Scope and resource interpretation

The exact ladder provides a two-link spectrum and an additional determinant/log moment; the rank-one equality itself is special. The separate range bound shows that this spectral departure does not evade low-temperature suppression for same-site parallel rails. The nearest-cell cross-node argument extends the low-temperature range obstruction when the counted affine spring sum is fixed.

The unconstrained one-link optimum used above is a stronger spectral benchmark at the same \(M,K,m_0\), not a comparison with a matched total internal-spring budget: \(\kappa\) is separately tunable in the ladder. Neither the parallel-rail nor nearest-cell cross-node bound covers longer-range links, vector elasticity with rotations, anharmonicity, finite contacts, or a fabricated device.
