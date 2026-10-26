# ASTRA / Interim Extra High 1 — Coherent delayed-measurement frames for quantum-memory services

27 October 2026. Independent mathematical continuation of `WHOLE_RUN_QUANTUM_PRIVATE_KEY_TAPE.md`, `DECOHERENCE_FREE_COHERENT_CHECK_FLAG.md`, and `T_MAGIC_INJECTION_WITH_UNREPRESENTED_QUANTUM_MEMORY.md`. **Proofs below are conditional on physical instrument assumptions. Python checks are simulations, not experiments. No scientific-priority claim.**

## Scientific decision

The preceding whole-run key-tape argument amortizes the privacy error of classically controlled Pauli frames but still assumes a cryptographically private classical tape and faithful gate control. A distinct interface **purifies the random Pauli choice into quantum flags, leaves the flags unmeasured during the unknown operation, and converts them to classical corrections only after that operation**. This is a specific implementation of deferred measurement and channel twirling; its potential value is substituting isolated short-lived quantum flags for a classical secret key-tape extractor. It does **not** remove trusted quantum control, nor prove that coherent flags outperform a good conventional random-number generator.

Two physically decisive observations:

1. **Information acquired by the bath from the data is not itself a violation of Pauli twirling.** The uncontrolled device can perform an arbitrary fixed quantum channel on the data and all its memory, including an adaptive measurement on the data which indirectly reveals the frame. Positivity still follows. What is prohibited is additional *direct* access to the flag register, to a flag-dependent control waveform, or to an unretired measurement label outside that common data–memory channel.
2. **Correctness of today's logical output is strictly weaker than future composability.** In a worked example, copying a flag into the bath *after* the noisy interaction leaves the current output state exactly unchanged but changes the joint output–bath state by trace distance `0.5`. Every theorem below is on the complete bath boundary, not just the delivered qubit.

## 1. Exact complete-memory delayed-frame theorem

Let `D` denote a qubit, `M` *every future-accessible quantum and classical memory subsystem* (possibly correlated with `D` and with untouched outside references `E`), and let the completed physical call be a fixed CPTP channel

\[
\mathcal E: \mathsf L(D\otimes M)\to\mathsf L(D\otimes M'),
\qquad K_\lambda=\sum_{s\in\{I,X,Y,Z\}}P_s\otimes B_{s\lambda}.
\]

The output `M'` explicitly includes any retained internal reports. The coefficients `B_{s\lambda}` are the unique Pauli matrix coefficients in the identified `D` input/output indices. Let `F=F_xF_z` be **new** controller qubits initialized in the uncorrelated pure state `|++>_F` after every previous use. The controller applies the quantum-controlled input frame

\[
C_{FD}=\sum_{k=0}^{3}|k\rangle\langle k|_F\otimes P_k
\]

(up to physically irrelevant branch phases). During the *entire* untrusted call `E`, the flag must have no physical interaction with the apparatus, and the implemented `E` must be the same fixed map regardless of the flag value. At its completion, the controller measures `F` in the computational basis, implements the corresponding *trusted* output Pauli correction, and prevents the fine key record from becoming another input to the future untrusted memory dynamics.

Conditioned on the measured key `k`, the complete output and memory map is

\[
\mathcal C_k(\rho_{DME})
=\tfrac14(\operatorname{Ad}_{P_k}\otimes\operatorname{id}_{M'E})\circ
(\mathcal E\otimes\operatorname{id}_{E})\circ
(\operatorname{Ad}_{P_k}\otimes\operatorname{id}_{ME})(\rho_{DME}). \tag{1}
\]

**Derivation.** The preinteraction joint state is `C (|++><++| ⊗ rho) C†`. All its flag-diagonal blocks are `(P_k⊗I) rho (P_k⊗I)/4`. The common physical call acts on each block without coupling to `F`, so measuring `F` afterward selects precisely the same map as (1). This does not assume that the flag remains unentangled from the data during the call. It holds on all operator-valued bath/reference blocks. Taking the sum and using Pauli-character orthogonality yields

\[
\boxed{\sum_k\mathcal C_k(\rho_{DME})
=\sum_{s,\lambda}(P_s\otimes B_{s\lambda}\otimes I_E)
\rho_{DME}
(P_s\otimes B_{s\lambda}\otimes I_E)^\dagger .}\tag{2}
\]

Every term is CP and positive. This equality **retains the entire memory `M'`**. The mathematical `s` labels are never acquired physical labels; their sum is the actual coarse operation. The good effect is

\[
F_I=\sum_\lambda B_{I\lambda}^\dagger B_{I\lambda},\qquad
W_{\rm bad}=I_M-F_I=\sum_{s\ne I,\lambda} B_{s\lambda}^\dagger B_{s\lambda}.\tag{3}
\]

No bath-dimension, stationarity, mixing-time or fault-independence condition is needed. An arbitrary future CP instrument can be composed **only after** the key has genuinely been excluded from its physical boundary; then distributivity composes the positive fault paths through noncommuting memory, adaptive feedback, endpoint reuse and correlated inputs.

### Causal role-opacity theorem

Before `E` sees its quantum input, tracing out inaccessible `F` gives

\[
\operatorname{Tr}_F[C(|++\rangle\langle++|\otimes\rho_{DME})C^\dagger]
=\tfrac12 I_D\otimes\rho_{ME}.\tag{4}
\]

Thus an unknown input correlated with the bath and a test input drawn uniformly from the six signed Pauli eigenstates give identical **apparatus-accessible** input states, provided their `M` marginals are equal and their role, timing, unencrypted references and controller signals are not separately available to the device. It is an exact input indistinguishability statement, not a claim that a bath can never learn a posterior about a frame from the data it processes.

### Matching destructive test instrument

A test draws an axis `j` uniformly from `X,Y,Z`, a signed eigenstate of `P_j` uniformly, and checks the sign at output *after* the trusted correction. The complete bath-update CP map of the failed test is

\[
\mathcal F_{\rm fail}=\tfrac23\sum_{s\ne I}\Phi_s,
\quad\Phi_s(\sigma)=\sum_\lambda B_{s\lambda}\sigma B_{s\lambda}^\dagger.\tag{5}
\]

This is equality of instruments on every bath operator, not just equality of numerical probabilities. With an independently calibrated **postmeasurement classical report flip** `t`, the effect is

\[
F_{\rm fail}=t I_M+\tfrac23(1-2t)W_{\rm bad}. \tag{6}
\]

An arbitrary coherent readout defect cannot be introduced into (6) merely because its output probabilities resemble a report flip.

## 2. Online finite-risk control

At each current physical boundary, all prior known records choose the physical setting and a private test probability `p_i`. Generate **fresh** isolated flags and run exactly the same complete physical call on either role. In the virtual positive refinement, let `B_n` count faulty completed uses and `A_i` denote a physically observed test failure. Let `f=t` and `nu=2(1-2t)/3` for (6). Fix `z>1`; choose

\[
a_i=1-\frac{(1-p_i)(z-1)}{p_i\nu}\in(0,1),
\qquad c_i=1-p_i f(1-a_i)>0.
\]

The *conditional operator identity* is

\[
(1-p_i)[I+(z-1)W_i]+p_i[I-(1-a_i)F_{\rm fail,i}]=c_i I.
\]

Consequently

\[
M_n=\frac{z^{B_n}\prod_{i:\operatorname{TEST}}a_i^{A_i}}{\prod_{j\le n}c_j}
\]

is a nonnegative martingale in the positive-path refinement, including an arbitrarily coherent hidden memory. Ville's inequality gives all-prefix coverage `1-delta` for

\[
B_n\le U_n=\frac{\log(1/\delta)+\sum_j\log c_j-
  \sum_{i:\operatorname{TEST}} A_i\log a_i}{\log z}.
\]

The old retained bound `V_n=min{U_n,V_(n-1)+1_USE}` still applies. Authorizing another physical candidate only when `V_n+1<=budget` bounds every *actually served prefix* on the confidence event; it does not certify the next individual input or infinite throughput. Fresh test/use coins, complete test effects, correct full-memory physical frames and an explicit finite risk/confidence budget remain assumptions.

**Executed reference:** 64 distinct 1,300-round-cap trajectories, two adaptive physical settings, a never-reset noncommuting two-level bath, 2.5% calibrated report flips, `delta=.01`, fault budget 90. Mean completed uses **579.453125**, mean sacrificial tests **464.21875**, mean latent virtual faults **31.96875**, mean retained numerical bound **86.76985**; **0/64 observed all-prefix violations**. Observing zero violations does not prove coverage. The observer in the simulation receives only role/test records and actions; the simulator samples virtual labels solely for validation. The actual quantum-flag implementation was separately checked against that exact positive instrument.

## 3. Non-Clifford gate via late-key **pre-gate** Pauli faults

Let a specified desired one-qubit operation be `G`, and the completed noisy physical operation be `N=E ∘ Ad_G`, with `E` any fixed coherent-memory CPTP map. Use quantum-controlled **input Pauli frames `P_k`** and, **after** `N` and measuring the flag, the matched output corrections

\[
Q_k=G P_k G^\dagger.\tag{7}
\]

Then `Q_k G P_k=G` (ignoring inconsequential Pauli phases) and the dressed channel twirls `E` by the *rotated Pauli basis* `Q_k`. Expand `K_lambda` for `E` as `sum_s Q_s ⊗ B_{s lambda}`. The resulting positive complete-channel decomposition is

\[
\boxed{\mathcal S_G(\rho)
=\sum_{s,\lambda}(G P_s\otimes B_{s\lambda})\rho
  (G P_s\otimes B_{s\lambda})^\dagger .}\tag{8}
\]

**Placement matters:** the errors are Pauli **before `G`**; for non-Clifford `G` they should not silently be treated as output Paulis. The matching sacrificial test prepares `P_j` eigenstates and measures output eigenstates of `G P_j G†`; the complete bath failed-test instrument is again (5).

For `G=T=diag(1,exp(i*pi/4))`, **every `T P_k T†` is a single-qubit Clifford**, allowing outcome-selected postcorrection with Clifford hardware. The coherent *pre*-frames are only quantum-controlled input Paulis (CNOT and controlled-Z under a standard qubit encoding). No quantum-controlled `T` or controlled-Clifford gate is required **during the noisy core**. The output Clifford must still be independently bounded as a real operation. The flag must remain inaccessible through that correction and final retirement.

**Executed check:** all 64 basis matrices of `D⊗M⊗E`, two noncommuting retained-memory noise branches, four classical key records and three rotated output test bases: maximum complete-path residual `1.11e-16`, complete three-basis bath-instrument residual `1.11e-16`; two noisy `T` calls sharing the same bath agree with their positive paths to `1.20e-16` trace distance.

This is a conditional method of **instrumenting** a non-Clifford call. It does not create a `T` gate, magic resource, universal fault-tolerance threshold or hardware capacity.

## 4. Physical noise tolerance for the flag: a decoherence-free realization

A bare qubit-key controller needs two transient flag qubits, one quantum-controlled `X`, one quantum-controlled `Z`, flag computational-basis readout and subsequent classical output correction. Instead encode each key bit in **two spins**:

\[
|0_L\rangle=|01\rangle,\qquad |1_L\rangle=|10\rangle,
\qquad |+_L\rangle=(|01\rangle+|10\rangle)/\sqrt2.
\]

The two encoded bits occupy **four** physical flag qubits. Each first physical flag spin can still control the data `X`/`Z` without changing the number of flag excitations, so the number of data-controlled two-qubit gates need not increase. Exchange/differential-`Z` flag preparation and encoded readout are additional physical costs. An arbitrarily strong noise term

\[
(Z_{f_1}+Z_{f_2})\otimes B_{M}(t)
\]

annihilates the encoded bit for *every* bath operator, including time-dependent and noncommuting operators. This proves exact protection **through the whole gate** under the specified collective-noise algebra; it is not a numerical small-coupling approximation.

**Executed:** complete correlated `D:M:E` state and physical four-spin flags, with two distinct large noncommuting bath operators. At collective-noise amplitude 230, the completed output-and-bath trace discrepancy was `1.60e-14` (floating-point residual). An additional *differential* coupling of strength `0.12` over duration `0.77` instead produced output–bath discrepancy `0.05894`, within its `0.0924` full-boundary Duhamel allowance. Collective-noise protection does not imply differential-noise protection.

If the only remaining flag perturbation is *off-code*, with accepted-code projector `P_F`, zero in-code part and integrated off-diagonal norm at most `L`, then

\[
\|P_F(U-U_0)P_F\|\le L^2/2.\tag{9}
\]

Proof: write Duhamel in the block-diagonal reference interaction picture; its first-order `P_F V P_F` term vanishes. Bound the intermediate out-of-code amplitude by `h t`, and integrate the second insertion. Arbitrarily large Hamiltonian terms entirely outside the code do not enter. With ideal deterministic outputs that assign *zero* probability to a specified wrong event, its accepted wrong-event probability is at most `L^4/4`. **This is not a fourth-order bound on the whole channel in the presence of arbitrary pre-existing faults.** In the nonzero witness, `L=0.2` gave accepted incorrect-output probability `9.9335e-05` versus ceiling `4.0e-04`, while about 1.97% of rounds were flagged as erasures.

## 5. Decisive failures and cost comparison

1. **Preinteraction direct flag-to-bath access.** A bath copies the `X` flag bit and subsequently uses a fixed `Z_D Z_M` interaction. Compared with the properly isolated-flag twirl, the logical output differs by trace distance exactly **0.3535533906** at `theta=pi/8`. Every observed flag bit remains perfectly uniform. Key-frequency tests do not certify control isolation.
2. **Postinteraction direct flag-to-bath access.** Copy the same key into the bath *after* the noisy interaction, prior to flag retirement. Now the current delivered data state has **zero** trace-distance discrepancy from the ideal case, yet the complete delivered-data-plus-bath state differs by exactly **0.5**. Subsequent calls can therefore depart from the assumed process, despite perfect current-output tomography. Full-boundary protection extends through correction and retirement.
3. **Too few distinct frames.** The 4×4 Pauli-character matrix has rank four. For arbitrary one-qubit errors, exact suppression of every nonidentity character forces the unique uniform four-key distribution. A single `I/X` quantum flag leaves coherent `X` rotations untouched. In a Choi witness, subtracting even a tiny positive ideal-identity CP component makes the result nonpositive.
4. **Reused quantum flag.** Reuse the same unmeasured four-valued key across two coherent `Z` rotations. At angle `pi/8`, the decoded two-call output differs from the independent-fresh-key process by trace distance **0.25**. An isolated **fresh initialization** or an independent preprepared flag for every call is necessary.
5. **Limited tomography.** Even complete current *logical* output tomography cannot detect all key-to-bath leakage (failure 2). A real complete-boundary isolation claim must be justified by a physical architecture, symmetry with specified allowed operators, or a independently established diamond/interaction-norm bound. The prior autonomous hidden-clock example forbids silently extrapolating arbitrary finite calibration to infinite life.

A bound `||H_flag-leak||<=h` over time `T` gives the conservative full-channel half-diamond allowance `hT` (capped at 1) for that call by Duhamel. Across an active finite sequence, complete-comb hybrid composition can cost the sum of such allowances unless an exact symmetry (such as the collective DFS above) removes the term. **It must not be represented as a Bernoulli fault probability** without a genuine positive CP decomposition.

### Comparison with an equally informed conventional controller

- **Protected classical two-bit RNG + classical Pauli pulses:** identical completed twirl and positive effects, simpler when RNG and pulse privacy are already trusted. No claimed performance separation.
- **Quantum delayed-key controller:** two transient coherent flags per qubit call (four physical spins if DFS encoded), two controlled-Pauli preframes and trusted postcorrection. No classical private frame key exists during the noisy core; the *quantum* flags still need genuine protection and fresh preparation. The bath may learn frame information from the data; only direct access to the flags/control channels violates the premise.
- **Entanglement-first/late teleportation:** earlier Astra equivalence gives another exact instrument using a protected Bell pair and trusted terminal Bell measurement instead of quantum-controlled preframes. It may be cheaper for remote entanglement delivery but more expensive when Bell measurement or output buffering is difficult.
- **Whole-run quantum-secure key-tape extraction:** amortizes quantum conditional-min-entropy overhead, needs classical protected tape and public seed. The quantum-flag method does not prove that random entropy is free: clean `|+>` preparations and private quantum flags are supplied quantum resources.

## 6. Scientific status and next physical experiment

The mathematical mechanism follows from **deferred measurement, Pauli twirling, quantum instruments, positive CP refinements and decoherence-free subspaces**. Those are established principles. The programme-specific consolidation is the *complete hidden-memory fault/test equality*, an active role-hidden service without classical frame-tape extraction, the pre-gate `T` error placement, and a full-boundary demonstration of harmless data-mediated inference versus destructive **direct key exposure**. No original priority, device acquisition, threshold or infinite lifetime is claimed.

The highest-leverage test is a small hardware demonstration using one noisy data qubit and a two-bit protected coherent flag: (i) prepare and optionally DFS-encode fresh flags, (ii) implement the two controlled input Paulis, (iii) vary a prescribed bath-coupling or simulated memory core without direct flag access, (iv) measure flag and decode the output, (v) repeat with a deliberate flag→bath side channel **before and after** the core, and (vi) compare the *complete instrument on a retained spectator memory*, not merely current data tomography or flag frequencies. Any future use must be budgeted separately for finite gate errors, report flips, key reinitialization and source staging. A strong classical RNG controller with the same trusted operations is the primary comparator.

## Prior literature and source scope

- Wallman & Emerson, *Noise tailoring for scalable quantum computation via randomized compiling*, Phys. Rev. A 94, 052325 (2016), https://doi.org/10.1103/PhysRevA.94.052325. Randomized compiling is established prior science; common-core/gate dependence matters.
- *Quantum circuits with classical channels and the principle of deferred measurements*, Theoretical Computer Science 920 (2022), https://doi.org/10.1016/j.tcs.2022.02.002. Deferred-measurement equivalence is established prior science.
- Tomamichel, Schaffner, Smith & Renner, *Leftover Hashing Against Quantum Side Information* (2011), https://arxiv.org/abs/1002.2436. Quantum-secure classical key-tape extraction, used in previous Astra branch.
- Lidar & Whaley et al., *Theory of decoherence-free fault-tolerant universal quantum computation*, Phys. Rev. A 63, 042307 (2001), https://doi.org/10.1103/PhysRevA.63.042307. DFS/noiseless-subsystem mechanisms are established.
- Kattemölle, Gulácsi & Burkard, *Non-Markovianity induced by Pauli twirling*, npj Quantum Information (2026), https://doi.org/10.1038/s41534-026-01345-5. Pauli-form logical channels do not make their baths Markovian.
- User-supplied governing source files: `LIBRARY_RENDERED_ACQUIRED_TASK_INTEGRITY_WITH_QUANTUM_MEMORY(1).txt` and `LIBRARY_RENDERED_COMPOSED_POSITIVE_SERVICE_FAULTS(1).txt`, plus the most recent private-key file at the beginning of this note. All referenced simulations are computations only, with the retained environment explicitly evolved for validation; the observer does not reconstruct it.

## Reproducibility

Run `bash RUN_VALIDATIONS.sh` in this directory (Python 3 with NumPy and SciPy). Six separate numerical scripts emit corresponding JSON results, and the run creates `validation_log.txt`. All numerical claims above are from files in this directory; no hardware device was used.
