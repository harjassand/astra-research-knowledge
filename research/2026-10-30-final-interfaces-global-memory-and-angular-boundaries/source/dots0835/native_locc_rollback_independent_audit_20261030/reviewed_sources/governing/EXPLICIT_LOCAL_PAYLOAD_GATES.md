# Explicit local Alice-read / Bob-GPT gate modules
2026-10-30. Exact finite circuit, in the declared grouped-site native scope. No atomic quantum instrument is assumed.

Let the imported ordinary local GPT rule at hub h use m mutually commuting Pauli stabilizers S_1,...,S_m on its FULL k-resource raw-read/write footprint. Write S_j=product_(r in support S_j) P_jr, with P_jr in {X,Y,Z}; any declared fixed stabilizer sign can be applied as a hub-local bit flip. Both CSS sectors may be included since all stabilizer checks commute. Let a be Alice's m-bit read. The imported finite deterministic lookup f_h maps the relative local syndrome a XOR b to a prescribed local Pauli mask (x,z) in {0,1}^{2k}, with all tie/no-move cases defined. This is the same ordinary-GPT table whose deterministic energy properties are imported; it is not replaced by a new decoder assumption.

## Alice READ: actual ordered gates

Allocate m hub syndrome qubits b_j, initially zero. For j=1,...,m execute, in this fixed order:

1. H on hub b_j;
2. for every r in support S_j in a fixed resource order, controlled-P_jr with hub b_j as control and DATA resource r as target;
3. H on b_j.

There are L_A=2m+sum_j weight(S_j) gates. Every controlled-P is a hub/resource two-site unitary; H is onsite. The native Feynman edge for an onsite gate can be ownership-guarded with any fixed declared partner resource without increasing two-site support. Even for Y the controlled-P unitary is a specified finite matrix; no nonlocal elementary synthesis is hidden.

The full unitary takes |psi>_D|0>_b to sum_b Pi_b|psi>_D |b>, where Pi_b are the joint stabilizer projectors. The actual complete terminal reset has separate equal-rate channels for every b (and any padded workspace basis), writes HOLD(DATA(b)) to the physical Alice worker, and resets the private quantum workspace. Its instrument is exactly rho -> Pi_b rho Pi_b with classical b. Nothing coherent crosses to Bob.

## Bob SUCCESS: actual ordered gates

Allocate the same m hub syndrome qubits b plus a 2k-bit hub mask register c, all initially zero. The immutable private program P contains a, copied by the onsite LOAD instrument before acquisition. Execute:

1. the SAME ordered stabilizer-read circuit, producing b;
2. ONE explicit hub-only reversible table gate

       T_f : |a,b,c> -> |a,b,c XOR enc[f_h(a XOR b)]>;

3. for r=1,...,k, controlled-Z on resource r from c_(z,r), followed by controlled-X from c_(x,r).

This gives L_B=2m+sum_j weight(S_j)+1+2k. T_f is an explicit permutation matrix on the finite grouped hub basis: its displayed formula defines every matrix element, including nonzero input c. No quantum oracle or all-resource gate is being assumed. Its dimension grows exponentially in the fixed m,k, as honestly allowed by the grouped-site model; it is not claimed one elementary-qubit gate. The ordered X/Z phase convention is retained consistently in the Pauli mask and is irrelevant to the syndrome-based target proof except for absorbed branch phases.

The complete terminal reset resolves all (b,c,P) erased labels. On a clean source P=a, W=0, its DATA Kraus operators are

    K_(a,b)=Pauli[f_h(a XOR b)] Pi_b.

This is exactly the local Bob read/table/correction instrument used by the atomic theorem. All gates and control lengths are identical for every a, so the clean clock/rollback record is payload-independent as required. Dummy positions can pad varying hub types to the maximum fixed L.

## Native realization and explicit costs

Each listed U_t appears only as a guarded off-diagonal two-site Hamiltonian edge

    g_t |C_t><C_(t-1)| tensor U_t tensor |o_h><o_h| + h.c.,

with the resource tag projector on its actual target (or declared partner for an onsite gate). Rollback uses the exact inverse U_t^dagger and the extended claim table. No timed external unitary pulse is assumed; the time-independent Hamiltonian rail, actual reset absorber, finite monitor and actual favorable-event proof implement these gates.

Alice workspace dimension can be 2^m; Bob workspace dimension can be 2^(m+2k), and Bob program dimension is 2^m. Clock dimensions are the explicit O(kL^2+k^2) numbers in EXTENDED_MACHINE_AND_OPERATOR_PROOF.md. Outer master/worker, finite FIFO capacities, local monitor dimensions, reset-channel counts and maintained entropy export are additional fixed factors. Total apparatus size is O(N) at fixed code degree and declared graph locality, but constants may be impractical.

The imported table f_h and Tanner energy/confinement hypotheses remain mathematical inputs. What was missing physically—the finite local quantum realization, immutable program, rollback, ownership, actual outcome pointer, and abort/retirement interface—is explicitly built here. This module does not assume pre-encoded Bell DATA, elementary-qubit two-locality, a coherent shared bus, ideal noisy preparation/readout, or a hardware threshold value.

## Numerical instrument regression

`check_payload_instruments.py` tests the full gate list for commuting ZZ and XX checks on two DATA qubits, four Alice programs and every terminal syndrome label, on ALL DATA matrix columns. Maximum intended Kraus error is 1.67e-16; every inverse prefix returns the entry columns within 6.67e-16; incorrect workspace-label amplitudes are exactly zero. This verifies the local gate/instrument template, not a whole-code threshold.
