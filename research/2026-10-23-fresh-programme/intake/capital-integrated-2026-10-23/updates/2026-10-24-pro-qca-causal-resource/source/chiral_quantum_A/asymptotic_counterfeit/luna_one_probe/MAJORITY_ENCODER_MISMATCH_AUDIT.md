# Odd-block majority encoder: mismatch audit

## One-period law

Fix \(L=2m+1\), and let the input bits in each block be iid Bernoulli\((p)\), with \(0<p<1/2\). The map
\[
x\longmapsto(q,s_1,\ldots,s_{L-1}),\qquad
q=\operatorname{Maj}(x),\quad s_j=x_j\oplus x_{j+1},
\]
is a bijection without extra workspace. Given \(s\), choosing \(x_1\) determines all of \(x\); the other possible string is \(\bar x\). Since \(L\) is odd, \(\operatorname{Maj}(\bar x)=1-\operatorname{Maj}(x)\), so \(q\) selects exactly one of the two strings.

Write \(X_k\) for input block \(k\), \(Q_k=\operatorname{Maj}(X_k)\), and \(S_k\) for its syndrome. In the co-moving frame of the reference fine shift, \(\sigma_{\rm right}^{-1}\Omega_L=P_L^\dagger C_{\rm left}P_L\). Up to the chosen shift orientation, decoding block \(k\) keeps \(S_k\) and replaces \(Q_k\) by the independent neighboring label \(Q_{k+1}\). The two inverse strings with syndrome \(S_k\) are \(X_k\) and \(\bar X_k\). Hence
\[
Y_k=
\begin{cases}
X_k,&Q_{k+1}=Q_k,\\
\bar X_k,&Q_{k+1}\ne Q_k.
\end{cases}
\]
Thus the block mismatch event is \(D_k=\mathbf 1\{Q_{k+1}\ne Q_k\}\), and on that event all \(L\) fine bits mismatch the reference; otherwise none do. The labels \(Q_k\) are iid Bernoulli\((\epsilon_L)\), where
\[
\epsilon_L=\Pr\!\left[\operatorname{Bin}(L,p)\ge m+1\right].
\]
For every fine coordinate \(j\), the **joint** mismatch probability is therefore exactly
\[
\Pr(Y_{k,j}\ne X_{k,j})
=\Pr(D_k=1)
=2\epsilon_L(1-\epsilon_L).
\]
This is relative to the reference fine translation \(\sigma_{\rm right}\); it is not the mismatch probability against the unshifted input at the same laboratory site.

## Per-label error

Let \(b=X_{k,j}\in\{0,1\}\). The neighboring majority \(Q_{k+1}\) is independent of \((X_k,S_k)\), but \(Q_k\) is correlated with this bit. Put
\[
r_1=\Pr(Q_k=1\mid X_{k,j}=1)
=\Pr[\operatorname{Bin}(2m,p)\ge m],\qquad
r_0=\Pr(Q_k=1\mid X_{k,j}=0)
=\Pr[\operatorname{Bin}(2m,p)\ge m+1].
\]
Then \(\epsilon_L=pr_1+(1-p)r_0\). The conditional and joint per-label mismatch probabilities are
\[
e_b:=\Pr(D_k=1\mid X_{k,j}=b)
=\epsilon_L+(1-2\epsilon_L)r_b,\qquad
e_b^{\rm joint}:=\Pr(X_{k,j}=b,D_k=1)=\Pr(X_{k,j}=b)e_b.
\]
In particular \(p e_1+(1-p)e_0=2\epsilon_L(1-\epsilon_L)\). The conditional errors are not equal to the joint error and are not equal across labels at finite \(L\); this distinction matters if the tag contract conditions on a particular input label.

For \(\rho=2\sqrt{p(1-p)}<1\), the Chernoff bound gives \(\epsilon_L\le\rho^L\). Also \(r_1,r_0\le\rho^{L-1}\), by applying the same half-threshold bound to the remaining \(L-1\) bits. Since \(0<\epsilon_L<1/2\),
\[
e_b\le \epsilon_L+r_b\le \rho^L+\rho^{L-1}.
\]
So both label-conditioned errors, as well as their joint weights, vanish exponentially for each fixed \(p<1/2\). The exponent is not uniform as \(p\uparrow1/2\): \(-\log\rho\to0\). At \(p=1/2\), \(\epsilon_L=1/2\), \(e_0=e_1=1/2\), and every fine site has mismatch \(1/2\). More generally, if \(p_L=1/2-c/\sqrt L\) with fixed \(c\ge0\), the binomial central limit gives \(\epsilon_L,r_0,r_1\to q:=\Phi(-2c)\); hence both conditional errors tend to \(2q(1-q)\), and the per-site mismatch has that same nonzero limit for finite \(c\).

Thus the raw per-label and joint tag mismatches vanish for fixed \(p\). If a separate contract uses a support-size eigenvalue floor \(p^{m_A}\) to turn a mismatch expectation into an operator-norm guarantee, that quotient needs its own estimate: the encoder radius grows with \(L\), and the Chernoff bound alone does not show \(e_b^{\rm joint}/p^{m_A}\to0\).

## Scope

This is an exact one-period statement for a fresh product preparation and a per-site classical tag comparison. Within each block the mismatch indicators are perfectly correlated. On an \(N\)-block periodic ring, the block mismatch flags are \(D_k=Q_{k+1}\oplus Q_k\), with \(\bigoplus_kD_k=0\), and
\[
\mathbb E\!\left[\sum_k D_k\right]=2N\epsilon_L(1-\epsilon_L),\qquad
\Pr(\text{at least one block changes})=1-\epsilon_L^N-(1-\epsilon_L)^N.
\]
For fixed \(L\) and \(0<\epsilon_L<1\), the latter tends to one as \(N\to\infty\). Thus the small per-site error does not give a system-size-uniform guarantee that the coupled input/output record is unchanged. This coupled mismatch probability is not itself the total-variation distance between the input and output marginals; any full-record total-variation claim needs a separate argument.

After one period the physical blocks are correlated, so the fresh-iid derivation cannot be reapplied to repeated periods. No repeated-cycle, stationary-source, global-record, or arbitrary-input quantum-channel approximation follows. The reversible encoder uses the \(L\) physical bits as its full workspace; no pure ancilla is assumed. This audit proves the mismatch law only and does not establish a fixed-time nearest-neighbor Hamiltonian implementation or its cost.

## Balanced-code lower bound and ideal cyclic work

For any reversible encoder onto one binary register \(q\) and \(L-1\) syndrome bits, exactly \(2^{L-1}\) input strings have each \(q\)-label. When \(p<1/2\), a string's Bernoulli probability decreases with its Hamming weight. Since \(L\) is odd, the least-probable half of the strings is exactly the set with more than \(L/2\) ones. Therefore, for every such encoder,
\[
\min\{\Pr(q=0),\Pr(q=1)\}\ge\epsilon_L.
\]
For iid input blocks, the \(q\)-labels in distinct blocks are independent. If their bias is \(u=\Pr(q=1)\), an adjacent-label replacement changes a block with probability \(2u(1-u)\ge2\epsilon_L(1-\epsilon_L)\). At such a change the two inverse strings for the same syndrome must be distinct, so at least one fine bit changes. Hence the period-averaged fine-bit mismatch for any encoder in this class is at least \(2\epsilon_L(1-\epsilon_L)/L\). The majority/domain-wall code attains \(2\epsilon_L(1-\epsilon_L)\) at every bit by making the two inverse strings complements.

The first term in the majority tail also gives a matching exponential lower bound:
\[
\epsilon_L\ge {L\choose (L+1)/2}p^{(L+1)/2}(1-p)^{(L-1)/2}
\ge \frac{1}{L+1}\sqrt{\frac{p}{1-p}}\,[2\sqrt{p(1-p)}]^L.
\]
The last step uses that the central binomial coefficient is the maximum among the \(L+1\) coefficients and is therefore at least \(2^L/(L+1)\). Together with the Chernoff upper bound, this pins the exponential rate within this balanced single-register code class, up to polynomial factors; it is not a lower bound over arbitrary QCAs.

For an ideal cyclic unitary on a compatible finite ring, take
\[
H_0=\Delta\sum_{i=1}^N |1\rangle_i\langle1|,\qquad
\tau_p=\bigotimes_i\bigl((1-p)|0\rangle\langle0|+p|1\rangle\langle1|\bigr),
\quad \Delta=k_BT\log\frac{1-p}{p}.
\]
Then \(\tau_p\) is Gibbs for \(H_0\). Cyclicity and Gibbs passivity give net work \(W=\operatorname{Tr}H_0(U\tau_pU^\dagger-\tau_p)\ge0\). For the upper bound, couple the initial bits to the reference-shifted output bits. The reference shift preserves the initial energy, and a bit's occupation can increase by at most its mismatch indicator. Thus
\[
0\le \frac{W}{N}\le\Delta\,e_{\rm site}
=2\Delta\,\epsilon_L(1-\epsilon_L).
\]
This is a net cyclic-work bound only; it does not price the controls, clock, synthesis, dissipation, or refrigeration. It also does not change the fresh-preparation scope: the post-period state is generally correlated, so the iid law and work estimate cannot simply be iterated as a repeated-cycle claim.
