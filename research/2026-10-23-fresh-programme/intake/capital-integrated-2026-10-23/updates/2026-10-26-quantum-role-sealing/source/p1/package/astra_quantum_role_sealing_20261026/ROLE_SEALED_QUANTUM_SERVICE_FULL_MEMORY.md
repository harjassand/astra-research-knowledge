# ASTRA — Causal role sealing and two equivalent quantum-memory service interfaces

**26 October 2026 (Australia/Brisbane).** Scientific continuation of the acquired quantum service. This document records derivations and reproducible *finite-dimensional reference executions*, not physical experiments, acquired laboratory primitives, or a claim of priority over existing quantum-information theory.

## Scientific decision

The previous frame-free and completed-teleportation services rely on the causal fact that test and use exercise the *same underlying physical operation*. Hiding a random test/use decision from the apparatus is an architectural requirement, not a consequence of favorable observed tests. The most productive next attack was to replace that assumption with an explicit physical construction wherever possible, and to quantify what a remaining violation costs.

Three results survived:

1. **Input-level causal role sealing.** A fresh uniform private two-bit Pauli key converts *any* incoming user qubit, including one correlated with the apparatus memory, into a maximally mixed ciphertext independent of the whole accessible memory. A uniformly selected six-state sacrificial test presents the identical accessible quantum state. Consequently the physical device cannot distinguish the roles from the quantum input, even with arbitrary coherent memory. The classical role and key must not leak via distinct timing, pulse records, control signals, or later interaction while the device can still act.
2. **Exact interchangeability of two quantum interfaces.** A direct private-Pauli-framed qubit service and an entanglement-first / deferred-use service realize the *same complete positive instrument on the bath*, including each publicly selected test axis, coarse pass/fail outcome and the positive Pauli-labelled use branches. The entanglement-first service prepares a fresh protected Bell pair, sends one half through the same physical channel, and chooses test or completed teleportation only after the physical call. The direct service avoids that quantum buffer but consumes the unknown input when used. The identity is valid on arbitrary correlated states with noncommuting quantum memory and hence composes through allowed adaptive histories.
3. **Operator-effect tolerance of imperfect test hardware.** Even when a test-only physical deviation spoils exact test/use equality, *if* the use channel retains its genuine positive Pauli-fault decomposition and the actual test failure effect obeys a full-memory operator lower bound, one can pay a calibrated mismatch inside a sequential estimation factor. This is weaker and more operationally honest than relabelling an arbitrary small coherent perturbation as a stochastic port fault. Finite correlated-bath simulations demonstrate the considerable throughput penalty.

The Pauli one-time pad, channel–state duality, Pauli twirling, teleportation, sequential estimation factors and non-iid spot-checking are established prior work. The programme-specific result here is their complete-bath interface equivalence, the causal role boundary, the matched coarse test instrument, the mismatch budget and the explicit failure controls. A conventional quantum controller supplied with the same physical ports and information can use every result.

## 1. Physical boundary and exact theorem

Let `D` be an unknown input qubit, `M` **all** future-accessible quantum memory and classical internal registers, and `E` an arbitrary untouched reference. The physical call at one chosen public setting is a complete CPTP instrument with sum channel

\[
\mathcal E: \mathsf L(DM)\rightarrow\mathsf L(BM'),\quad
K_\lambda=\sum_{s\in\{I,X,Y,Z\}}P_s\otimes B_{s\lambda}.
\]

The Pauli expansion is an operator identity, with
\(B_{s\lambda}=\tfrac12\operatorname{Tr}_{B,D}[(P_s\otimes I)K_\lambda]\), where the partial trace is over the identified logical input/output matrix indices, not a physical trace after evolving the channel. A Kraus description represents the entire *complete* physical call, including any recorded internal data included in `M'`. Define

\[
\Phi_s(\sigma)=\sum_\lambda B_{s\lambda}\sigma B_{s\lambda}^\dagger,
\quad W=\sum_{s\ne I}\Phi_s^*(I_M)
=\sum_{s\ne I,\lambda}B_{s\lambda}^\dagger B_{s\lambda}.
\]

\(0\preceq W\preceq I_M\). No size, mixing-rate, reset, Markov, classical-noise or product input state is assumed for `M`. The same physical channel must act during each complete call for either role; past observations may choose its setting. The future role and fresh key cannot reach the physical call as extra unmasked classical controls. The mode has genuine port-identification, isolation and routing requirements, not guaranteed by this algebra.

### Theorem A — direct masked role seal and positive use branches

Prepare either (USE) an arbitrary joint \(\rho_{DME}\) and apply a fresh, uniform private \(P_k\) to `D`, or (TEST) an independent uniform eigenstate of `X`, `Y` or `Z`, again through the same physical Pauli-frame interface. In each role the complete accessible state at the entry of the untrusted call is

\[
\rho^{\rm in}_{DME}=\frac{I_D}{2}\otimes \rho_{ME}.
\tag{1}
\]

This holds even if the unencrypted message was originally entangled with `M E`. (During TEST, the original message remains in the protected client laboratory; the local test carrier is inserted through the same port.) Consequently **every** CPTP map applied only to the entering carrier and accessible apparatus memory before the role is revealed has identical role-conditioned output states. Early private role selection is possible; unlike a merely promised late coin, there is no information about the role in the incoming quantum state.

After the fixed call, correct the Pauli frame at the output and retire the key. Character orthogonality gives the exact full-memory channel

\[
\mathcal E_{\rm direct,USE}(\rho_{DME})
=\sum_s\sum_\lambda (P_s\otimes B_{s\lambda}\otimes I_E)
\rho_{DME}(P_s\otimes B_{s\lambda}\otimes I_E)^\dagger .\tag{2}
\]

Each summand is completely positive. A virtual label `s` is neither an ontological microscopic error nor an observable record. The effect of its aggregate nonidentity branches is `I_D ⊗ W`. Actual use outputs, memory and references are all included in (2). The key must be fresh/independent of *current entire* apparatus state; simply cycling known frame pulses is not sufficient.

### Theorem B — entanglement-first deferred-use interface gives the same instrument

Independently of `M` and of the unknown user message, prepare `|Phi+>_{RC}`, retain `R` locally and pass only `C` through **the same** physical \(\mathcal E\). Before the role is chosen the resource expands formally into orthogonal Bell sectors:

\[
(\mathrm{id}_R\otimes K_\lambda)
(|\Phi^+\rangle_{RC}\otimes|\xi\rangle_M)
=\sum_s |\beta_s\rangle_{RB}\otimes B_{s\lambda}|\xi\rangle_M,
\quad |\beta_s\rangle=(I\otimes P_s)|\Phi^+\rangle.
\tag{3}
\]

If TEST is chosen *after the physical call has finished and the candidate is isolated*, measure an independently, privately selected local Bell stabilizer `XX`, `ZZ` or `-YY`. Record only its parity (and, if useful, the selected setting) and physically retire the individual local measurement outcomes. If USE is chosen, Bell-measure the real input jointly with `R`, correct the receiver `B` and physically retire the individual teleportation Bell outcome. These terminal operations are specified trusted instruments, not something inferred from the earlier source tests.

The completed USE channel on `D M E` is **exactly (2)**, including initial correlations of `D` with `M` and `E`. Each virtual Bell sector has the same map \(\Phi_s\) on the retained memory. The statement does **not** claim that an unrestricted arbitrary channel is simulated by its Choi state using *unmodified* teleportation; the result is the Pauli-*twirled* effective channel of the specified teleportation procedure. This is consistent with established limits on Choi-state teleportation simulation of non-Pauli channels.

Moreover, conditional on a publicly selected test axis `j ∈ {X,Y,Z}`, **both direct and EPR TEST** induce exactly the same *coarse CP instrument* on `M`:

\[
\mathcal F_{j,\mathrm{fail}}=\sum_{s:\,P_sP_j=-P_jP_s}\Phi_s,
\qquad
\mathcal F_{j,\mathrm{pass}}=\sum_{s:\,P_sP_j=P_jP_s}\Phi_s.
\tag{4}
\]

Averaging the three axes yields

\[
\mathcal F_{\mathrm{fail}}=\frac23\sum_{s\ne I}\Phi_s,
\qquad
\mathcal F_{\mathrm{pass}}=\Phi_I+\frac13\sum_{s\ne I}\Phi_s,
\quad F_{\mathrm{fail}}=\frac23W.
\tag{5}
\]

These are equalities of the **entire memory-update CP maps**, not just scalar test probabilities. The complete maps agree coefficientwise on every operator on `M`, and tensor with identity on arbitrary references. Therefore any adaptive quantum comb using their coarse records and completed use outputs can substitute one interface for the other without changing its joint mathematical process, *provided the underlying physical call is the same and all stated auxiliary operations are implemented exactly*. In particular no new bath model or reset is needed. This is operational *interchangeability*, not evidence that real devices provide cost-free or error-free terminal gates.

### Where two classical key bits are necessary

The completely depolarizing qubit channel \(\rho\mapsto I/2\) has normalized Choi state \(I_4/4\), with entropy 2 bits. Any exact random-unitary encryption \(\sum_k p_k\,U_k(\cdot)U_k^\dagger\) representing it is an ensemble of pure Choi states, so \(H(p)\ge S(I_4/4)=2\) bits. Fresh two-bit Pauli frames attain this bound. This is the known private quantum channel result (Ambainis--Mosca--Tapp--de Wolf, 2000), not a new optimality theorem.

It is important **not to conflate** a one-bit frame that cancels a known coherent `I/Z` interference term with perfect role hiding against arbitrary `D:M` correlations. For example, encrypting the `D` half of \(|\Phi^+\rangle_{DM}\) with only `{I,X}` gives a state at trace distance `1/2` from \(I_D/2\otimes I_M/2\). The optimal apparatus guessing probability between TEST and USE with equal priors is therefore `3/4`, even though the marginal state on the carrier alone is exactly `I/2`.

### Imperfect, reused or exposed keys

For a fresh but independently **biased** four-Pauli key distribution `p`, let \(\tau=\tfrac12\sum_k|p_k-1/4|\). The accessible TEST/USE input states have trace distance at most \(\tau\), and the complete physical current-call channel averaged with `p` differs from the uniform-twirl reference by half diamond norm at most \(\tau\). A maximally entangled `D:M` witness attains the first inequality exactly: the bath can distinguish the four Bell-labelled ciphertexts. Bias therefore cannot safely be assessed by looking only at the logical carrier marginal.

**Crucial scope:** nonuniform keys generally reintroduce coherent cross terms. They **do not** leave exact positive fault paths in the actual implemented channel. A globally compositional replacement by the uniform reference costs at most \(\sum_i\tau_i\) in finite-block event probability *if* each bound is uniform over the complete current boundary and conditioned past. An effect-level fault estimator cannot freely replace that accumulated diamond allowance. Similarly a single private key reused across calls is not the required fresh, conditionally independent key: the joint twirl can preserve inter-round coherent interference. Actual execution below gives a two-call discrepancy near 0.0985.

A side channel exposing key bits, a separate role-dependent pulse signal, timing differences or an unisolated output invalidates the equality of accessible TEST and USE quantum inputs as a description of **all** information physically available to the device. Only an explicit complete-boundary isolation/secrecy bound can justify claiming otherwise. The Pauli frame itself is **not** certified by the six-state data.

## 2. A robust operator-effect mismatch theorem

Exact instrument equality is stronger than is needed for a *statistical* fault certificate. Suppose the USE remains exactly decomposable as in (2) with nonidentity effect `W`, but the actual sacrificial test—potentially a different bath-disturbing instrument—has an effect satisfying the **operator inequality**

\[
F_{\mathrm{test}}\succeq fI_M+\nu W-\epsilon I_M, \quad 0<\nu\le1.
\tag{6}
\]

This must hold for every possible current hidden state, not only a fitted calibration state. For the ideal three-basis TEST, `f=0`, `nu=2/3`, `epsilon=0`. `epsilon` may pay a separately calibrated full-boundary role-specific difference. For example, an extra test-only coherent single-qubit rotation `exp(-i phi Z)` after the common call has uniform half-diamond deviation at most `|phi|`; a test event then changes by at most `|phi|` on every hidden/reference input. Its effect obeys (6) with `epsilon=|phi|` even though that coherent rotation is **not** a classical stochastic fault event.

At each round `i`, privately TEST with predictable probability `p_i` and USE otherwise. For fixed `z>1`, choose

\[
a_i=1-\frac{(1-p_i)(z-1)}{p_i\nu}\quad \text{with }0<a_i<1,
\quad
c_i=1-p_i(f_i-\epsilon_i)(1-a_i)>0.
\]

Let `A_i` be the actual failed-test indicator, and let `B_n` be the count of *virtual nonidentity USE Pauli branches* obtained from the positive complete-use refinement. On every current complete state, including any prior refined fault history, the weighted one-step effect is

\[
(1-p_i)[I+(z-1)W_i]+p_i[I-(1-a_i)F_i]\preceq c_iI.
\tag{7}
\]

Thus \(M_n=z^{B_n}\prod_{\mathrm{TEST}}a_i^{A_i}/\prod_{j\le n}c_j\) is a nonnegative supermartingale of initial mean at most 1, without a model of `M`. Ville's inequality supplies one all-prefix confidence event of probability at least `1-delta` with

\[
B_n\le U_n=\frac{\log(1/\delta)+\sum_{i\le n}\log c_i
-\sum_{i:\mathrm{TEST}}A_i\log a_i}{\log z}.
\tag{8}
\]

Because the latent count increases by at most one on a USE and not at all on a TEST, every historical numerical upper bound transports sharply within that information class as

\[
V_0=0,\qquad V_n=\min\{U_n,\ V_{n-1}+\mathbf 1_{\mathrm{USE},n}\}.
\tag{9}
\]

A controller authorizing the next candidate only when `V_n+1 <= Bmax` guarantees on that confidence event that every actually admitted use prefix respects the declared **virtual** fault budget. It does not identify each faulty output, certify the next quantum state, justify unlimited renewal, or automatically turn the fault-count bound into a valid quantum code. If instead the USE's positive decomposition itself fails because of coherent terminal key leakage, equations (7)–(9) cannot be applied to a fictional latent count: only the weaker full-channel approximation or frame-free task-error bound from the earlier programme remains.

**Cost of tolerance.** At zero test false-positive baseline, \(c_i=1+p_i(1-a_i)\epsilon_i\). Over many rounds, \(\sum\log c_i\) becomes a substantial *risk-credit cost*, rather than an arbitrarily small fixed-confidence exception. A nonzero bounded mismatch can make a safe controller stop much earlier, even if actual physical faults are infrequent. It is therefore worth physically sealing the role or delaying its choice instead of trying to fix poor causal separation by collecting more data.

## 3. Executed reference calculations

All scripts use NumPy and SciPy, supply their actual JSON output files and contain assertions. The bath is deliberately represented in the **validation** simulator; the simulated observer never receives its state or the virtual fault labels.

| Executed independent check | Quantitative outcome | Script |
|---|---|---|
| Complete Pauli-twirl channel versus positive hidden-memory Pauli paths | Largest sampled full-boundary half-trace residual `7.74e-17` | `causal_role_sealing_exact.py` |
| Direct three-basis TEST effect versus `(2/3)W` | Operator residual `1.12e-16` | same |
| Two-bit role hiding vs one-bit role hiding (Bell-correlated input/bath) | `~0` vs `0.5` trace distance; one-bit guess success `0.75` | same |
| Biased 2-bit role hiding | Trace distance `0.20`, exactly equal to the chosen key's TV from uniform | same |
| Reusing the same key on two coherent calls | Complete two-use output discrepancy `0.09854496` | same |
| Full TEST *bath CP instrument* by public X/Y/Z test setting: direct frame vs EPR late choice | Maximum all-operator matrix-unit residual `3.15e-16` | `ebit_vs_encrypted_instrument.py` |
| EPR Bell-sector projections vs positive Pauli bath subinstruments | Residual `4.47e-16` | same |
| **Entire USE quantum channel** on unknown input + retained bath + untouched reference: EPR teleport vs direct Pauli twirl | Maximum all-matrix-unit Frobenius residual `7.81e-16` | `ebit_complete_teleport_reference.py` |
| Retaining local test outcomes when parity alone would suffice | Full flagged-bath half-trace discrepancy `0.5`; parity-only discrepancy `3.14e-16` | `fine_record_and_last_gate_no_go.py` |
| Last untrusted terminal X after upstream perfect Bell test | Can make a delivered `|0>` exactly orthogonal to intended output | same |

The nonunitary equivalence test uses **two different noncommuting full system–bath unitary Kraus branches**. The complete USE test uses five physical register positions and two Kraus branches, and verifies a 64-element basis for the `D:M:E` operator space, not merely random Bell-state fidelity.

### Active adaptive service

`online_causal_sealed_memory.py` executed two ensembles of 90 independent 680-round-cap references, with a two-level noncommuting bath reused without reset. Physical setting and private audit probability adapt to **received** test and query records, not to hidden validation fault labels, bath state or Pauli coefficients. Both ensembles use `delta=.01` for a simultaneous all-prefix certificate and a predeclared risk admission budget of 100.

| | Matched protected role | Extra 0.07-radian TEST-only coherent output rotation, calibrated `epsilon<=0.07` |
|---|---:|---:|
| Mean admitted physical rounds | 572.56 | 312.52 |
| Mean completed quantum uses | 394.68 | 213.81 |
| Mean latent virtual USE faults (not observer-visible) | 42.38 | 22.93 |
| Mean final received transported fault bound | 96.28 | 99.35 |
| Observed violations of the **correct** upper bound in 90 trajectories | 0 | 0 |
| Stopped before 680-round cap | 67 | 90 |

The smaller throughput in the mismatched ensemble is primarily the conservative **uniform operator allowance**, not evidence the physical bath suddenly became more faulty. No empirical success frequency from 90 references is represented as a new statistical theorem; (7)–(9) supply the formal coverage under their premises.

## 4. Decisive obstructions and physical tradeoffs

**The fine-record obstruction is real.** Let the Bell-pair candidate and bath be in the pure coherent state \((|\Phi^+\rangle_{RB}|0\rangle_M+|\Phi^-\rangle_{RB}|1\rangle_M)/\sqrt2\). A coarse `ZZ` parity test always passes and, with the local outcomes physically discarded, leaves the expected bath mixture. Keeping the separate `00` versus `11` local outcomes instead steers the bath into `|+>` versus `|->`. The resulting *flagged* bath state differs from the Bell-pinched positive-path comparator by half trace distance exactly `1/2`. A test's aggregate effect can be valid while its **fine** future-accessible record defeats a complete multi-round identity.

**A final untested operation remains unbounded.** A trusted perfect Bell-pair test cannot constrain a subsequently unverified logical `X` on the delivered qubit. The actual output can be orthogonal to the intended state despite every upstream test passing. A sequence of new untrusted wrappers does not remove the requirement for an actual trusted or independently bounded terminal quantum interface.

**The two architectures trade hardware capabilities, not theories.** Direct encryption needs a private, fresh two-bit key and reliable input/output Pauli framing of the *whole physical call*. It can send an unknown input immediately but cannot undo damage to that input. Entanglement-first late choice needs one locally prepared and protected Bell pair, output extraction/isolation, reliable destructive parity tests, a Bell-measurement-and-correction terminal interface, and protected unknown-input holding until that late decision. It does not require a secret key during the physical channel call, and avoids sending the actual unknown input before acceptance. Both require genuinely matched physical coupling and a means of retiring fine readout records. They cannot be compared merely by counting abstract gates without considering protected storage, duration, fault rates and routed ports.

**Mathematical memory equivalence is not experimental identity.** Actual two hardware realizations may expose the bath differently or have different durations, helper errors and leakage. Such differences require *complete-boundary* physical justifications and correctly oriented operator bounds. A favorable likelihood observed in a limited calibration period does not establish uniform future behavior against an unrestricted hidden autonomous clock.

## 5. Next highest-leverage physical attack

The mathematical choice is clearer than before. If trustworthy Pauli framing is cheap, input encryption seals test/use indistinguishability without requiring role selection after the expensive operation. If frames are problematic but a protected local Bell qubit and terminal teleportation are available, late-choice EPR certification realizes exactly the same fault instrument. The practical research objective is now to **construct and calibrate at least one complete boundary**, especially its independent input/source preparation, output isolation, record retirement and post-call correction. Native exchange-preserving dynamical decoupling results from Astra N1004 provide conditional full-boundary norm estimates for specified bounded unwanted interaction classes, but do not automatically suppress unknown bath-modulated exchange terms in the control commutant or certify arbitrary pulsed measurement electronics.

A legitimate next experiment must measure both physical branches and bound their *full quantum instruments*, including the remaining bath boundary where possible. Without that, an attractive exact algebraic certificate remains a conditional quantum-service design rather than an acquired hardware capability.

## Governing sources and relevant established science

User-supplied originals were read: `LIBRARY_RENDERED_ACQUIRED_TASK_INTEGRITY_WITH_QUANTUM_MEMORY(1).txt`; `LIBRARY_RENDERED_COMPOSED_POSITIVE_SERVICE_FAULTS(1).txt`. Most recent saved local governing return: `astra_quantum_causal_leakage_20261026/TASK_ALIGNED_FRAME_PRIVACY_AND_FRAME_FREE_INTEGRITY.md`. Astra task-first instructions and packet `N1004` were fetched at public Git revision `56d4aebfb8a43cd1a31fdf0f4e14da765ed6f950`. Archived research instructions were treated as source material, not as fresh commands.

- Ambainis, Mosca, Tapp, de Wolf, *Private Quantum Channels* (2000), DOI `10.1109/SFCS.2000.892142` / https://homepages.cwi.nl/~rdewolf/publ/qc/AMTW00.pdf — classical random-key cost and exact Pauli quantum one-time pad.
- Cope, Hetzel, Banchi, Pirandola, *Simulation of non-Pauli channels*, Physical Review A **96**, 022323 (2017), DOI `10.1103/PhysRevA.96.022323` — cautions against treating general Choi-state teleportation as direct exact simulation of the original channel.
- *Constructing Smaller Pauli Twirling Sets for Arbitrary Error Channels*, Scientific Reports (2019), DOI `10.1038/s41598-019-46722-7` — prior art for restricted Pauli-twirl groups; small twirls per se are not new.
- Kattemölle, Gulácsi, Burkard, *Non-Markovianity induced by Pauli twirling*, npj Quantum Information (2026), DOI `10.1038/s41534-026-01345-5` — an important caution that Pauli-form outputs do not justify a Markovian microscopic bath.
- Zhang, Seshadri, Knill, sequential spot-checking / estimation factors (2026), https://arxiv.org/html/2602.08114 — general underlying sequential-inference machinery.

## Reproducibility

Run `bash RUN_VALIDATIONS.sh` here. Its five programs emit actual `*_results.json` files and assertion checks. NumPy and SciPy are required. `validation_console.txt` is the saved combined rerun. No code was pushed to GitHub and no physical device was operated.
