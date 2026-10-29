# Independent review: one-call coherent commutator acquisition
2026-10-29. Receiving review by a different research worker from the author.

## Decision and scope
Accepted as an exact complete CP-instrument construction, conditional on trusted isolated coherent controls and one common complete source map across branches. Accepted also: transpose convention, memory/reference handling, programming obstructions, and the stated compositional primitive-gate upper budget. This is not an accepted recovery algorithm, gap-free kernel preparation algorithm, practical acquisition advantage, noise-tolerant implementation, historical novelty claim, or executed elementary-gate compiler.

The governing phrase “control uniformly in its nine labels” must be read as the PURE coherent state `(1/3) sum_j |j>`, as used explicitly by the isometry/circuit and code, not a uniform classical mixture. This review makes that operational interpretation explicit without altering the frozen source.

## Independent derivation
For each Kraus and label, a plus flag and the two known controlled-Pauli windows give `(K P_j ± P_j K)/2`. There is no controlled unknown source. Uniform pure control contributes another factor 1/3. Purification of the fresh `I_D/D` contributes `1/sqrt(D)`. Tracing the system and its preparation reference therefore gives Kraus operators `sum_j |j> <u|(K P_j ± P_j K)|v> / (6 sqrt(D))`, exactly those in the manuscript. This derivation remains valid for unequal memory input/output dimensions and arbitrary initially entangled M:Q.

Writing Delta_j=K P_j-P_j K, the control jk entry is `sum Tr[Delta_j(I⊗sigma)Delta_k†]/(36D)`. With the manuscript H convention, this is H_kj/18, not H_jk/18. H is a PSD Gram matrix. A real commuting rotation vector c satisfies Hc=0 and hence H^T c=0. This does not turn the emitted positive state into a kernel state.

For arbitrary independent control rho, the same calculation gives `rho ∘ H^T / 2`. Uniform control postselection on normalized pure c gives probability `c†Hc/18`. These formulas do not represent H rho H. Complete plus/minus sum followed by control retirement leaves exactly one ordinary maximally-mixed-input source update on M:Q: pre-source Paulis preserve I_D/D and post-source target unitaries disappear under its trace. Conditioned or control-retaining outputs generally do not have that marginal.

## Scalar-objective comparator (additional consequence)
For a rotation coefficient vector c=vec(C), ||c||²=3, the earlier physical Bell-sign probe obeys

`q_positive(C) = c† H c / 8`.

Indeed, the twisted swap is `(I+sum c_j P_j)/2`, its commutator squared carries a factor 1/4, and the Bell-sign transition probability carries the previously proved `1/(4D)` factor. Feeding the *normalized* coefficient state c/sqrt(3) into this coherent instrument and accepting both minus flag and uniform-control projection gives

`p_scalar = c† H c / 54 = (4/27) q_positive(C)`.

Thus this direct scalar use has the same zero and objective but a smaller Bernoulli signal, in addition to extra coherent controls. It is not an improvement over the existing positive probe. This does not prove a no-go against every coherent downstream algorithm. The full complex Gram state contains coherences not determined by the real quadratic rotation objective alone; whether these help any separately specified operational task remains open. Its local dimension is fixed at nine, so omitting classical output by itself supplies no asymptotic advantage.

## Control count and source scope
The author's 12 addressed three-control Paulis decompose into 36 exact Toffolis. Using 6 CNOT and 9 one-qubit gates per Toffoli gives 216 and 324. Open-control conjugations add 44 X; Y/Z target conjugations add 16. Two encoded-qutrit preparations contribute 4 CNOT and 10 singles; flag preparation/readout contributes 2 H. For D=4, two reference Bell pairs add 2 CNOT and 2 H: total 222 CNOT and 398 singles. This is a valid compositional upper bound, not a simulated complete netlist or optimized hardware schedule. The peak 10/14-qubit counts include a reusable clean work qubit and the appropriate fresh references. Arbitrary controller noise, routing, idle, reset, and terminal operations are not certified by this calculation.

I read the copied N1041 governing proof. Its isolated coherent-check premise is compatible, but its dual-rail collective-dephasing cancellation protects the encoded flag under specific generators, not the nine labels or arbitrary acquisition controls. Its task-specific teleportation and protected physical services are not inherited. The source-freshness statement reports a failed plugin refresh and pinned fallback honestly; this review does not certify that pinned revision as latest.

## Tests and limits
New independent `check_rectangular_instrument.py` executes 16 random CPTP channels with memory dimensions 1→2, 2→3, 3→2 and 2→1. It compares a dense pre/source/post coherent circuit to the full Kraus instrument with retained entangled M:Q, verifies H transpose, the arbitrary complex-coefficient Schur map and postselection probability, and the unconditioned ordinary memory update. Maximum residual: 7.78e-16. These floating checks support exact derivations; they are not interval certificates or hardware observations.

Author scripts/source were inspected. Their nonunital, collective, identity, dephasing and kernel-not-filter counterexamples are consistent with the formulas. The review does not promote a history-dependent sequence of quantum outputs into iid copies, a density-exponentiation oracle, an inverse spectral gap, deterministic unknown-program implementation, or future symmetry guarantee. No control-error bound or readout statistics have been acquired here.
