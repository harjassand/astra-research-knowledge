# Independent R1 finite-use review

Reviewer scope: the first-failure converse, its approximate-output extension, the shifted finite stock, and the graded weak-output counterexample. Date: 21 October 2026. Input was the full supplied `seeds/R1_MODEL_AND_PROOF.txt` and `sources/constructive_reservoir.txt`, not an original executable archive. This is an internal analytic reconstruction; no historical finite-check count is treated as evidence.

## Verdict and necessary normalization

The first-failure proof, its approximation variant, shifted stock, and graded counterexample survive reconstruction. The graded return inequality must be typeset as

\[
\|\tau_j-\tau\|_1\le \alpha j/\sqrt L,
\]

not `alpha j/L`. The text extraction obscures the square root, but its later condition `L>4J^2` is consistent with the correct expression.

Throughout this review, \(\varepsilon=\|\tau'-\tau\|_1\) is a full trace norm and \(\delta=\varepsilon/2\) is half trace distance. Natural logarithms are used. \(J\) below denotes the number of Bell outputs in a block; \(N\) is the number of repetitions of that block in the analytical converse. The graded example also uses \(J\) as its chosen number of positive return times, with tomography horizon \(n=1\); these are separate uses of the symbol, not a claimed identification of the two operational questions.

All statements retain finite external ports, normal bipartite tensor-product memory, fixed finite-round finite-outcome LOCC, complete averaging over outcomes, a faithful product reference, and all retained registers. The constructions ignore incoming ports; hence their complete output states determine their response even to adaptive/reference-entangled testers. No fresh entanglement enters after initialization.

## 1. First-failure lower bound: full proof

Let \(T\) be the \(J\)-call channel under the faithful product inputs. Let \(D=2^J\), \(B_D=|\Phi_D\rangle\langle\Phi_D|\), and assume that the joint output of the first block is exactly \(B_D\). A pure output marginal forces the joint output-memory state to factor:

\[
T(\tau)=B_D\otimes\tau',\qquad
\tfrac12\|\tau'-\tau\|_1\le\delta.
\]

This factorization is automatic even if the original task stated only the pure external marginal. Define the completely positive trace-nonincreasing map

\[
S(x)=\operatorname{Tr}_{O}[(B_D\otimes I)T(x)(B_D\otimes I)].
\]

Then \(S(\tau)=\tau'\). Define \(s_m=\operatorname{Tr}S^m(\tau)\), with \(s_0=1\). The operator \(E_m=(S^*)^{m-1}(I)\) is an effect, so the Jordan decomposition of the trace-zero operator \(\tau'-\tau\) gives

\[
s_m-s_{m-1}=\operatorname{Tr}E_m(\tau'-\tau)\ge-\delta.
\]

Since \(s_1=1\),

\[
s_m\ge[1-(m-1)\delta]_+.
\tag{F1}
\]

Run the actual channel \(T\), unmodified, for \(N\) blocks, retaining its external outputs. Afterwards perform the global Bell projector on each block and set \(K\) equal to the number of initial consecutive successes, capped at \(N\). Deferred measurement justifies \(\Pr(K\ge m)=s_m\): earlier output projectors commute with future channels on the memory. No physical LOCC implementation of the Bell test is asserted or needed; it is an analytical measurement used in relative-entropy data processing.

For a separable initializer \(\gamma\), the unconditioned full output remains separable across all Alice outputs versus all Bob outputs. Its first \(k\) blocks have Bell-product overlap at most \(D^{-k}\). To see this, a product pure state has overlap squared at most \(D^{-k}\) with the maximally entangled vector of local dimension \(D^k\), and convexity extends this to all separable states. Thus if \(r\) is the law of \(K\) from \(\gamma\),

\[
r_k\le\Pr_\gamma(K\ge k)\le D^{-k}.
\]

If \(p\) is the law from \(\tau\), data processing gives, including the usual extended-real conventions,

\[
D(\tau\|\gamma)\ge D(p\|r)
\ge(\ln D)\mathbb E_pK-H(p).
\]

Here \(p_0=0\), so \(H(p)\le\ln N\). Taking the infimum over normal separable \(\gamma\), then using (F1), proves

\[
E_R(\tau)\ge J\ln2\sum_{m=1}^{N}[1-(m-1)\delta]_+-\ln N.
\tag{F2}
\]

No closest separable state is required, no infinite quantity is subtracted, and no separability after Bell postselection is assumed. The argument allows arbitrary output correlations on subsequent repetitions.

For \(0<\delta\le1\), take \(N=\lceil1/\delta\rceil\). Writing \(\theta=N-1/\delta\in[0,1)\), the sum is exactly

\[
N-\delta N(N-1)/2
=1/(2\delta)+1/2+\delta\theta(1-\theta)/2.
\]

Consequently

\[
E_R(\tau)\ge J\ln2\left(\frac1{2\delta}+\frac12\right)
-\ln\lceil1/\delta\rceil
=\frac{J\ln2}{2\delta}-\ln(1/\delta)+O_J(1).
\tag{F3}
\]

In full norm \(\varepsilon=2\delta\), the leading term is \(J\ln2/\varepsilon\). This lower bound imposes only terminal block return; therefore it also bounds the stricter every-use-return task. At \(\delta=0\), it forces \(E_R(\tau)=\infty\); ruling out the remaining infinite-resource normal case uses the separate recurrence theorem, not (F2) alone.

## 2. Approximate output and approximating initializer

Let \(M=\operatorname{Tr}_OT(\tau)\), let \(\|M-\tau\|_1\le\varepsilon\), and let the *whole-block* Bell infidelity be

\[
q=1-\operatorname{Tr}[(B_D\otimes I)T(\tau)].
\]

The positive failure operator \(F=M-S(\tau)\) has trace \(q\). Positivity holds because partial trace removes the off-diagonal blocks of the projection \(B_D\otimes I\). For the same effects \(E_m\),

\[
\operatorname{Tr}E_m(S(\tau)-\tau)
=\operatorname{Tr}E_m(M-\tau)-\operatorname{Tr}E_mF
\ge-\varepsilon/2-q.
\]

Thus

\[
\operatorname{Tr}S^m(\tau)\ge[1-q-(m-1)(\varepsilon/2+q)]_+.
\]

If \(\|\sigma-\tau\|_1\le\xi\), the entire success-prefix probability is one effect on the initializer, and hence

\[
\operatorname{Tr}S^m(\sigma)
\ge[1-q-\xi/2-(m-1)(\varepsilon/2+q)]_+.
\]

Applying the preceding relative-entropy argument to \(\sigma\), now with \(K\in\{0,\ldots,N\}\), yields

\[
E_R(\sigma)\ge J\ln2\sum_{m=1}^{N}
[1-q-\xi/2-(m-1)(\varepsilon/2+q)]_+-\ln(N+1).
\tag{F4}
\]

This proves the supplied formula. The approximation error affects the intercept, not the slope. It does not accumulate once per repetition because the initial-state comparison is applied to one full-prefix effect. No decoupling or square-root gentle-measurement penalty is needed. If the complete output's full trace error from \(B_D\) is at most \(u\), then \(q\le u/2\). A per-output error should not silently be substituted for this whole-block quantity. With correlated outputs it requires a separate bound (a union bound is available for the commuting Bell projectors).

Equation (F4) is a rigorous lower bound, not a demonstrated jointly optimal noisy-output law.

## 3. Shifted stock: exact operation and exhaustion

Fix once the local separable Hilbert space \(\mathcal C=\bigoplus_{k\ge0}(\mathbb C^2)^{\otimes k}\). On positive length sectors, a local partial isometry releases the last qubit and maps the remainder to sector \(k-1\). On the vacuum sector a second Kraus operator prepares an output \(|0\rangle\) and leaves vacuum. These two local Kraus operators satisfy the completeness relation. Their tensor-product channel is fixed, normal, and finite-outcome; no communication is needed.

Let \(\omega_k\) be \(k\) Bell pairs in the matching orthogonal length sectors. For \(J\ge1\), \(L\ge1\), initialize

\[
\tau_{J,L}=L^{-1}\sum_{k=J}^{J+L-1}\omega_k.
\]

Writing \(Z=|00\rangle\langle00|\), the complete state after \(j\) calls is

\[
\Omega_j=L^{-1}\sum_{k=J}^{J+L-1}
B^{\otimes\min(k,j)}\otimes Z^{\otimes(j-k)_+}
\otimes\omega_{(k-j)_+}.
\tag{S1}
\]

For \(j\le J\), this factors as \(B^{\otimes j}\otimes\tau_j\); all useful outputs are exact and independent. Afterwards the exhaustion time generates correlations, which (S1) retains.

Since length sectors are locally orthogonal, the memory distance is the classical full \(\ell^1\) distance between the initial uniform interval and its downward shifted/clamped law. Their overlapping mass is \((1-j/L)_+\), giving, for all \(j\ge0\),

\[
\|\tau_j-\tau_{J,L}\|_1=2\min(j/L,1).
\tag{S2}
\]

The locally readable flags give

\[
E_R(\tau_j)=\frac{\ln2}{L}\sum_{k=J}^{J+L-1}(k-j)_+,
\qquad E_R(\tau_{J,L})=\left(J+\frac{L-1}{2}\right)\ln2.
\tag{S3}
\]

For completeness, the flag identity follows by applying local flag dephasing to a separable competitor: classical relative entropy of flag probabilities is nonnegative, and each conditioned comparison costs at least the corresponding conditional \(E_R\). Matching mixtures of conditional optimizers give the reverse inequality.

Choosing \(L=\lceil J/\delta\rceil=\lceil2J/\varepsilon\rceil\) attains every-use half return error \(\delta\) and cost \(J\ln2/(2\delta)+O(J)\). It matches the leading coefficient in (F3), but by itself does **not** prove the negative logarithmic correction is attainable. That requires the separate unflagged construction.

All used local sectors have total dimension \(\sum_{k=0}^{J+L-1}2^k=2^{J+L}-1\). Preparation consumes an expected \(J+(L-1)/2\) Bell pairs and at most \(J+L-1\). During the useful horizon exactly one Bell pair is consumed per call. Neither small trace disturbance nor a large state count makes this indefinite reuse. The average number of non-exhausted outputs is not the entanglement of an unflagged output mixture; \(B\) and \(Z\) are nonorthogonal.

## 4. Graded weak-output construction: direct proofs

Define

\[
|p_x\rangle=\cos(x/2)|00\rangle+\sin(x/2)|11\rangle,
\quad
q_x=\tfrac12\bigl(|00\rangle\langle00|+|11\rangle\langle11|
+\sin x(|00\rangle\langle11|+|11\rangle\langle00|)\bigr).
\]

Here \(p_x\) also denotes its rank-one density operator. Both cell families have full trace distance \(\sin x\) to SEP. Dephasing in the displayed product basis supplies an upper bound: the difference has eigenvalues \(\pm\sin x/2\). For the lower bound use the witness

\[
W=|01\rangle\langle01|+|10\rangle\langle10|
-|00\rangle\langle11|-|11\rangle\langle00|.
\]

It has operator norm one and equals twice the partial transpose of the projector onto \((|01\rangle-|10\rangle)/\sqrt2\), so its expectation is nonnegative in every separable state. Its expectation in either cell is \(-\sin x\). Trace-norm duality proves the lower bound.

### Relative entropy is exactly calculable

For a finite-dimensional maximally correlated state \(\rho=\sum_{a,b}c_{ab}|aa\rangle\langle bb|\),

\[
E_R(\rho)=S(\rho_A)-S(\rho).
\tag{G1}
\]

A direct proof avoids assuming general additivity of \(E_R\). Any separable \(\sigma\) satisfies the reduction inequality \(\sigma\le\sigma_A\otimes I\), since every local density matrix on B is bounded by \(I\). Operator monotonicity of log (with standard regularization at zero eigenvalues) gives

\[
D(\rho\|\sigma)\ge-S(\rho)-\operatorname{Tr}\rho_A\ln\sigma_A
\ge S(\rho_A)-S(\rho).
\]

The separable state \(\sum_a c_{aa}|aa\rangle\langle aa|\) attains equality. Tensor products of maximally correlated states are again maximally correlated, so (G1) directly proves additivity for this restricted family. Therefore

\[
E_R(p_x)=h(\sin^2(x/2)),\qquad
E_R(q_x)=\ln2-h((1+\sin x)/2).
\tag{G2}
\]

This machinery is inherited, not an Astra novelty; see references below.

### The fixed device and complete state

Fix positive integers \(J,L\), set \(M=J+L-1\), and use weights \(f_i=1\) for \(1\le i\le J\), \(f_{J+r}=1-r/L\) for \(1\le r<L\), and zero thereafter. Initialize

\[
\tau_r(\alpha)=\bigotimes_{i=1}^M r_{\alpha f_i},\qquad r=p\text{ or }q.
\]

The device releases the first cell, shifts the rest, and appends the separable cell \(r_0\). Pure padding is locally prepared. Mixed padding uses a shared fair classical bit generated by a finite two-outcome LOCC step; it brings no entanglement. The channel, ports, and finite memory dimension stay fixed while \(\alpha\) varies.

For every \(j\), including exhaustion,

\[
\Omega_r(j)=\left(\bigotimes_{i=1}^j r_{\alpha f_i}\right)
\otimes\left(\bigotimes_{i=1}^M r_{\alpha f_{i+j}}\right).
\tag{G3}
\]

The first \(J\) outputs are exactly independent copies of \(r_\alpha\), with no memory correlations. The memory subsequently becomes entirely separable after the finite stock is depleted.

### Return bound

For the pure family,

\[
\|\tau_{p,j}-\tau_p\|_1
=2\sqrt{1-\prod_{i=1}^M\cos^2(\alpha(f_i-f_{i+j})/2)}
\le\alpha\|f-T^j f\|_2,
\]

where \(T\) is the forward shift of the zero-extended sequence. The last inequality follows from \(1-\prod(1-u_i)\le\sum u_i\) and \(|\sin z|\le|z|\). The first difference \(f-Tf\) has precisely \(L\) entries of magnitude \(1/L\), so \(\|f-Tf\|_2=1/\sqrt L\). Since the forward shift contracts \(\ell^2\), the telescoping identity gives

\[
\|f-T^j f\|_2\le j/\sqrt L.
\]

The bilateral twirl \(\mathcal T(\rho)=[\rho+(X\otimes X)\rho(X\otimes X)]/2\) maps every \(p_x\) to \(q_x\), including padding. Contractivity of \(\mathcal T^{\otimes M}\) yields

\[
\|\tau_{q,j}-\tau_q\|_1\le\|\tau_{p,j}-\tau_p\|_1\le\alpha j/\sqrt L.
\tag{G4}
\]

The mixed family also commutes in the product Bell basis, so its exact full norm is a finite product-Bernoulli \(\ell^1\) distance. No classical approximation is being substituted for noncommuting matrices.

### Resource scaling and countertheorem

By (G2),

\[
R_q=\sum_i[\ln2-h((1+\sin(\alpha f_i))/2)]=\Theta(\alpha^2),
\]

\[
R_p=\sum_i h(\sin^2(\alpha f_i/2))
=\Theta(\alpha^2\ln(1/\alpha)),
\]

with fixed \(J,L\) as \(\alpha\downarrow0\). Preparing the mixed stock by bilateral twirling the pure stock consumes the latter resource and loses \(R_p-R_q\). The pure construction alone suffices for the exponent counterexample even under this more conservative entropic preparation accounting. These quantities must not be identified with exact one-shot Bell-pair formation cost.

For the one-slot replacement-output process, full strategy distance to causal LOCC closure is exactly \(d=\sin\alpha\). A free input witnesses the lower bound through distance to SEP; the nearest separable replacement channel attains the upper bound, including arbitrary reference inputs.

Fix \(L>4J^2\) once, and set \(\varepsilon=\alpha J/\sqrt L\). Every positive return time \(1,\ldots,J\) meets that full error. Take the finite-resource approximant equal to the initializer. Then

\[
d-2\varepsilon=\alpha(1-2J/\sqrt L)+O(\alpha^3)=\Theta(\alpha)>0,
\]

while for every \(\beta>1/2\), both \((R_q/J)^\beta=o(\alpha)\) and \((R_p/J)^\beta=o(\alpha)\). Thus no bound

\[
d\le2\varepsilon+C(R/J)^\beta,\qquad\beta>1/2,
\]

can hold with finite coefficient \(C\) uniform over initializers of this one fixed finite device. The coefficient may depend on that fixed device, \(J\), and the one-slot horizon; taking \(\alpha\to0\) still contradicts it.

This establishes the sharp resource exponent only. It does not establish optimal joint horizon dependence or optimal tomography constants. Keeping the displayed return-to-output ratio fixed while varying \(J\) requires \(L\) of order \(J^2\).

## 5. Literature boundary and embezzling comparison

1. **Maximally correlated entanglement.** Chen–Yang, *The relative entropy of entanglement of Schmidt correlated states and distillation*, Quantum Information Processing 1, 389–395 (2002), https://arxiv.org/pdf/quant-ph/0204152, Corollaries 1 and 2, explicitly states the optimal dephased separable comparator and additivity. It attributes the formula to earlier Rains and Wu et al. work. Rains, *A semidefinite program for distillable entanglement*, IEEE Trans. Inf. Theory 47 (2001), https://arxiv.org/pdf/quant-ph/0008047, treats maximally correlated states. The direct proof (G1) makes the present argument independent of any additional machinery in those papers.

2. **Approximate embezzlement.** Van Dam–Hayden, *Universal entanglement transformations without communication*, Phys. Rev. A 67, 060302(R) (2003), https://arxiv.org/pdf/quant-ph/0201041, Eq. (4), gives an amplitude-overlap bound \(F\ge1-\ln m/\ln n\). For pure global states the half trace distance is \(\sqrt{1-F^2}\), hence is bounded by \(\sqrt{2\ln m/\ln n}\). This is an approximate whole-state production result, not an exact Bell-output result under the identical error contract. Local marginal trace distances do not imply complete bipartite-memory trace distance. The theorem (F2) covers any admissible embezzling alternative that actually meets the exact-output specification.

3. **Earlier resource divergence.** Rubboli–Tomamichel, *Fundamental Limits on Correlated Catalytic State Transformations*, Phys. Rev. Lett. 129, 120506 (2022), https://arxiv.org/pdf/2111.13356, Proposition 4 and its resource-monotone extension, gives dimension-independent sandwiched-Rényi continuity using half trace distance. Its main Theorem 2 explicitly states logarithmic resource divergence in its general setting. Obtaining inverse-error divergence in the exact Bell task requires optimizing its parameter toward one; it should not be attributed to the literal statement of Theorem 2.

For the last comparison, write \(a=J\ln2\), \(s=1-\alpha\in(0,1/2]\), use pure-Bell additivity and monotonicity, and apply that continuity bound between \(\tau\) and \(\tau'\). It yields

\[
E_R(\tau)\ge\frac1s\ln\frac{1-e^{-sa}}{\delta^{1-s}}.
\tag{L1}
\]

If the small-distance hypothesis of the continuity bound fails, the stronger estimate \(E_\alpha(\tau)\ge(\alpha/s)\ln(1/\delta)\) already implies (L1). Otherwise the continuity estimate itself implies it. Choosing \(s=e\delta/a\) for sufficiently small \(\delta\) gives

\[
E_R(\tau)\ge a/(e\delta)-\ln(1/\delta)+O_J(1).
\]

In full norm, its leading coefficient is \(2/e\) times the \(a/\varepsilon\) coefficient in (F3). This independently supports the supplied comparison as an *application of prior machinery*, not a claim that this is the best pre-existing bound in all literature. A careful infinite-dimensional application needs the corresponding extensions or truncation justification; the first-failure proof above applies directly to normal memories and avoids that issue.

No priority certification follows from this limited literature check. The potential distinctive mathematical objects are the direct first-failure converse, its block-infidelity/finite-approximant extension, and this fixed-device graded counterexample, subject to a fuller novelty review. Inverse-error divergence, ordinary entanglement stocks, the maximally correlated identities, and approximate embezzlement themselves are inherited.

## 6. Consequences for consolidation

The exact Bell and weak-output statements answer different questions and should be integrated once, without counting them as competing discoveries. The Bell theorem excludes hidden catalytic savings beyond its quantified budget under the stated exact target. The graded example explains why its stronger task-specific converse cannot be promoted to a universally larger resource exponent.

Terminal return is sufficient for the converse, while the exhibited upper constructions provide every-use return; this is a real operational distinction. Changing \(\varepsilon\) to \(\delta=\varepsilon/2\) is merely notation. Product outputs and correlated outputs must remain distinguished. All finite stocks become depleted, so these examples do not challenge trace-norm recurrence.

No further additive-constant optimization, tomography refinement, or separate reservoir campaign is justified by these results alone. A sharp noisy-output law is unresolved, but should receive new investment only if an explicitly selected operation makes that precision consequential. The supplied historical runnable package was not retrieved or replayed by this reviewer; the conclusions above rest on the displayed arguments, not its reported tests.
