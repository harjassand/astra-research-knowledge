# ASTRA Meta-Genesis: two-contact rigidity, concentration defects, and contact shears

Research date: 14 October 2026.

## Status

The complete implication from rank-one convexity to quasiconvexity for the nine-dimensional left-SO(2)-invariant homogeneous quartic cone is **not established in this investigation**. No compatible gradient with a negative quasiconvexity gap was found.

This note establishes three types of result against the positive-definite barrier:

* A full-cone **two-contact rigidity theorem**, improving the previous rank-three covariance threshold to rank two, with a quantitative covariance coercivity consequence.
* An actual, explicit **full-rank compatible concentrating sequence** for an exactly certified rank-one-convex, non-polyconvex quartic. Its averaged Hessians are positive definite and approach a nonzero singular Hessian, but the optimized cubic loss has a strictly positive limit. Thus a natural continuity extension of exact nullspace closure is false, even in the relevant non-polyconvex sector. The sequence's variational gaps are positive, not negative.
* A **contact-shear theorem**: the remaining semidefinite rank-two acoustic tangencies must be determinant-preserving shears, and their cubic restriction is invariant along that shear. An explicit nonlinear change of coordinates straightens any finite contact-shear profile. The resulting energy has spatially varying coefficients, whose general positivity is not proved.

An exact gluing/defect formula separates the contribution of localized profiles. Its matrix inequality is standard quadratic duality, not a new positivity principle. The original rank-one-convexity problem remains in the compatible, internally resonant profiles and their interactions.

All analytic arguments and constants used below are explicit. `verify_positive_definite.py` independently reconstructs the finite identities from constants in the script. It uses SymPy, not an optimization solver or prior verification output. Twelve grouped checks passed. These checks are not a proof-assistant formalization or external review. Historical priority has not been cleared.

The previous nullspace theorem and low-rank lemma were reconstructed before reuse. The previous twelve-group verifier was also actually replayed; its log is included. No earlier heat-certificate theorem is a premise of the new results.

## 1. Setting and reconstructed foundation

Let
\[
 A=(x\mid y)=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
 u=a^2+c^2,\ v=b^2+d^2,\ w=ab+cd,\ q=ad-bc.
\]
The row-major vector of a matrix is \((a,b,c,d)^T\). A homogeneous quartic invariant under left SO(2) has all nine coefficients
\[
 F=A_cu^2+B_cv^2+Cuv+Ew^2+Guw+H_0vw+Lqu+Mqv+Nqw.                 \tag{1.1}
\]
No equality between \(L,M\) or vanishing of \(N\) is assumed in the structural theorems.

Rank-one convexity means
\[
 D^2F(A)[R,R]\ge0\quad\text{whenever }q(R)=0.                 \tag{1.2}
\]
For a periodic or zero-boundary potential, put \(X=D\varphi\) and take averages over a unit-volume domain. Then
\[
 \mathbb EX=0,\qquad \mathbb E q(X)=0.
\]
The determinant identity follows by integration by parts and extends by density to \(W^{1,4}\).

Define
\[
 C_X=\mathbb E XX^T,\quad H=\mathbb E D^2F(X),\quad
 b_F=\mathbb E DF(X),\quad c_F=\mathbb E F(X).
\]
Here and below the matrix product \(XX^T\) in the covariance definition uses the row-major vector. Quartic polarization gives
\[
 \mathbb E[F(B+X)-F(B)]
 =c_F+b_F:B+\tfrac12 B:H B.                                 \tag{1.3}
\]

### 1.1 Quadratic decomposition and cubic closure

The following is the indefinite case of the non-strict Finsler lemma [1]. If an indefinite quadratic form \(q\) and a quadratic form \(Q\) satisfy \(Q\ge0\) on \(q=0\), then
\[
 Q=P+\lambda q,\qquad P\succeq0.                             \tag{1.4}
\]
For completeness, on any plane spanned by a positive-q and a negative-q vector, normalize \(q=s^2-t^2\). If \(Q=\alpha s^2+2\beta st+\gamma t^2\), the null-cone condition is \(\alpha+\gamma\ge2|\beta|\), and \(Q-((\alpha-\gamma)/2)q\succeq0\) on that plane. Consequently
\[
 \sup_{q(Y)<0}\frac{Q(Y)}{q(Y)}
 \le\inf_{q(X)>0}\frac{Q(X)}{q(X)}.
\]
Both endpoints are finite by fixing one vector of each sign. Any scalar between them proves (1.4).

Quartic tensor symmetry gives
\[
 D^2F(A)[X,X]=D^2F(X)[A,A].                                  \tag{1.5}
\]
For any fixed \(A\), (1.4) therefore gives
\[
 D^2F(A)[X,X]=P_A(X)+\lambda_Aq(X),\qquad P_A\succeq0.        \tag{1.6}
\]
For every law with \(\mathbb E q(X)=0\), not necessarily a gradient law,
\[
 A:H A=\mathbb E P_A(X)\ge0.                                \tag{1.7}
\]

If \(A\in\ker H\), the law is supported on \(U=\ker P_A\). For \(R\in U\) with \(q(R)=0\), the globally nonnegative quadratic
\(t\mapsto D^2F(A+tY)[R,R]\) has value zero at zero, so
\[
 D^3F(A)[Y,R,R]=0\quad\text{for every }Y.                    \tag{1.8}
\]
For the homogeneous cubic \(\mathcal C_A(X)=DF(X)[A]\), symmetry yields
\[
 D^2\mathcal C_A(Y)[R,R]=D^3F(A)[Y,R,R].                     \tag{1.9}
\]
If \(q|_U\) is indefinite, every quadratic vanishing on its null cone is a scalar multiple of \(q|_U\). This follows by diagonalizing \(q\), testing opposite-sign coordinate pairs, and then radical directions. Thus
\(D^2\mathcal C_A(Y)|_U=\ell(Y)q|_U\). In diagonal coordinates, for each coordinate \(k\), choose \(i\ne k\) with \(q_{ii}\ne0\). Cubic tensor symmetry gives
\[
 \ell(e_k)q_{ii}=D^2\mathcal C_A(e_k)[e_i,e_i]
 =D^2\mathcal C_A(e_i)[e_k,e_i]=\ell(e_i)q_{ki}=0.
\]
Hence \(\ell=0\) and \(\mathcal C_A=0\) on \(U\).

If \(q|_U\) is semidefinite, its zero mean forces \(q(X)=0\) almost everywhere. Putting \(R=Y=X\) in (1.8) gives the same almost-everywhere conclusion. Therefore
\[
 H\succeq0,\qquad A\in\ker H\Longrightarrow DF(X)[A]=0
 \text{ almost everywhere},\qquad b_F\in\operatorname{ran}H. \tag{1.10}
\]
This reconstruction covers all 35 planar quartic coefficients. It does not prove the quartic gap nonnegative.

In particular, the background minimum is attained and equals
\[
 \Delta_F(X):=\inf_B\mathbb E[F(B+X)-F(B)]
 =c_F-\tfrac12b_F^TH^\dagger b_F.                            \tag{1.11}
\]
We denote the subtracted term by \(\mathcal L_F(X)\). This notation names an explicitly minimized quadratic term, not a new assumption of positivity.

## 2. Full-cone two-contact rigidity

For complex output columns \(x_{\mathbb C},y_{\mathbb C}\), define
\[
 \mathcal E=\{\gamma q^2+|\alpha x_{\mathbb C}+\beta y_{\mathbb C}|^4:
 \gamma\ge0,\ \alpha,\beta\in\mathbb C\},
\]
and the larger, still explicitly polyconvex class
\[
 \mathcal P_2=\mathcal E\ \cup\
 \{a|Ar|^4+|\alpha x_{\mathbb C}+\beta y_{\mathbb C}|^4:
 a\ge0,\ r\in\mathbb R^2,\ \alpha,\beta\in\mathbb C\}.        \tag{2.1}
\]
Coefficients can be zero. In the second set both summands are convex functions of the entries. Both classes are preserved by invertible real input-coordinate changes.

Let \(J_{\det}\) be the symmetric matrix for the quadratic form \(q\), and
\[
 \mathcal K=\{C\succeq0:\operatorname{tr}(J_{\det}C)=0\}.
\]
The average Hessian depends linearly on the second moment; write this map as \(H_F(C)\).

### Theorem 2.1

For a rank-one-convex \(F\) in the complete class (1.1), the following are equivalent:

(a) Some \(C\in\mathcal K\) with rank at least two has \(H_F(C)\) singular.

(b) There are two linearly independent rank-one matrices \(R,S\) such that
\(D^2F(R)+D^2F(S)\) is singular.

(c) \(F\in\mathcal P_2\).

Consequently, for every non-polyconvex member of the nine-coefficient cone,
\[
 \boxed{\operatorname{rank}C\ge2\Longrightarrow H_F(C)\succ0.} \tag{2.2}
\]
The result also applies to polyconvex members outside \(\mathcal P_2\). It does not classify all polyconvex quartics.

### 2.2 Proof: reduction to a positive remainder of rank at most two

Assume (a), choose nonzero \(A\in\ker H_F(C)\), and use (1.6). Then
\(\operatorname{tr}(P_AC)=0\). Positivity gives
\(\operatorname{ran}C\subseteq\ker P_A\), hence \(\operatorname{rank}P_A\le2\).

We first record the reconstructed rank-at-most-one case from the previous note. If \(A\) is rank one, \(D^2F(A)\succeq0\) by (1.5). A nonzero multiple of the determinant has two negative directions, so a rank-one positive remainder cannot compensate it: \(\lambda_A=0\). Rotation covariance and homogeneity give
\[
 D^2F(A)A=3DF(A),\qquad D^2F(A)(JA)=JDF(A),
\]
where \(J\) rotates each output column by a quarter-turn. A positive value \(F(A)\) would give two independent vectors in the Hessian range, a contradiction. Thus the convex binary rank-one restriction has a zero direction. Its fourth root is a seminorm, so after a real input change it is \(a u^2\) on rank-one matrices. Comparing (1.1) gives
\(F=a u^2+\lambda q^2+q(Lu+Mv+Nw)\). PSD Hessians at the rank-one matrices \(e_{12},e_{11}\) force \(M=N=L=0\), \(\lambda\ge0\). Thus \(F\in\mathcal E\).

For invertible \(A\), normalize it to \(I\). In the basis
\[
 I,\quad J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad
 K=\operatorname{diag}(1,-1),\quad L_0=\begin{pmatrix}0&1\\1&0\end{pmatrix},
\]
write a matrix as \(iI+jJ+kK+lL_0\), so \(q=i^2+j^2-k^2-l^2\). Set
\(f=F(I)\), \(a=DF(I)[K]\), \(b=DF(I)[L_0]\). The first two Hessian rows are forced to be
\[
 D^2F(I)=\begin{pmatrix}12f&0&3a&3b\\0&4f&-b&a\\3a&-b&*&*\\3b&a&*&*\end{pmatrix}. \tag{2.3}
\]
If its positive determinant-corrected remainder has rank at most one, comparison with \(vv^T+\lambda\operatorname{diag}(1,1,-1,-1)\) forces \(a=b=0\). For \(f<0\), its kernel is indefinite and contains \(I\), contradicting (1.8)-(1.9). For \(f>0\), use complex variables \(z=i+\mathrm i j,w=k+\mathrm i l\). The complete polynomial reduces to
\(f q^2+g|w|^4+\operatorname{Re}(\eta |w|^2z\bar w)\). Cubic closure on \(i=0\) kills \(\eta\); rank-one convexity gives \(g\ge0\). For \(f=0\), the possible residual polynomial is
\(\tau(\operatorname{Re}z\bar w)^2+g|w|^4+h|w|^2\operatorname{Re}(z\bar w)\), after a rotation. Here the polynomial and its first derivative vanish on the conformal plane \(w=0\). The rank-one segment from \((z-w,0)\) in direction \((w,w)\) proves nonnegativity of the whole residual polynomial. Taking \(w=1,z=\mathrm iT\) for arbitrary real \(T\) removes the imaginary part of \(\eta\). Testing at \(z=\mathrm iZ,w=\mathrm iW\) in directions \((\sigma,1)\), \(\sigma=\pm1\), forces \(\tau=h=0\), \(g\ge0\). Again \(F\in\mathcal E\). This covers the rank-at-most-one remainder without taking it as an unaudited premise.

We therefore assume \(\operatorname{rank}P_A=2\). Then \(\operatorname{ran}C=\ker P_A=:U\) is a plane, and \(C\) is positive definite on that plane. The determinant restricted to \(U\) is consequently either indefinite or identically zero. A nonzero semidefinite restriction could not have zero average under a positive-definite second moment on \(U\).

### 2.3 Rank-one distinguished background

Normalize \(A=e_{11}\). Reciprocity makes \(Q=D^2F(e_{11})\) PSD. The balance identity gives \(\operatorname{tr}(QC)=0\), so \(\operatorname{ran}C\subseteq\ker Q\) and \(\operatorname{rank}Q\le2\). If \(F(e_{11})=0\), the degenerate binary argument just given proves \(F\in\mathcal E\). Suppose \(A_c=F(e_{11})>0\). Direct differentiation gives
\[
 Q=\begin{pmatrix}
12A_c&3G&0&3L\\
3G&2C+2E&-L&N\\
0&-L&4A_c&G\\
3L&N&G&2C
\end{pmatrix}.                                               \tag{2.4}
\]
The positive \((a,c)\) block has rank two. Hence its Schur complement vanishes, and the kernel is
\[
 a=-\frac{Gb+Ld}{4A_c},\qquad c=\frac{Lb-Gd}{4A_c},\qquad
 q|_{\ker Q}=-\frac{L}{4A_c}(b^2+d^2).                      \tag{2.5}
\]
Balanced rank-two covariance therefore forces \(L=0\). The Schur identities give
\(C=G^2/(8A_c), E=G^2/(4A_c),N=0\). Subtracting
\(A_c|x+(G/(4A_c))y|^4\) and making this real input shear leaves
\(B'v^2+H'vw+M'qv\). Positivity of the Hessian at \(e_{12}\) forces \(H'=M'=0\), \(B'\ge0\). This is a convex member of \(\mathcal P_2\).

### 2.4 Invertible distinguished background: generic top block

Normalize \(A=I\). In complex coordinates, every invariant quartic is
\[
 F=f|z|^4+\beta|z|^2|w|^2+g|w|^4+
 \operatorname{Re}(\delta z^2\bar w^2+\epsilon |z|^2z\bar w+\eta |w|^2z\bar w). \tag{2.6}
\]
A conjugation by rotations fixing \(I\) lets us take \(\epsilon=a\ge0\) real. Put
\[
 p=12f-\lambda,\qquad r=4f-\lambda.
\]
If \(p,r>0\), rank two of \(P\) forces its lower Schur complement to vanish:
\[
 \operatorname{Im}\delta=0,\quad
 \beta=\frac{9a^2/p+a^2/r-2\lambda}{4},\quad
 \delta=\frac{9a^2/p-a^2/r}{4},                              \tag{2.7}
\]
with kernel
\[
 i=-3ak/p,\qquad j=-al/r.                                  \tag{2.8}
\]
If \(q|_U\) is indefinite, cubic closure says \(\partial_iF|_U=0\). Its \(l^3\) coefficient is \(\operatorname{Im}\eta\), so this part vanishes. The difference of its \(k^3\) and \(kl^2\) coefficients is exactly
\[
 \boxed{-\frac{4\lambda^3a^3}{r^2p^3}.}                    \tag{2.9}
\]
Hence \(\lambda a=0\). But \(a=0\) makes the determinant negative definite on \(U\), while \(\lambda=0\) makes its two diagonal coefficients equal and hence semidefinite. Neither is indefinite. This case is impossible.

If \(q|_U=0\), (2.8) gives \(p=3a,r=a\), so \(\lambda=0,a=4f>0\). All vectors in \(U\) are rank one; (1.8) forces \(\eta=4f\) real. The whole integrand, not just its Hessian, becomes
\[
 F=f|z+w|^4+(g-f)|w|^4,\qquad g-f\ge0.                    \tag{2.10}
\]
The first linear functional is the real first input column. Undoing the input change gives precisely the second class in (2.1).

### 2.5 Invertible background: singular top blocks

If \(p=0,r>0\), PSD forces \(a=0\), \(f<0\), and the kernel includes \(I\) and a nonzero anticonformal vector. The determinant is indefinite there, so cubic closure contradicts \(DF(I)[I]=4f<0\).

If \(r=0,p>0\), then \(f>0,a=0\), and the remaining lower PSD block has rank one. Rotate \(w\) to diagonalize it. The polynomial has the form
\[
 fq^2+\tau(\operatorname{Re}z\bar w)^2+g_0|w|^4+
 \operatorname{Re}(\eta |w|^2z\bar w).
\]
The kernel is \(\operatorname{span}\{J,L_0\}\), an indefinite plane, which forces \(\operatorname{Im}\eta=0\). Write \(\eta=h\). At \(z=\mathrm i Z,w=\mathrm iW\), the rank-one directions \((\sigma,1)\), \(\sigma=\pm1\), give
\[
 2[(2\tau\sigma+h)ZW+(2g_0+h\sigma)W^2].                   \tag{2.11}
\]
The determinant-square term contributes zero to this test. Nonnegativity for arbitrary \(Z\) forces \(\tau=h=0\), reducing to \(\mathcal E\) and contradicting an exactly rank-two remainder.

If \(p=r=0\), then \(f=\lambda=a=0\) and the kernel is the conformal plane. Its determinant is positive definite, incompatible with balanced rank-two covariance. This exhausts the cases and proves (a) implies (c).

### 2.6 Converse and two-contact formulation

For \(F\in\mathcal E\), choose nonzero \(A\) in the kernel of its complex linear functional. There are two independent rank-one \(R,S\) in the hyperplane \((\operatorname{cof}A):R=0\). Both Hessians annihilate \(A\). This follows directly by differentiating the two summands; a real coordinate normalization handles invertible or rank-one \(A\).

For \(F=a|Ar|^4+|\ell(A)|^4\), choose nonzero \(A\in\ker\ell\) and independent rank-one \(R,S\) with \(Rr=Sr=0\). The first summand has zero Hessian at these matrices; the second annihilates \(A\). Thus (c) implies (b). Taking \(C=RR^T+SS^T\) proves (b) implies (a). QED.

## 3. A quantitative consequence determined by two acoustic directions

For \(F\notin\mathcal P_2\), define
\[
 \mu_F(s)=\min\left\{\lambda_{\min}(D^2F(R)+D^2F(S)):
 |R|=|S|=1,\ q(R)=q(S)=0,\ 1-(R:S)^2\ge s^2\right\},
 \quad 0<s\le1.                                            \tag{3.1}
\]
Theorem 2.1 and compactness prove \(\mu_F(s)>0\). This is a fixed-dimensional local acoustic minimum, not the unknown quasiconvexity minimum. No efficient exact acquisition claim or universal power law for this modulus is made.

### Theorem 3.1

Let \(C\in\mathcal K\setminus\{0\}\), \(M_2=\operatorname{tr}C\), and
\(\tau=1-\lambda_{\max}(C)/M_2\). If \(\tau>0\), then
\[
 \boxed{\lambda_{\min}H_F(C)
 \ge \frac{M_2\tau}{4}\,\mu_F(\sqrt{\tau/2}).}              \tag{3.2}
\]

**Proof.** Factor \(C=TT^T\) with \(T\) injective on \(\mathbb R^{\operatorname{rank}C}\). The symmetric form \(T^TJ_{\det}T\) has trace zero. It has an orthonormal basis with zero quadratic diagonal: choose one unit zero by the intermediate value theorem between signs, restrict to its orthogonal complement (still trace zero), and continue. Thus
\(C=\sum_j R_jR_j^T\) with each nonzero matrix \(R_j\) rank one. There are at most four atoms.

Normalize these atoms to a probability law \(\pi\) on unit rank-one matrices, weighted by \(|R_j|^2/M_2\). For independent \(R,S\sim\pi\),
\[
 \mathbb E[1-(R:S)^2]
 =1-\operatorname{tr}[(C/M_2)^2]\ge\tau.
\]
The event \(1-(R:S)^2\ge\tau/2\) has probability at least \(\tau/2\). On it, the acoustic Hessian sum is at least \(\mu_F(\sqrt{\tau/2})I\); off it the sum is PSD. Taking expectations gives (3.2). QED.

Thus, for a fixed non-polyconvex integrand, an ill-conditioned normalized averaged Hessian must accompany covariance collapse toward a single matrix line. This is stronger than the previous rank-three gap. It still says nothing by itself about the fourth-moment mass on that line or away from it.

For example, normalize \(\mathbb E|X|^4=1\). Put \(B_F=\max_{|A|=1}|DF(A)|\). If \(M_2\ge m>0\) and \(\tau\ge\delta>0\), the optimizing affine background obeys the explicit bound
\[
 |H^{-1}b_F|\le
 \frac{4B_F}{m\delta\mu_F(\sqrt{\delta/2})}.                 \tag{3.3}
\]
This bounds backgrounds, not Fourier bandwidths, and does not prove the optimized value nonnegative.

## 4. The remaining tangent contacts are determinant-preserving shears

The rank-two theorem excluded indefinite and totally-null contact planes outside a polyconvex class. A more delicate possibility is a rank-two PSD remainder whose determinant restriction is semidefinite of rank one. It is not eliminated: the explicit example in Section 5 realizes it.

### Theorem 4.1 — Contact shear and cubic invariance

Let \(F\) be a non-polyconvex rank-one-convex member of (1.1). Suppose \(A\) is invertible and
\[
 D^2F(A)[X,X]=P(X)+\lambda q(X),\quad P\succeq0,\quad
 \operatorname{rank}P=2,
\]
with \(q|_{U}\), \(U=\ker P\), semidefinite of rank one. Its radical is a unique rank-one matrix line, spanned by \(R\ne0\). Then
\[
 \boxed{\operatorname{tr}(A^{-1}R)=0,\qquad
 DF(X+tR)[A]=DF(X)[A]\quad(X\in U,t\in\mathbb R).}           \tag{4.1}
\]
In particular, \(\det(A+tR)=\det A\) for every real \(t\).

### Proof

Normalize \(A=I\) as before. Singular top-block cases either belong to \(\mathcal E\), have indefinite kernels already excluded, or have definite determinant on the kernel. Thus use (2.7)-(2.8) with \(p,r>0\). Semidefiniteness of rank one means exactly one of
\(p=3a\) or \(r=a\) holds.

The branch \(p=3a\) is not compatible with rank-one convexity unless it degenerates to the polyconvex case. This requires a joint contact test, not merely vanishing first derivatives.

The radical in this branch is \((z,w)=(-1,1)\). The condition \(D^2F(R)I=0\), which follows from reciprocity and PSD, gives \(\eta=r\) real. Put \(V=F(-1,1)\). Rank-one convexity gives \(V\ge0\); equality gives a degenerate binary restriction and hence the already excluded polyconvex class. Thus \(V>0\).

Use \(p,r,V\) as parameters. Then
\[
 f=(p-r)/8,\quad\lambda=(p-3r)/2,\quad a=p/3,
\]
\[
 \beta=p^2/(36r)+3r/4,\quad
 \delta=(p-p^2/(9r))/4,\quad
 g=V-(p-9r)/24.
\]
Rotate the critical output so that its rank-one direction is \(e_1\otimes(0,1)\). The corresponding background vector is \(n=(0,-1,1,0)^T\). Let \(M(t)\) be the acoustic matrix for \(e_1\otimes(t,1)\), so \(M=M_0+tM_1+t^2M_2\) and \(M_0n=0\). Let \(U_0\) have columns \(e_1,e_4,e_2+e_3\). Direct calculation gives
\[
 C_0=U_0^TM_0U_0=
 \begin{pmatrix}
 (p-3r)^2/(36r)+V/4&-V/4&0\\-V/4&V/4&0\\0&0&3V
 \end{pmatrix},
\]
\[
 \det C_0=V^2(p-3r)^2/(48r),\qquad
 n^TM_2n-(U_0^TM_1n)^TC_0^{-1}(U_0^TM_1n)
 =-\frac{(p-3r)^4}{324r^2V}.                                \tag{4.2}
\]
When \(p\ne3r\), \(C_0\) is positive definite and the last expression is strictly negative. The actual background
\(n-tU_0C_0^{-1}U_0^TM_1n\), tested in the actual rank-one direction \(e_1\otimes(t,1)\), has negative acoustic energy for sufficiently small nonzero \(t\). This contradicts rank-one convexity. When \(p=3r\), \(\lambda=0\) and the determinant vanishes identically on \(U\), giving (2.10), also excluded.

Only \(r=a\) remains. Its radical is \(z=-\mathrm i l,w=\mathrm i l\), the physical line spanned by \(e_{12}\), whose trace is zero. The full contact equation gives
\[
 \operatorname{Im}\eta=0,\qquad
 \operatorname{Re}\eta=(48f^2-40f\lambda+7\lambda^2)/p.
\]
On the kernel (2.8), direct substitution yields
\[
 \boxed{DF(X)[I]|_U=-\frac{4\lambda^3r}{p^3}\,k^3.}          \tag{4.3}
\]
It is independent of the radical coordinate \(l\). Undoing the input normalization proves (4.1). QED.

### 4.2 An actual nonlinear coordinate operation

Write \(R=a_0\otimes b_0\) and \(v_0=A^{-1}a_0\). Then \(b_0\cdot v_0=0\). For a differentiable scalar profile \(h\), define
\[
 \Psi_h(x)=x+v_0h(b_0\cdot x),\qquad
 \Psi_h^{-1}(x)=x-v_0h(b_0\cdot x).                         \tag{4.4}
\]
Both identities are exact: \(b_0\cdot\Psi_h(x)=b_0\cdot x\), and
\(\det D\Psi_h=1\). Thus
\(A\Psi_h(x)=Ax+a_0h(b_0\cdot x)\) is a globally invertible finite contact shear. For integer \(b_0\) and a periodic profile it induces a torus diffeomorphism.

For a periodic residual \(w\), let \(\widetilde w=w\circ\Psi_h^{-1}\). Change of variables gives
\[
 \int_Q F(A+Rh'(b_0\cdot x)+Dw(x))\,dx
 =\int_Q F((A+D\widetilde w(z))
       [I+v_0\otimes b_0\,h'(b_0\cdot z)])\,dz.             \tag{4.5}
\]
This straightens the compatible contact mode without a linear flow. Each frozen right-transformed integrand is still rank-one convex, but it depends on position and is correlated with the residual. Replacing it by its average would be unjustified. Equation (4.5) is not a proof of the missing global inequality.

The pure shear itself has an exact positive gap. Acoustic equality kills the quadratic coefficient; nonnegativity of the second derivative along its rank-one line kills the cubic coefficient. Hence for mean-zero \(h'\),
\[
 \int_Q[F(A+Rh')-F(A)]=F(R)\int_Q(h')^4\ge0.                \tag{4.6}
\]
The unresolved issue is interaction with the residual in (4.5), not the contact mode alone.

## 5. An explicit non-polyconvex quartic with a tangent contact

Consider
\[
 \boxed{G(A)=3(u+v-2q)^2+\frac{35}{24}u^2+q^2-\frac52qu.}   \tag{5.1}
\]
Its nine coefficients are
\[
 (A_c,B_c,C,E,G_c,H_c,L,M,N)
 =(107/24,3,19,-13,0,0,-29/2,-12,0).
\]
Thus the orientation coefficients are unequal. This example is used to test the quantitative mechanism, not as a substitute for a theorem on the full cone.

### 5.1 Exact rank-one-convexity certificate

Let \(M_{11},M_{12},M_{22}\) be the symmetric matrices for the quadratic polynomials
\(\partial_{aa}G,\partial_{ab}G,\partial_{bb}G\), respectively. Thus
\[
 D^2G(A)[e_1\otimes(s,t),e_1\otimes(s,t)]
 =X^T(s^2M_{11}+2stM_{12}+t^2M_{22})X.
\]
Choose the skew matrix whose independent entries \((01,02,03,12,13,23)\) are
\[
 (11,91/6,0,0,11,41/3),
\]
and form
\[
 Q=\begin{pmatrix}M_{11}&M_{12}+K\\M_{12}-K&M_{22}\end{pmatrix}.
\]
The exact vectors
\[
 (-2/3,0,0,-2/3,0,-1,1,0)^T,\quad (0,0,0,0,1,0,0,1)^T
\]
are in its kernel. Its leading principal minors of orders one through six are
\[
 107/2,\quad642,\quad1605/8,\quad8445/16,\quad2815/8,\quad26865/4.
\]
All are positive. The rank is six, so the Schur complement of this positive block vanishes and \(Q\succeq0\). The exact polynomial identity with the differentiated acoustic form proves rank-one convexity. Necessity of a sum-of-squares representation is not required for this certificate.

For non-polyconvexity,
\[
 G(I)=-1/24,\qquad G(\operatorname{diag}(1,-1))=1271/24.
\]
Put mass \(1/[2(1+36^2)]\) at each of \(\pm36I\) and mass \(36^2/[2(1+36^2)]\) at each of \(\pm\operatorname{diag}(1,-1)\). Mean matrix and mean determinant vanish, but mean energy is \(-1350/1297\). This contradicts any convex lift in the entries and determinant. It is only a polyconvexity witness, not a gradient construction.

### 5.2 Its exact tangent plane

At background \(I\),
\[
 D^2G(I)[X,X]=\frac12(3a-2d)^2+\frac56c^2-q(X).              \tag{5.2}
\]
The PSD remainder has kernel
\[
 U=\{c=0,\ d=3a/2\},\qquad q|_U=3a^2/2,
\]
whose radical is the shear line \(\mathbb R e_{12}\). Its cubic restriction is
\[
 DG(X)[I]|_U=-5a^3/12.                                     \tag{5.3}
\]
This is the semidefinite situation where exact determinant balance kills the cubic only on the law's support, not everywhere in \(U\).

## 6. A compatible counterexample to near-singular loss continuity

The following construction stays inside the positive-definite averaged-Hessian sector and has **positive-definite covariance as well**. It is not a negative quasiconvexity gap.

Work on the unit torus. Let \(h_0(0)=0\), with periodic derivative
\[
 h_0'(y)=\begin{cases}1&0<y<1/4,\\-1&1/4<y<1/2,\\0&1/2<y<1.\end{cases}
\]
Set \(\varphi_0=(h_0(y),0)\). Its gradient vanishes in the upper half of the torus, its cubic vector is zero, and for (5.1)
\[
 H_0=\begin{pmatrix}6&0&0&-6\\0&18&18&0\\0&18&19&0\\-6&0&0&6\end{pmatrix},
 \quad\ker H_0=\mathbb RI,\quad c_0=3/2.                    \tag{6.1}
\]

Define a zero-boundary profile on the unit square by
\[
 k(t)=t(1-t),\qquad
 f(s)=\begin{cases}2s&s\le1/3,\\1-s&s\ge1/3,\end{cases}
\]
\[
 \psi(s,t)=(f(s)k(t),\ s(1-s)k(t)).                         \tag{6.2}
\]
For \(0<\rho<1/4\), place the square at \(x_*=(1/4,3/4)\) and put
\[
 \varphi_\rho(x)=\varphi_0(x)+
 \begin{cases}\rho^{1/2}\psi((x-x_*)/\rho)&x\in x_*+\rho(0,1)^2,\\0&\text{otherwise}.\end{cases} \tag{6.3}
\]
These are genuine periodic Lipschitz potentials. Their Lipschitz constants are not uniformly bounded as \(\rho\downarrow0\). Their fourth gradient moments are uniformly bounded and in fact constant, but are not equiintegrable.

Exact polynomial integration gives profile moments
\[
 C_\psi=\begin{pmatrix}
1/15&0&1/45&0\\0&4/81&0&11/486\\1/45&0&1/90&0\\0&11/486&0&1/90
\end{pmatrix}\succ0,
\]
\[
 H_\psi=\begin{pmatrix}
2581/540&41/405&248/1215&-2189/540\\
41/405&47/15&121/36&-14/405\\
248/1215&121/36&1229/324&-41/405\\
-2189/540&-14/405&-41/405&494/135
\end{pmatrix}\succ0,
\]
\[
 b_\psi=(191/756,\ 1231/11340,\ 1439/11340,\ -2299/11340)^T,
 \quad c_\psi=5951/58800,
 \quad\mathbb E|D\psi|^4=29023/1071630.                     \tag{6.4}
\]
In particular,
\[
 b_\psi:I=283/5670,\qquad I:H_\psi I=179/540.
\]
Disjoint support and homogeneity yield
\[
 C_\rho=C_0+\rho C_\psi\succ0,\quad
 H_\rho=H_0+\rho H_\psi\succ0,\quad
 b_\rho=\sqrt\rho\,b_\psi,\quad c_\rho=3/2+5951/58800.       \tag{6.5}
\]
The fourth moment is the fixed number \(1/2+29023/1071630\).

### Theorem 6.1

Although \(H_\rho\to H_0\ne0\), \(b_\rho\to0\), and the limit field has zero optimized cubic loss,
\[
 \boxed{\lim_{\rho\downarrow0}\mathcal L_G(D\varphi_\rho)
 =\frac12\frac{(283/5670)^2}{179/540}
 =\frac{80089}{21313530}>0.}                               \tag{6.6}
\]
Furthermore,
\[
 \sqrt\rho\,(-H_\rho^{-1}b_\rho)\longrightarrow
 -\frac{566}{3759}I.                                      \tag{6.7}
\]
Thus optimizing over affine backgrounds does not commute with this concentrating limit. The effect persists after a constant normalization of the fourth moment to one; the limiting Hessian remains nonzero and has positive trace.

**Proof.** Resolve matrix space as \(\ker H_0\oplus(\ker H_0)^\perp\). On the one-dimensional kernel, the leading Hessian is \(\rho H_\psi\), while the cubic component is \(\sqrt\rho b_\psi\). The complementary block remains strictly positive. The elementary block inverse gives (6.6)-(6.7). Alternatively, the full rational expression checked independently is
\[
 \mathcal L_G(D\varphi_\rho)=
 \frac{12967042540131421\rho^3+153720203207188095\rho^2+
 481509250819516800\rho+330966608464224000}
 {39690(37733432214853\rho^3+511714179868320\rho^2+
 2009086057591200\rho+2219144560992000)}.                     \tag{6.8}
\]
The verifier checks positive leading minors of \(H_\rho\) as polynomials in \(\rho>0\), and the exact limit. QED.

The actual optimized gaps are **positive**. Their exact expression is
\[
 \frac{95402608462831612841\rho^3+1294668039088831776840\rho^2+
 5087991087990484250400\rho+5627997683834291424000}
 {1587600(37733432214853\rho^3+511714179868320\rho^2+
 2009086057591200\rho+2219144560992000)} >0.                 \tag{6.9}
\]
This construction disproves a vanishing/continuity extension for the Schur loss. It does not disprove quasiconvexity of \(G\), nor does it rule out estimates with equiintegrability or additional concentration data.

A simpler independent example exists even for the convex quartic \(u^2+v^2\): retain only the first output of \(\psi\). Then the same construction has loss exactly \(1/490\) for every \(\rho>0\), and zero at its limit. Its explicit moments are included in the verifier. The full-rank construction above avoids relying on that easier convex case.

## 7. Concentration scaling and an exact profile-defect operation

### 7.1 Pure concentration preserves the complete optimized gap

For any homogeneous quartic and any fixed zero-boundary profile, the scaling
\(\psi_\rho(x)=\rho^{1/2}\psi(x/\rho)\) in two spatial dimensions gives
\[
 C_\rho=\rho C,\quad H_\rho=\rho H,\quad
 b_\rho=\sqrt\rho b,\quad c_\rho=c,
\]
\[
 \boxed{\Delta_F(D\psi_\rho)=\Delta_F(D\psi).}              \tag{7.1}
\]
Every hypothetical negative-gap profile could therefore be placed arbitrarily close to the zero averaged Hessian without changing its optimized deficit. Small absolute Hessian norm, even with fixed fourth moment, cannot by itself make the full problem easier. Homogeneous concentration scaling is standard; related p-homogeneous concentration constructions are discussed in recent higher-dimensional work [5]. No novelty is claimed for the scaling principle itself.

### 7.2 Finite profile gluing with a nonzero singular background

Let a base gradient vanish on enough open regions to place finitely many disjoint profiles. Suppose its moments satisfy \(H_0\succeq0\), \(b_0=0\), and write \(N=\ker H_0\). Place profiles \(\psi_j\) at scales \(\rho\theta_j\), \(\theta_j>0\), with the same critical amplitude normalization. Then exactly
\[
 H_\rho=H_0+\rho\sum_j\theta_jH_j,\quad
 b_\rho=\sqrt\rho\sum_j\sqrt{\theta_j}b_j,\quad
 c_\rho=c_0+\sum_j c_j.                                   \tag{7.2}
\]
Put
\[
 K=P_N\left(\sum_j\theta_jH_j\right)P_N|_N,
 \qquad d=P_N\sum_j\sqrt{\theta_j}b_j,
\]
and assume \(K\succ0\) on \(N\). Then
\[
 \boxed{\lim_{\rho\downarrow0}\Delta_F(D\varphi_\rho)
 =c_0+\sum_jc_j-\tfrac12d^TK^{-1}d.}                        \tag{7.3}
\]
This is an exact compatible construction plus a block-inverse limit, not a conjectured profile decomposition for arbitrary sequences.

The defect obeys
\[
 d^TK^{-1}d\le\sum_j b_j^TH_j^\dagger b_j.                  \tag{7.4}
\]
Indeed, by (1.10), every \(b_j\) lies in \(\operatorname{ran}H_j\). The variational formula for the left side is
\[
 \sup_{v\in N}\sum_j[2\sqrt{\theta_j}b_j:v-\theta_jv:H_jv]
 \le\sum_j\sup_w[2b_j:w-w:H_jw].
\]
Consequently
\[
 \lim\Delta_F(D\varphi_\rho)\ge c_0+\sum_j\Delta_F(D\psi_j).\tag{7.5}
\]
Separate nonnegative profiles do not become a negative-gap construction simply by sharing a diverging affine background. The common-background quadratic coupling has the opposite inequality. The matrix inequality is ordinary quadratic duality and is not claimed as a new theorem of matrix analysis.

For any exact disjoint-support sum, even before taking a limit, \(\Delta\) is superadditive; this also follows immediately by taking an infimum of the sum of the individual background-gap functions. Its value here is in the explicit finite defect (7.3), which retains information discarded by the ordinary limiting pair \((H_0,b_0)\).

Nothing here proves that all sequences admit an error-controlled decomposition into such isolated profiles, or that the internal resonances of a profile have nonnegative gap.

## 8. Why determinant moments alone cannot replace compatibility

The following bounded law is **not** a compatible gradient construction.

For \(G\) in (5.1), set \(m=9\), \(\varepsilon=10^{-6}\),
\[
 S=\operatorname{diag}(1,3/2),\quad
 t=\frac{(9/2)m^2\varepsilon}{1-(3/2)\varepsilon},\quad
 R_t=\begin{pmatrix}0&1\\t&0\end{pmatrix}.
\]
Put probability \((1-3\varepsilon/2)/2\) at each of \(\pm R_t\), probability \(\varepsilon\) at \(mS\), and probability \(\varepsilon/2\) at \(-2mS\). The mean matrix and mean determinant are exactly zero. Its covariance has rank two and its averaged Hessian is positive definite. Exact arithmetic gives
\[
 I:H I=\frac{177147}{1599997600000},\qquad
 b:I=\frac{729}{800000},
\]
\[
 c-\frac{(b:I)^2}{2(I:H I)}
 =-\frac{11792123534471829388849317}
 {15999928000107999946000000}<0.                            \tag{8.1}
\]
The minimizing background within the line \(\mathbb RI\) has coefficient \(-1999997/243\).

The support lies in a two-dimensional matrix subspace. Any *actual* periodic gradient confined to such a subspace satisfies rank-one Jensen: either the subspace is entirely rank one, determinant balance reduces it to a rank-one line, or its rank-one cone has two lines and Fourier compatibility separates it into two independent phases. Thus (8.1) cannot be an actual gradient distribution. It is an exact test showing that determinant balance, covariance rank, a positive-definite Hessian, and bounded support are insufficient for the desired inequality.

With fixed \(m\) and \(\varepsilon\downarrow0\), the directional Schur loss tends to \(5m^2/108\), while \(c\to3\). The discontinuity is therefore possible for bounded *noncompatible* laws as well. This does not establish such discontinuity for uniformly bounded compatible sequences; Section 6 uses genuine concentration.

## 9. Actual compatible Fourier search

A second route searched directly for a compatible negative gap for the exactly certified \(G\). It used real finite Fourier potentials, cutoff three, a dealiased 13-by-13 periodic grid, six initializations, and 800 Adam steps per initialization, in double precision. The gradient fourth moment was normalized to one. Backgrounds were eliminated using \(H+10^{-9}I\); the displayed gaps were reevaluated with the unregularized polynomial expansion at the resulting backgrounds.

The smallest recorded value was approximately
\[
 1.1651868296208177.
\]
No negative gap was obtained. The nearly identical values from all starts indicate convergence to the same observed configuration, not a global lower bound. This is numerical search evidence only. The exact rank-one-convexity certificate for \(G\) is independent of this optimization. The script and raw JSON are retained under `exploration/` in the package.

The additional exploratory family used to discover the excluded nonshear tangent branch gave small negative matrix residuals. Those residuals were not used as an infeasibility proof. They were replaced by the analytic negative acoustic second-order coefficient (4.2), which tests an actual rank-one direction.

## 10. Literature comparison and exact boundary of the advance

The quadratic decomposition is the classical indefinite non-strict Finsler lemma [1]. Tartar-type cubic conditions and fourth-order resonant necessary conditions already have foundational literature: Gutiérrez [2] studies them explicitly for degree-four polynomials. Accordingly, neither differentiation at an acoustic zero nor cubic/quartic resonance testing is represented here as historically unprecedented. The specific two-contact classification, shear restriction, and optimized-loss examples require their own priority review.

Bruno and Pasqualotto [3] prove the Dacorogna-Marcellini result and the left-and-right-rotation-invariant quartic theorem using heat flow and exact differential corrections. No heat monotonicity assertion is a premise here.

Arroyo-Rabasa and Aussedat [4] study quantified compensated compactness for A-free measures on cones separated from the wave cone. Such ellipticity/cone hypotheses do not remove the present rank-one concentration mechanism. Their L1 concentration statements are not silently imported as L4 Schur-loss estimates.

Recent work of Cassese [5] produces counterexamples in larger matrix spaces and discusses p-homogeneous concentration. It does not give a planar 2-by-2 counterexample. No higher-dimensional construction is transferred here without preserving dimensions and gradient compatibility.

What is established is a sharper full-cone rigidity theorem, a local acoustic modulus controlling second-moment conditioning, a determinant-preserving contact-shear operation, and a compatible concentration defect showing why the ordinary minimized moment expression is unstable at singularity.

The complete inequality
\[
 c_F\ge\tfrac12 b_F^TH^{-1}b_F
\]
for every compatible positive-definite instance remains unproved. The missing operation must retain both the finite concentration defect and the correlations among resonant gradients, or else produce an exact compatible violation. Straightening a contact shear creates a spatially varying rank-one-convex energy; no valid argument currently averages away that dependence. Likewise, the finite gluing formula does not prove a general profile decomposition or positivity of the unresolved individual profiles.

### References

[1] T. J. Meijer et al., *A General Non-Strict Finsler's Lemma*, arXiv:2403.10306v1 (2024). https://arxiv.org/html/2403.10306v1

[2] S. Gutiérrez, *A Necessary Condition for the Quasiconvexity of Polynomials of Degree Four*, Journal of Convex Analysis 13 (2006), 51-60. https://www.heldermann-verlag.de/jca/jca13/jca0514_b.pdf

[3] G. Bruno and F. Pasqualotto, *Quasiconvexity for the Dacorogna-Marcellini Energy*, arXiv:2608.06367v1 (2026). https://arxiv.org/html/2608.06367v1

[4] A. Arroyo-Rabasa and A. Aussedat, *Quantified rigidity of A-free Young measure concentrations*, arXiv:2606.16762v2 (2026). An earlier retrieved rendering used the title *Compensated compactness of A-free measures on cones with quantified aperture*. https://arxiv.org/pdf/2606.16762

[5] G. Cassese, *A solution to Morrey's problem in R^{2 x m}*, arXiv:2608.03488 (2026), retrieved manuscript. https://arxiv.org/pdf/2608.03488

[6] A. Guerra and R. Teixeira da Costa, *Numerical evidence towards a positive answer to Morrey's problem*, arXiv:2006.09063. https://arxiv.org/html/2006.09063v1

[7] Prior conversation artifact, *ASTRA Meta-Genesis: nullspace closure and full-cone quartic rigidity*, 14 October 2026. Its foundation is reconstructed in Sections 1-2, and its exact checker was rerun. It remains internally supported rather than externally validated.

## 11. Reproduction

Run

```bash
python verify_positive_definite.py
```

The script verifies the all-35-coefficient polarization identities, the dimension-nine invariant basis, the finite calculations in the two-contact proof, the joint acoustic shear obstruction, the explicit rank-one-convex/non-polyconvex tangent integrand, exact compatible concentration moments, the nonzero optimized-loss limit, and the distinct noncompatible negative-gap law. It writes `positive_definite_verification.json`.

The JSON, script, and this note are sufficient for the finite checks. Exploratory optimizer output is not an input to verification. The analytic compactness, Finsler, nullspace, support, change-of-variables, and block-limit arguments are proved in the note, not delegated to a finite test. No full proof-assistant check, external mathematical review, novelty clearance, or repository publication is claimed.
