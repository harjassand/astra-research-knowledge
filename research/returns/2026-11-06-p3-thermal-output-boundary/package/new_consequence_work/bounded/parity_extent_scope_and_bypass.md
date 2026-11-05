# Fermionic preparation: valid causal obstruction and adaptive bypass

Status: a valid auxiliary theorem at the local-causal scope; **not selected as the main new apparatus theorem**. Unrestricted measurement-dependent global classical feedforward defeats a bound on quantum gate layers alone. This note records that failure rather than silently changing the access model.

## Explicit bypass

Put two fermionic modes at each internal site of a path and one mode at each endpoint. On every edge prepare the even Bell state

\[
 |\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2.
\]

The edge states are independent bounded-range even seeds. At every internal site simultaneously measure its two modes in the Bell basis. All four Bell projectors commute with that site's fermion parity: the two \(\Phi\) vectors have even parity and the two \(\Psi\) vectors have odd parity. A parity-even two-mode unitary, followed by occupation measurements, implements the measurement. No odd local pure state or broken parity reference is used.

Conditioned on the measurement outcomes, the endpoint pair is a Bell state. Its Pauli frame is a computable parity of the intermediate outcome bits (occupation-ordering conventions can change known signs). With unrestricted classical feedforward, send this frame to the final site. A local phase correction is even. For an occupation-flipping correction, introduce one local ancilla mode in \(|0\rangle\) and apply \(X_{\rm out}X_{\rm anc}\), an even two-mode unitary. It applies the required \(X\) to the endpoint and leaves the ancilla in \(|1\rangle\); the ancillary occupation retains the corresponding parity record. In a Jordan--Wigner ordering in which these two local modes are adjacent, \(X_{\rm out}X_{\rm anc}\) is a Majorana bilinear up to sign. Thus it is a legitimate local fermionic operation.

After these corrections the two endpoints are exactly in the chosen even Bell state, independently of the retained classical outcomes and ancillary parity record. Quantum gate depth and seed footprint are bounded independently of path length. Classical communication latency is linear in path length under a finite propagation-speed model; endpoint storage, classical computation, reset, and delivery remain paid. Postselection on the appropriate global outcome parities gives another conditional bypass, with acceptance and waiting paid.

**Consequence.** A light-cone argument conditioned only on preloaded classical labels does not extend to arbitrary global measurement-dependent feedforward. Counting only local quantum layers would omit a decisive causal resource. This bypass alone does not construct arbitrary thermal-state preparation with bounded coherent factories, but it rules out the proposed universal quantum-layer lower bound.

## The valid local-causal theorem

Consider an open nearest-neighbor half-filled hopping chain of \(N\) fermion modes,

\[
 H_N=-J\sum_{i=1}^{N-1}(c_i^\dagger c_{i+1}+c_{i+1}^\dagger c_i),
 \qquad \rho_N=e^{-\beta H_N}/Z_N,
 \quad 0<\beta J<\infty.
\]

Start from an arbitrary classical mixture of tensor products of parity-invariant quantum seed blocks of spatial diameter at most \(b\). The classical mixture may be globally correlated. All quantum gates, fresh ancillary states, noise environments, measurements, and classical feedback respect a spatial causal circuit of depth \(d\) and propagation range at most \(R\) per round. The classical seed is available at the start. A quantum block or bath initially entangled across remote sites counts as a seed, not as classical programming. The complete deterministic output is used; no zero-time global postselection is supplied.

There are constants \(c_{\beta J}>0,C_{\beta J}<\infty\) such that any output satisfying

\[
 \tfrac12\|\sigma_N-\rho_N\|_1\le\epsilon\le1/2
\]

must obey, for all sufficiently large odd \(N\),

\[
 b+2Rd\ \ge\ c_{\beta J}
 \min\{N,\log N+\log(1/\epsilon)\}-C_{\beta J}.
\]

This lower bound concerns **total causal extent**, including measurement-dependent classical propagation. It is not a claim that every individual carrier has a long coherent lifetime.

### Mechanism and proof

Write \(a_i=c_i+c_i^\dagger\), \(b_i=(c_i-c_i^\dagger)/i\), and let \(W=b+2Rd\). If endpoints have pairwise separation greater than \(W\), their backward cones meet disjoint parity-invariant quantum seed groups. In a local Stinespring dilation each pulled-back Majorana is odd in its own group. Every nonempty product of commuting bilinears

\[
 O_j=s_j i a_{u_j}b_{v_j}
\]

therefore has zero expectation on the prepared state, provided all endpoints are so separated. This holds for each globally preloaded classical label individually, and thus also after averaging over arbitrary correlated classical programming. The joint measurement law of the \(O_j\) is exactly uniform independent Rademacher.

For the thermal target, put \(x=\beta J\) and \(\kappa_m=\operatorname{asinh}[\pi(2m+1)/(2x)]\). The infinite-chain occupation covariance for positive odd distance \(r\) is

\[
 g(r)=\frac{(-1)^{(r-1)/2}}{x}
 \sum_{m\ge0}\frac{e^{-\kappa_m r}}{\cosh\kappa_m}.
\]

This follows by applying the partial-fraction expansion
\(\tanh z=2z\sum_{m\ge0}(z^2+\pi^2(m+1/2)^2)^{-1}\)
to the Fourier symbol \((1+\tanh(x\cos k))/2\). All terms have the same sign. On a ring of size \(L\equiv0\pmod4\), replace each exponential by

\[
 \frac{e^{-\kappa_m r}-e^{-\kappa_m(L-r)}}{1-e^{-\kappa_m L}}.
\]

For an odd-length open chain, the sine-transform image identity is
\(C_{ij}=g_{2(N+1)}(i-j)-g_{2(N+1)}(i+j)\).
Consequently, for sites in the middle half of the chain and odd separation \(r\le N/8\),

\[
 s_r\langle i a_i b_{i+r}\rangle_{\rho_N}
 \ge A_xe^{-\kappa_0r},
 \qquad
 |\langle i a_i b_j\rangle_{\rho_N}|
 \le B_xe^{-\kappa_0|i-j|},
\]

after increasing a fixed minimum length; \(A_x>0,B_x<\infty\) depend only on temperature. Choose an odd \(r>W\), and place \(M=\Theta(N/r)\) pairs at spacing \(4r\) in that middle region. Wick's rule and the second bound imply

\[
 \mathbb E_{\rho_N}S\ge MA_xe^{-\kappa_0r},
 \quad \operatorname{Var}_{\rho_N}S\le V_xM,
 \quad S=\sum_j O_j,
\]

with \(V_x\) independent of \(N,r\). The shallow output has mean zero and variance \(M\). Applying Chebyshev's inequality to the threshold at half the target mean gives

\[
 D(\sigma_N,\rho_N)
 \ge 1-\frac{4(V_x+1)}{MA_x^2e^{-2\kappa_0r}}.
\]

Thus fixed global accuracy requires
\(2\kappa_0r+\log r\ge\log N-O_x(1)\).
A single pair also yields \(D\ge A_xe^{-\kappa_0r}/2\), hence
\(r\ge\kappa_0^{-1}\log[A_x/(2\epsilon)]\).
Combining the bounds gives the displayed theorem whenever \(W\) is smaller than a fixed fraction of \(N\); otherwise its diameter-capped conclusion already holds. The bound saturates at finite diameter rather than diverging as \(\epsilon\to0\).

## Comparison and retained limits

The constant-depth spin Gibbs result arXiv:2609.35973 does not supply a contradiction: its fermionic version explicitly supplies a potentially global Gaussian seed and applies bounded block unitaries to it. This theorem quantifies a resource that such a seed can contain. The mixed-state lower-bound paper arXiv:2510.02275 already permits arbitrary mixtures of local circuits; shared classical randomness is therefore not, by itself, a new conceptual distinction. The present proof uses physical parity and exact vanishing of all separated odd-group moments. Nevertheless, global adaptive classical feedforward is a genuine bypass and makes this candidate weaker than an endpoint obstruction valid against arbitrary upstream quantum resources.

No fixed-component-noise matching preparation is asserted here. A known terminal isotropic Gaussian attenuator can be inverted when its spectral contraction leaves the target covariance inside \([0,I]\), but repeated unknown or gate-level noise is a separate operation. The accepted bounded noisy-factory theorem is unchanged.
