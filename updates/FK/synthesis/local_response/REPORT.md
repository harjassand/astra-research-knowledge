# Finite-patch certification of a local thermal response

**Status:** conditional finite-patch theorem derived; exact small-model identities independently checked. The proof composes a finite-range spin Lieb–Robinson bound with a separate thermal-boundary estimate. The latter is available under an explicit high-temperature hypothesis, or must be supplied by another verified mixing theorem. This is not a general locality theorem, a Gibbs-preparation result, a physical validation, or a priority claim.

A local imaginary-frequency susceptibility can be certified from a finite patch without reconstructing the global partition function or spectrum, provided that both (i) dynamics outside the patch have a certified locality envelope and (ii) the full and patch thermal marginals are close on the region reached by the response light cone. These are distinct inputs. Local faithfulness, global covariance conditioning, or a local measurement variance bound alone does not supply either input. For small frequency regulator \(\eta\), the sufficient patch radius in this certificate scales as \(v_{\rm LR}\eta^{-1}\log(1/\epsilon)\), and the patch Gibbs state still has a preparation or computation cost.

## Target and model

Let \(\Lambda\) be a finite graph with finite-dimensional spin sites and Hamiltonian
\[
H=\sum_{Z\subseteq\Lambda} h_Z,
\]
where each Hermitian interaction has diameter at most \(r_{\rm int}\), norm at most \(J\), and at most \(z\) interaction terms meet any one site. Let \(A=A^\dagger\) be supported on \(X\subset\Lambda\), with \(s_A=|X|\) and \(a=\|A\|_{\rm op}\). Fix inverse temperature \(\beta>0\) and regulator \(\eta>0\), and write \(\rho_H=e^{-\beta H}/\operatorname{Tr}e^{-\beta H}\).

Use the supplied thermal-response convention
\[
d\mu_{\beta,H,A}(\Delta)
 =\sum_{E_m>E_n}(p_n-p_m)|A_{nm}|^2
   \delta_{E_m-E_n}(d\Delta),\qquad
\chi_{\beta,H,A}(i\eta)
 =\int_0^\infty\frac{2\Delta}{\Delta^2+\eta^2}\,
   d\mu_{\beta,H,A}(\Delta).
\]
The spectral identity gives
\[
\chi_{\beta,H,A}(i\eta)
 =\int_0^\infty e^{-\eta t}G_H(t)\,dt,\qquad
G_H(t)=i\operatorname{Tr}\rho_H[A_H(t),A],\qquad
A_H(t)=e^{itH}Ae^{-itH}.
\]
For each positive gap \(\Delta=E_m-E_n\), the commutator signal contributes \(2(p_n-p_m)|A_{nm}|^2\sin(\Delta t)\), and the Laplace transform of \(\sin(\Delta t)\) is \(\Delta/(\Delta^2+\eta^2)\). Also \(|G_H(t)|\le 2a^2\).

For the graph ball \(B_R(X)\), define the open-boundary patch Hamiltonian \(H_R=\sum_{Z\subseteq B_R(X)}h_Z\) and its Gibbs state \(\rho_R\). The patch estimate is \(\chi_{\beta,H_R,A}(i\eta)\), with patch dynamics and patch Gibbs state. The theorem compares it with the finite-full-system response. A thermodynamic-limit target needs an additional finite-volume convergence error.

## Finite-patch response theorem

Assume the model class supplies constants \(c_{\rm LR},v_{\rm LR},\xi_{\rm LR}>0\) such that the following local-approximation estimate holds whenever \(S_t\subseteq B_R(X)\):
\[
\|A_H(t)-A_{S_t}(t)\|_{\rm op},\
\|A_{H_R}(t)-A_{S_t}(t)\|_{\rm op}
 \le c_{\rm LR}s_Aa\,e^{-\ell/\xi_{\rm LR}},\qquad
S_t=B_{r_A+v_{\rm LR}t+\ell}(X).
\tag{LR}
\]
Here \(r_A\) contains the radius of \(X\), and \(A_{S_t}(t)\) evolves under the Hamiltonian restricted to \(S_t\). This is the bounded finite-range spin Lieb–Robinson interface of [Bravyi, Hastings, and Verstraete](https://arxiv.org/abs/quant-ph/0603121v1); its constants must follow from the actual range, graph growth, and interaction-strength envelope.

For a region \(S\subseteq B_R(X)\), let \(\rho_H^S,\rho_R^S\) be the reduced Gibbs states. Suppose a certified thermal-boundary estimate \(\delta_{\rm th}(S,R)\) satisfies
\[
\|\rho_H^S-\rho_R^S\|_1\le\delta_{\rm th}(S,R).
\]
For \(T>0,\ell\ge0\), put
\[
r_*=r_A+v_{\rm LR}T+\ell,\qquad S_*=B_{r_*}(X),
\]
and require \(S_*\subseteq B_R(X)\). Then
\[
\boxed{
|\chi_{\beta,H,A}(i\eta)-\chi_{\beta,H_R,A}(i\eta)|
\le \frac{1-e^{-\eta T}}{\eta}
 \left(4c_{\rm LR}s_Aa^2e^{-\ell/\xi_{\rm LR}}
       +2a^2\delta_{\rm th}(S_*,R)\right)
 +\frac{4a^2}{\eta}e^{-\eta T}.
}
\tag{1}
\]

The last term is the finite-time Laplace tail, the first term inside parentheses is dynamics locality, and the second is equilibrium boundary error. Thus the certificate is finite once the local patch Hamiltonian, a verified global finite-range/strength/geometry envelope, and a certified thermal marginal error are available. The full-system partition function and spectrum are not needed.

**Proof.** For \(t\le T\), the full and patch systems share the restricted Hamiltonian on \(S_t\). Let \(O_t=i[A_{S_t}(t),A]\). Its support lies in \(S_t\subseteq S_*\) and \(\|O_t\|_{\rm op}\le2a^2\). Replacing either full or patch evolved observable by \(A_{S_t}(t)\) changes its commutator expectation by at most \(2a\,c_{\rm LR}s_Aa e^{-\ell/\xi_{\rm LR}}\). The two dynamics replacements together cost at most \(4c_{\rm LR}s_Aa^2e^{-\ell/\xi_{\rm LR}}\). The difference of the two expectations of \(O_t\) is at most \(2a^2\delta_{\rm th}(S_*,R)\), by trace duality. Integrating on \([0,T]\) against \(e^{-\eta t}\) gives the first term of (1). Each original signal has magnitude at most \(2a^2\), so the two tails sum to at most \(4a^2e^{-\eta T}/\eta\). This proves the claim. \(\square\)

## Explicit high-temperature thermal-boundary term

For a bounded spin system with a finite interaction graph, let \(\alpha_{\rm an}\) be its interaction-animal growth constant and \(J\) the maximum local-term norm. [Kliesch, Gogolin, Kastoryano, Riera, and Eisert](https://arxiv.org/abs/1309.0816v4) give this explicit high-temperature estimate (Theorem 2 and Corollary 2):
\[
\beta<\beta_*:=
\frac{1}{2J}\ln\!\left(
 \frac{1+\sqrt{1+4/\alpha_{\rm an}}}{2}\right),\qquad
\xi_{\rm th}(\beta)=
\left|\ln\!\left[\alpha_{\rm an}e^{2\beta J}
                       (e^{2\beta J}-1)\right]\right|^{-1}.
\]
If \(d=\operatorname{dist}(S,\partial B_R)\ge
L_0(\beta,|\partial S|)\), their corollary yields
\[
\delta_{\rm th}(S,R)=
\frac{4\beta J|\partial S||\partial B_R|}
     {\ln(3)(1-e^{-1/\xi_{\rm th}})}
e^{-d/\xi_{\rm th}},\qquad
L_0(\beta,b)=\xi_{\rm th}
\left|\ln\frac{\ln(3)(1-e^{-1/\xi_{\rm th}})}{b}\right|.
\tag{2}
\]
The boundary counts are those of the interaction graph/hypergraph in that theorem. Apply (2) with \(S=S_*\). Interpolating the boundary interactions scales their strengths between zero and their original values, so the same range, strength, and graph-growth envelope applies throughout. The estimate is uniform over the exterior within that envelope and does not require its exact coefficients or the full partition function.

This route does not cover arbitrary \(\beta\). The source notes long-range correlations in low-temperature two-dimensional ferromagnetic Ising models. Outside its high-temperature range, one may substitute a separately certified model-specific \(\delta_{\rm th}\); without one, the thermal patch error remains unknown.

## Error and cost at small \(\eta\)

Allocate total deterministic error as \(\epsilon_{\rm LR}+\epsilon_{\rm th}+\epsilon_{\rm tail}\). Sufficient conditions are
\[
T\ge\eta^{-1}\ln\frac{4a^2}{\eta\epsilon_{\rm tail}},\qquad
\ell\ge\xi_{\rm LR}\ln\frac{4c_{\rm LR}s_Aa^2}
                                  {\eta\epsilon_{\rm LR}},
\]
rounded upward and clipped at zero, together with
\[
\delta_{\rm th}(S_*,R)\le\frac{\eta\epsilon_{\rm th}}{2a^2},
\qquad
R-r_*\ge L_0(\beta,|\partial S_*|)
\]
for the high-temperature estimate. Equation (1) is then at most the allocated sum. The factor \(|\partial B_R|\) in (2) depends on the unknown radius, so the certified radius is the smallest \(R\) satisfying the displayed inequalities; it must not be dropped. On a bounded-degree \(D\)-dimensional lattice, \(|\partial B_R|=O(R^{D-1})\), giving a thermal buffer of order
\(\xi_{\rm th}[\log(1/\epsilon_{\rm th})+(D-1)\log R+
\log(\beta J|\partial S_*|)]\), subject to the \(L_0\) threshold. Meanwhile \(r_*=r_A+v_{\rm LR}T+\ell\). The sufficient dynamical radius therefore scales as \(v_{\rm LR}\eta^{-1}\log(1/\epsilon_{\rm tail})\) at small \(\eta\). The exact gapless example below shows why a regulator-independent radius is false in general.

Two implementation routes remain explicitly charged:

1. **Model computation.** For site dimension \(q\) and \(n_R=|B_R|\), dense patch diagonalization costs \(O(q^{3n_R})\) arithmetic operations and \(O(q^{2n_R})\) memory; the resulting local spectral sum costs \(O(q^{2n_R})\). These are arithmetic counts, not bit-complexity or a practical-efficiency claim. This avoids a full-system spectrum but remains exponential in patch size. The complete model-computation charge also includes \(C_{\rm acquire}(B_R)+C_{\rm verify-env}(\Lambda)+C_{\rm certify-th}(\beta,S_*,R,\delta_{\rm th})\); verifying the global envelope or a model-specific thermal bound may itself require global work and is not free.

2. **Physical/digital response sampling.** Let \(G_R(t)=i\operatorname{Tr}\rho_R[A_R(t),A]\). Use midpoint quadrature on \([0,T]\) with \(M\) nodes \(t_j=(j-\tfrac12)h\), \(j=1,\ldots,M\), step \(h=T/M\), weights \(w_j=h e^{-\eta t_j}\), and \(W_M=\sum_jw_j\). If \(z_X\) terms meet \(X\), then
\[
|G'_R(t)|\le2a\|[H_R,A]\|\le4a^2Jz_X.
\]
Thus \(f(t)=e^{-\eta t}G_R(t)\) is Lipschitz with
\(L_f=4a^2Jz_X+2\eta a^2\), and midpoint quadrature error is at most \(L_fT^2/(4M)\). It suffices to choose \(M\ge L_fT^2/(4\epsilon_{\rm quad})\). Suppose a calibrated Hadamard-test or block-encoding procedure returns an unbiased random variable in \([-2a^2,2a^2]\) at each node. With \(N\) independent Gibbs copies per node, a union bound and Hoeffding give total signal error at most \(\epsilon_{\rm stat}\) with failure probability \(\delta_{\rm stat}\) if
\[
N\ge\frac{8a^4W_M^2}{\epsilon_{\rm stat}^2}
       \ln\frac{2M}{\delta_{\rm stat}}.
\tag{3}
\]
The total number of independent equilibrium copies is \(MN\). Since \(W_M\le1/\eta\), the worst-case shot bound has \(N=O(a^4\eta^{-2}\epsilon_{\rm stat}^{-2}\log(M/\delta_{\rm stat}))\). For fixed local parameters and error allocations, \(T=O(\eta^{-1}\log(1/\eta))\), \(M=O(\eta^{-2}\log^2(1/\eta)/\epsilon_{\rm quad})\), and thus \(MN=O(\eta^{-4}\log^2(1/\eta)\log(M/\delta_{\rm stat}))\), up to parameter/error factors. A trace-distance preparation error \(\epsilon_{\rm prep}\) per copy adds at most \(2a^2W_M\epsilon_{\rm prep}\); implemented-evolution operator error \(\zeta_U\) at each node adds at most \(2aW_M\zeta_U\). The total response-estimation error is bounded by \(\epsilon_{\rm quad}+\epsilon_{\rm stat}+2a^2W_M\epsilon_{\rm prep}+2aW_M\zeta_U\), in addition to the patch error (1). Gibbs preparation bias, controlled time evolution, observable calibration, and readout noise are separate charges. A cost expression is
\[
C_{\rm acquire}(B_R)+C_{\rm verify-env}(\Lambda)+C_{\rm certify-th}(\beta,S_*,R,\delta_{\rm th})
+MN\left(C_{\rm Gibbs}(B_R,\beta,\epsilon_{\rm prep})
+C_{\rm control}(B_R,T,\zeta_U)+C_{\rm readout/calibration}\right).
\]
These terms remain model-dependent and unknown until supplied or measured.

[Brandão–Kastoryano](https://arxiv.org/abs/1609.07877v2) provide a conditional preparation route: for finite-dimensional bounded local Hamiltonians, uniformly decaying correlations and a uniform approximate-Markov property on every induced subgraph imply a local-channel thermal-state preparation theorem (arXiv:1609.07877v2, Theorem 6). It assumes efficient implementation of the local channels and gives a global trace-distance guarantee. It is not a generic Gibbs-preparation oracle. The high-temperature local-expectation result is likewise not, by itself, a physical Gibbs sampler.

The response routes need the patch Gibbs state, not the global normalizer \(Z_H\). Certification still needs the global interaction-class envelope to bound omitted dynamics and exterior influence. If only the patch Hamiltonian is known and the outside range, strength, or geometry is unknown, neither (LR) nor (2) follows.

## Relation to the thermal-response target and capital

The incoming thermal report targets the observable-specific positive measure \(\mu_{\beta,A}\), not the full spectral function, and distinguishes explicit model access from equilibrium-preparation cost. Its finite-anchor analysis finds that one source/anchor architecture tends to the wrong zero-temperature response; it does not rule out the local Kubo-patch calculation here. This route uses real-time local dynamics and local Gibbs marginals, not a reconstructed transition list.

| Capital | Exact useful input | What it does not supply here |
|---|---|---|
| N705 | Source-claimed local KMS faithfulness for a boundedly coupled finite subsystem and arbitrary finite bath; a finite-band absolute KMS floor. | The finite-band result allows zero-frequency weight and is expressly not a nonzero-frequency absorption, mixing, or time-to-resolution bound. It supplies no thermal boundary decay or patch-state preparation. Its review gate remains open. |
| N711 | Source-claimed all-direction BKM covariance floor for a bounded-incidence Pauli dictionary and unrestricted full-rank Gibbs state, with no clustering assumption. | A lower covariance floor is not spatial clustering, an upper response bound, or a Gibbs sampler. The manuscript and independent-review gate remain open. |
| N712 | Source-claimed fixed local Pauli readout and variance certificate for static equilibrium parameter Fisher information, with independent Gibbs copies and calibrated detectors. | It does not measure the real-time Kubo correlator or bound Gibbs-marginal changes at a patch boundary. Its sample count excludes state preparation. Its review gate remains open. |
| N625 | Source-reported conditional hardness for a global partition-function approximation family at \(\beta=n+2\). | It does not establish hardness of local susceptibility or remove patch Gibbs costs. Its growing-\(\beta\) instances are outside the fixed high-temperature threshold in (2); its independent proof gate remains open. |

None of N705, N711, N712, or N625 is a premise in (1). Their result statuses remain as reported in the pinned capital: N705/N711/N712 are source-derived and unreviewed; N625 is source-reported with an open independent audit. The original dimensional, temperature, and dictionary restrictions remain unchanged. This is not an inverse-Hamiltonian-learning theorem and does not close any of those gates.

## Counterexamples and exact witnesses

### Gapless harmonic chain

Consider a one-dimensional massless harmonic chain with Dirichlet endpoints,
\[
H_R=\frac12\sum_jp_j^2+\frac12q^TK_Rq,\qquad
(K_R)_{jj}=2\kappa,\quad (K_R)_{j,j+1}=-\kappa,
\]
on sites \(-R,\ldots,R\), with \(A=q_0\). For each finite chain, the Gibbs state exists at \(\beta>0\). Normal-mode decomposition gives, at every finite temperature,
\[
\chi_R(i\eta)=[(K_R+\eta^2I)^{-1}]_{00}
 =\frac{\tanh((R+1)\theta)}{2\kappa\sinh\theta},\qquad
\cosh\theta=1+\frac{\eta^2}{2\kappa}.
\]
The infinite-chain response at \(\eta>0\) is
\[
\chi_\infty(i\eta)=\frac{1}{2\kappa\sinh\theta}
 =\frac{1}{\eta\sqrt{\eta^2+4\kappa}}.
\]
Its exact relative truncation error is \(1-\tanh((R+1)\theta)\), so relative error at most \(\epsilon\) requires
\[
R\ge\left\lceil\frac{\operatorname{artanh}(1-\epsilon)}{\theta}\right\rceil-1
 \sim\frac{\sqrt{\kappa}}{2\eta}\ln\frac{2}{\epsilon}
 \quad(\eta\downarrow0).
\]
The dispersion is gapless, \(\omega(k)\sim\sqrt{\kappa}|k|\). This is a bosonic unbounded-site model, so it is not an application of the bounded-spin LR/high-temperature theorem; its closed form is its own certificate. The exact example shows that finite-temperature access does not eliminate the small-\(\eta\) response length.

The independent implementation compares the formula with dense tridiagonal inversion. At \(\eta=0.05,\kappa=1,R=30\), relative error is 8.624%, while the exact 1% radius is 52; closed-form/matrix discrepancy is \(4.62\times10^{-14}\). Four \(\eta\)-values and radius checks are recorded in the results JSON.

### Low-temperature boundary sensitivity in finite-range Ising

Take a ferromagnetic nearest-neighbour Ising chain with longitudinal field \(h\) and transverse field \(g\) only at the center, and remote end fields \(+b\) or \(-b\). Let \(A=Z_0\). All noncentral \(Z_j\) commute with the Hamiltonian. Conditional on their values, the center is a two-level system with effective field \(h_{\rm eff}\). For uniformly polarized neighbors of coordination \(z\), \(h_{\rm eff}^{\pm}=h\pm zJ\), \(E_\pm=\sqrt{(h\pm zJ)^2+g^2}\), and the exact conditional response is
\[
\chi_\pm(i\eta)=
\tanh(\beta E_\pm)\frac{4g^2}{E_\pm(4E_\pm^2+\eta^2)}.
\]
For \(h\ne0\), these conditional values differ. The thermal-locality source notes long-range correlations in low-temperature two-dimensional ferromagnetic Ising models, so finite range alone does not imply a uniform thermal-mixing guarantee. The exact finite-size check below demonstrates actual response sensitivity to remote boundaries; it does not establish non-decay as distance grows at fixed temperature.

The check used a 7-site chain at \(\beta=5,\eta=0.25,J=1,h=0.5,g=1,b=2\), compared with the identical open 3-site patch. Exact block decomposition and finite thermal traces give responses 0.051116 for plus end fields and 0.169863 for minus end fields; the patch response is 0.052981. The remote-boundary gap is 0.118747. A separate diagonal Ising calculation is also in the JSON. These finite examples show the mechanism, not an asymptotic phase theorem by themselves.

### Hidden long-range sector when no range promise is known

For any proposed patch radius, put an unseen qubit at distance \(R\) and allow
\[
H_s=-hZ_0-\lambda Z_0Z_R-sbZ_R,\qquad
A=X_0,\quad s\in\{+1,-1\}.
\]
The patch Hamiltonian agrees for the two signs, but the unseen qubit changes the local transition gap. Exact two-qubit thermal summation at \(\beta=2,\eta=0.25,h=0.3,\lambda=b=1\) gives responses 0.756551 and 1.199986, a gap 0.443435. This violates the finite-range premise and shows why a patch alone cannot certify its exterior when the range envelope is absent.

## Missing operation and scope verdict

The high-leverage missing operation is a **certified local Kubo-response interface** with three inputs: (1) a finite patch plus a verified global range, strength, graph-growth, and boundary envelope, sufficient to compute the LR cone and thermal marginal error; (2) independent patch Gibbs copies, or a declared Gibbs-preparation routine with trace-distance and per-copy cost guarantees; and (3) calibrated real-time commutator measurement or controlled Hamiltonian simulation with bounded outcomes, time-control error, and shot count as in (3).

High-temperature locality supplies the thermal component of the envelope under its stated hypotheses. At lower temperature, an independently proved clustering or local-indistinguishability theorem could replace it. N705 faithfulness, N711 covariance conditioning, N712 readout bounds, and N625 partition hardness do not supply that missing thermal-boundary operation. The result is an observable-specific finite-patch route, not a full spectral reconstruction or global Gibbs description. Novelty, material advantage, fast low-temperature preparation, and improved small-\(\eta\) scaling beyond the stated bound remain unknown.

## Verification boundary

The exact-model code is independently written for this packet, not a replay of supplied capital code. It checks the harmonic resolvent against dense matrices, checks its radius/error identity, and evaluates finite Ising responses by explicit finite sums or exact blocks. Floating-point agreement verifies these finite identities at the displayed precision. It does not validate the general high-temperature theorem, provide interval proof, establish efficient implementation, or demonstrate a laboratory result. No files under the pinned capital checkout were modified.
