# Independent review and reconstruction of the Bell-reservoir logarithmic law

Reviewer: `logarithmic_law_review`, 21 October 2026.

## Decision and provenance

The claimed two-term asymptotic law can be independently proved in the stated normal bipartite tensor-product model:

\[
R_{\min}(J,\delta)
=\frac{J\ln2}{2\delta}-\ln(1/\delta)+O_J(1),
\qquad \delta\downarrow0,\quad J\ge1\text{ fixed}.
\]

Here the resource is **intrinsic initial relative entropy of entanglement**, and `delta` is **half of the trace norm of the entire retained bipartite memory difference**. It is not a bound on the entanglement consumed by every possible state-preparation procedure. The distinction matters for the logarithmic term.

This review independently reconstructs an explicit unflagged mixed reservoir and a matching converse. It does **not** replay or authenticate Ultra's unavailable original archive, and makes no inference from the reported 23,630 finite checks. The lower bound uses the substantive first-failure argument supplied in `sources/constructive_reservoir.txt`; the upper bound below was reconstructed independently from the labelled summary and the model. Its correspondence to Ultra's exact original construction is unknown until that source is obtained.

The all-use and terminal-return optimizations have the same displayed two-term asymptotic, because the converse needs only terminal return and the construction meets every earlier return tolerance. The law is not an assertion about every arbitrarily prescribed device. The upper bound is attained asymptotically by **one specified fixed normal device** on a fixed countable direct-sum memory; the lower bound is universal over admitted devices.

## 1. Exact operation and quantifiers

Let `B` denote the two-qubit maximally entangled state \(|\Phi_+\rangle\langle\Phi_+|\), with \(|\Phi_+\rangle=(|00\rangle+|11\rangle)/\sqrt2\). A device receives faithful product reference inputs and releases one two-qubit output per call. The required first `J` outputs have joint state \(B^{\otimes J}\). Since this state is pure, it factors from every other register at that horizon. Alternatively, if all `J` individual marginal outputs are exactly `B`, their joint state is necessarily this product, so exactness leaves no output-correlation loophole.

For an initializer `tau`, write `tau_j` for the complete retained memory after `j` calls. Define terminal return by

\[
\tfrac12\|\tau_J-\tau\|_1\le\delta,
\]

and all-use return by the same inequality for every \(1\le j\le J\). The full-norm convention in the supplied constructive report is \(\epsilon=2\delta\). All logarithms below are natural.

Let \(R_{\rm term}(J,\delta)\) and \(R_{\rm all}(J,\delta)\) be the infima of initial \(E_R\) over admitted realizations of these two tasks. Clearly \(R_{\rm term}\le R_{\rm all}\). Every retained register is included; all branches of the LOCC device are averaged; no later entangled resource is supplied. Local spaces are separable, and states and channels are normal.

The upper-bound device ignores external inputs, so its state formulas determine the complete causal external process, including adaptive or reference-entangled tests. The converse only requires the product reference input and therefore applies to the larger class of devices that may also respond nontrivially to other inputs.

## 2. Universal first-failure converse

Put \(D=2^J\), \(a=\ln D=J\ln2\), and let \(T\) denote the `J`-call channel from memory to the entire output block and memory, with product reference inputs supplied. Exact output implies

\[
T(\tau)=B_D\otimes\tau',\qquad
\tfrac12\|\tau'-\tau\|_1\le\delta.
\]

Here \(B_D=B^{\otimes J}\). Define the completely positive trace-nonincreasing success map

\[
S(x)=\operatorname{Tr}_O[(B_D\otimes I)T(x)(B_D\otimes I)].
\]

Then \(S(\tau)=\tau'\). Put \(s_m=\operatorname{Tr}S^m(\tau)\). The normal adjoint of a completely positive trace-nonincreasing map sends effects to effects, so

\[
E_{m-1}=(S^*)^{m-1}(I),\qquad0\le E_{m-1}\le I.
\]

Because \(\tau'-\tau\) has trace zero,

\[
s_m-s_{m-1}=\operatorname{Tr}E_{m-1}(\tau'-\tau)\ge-\delta.
\]

Using \(s_1=1\) gives

\[
s_m\ge[1-(m-1)\delta]_+.
\tag{2.1}
\]

Repeat the actual block `N` times, retaining all outputs. Only after these operations, measure each output block using the Bell projector and its complement. Let `K` be the number of consecutive initial successes, capped at `N`. Measuring earlier blocks cannot affect the later channel, which acts only on retained memory, so the probability of passing the first `m` tests equals `s_m`. Thus

\[
\mathbb E_\tau K=\sum_{m=1}^N s_m.
\]

For every separable initializer `gamma`, the **unconditioned** complete output is separable across all Alice outputs versus all Bob outputs. A separable state has overlap at most \(D^{-k}\) with `k` maximally entangled blocks. Consequently, if `r` denotes the distribution of `K` for `gamma`,

\[
r_k\le\Pr_\gamma(K\ge k)\le D^{-k}.
\]

If `p` is the corresponding distribution for `tau`, relative-entropy data processing gives

\[
\begin{aligned}
D(\tau\|\gamma)&\ge D(p\|r)\\
&\ge a\,\mathbb E_\tau K-H(p)\\
&\ge a\sum_{m=1}^N[1-(m-1)\delta]_+-\ln N.
\end{aligned}
\]

The last entropy bound uses exact first-block success, so `p` is supported on \(\{1,\ldots,N\}\), although `r` may also have mass at zero. Taking the infimum over all normal separable `gamma` proves

\[
E_R(\tau)\ge a\sum_{m=1}^N[1-(m-1)\delta]_+-\ln N.
\tag{2.2}
\]

This proof does not assert that Bell-postselected memory stays separable. That statement would be false. Only the unconditioned outputs are used to bound the alternative hypothesis probabilities. No finite-dimensional memory assumption is used; normal quantum relative-entropy data processing covers infinite memory, and an infinite left side is harmless.

Choose \(N=\lceil1/\delta\rceil\) for \(0<\delta\le1\). Writing \(r=N-1/\delta\in[0,1)\),

\[
N-\frac{\delta N(N-1)}2
=\frac1{2\delta}+\frac12+\frac\delta2r(1-r).
\]

Therefore

\[
E_R(\tau)\ge
\frac{a}{2\delta}-\ln(1/\delta)
+\frac a2-\ln(\delta\lceil1/\delta\rceil)
+\frac{a\delta}2r(1-r).
\tag{2.3}
\]

In particular,

\[
R_{\rm term}(J,\delta)\ge
\frac{J\ln2}{2\delta}-\ln(1/\delta)
+\frac{J\ln2}{2}-\ln2.
\tag{2.4}
\]

This establishes the necessary logarithmic correction as a lower-bound term. A matching construction is still needed before the coefficient of this term is an asymptotic theorem.

## 3. Unflagged mixed construction

Define the separable, classically correlated padding cell

\[
C=\tfrac12(|00\rangle\langle00|+|11\rangle\langle11|)
=\tfrac12(B_++B_-),
\]

where \(B_-=|\Phi_-\rangle\langle\Phi_-|\) and \(|\Phi_-\rangle=(|00\rangle-|11\rangle)/\sqrt2\).

For positive integers `J,L`, set \(M=J+L-1\), and define on `M` cells

\[
\omega_k^{(M)}=B^{\otimes k}\otimes C^{\otimes(M-k)},
\quad0\le k\le M,
\qquad
\tau_{J,L}=\frac1L\sum_{k=J}^{M}\omega_k^{(M)}.
\tag{3.1}
\]

There is **no retained shared label identifying `k`**. The different `k` terms are mixed in the same physical memory; introducing a retained orthogonal `k` flag would change its resource value and remove the logarithmic saving.

Each call releases the first cell, shifts the remaining cells one place, and appends a new separable `C` cell. This requires a fair classical bit shared through a two-outcome LOCC step. Every branch contributes to the averaged channel. The bit record need not be retained separately; the appended cell is counted as memory. No entanglement is injected.

For every \(0\le j\le J\),

\[
\Omega_j=B^{\otimes j}\otimes\tau_j,\qquad
\tau_j=\frac1L\sum_{k=J}^{M}\omega_{k-j}^{(M)}.
\tag{3.2}
\]

The first `J` outputs are exact and independent. Since the two sums for `tau_j` and `tau` share `L-j` terms when `j<L`, cancellation and the triangle inequality give

\[
\frac12\|\tau_j-\tau\|_1\le\min\{j/L,1\}.
\tag{3.3}
\]

Thus \(L=\lceil J/\delta\rceil\) meets every-use return.

For arbitrary `j`, including depletion, the complete state is

\[
\Omega_j=\frac1L\sum_{k=J}^{M}
\left(B^{\otimes\min(k,j)}\otimes C^{\otimes(j-k)_+}\right)_O
\otimes\omega_{(k-j)_+}^{(M)}.
\tag{3.4}
\]

Exhausted outputs are `C`, and all branches are present. Output correlations appear after depletion because different `k` values cause different exhaustion times. They are not discarded or replaced by a statement about one-output marginals.

### One fixed device and one fixed normal memory for the full family

The family does not require a changing device. Fix

\[
\mathcal C_A=\mathcal C_B=
\bigoplus_{M\ge1}(\mathbb C^2)^{\otimes M}.
\]

The local `M` sector label is part of memory. For a fixed appended bit \(c\in\{0,1\}\), define on each sector

\[
V_c|M;x_1\cdots x_M\rangle
=|x_1\rangle_O\otimes|M;x_2\cdots x_Mc\rangle_C.
\]

The direct sum of these sector maps is an isometry: orthogonality within each sector and between sectors is preserved. It is bounded and defines a normal local channel. Alice samples `c` uniformly, sends it to Bob, and both use `V_c`; discarding the two-valued message record after use gives the average channel

\[
\Lambda_*(\xi)=\tfrac12\sum_{c=0}^1
(V_c^A\otimes V_c^B)\xi(V_c^A\otimes V_c^B)^*.
\]

External inputs are traced out first. This has finite external ports, one communication round, two classical outcomes and fixed normal tensor-product memory. It requires no measurement with infinitely many outcomes. Both initial sector labels equal the deterministic chosen `M`; they are counted but add no entanglement. Every initializer has finite support. The same `Lambda_*` works for all `J,L`.

For a globally fixed finite-dimensional memory the limit \(\delta\downarrow0\) would eventually be impossible, as the converse exceeds its maximum `E_R`. The countable direct sum supplies increasing **finite occupied supports** without changing the algebra or device.

## 4. Exact resource and bounded conditional entropy

All states \(\omega_k^{(M)}\) commute in the product Bell-sign basis. Let `K` be uniform on \(\{J,\ldots,M\}\). Conditional on `K=k`, the first `k` Bell signs are plus and the remaining `M-k` signs are independent fair signs. Call the resulting phase string `Y`.

The state `tau` is maximally correlated in the computational basis, and its local marginal is \(I/2^M\). Its computational diagonal is the separable state

\[
\Delta\tau=2^{-M}\sum_x|xx\rangle\langle xx|.
\]

It follows directly that

\[
E_R(\tau)=M\ln2-S(\tau).
\tag{4.1}
\]

For completeness, the displayed diagonal gives the upper bound. For any separable finite-dimensional `sigma`, the reduction inequality \(\sigma\le\sigma_A\otimes I_B\), operator monotonicity of logarithm and nonnegativity of relative entropy give

\[
\begin{aligned}
D(\tau\|\sigma)
&\ge-S(\tau)-\operatorname{Tr}\tau_A\log\sigma_A\\
&=S(\tau_A)-S(\tau)+D(\tau_A\|\sigma_A)\\
&\ge M\ln2-S(\tau).
\end{aligned}
\]

Non-full-rank comparators follow by regularization. The equality is unchanged by local isometric embedding into the fixed direct-sum memory: local projection/recovery to the occupied sectors and data processing show that additional unoccupied sectors cannot lower the infimum.

Classical entropy bookkeeping now gives

\[
\begin{aligned}
S(\tau)&=H(Y)\\
&=H(K)+H(Y\mid K)-H(K\mid Y)\\
&=\ln L+(M-\mathbb EK)\ln2-h_L,
\end{aligned}
\]

where \(h_L=H(K\mid Y)\). Hence

\[
E_R(\tau_{J,L})
=\left(J+\frac{L-1}{2}\right)\ln2-\ln L+h_L.
\tag{4.2}
\]

The crucial point is that `h_L` stays uniformly bounded. Let `T` be the number of initial plus signs in `Y`, with `T=M` if all signs are plus. The likelihood of any string with `T=t`, conditioned on `K=k`, is proportional to \(2^k\) for \(J\le k\le t\), and vanishes otherwise. Thus `T` is sufficient for `K`, and

\[
\Pr(K=k\mid T=t)=\frac{2^k}{\sum_{\ell=J}^t2^\ell}.
\]

Equivalently \(Z=t-K\) is a truncated geometric distribution with mass proportional to \(2^{-z}\), \(0\le z\le t-J\). Its mean is at most one and its normalization is at most two. Consequently

\[
H(K\mid T=t)
=\ln\left(\sum_{z=0}^{t-J}2^{-z}\right)
+\ln2\,\mathbb E[Z\mid T=t]
\le2\ln2.
\]

Therefore

\[
0\le h_L\le2\ln2.
\tag{4.3}
\]

This is the entire logarithmic saving: the unflagged mixing adds nearly `ln L` to the joint entropy while leaving the local marginal fixed.

With \(L=\lceil J/\delta\rceil\), equations (4.2)–(4.3) give the explicit bound

\[
R_{\rm all}(J,\delta)\le
\frac{J\ln2}{2\delta}-\ln(1/\delta)
+J\ln2+2\ln2-\ln J.
\tag{4.4}
\]

Combining (2.4) and (4.4) sandwiches both optimizations:

\[
\boxed{\quad
R_{\rm term}(J,\delta)
=R_{\rm all}(J,\delta)+O_J(1)
=\frac{J\ln2}{2\delta}-\ln(1/\delta)+O_J(1).
\quad}
\]

The first equality expresses only a bounded asymptotic difference, not equality of the two optimizations at finite error.

## 5. Preparation, consumed resource and scientific scope

One explicit preparation recipe samples `K`, supplies `K` Bell pairs and `M-K` separable `C` cells, and discards the `K` record before initialization. Its expected consumed Bell resource is

\[
\mathbb EK\ln2=\left(J+\frac{L-1}{2}\right)\ln2,
\]

and its maximum consumption is `M` Bell pairs. The intrinsic loss due to discarding the flag is \(\ln L-h_L\). The proof does not claim that exact one-shot formation cost equals `E_R`, or that this recipe has a logarithmic operational preparation saving. If the sampled `K` remains in a usable shared register, it belongs to memory and the flagged cost is the average `K ln2`; it cannot be excluded merely to claim a saving.

During the useful horizon,

\[
E_R(\tau_j)=E_R(\tau)-j\ln2,\qquad 0\le j\le J.
\]

Indeed, shifting removes an exact pure Bell cell and appending independent separable `C` adds one bit of joint entropy while leaving local memory dimension unchanged. Every useful call consumes exactly one ebit of intrinsic resource. Small complete-memory disturbance is compatible with this because occupied dimension grows as error shrinks. Nothing is recurrent; after `M` calls the memory is `C` on every cell.

The result is therefore a mathematically substantive two-term resource law for exact Bell production. It strengthens the leading inverse-error statement by identifying the logarithmic term and separates unflagged mixing from ordinary flagged stock. It is not a renewable reservoir, an implementation advantage in formation cost, a noisy-output optimum, or a demonstrated scientific technology.

## 6. Attribution boundaries and remaining questions

The converse is inherited from the supplied constructive report, with full/half trace conversion made explicit here. The maximally correlated relative-entropy identity, entropy chain rule, classical-information loss and broad entanglement batteries are established machinery. The new independent work in this review is the self-contained reconstruction and audit needed to establish that these ingredients actually prove the stated logarithmic law in the complete fixed-device model.

Relevant primary literature to compare before a priority claim includes:

- R. Rubboli and M. Tomamichel, *Fundamental Limits on Correlated Catalytic State Transformations*, Phys. Rev. Lett. 129, 120506 (2022), https://arxiv.org/pdf/2111.13356 and https://doi.org/10.1103/PhysRevLett.129.120506. Main-text Proposition 4 and supplementary Corollary 4 give dimension-free continuity for sandwiched Renyi divergences and their resource monotones in half trace distance. Their finite-dimensional scope and different catalytic task must be respected.
- Á. M. Alhambra, L. Masanes, J. Oppenheim and C. Perry, *Entanglement fluctuation theorems*, Phys. Rev. A 100, 012317 (2019), https://arxiv.org/abs/1709.06139. Entanglement batteries and broad distributions or superpositions over entanglement content predate this work.
- L. Henderson and V. Vedral, *Information, Relative Entropy of Entanglement and Irreversibility*, https://arxiv.org/abs/quant-ph/9909011. Classical ensemble information and its removal already play a recognized role in relative-entropy entanglement accounting.

These are comparison targets, not a completed priority certificate. This reviewer opened the primary papers, examined the stated scopes, the first paper's Proposition 4 and supplementary Corollary 4, the battery paper's Appendix J and the classical-information discussion. This is not a check of every proof in those papers.

For a scoped comparison, write `t=1-alpha` and `a=J ln2`. Bell additivity and the cited continuity bound imply in finite dimension

\[
E_R(\tau)\ge
\frac{1-t}{t}\ln(1/\delta)
+\frac1t\ln(1-e^{-ta}).
\]

Choosing \(t=e\delta/a\) for small `delta` yields a leading lower bound \(a/(e\delta)\), which is `2/e` times the leading coefficient proved here. This is an application derived from their machinery, not a claim that their theorem states this specialization, that it is the strongest prior lower bound, or that their finite-dimensional theorem has already been extended to the complete infinite-dimensional model. The proof in Sections 2–4 stands independently of this comparison.

The important unresolved operation is not the bounded additive constant. A genuinely different question would concern noisy outputs under a complete multi-output process criterion, joint dependence on output strength/error/return error/horizon, or an operational preparation cost distinct from `E_R`. This review supplies no reason to launch an additional reservoir campaign automatically. Preserve this law and its proof, and require a clearly specified operation and an expected consequential result before assigning more foundational resources.

