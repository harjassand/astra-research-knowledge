# A uniform obstruction to unconstrained polynomial-square certificates

27 October 2026. This continues the same all-copy qutrit Werner target. The target remains unresolved. The auxiliary PPT states below are **dual witnesses against a certificate cone**, not admissible negative rank-two Werner witnesses.

## 1. The shared-qubit representation retains the full target

Write \(O_d=|\Omega_d\rangle\langle\Omega_d|\), \(P_d=O_d/d\), \(Q_d=I-P_d\), and

\[
K=I_9-\tfrac12O_3,\qquad W_n=K^{\otimes n}\otimes O_2.
\]

The ordering here groups each physical Alice--Bob pair together, then the auxiliary Alice--Bob qubits. Regard \(W_n\) bipartitely across \((A_1\cdots A_n a):(B_1\cdots B_n b)\), and let \(\Gamma\) transpose the entire second party.

For arbitrary complex \(3^n\)-by-two matrices \(U,V\), put \(a=\operatorname{vec}U\), \(b=\operatorname{vec}\bar V\), using the corresponding factor regrouping. Contracting the auxiliary \(O_2\) gives

\[
f_n(U,V):=q_n(UV^*)=\langle a\otimes b,W_n(a\otimes b)\rangle.\tag{1}
\]

Every rank-at-most-two \(C\) factors as \(UV^*\). Thus block positivity of \(W_n\) for every \(n\) is exactly the full target. At \(n=1\), this positivity is already established by the rank-two trace inequality. We do not assume it at general \(n\).

The stage-one invariant \(\Gamma_n\) and its zero-growth obligation are unchanged. The new object here is an explicit state separating \(W_n\) from decomposable and polynomial-square certificate cones.

## 2. An exact complex certificate obstruction with sharp one-copy margin

A decomposable Hermitian operator has the form \(D=A+B^\Gamma\) with \(A,B\succeq0\). It has nonnegative pairing with every PPT state. Define the following normalized state on \(6\)-by-\(6\):

\[
\sigma_{\mathbb C}=\frac{4P_3\otimes P_2+Q_3\otimes Q_2}{28}.\tag{2}
\]

It is positive and has trace one. Since \(O_d^\Gamma=F_d\), the eigenvalues of its partial transpose, multiplied by \(28\), on the \((F_3,F_2)\) sectors \((+,+),(+,-),(-,+),(-,-)\), are

\[
1,\quad1/3,\quad0,\quad8/3.
\]

Thus it is PPT. Direct pairing gives

\[
\operatorname{Tr}(\sigma_{\mathbb C}W_1)=-1/7.\tag{3}
\]

Consequently

\[
\operatorname{dist}_\infty(W_1,\mathcal D)\ge1/7,\qquad
\mathcal D=\{A+B^\Gamma:A,B\succeq0\}.\tag{4}
\]

The bound is sharp, with an explicit dual certificate. Let \(A_d=(I-F_d)/2\) and \(T_d=(I+F_d)/2\). Then

\[
W_1+\tfrac17 I
=\tfrac37P_3\otimes Q_2
+\tfrac{12}7Q_3\otimes P_2
+\left(\tfrac47A_3\otimes T_2\right)^\Gamma.\tag{5}
\]

All three untransposed summands are positive. Expanding \(F_d^\Gamma=O_d\) proves the identity. Hence the exact distance in (4) is \(1/7\), and \(1/7\) is the smallest scalar identity noise making \(W_1\) decomposable.

This is stronger than failure of one proposed numerical Gram matrix: the PPT state separates every possible decomposable representation.

## 3. Why this is also a polynomial-square obstruction

For a Hermitian \(W\), the complex biquadratic polynomial

\[
p_W(a,b)=\langle a\otimes b,W(a\otimes b)\rangle
\]

is invariant under independent global phases of \(a,b\). If it is a sum of squares of real polynomials in their real and imaginary parts, each squared polynomial must be real bilinear between the two groups. Indeed total degree four bounds its degree by two, and setting either group to zero forces every square to vanish separately.

Any real bilinear form can be written as the real part of a sum of a complex bilinear and a complex sesquilinear form. Averaging its square over the two independent phases eliminates the mixed characters and leaves positive sums of

\[
|a^TMb|^2,\qquad |a^*Nb|^2.
\]

The first type is a positive Gram contribution and the second a partial transpose of a positive Gram contribution. Equality of complex biquadratic polynomials determines their Hermitian coefficient operator uniquely. Therefore

\[
p_W\text{ is a real-polynomial SOS}\quad\Longleftrightarrow\quad W\in\mathcal D.\tag{6}
\]

In particular the globally nonnegative one-copy polynomial \(f_1\) is not an unconstrained real-polynomial sum of squares. The exact smallest \(\delta\) for which

\[
f_1(U,V)+\delta\|U\|_F^2\|V\|_F^2
\]

is such a sum of squares is \(1/7\). This concerns free complex \(U,V\), not a normalized SVD chart with equations imposed.

## 4. An independent real-variable obstruction, also with a sharp margin

Restrict \(U,V\) to real matrices. Put \(\mathcal S(M)=(M+M^\Gamma)/2\) and \(W_{\mathbb R}=\mathcal S(W_1)\). On real product vectors, \(W_1\) and \(W_{\mathbb R}\) have the same polynomial.

For a real symmetric Gram matrix \(G\), equality of its real biquadratic polynomial to that of \(W_1\) is equivalent to \(\mathcal S(G)=W_{\mathbb R}\). The only discarded coefficients are antisymmetric in the two indices of each real variable group.

Consider the explicitly rational matrix

\[
\begin{aligned}
\sigma_{\mathbb R}=\frac1{240}\big[&
9I\otimes I-3I\otimes(F_2+O_2)-(F_3+O_3)\otimes I\\
&+7(F_3\otimes F_2+O_3\otimes O_2)\\
&-3(F_3\otimes O_2+O_3\otimes F_2)\big].
\end{aligned}\tag{7}
\]

It satisfies \(\sigma_{\mathbb R}^\Gamma=\sigma_{\mathbb R}\). Let \(S_d=T_d-P_d\), the symmetric traceless sector. On the nine sectors \((P_3,S_3,A_3)\otimes(P_2,S_2,A_2)\), in row-major order, its eigenvalues are

\[
(1/8,\,0,\,1/24;\quad0,\,1/20,\,1/60;\quad0,\,0,\,1/12).\tag{8}
\]

These are nonnegative and, with sector dimensions \((1,5,3)\) and \((1,2,1)\), sum to trace one. Moreover

\[
\operatorname{Tr}(\sigma_{\mathbb R}W_{\mathbb R})
=\operatorname{Tr}(\sigma_{\mathbb R}W_1)=-1/8.\tag{9}
\]

For every \(G\succeq0\),

\[
\operatorname{Tr}[\sigma_{\mathbb R}\mathcal S(G)]
=\operatorname{Tr}(\sigma_{\mathbb R}G)\ge0.
\]

Thus no unconstrained real bilinear-square representation exists. The scalar noise threshold is exactly \(1/8\): the positive matrix

\[
G_*=\tfrac34P_3\otimes S_2
+\tfrac32S_3\otimes P_2
+\tfrac52A_3\otimes P_2
+\tfrac12A_3\otimes S_2\tag{10}
\]

satisfies

\[
\mathcal S(G_*)=W_{\mathbb R}+\tfrac18I.\tag{11}
\]

Equations (7)--(11) prove both the lower bound and the attaining sum-of-squares certificate, without relying on an SDP solver. They also give

\[
\operatorname{dist}_\infty(W_{\mathbb R},\mathcal S(\mathrm{PSD}))=1/8.\tag{12}
\]

## 5. The obstruction persists uniformly at every copy number

Append \(n-1\) physical spectator pairs in the real product state

\[
\tau=|0\rangle\langle0|_A\otimes|1\rangle\langle1|_B.
\]

It is unchanged by partial transpose and \(\operatorname{Tr}(\tau K)=1\). Tensoring (2) or (7) with these spectator pairs and regrouping the auxiliary factor therefore gives normalized PPT states \(\sigma_{\mathbb C,n}\) and partial-transpose-invariant positive states \(\sigma_{\mathbb R,n}\), respectively, with

\[
\operatorname{Tr}(\sigma_{\mathbb C,n}W_n)=-1/7,\qquad
\operatorname{Tr}[\sigma_{\mathbb R,n}\mathcal S(W_n)]=-1/8.\tag{13}
\]

Hence for **every** \(n\),

\[
\operatorname{dist}_\infty(W_n,\mathcal D)\ge1/7,\qquad
\operatorname{dist}_\infty(\mathcal S(W_n),\mathcal S(\mathrm{PSD}))\ge1/8.\tag{14}
\]

Equivalently one can substitute \(U_n=U_1\otimes0^{n-1}\), \(V_n=V_1\otimes1^{n-1}\), so that \(UV^*\) is padded by \(E_{01}^{\otimes(n-1)}\). The polynomial and both factor norms then remain exactly their one-copy values.

Thus increasing copy number cannot give a vanishing unweighted-noise SOS approximation to the free rank-two factorization polynomial. These uniform certificate gaps are compatible with true rank-two positivity: the one-copy target is true while both gaps are already strictly positive. They are not negative Werner witnesses, and they do not imply that \(\Gamma_n>1\).

## 6. Strong opposition to an overbroad no-go claim

Normalization equations can evade this obstruction. If the columns of \(U\) are orthonormal, \(\|U\|_F^2=2\) and \(\|UV^*\|_F^2=\|V\|_F^2\). The ordinary complex Lagrange identity gives the exact constrained certificate

\[
q_1(UV^*)=\tfrac12\sum_{i<j}
|(\operatorname{vec}U)_i(\operatorname{vec}V)_j
-(\operatorname{vec}U)_j(\operatorname{vec}V)_i|^2.\tag{15}
\]

Here the identity is on the Stiefel constraint \(U^*U=I_2\). Thus the present obstruction does **not** exclude constrained SOS, rational multipliers, SVD gauges, or a different auxiliary positivity proof. In particular it does not refute the actual stage-one orthonormal-frame growth route. It tells us why replacing that difficult route by an unconstrained quartic Gram matrix cannot work.

## 7. The complete one-copy noise comparison on the Werner parameter interval

This construction extends without a new optimization. Put \(W(t)=(I-tO_3)\otimes O_2\), \(0\le t\le1\), and \(f_t(U,V)=q_{1,t}(UV^*)\). Let the noise polynomial be \(N=\|U\|_F^2\|V\|_F^2\). The exact smallest nonnegative identity-noise amounts are:

| Required property of \(f_t+\delta N\) | Smallest \(\delta\), \(0\le t\le1\) |
|---|---|
| Nonnegative for all complex \(U,V\) | \(\max(0,t-1/2)\) |
| Polynomial SOS for free real \(U,V\) | \(\max(0,(3t-1)/4)\) |
| Polynomial SOS in real and imaginary parts of free complex \(U,V\) | \(\max(0,2(3t-1)/7)\) |

For positivity, \(|\operatorname{Tr}C|\le\|C\|_1\), \(\|C\|_F^2\ge\|C\|_1^2/2\), and \(\|UV^*\|_1^2\le N\). For \(t\ge1/2\) this gives \(f_t\ge(1/2-t)N\). Equality is attained by \(U=V\) an orthonormal two-frame, after any common scalar normalization. For \(t\le1/2\), the usual rank-two trace inequality gives positivity with no added noise.

For complex polynomial squares, the same fixed state (2) pairs to \(2(1-3t)/7\). For \(t\ge1/3\), the matching decomposable identity is

\[
\begin{aligned}
W(t)+\frac{2(3t-1)}7I
={}&\frac{6(3t-1)}7P_3\otimes Q_2
+\frac{6(3-2t)}7Q_3\otimes P_2\\
&+\left(\frac{8(3t-1)}7A_3\otimes T_2\right)^\Gamma .
\end{aligned}\tag{17}
\]

All untransposed coefficients are nonnegative on the stated interval.

For real polynomial squares, (7) pairs to \((1-3t)/4\). The matching positive Gram matrix is

\[
\begin{aligned}
G(t)={}&\tfrac32(3t-1)P_3\otimes S_2
+3(1-t)S_3\otimes P_2\\
&+(1+3t)A_3\otimes P_2
+(3t-1)A_3\otimes S_2,
\end{aligned}
\]

and it satisfies

\[
\mathcal S(G(t))=\mathcal S(W(t))+\tfrac14(3t-1)I.\tag{18}
\]

It is positive for \(1/3\le t\le1\). When \(t\le1/3\), \(W(t)\succeq0\), so both SOS noise thresholds are zero. This proves every entry of the table. In particular the nonzero endpoint certificate gaps are not negative objective gaps, and their persistence with \(n\) must not be used as evidence of Werner distillability.

## 8. The auxiliary state is an explicit activator, not a free premise

There is a useful constructive interpretation of (2). Set \(\alpha=\sigma_{\mathbb C}^{\Gamma}\). Both \(\alpha\) and its partial transpose are positive, so it is a PPT state. Combine \(\alpha\) with one target Werner state \(\rho=(2I-F_3)/15\). Alice projects the two physical qutrits in her laboratory onto the normalized maximally entangled vector, and Bob does the same. Retain the auxiliary qubits.

The unnormalized output, by ordinary Bell contraction, is

\[
\tau=\frac19\operatorname{Tr}_{\mathrm{physical}}
[(\rho^T\otimes I_4)\alpha]
=\frac{8I_4-5F_2}{1890}.\tag{19}
\]

Its success probability is \(11/945\), and its normalized form is

\[
\widehat\tau=\frac{8I_4-5F_2}{22},\qquad
\lambda_{\min}(\widehat\tau^\Gamma)=-1/11.\tag{20}
\]

It is a distillable two-qubit NPT output. Equations (19)--(20) are an explicit mathematical activation protocol; no equipment was operated. They illustrate exactly why the PPT dual state is not a negative rank-two witness for the input Werner tensor powers.

In fact the same fixed activator works on the whole qutrit NPT Werner interval. For \(\rho_t=(I-tF_3)/(9-3t)\), the same contraction gives

\[
\tau_t=\frac{4I_4-(1+3t)F_2}{378(3-t)},\quad
p_t=\frac{7-3t}{189(3-t)},\quad
\lambda_{\min}(\widehat\tau_t^\Gamma)=\frac{1-3t}{7-3t}.\tag{21}
\]

Thus its output is NPT exactly when \(t>1/3\). This does not claim a new activation phenomenon; activation by PPT entanglement is already discussed in Hiroshima's introduction and its cited primary literature.

The activator is an additional entangled resource. No LOCC preparation of \(\alpha\) from the target Werner copies has been established here. Assuming that preparation would silently supply the missing resource and could turn this certificate obstruction into a false distillation claim. If such a preparation from \(m\) target copies were actually proved, the displayed protocol would give an \((m+1)\)-copy counterexample. The known two-copy theorem already rules out a one-copy preparation. For larger \(m\), no preparation or impossibility is proved.

## 9. Source overlap and verification

The qualitative one-copy non-SOS phenomenon is existing literature: T. Hiroshima, [arXiv:1007.1830v1](https://arxiv.org/pdf/1007.1830), especially Section III. Its formulation, non-SOS discussion and rational-function remedy were read during this block. It is not claimed as a new discovery here. The present work gives explicit rational dual states, matching primal identities, exact noise thresholds \(1/7\) and \(1/8\), and the copy-uniform embedding; no exhaustive historical-priority claim is made for those formulas.

D. Z. Djokovic, [arXiv:1005.4247v2](https://arxiv.org/pdf/1005.4247), was consulted for the established four-hypermatrix CBS formulation and rank-one Lagrange mechanism. No conjectural statement from it is imported. Astra was searched read-only at revision 65aae508a61d02e4a6ba5b368a94779ae6d744cf for overlapping Werner/SOS/Hiroshima material. Stage-one and frozen-stage-one files were not edited.

The floating-point five-variable LP used only to discover (7) and (10) is not a proof premise. The retained verifier checks their complete rational matrix identities, sector decompositions, partial transposes, normalizations and pairings. It independently checks (1) on a complex factorization and checks a spectator embedding using partial traces. The algebra above proves the scope; finite verification is not a solution of the all-copy target.

The hardest remaining obligation remains a proof that the stage-one \(\Gamma_n\) has subexponential growth, or a rigorous violated rank-two Cauchy determinant. No such proof or endpoint counterexample was found.
