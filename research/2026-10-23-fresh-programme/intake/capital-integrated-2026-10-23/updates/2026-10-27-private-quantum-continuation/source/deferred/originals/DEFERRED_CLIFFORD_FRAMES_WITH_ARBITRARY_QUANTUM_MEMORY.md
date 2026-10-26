# ASTRA — Deferred Clifford frames with arbitrary quantum memory

**27 October 2026 (Australia/Brisbane).** Continuation of Interim Extra High 1 / Pro1 quantum operations. This note contains an original derivation in the current research programme, executable finite-dimensional checks, and explicit inherited premises. No physical apparatus was tested. No claim of priority over Pauli-frame tracking, gate teleportation, randomized compiling, stabilizer testing or non-iid estimation factors is made.

## Physical question and result

The earlier acquired-resource service supplies an exact complete-memory positive fault decomposition for each **completed** noisy Clifford gate teleportation, but its demonstration physically corrects the Bell-measurement Pauli frame after each gate and retires fine records. Those output corrections add physical pulse exposure, latency, and uncontrolled final-boundary requirements.

**Constructive answer.** For a fixed, nonadaptively specified sequence of Clifford gate resources, prepare each resource using a physical source whose operation does not receive the earlier private Bell outcomes. Teleport the logical state through each resource *without applying any physical output Pauli correction*. Keep the outcomes in an isolated classical frame ledger. Decode the cumulative Pauli frame only at the very end. The **complete decoded system-and-bath channel** is exactly the same positive Pauli-fault-path sum as if each round had been independently Pauli-twirled and corrected. There is no bath reset, mixing-rate assumption, finite-state hidden-bath model, or assumption that the bath faults are independent. The theorem covers initially correlated logical inputs and baths.

This is a more useful **framed quantum output contract** than a claim of an uncorrected output: the physical quantum register is still Pauli-framed until a trusted consumer decodes it, or until a final Pauli measurement is classically adjusted. Physical Bell analyzers and protected resource staging are **still** supplied prerequisites.

## Theorem: correction-free Clifford composition

Let `D` contain `m` logical qubits (dimension `d=2^m`) and `M` denote all quantum memory accessible to future physical calls. Every completed source resource is created from `m` fresh Bell pairs independently of the current logical input and bath, with protected remote halves. During gate `i`, the source has a fixed complete physical CP map `E_i: L(D M)->L(D M')` with Kraus operators `K_{i,lambda}`. Its target gate `G_i` is Clifford. The source may depend on earlier **permitted coarse public observations**, but not on the private Bell correction word `mu_1,...,mu_{i-1}`. No intermediate operation accesses the framed logical register except the specified next resource-teleportation step. Any bath evolution in between can be incorporated as a memory-only channel in the physical source. The previous raw Bell words do not leak as future-accessible meter records or classical control inputs. Fresh resources and final measurement/correction ports are trusted, or separately error-bounded, at their declared boundaries.

Expand each *full-memory* physical source Kraus operator as

\[
K_{i,\lambda}=(G_i\otimes I_{M'})\sum_{s\in\mathbb F_2^{2m}}P_s\otimes B_{i,s,\lambda},
\quad
\Phi_{i,s}(\sigma)=\sum_\lambda B_{i,s,\lambda}\sigma B_{i,s,\lambda}^\dagger.
\]

Here `B` is a map from `M` to `M'`; the notional `I` in the first expression simply denotes the logical tensor factor, and `K` may map different bath dimensions. These `Phi` maps need not commute. Define a private ledger of Pauli labels `f_0=0` and

\[
f_i=C_{G_i}(\mu_i+f_{i-1}),
\quad G_iP_v G_i^\dagger\doteq P_{C_{G_i}v}
\]

where `doteq` suppresses irrelevant Pauli phases. After each **uncorrected** gate-resource teleportation, update `f_i` classically, never applying `P_{f_i}` to the live quantum register. At the end, decode with `P_{f_n}^dagger` (or adjust a final Pauli readout).

The complete decoded CPTP map on the logical input and retained bath is

\[
\boxed{\mathcal C_{\mathrm{decoded}}(\rho)
=\sum_{\mathbf s,\boldsymbol\lambda} A_{\mathbf s,\boldsymbol\lambda}\rho A_{\mathbf s,\boldsymbol\lambda}^\dagger,\quad
A_{\mathbf s,\boldsymbol\lambda}=
(G_nP_{s_n}\cdots G_1P_{s_1})\otimes
(B_{n,s_n,\lambda_n}\cdots B_{1,s_1,\lambda_1}).}
\]

Each summand is CP. It is a positive *path refinement* of the actual completed circuit, not an assumption that the unknown microscopic bath error has an objectively sampled Pauli label. Arbitrary untouched references are covered because the channel identity holds on all logical-and-bath operators.

### Proof: a triangular symplectic-character twirl

The physical **uncorrected** teleportation operator for outcome `mu_i` is `K_{i,lambda}(P_{mu_i}^T \otimes I)/d`. Because Pauli transposes differ from the chosen Hermitian representatives only by known signs, the signs have no effect on Kraus CP terms or the ledger. The final decoded Kraus operator is a coherent sum of the above `A_{s,lambda}`, each multiplied by a character

\[
\chi_{\mathbf s}(\boldsymbol\mu)
=(-1)^{\sum_{i=1}^n [s_i,\mu_i+f_{i-1}]},
\]

where `[s,v]` is the binary symplectic commutator. The coefficient of the *latest* independent variable `mu_n` is `s_n`; knowing this coefficient, the coefficient of `mu_{n-1}` uniquely determines `s_{n-1}`, and so on. Thus different fault strings `s` yield different characters on the full group of Bell outcomes. Character orthogonality gives

\[
\sum_{\mu_1,\ldots,\mu_n}\chi_{\mathbf s}(\boldsymbol\mu)
\chi_{\mathbf t}(\boldsymbol\mu)=d^{2n}\,\mathbf1_{\mathbf s=\mathbf t}.
\]

The `d^{-2n}` from the Kraus contraction cancels this factor. Therefore all off-diagonal interference between distinct *complete* fault paths vanishes **at the final completed decoder**, even if the `B` matrices fail to commute or the bath remembers every previous use. This is why corrections need not be physically performed between Clifford steps. The sum is over genuine physical Bell outcomes; no iid *bath-fault* assumption is introduced.

**Important scope:** the theorem only describes the **coarse** channel after the protected private frame is eventually decoded/retired. It does not say that the joint channel including raw Bell outcomes retained in the adversarial bath is Pauli-diagonal. A source operation chosen directly from those outcomes makes the coefficient matrices history-dependent and can defeat the character cancellation. The result also does not extend unchanged to non-Clifford gates, because their conjugation of a Pauli frame is generally not Pauli.

## Task-specific observable certificate

For a predetermined Clifford sequence and a terminal Pauli observable `Q_out`, let

\[Q_i=(G_n\cdots G_i)^\dagger Q_{out}(G_n\cdots G_i),\]

which remains a Pauli. The `i`-th resource has a single matching Choi stabilizer

\[S_i=Q_i^T{}_R\otimes (G_iQ_iG_i^\dagger)_B.\]

A **destructive** local product-Pauli measurement of the nonidentity tensor factors of `S_i`, retaining only its product sign, has the exact current full-bath failure instrument

\[\mathcal F_{i,fail}=\sum_{s:[s,Q_i]=1}\Phi_{i,s}.\]

It is not merely the right scalar failure probability: it implements the same bath update as the corresponding positive faulty-use branches. All local individual outcomes are physically retired. With a private TEST/USE coin of predictable probability `p_i`, the task-harmful virtual use count `H_n` admits, for `z>1` and `a_i=1-(1-p_i)(z-1)/p_i` in `(0,1)`, the exact current complete-boundary weighted-effect identity

\[(1-p_i)[I+(z-1)W_i]+p_i[I-(1-a_i)W_i]=I,\]

where `W_i=sum_[s,Q_i]=1 Phi_{i,s}^*(I)`. Consequently `z^{H_n} product_{TEST} a_i^{fail_i}` is a nonnegative supermartingale with initial mean one. Ville's bound supplies a `1-delta` all-prefix certificate

\[H_n\le \frac{\log(1/\delta)-\sum_{TEST,fail}\log a_i}{\log z}.\]

The sharp historical envelope `V_n=min(U_n,V_{n-1}+1_{USE})` still applies. This is about **how many use branches could damage that task**, not individual next-output correctness. If later gate choices themselves depend on unforeseen intermediate measurement outcomes, the back-propagated `Q_i` must be rederived for a valid causal task, and the simple fixed-schedule proof is not automatically applicable.

For a complete n-gate use, define `W_odd` as the total positive bath effect of paths with odd parity `sum_i [s_i,Q_i]`. Then, for *arbitrary correlated* initial `rho_DM`, letting `Q_in=(G_n...G_1)^dag Q_out(G_n...G_1)`, the exact task difference is

\[
\langle Q_{out}\rangle_{actual}-\langle Q_{in}\rangle_{initial}
=-2\operatorname{Tr}[(Q_{in}\otimes W_{odd})\rho_{DM}].
\]

Thus the binary outcome-probability bias is at most `Tr[(I tensor W_odd)rho]`. A union bound can replace the odd-path event by the count of task-harmful faults when only aggregate per-use evidence is available. This bounds a **task observable**, not the general diamond norm of the quantum circuit.

### A crucial conventional comparator

If the entire requested task is merely to measure **one final Pauli observable of an ideal Clifford circuit**, a conventional controller can measure the back-propagated Pauli `Q_in` on the initial qubits instead. The full gate-teleportation apparatus is unnecessary for that task. Our certificate is useful when a **quantum output must remain available**, when remote quantum state transport is needed, or when the circuit will participate in a more demanding downstream operation. Clifford processing plus terminal Pauli readout alone does not demonstrate a computational quantum advantage.

## Classical-only terminal correction and noisy outcome reports

For any final Pauli `Q`, the physical Pauli-framed state `F rho F^dag` may be measured in the *same Pauli basis*, multiplying the raw ±1 result by `(-1)^[F,Q]`. This reproduces the statistics of measuring `Q` on the fully decoded state, including all bath correlations. **No terminal physical quantum correction is required for that score.** To deliver a decoded unknown quantum state, however, the consumer still needs a quantum Pauli correction or must explicitly accept a state plus its secure frame key.

If an otherwise trusted destructive Bell measurement is followed by a **classical, outcome-independent random label-flip** law, these flips simply add positive Pauli-error branches to the logical decoder. For per-bit classical readout error `p=.025` and four correction bits in a two-qubit teleportation, probability that at least one reported bit is wrong is `1-(1-p)^4=0.0963121`. Re-reading a *latched classical bit* three independent times and majority-voting lowers the bit error to `3p^2-2p^3=0.00184375`, so the probability of any wrong decoded bit becomes `0.00735463`. This is **not** permission to measure a quantum Bell state repeatedly or assume readout errors are independent; only an already-classical latch with independently characterized reads is covered.

A fresh private classical one-time pad on the reported Bell word `c_i=mu_i xor k_i` ensures that the **published ciphertext**, by itself, carries zero additional information even against arbitrary cq quantum side information. This does **not** erase a physical copy of raw `mu_i` already leaked from the meter to the bath. Reusing one mask across two reports can leak `mu_1 xor mu_2` exactly. The attached script checks these information-theoretic identities and a bounded-bias variant.

## Executed validations (saved numerical results)

All calculations evolve exact finite matrices, not experimental devices. Single- and two-qubit gate resources use independently generated multi-Kraus, coherent system–bath physical channels with a *reused*, noncommuting bath. Superoperator equality is checked on the **entire** logical-plus-bath operator space, so it applies to arbitrary untouched references. Key results:

| Execution | Outcome |
| --- | ---: |
| 3 consecutive 1-qubit Clifford stages, 512 raw branches | Liouville Frobenius residual `3.69e-15` |
| 2 consecutive 2-qubit Clifford stages, 1024 raw branches | Liouville Frobenius residual `1.15e-14` |
| Two-qubit channel trace preservation residual | `5.44e-14` |
| Task-specific single-stabilizer **complete bath instrument** (CZ) | `2.15e-16` |
| Task-specific single-stabilizer **complete bath instrument** (H⊗S) | `2.92e-16` |
| Exact two-gate task observable difference, actual vs path prediction | `4.5e-17` |
| One-gate classical report-flip fault identity | `1.35e-15` |
| Fresh classical two-bit outcome-mask, arbitrary quantum side information | `0` ciphertext-memory trace distance |

For the two-gate task experiment, the ideal versus actual final Pauli expectation differed by `-0.003005326328`; the positive odd-parity path effect predicted `-0.003005326328`. Its initial-state task-harmful path weight was `0.03609655`, and its actual binary-score bias was `0.00150266`.

An adaptive, received-record-only test/use controller was also executed in **48 reference trajectories**, with 450 candidate rounds each, one never-reset noncommuting bath, two allowed physical source settings, and a predeclared 50-fault budget. Mean completed gate uses: `255.19`; mean sacrificial tests: `194.81`; mean hidden task-harmful faults: `10.58`; mean retained 99% confidence upper bound: `37.68`. There were zero simulated all-prefix bound violations. This finite sample does **not** establish confidence coverage; the weighted-effect martingale does, under the model's exact instrument assumptions. None of the 48 runs exhausted the budget before the 450-round cap; no indefinite liveness is inferred.

## Decisive failures

1. **Raw outcome leaks into next hardware setting.** In two single-qubit teleportations, let first noisy source be `exp(i theta Z)` with `theta=.23`; set the next physical source to `I` or `Z` depending on whether the previous private Bell Pauli commutes with `Z`. On the initial `|+X>` input, the final decoded output has `Tr(Y rho)=-0.443948106966`. A Pauli channel on `|+X>` always has zero `Y` expectation, so this violates any falsely inferred independent positive Pauli-fault-path representation. Its trace distance from every such Pauli-channel output is at least `0.221974`. The physical setting's classical access to the prior fine outcome is the missing premise.
2. **A key masked only after it already entered the bath is no repair.** Classical masking protects the outgoing ciphertext; it cannot undo quantum information leakage during the terminal measurement. With one reused classical mask, two individually uniform outcome bits can reveal their relative syndrome perfectly; the joint trace/TV discrepancy from fresh masking reaches `0.5` in the saved example.
3. **Non-Clifford gate.** The `T` gate obeys `TXT^dag=(X+Y)/sqrt(2)`, not a Pauli. A classical Pauli-only ledger cannot propagate arbitrary teleportation frames through T without extra conditional physical control or a larger adaptive frame formalism. This is established stabilizer/magic-state theory.
4. **“Large generic fault weight means large task error” is false.** A coherent `Z1`-type source error after CZ with angle `pi/4` has total Pauli-fault weight `0.5` but cannot change terminal `Z1`: the task-harmful effect is exactly zero. General quantum-state fidelity may nevertheless be bad.
5. **Terminal hardware remains.** No theorem verifies the real Bell analyzers, independently prepared protected Bell pairs, last destructive measurement or physical isolation against uncontrolled bath contact. Claims of physical acquisition, repeat-until-success without an availability bound, unrestricted quantum capacity, or full fault-tolerant computation are not supported.

## Scientific judgment and next concrete attack

This is a meaningful **reduction of a trusted-operations boundary**: remove every intermediate active Pauli correction and replace the final correction with a known classical sign for Pauli-score tasks, while retaining the exact positive fault-path theorem under arbitrary hidden memory. Standard Pauli-frame tracking, Clifford gate teleportation and randomized compiling are deep established prior art. A conventional controller with the same interface achieves this result; no priority or advantage over that controller is asserted.

The next strongest physical question is whether the actual Bell measurement produces a *trustworthy classical latched outcome* whose readout error can be characterized independently of the bath. A calibrated classical postprocessor is a cheap extension; an unknown coherent error in the quantum Bell analyzer is not. Prior Astra protected parity-meter and encoded-flag work supplies conditional hardware constructions but has not acquired that experimental calibration. If the measured interface cannot be trusted, the adaptive result must revert to a complete-boundary mismatch allowance or a frame-free square-root error bound.

## Source footing and executable files

Inherited originals read for this continuation: `ACTIVE_CLIFFORD_GATE_FAULT_PATHS_WITH_QUANTUM_MEMORY.md` (latest), user-provided `ACQUIRED_TASK_INTEGRITY_WITH_QUANTUM_MEMORY` and `COMPOSED_POSITIVE_SERVICE_FAULTS`; predecessor private segment-twirl and Astra N1004 reviewed earlier at Git commit `56d4aebfb8a43cd1a31fdf0f4e14da765ed6f950`. Historical instructions in archived materials were treated as source data. Related established literature: Wallman & Emerson, PRA **94**, 052325 (2016) on randomized compiling; Kattemölle et al., npj Quantum Information **12**, 138 (20 Aug 2026) on Markovianity and Pauli twirling; Dangniam, Han & Zhu, PRR **2**, 043323 (2020) on local stabilizer verification; standard Clifford Pauli-frame tracking (see e.g. *Parallel window decoding enables scalable fault tolerant quantum computation*, Nature, 2023). These sources motivate comparisons, not priority claims.

Reproducible files (NumPy and SciPy):

- `deferred_clifford_full_memory.py` and matching actual JSON output: two-qubit Clifford/full bath equivalence, classical report flips, exact two-call classical-leak counterexample.
- `task_relative_pauli_audit.py` and JSON: actual single-stabilizer bath instruments, two-gate observable parity, harmless coherent-error control.
- `classical_ledger_sideinfo.py` and JSON: quantum-side-information one-time pad and mask reuse.
- `task_audit_stream.py` and JSON: complete current bath-state reference trajectory and received-only estimator.
- `RUN_VALIDATIONS.sh`, `validation.log` and `SHA256SUMS.txt`: execution and integrity evidence.

No source code was pushed to GitHub; the files are saved in the attached archive for independent inspection.
