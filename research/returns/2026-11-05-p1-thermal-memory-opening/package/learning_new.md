# Independent non-quantum opening: operational replica symmetry in the SK model

Date: 2026-11-05. This question was selected without inspecting the external rival's new proposal. It is a candidate and constructive opening, not a completed theorem.

## Full question and consequence

Does the Sherrington–Kirkpatrick Gibbs distribution admit polynomial-time randomized sampling with full total-variation accuracy throughout the strict de Almeida–Thouless (AT) region, without assuming a Glauber mixing gap?

Use the convention

\[
\mu_{\beta,h,W}(\sigma)\propto
\exp\{\tfrac\beta2\sigma^T W\sigma+h\sum_i\sigma_i\},
\quad W\sim\mathrm{GOE}(N),\quad\sigma\in\{-1,1\}^N.
\]

The replica-symmetric fixed point and stability parameter are

\[
q=\mathbb E\tanh^2(h+\beta\sqrt q Z),\qquad
r_{\rm AT}=\beta^2\mathbb E\operatorname{sech}^4(h+\beta\sqrt q Z).
\]

Target compact subsets of the region \(r_{\rm AT}<1\), with explicit strict margin. The input is a supplied dense random coupling matrix, with paid input and precision costs. The output must be within \(\epsilon\) TV with high probability over disorder and the algorithm. This does not cover worst-case matrices, unknown physical couplings, or a uniform polynomial in arbitrarily large inverse temperature.

A full solution would make the thermodynamic replica-symmetric phase computationally operational, including low temperatures stabilized by a field. TV controls every bounded observable, unlike normalized Wasserstein approximation. Sampling would support repeated-sample estimation and annealing-based partition-function estimation with their additional costs. This is a substantial named open frontier, not a newly discovered question.

## Strongest primary comparisons

Du, Huang, Mohanty and Rajaraman, *Sampling from the SK Model up to Criticality*, arXiv:2610.17717v1 (October 2026), already solve zero-field sampling throughout \(\beta<1\) to inverse-polynomial TV accuracy, through weak Poincaré and high-probability covariance-operator control. Their Problem 1.6 explicitly asks for the AT extension. Zero-field “up to criticality” is therefore not an available new consequence.

Kumar, Sarkar, Tian and Zhu, *High-Magnetization Sampling at Low Temperatures*, arXiv:2609.08873v1, provide polynomial algorithms in sufficiently magnetized SK regimes, including strong-field regimes near the AT scale up to constants. They do not settle the whole strict AT region.

Kusuoka and Nakajima, *A quantitative replica-symmetric bound of the SK model in the entire AT region*, arXiv:2608.23413, claim full-region quantitative overlap concentration. Only the abstract was available in this audit, so its proof is not independently checked. Even granting it does not settle the covariance geometry needed by a sampler.

- https://arxiv.org/html/2610.17717v1
- https://arxiv.org/html/2609.08873v1
- https://arxiv.org/abs/2608.23413

## Exact counterexample 1: overlap does not control covariance norm

Let \(Z\) be a uniform sign. Conditionally on \(Z\), let the spins be independent with

\[
\mathbb E[\sigma_i\mid Z]=Za_Nv_i,
\quad v_i\in\{-1,1\},\quad a_N=N^{-1/4}.
\]

Then their unconditional mean is zero and

\[
C=(1-a_N^2)I+a_N^2vv^T,
\qquad\|C\|_{\rm op}=1-a_N^2+Na_N^2=\Theta(\sqrt N).
\]

For independent replicas and \(R=N^{-1}\sum_i\sigma_i^{(1)}\sigma_i^{(2)}\),

\[
\mathbb E R^2=\frac1N+\frac{N-1}{N}a_N^4
=\frac2N-\frac1{N^2}.
\]

Thus optimal-scale scalar overlap concentration alone cannot give a constant covariance-operator bound. This is not an SK counterexample. It proves that the desired algorithmic implication needs extra quenched geometry.

## Exact counterexample 2: observation can increase squared susceptibility

For a hidden sign under continuous Gaussian observation \(dY_t=Xdt+dW_t\), write \(m_t=\mathbb E[X\mid Y_{[0,t]}]\), \(v_t=1-m_t^2\). The innovation equation is \(dm_t=v_t\,dB_t\). Itô's formula gives

\[
\frac d{dt}\mathbb E v_t=-\mathbb E v_t^2,
\qquad
\frac d{dt}\mathbb E v_t^2
=2\mathbb E[v_t^2(3m_t^2-1)].
\]

When \(m_0^2>1/3\), squared susceptibility initially increases although mean-square uncertainty decreases. This does not prove an actual SK AT-boundary crossing; it defeats the naive monotonicity argument.

## Constructive opening: exact erasure-pinning decomposition

For an arbitrary binary-vector distribution, let \(m=\mathbb E\sigma\), \(C=\operatorname{Cov}(\sigma)\), \(D_i=1-m_i^2>0\), \(c_i=Ce_i\), and

\[
(T_i)_{jk}=\mathbb E[(\sigma_i-m_i)(\sigma_j-m_j)(\sigma_k-m_k)].
\]

Conditioning on \(\sigma_i=s\), set \(a_s=(s-m_i)/D_i\). Binary interpolation yields

\[
m^{(s)}=m+a_sc_i,
\qquad
C^{(s)}=C-\frac{c_ic_i^T}{D_i}+a_sK_i,
\quad K_i=T_i+\frac{2m_i}{D_i}c_ic_i^T.
\]

Since \(\mathbb E a_s=0\) and \(\mathbb E a_s^2=1/D_i\),

\[
\mathbb E\operatorname{tr}[(C^{(s)})^2]
=\operatorname{tr}C^2-\frac{2c_i^TCc_i}{D_i}
+\frac{\|c_i\|^4}{D_i^2}+\frac{\|K_i\|_F^2}{D_i}.
\]

For independent coordinates, \(K_i=0\) exactly, including at strong fields. The first pin from a spin-flip symmetric zero-field distribution also has \(K_i=0\). Exact revelation therefore removes the intrinsic single-bit observation noise seen above and isolates an interaction-dependent matrix noise term.

The serious opening is to use erasure or hybrid localization and prove that AT stability controls the accumulated \(K_i\) process. An integrated covariance-operator estimate might suffice for weak-Poincaré/annealing methods even when a uniform conditional bound is too strong.

### Missing central theorem

For typical SK disorder in a compact strict AT region, bound the interaction-noise process along a usable revelation/localization schedule strongly enough to control integrated covariance and produce polynomial sampling. The conditional fields generated by revelation must be controlled, not merely the initial equilibrium overlap. The displayed identity is exact algebra, not a proof of this theorem; coordinate pinning itself is established machinery.

## Selection assessment

This is a consequential, sharply testable alternative. It avoids the already-solved zero-field frontier and exposes a concrete central obstruction. Its opening is less developed than the conditional decoder-history polymer sampler: no current bound closes its SK interaction-noise term. Preserve it without treating the exact algebra as evidence that the full AT theorem is close.
