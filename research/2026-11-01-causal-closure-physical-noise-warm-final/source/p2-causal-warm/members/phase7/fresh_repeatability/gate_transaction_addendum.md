# Exact warm-oscillator entangler and repeated Bacon–Shor transaction

This addendum supplies a useful entangling operation using the same storage oscillator and declared switchable couplings as the parity meter. It adds an **unconditional linear drive**, counts actual local gates and recovery, and uses the existing finite receiver. The forced-oscillator/qubus gate and Bacon–Shor tools are established methods. No new gate, threshold, or physical logical-error rate is claimed.

## 1. Full-loop identity with finite positive ramps

During isolated mapping, set the reciprocal readout coupling to zero and use

\[
H(t)=\chi(t)\{Z_1 n_a+\Lambda(a+a^\dagger)\},
\qquad \Lambda=\lambda_0+\lambda_2Z_2,
\qquad \int_0^T\chi(t)dt=2\pi.
\]

The unconditional term lambda0 chi(t)(a+a-dagger) is an added real actuator. All operators inside braces commute with their copies at other times, so arbitrary pulse shaping of the common envelope is permitted. Completing the square with beta=Z1 Lambda gives the exact whole-space unitary

\[
U(T)=e^{i2\pi Z_1\Lambda^2}\otimes I_a
=e^{i2\pi(\lambda_0^2+\lambda_2^2)Z_1}
 e^{i4\pi\lambda_0\lambda_2 Z_1Z_2}\otimes I_a.
\]

No oscillator preparation, reset, vacuum approximation, or Fock cutoff occurs in this identity. It holds on states correlated with all other apparatus, prior records, data errors, and external references. The isolated readout mode may undergo arbitrary data-independent free evolution; include it and its outlet in the retained memory M. The total nominal map is the stated data unitary times a memory-only map.

For lambda0=lambda2=1/4,

\[
U_\mathrm{loop}=e^{i\pi Z_1/4}e^{i\pi Z_1Z_2/4},
\qquad Z_1 S_2U_\mathrm{loop}=i\,\mathrm{CZ}_{12},
\]

where S2=diag(1,i) on data qubit 2. A physical CNOT therefore uses, chronologically,

**H2 → oscillator loop → S2 → H2**, followed by the known **Z1 Pauli-frame update**.

The two H pulses and S pulse are actual finite local operations. The S pulse cannot be discarded as a Pauli-frame correction. A more general Clifford frame would require correspondingly changing later physical controls and is not assumed here.

For chi_max=2g and two linear ramps of duration 0.1/g, the plateau lasts (pi−0.1)/g and

\[
T=(\pi+0.1)/g=3.241592653589793/g.
\]

The maximum force coefficient is chi(t)/2, hence at most g. Each of the unconditional and conditioned drive components peaks at g/2. This duration excludes local gates and the actual isolation/switching overhead. Negative chi and instantaneous echoes are unnecessary.

**Prior art:** van Loock et al., *Hybrid Quantum Computation in Quantum Optics*, PRA 78, 022303 (2008), https://arxiv.org/abs/quant-ph/0701057 , explicitly derives exact forced-oscillator conditional displacements and qubus entanglers. The present full-loop specialization is credited to that ordinary control framework.

## 2. Finite storage loss: closure is not a perfect gate

For intrinsic amplitude-damping rate kappa, let theta(t)=integral_0^t chi(s)ds and compensate both forces by

\[
f(t)=\Lambda\chi(t)e^{-\kappa t/2}.
\]

The Heisenberg solution has final initial-mode coefficient

\[
a(T)=e^{-\kappa T/2}a(0)+0\cdot\Lambda
+\sqrt\kappa\int_0^T e^{-\kappa(T-t)/2}
e^{-iZ_1[2\pi-\theta(t)]}b_\mathrm{in}(t)dt,
\]

up to the input-field sign convention. Thus the driven storage displacement closes exactly and the initial storage coefficient is the data-independent attenuation e^(-kappa T/2). This remains true with finite chi ramps.

**It does not imply data-memory factorization.** The emitted loss field and its noise transfer retain data dependence. Even the deterministic force-induced Magnus phase is changed: its coefficient is

\[
\Phi_\kappa=\int_0^T\chi(t)e^{-\kappa t}[1-\cos\theta(t)]dt,
\]

which equals 2pi only at kappa=0. Calibration can account for a known phase but cannot remove information already emitted into an unobserved reservoir. Finite kappa, imperfect isolation, control mismatch, input-field noise, and local-pulse faults belong in the physical fault expansion. A uniform probability or amplitude bound requires the actual noise and oscillator-energy model; no rate follows from this addendum.

The useful structural fact is support: throughout this gate all apparatus-mediated data dependence is on the intended pair. Any microscopic fault localized to that pair, its oscillator, and its environment propagates to an operator on those two data sites and memory only. Across two code blocks it therefore affects at most one physical site per block. A prior quantum state error retained by the oscillator does not become an uncounted new data error when the next nominal full-loop operation resumes, because that operation acts as identity on the whole oscillator space. A permanently changed control parameter is different and must be charged on each damaging use or treated as a persistent defect; the transaction below assumes no such unbounded off-gauge defect set.

## 3. Explicit two-block transaction

Use the orientation from `phase7/persistent_faults/REPEATED_MEMORY_RECEIVER.txt`: horizontal XX gauges, vertical ZZ gauges. A Pauli modulo gauge is described by an X row-parity vector x and a Z column-parity vector z. Each incoming 7-by-7 block has

\[
|x|\le1,\qquad |z|\le1,
\]

possibly at different sites, with arbitrary coherent correlations to M. This is the b=0,s=1 boundary produced by the actual previous recovery cycle.

Run 49 indexwise physical CNOTs using the loop above, then run the actual recovery on both blocks. The **one-fresh-fault budget is over the entire gate plus both recoveries and all intervening idles/local operations**, not one separately in each piece.

An ideal transversal CNOT A→B maps

\[
x_A'=x_A,\quad x_B'=x_A\oplus x_B,
\qquad z_A'=z_A\oplus z_B,\quad z_B'=z_B.
\]

Thus before a new fault the component weights obey (xA,zA;xB,zB)<=(1,2;2,1). One fresh localized fault in a gate, local pulse, or recovery adds at most one row and one column in every affected block. The worst gate case is (2,3;3,2). Seven rows and columns have repetition-decoder capacity three, so every actual uncorrupted syndrome snapshot remains decodable.

### Actual receiver and final residuals

For each syndrome axis, keep the physical basis fixed and acquire complete same-axis vectors until **two consecutive full vectors agree**, with a hard cap of four snapshots. Use the explicitly implemented adjacent-difference/minimum-weight decoder and update the Pauli frame. Restore the basis only after that axis block; do not insert fresh H pairs for each repeat. One fresh event may make its entire containing snapshot arbitrary.

At least one snapshot in an accepted equal pair is uncorrupted. Choose the last such snapshot in the proof. Correcting that syndrome removes all incoming/imported errors; only fault components occurring after that snapshot survive. Therefore:

| Location of the single fresh event | End-of-transaction residuals |
|---|---|
| No event | Both blocks have x=z=0 modulo gauge and the tracked frame |
| Event during an interblock loop or its local CNOT pulses | Both later recoveries are clean; both blocks have x=z=0 |
| Event during one block's recovery or late isolated idle | That block has at most one residual X row and one residual Z column; the other block is clean |

The conservative common output contract is again |xA|,|zA|,|xB|,|zB|<=1. It is therefore composable with another identical transaction. The incoming residual plus a newly imported residual plus a fresh fault are all charged. The proof uses error-family linear spans with operator coefficients on the full memory, so it does not replace M by vacuum or introduce independent fault coins.

Physical gauge-only semantics must hold during completed, idle, and basis-change intervals. In particular, nominal hot dispersive links are actually off during the required local H/S operations unless their remaining action has separately been proved gauge-only. The extra switch and its imperfections are real resources/faults.

The single-fresh-event contract is the consumer's **one-row/one-column support contract**, not every conceivable physical failure. For example, a common switching failure that leaves both participants of an intra-block module coupled during a nongauge H interval can produce two off-gauge sites. Without a further algebraic reduction, old two plus new two needs capacity four (for example, a 9-by-9 block), not the seven-by-seven bound proved here. Similarly, a shared pulse failure across an entire block is not a local single-site fault. Such events must be counted with their actual support or bounded in the physical failure term. The interblock gate's two-site support is safe because the two sites belong to different blocks.

A corrupt general classical decoder or Pauli-frame register can prescribe many wrong corrections; it cannot simply be relabeled a one-site fresh fault. Retain the consumer's explicit controller-failure budget or implement protected classical registers/logic. No perfect final flag, decoder, or terminal decision is assumed. This is the same ordinary issue identified explicitly by AGP, https://arxiv.org/abs/quant-ph/0504218 .

## 4. Actual single-qubit preparation and terminal readout

### Finite measurement followed by a real conditional X

The 49 physical zero preparations are themselves implemented by the same apparatus; no ideal physical reset is supplied. For one qubit, switch off its module's second participant's conditioned force and use the already charged unconditional drive:

\[
H(t)=\chi(t)Z n_a+\lambda\chi(t)e^{-\kappa t/2}(a+a^\dagger),
\qquad \theta(T)=\pi.
\]

The final affine storage map is

\[
a(T)=-e^{-\kappa T/2}a(0)-2\lambda e^{-\kappa T/2}Z
+\text{input-field noise}.
\]

Use the finite bracketed pre/post receiver that nulls the initial a,m response columns. Its earned selected-mode factorization gives a pure pointer conditioned on Z when **all fresh input fields are vacuum**, including at finite kappa. All remaining data dependence W_z is in Alg(Z), precisely the observable being measured; loss-induced Z information is therefore compatible with this measurement. The exact finite-kappa vacuum theorem is distinct from the separately established kappa=0 homogeneous-thermal theorem. No finite-kappa thermal or unequal-temperature-port factorization is asserted here. Imperfect input-state or control conditions remain in their actual physical error budget.

Let the actual coarse-grained receiver instrument obey the proved constant-weight CP decomposition

\[
\mathcal M_r=(1-e)\mathcal G_r+e\mathcal B_r,
\quad
\mathcal G_r(\rho)=(P_r\otimes W_r)\rho(P_r\otimes W_r)^\dagger,
\quad P_r=(I+rZ)/2.
\]

The sum over r of each normalized instrument is trace preserving; W_r may act on all retained memory and unobserved outputs. This is a genuine projective good component. For symmetric pure pointers its weight is obtained from the outcome Gram matrix: if epsilon is the classification tail and c the overlap integral over one outcome region, then e=epsilon+|c|^2/epsilon is valid for epsilon>0. Subtracting the good projector leaves a positive semidefinite matrix. The CP bad weight e must not be replaced silently by the smaller raw classification tail epsilon.

After reporting r=-1, apply an **actual finite X pulse**; after r=+1, do nothing. With nominal feedback the good component is exactly

\[
(1-e)|0\rangle\langle0|\otimes
\sum_{r=\pm1}W_r\langle r|\rho|r\rangle W_r^\dagger.
\]

Thus every input, including arbitrary qubit-memory-reference correlations, becomes a prepared zero tensor arbitrary junk in the good branch. The bad component retains weight e uniformly over that input. The good/bad labels are a CP analysis decomposition, not supplied perfect flags; the actual controller uses only the reported r. No apparatus reset is performed. Faults in the conditional X pulse or its classical control are additional actual faults. A local Z phase from the mapping does not require a compensating pulse here: it is scalar on each measured eigenspace. A physical plus preparation adds a real H pulse after this zero-preparation primitive.

### Preparing the encoded block

Apply this finite measurement-and-feedback primitive to all 49 qubits. In the all-good component their joint state is |0>^49 tensor arbitrary retained memory. One localized bad preparation component or X-pulse fault affects one physical site; all good preparations erase their own input correlations exactly. Then perform the actual noisy horizontal-XX gauge-projection block using the same temporal receiver and its Z-component frame correction, followed by the vertical-ZZ block and X-component correction.

The all-zero product has all Z-type stabilizers and logical Z equal to +1. Its initial X-stabilizer syndrome can be arbitrary: any complementary logical-Z ambiguity in the first correction acts trivially on the known logical-zero state. Under at most one localized event across all 49 preparations, feedback pulses, and the whole projection/recovery procedure, the result is logical zero with the same at-most-one-row/column residual boundary. The finite CP bad components are charged, not suppressed by declaring a weak measurement projective. Logical plus uses the axis-dual construction with the actual H-based physical-plus primitives.

### Terminal measurement

For terminal logical Z, use the same finite single-qubit Z instrument on every qubit, without conditional reset, then form seven row parities and their majority. The same CP tags account for the physical readout errors. In the code all row parities equal the logical value; an incoming residual affects at most one row and one additional localized measurement event affects at most one more. Seven-row majority therefore succeeds within this budget. Logical X uses actual H pulses, the same Z instrument, and column parities. A physical failure of the classical parity/majority network remains separately charged or its output remains a protected classical block.

These are standard measurement-and-feedback preparations and subsystem readouts using the earned apparatus/receiver, not encoded ancillas or noiseless physical preparations supplied for free. Aliferis–Cross, *Subsystem Fault Tolerance with the Bacon-Shor Code*, PRL 98, 220502 (2007), https://arxiv.org/abs/quant-ph/0610063 , is the primary gauge-extraction and recovery precedent.

### Reusing existing modules: an explicit orientation

The 7-by-7 grid has 84 horizontal/vertical gauge edges. Assign each edge's dispersive participant to be its directed source. Orient the four-cycle (0,0)→(0,1)→(1,1)→(1,0)→(0,0). Every other vertex chooses one edge toward that cycle: if row>=2, point to (row-1,column); otherwise point to (row,column-1). These choices form a forest directed toward the cycle. Orient all remaining edges arbitrarily.

Every one of the 49 vertices is the source of its own chosen edge, and all 49 chosen edges are distinct. Its chosen module therefore performs that qubit's single-qubit measurement with the other participant's conditioned force off. All 49 can be used in parallel under the corresponding isolation/locality contract. No new graph edges or quantum modes are needed. The added resource is unconditional-drive capability on **49 of the 84 existing modules per block**, plus the already declared isolation controls. The orientation is a hardware design/assignment condition; an already fabricated incompatible source assignment cannot be reversed by a software label. Without suitable sources or real routing, provide **49 additional preparation/readout modules per block** instead.

`preparation_module_assignment.json` records all 84 directed edges and the 49 selected source modules. The executable verifies the distinct-source property directly, without graph search.

## 5. Resource ledger and exact checks

- Two 7-by-7 blocks: **98 data qubits**.
- Transversal entangler: **49 oscillator loops**, **98 physical H pulses**, **49 physical S pulses**. The known product of Z updates can be stored as a logical/control Pauli frame.
- Both recoveries: **196 further physical H pulses** and at most one known phase correction per meter use.
- Path-gauge snapshots: **42 meter uses per full same-axis snapshot**. Two clean recoveries use **336** meter calls. With one fresh event in the whole transaction, the worst total is **420**. The unconditional hard cap is **672**.
- Dedicated implementation: **168** intra-block gauge modules, plus **49** interblock pair modules if those couplings are supplied by dedicated apparatus. If each is the two-mode meter architecture, this is **434 apparatus modes**. Existing intra-block gauge edges do not automatically supply interblock indexwise couplings. Sharing/routing requires an explicit hardware and fault-support contract.
- Preparation/readout can reuse **49 of the 84 existing gauge modules per block**, so the oriented construction adds no apparatus modes; it does add unconditional-drive capability to those modules. A block preparation uses **49 single-qubit meter calls**, up to **49 conditional X pulses**, and the gauge-projection/recovery procedure: **217 total meter calls** when clean and at most **301** with one fresh event over the complete preparation. Physical-plus primitives add **49 H pulses**. Terminal Z readout uses **49 meter calls**; terminal X also uses **49 H pulses**. These preparation/readout costs are not part of every CNOT transaction unless the computation actually performs them.
- Fully serial mapping alone costs **49(pi+0.1)/g = 158.838040025/g**; 49 genuinely parallel pair modules reduce the loop portion to (pi+0.1)/g. Neither figure includes local gates, recovery, switching, or controller latency.

`verify_gate_transaction.py` verifies the two-qubit CZ/CNOT phases; integrates the finite ramp response for kappa=0,0.01g,0.2g; checks 1,792 component propagation cases; and runs **59,392** adversarial histories of the actual cap-four temporal receiver with arbitrary incoming weight at most two. Every checked history is unflagged within the promised budget and leaves either zero or the new one-component residual. It also verifies the 49-source grid assignment and the positive-semidefinite CP subtraction for four finite pure-pointer examples. The exact whole-oscillator identity and general CP statements are derived analytically, not asserted from truncated Fock numerics. Results are in `gate_transaction_results.json`.
