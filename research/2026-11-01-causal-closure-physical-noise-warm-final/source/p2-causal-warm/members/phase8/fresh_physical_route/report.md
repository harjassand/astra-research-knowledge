# Independent physical route: a bounded dirty mediator is the ordinary benchmark

## Result and scope

Starting from the desired capability, without reading the phase7 construction, I obtain a strong ordinary architecture: use a finite mediator with two anticommuting unitary controls, close a four-interaction group commutator for every physical two-qubit operation, and compile parity extraction and consumed CNOT into standard fault-tolerant Clifford gadgets. The mediator can start every use in an arbitrary state, including a state entangled with the data, earlier syndrome records, another mediator, or an external reference. It need not be measured or reset.

This is **not a new no-reset gate principle**. Proctor, Dooley, and Kendon give the qudit version of the same closed-loop construction in 2015 [1, Eqs. (21), (25)]. Its qubit case is already sufficient here. The consequential physical property is a **uniformly bounded harmful interaction and noise algebra**, together with an exact ideal operation that acts as identity on the mediator. Those two properties allow arbitrary retained memory to be carried through a fault-path proof without an energy cutoff or a fresh-error assumption.

The resulting architecture is conditional on measurable hardware requirements: bounded errors per interaction, finite and budgeted preparation/readout/wait times, physical fault-tolerant syndrome gadgets, and enough parallelism that idle exposure does not grow without bound with code size. It is a complete architecture-level comparator, not an experimentally validated device design or a numerical threshold estimate. The accompanying code verifies the exact gate and all eight branches of the consumed-CNOT identity; it does not replace fault-tolerant circuit certification.

Changing to a finite spin is a real architectural change. It handles arbitrary spin-state uncertainty; it does not reproduce an oscillator's unbounded excitation ladder. Nor does it imply temperature-independent noise rates: if the physical bath temperature increases relaxation/excitation rates, the resulting integrated rates still have to satisfy the fault-tolerance bound. The permission to change the mediator makes this a legitimate benchmark; a task that specifically requires an unbounded harmonic mediator must retain the stronger oscillator admission problem.

For a genuinely unbounded oscillator, the analogous uniform conclusion does not follow from a hot-bus ideal identity or a mean-energy bound. An arbitrarily small residual conditional displacement has order-one effect on sufficiently hot input states. Exact closure, a proven global state-tail condition, or a protected bounded subsystem is still necessary. The root investigation's two-sided damped force closure is therefore a substantive condition; it should be compared against the ordinary dirty-qudit construction rather than advertised as the first way to reuse an uninitialized mediator.

## 1. Exact construction, including arbitrary quantum memory

Let A and B be computational qubits and M a mediator qubit. Define

\[
 C_A(X_M)=|0\rangle\!\langle0|_A\otimes I_M+
 |1\rangle\!\langle1|_A\otimes X_M,
\]

and similarly \(C_B(Z_M)\). Apply, in chronological order,

\[
 C_A(X_M),\quad C_B(Z_M),\quad C_A(X_M),\quad C_B(Z_M).
\]

For computational values a,b, the operation on M is

\[
 Z_M^bX_M^aZ_M^bX_M^a=(-1)^{ab}I_M.
\]

Consequently the full operator is

\[
 W_{ABM}=\operatorname{CZ}_{AB}\otimes I_M. \tag{1}
\]

This is an operator identity, not a statement about an initialized or thermal ensemble. For every joint state \(\rho_{ABMR}\),

\[
 (W\otimes I_R)\rho(W^\dagger\otimes I_R)
 = (\operatorname{CZ}_{AB}\otimes I_{MR})\rho
   (\operatorname{CZ}_{AB}^\dagger\otimes I_{MR}). \tag{2}
\]

Thus an old mediator error, or an arbitrary mediator-reference correlation produced in earlier uses, cannot spread onto new data through a later **complete ideal** loop. This statement survives conditioning on any physically obtained past record because it holds on every joint input operator.

The standard d-dimensional generalization uses Weyl operators satisfying \(ZX=\omega XZ\), with \(\omega=e^{2\pi i/d}\). The commutator produces \(\omega^{ab}\) on the computational controls and identity on the mediator. The 2015 qudit-bus paper explicitly distinguishes this initial-state-independent closed-loop identity from schemes whose arbitrary angle depends on a selected initial qudit state [1].

### Continuous physical controls

These operations do not require instantaneous ideal pulses. For duration \(\tau\), bounded Hamiltonians

\[
 H_{AM}=\frac{\pi}{2\tau}|1\rangle\!\langle1|_A\otimes(I-X_M),
 \qquad
 H_{BM}=\frac{\pi}{2\tau}|1\rangle\!\langle1|_B\otimes(I-Z_M)
 \tag{3}
\]

generate the desired controlled Paulis. Their operator norms are \(\pi/\tau\). Known mediator free evolution may be included in the control frame. Unknown free evolution during the loop is noise and must be charged; arbitrary mediator-only evolution **between** loops can be absorbed into the retained memory without a data penalty.

For a common relative angle error \(\delta\) in all four controls, telescoping gives

\[
 \|\widetilde W-W\|\le4\pi|\delta|, \tag{4}
\]

with the trivial cap 2. Unlike a residual bosonic displacement, this bound is uniform on every mediator state. It includes systematic calibration error repeated coherently over many uses; it does not presume independent calibration draws.

### What a fault can spread

A fault inside one complete loop may act arbitrarily on A, B, and M. That is an ordinary two-data-qubit fault, with memory attached. A subsequent fault-free complete loop on A',B' is \(\mathrm{CZ}_{A'B'}\otimes I_M\), so retained M cannot enlarge the previous fault's data support. A later faulty loop may introduce an additional pair-supported error, but that event consumes a second physical fault contribution.

For transversal operations, each pair contains one physical coordinate from each encoded block. One faulty loop can therefore affect at most one coordinate in each block. It must not be silently promoted to a high-weight fanout loop: using M to entangle many coordinates before closing would enlarge the support of one fault and alter the code's fault budget.

### A stronger equal-component parity comparison

For exactly two data qubits, one can safely exploit a more compact construction when the receiver certifies the corresponding pair-error algebra. Use one dirty qubit M and one real readout ancilla A. In chronological order apply

\[
 \mathrm{CX}_{D_1\to M},\ \mathrm{CX}_{D_2\to M},\
 \mathrm{CZ}_{A M},\ \mathrm{CX}_{D_2\to M},\
 \mathrm{CX}_{D_1\to M},\ \mathrm{CZ}_{A M}.
\]

The operator is exactly

\[
 V=\mathrm{CZ}_{A D_1}\mathrm{CZ}_{A D_2}\otimes I_M. \tag{1a}
\]

Preparing A in \(|+\rangle\) and reading \(X_A\) gives the even/odd projectors of \(P=Z_1Z_2\), with no additional data phase frame. It uses six two-body interactions, or four stages if the commuting two-data couplings run simultaneously. There are the same three coupling channels D1–M, D2–M, A–M as in a one-bus force-loop parity experiment. Control type, coupling strength, duration, and parallel pulse capability differ and must be compared explicitly. Multi-control geometric compression is already ordinary prior art [1, Eq. (28)].

The finite comparator requires access to two noncommuting mediator control axes. If only controlled-Z couplings are native, the data-controlled X stages require mediator Hadamard rotations; four such rotations suffice after combining adjacent basis changes in the fused sequence. Their duration and noise must be counted. The force bus instead requires controllable quadratures. Merely equating the number of boxes in the circuits would obscure this hardware distinction.

There is a precise single-fault containment argument for this fused construction and for the root team's diagonal force construction. Let \(\mathcal A_Z=\operatorname{alg}(Z_1,Z_2)\). If every nominal evolution is in \(\mathcal A_Z\otimes\mathcal B(AM)\), a fault on data site j yields an operator in

\[
 \mathcal B(\mathbb C_j^2)\,\operatorname{alg}(P)\otimes\mathcal B(AM), \tag{1b}
\]

because each diagonal operator has the form \(A(P)+Z_j B(P)\). A mediator-only/ancilla-only fault, or a force-control fault that preserves data-Z diagonality, gives the smaller span \(\operatorname{span}\{I,Z_j\}\operatorname{alg}(P)\). This remains true for arbitrary fault time, fault strength, and retained memory.

If P is a **gauge operator of the actual receiver code**, the gauge factors can be removed from the logical error budget and the remaining data action has a one-site representative. If P is a measured logical parity in a consumed CNOT, arbitrary functions of P cannot simply be dismissed as gauge. The physical parity instrument then has to be certified within its encoded gadget. In either case (1b) is an error-support statement, not a bound on how often or how strongly the error occurs. The detailed proof is in `single_fault_support.md`.

## 2. Real parity extraction and a consumed CNOT

The mediator is a transport/control element. A parity measurement still needs an entropy sink: actual preparation and actual readout of ancillary degrees of freedom. An arbitrary maximally mixed mediator does not supply a known syndrome bit merely because it is reusable. All such ancillary operations below are noisy physical operations included in the circuit.

### Logical ZZ and XX parity

Use a CSS code with transversal CNOT; a concatenated Steane code is a concrete ordinary choice. To measure \(Z_L^C Z_L^T\), physically prepare an encoded \(|0_L\rangle_S\), apply logical CNOTs C→S and T→S, and physically measure \(Z_L\) on S. Implement every physical CNOT as target Hadamards surrounding (1). The preparation, transversal interactions, decoded readout, and error-correction rounds are implemented with the usual finite noisy circuits.

An XX measurement follows by Hadamards on the relevant logical inputs, or by the corresponding dual CSS circuit. Fault-tolerant encoded preparation and measurement are essential. One noisy physical readout ancilla coupled in sequence to all data qubits can acquire an X-type hook that spreads to many data coordinates. Closing the mediator loop does not fix that separate fault path. Verified cat-state extraction, encoded-block extraction, or a certified flag construction can address it; all verification measurements, flags, rejected preparations, and waits must be charged as physical operations. Ordinary constructions of these components are available [2, Secs. 7–8].

A bounded schedule is needed. One can compile a fixed finite preparation/verification-and-fallback gadget and count every branch, rather than condition on indefinite successful retries. Alternatively one must explicitly prove a tail bound on retry duration and include the receiver's waiting noise. Neither acceptance nor a flag is an oracle.

### The consumed ancilla CNOT identity

Let C and T be encoded control and target blocks, and A an encoded ancilla. At the logical ideal level:

1. Prepare \(|+_L\rangle_A\).
2. Measure \(Z_L^C Z_L^A\), with outcome \((-1)^{m_{ZZ}}\).
3. Measure \(X_L^A X_L^T\), with outcome \((-1)^{m_{XX}}\).
4. Measure \(Z_L^A\), with outcome \((-1)^{m_{ZA}}\), consuming A.
5. Track the Pauli frame
   \(Z_L^{C\,m_{XX}}X_L^{T\,(m_{ZZ}\oplus m_{ZA})}\).

The resulting operation on C,T is CNOT. Direct multiplication of the projectors shows that every corrected branch Kraus operator is \(\pm\mathrm{CNOT}/\sqrt8\). `verify_dirty_bus.py` checks all eight branches and their completeness. This identity is derived here to specify the receiver and the outcome information exactly; it is an ordinary measurement-based Clifford construction, not a novelty claim.

The physical implementation uses the real parity circuits above. The final C,T blocks are retained and enter the same noisy receiver schedule used for any candidate: storage, further encoded H/CNOT operations, error correction, and eventual physical readout. An ideal decoder may be used as a mathematical equivalence in the proof; it is never a physical recovery step supplied to the protocol.

If a consumed *four-block Choi resource* is preferred, prepare two noisy encoded Bell pairs, apply a fault-tolerant CNOT to their output halves, and consume the two input halves in physical encoded Bell measurements. The same receiver and the same physical fault accounting apply. This changes resource bookkeeping, not the underlying memory guarantee.

### Errors that survive one cycle

For a distance-three code, a late error after cycle k's effective recovery can remain correctable at its output. A fresh error in cycle k+1 can then produce an uncorrectable pair. Therefore “every cycle tolerates one fault on a clean input” is inadequate, and conditioning on an already faulty input generally changes a putative \(O(p^2)\) next-cycle bound to \(O(p)\).

The proper unit is an extended rectangle containing the gate, its leading and trailing recovery, ancilla preparation/readout, and all associated idles. Adjacent extended rectangles overlap. A proof must use truncation or an equivalent overlap convention so that a shared recovery fault is neither dropped nor assigned independent probabilities twice. The established distance-three threshold analysis was designed to handle this issue [2].

The retained mediator adds no hidden propagation in a fault-free loop, but retained **data** errors remain in the ordinary extended-rectangle budget. The deterministic repetition-code example in the verification output illustrates this distinction: a late X on coordinate 1 and a fresh X on coordinate 2 cause the next majority correction to fail, even though each individual error was correctable.

## 3. Joint history guarantees under continuing noise

Two different statements must be kept separate. A general coherent-noise model yields a joint **fault-path norm** guarantee. A classical probability bound on fault histories additionally requires a physical CP trajectory/instrument decomposition. Calling a coherent norm bound a probability bound is incorrect.

### 3.1 State-uniform local channel bounds

Include the retained mediators and any non-Markovian environment in a common memory E. For a primitive location l, suppose the exact ideal joint channel is

\[
 \mathcal G_l=\mathcal U_l^{D_l}\otimes\mathcal B_l^E,
\]

where \(D_l\) contains at most the allowed physical pair, and \(\mathcal B_l\) is a memory-only channel. Let the actual map be \(\mathcal N_l=\mathcal G_l+\mathcal F_l\), with

\[
 \|\mathcal F_l\|_\diamond\le\epsilon_l. \tag{5}
\]

This norm is taken on the **joint** data-memory space, with an arbitrary additional reference. A reduced data channel evaluated only on one thermal state is insufficient.

For a specified ordered set S of r marked locations, sum all fault paths that have a fault factor at every marked location and either factor at all unmarked locations. Algebraically this sum is the circuit product with \(\mathcal F_l\) at marked locations and the full \(\mathcal N_l\) elsewhere. Since every unmarked \(\mathcal N_l\) is CPTP and has diamond norm 1,

\[
 \|\mathcal F(S)\|_\diamond
 \le\prod_{l\in S}\epsilon_l. \tag{6}
\]

There is no independence, fresh-bath, factorized-input, or conditional-energy assumption. All retained quantum memory is still present in the composition. The microscopic generator locality must match the circuit locality: a common control fault that simultaneously reaches many data coordinates must be charged to its actual support, not split into artificial independent pair faults.

### 3.2 Deriving (5) from physical generators

For a finite active mediator, bounded local control errors and bounded jump operators supply a simple sufficient condition. Write, on the joint active system and memory,

\[
 \mathcal L(t)=\mathcal L_0(t)
 -i[\Delta H(t),\cdot]+\sum_a\mathcal D[L_a(t)],
\]

with \(\mathcal L_0\) the ideal control plus any allowed memory-only dynamics. Duhamel's formula and CPTP contraction give

\[
 \|\mathcal N_l-\mathcal G_l\|_\diamond
 \le\int_l\!\left(2\|\Delta H(t)\|
       +2\sum_a\|L_a(t)\|^2\right)dt
 \equiv\eta_l. \tag{7}
\]

The identity \(\|\mathcal D[L]\|_\diamond\le2\|L\|^2\) follows by bounding its three terms. This is a conservative sufficient bound, not a fitted infidelity. It counts relaxation, excitation, dephasing, coherent calibration, and the non-Hermitian no-jump contribution. In particular it never argues that “no jump” means “no error.”

Parallel local noise and spectator idles can be treated by a microscopic Trotter expansion and regrouped into space-time locations. All local generator terms must be counted. Alternatively a bounded local joint Hamiltonian dilation gives the standard amplitude version of (6); arbitrary bath-only dynamics need no smallness or reset assumption [2, Sec. 11].

Preparation and readout use their actual joint CPTP maps, including a classical outcome register. A norm bound of the same form must be supplied for each map, or derived by integrating a physical preparation/readout model. Readout duration and feedforward latency are idle locations on the retained receiver. Finite dimensionality alone does not prove those devices have sufficiently small errors.

Classical record storage and Pauli-frame processing also require a reliability assumption or an explicit protected implementation. A controller that can flip an unbounded number of parity records in one common event violates the stated local support condition. It cannot be represented by independent readout error coins merely for convenience.

### 3.3 From physical locations to logical locations

Suppose a physically compiled, single-fault-tolerant extended rectangle contains at most A primitive locations. For disjoint fault-counting regions, an inclusion-exclusion count of paths with at least two faults gives the conservative form

\[
 \epsilon^{(1)}\le {A\choose2}\epsilon^2e^{(A-2)\epsilon}. \tag{8}
\]

The analogous marked-region bound has the product form \([\epsilon^{(1)}]^{|R|}\). The extended-rectangle overlap/truncation proof is needed for adjacent regions; simply asserting (8) independently for consecutive clean-input cycles is invalid. Standard concatenated-gadget analysis supplies the corresponding recurrence after those correctness conditions are certified [2].

With a suitable constant C, the recurrence \(\epsilon_{k+1}\le C\epsilon_k^2\) yields

\[
 \epsilon_k\le C^{-1}(C\epsilon_0)^{2^k}.
\]

This is a joint local-noise guarantee and hence a route to reliable arbitrary receiver circuits, not just a good marginal stored state. It does **not** justify replacing \(\epsilon_k\) by a per-cycle classical error probability for arbitrary coherent noise. Also, the published independent-stochastic numerical threshold of a particular Steane construction must not be reused for this general noise model or for a newly compiled mediated circuit.

### 3.4 A sufficient condition for genuine probability histories

A physically restrictive but explicit probability version is possible. Suppose the actual continuous noise has jump operators

\[
 L_a(t)=P_a^{D_lM}\otimes B_a^E(t), \qquad P_a^\dagger P_a=I,
\]

with support on the active location, and

\[
 \sum_a B_a^\dagger(t)B_a(t)\le\lambda_l(t)I_E. \tag{9}
\]

The no-jump drift then acts only on E, so it cannot alter the ideal data-mediator loop. Jumps at arbitrary times are real CP trajectory events; after conjugation through the remainder of one loop they remain supported on the current pair and mediator. The conditional jump intensity is bounded by \(\lambda_l\) for every retained quantum state, including states selected by previous records. Therefore, for disjoint marked windows,

\[
 \Pr\{\hbox{at least one physical jump in every }l\in S\}
 \le\prod_{l\in S}\int_l\lambda_l(t)dt. \tag{10}
\]

One proof iterates the CP jump instrument and uses its adjoint effect bound \(J_l^*(I)\le p_l I\); a counting-process factorial-moment proof gives the same inequality. The bath can retain arbitrary memory and change the later conditional intensity. No independent error coins are assumed. Equation (9), not a desired histogram, establishes the domination.

Random-unitary spin dephasing/depolarization is an example. Equal-rate spin excitation and relaxation also admit a Pauli-jump Lindblad representation. Generic unequal-rate amplitude damping has a state-dependent no-jump action on M during the gate and does not automatically satisfy this probability construction. Generic coherent calibration errors likewise require the norm formulation, or an additional physically justified randomization/instrument analysis. Noiseless twirling gates may not be inserted as an oracle to evade that requirement.

## 4. The ordinary comparison, with the same information and receiver

All comparisons should use the same physical outcome records and receiver schedule. Every preparation, verification, false flag, missed flag, readout, waiting interval, recovery, and consumed-resource operation belongs in the model. A conditional accepted-state fidelity and an unconditional operational CNOT reliability are different quantities.

| Mechanism | Strong ordinary capability | What remains necessary for this task |
|---|---|---|
| Finite dirty-qudit commutator | Exact ideal entangling gate for arbitrary mediator state/reference, without initialization [1] | Bounded harmful noise; four interactions per physical CZ; actual syndrome circuits; bounded idle schedule |
| GPI with a three-level ancilla | A full bosonic fault-tolerance framework and universal gadgets for four-legged cats, designed to tolerate one photon loss and an arbitrary ancilla fault [3] | Actual ancilla preparation/outcome records and the stated correctable-error domains; calibration mismatch and adjacent recovery budgets cannot be omitted |
| Matched-qutrit error-transparent detection | Engineered dispersive interactions suppress propagation of dominant transmon faults; demonstrated experimentally [4] | Matching imperfections, higher-level leakage, preparation/readout, and repeated-use accounting |
| Stabilized cat ancilla | Biased dominant ancilla noise can be made transparent to data during syndrome extraction [5] | Residual wrong-bias noise, leakage/confinement, noisy preparation/readout, and continuous receiver errors |
| Erasure/detectable bosonic gates | Physical detection of leading errors can turn substantial noise into located erasures [6,7] | Use the actual noisy flag instrument; false negatives, false positives, rejected-resource waits, and receiver errors remain |
| Hot-bus geometric gates | Ideal closed displacement loops already remove initial mediator-state dependence; realistic thermal/dissipative gate analyses exist [1,8] | Exact joint decoupling under damping, calibration residuals, continued-noise history bounds, and full encoded receiver |

The GPI paper is especially strong prior art against a novelty claim based only on single-fault tolerance, parity extraction, or availability of a universal encoded gadget set. Its finite-mismatch discussion explicitly notes that some rotations cease to be strictly one-fault tolerant when mismatch propagates through the final beam splitter [3, Secs. VI.2–VI.3]. This is a physical condition to compare, not a reason to substitute an artificially weak ideal-reset baseline.

There is also a precise scope limit: the preprint's Proposition 1 proof explicitly assumes quantum-jump errors independent between level-1 gadgets [3, Sec. III]. Its gadget definitions correctly budget inherited data errors together with fresh faults, but this particular probability argument is not a proof for an arbitrary retained mediator. A joint-space local-noise admission argument such as (5)–(7), or a real CP instrument theorem, is still required.

If no connectivity or interaction restriction is imposed, an even simpler ordinary comparator is a readout ancilla with a direct bounded interaction \(H=(\pi/4T)Z_A(Z_1+Z_2)\). It implements the force-loop proposal's nominal data-ancilla unitary without a harmonic bus. The same diagonal-algebra support lemma applies. A mediator becomes enabling when it supplies connectivity or a coupling unavailable in the direct architecture, or improves an explicit exposure/resource metric. The extra harmonic degree of freedom alone is not a new computational capability.

### A further ordinary baseline: finite noisy reset

Even when the mediator is deliberately reset, a finite physical reset need not be an oracle. For amplitude damping of a qubit over duration T with residual survival \(r=e^{-\gamma T}\), a Stinespring comparison with replacement by \(|0\rangle\) gives the conservative uniform bound

\[
 \|\mathcal A_T-\mathcal R_0\|_\diamond
 \le\min\{2,2\sqrt{2r}\}. \tag{11}
\]

This holds for arbitrary input-reference correlations. Reset duration, thermal excitation floor, and implementation noise are then charged as ordinary locations. A candidate should beat this physically implemented baseline on a declared resource metric if no-reset operation is proposed as a practical advantage. The dirty commutator avoids that reset cost altogether, at the cost of its controlled interactions.

## 5. The important boundary: arbitrary bosonic occupation

Consider an otherwise ideal controlled operation that leaves a differential displacement \(D(\beta)\) on an oscillator. For a centered thermal state with mean occupation \(\bar n\), its characteristic function is

\[
 \operatorname{tr}[\rho_{\rm th}D(\beta)]
 =\exp[-(\bar n+1/2)|\beta|^2].
\]

Hence an input data \(|+\rangle\) undergoes dephasing with

\[
 p_Z=\frac{1-e^{-(\bar n+1/2)|\beta|^2}}2. \tag{12}
\]

For every nonzero \(\beta\), \(p_Z\to1/2\) as \(\bar n\to\infty\). For example, \(|\beta|=10^{-3}\) gives about 0.316 dephasing probability at \(\bar n=10^6\). Arbitrary coherent initial states can also turn a small displacement into an order-one relative phase. Thus an arbitrarily accurate finite calibration does not by itself furnish a state-uniform small-error bound on an unbounded oscillator.

This does not refute a perfectly closed hot-bus protocol. It says its actual Hamiltonian and noise must either preserve the exact decoupling algebra or admit a state-sensitive bound justified over the entire continued-noise history. A mean occupation at one time is too weak to supply that joint guarantee. Small residual coefficients multiplied by an unbounded quadrature are precisely the term that finite dirty mediators avoid.

For damped force gates, distinguish returning to the **same coherent state** from returning to a common freely damped state independent of the data. Müller, Luoma, and Strunz analyze damping-compensated forces; their Eq. (25) and accompanying discussion concern return to the same selected initial coherent state, and their Eq. (30) imposes positive-exponential moments and offset robustness [9]. That paper's abstract is not a proof of arbitrary-initial-memory factorization with two-sided damped closure. The root team's stronger criterion needs its own derivation and a targeted prior-art search.

## 6. What would actually be enabling?

If changing to a finite mediator is permitted, the requested capability is already enabled by ordinary group-commutator control plus physical fault-tolerant circuits, subject to the uniform local noise and resource conditions above. No new physical principle is needed to obtain the abstract consequence.

If an unbounded hot oscillator is essential, a consequential advance would provide one of the following, with the full receiver included:

- Exact data-memory factorization for the **actual** dissipative dynamics over a nontrivial class of physical control uncertainties, together with a useful entangling action.
- A global, unnormalized, continued-noise tail/instrument theorem strong enough to obtain joint rare-history bounds without postulating a low-energy state after every use.
- A physical bounded logical subsystem whose harmful control and noise are uniformly bounded independently of its hot gauge sector.

The third possibility can be stated algebraically. Identify \(|2n+b\rangle\leftrightarrow|b\rangle\otimes|n\rangle\) and define bounded involutions that exchange \(|2n\rangle\) with \(|2n+1\rangle\) and assign their parity sign. They anticommute and would implement (1) uniformly over n. But realizing those identical matrix elements in every number sector is a serious hardware requirement. Ordinary photon loss has amplitudes \(\sqrt n\), acts nontrivially on the parity subsystem, and violates a uniform harmful-rate bound. Merely relabeling the oscillator as a subsystem does not solve the problem.

For the force-loop candidate, a meaningful contribution could be its simultaneous incoming-memory and outgoing-memory closure under damping, plus a rigorous physical-noise admission theorem and a resource advantage. I have not established novelty of that combined result. The ordinary finite dirty-bus comparator and existing hot-gate literature make clear which claims are already known and where a new theorem would have to add substance.

## Verification and limitations

`verify_dirty_bus.py` generated `verification_results.json`. It found zero floating-point residual for the dirty-mediator operator identity and for every corrected consumed-CNOT branch. The eight branch effects sum to identity with residual \(1.11\times10^{-16}\). The code also lists how mediator Pauli faults propagate at the four internal boundaries, checks the bounded calibration estimate, and evaluates (12).

These are algebra checks. No hardware noise values, measured gate fidelities, receiver threshold, complete compiled malignant-pair count, or novelty conclusion is claimed. The derived norm theorem is conditional on the joint-space assumptions in (5)–(7); the true probability theorem has the stronger explicit physical assumptions in (9). The distinction is part of the result.

## Primary references

1. T. J. Proctor, S. Dooley, V. Kendon, *Quantum computation mediated by ancillary qudits and spin coherent states*, Phys. Rev. A **91**, 012308 (2015). https://doi.org/10.1103/PhysRevA.91.012308 ; full text https://arxiv.org/html/1402.6674v4 . Exact initial-state-independent loop: Eqs. (21), (25). Web reference: turn93view0.
2. P. Aliferis, D. Gottesman, J. Preskill, *Quantum accuracy threshold for concatenated distance-3 codes*, Quantum Inf. Comput. **6**, 97–165 (2006). https://arxiv.org/html/quant-ph/0504218v3 . Physical gadgets: Secs. 7–8; correlated quantum memory and overlapping rectangles: Sec. 11. Web references: turn104view0, turn105view2.
3. Q. Xu, P. Zeng, D. Xu, L. Jiang, *Fault-Tolerant Operation of Bosonic Qubits with Discrete-Variable Ancillae*, Phys. Rev. X **14**, 031016 (2024). https://doi.org/10.1103/PhysRevX.14.031016 ; preprint full text https://arxiv.org/html/2310.20578v1 . Web references: turn95view0, turn96view3, turn99view1.
4. S. Rosenblum et al., *Fault-tolerant detection of a quantum error*, Science **361**, 266 (2018). https://arxiv.org/abs/1803.00102 ; https://doi.org/10.1126/science.aat3996 . Web reference: turn96view1.
5. S. Puri et al., *Stabilized Cat in a Driven Nonlinear Cavity: A Fault-Tolerant Error Syndrome Detector*, Phys. Rev. X **9**, 041009 (2019). https://doi.org/10.1103/PhysRevX.9.041009 . Web reference: turn104view1.
6. T. Tsunoda et al., *Error-Detectable Bosonic Entangling Gates with a Noisy Ancilla*, PRX Quantum **4**, 020354 (2023). https://doi.org/10.1103/PRXQuantum.4.020354 . Web reference: turn96view2.
7. J. D. Teoh et al., *Dual-rail encoding with superconducting cavities*, PNAS **120**, e2221736120 (2023). https://pmc.ncbi.nlm.nih.gov/articles/PMC10576063/ . Web reference: turn94search16.
8. M. J. A. Schuetz, G. Giedke, L. M. K. Vandersypen, J. I. Cirac, *High-fidelity hot gates for generic spin-resonator systems*, Phys. Rev. A **95**, 052335 (2017). https://arxiv.org/abs/1607.01614 ; https://doi.org/10.1103/PhysRevA.95.052335 . Web reference: turn96view0.
9. K. Müller, K. Luoma, W. T. Strunz, *Geometric phase gates in dissipative quantum dynamics*, Phys. Rev. A **102**, 032611 (2020). https://arxiv.org/html/1907.08033v2 ; https://doi.org/10.1103/PhysRevA.102.032611 . Web references: turn104view2, turn105view0, turn105view1.

Research performed 2026-10-31. No phase7 file was read in forming this route.
