# Focused check: coherent-input depth drift and product stationarity

Reviewer: `/root/stopping_converse`  
Date: 21 October 2026  
Scope: the new one-step drift identity, its domain and coherence bound, and the proposed exact-product-stationarity obstruction. This is a short distinct check, not another review of the capacity-floor theorem.

## Verdict

The proposed drift sign, coefficients, and coherence bound are correct. The exact-product-stationarity obstruction is also correct for \(\alpha\ne0\). One domain qualification is necessary: for a normal bath state of infinite mean depth, the bounded increment has a well-defined expectation, but an ordinary expression \(\infty-\infty\) must not be used. The increment equals a limit of differences of capped-depth expectations.

## 1. Operators and bounded increment

In the two-seed Fock representation, let \(P_0\) project onto the two root seeds, \(R_0\) swap those seeds and vanish elsewhere, and \(S_a\), \(a=1,2\), append color \(a\). Then

\[
S_a^\dagger S_b=\delta_{ab}I,
\qquad\sum_aS_aS_a^\dagger=I-P_0,
\]

and the fixed edge reversal is

\[
U=|0\rangle\langle0|\otimes R_0
+\sum_{a=1}^2\left(|0\rangle\langle a|\otimes S_a
+|a\rangle\langle0|\otimes S_a^\dagger\right).
\]

Let \(L\) be Fock word length. Its finite-support core satisfies
\([L,S_a]=S_a\), \([L,S_a^\dagger]=-S_a^\dagger\), and \([L,R_0]=0\). These shifts preserve \(\operatorname{Dom}L\), so \(U\) and \(V_s=\alpha U+i\beta I\) do also. Assume real \(\alpha,\beta\) with \(\alpha^2+\beta^2=1\).

Direct multiplication gives

\[
D:=U(I\otimes L)U-I\otimes L
=(I-2|0\rangle\langle0|)\otimes I
+|0\rangle\langle0|\otimes P_0.
\]

The \(00\) block is \(-I+P_0\); each nonzero color block is \(+I\). Expanding the perturbed unitary gives

\[
\boxed{
K:=V_s^\dagger(I\otimes L)V_s-I\otimes L
=\alpha^2D
+i\alpha\beta\sum_{a=1}^2
\left(-|0\rangle\langle a|\otimes S_a
+|a\rangle\langle0|\otimes S_a^\dagger\right).
}
\]

This is first an equality on \(\operatorname{Dom}L\), with a bounded self-adjoint right side. In fact \(UDU=-D\), the cross term is \(i\alpha\beta DU\), and

\[
K^2=\alpha^2D^2
=\alpha^2(I-|0\rangle\langle0|\otimes P_0),
\qquad\|K\|=|\alpha|.
\]

For \(L_M=\min\{L,M\}\), the same argument with \(D_M=U(I\otimes L_M)U-I\otimes L_M\) gives \(\|V_s^\dagger(I\otimes L_M)V_s-I\otimes L_M\|\le|\alpha|\). These bounded increments converge strongly to \(K\). Their expectations consequently converge against every normal trace-class density.

If \(\operatorname{Tr}\tau L<\infty\), the formula is the ordinary change of mean depth, and the final mean is also finite. For arbitrary normal \(\tau\), define the bounded-increment expectation directly, or equivalently as the limit of capped-depth differences. Neither normality nor the present identity licenses subtracting two infinite mean depths.

## 2. Product-input drift and its sign

For a product input \(\rho\otimes\tau\), put

\[
q=\rho_{00},\quad p_0=\operatorname{Tr}(\tau P_0),\quad
\gamma=(\rho_{10},\rho_{20}),\quad
x=\sum_{a=1}^2\rho_{a0}\operatorname{Tr}(\tau S_a).
\]

The relevant matrix traces are \(\operatorname{Tr}(\rho|0\rangle\langle a|)=\rho_{a0}\) and \(\operatorname{Tr}(\rho|a\rangle\langle0|)=\rho_{0a}\). Thus the cross term is
\(i\alpha\beta(-x+\overline x)=+2\alpha\beta\operatorname{Im}x\). Therefore

\[
\boxed{
\operatorname{Tr}[(\rho\otimes\tau)K]
=\alpha^2(1-2q+qp_0)+2\alpha\beta\operatorname{Im}x.
}
\]

The plus sign in front of \(\operatorname{Im}x\) is correct for the stated convention \(V_s=\alpha U+i\beta I\) and \(\gamma_a=\rho_{a0}\).

For each \(a\), Hilbert--Schmidt Cauchy--Schwarz gives

\[
|\operatorname{Tr}(\tau S_a)|^2
=|\langle S_a^\dagger\tau^{1/2},\tau^{1/2}\rangle_{\rm HS}|^2
\le\operatorname{Tr}(\tau S_aS_a^\dagger).
\]

Summing and applying ordinary Cauchy--Schwarz proves the requested bound

\[
\boxed{|x|\le\|\gamma\|_2\sqrt{1-p_0}.}
\]

Positivity of the port density also implies \(\|\gamma\|_2^2\le q(1-q)\), by the Schur complement of its \(00\) block, with the endpoints handled directly. Hence one useful necessary bound is

\[
\operatorname{Tr}[(\rho\otimes\tau)K]
\ge\alpha^2(1-2q+qp_0)
-2|\alpha\beta|\sqrt{q(1-q)(1-p_0)}.
\]

For \(q<1/2\) and \(\alpha\beta\ne0\), exact cancellation of this one-step drift therefore requires sufficiently large coherences with the appropriate phase. This is a necessary scalar condition only. It supplies neither a normal stationary bath nor a quantum communication rate.

## 3. Equivalence of exact product stationarity

For any bounded density \(X=\rho\otimes\tau\), unitarity gives

\[
V_sXV_s^\dagger=X
\quad\Longleftrightarrow\quad[V_s,X]=0.
\]

Since \([V_s,X]=\alpha[U,X]\), for **\(\alpha\ne0\)** this is equivalent to \([U,X]=0\), hence to

\[
UXU=X.
\]

There is no additional condition on \(\beta\). The exceptional case \(\alpha=0\) is different: \(V_s\) is a scalar multiple of identity, so every product density is stationary. That exception must remain explicit.

## 4. Normal product stationarity forces low input entropy

Suppose \(UXU=X\), with \(\tau\) a normal density and \(\rho\) any port density. Comparing the color blocks \(a,b\in\{1,2\}\) gives exactly

\[
qS_a^\dagger\tau S_b=\rho_{ab}\tau.
\]

The case \(q=0\) is impossible: the diagonal equations would force \(\rho_{11}=\rho_{22}=0\), contradicting \(\operatorname{Tr}\rho=1\). Summing the diagonal color equations gives

\[
q\sum_aS_a^\dagger\tau S_a=(1-q)\tau.
\]

Let \(P_j\) project onto Fock depth \(j\), and write \(m_j=\operatorname{Tr}(\tau P_j)\). Since \(\sum_a S_aP_jS_a^\dagger=P_{j+1}\),

\[
qm_{j+1}=(1-q)m_j.
\]

If \(m_0=0\), every \(m_j\) vanishes, contradicting normality and trace one because \(\sum_jP_j=I\) strongly. Thus \(m_0>0\), and the geometric sequence is summable only when

\[
\boxed{q>1/2.}
\]

More explicitly, with \(\lambda=(1-q)/q<1\), \(m_j=(1-\lambda)\lambda^j\) and \(m_0=(2q-1)/q\). No faithfulness or finite-entropy assumption on \(\tau\) was needed.

For a three-dimensional port density with fixed \(\rho_{00}=q\), let \(H(\rho)=-\operatorname{Tr}(\rho\log_2\rho)\) denote von Neumann entropy in bits. Pinching between the zero and color sectors and maximizing the color-block entropy gives

\[
H(\rho)\le h_2(q)+(1-q)\log_2 2=h_2(q)+1-q.
\]

This expression equals \(3/2\) at \(q=1/2\) and is strictly decreasing for \(q>1/2\). Therefore

\[
\boxed{H(\rho)<3/2}
\]

for every normal exactly product-stationary input/bath pair when \(\alpha\ne0\). Coherent port entries do not evade this obstruction; they cannot increase entropy above the pinched maximizer at fixed \(q\).

## Interpretation for the proposed next operation

The drift identity leaves open a weaker marginal stationary or otherwise controlled coherent-bath mechanism. The exact product-stationarity route cannot supply input entropy above \(3/2\) for a nontrivial \(\alpha\ne0\) device. It follows neither that every high-entropy coherent input has positive long-run drift nor that a zero one-step drift condition yields a high-rate code. The established capacity-floor theorem and its sources are unchanged.

This check is analytic; no old numerical replay or broad literature audit was performed. It is internal verification, not external certification or a historical-priority claim.
