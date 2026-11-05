# Raw quantum ports and independent output refresh

Research note, 5 November 2026. This supplies the active-interface contribution to the noisy passive-register construction. It does not change the accepted passive bath theorem.

## 1. Sharp raw-port boundary

Write the qubit replacement-depolarizing channel as

\[
\mathcal D_a(\rho)=(1-a)\rho+aI\operatorname{Tr}(\rho)/2,
\qquad0\le a\le1.
\]

An unknown qubit, possibly entangled with an unrestricted reference, crosses this channel before encoding. The eventual raw output crosses an independent channel \(\mathcal D_b\). Ancillas start independent of the input. Allow any intermediate CPTP map \(\mathcal R\), including encoding, memory, active control and decoding. Then

\[
\boxed{\inf_{\mathcal R}\tfrac12
\|\mathcal D_b\mathcal R\mathcal D_a-\mathrm{id}\|_\diamond
=\tfrac34(a+b-ab).}
\tag{1}
\]

**Proof.** Feed half of a maximally entangled state \(\Phi\). For any qubit channel \(\mathcal R\),

\[
F_e(\mathcal D_b\mathcal R\mathcal D_a)
=(1-a)(1-b)F_e(\mathcal R)
+[1-(1-a)(1-b)]/4.
\]

The replacement term has overlap \(1/4\) with \(\Phi\), even for nonunital \(\mathcal R\). Since \(F_e(\mathcal R)\le1\), trace distance from \(\Phi\) is at least \(3(a+b-ab)/4\). Taking \(\mathcal R=\mathrm{id}\) attains the bound: the composed channel is \(\mathcal D_{a+b-ab}\), whose half diamond distance is exactly \(3(a+b-ab)/4\). ∎

For Pauli depolarizing noise of total nonidentity probability \(p\), \(a=4p/3\) for \(p\le3/4\). A permitted first-location replacement fault in a broader stochastic circuit model similarly gives a constant-order lower bound. Equation (1)'s exact coefficient applies only to the stated cut model.

The honest raw-port target is \(O(p)+\epsilon\), preserving arbitrary references. An arbitrarily accurate encoded port is a different specification whose acquisition and final decoding must be charged. New raw deliveries pay new endpoint errors; reuse of an already encoded state need not pay the original input error again.

## 2. Existing active fault tolerance attains this endpoint scale

Christandl, Fawzi and Goswami, *Fault-tolerant quantum input/output*, arXiv:2408.05260v3, Theorem 43, constructs a circuit of size \(|\Phi|\operatorname{poly}(k)\) satisfying, for independent stochastic circuit fault rate \(p\),

\[
\|\widetilde\Phi-(\otimes_i W_i)(\Phi\otimes F)(\otimes_j N_j)\|_\diamond
\le4|\Phi|(cp)^k.
\tag{2}
\]

Here \(\operatorname{Tr}_{F_k}N_j=(1-\eta_j)\mathrm{id}+\eta_jZ_j\) and \(W_i=(1-\xi_i)(\mathrm{id}\otimes\operatorname{Tr}_{F_k})+\xi_iZ'_i\), with \(\eta_j,\xi_i\le2cp\). The auxiliary \(F\) can correlate syndrome systems. One raw input and output therefore give \(O(p)+\epsilon\), choosing \(k=O(\log(|\Phi|/\epsilon))\).

The theorem assumes noiseless classical computation and has no geometric-locality guarantee. Both restrictions need a paid bridge. Source: https://arxiv.org/pdf/2408.05260 . Relevant results: Corollaries 26–27, Lemmas 40–42, Theorem 43.

## 3. Direct bottom decoding does not productize noise

A computational output can have correct logical information while its correctable syndrome subsystems remain correlated with prior faults, other outputs and records. Noisy bottom decoders can expose those correlations. Independence of new decoder faults is insufficient. The auxiliary \(F\) in (2) retains this phenomenon; concatenation alone does not make the uncorrected physical state close to a perfect codeword.

## 4. Independent encoded Bell refresh

For each intended physical output \(i\): independently prepare a protected Bell pair \(A_iB_i\); perform the logical Bell transform on \(D_i,A_i\), fan out its two logical Z bits into protected copy pools, and discard \(D_i,A_i\). Independently descend the copies to raw bits; regenerate the two Bell bits through fixed noisy majority trees. Independently descend \(B_i\), and apply the byproduct only as a final raw Pauli. No old coherent control touches \(B_i\). Reset fine internal records, charging their storage and erasure. Retain pre-existing external records and references. The fully closed same-code construction is in same_code_controller_bridge.md; the tree proof is in ../passive_route/static_tree_regenerator.md.

The majority-tree root and the raw quantum output arrive at the same prescribed clock. Their terminal paths overlap; earlier padding occurs while registers remain encoded. Early descent or an early raw classical root followed by a growing wait is invalid. Factory schedules are deterministic and padded. No adaptive global factory acceptance is used.

### Exact virtual identity

Let the incoming state be arbitrary \(\omega_{D_LS_DR}\), and let an independent fresh resource be \(\Phi_{A_LB_L}\otimes\tau_{S_AS_B}\). The ideal destructive logical Bell instrument traces \(S_D,S_A\). After the Pauli correction its output is exactly

\[
\omega_{D_LR}\otimes\tau_{S_B},
\tag{3}
\]

with \(D_L\) relabelled \(B_L\). Bell outcomes are uniform, independent of the input and surviving syndrome. This holds for arbitrary logical–syndrome–reference correlations and for entangled \(S_A,S_B\). For independent resources, the new syndrome marginal is \(\otimes_i\tau_{S_{B_i}}\); logical outputs can remain arbitrarily entangled.

CFG Corollary 26 gives an exact replacement for protected pure-state preparation of virtual form \(|\psi\rangle\langle\psi|\otimes\tau\). Corollary 27 gives an exact replacement for a destructive measurement of form intended logical measurement tensored with trace of its syndrome. Bell preparation and Bell measurement are instances.

### No global success conditioning

Use hybrid replacement of high-level Bell preparation/measurement circuits, whose total diamond error is at most \(\epsilon\). Do not condition on global success: it could correlate resources. Each local resource/descent keeps its full independent noise ensemble.

For Pauli stabilizer circuits the comparison is explicit: sample a local resource fault ensemble, virtually decode it, correct rare logical Bell errors in the comparison, and retain its syndrome label. Paths outside the protected code are assigned a fixed allowed syndrome. The discrepancy is bounded by protected preparation error. This gives an independent classically sampleable comparison distribution without conditioning.

## 5. Product boundary channels, with exact Pauli twirling

The active noise contract has an independent stochastic Pauli fault at every bounded-arity quantum gate, preparation, measurement and idle, with specified probabilities. Fault laws are independent of the unknown input and, for Pauli correction gates, independent of the Pauli label. Classical elementary operations also have fixed nonzero independent stochastic errors; they are protected, not ideal. Fresh resource factories and descents use disjoint noise variables. Common drift is outside this contract.

At sufficiently small fixed component error \(p\), protected execution plus refresh gives independent single-qubit channels \(K_i\), with the total implementation within \(\epsilon\) of

\[
(\otimes_iK_i)\circ\Phi,
\qquad \tfrac12\|K_i-\mathrm{id}\|_\diamond\le Cp.
\tag{4}
\]

Input to \(\Phi\) here is already computationally encoded. A raw unknown input adds its separate \(O(p)\) injection channel. The constant is independent of requested size, duration and accuracy, though the actual \(K_i\) can depend on the chosen concatenation level and schedule. Encoded waits and byproduct processing are counted. The statement holds against arbitrary pre-existing references and records, after resetting fine internal transcripts.

The static tree erases dependence of its final classical bit errors on old physical-control syndromes, up to the chosen additive error. Ordinary coherent protected feedforward alone does not earn this fact: even correct logical controls could imprint old gauges on the fresh Bell half. Defer all byproducts to the raw output. The uniform Bell outcome itself supplies the twirl; no additional random seed is needed. If \(E_i\) is the independent uncorrected quantum descent, the corrected channel contains

\[
\overline E_i=\tfrac14\sum_{R\in\{I,X,Y,Z\}}
\mathcal R^{-1}E_i\mathcal R,
\]

composed with the tree's independent bit-error Pauli channel and terminal independent Pauli-gate noise. It is exactly Pauli and remains \(O(p)\)-close to identity. The Bell outcomes and fine tree records are reset after use. The statement concerns the averaged marginal after those internal records are discarded.

The terminal correction uses an always-scheduled physical CNOT and controlled-Z from the two raw classical control bits to the output. Both are bounded-arity native gates with the declared stochastic faults. No ideal gate-selection controller is required.

This avoids an assumption that every protected controller circuit is Clifford or classically simulatable. The same-code AB prefix, local-stochastic fanout, noisy-tree decoupling and terminal correction supply the complete interface.

### Explicit comparison resources and acquisition

The comparison resource need not be existential. Apply a specified virtual decoder to the independently generated Bell resource; discard its logical pair; replace that pair by an ideal Bell state; retain its syndrome marginal; and re-encode. Extend the virtual decoder by a fixed channel outside the protected code. If the physical resource has logical Bell fidelity at least \(1-\delta\) and protected-code leakage at most \(\delta\), this replacement changes its state by \(O(\sqrt\delta)\). Choose the protected error \(\delta\) small enough for the desired total \(\epsilon\). This operation is only a mathematically defined comparison and calibration circuit; it is not an ideal physical step in the actual interface.

For a specified Pauli fault model, the channel probabilities are computable from known finite circuits. Stabilizer paths admit efficient classical Monte Carlo. More generally, protected quantum simulation of the known noisy circuit and its explicit virtual decoder samples the comparison channel. Prepare an encoded Bell state, simulate the comparison channel intentionally including the sampled fault variables, and measure its encoded Bell basis. This is a known-state, classical-output calculation and therefore has no raw-port accuracy floor. Its actual computational faults are suppressed below the desired calibration accuracy using the same fixed-rate fault tolerance.

Operationally, keep the sampled classical outcomes, counters and parameter estimates encoded and pass them directly to the protected preparation algorithm. A logical measurement can be represented by copying its basis label into an encoded register and discarding the measured system. There is no requirement to export one arbitrarily reliable raw classical bit and reimport it. A user-facing numerical report may use redundant readout; it is not the controller on which the preparation depends.

Estimating four probabilities to total variation \(\eta_i\), with failure probability \(\delta_i\), uses \(O(\eta_i^{-2}\log(1/\delta_i))\) samples, each costing the protected simulation size. Product-channel uncertainty is at most \(\sum_i\eta_i\). Charge this once for each level, schedule and distinct gadget law used; reuse only under justified homogeneity. Experimental justification of the independent Pauli model and estimation of its elementary parameters remain commissioning tasks. A theorem for specified noise parameters is not a hardware-identification theorem.

## 6. Noisy read injection

On reading a physical memory, apply independent actual raw-to-computational-code interfaces to its physical qubits, built by the adjacent-level construction in the same AB code. Each logical marginal is \(O(p)\)-close to identity against arbitrary references. For exact Pauli twirling, commission protected uniform two-bit seeds before the scheduled read; deliver their noisy raw versions through the same independent majority-tree regenerators. Apply each raw seed Pauli at capture and the inverse of its protected logical seed after injection. The tree's fresh binary-symmetric seed discrepancy and the raw gate faults add an independent Pauli factor to the twirled input channel \(J_i\). Preparation occurs while the memory continues its counted passive hold. No raw memory qubit waits for seed processing.

Thus reading realizes, up to \(\epsilon\), a product input channel \(\otimes_iJ_i\) followed by the intended protected decoder. This fact alone does not prove thermal logical stability: the product channel is applied to the stored state before decoding. That bridge is provided separately by the forward-noise prefix lemma and perturbed-history bound in the root inverse-noise theorem. There is no invocation of an unproved dynamical basin.

Read injection begins simultaneously across physical ports. Its bare first steps have a bounded predetermined duration. The remaining injection and decoder operations take place in protected computational codes. Raw final delivery occurs only after the global protected computation and feedforward have completed.

## 7. Replacing noiseless classical processing

The definitive route uses Aharonov–Ben-Or's measurement-free native scheme throughout: https://arxiv.org/pdf/quant-ph/9906129 . Its §4 constructs noisy quantum versions of all classical syndrome processing; §7 proves correctness of sparse fault paths for arbitrary correctable incoming states. The finite native gate set includes CNOT and Toffoli, preparation, discard and idle. No mutable classical controller is noiseless. The exact code, spread margin, adjacent-level interfaces and independent bad-fault tags are derived in same_code_controller_bridge.md.

The static majority tree is implemented by the bounded-arity circuit CNOT(a,b), CNOT(a,c), Toffoli(b,c,a), retaining a. Its Pauli-fault truth tables preserve simultaneous complement of all input bits. The tree couples its possibly correlated initial errors to a reference process using fresh internal faults, so its final bit is a fresh binary-symmetric channel up to a vanishing error. This supplies the necessary physical-control independence before the terminal raw Pauli.

Paz-Silva, Brennen and Twamley, https://arxiv.org/pdf/1002.1536 , is a useful additional example of noisy measurement-free control, but its distance-three implementation is not silently substituted into CFG's concrete rectangle construction. No published numerical threshold is transferred after a change of code or layout.

All controller storage, gates, idles, copies, processing, measurements and resets are charged. No unprotected shared classical bit controls an encoded macroscopic correction. The final classical controls touch only their bounded local raw gate.

## 8. Explicit deployment architecture and its boundary

For the complete circuit theorem, use the following architecture rather than silently assuming three-dimensional local routing:

1. At each memory site install one constant-size base-code cell, including the ancillas used in the fixed bottom encoder/decoder gadget. A constant geometric dilation provides room for these cells. The original Hamiltonian interactions then have a larger but still constant range. Fabricating the enlarged interaction cells and the switching couplers is part of the device specification.
2. Put all growing higher-level code blocks, resource factories and protected controllers in a separately charged active processor fabric. The active gate set explicitly permits scheduled nonlocal gates between its qubits and the base-code cells, with specified bounded stochastic error, clock duration and per-use cost. At most one gate touches any qubit in a clock step.
3. Compile the finite active computation into this gate set, counting every waiting location, quantum/classical ancilla, reset and interconnect use. The resource factories and full descents have predetermined padded schedules. All last bottom-level descents occur at the same prescribed time, entirely inside their local cells.
4. Immediately swap each physical result into its memory site using a constant-duration local gate, then engage the holding Hamiltonian. Include the local SWAP and its idle/switching exposure in that site's terminal Pauli channel. Reading reverses this bounded local access step and starts all base-level encoders together.

No growing decoder sidecar is placed beside every dense memory site. The growing workspace is in the paid active fabric; the active nonlocal gate set is an explicit architecture assumption supplied equally to the ordinary active comparator.

This architecture is a fully specified noisy-circuit model with local final physical coupling. It is **not** a theorem that a constant-time nonlocal gate fabric can be realized with bounded density, finite-speed communication and only short-range interactions in three-dimensional space. If physical link latency grows, its actual time and idles must be paid. Moreover, a fixed-size terminal code cell cannot simply hold a decoded qubit through an arbitrarily growing communication delay. A fully local finite-speed architecture must separately prove protected transport and synchronized arrival, or pay growing terminal workspace. Neither a polynomial routing count nor BDL bounded density alone establishes that fact.

Within the stated architecture, the majority-tree regeneration adds M=poly(N/epsilon) protected copies per output. The expanded protected workload, including those copies, then receives the usual polylogarithmic FT overhead, with the chosen code's large fixed constants and explicit interconnect charges. One must not report only the polylogarithmic overhead of the original computation. Total spacetime sums all occupied quantum and classical locations over clock steps; active time is the critical-path duration; energy sums the specified gate/reset/link costs and background loads. Mathematical gate count alone does not set those physical costs.

The elementary fault rate \(p\) is fixed independently of \(G\), memory size and requested holding duration. No protected operation is supplied as an inverse-polynomial-error physical primitive: protection is compiled from the noisy elementary gates. The nonlocal gate architecture and the independent Pauli noise law remain stated physical assumptions, not consequences of the passive Hamiltonian construction.

Ordinary active correction receives the same cells, fabric, fault rate, cooling, controller, switching, metrology and port access. It therefore obtains the same \(O(p)+\epsilon\) raw endpoint accuracy. A passive-memory consequence must concern the holding/control objective or an explicitly proved total-resource comparison; the endpoint theorem itself does not establish an advantage over active fault tolerance.

## 9. Earned scope

This note and same_code_controller_bridge.md prove the exact depolarizing-cut floor and the controller-closed Bell-refresh interface, using the static-tree theorem to remove the final old-control dependence. The natural Bell twirl gives product Pauli boundary channels with actual noisy input/output operations. The full circuit architecture specifies local final access and the paid nonlocal-control premise.

The root inverse-noise theorem supplies positivity/sampling for compensated Gibbs arrival and the forward-prefix argument for noisy read. Neither operation is replaced by an assumed thermal basin. No unrestricted hardware-noise theorem, finite-speed local3D deployment theorem, or unconditional total physical-resource advantage is claimed here.
