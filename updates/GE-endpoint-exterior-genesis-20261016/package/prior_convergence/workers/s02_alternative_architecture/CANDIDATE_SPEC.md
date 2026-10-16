# Conserved-token, occupied-port quantum ratchet: candidate specification

16 October 2026. Independent candidate from worker s02. Status: **exact ideal asynchronous gate-history lemma at a bounded physical vertex; conditional one-level noisy interface; recursive quantum threshold NOT proved**. The construction is deliberately different from repairing a modulo update counter. Its actual execution record is a change in the occupied quantum port together with physical consumption of a one-use instruction token. Repeated Poisson proposals for the same gate are harmless on the legal sector. Identity/error-correction (EC) rounds alone are allowed to cycle through reused finite banks.

## 1. Fixed local alphabet and circuit geometry

Take a finite universal gate alphabet \(\mathcal G=\{I,H,T,\mathrm{CNOT}\}\), with the usual noncommuting \(H,T\). Compile a requested finite nearest-neighbor circuit into a directed acyclic network of constant-degree vertices. A one-wire vertex has one input port and one output port; a CNOT vertex has two of each. Physical spatial embedding uses a two-dimensional strip with one direction for wire position and the other for circuit progress; longer routing is compiled into SWAP/identity vertices. It can use area proportional to the **full circuit volume**. No polylogarithmic-space claim is made.

Each port has two reusable banks \(A,B\), each with local Hilbert space \(\mathcal H_\perp=\mathbb C|\perp\rangle\oplus\mathbb C^2\), or a fixed-size encoded realization of this logical qutrit. Exactly one bank carries an occupied data packet in a legal live port. The other is vacuum. A vertex has a physical classical program token \(g\in\mathcal G\) or the state SPENT. The token is present until that vertex fires and is then consumed; a one-shot vertex is never reprogrammed during that circuit. Program and occupancy are both local physical degrees of freedom, and their ideal update maps are fixed translations of finitely many channel types. The program pattern is part of the initial state, so the local rule does not depend on the circuit.

The rule contains no modulo phase or saved gate counter. There are independent rate-\(\lambda\) proposal clocks for gate vertices and rate-\(\mu\) EC shuttles. A gate proposal reads the current ports atomically within its constant physical support. For an encoded level, this atomic action is only an **abstract interface** and must be compiled into lower-level local moves; it cannot be assumed to occur on an arbitrarily large block in one physical jump.

## 2. Exact local quantum channel

For gate vertex \(v\) and an input-bank choice \(\sigma\in\{A,B\}^r\), where \(r=1\) or \(2\), let \(P_{v,\sigma}\) project onto: its token is \(g_v\); each required input port is occupied in precisely the bank specified by \(\sigma\); and each output bank is vacuum. Set \(P_v=\sum_\sigma P_{v,\sigma}\). On a legal acyclic rail, occupancy can arrive only from the appropriate predecessor; no remote predecessor bit is queried. For each \(\sigma\), let \(V_{v,\sigma}:P_{v,\sigma}\mathcal H\to Q_v\mathcal H\) be an isometry that:

1. applies \(U_{g_v}\) to the occupied quantum input state, including arbitrary entanglement with a remote reference;
2. moves the resulting state into the vacant output port or ports;
3. leaves both input banks in \(|\perp\rangle\);
4. changes the token from \(g_v\) to SPENT.

For \(H\) followed by \(T\), the output is \(TH\rho H^\dagger T^\dagger\), and reversing the physical vertex order is disabled by vacant-input tests. CNOT acts jointly on two occupied ports and moves both qubits. The channel for a gate proposal is
\[
\Phi_v(\rho)=\sum_\sigma V_{v,\sigma}P_{v,\sigma}\rho P_{v,\sigma}V_{v,\sigma}^\dagger+(I-P_v)\rho(I-P_v).
\tag{1}
\]
It is CPTP since \(V_{v,\sigma}^\dagger V_{v,\sigma}=P_{v,\sigma}\) when extended by zero, and the projectors are orthogonal. Its range lies in \(I-P_v\), so \(\Phi_v^2=\Phi_v\) exactly. Different bank choices may map to the same output; hence they are separate Kraus branches, not one isometry that silently forgets a bank bit. Equation (1) dephases coherences between bank choices and between enabled and disabled sectors. This is harmless for the promised legal sector, where occupation and token states are classical and definite. The data state inside the chosen occupied branch is never measured or copied.

In a physical Lindbladian, use \(\mathcal L_0=\sum_v\lambda(\Phi_v-\mathrm{id})+\sum_r\mu(\Psi_r-\mathrm{id})+\mathcal L_{\rm reset}\), where the sum runs over translated bounded-support vertex and EC channel types. The Poisson proposal times are exogenous and independent of the quantum state. The gate channel may be implemented as a finite local CPTP map at the bottom scale. At larger scales, its decomposition is the central missing theorem.

## 3. Reused EC banks and the finite transition table

An EC shuttle is an idempotent occupied-port move \(A\to B\) or \(B\to A\). It applies an encoded recovery \(\mathcal R\) before transferring the packet and leaves the old bank vacuum. Its enabled projector \(P\) requires source occupied and destination vacuum. If \(W_jP\) are Kraus operators for recovery followed by movement, with \(\sum_j P W_j^\dagger W_jP=P\) and all ranges orthogonal to \(P\), its channel is \(\Psi(\rho)=\sum_j W_jP\rho P W_j^\dagger+(I-P)\rho(I-P)\). This is CPTP and idempotent, although recovery itself need not be an isometry. Repeated proposals in one direction become no-ops; a proposal in the opposite direction starts the next EC round. Because each round is a logical identity, cycling through a finite \(A/B\) pair does not create a noncommuting history ambiguity.

| Current local condition | Ideal proposal | Result | Effect on logical data |
| --- | --- | --- | --- |
| \(A\) occupied, \(B\) vacant, gate pending or ready | EC \(A\to B\) | \(A\) vacant, \(B\) occupied | recovery, logical identity |
| \(B\) occupied, \(A\) vacant, gate pending or ready | EC \(B\to A\) | \(B\) vacant, \(A\) occupied | recovery, logical identity |
| both gate inputs live in either bank; output banks vacant; token \(g\) live | gate proposal | both inputs vacated; both outputs occupied; token SPENT | exactly one \(U_g\) |
| any gate precondition false | gate proposal | no state change | identity |
| bank certified vacant | vacuum-reset proposal | prepare \(|\perp\rangle\) in that bank | identity on live data |
| data reaches terminal output port | terminal EC proposal | continue \(A/B\) EC shuttle | protected hold, charged by elapsed time |

For one-input gates the two-input row is read with one input. If an EC proposal and a gate proposal compete, Poisson jumps are sequential almost surely. An EC jump changes the bank but leaves a live input; the gate proposal chooses its occupied bank. After a gate jump, both input banks are vacuum, so every old EC and gate proposal becomes a no-op. No lock or repaired phase bit authorizes a second \(U_g\).

The reset map must be **conditioned on the physical vacancy code sector**, not on a separate repairable flag. A reset on a genuinely occupied bank destroys unknown quantum data. A faulty vacancy decision is a data fault and cannot be excused as clock repair.

## 4. Occupancy is itself quantum-code data

For each protected bank, encode the three-dimensional logical space \(\mathrm{span}\{|\perp\rangle,|0\rangle,|1\rangle\}\) in a fixed qudit code with distance \(d\ge 2t+1\). Occupancy is the logical projector \(P_{\rm occ}=|0\rangle\langle0|+|1\rangle\langle1|\). Measuring \(P_{\rm occ}\) is nondemolition for any quantum state in the occupied two-dimensional subspace, including entanglement with other blocks. A recovery gadget must correct every error on at most \(t\) physical sites while preserving whether the block is vacant or occupied; it must not infer occupancy from a single unprotected classical bit. The qutrit code exists abstractly, and a bottom-scale bounded-support recovery channel exists as a mathematical CPTP map. A geometrically local, fault-tolerant implementation with reusable ancillas, asynchronous concurrency and universal logical gates is **not supplied by this abstract statement**.

With fewer than \(d\) local physical faults, a completely vacant encoded block cannot be turned into a *valid* independently occupied codeword by a local unitary jump; it is in a detectable/correctable sector. This protects against a single phantom packet only within the stated correctability radius. More faults can create a valid phantom or erase a packet; later collision and propagation need a separate causal-damage proof.

## 5. Ideal gate-history and service proposition

Assume (i) the network is a finite DAG with unique ownership of every live input and output port, (ii) each gate token is one-use, (iii) vacuum resets act only on vacant code sectors, (iv) EC shuttles are logical identities and leave a live input at the same vertex, and (v) the initial program and occupancy pattern is legal.

**Proposition.** Every finite fault-free Poisson trajectory that has completed all vertices applies exactly the circuit channel dictated by the DAG, for every joint input/reference state. Each vertex applies its \(U_g\) exactly once. The order of simultaneous-ready vertices is immaterial whenever they are incomparable and have disjoint quantum supports.

**Proof.** A vertex cannot fire before all occupied inputs exist. On firing, its token becomes SPENT and inputs become vacuum. It therefore cannot fire again. Unique ownership means no other vertex can remove its input while it is ready. EC shuttles preserve that readiness and are logical identities. The actual firing sequence is consequently a topological ordering of the DAG. Every legal topological ordering implements the same circuit because incomparable vertices have disjoint support. Equation (1) implements the correct channel with reference systems untouched. This argument proves actual quantum gate history, not merely classical token consistency.

After a vertex becomes causally ready, one private rate-\(\lambda\) proposal remains enabled irrespective of the number and timing of its EC shuttle proposals. Thus its clean service time is \(\mathrm{Exp}(\lambda)\) from every legal ready state, independent of exterior evolution that respects port ownership. If there are \(V\) vertices, longest dependency path length \(L\), and at most \(d_0\) choices for a predecessor at each step, a max-plus path Chernoff bound gives, for \(0<\theta<\lambda\),
\[
\Pr(T_{\rm finish}>t)\le
V e^{-\theta t}\sum_{k=1}^{L}
\bigl[d_0\lambda/(\lambda-\theta)\bigr]^k.
\tag{2}
\]
Consequently \(T_{\rm finish}=O((L+\log V+s)/\lambda)\) with tail \(O(e^{-s})\). This is an ideal *gate-service* bound; it does not erase noise accumulated in EC, token storage, or final hold.

## 6. Noisy local contract that would suffice

Use exogenous local fault clocks of total rate at most \(p\) per physical support, acting as bounded-support unitary jumps, as in [Dünnweber–Styliaris–Trivedi VII](https://arxiv.org/html/2601.20818v3). This is narrower than their synchronous non-Markovian local diamond-norm model and does not cover faulty engineered proposal channels. Assign a canonical deterministic label to each gate token, EC shuttle round, program-storage recovery round, reset, and final readout. A local fault can directly affect at most \(R\) simultaneously guarded labels, where \(R\) must be computed after physical compilation and exRec overlap.

At an abstract fixed-size ready gate, if its guard has weighted fault mass \(b\), the probability of a direct guard fault before its private clean service proposal is at most \(pb/(\lambda+pb)\). For a fixed label set, the stronger all-set estimate can follow from a stopped-exposure theorem only after the exact guards, admissions, first-fault retirements and exterior-uniform service are proved for the actual controller. Crucially, every earlier token-storage and quantum-wait interval must be represented by protected maintenance labels; it cannot be charged to a short gate interval after readiness.

A usable recursive induction would need:

* a fault-tolerant compiler of each encoded EC shuttle and encoded \(H,T,\mathrm{CNOT}\) move to a **finite DAG of lower-level one-way moves** with fixed local alphabet and no unprotected intermediary state;
* a recovery/collision rule taking any correctable occupancy or program error back to a legal single-packet state without erasing live unknown data;
* a causally convex packet lemma showing that a bad lower-level vertex, including its reset and token-consumption effects, gives at most a bounded number of bad upper-level exRecs;
* joint, input/reference-uniform CP-subchannel bounds for every fixed set of upper-level bad labels, including all random EC and program-storage rounds;
* total elapsed-time, waiting-round, final-hold and readout accounting.

None of these five bullet points is proved here. In particular, (1) on a large encoded block is not a bounded-support physical jump, and the displayed one-level \(O(p)\) estimate is not a threshold theorem.

## 7. Finite reuse boundary and safe restricted variant

The EC \(A/B\) banks are genuinely reused an arbitrary finite number of times because their repeated action is logical identity. A gate vertex and its noncommuting instruction token are used once in the finite circuit. This avoids a stale-token ABA problem and costs at least one program vertex per gate. A streaming version could transport one-use program tokens through a finite workspace by nearest-neighbor exclusion: every ideal transition either conserves a token or consumes exactly one, never copies it; a fault creates/deletes only boundedly many physical tokens; an instruction's actual application and consumption occur in the same occupied-port channel. This is a concrete alternative for reducing space, but its noisy FIFO order, encoded token repair, two-wire rendezvous, and recycling drain are unproved.

If full reuse of a gate port with finite tags is required, impose a **causal drain** before reloading it: every earlier token and message capable of affecting that port must be physically consumed or quarantined, and the occupied quantum packet must have left. A mere timeout or modulo-tag agreement does not prove this. The restricted one-shot program rail plus reused EC banks is the only portion with a complete ideal-history proof at present.

## 8. Scope against predecessors

[Dünnweber–Styliaris–Trivedi, arXiv:2601.20818v3](https://arxiv.org/abs/2601.20818v3) proves a synchronous two-dimensional QCA threshold and outlines a time-independent asynchronous Lindbladian transfer using repaired finite clocks. Its Supplement III already includes occupancy-conditioned quantum-data transport, following [Arrighi–Fargetton–Wang](https://dl.acm.org/doi/10.5555/1549637.1549652); it stores occupancy in a classical flag, explicitly to keep data faults from steering the program. This candidate instead couples protected occupancy, a noncommuting gate and physical token consumption in one map; it does not inherit the source's threshold transfer, and it takes on a new occupancy-damage burden. [Drechsler–Oreg–Aharonov, arXiv:2610.05589v1](https://arxiv.org/abs/2610.05589v1) rigorously transfers certain classical memories to periodic Floquet Lindbladians; it does not supply time-independent universal noncommuting gates. One-way gate teleportation and dissipative computation have substantial predecessors, including [Silva et al.](https://arxiv.org/abs/quant-ph/0611273) and [Verstraete–Wolf–Cirac](https://arxiv.org/abs/0803.1447). The occupied-port contract is a candidate synthesis, not an established originality or physical-capability claim.
