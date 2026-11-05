# Primary comparison audit — broad preparation round, 5 November 2026

This note records current primary-source conditions. It does not re-audit the accepted memory, loader, bath or Bell/tree boundary results. The main scientific distinction is between (i) existence of a positive preimage, (ii) efficient sampling/computation of its preparation, and (iii) delivery of an unencoded global target through imperfect apparatus. Ordinary fault-tolerant methods receive the same controls and can use any new state-specific precompensation theorem.

## Decisive attribution and new work

The ideal high-temperature operation is already available in BLMT: interacting, noncommuting high-temperature Gibbs states are classical mixtures of product Pauli states, with a polynomial classical sampler and depth-one ideal quantum preparation. Their proof already contains quantitative coefficient slack, so shrinking the local Bloch palette is a corollary of an existing mechanism. Do not sell a new name for that ideal sampler, or the absence of interqubit quantum gates by itself, as a new operation.

The strongest new bridge found in this audit is a robust **all-temperature one-dimensional** block-mixture adaptation of the more recent 2609.35973 result. Its existing pure-block construction can be modified to retain a uniform spectral floor in each sampled bounded block. The definitive derivation, incorporating a separate independent audit, is in `robust_1d_block_opening.md`. This makes bounded-block inverse-noise operations possible uniformly in chain size. Actual physical realization uses the already earned full fault-tolerant/product-boundary compiler; random partition scheduling and routing have not been independently closed by the finite-cell proposal.

## 1. BLMT high-temperature separability and preparation

**Ainesh Bakshi, Allen Liu, Ankur Moitra, Ewin Tang**, *High-Temperature Gibbs States are Unentangled and Efficiently Preparable*, arXiv:2403.16850v2, revised 24 February 2025.

Primary full text: https://arxiv.org/pdf/2403.16850

Theorem 1.7 covers bounded-degree low-intersection Pauli Hamiltonians at beta<beta_c=1/(gamma dK), with universal gamma. It outputs a classical distribution over product Pauli eigenstates approximating the full Gibbs state in trace norm, and provides a polynomial sampler. Theorem 4.18 bounds the monomial coefficient by |c|<=(beta/beta_c)^t; each degree-t monomial has support at most Kt. Section 4.3 explicitly observes unused coefficient slack. Hence beta/beta_c<=u^K allows the same factors to be decomposed into product states with Bloch radius u<1 rather than pure local states. This is a direct constructive corollary of the existing proof. The published operation uses ideal local preparation; it does not by itself include apparatus acquisition, noisy controller delivery or global-accuracy calibration costs.

## 2. Stronger 1D constant-depth preparation at every fixed positive temperature

**Saul Pilatowsky-Cameo, Georgios Styliaris, Ainesh Bakshi, Daniel Malz**, *One-dimensional quantum Gibbs states in constant circuit depth*, arXiv:2609.35973v1, 28 September 2026.

Primary full text: https://arxiv.org/pdf/2609.35973

Theorems 1–2 give an exact mixture of pure product states over contiguous bounded blocks for every fixed beta and finite interaction range, plus polynomial classical sampling to global trace error epsilon. The stated block bound is doubly exponential in beta, with a very unfavorable range-dependent constant. This already yields constant ideal quantum depth. Appendix C contains mixed QPI factors with explicit floors, but Appendix A subsequently introduces rank-one spectral factors; the final theorem supplies pure blocks. Thus fixed-noise raw delivery is not an immediate consequence of the theorem statement. The new adaptation halves the source cut factor, replaces sharp spectral factors by full-rank ones, and retains mixed Pauli factors, giving a uniform interior block mixture. Its output remains compatible with the source's classical forward-backward sampler.

Supporting primary source for local dressing/inverse bounds:

**Bakshi, Choi, Pilatowsky-Cameo**, *Entanglement in quantum spin chains is strictly finite at any temperature*, arXiv:2602.13386v2, updated 2 November 2026: https://arxiv.org/pdf/2602.13386 . Lemma 8.4 explicitly writes the finite-support Araki dressing matrix as a product of Gibbs exponentials and bounds its norm and inverse. The v2 improves constants. Its original theorem gives bounded-bond MPS mixtures, while 2609.35973 gives the stronger bounded-block representation used here.

## 3. Existing quantum error pre-compensation

**Chengjie Zhang, Liangsheng Li, Guodong Lu, Haidong Yuan, Runyao Duan**, *Quantum error pre-compensation for quantum noisy channels*, arXiv:2309.01434; journal Phys. Rev. A 106, 042440 (2022).

Primary full text: https://arxiv.org/pdf/2309.01434

For a known channel and known target, this work analytically solves the inverse-channel linear system when an exact positive preimage exists, and uses semidefinite programs to optimize fidelity otherwise. The setting is not limited to one-qubit targets; it includes entangled and multipartite examples. It does not provide a dimension-independent positivity threshold or efficient preparation guarantee for interacting many-body families. General matrix inversion/SDP has exponentially growing Hilbert-space dimension, and physical construction of the inverse input remains a separate operation. New work should be described as structural/operational consequences of precompensation, not invention of precompensation.

## 4. Fault-tolerant input/output and modern qLDPC preparation

**2408.05260v3**, *Fault-tolerant quantum input/output*: https://arxiv.org/html/2408.05260v3 .

This is a general same-input/output circuit-simulation framework accounting for noisy boundaries and general coherent errors, with local-stochastic specializations. It is an essential comparator, not a reason to assume an ideal raw output. Its boundary noise need not be independent of the full retained record. The accepted Astra Bell/tree compiler has already earned its additional independence conditions under its stated noise model; do not reprove or generalize that input without a bridge.

**2602.16948v2**, updated 29 September 2026: https://arxiv.org/html/2602.16948v2 .

Theorem 44 prepares an x-qubit target circuit of polynomial size and O(x) workspace with O(x) physical qubits, to a vanishing simulation error followed by a local-stochastic output channel of parameter (kappa_1 delta)^(kappa_2). This is a strong constant-quantum-space-overhead comparator. It leaves a residual physical output channel; that channel is not automatically an independent tensor product and cannot automatically be canceled by a product inverse. Conversely, an ordinary controller given the same earned product boundary and new structural inverse can perform the same preparation. No exclusive hardware or total-resource advantage follows from composing those ingredients.

## 5. Autonomous correction/computation, current v3

**Dunnweber, Styliaris, Trivedi**, *Quantum Memory and Autonomous Computation in Two Dimensions*, arXiv:2601.20818v3, 25 September 2026.

Primary full text: https://arxiv.org/html/2601.20818v3

The v3 gives a formal local-noise theorem in diamond norm, allowing correlated and possibly non-Markovian fault expansions. It achieves polynomial-logarithmic space/time overhead for finite logical computation using engineered local dissipative QCA, code correction, Toom correction and repair of mutable clock/program structure. Its formal theorem assumes a sufficiently correct hierarchical initial state. Section VI discusses recursive encoded preparation, classical measurement plus decoding at readout, or storing the encoded quantum output. Continuous-time dynamics consists of local CPTP update generators. These are active autonomous correction dynamics, not a passive Hamiltonian with a Davies bath. It does not directly deliver arbitrary unencoded Gibbs states at vanishing global trace error through fixed noisy physical output. It remains a legitimate alternative controller under compatible access and preparation assumptions; the new state-specific inverse theorem can be used by such a controller too.

## 6. Existing Gibbs samplers and current all-temperature 1D result

**Rouze and Stilck Franca**, *Rapid mixing of Gibbs samplers via quantum Dobrushin–Shlosman conditions*, arXiv:2610.03578, 2 October 2026: https://arxiv.org/pdf/2610.03578 . This is the strongest ideal 1D cost comparator found in the targeted follow-up. Theorems 5.1 and 3.11 give all-fixed-temperature logarithmic trace-norm mixing and N polylog(N/epsilon) gates plus classical bit operations, respectively, from digital bounded local terms and fixed construction parameters. The updates combine Gibbs resets, quantum belief propagation and KMS completion. The circuit prefactor is doubly exponential in beta times interaction strength. Its stability theorem concerns target-Hamiltonian perturbations, not uncontrolled fixed apparatus noise. It does not supply the product-noise preimage operation. Our source classical sampler remains only polynomial(N,1/epsilon); no near-linear speed comparison is claimed.

**Chen, Kastoryano, Gilyen**, *An efficient and exact noncommutative quantum Gibbs sampler*, arXiv:2311.09207: https://arxiv.org/abs/2311.09207 . It constructs an efficiently implementable exactly detailed-balanced Lindbladian for general noncommuting Hamiltonians. Its runtime depends on mixing, and its ideal implementation still requires accuracy control.

**Rouze, Stilck Franca, Alhambra**, *Optimal quantum algorithm for Gibbs state preparation*, arXiv:2411.04885v2: https://arxiv.org/html/2411.04885v2 . It proves high-temperature logarithmic mixing for a suitable exact Gibbs Lindbladian under locality/Lieb–Robinson conditions. This is a stronger ideal mixing comparator than slow generic dynamics. It does not eliminate fixed uncontrolled output noise or include a general physical precompensation compiler.

**Zhiyan Ding, Bowen Li, Ruizhe Zhang**, *Efficient thermalization of one-dimensional noncommuting Hamiltonians via system-bath interactions with Theta(n) ancilla qubits*, arXiv:2611.03422v1, 2 November 2026.

Primary full text: https://arxiv.org/pdf/2611.03422

Theorem 1.1 covers every fixed positive temperature, nearest-neighbor bounded interactions and fixed local dimension, with arbitrary initial states and global trace error epsilon. It uses Theta(n) bath ancillas, prescribed thermal resets, random bath frequencies and durations, and prescribed local time-dependent couplings. The coupling obeys alpha^2=c epsilon/n. Expected total Hamiltonian evolution time is roughly O(n/epsilon), with logarithmic factors. That metric does not count all reset, calibration, metrology or uncontrolled component-noise costs. This newer result prevents claiming that 1D all-temperature thermalization itself is unavailable. It does not supply the fixed-noise raw-output operation targeted by robust block precompensation.

## 7. Related noisy-channel and variational methods — boundaries

**Putterman, Zlokapa and Cotler**, *When quantum thermal states look classical*, arXiv:2607.28536v2, 5 October 2026: https://arxiv.org/pdf/2607.28536 . Theorem 2 strengthens BLMT's ideal high-temperature comparator to bounded-site-strength long-range Pauli Hamiltonians. At beta<=1/(4096 e s k), its polynomial classical algorithm samples product stabilizer states; Theorem 1 gives tight separability scales. The final theorem remains a high-temperature pure-product operation, not an all-temperature 1D mixed-block or inverse-noise theorem. Its runtime includes an n^11 epsilon^(-5) term, so the mathematical polynomial should not be portrayed as a practical resource advantage.

**Brunner et al.**, *Lindblad engineering for quantum Gibbs state preparation under the eigenstate thermalization hypothesis*, https://arxiv.org/html/2412.17706v3 . Its Section 6 proves a real stochastic-noise resilience bound. For noiseless convergence B exp(-alpha M) and total per-step noise lambda, its asymptotic trace-error bound is B lambda/[1-(1-lambda) exp(-alpha)]. This is a noise-dependent residual error, not arbitrary accuracy at fixed lambda. The efficiency theorem assumes ETH; Section 7 numerically studies algorithmic and depolarizing gate errors. Its useful robustness result is preserved at that scope.

**Arad, Firanko, Gurevich**, *Local quantum channels giving rise to quasi-local Gibbs states*, arXiv:2408.08672v2: https://arxiv.org/pdf/2408.08672 . Its stationary-state logarithm has a geometrically local perturbative expansion; the generally exponential coefficient-norm bound needed for full quasi-locality is an explicit additional condition, not a general theorem. A reset-channel case gives local-observable perturbation algorithms. It neither inverts a specified arbitrary Gibbs target nor provides global raw-state preparation to arbitrary accuracy at fixed uncontrolled apparatus noise.

**Granet, Dreyer**, *Adiabatic preparation of thermal states and entropy-noise relation on noisy quantum computers*, arXiv:2509.05206: https://arxiv.org/abs/2509.05206 . This is a meaningful physical comparator for local thermal observables: it assumes thermalization, studies entropy density and energy-temperature behavior, and reports numerical/hardware evidence of resilience. Its claimed endpoint is not a uniform theorem of arbitrarily small global trace error under a fixed component-noise contract. No dismissal of that operationally useful weaker objective is warranted.

## What a completed consequence can honestly assert

The audited robust block proof and compatible delivery composition imply that every fixed-temperature bounded-range 1D qubit Gibbs state can be prepared to arbitrarily small global error with a nonzero component-noise tolerance depending only on temperature, interaction range and the fixed physical compiler—not on chain length or requested accuracy. The classical Gibbs sampler, local inverse matrix computations, known-input fault-tolerant preparation and noisy boundary are all inside the operation. The claim is a broad existence/constructive threshold theorem for interacting targets, with exceptionally bad constants. It does not establish practical feasibility, lower total energy/spacetime, an unknown-input channel, a passive-hold guarantee, or a universal result for every fault-tolerant boundary law. The targeted prior-art search found no primary statement of the precise robust theorem; no exhaustive priority claim is made.
