# Audit of the explicit Ramsey calibration operation

**Verdict:** the gap identity, restricted-sign character inversion, and conservative shot bound in `calibration_operation.md` are correct under its stated commuting-stabilizer, coherent-control, bath-isolation and paid-preparation contract. There is no need for a controlled-Hamiltonian oracle. No substantive mathematical correction is required. The two practical clarifications below make the estimator and the distinction between statistical and physical costs explicit.

## 1. The Ramsey echo measures the asserted signed gap

Write \(H=\sum_a J_a(I-S_a)/2\), with a consistent stabilizer group, and let \(|\phi_R\rangle=R|\psi_0\rangle\). Its check eigenvalues are \(\chi_a(R)\). A Hermitian one-site Pauli \(P\) reverses exactly those eigenvalues indexed by \(B(P)\); therefore

\[
E(P\phi_R)-E(\phi_R)=\sum_{a\in B(P)}J_a\chi_a(R)=\Delta_P(R).
\]

The two controlled-P gates with a single intervening natural evolution give the joint state, up to an overall phase,

\[
\frac{|0\rangle+e^{-i\tau\Delta_P(R)}|1\rangle}{\sqrt2}
\otimes|\phi_R\rangle.
\]

Consequently the ancilla Y expectation is \(-\sin(\tau\Delta_P(R))\) in the usual Pauli convention. Neither the unknown common eigenenergy nor an unknown input qubit enters the experiment. It is performed on a prepared calibration state. The factor in the gap is J, not 2J, because the Hamiltonian uses projector terms \(J(I-S)/2\).

Taking \(\tau=\pi/(4dJ_{\max})\) ensures \(|\tau\Delta|\le\pi/4\). A fully specified estimator is

\[
\widehat\Delta=-\tau^{-1}\arcsin\!\left(\operatorname{clip}_{[-1/\sqrt2,1/\sqrt2]}\overline Y\right).
\]

Clipping is nonexpansive and inverse sine is \(\sqrt2\)-Lipschitz on this interval. Thus \(|\widehat\Delta-\Delta|\le\sqrt2|\overline Y-\mathbb E Y|/\tau\). The sign is merely a measurement convention; one can instead measure minus Y.

## 2. Stabilizer relations do not defeat the character inversion

The Pauli group modulo phases is a finite binary vector space with nondegenerate symplectic form. Each nonidentity physical Pauli S defines a nontrivial character \(R\mapsto\chi_S(R)\). Distinct stabilizer elements have distinct characters: two members of a consistent stabilizer group cannot differ only by a minus sign. Consequently

\[
\mathbb E_{R\text{ uniform Pauli}}[\chi_a(R)\chi_b(R)]=\delta_{ab}.
\]

The map from Pauli R to its signs on B(P) is linear over the binary field. Every attainable sign pattern has the same number of preimages. Enumerating its image by Gaussian elimination and averaging uniformly over that image therefore gives the same character expectation. It is unnecessary, and generally incorrect, to assume that all \(2^{|B(P)|}\) sign patterns are attainable independently.

It follows exactly that

\[
J_a=|\mathcal I_P|^{-1}\sum_{\chi\in\mathcal I_P}\chi_a\Delta_P(\chi),
\qquad a\in B(P).
\]

Estimating every gap to absolute error at most \(\delta_J\) estimates every recovered coefficient to that same accuracy, because this inversion is an average with coefficients of magnitude one. Each nonidentity S has an anticommuting one-site probe. Exact duplicate physical terms must first be aggregated, as the operation already says: their individual coefficients are unidentifiable, while their sum is the physically relevant coefficient. There is no replacement by a basis of independent checks.

## 3. Shot count and physical resources

Let \(M\le m2^d\) be the total number of probe-pattern settings. Independent ancilla measurements with outcomes in \(\{-1,1\}\), followed by the clipped estimator, require at most

\[
n\ge \frac{4}{\tau^2\delta_J^2}\log\frac{2M}{\alpha}
\]

shots per setting by Hoeffding's inequality and a union bound. Hence the stated \(O(m^3\epsilon_{\rm cal}^{-2}\log(m/\alpha))\) shot count is valid at fixed d, positive coupling bounds and temperature when \(\delta_J=O(\epsilon_{\rm cal}/m)\). This is deliberately conservative. It does not assert optimal information complexity.

The physical resource accounting in the operation is necessary and sufficient as a *conditional* construction: each shot pays for an initialized ground eigenstate, Pauli representative, controlled-P gates, isolation, timed evolution, readout and reset, including their compiled accuracy costs. The ideal echo permits reusing the data state, but no such reuse is needed for the conservative bound, and the report should not omit fresh preparation costs on that basis. A Pauli representative can be found over the whole device and compiled; no constant-support representative is needed for the stated polynomial conclusion.

Timing and coherent-control biases must be converted to a gap error and included in the allocated \(\delta_J\). For example, an interrogation-time error \(|\delta\tau|\) contributes at most \(dJ_{\max}|\delta\tau|/\tau\) to the inferred gap before other phase biases. Bath isolation by itself does not imply these biases are arbitrarily small at polynomial cost. The operation explicitly assumes calibrated primitives and charges their requested accuracy, which is the correct qualification.

For the thermometer, bounded-away-from-zero-and-one occupation and fixed known probe gap give the claimed inverse-Lipschitz conversion and \(O(\delta_\beta^{-2}\log(1/\alpha))\) independent-sample cost. Independence, the accuracy of thermal equilibration, and access to the same bath must be supplied and paid; an upper bound on bath rates alone supplies none of them. Finite-time preparation bias should enter the thermometer's error allowance as well as sampling fluctuation.

## 4. Calibration error is paid once for a retained background

For \(\lambda=\beta J\), the bound \(\mathrm{TV}(p_\lambda,p_{\widehat\lambda})\le\frac14\sum_a|\lambda_a-\widehat\lambda_a|\) applies directly to the constrained syndrome distribution; it does not need independent checks. The displayed product-uncertainty budget correctly bounds \(|\beta J_a-\widehat\beta\widehat J_a|\). Once this distribution is prepared, any subsequent fixed physical evolution and ideal adaptive logical-use protocol is a channel, including its complete transcript. Contractivity therefore pays the initial calibration discrepancy once. New independently prepared backgrounds, new calibration-dependent imperfect gate implementations, or a changing physical Hamiltonian require their own budget; they are outside that retained-background sentence.
