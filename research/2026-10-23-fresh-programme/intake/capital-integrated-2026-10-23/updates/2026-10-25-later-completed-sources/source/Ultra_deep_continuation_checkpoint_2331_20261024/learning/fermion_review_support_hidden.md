# Bounded audit: scalar pair-count real roots and near-mean mass

## Verdict

PASS for the hard-endpoint scalar polynomial in §5, for every complex \(n\times n\) matrix \(F\). The principal-minor average and stability argument is algebraically consistent, including rank-deficient \(F\) and the constant-polynomial case. The near-mean lemma gives the stated \(3/[4(m+1)^2]\) lower bound for an integer \(k\in\{0,\dots,m\}\) when the Poisson-binomial mean is within \(1/4\) of \(k\). The proof does not by itself establish multivariate occupation stability, a hard-configuration sampler, or real-rootedness for additional onsite weights not represented in this scalar identity.

## Independent derivation of the scalar polynomial

Let \(H=\begin{psmallmatrix}0&2F\\2F^*&0\end{psmallmatrix}\), which is Hermitian for arbitrary complex \(F\). For \(A\subseteq[n]\), the selected principal set \(S_A=U_A\cup V_{A^c}\) has size \(n\). In a principal minor of \(H[S_A]\), a nonzero determinant must select the same number \(k\) of \(U\)- and \(V\)-indices. If their label sets are \(I\subseteq A\) and \(J\subseteq A^c\), the block determinant is

\[
\det\begin{pmatrix}0&2F[I,J]\\2F[I,J]^*&0\end{pmatrix}
 =(-1)^k4^k|\det F[I,J]|^2.
\]

The characteristic-polynomial sign contributes \((-1)^{2k}=1\), so the coefficient is \((-1)^k4^k|\det F[I,J]|^2\). A fixed pair \((I,J)\) occurs in a uniform \(A\) exactly when \(I\subseteq A\) and \(J\subseteq A^c\); this is impossible if \(I\cap J\ne\varnothing\), and otherwise has probability \(2^{-2k}\). The factor cancels \(4^k\). Thus

\[
2^{-n}\sum_A\det(xI-H[S_A])
 =\sum_k(-1)^k c_kx^{n-2k}
 =x^nZ(-1/x^2),\qquad
c_k=\sum_{\substack{|I|=|J|=k\\I\cap J=\varnothing}}|\det F[I,J]|^2.
\]

In particular \(c_k\ge0\), \(c_0=1\), and \(Z\) is nonzero. In the physical \(2m\)-site case the degree is at most \(m\); for general \(n\) it is at most \(\lfloor n/2\rfloor\), since \(I,J\) must be disjoint.

## Stability and zero-polynomial boundary

The multiaffine polynomial \(p(y)=\det(\operatorname{diag}(y)-H)\) has real coefficients and is real stable: if every \(\operatorname{Im} y_j>0\), a null vector would contradict the strictly positive imaginary part of \(v^*\operatorname{diag}(y)v\), since \(v^*Hv\) is real. Applying \(\prod_i(\partial_{U_i}+\partial_{V_i})\) is a sequence of positive-direction derivatives and preserves real stability unless the result is zero. Its top-degree monomial \(\prod_j y_j\) gives a positive \(x^n\) coefficient after diagonal specialization (equal to \(2^n\) before averaging), so the result cannot be zero. Differentiation selects complements of the \(S_A\), which are the same family under \(A\leftrightarrow A^c\); diagonal specialization gives the averaged characteristic polynomial above. A univariate real stable polynomial with real coefficients is real-rooted.

For any root \(z\) of \(Z\), \(z\ne0\) because \(Z(0)=1\). Choose a nonzero complex \(x\) with \(x^2=-1/z\). Then \(x^nZ(-1/x^2)=0\). The averaged characteristic polynomial is real-rooted, so this nonzero \(x\) is real and \(z=-1/x^2<0\). Rank deficiency or missing high coefficients may make the averaged characteristic polynomial have a zero at \(x=0\); that factor corresponds only to missing top degree and does not create a zero of \(Z\). If \(Z\equiv1\), the root claim is vacuous and the mass lemma is immediate for the only compatible target \(k=0\).

## Near-mean mass lemma

Factor a nonconstant \(Z\) with constant term one as

\[
Z(t)=\prod_{\ell=1}^{s}(1+t/\rho_\ell),\qquad \rho_\ell>0.
\]

For \(r>0\),

\[
\frac{Z(rt)}{Z(r)}=\prod_{\ell=1}^s\bigl((1-p_\ell)+p_\ell t\bigr),
\qquad p_\ell=\frac r{r+\rho_\ell}.
\]

Thus \(K\) is a sum of at most \(m\) independent Bernoulli variables (pad with zero variables if \(s<m\)); its mass sequence is unimodal, and \(\mu=\mathbb E K\). Let \(p_j=\Pr(K=j)\).

If a mode lies left of \(k\), then \(p_j\le p_k\) for \(j\ge k\). With \(L=m-k+1\),

\[
\mu\le k-1+\sum_{j=k}^m(j-k+1)p_j
\le k-1+\frac{L(L+1)}2p_k
\le k-1+L^2p_k.
\]

The lower mean bound \(\mu\ge k-1/4\) gives \(p_k\ge3/(4L^2)\ge3/[4(m+1)^2]\). If a mode lies right of \(k\), apply the same argument to \(m-K\) and target \(m-k\), using \(|\mathbb E(m-K)-(m-k)|\le1/4\). If \(k\) is a mode, \(p_k\ge1/(m+1)\), which is stronger. The endpoint cases are covered by the reflection or the mode case; a mode-left case cannot occur at \(k=0\). This proves the claimed lower bound without requiring roots as input.

The logical scope is exactly the scalar hard-endpoint pair-count polynomial. Any extension to a non-hard onsite filter needs its own stability-preserving construction or the cited prior theorem; it does not follow from the displayed principal-minor average alone.
