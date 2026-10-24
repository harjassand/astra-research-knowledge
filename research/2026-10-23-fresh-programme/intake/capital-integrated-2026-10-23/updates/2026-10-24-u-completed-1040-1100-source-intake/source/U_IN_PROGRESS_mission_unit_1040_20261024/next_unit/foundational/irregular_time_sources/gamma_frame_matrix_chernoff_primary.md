# Gamma-frame concentration: exact matrix Chernoff import

Status: bounded primary-source pin, 2026-10-24. This records the finite-dimensional concentration step and its dependence assumptions; it does not establish the random-frame construction or assert novelty.

## Primary theorem and direct specialization

Joel A. Tropp, “User-Friendly Tail Bounds for Sums of Random Matrices,” *Foundations of Computational Mathematics* 12 (2012), 389–434; author-hosted preprint [PDF](https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf). The precise convenient statement is Corollary 5.2 (Matrix Chernoff II), pp. 20–21 of the preprint. It assumes a finite sequence of independent random self-adjoint \(d\)-by-\(d\) matrices \(X_j\) with \(X_j\succeq0\) and \(\lambda_{\max}(X_j)\le R\) almost surely. Writing
\[
\mu_{\min}=\lambda_{\min}\!\left(\sum_j\mathbb E X_j\right),\qquad
\mu_{\max}=\lambda_{\max}\!\left(\sum_j\mathbb E X_j\right),
\]
it gives
\[
\Pr\!\left\{\lambda_{\min}\!\left(\sum_jX_j\right)\le(1-\delta)\mu_{\min}\right\}
\le d\left(\frac{e^{-\delta}}{(1-\delta)^{1-\delta}}\right)^{\mu_{\min}/R}
\quad (0\le\delta\le1),
\]
and
\[
\Pr\!\left\{\lambda_{\max}\!\left(\sum_jX_j\right)\ge(1+\delta)\mu_{\max}\right\}
\le d\left(\frac{e^\delta}{(1+\delta)^{1+\delta}}\right)^{\mu_{\max}/R}
\quad (\delta\ge0).
\]
Theorem 5.1 is a stronger information-divergence form. Remark 5.4 explicitly explains the rank-one/independent-column application \(\sum_j z_jz_j^*\), with independent random columns. Tropp also notes in Remark 5.6 that the dimension factor cannot in general be removed.

For one frame \(F_x=(kMq)^{-1}\sum_{r=1}^{kM}v_rv_r^*\), put
\[
X_{x,r}=(kMq)^{-1}v_rv_r^*.
\]
The stated frame assumptions must imply, for each fixed \(x\):

* the \(kM\) matrices \(X_{x,r}\) are independent random matrices;
* \(X_{x,r}\succeq0\) and \(\|X_{x,r}\|\le 1/(kq)\) almost surely (for example, \(\|v_r\|^2\le M\));
* \(\sum_r\mathbb E X_{x,r}=\mathbb E F_x=I_d\).

Then \(R=1/(kq)\) and \(\mu_{\min}=\mu_{\max}=1\). For \(0<\delta<1\), define
\[
h_-(\delta)=\delta+(1-\delta)\log(1-\delta),\qquad
h_+(\delta)=(1+\delta)\log(1+\delta)-\delta.
\]
The exact corollary yields
\[
\Pr\{\lambda_{\min}(F_x)\le1-\delta\}\le d\,e^{-kq h_-(\delta)},\qquad
\Pr\{\lambda_{\max}(F_x)\ge1+\delta\}\le d\,e^{-kq h_+(\delta)}.
\]
Thus a two-sided operator-norm frame guarantee has failure probability at most
\[
d\big(e^{-kq h_-(\delta)}+e^{-kq h_+(\delta)}\big)
\]
for this frame. For small \(\delta\), both rate functions are \(\delta^2/2+O(\delta^3)\); a convenient sufficient scaling is \(kq\gtrsim 2\delta^{-2}\log(d/\eta)\) for one-sided failure \(\eta\), with the exact rate functions above preferred for constants.

## Simultaneous frames and score operators

For any finite list \(\mathcal E\) of events, a union bound multiplies the relevant individual tail bound by \(|\mathcal E|\). It requires no independence between events. In particular, for \(k\) frames of common dimension \(d\),
\[
\Pr\{\text{some frame has }\lambda_{\min}\le1-\delta\}
\le kd\,e^{-kq h_-(\delta)}.
\]
If there are also \(N\) candidate score-operator events and each has the same applicable Chernoff bound, the generic factor is \(kN d\) when there is one event per frame-candidate pair; use \(Nd\) or \(kd\) if the index set is only candidates or only frames. If candidate operators are scalar, their matrix dimension is \(d=1\) for their individual bounds. Correlation among candidates within a row does not affect this union bound.

The matrix-Chernoff theorem does require independence of the summands *within the particular sum to which it is applied*. “Rows are independent” suffices to apply the theorem to a fixed candidate's sum over rows, even if different candidates are dependent within each row. But it does not establish a Chernoff bound for a sum of dependent terms inside a row/frame. Likewise, shared \(\Gamma\)-entries across distinct frames can make the frames dependent; this is harmless for the union bound, but only after each individual frame's within-sum independence has been proved. Independent mean-zero phases can help establish \(\mathbb E F_x=I\); they do not by themselves imply independence of rank-one summands if those summands reuse the same Bernoulli entries.

The problem statement's “\(kM\) independent rank-one terms” is therefore exactly the needed within-frame hypothesis if meant literally. Verify it against the index map \((x,i,y)\mapsto(s,t)\): each rank-one summand may have internally dependent coordinates, but two summands in a fixed Chernoff sum must be independent random matrices. If this fails, Corollary 5.2 cannot be applied as written; a dependency-robust theorem or a different grouping is needed.

## Frame whitening is elementary algebra

If \(G=\sum_r v_rv_r^*\succ0\), then \(w_r=G^{-1/2}v_r\) obeys
\[
\sum_rw_rw_r^*=G^{-1/2}GG^{-1/2}=I.
\]
Consequently the rank-one effects \(E_r=w_rw_r^*\) form a POVM. If the convention is \(F=cG=c\sum_r v_rv_r^*\), use \(w_r=\sqrt c\,F^{-1/2}v_r\); then \(\sum_r w_rw_r^*=I\). In particular, for \(c=(kMq)^{-1}\), the normalized vector is \((kMq)^{-1/2}F^{-1/2}v_r\). This identity is all that is needed for the frame-to-POVM normalization. HJW concerns which ensembles of a fixed state can be generated by measurements on a purification; it is not needed to prove this whitening identity.
