# Sampling a low-activity history gas with weak soft interactions

This lemma supplies the sampling step after an inverse-noise cluster expansion produces small summable effective potentials. It extends the accepted positive-history-polymer sampler; it does not assume that the perturbed law remains a factorized polymer gas.

## Setup

Let G be the accepted bounded-degree history graph, augmented by bounded-degree physical-check adjacency if needed. Its degree is D. A polymer gamma is a connected nonzero history assignment, with support V(gamma), size |gamma|, and energy E(gamma) >= a |gamma|. Distinct polymers in a configuration are compatible when their supports have graph distance at least two. Let h_X denote the history assembled from a compatible collection X.

The perturbed law has weight

\[
W(X)=\exp\left[-\beta\sum_{\gamma\in X}E(\gamma)+U(h_X)\right],\qquad
U(h)=\sum_A\phi_A(h|_A).
\]

The potential scopes A can be arbitrary finite subsets of history vertices. Define

\[
\xi=\sup_x\sum_{A\ni x}|A|\|\phi_A\|_\infty<\infty,
\quad b=\beta a-2\xi,
\quad Q(b)=\sup_x\sum_{\gamma\ni x}|\gamma|e^{-b|\gamma|}.
\]

All series can first be finite and then be taken to the absolutely convergent limit. Suppose

\[
\theta=[D+1+4\xi]Q(b)<1.
\tag{1}
\]

This condition holds at sufficiently low temperature for sufficiently small fixed xi. If there are at most c^m polymers of size m containing a specified vertex, then Q(b) <= sum_{m>=1} m c^m e^{-bm}.

## Theorem

Fix a size cutoff L and enumerate all K polymers of size at most L. Consider the single-occupancy heat-bath chain: select one polymer eta uniformly; conditional on the other occupations, set it absent if incompatible with an occupied polymer, and otherwise set it present with odds

\[
r_\eta(X)=\exp[-\beta E(\eta)+U(h_{X\cup\eta})-U(h_X)].
\]

The chain is irreducible, reversible for the truncated positive law, and contracts weighted Hamming distance by a factor at most

\[
1-\frac{1-\theta}{K}
\]

per update. Starting from the empty configuration, its mixing time to TV error delta is at most

\[
\frac{K}{1-\theta}\log\frac{N}{\delta}
\]

up to rounding, where N is the number of history vertices. The omitted-polymer probability under the full law is at most

\[
N\sum_{m>L}c^m e^{-bm}.
\tag{2}
\]

Hence L=O(log(N/delta)) makes truncation error O(delta); bounded-degree enumeration makes K polynomial in N/delta. If potential differences can be evaluated to inverse-polynomial additive precision in polynomial time, this is a polynomial sampler.

## Proof

Adding gamma changes only potentials whose scopes intersect its support. Thus

\[
|U(h_{X\cup\gamma})-U(h_X)|
\le2\sum_{A:A\cap V(\gamma)\ne\varnothing}\|\phi_A\|_\infty
\le2\xi|\gamma|.
\]

Therefore every allowed insertion odds is bounded by e^{-b|gamma|}. Deletion of a specified occupied gamma maps injectively to legal configurations without it, and the ratio of weights is at most e^{-b|gamma|}. Its marginal inclusion probability is at most this same bound. Counting anchored polymers proves (2); no independence of their occupations is needed.

For the mixing claim use distance d(X,Y)=sum_{gamma in X symmetric-difference Y}|gamma|. Compatible sets form a path-connected graph under insertion/deletion, and this distance equals the induced shortest-path metric: remove X\\Y first, then insert Y\\X. Consider adjacent configurations differing only by gamma_0 and use the same selected update polymer eta and maximal Bernoulli coupling.

Updating gamma_0 removes the disagreement exactly, since the conditional exterior configuration is the same. If eta conflicts with gamma_0, the chance of creating a disagreement is at most e^{-b|eta|}. If eta is compatible with gamma_0, its log-odds difference is bounded by the mixed variation

\[
d_{\eta,\gamma_0}
\le4\sum_{A:A\cap V(\eta)\ne\varnothing,\ A\cap V(\gamma_0)\ne\varnothing}
\|\phi_A\|_\infty.
\]

The Bernoulli function of log odds has derivative p(1-p) <= odds. Along the interval between the two log odds, both odds are bounded by e^{-b|eta|}; therefore the disagreement probability is at most e^{-b|eta|}d_{eta,gamma_0}.

The total weighted hard-core influence satisfies

\[
\sum_{\eta\not\sim\gamma_0}|\eta|e^{-b|\eta|}
\le(D+1)|\gamma_0|Q(b).
\]

For the soft influence, interchange nonnegative sums:

\[
\begin{aligned}
\sum_\eta |\eta|e^{-b|\eta|}d_{\eta,\gamma_0}
&\le4Q(b)\sum_{A:A\cap V(\gamma_0)\ne\varnothing}|A|\|\phi_A\|_\infty\\
&\le4\xi Q(b)|\gamma_0|.
\end{aligned}
\]

Thus expected distance after one step is at most

\[
|\gamma_0|\left[1-\frac1K+\frac\theta K\right].
\]

Path coupling extends this contraction to all configurations. Since compatible supports are disjoint, their total occupied size is at most N; the initial distance between the empty configuration and any stationary configuration is at most N. The minimum nonzero distance is one, so the coupling bound gives the claimed TV mixing time.

## Computable truncation of an infinite potential expansion

If the cluster expansion yields the stronger norm

\[
\sup_x\sum_{A\ni x}|A|e^{\kappa\ell(A)}\|\phi_A\|_\infty\le\xi,
\]

where ell(A) is the total cluster order, truncating to ell(A)<=M changes every insertion log odds by at most 2xi |gamma| e^{-kappa M}. On the L-truncated polymer state space this is at most 2xi L e^{-kappa M}. Over t heat-bath updates the resulting TV error is at most 2t xi L e^{-kappa M}. Thus M=O(log(tL/delta)) suffices. A standard cluster-expansion coefficient algorithm must still establish that those potentials and their values can be enumerated/computed in exp(O(M)) work; positivity alone does not establish that computational claim.

The statement is an explicit sampler theorem once that last cluster-evaluation property has been supplied. It avoids global rejection, whose acceptance probability could be exponentially small in N even when xi is a small constant.
