# Two-site native strict edge-energy majority payload and clean-prefix port witness
30 October 2026. Finite payload construction and exact forest-frame witness. This is NOT a proof of native service/dirty-credit constants or of the full classical memory threshold.

## Governing sources and exact scope
This instantiates the reset-first A/C/Q architecture and full-Hilbert forest frame in:
- `producer-workspace/FULL_HILBERT_FOREST_GAUGE.md`;
- `producer-workspace/RESULT.md`;
- `producer-workspace/NATIVE_GPT_IDEMPOTENT_PAYLOAD.md`;
- `producer-workspace/NATIVE_CONTINUOUS_BRIDGE_MANUSCRIPT_V1.md`.

The code below uses only two-site hub/resource Hamiltonians and on-site complete resets in the grouped-qudit model of those sources. No high-body atomic majority reset is granted as physical hardware. The exact finite service and history matrices must be rebuilt for this gate list before importing any native-memory rate inequality.

## 1. Strict edge-energy minimizer, ignoring self-loop votes
Let v be a classical bit resource with fixed nonnegative integer vote weights w_vx. Let R_v be the DISTINCT resources in {v} union N(v); write r=|R_v|<=d+1 for the padded graph row sum d. Fix their order and let y_x be their input bits. Self-loops contribute ZERO edge-disagreement energy and are deliberately ignored by the payload rule.

Set D_ext=sum_(x!=v) w_vx and O_v(y)=sum_(x!=v) w_vx 1[y_x!=y_v]. Define

 f_v(y)=1 iff 2 O_v(y)>D_ext; otherwise f_v(y)=0,
 m_v(y)=y_v XOR f_v(y).

Thus T_v changes only y_v, using external weighted majority and RETAINING the old value on a tie. It is exactly the strict edge-energy orbit-minimizer over {I,X_v}, not merely a self-vote-majority update. A selected flip has integer energy decrement 2O_v-D_ext>=1. After a flip the opposite weight becomes D_ext-O_v<D_ext/2, so a second update is identity. If no flip is selected, the old state was already a minimizer. The rule is invariant under global bit complement and requires no stored comparison bit b.

The parent spectral activity lower bound is inherited without alteration. If a canonical wrong vertex sees a good majority in the FULL padded d-vote graph (including self-votes), the good external vote weight is >d/2 and hence >D_ext/2. That vertex is strictly edge-energy-improving under this payload. Therefore all the >=(1-c)|C| correcting-active vertices established by the full padded spectral estimate remain active. Extra active hubs do not harm monotonicity. Using the self-vote majority itself would be idempotent but need not select an edge-energy orbit minimum; that weaker rule is NOT used here.

## 2. Explicit reversible gate list
At hub h_v allocate private workspace Y=(Y_x:x in R_v) and one bit A. They all start at zero after the actual irreversible complete commitment to C_0. No additional scratch is needed. All these registers are part of ONE grouped hub qudit.

Use the following finite gate list:

1. For x in the fixed order of R_v, apply CNOT(data_x -> Y_x). The resource bit is a Z-basis control and is NOT altered.
2. Apply the hub-only Boolean permutation

       U_tab |y,a> = |y,a XOR f_v(y)>.

   This is an exact reversible XOR truth-table oracle on a fixed-dimensional grouped hub. It is a permutation on EVERY workspace input, not merely a clean workspace promise. Because all workspace qubits are one physical hub site, U_tab can be used directly as the payload unitary of one on-site/hub edge. A decomposition into elementary gates inside that site is unnecessary for the stipulated locality model. If a more restrictive internal gate model is later imposed, that is a new compilation task.
3. Apply CNOT(A -> data_v).
4. Keep Y and A. Do not uncompute Y after changing data. Reset the entire workspace only by the actual complete label-resolved terminal or abort instrument.

There are L=r+2 payload gates. On a clean workspace, the total payload has the exact basis action

 U_v |y>_R |0>_W = |T_v(y)>_R |y,f_v(y)>_W.          (1)

The intended complete terminal channel is

 Phi_v(rho)=sum_y |T_v(y)><y| rho |y><T_v(y)|,       (2)

with the untouched exterior understood. Redundant workspace labels can be included in the sum. This is a CPTP idempotent map on ALL operators, not only diagonal states: the first application measures the full local input string and changes v deterministically; the second has no further effect. For classical record storage the additional Z-basis dephasing is harmless; for a coherent record source its permissibility must be handled by the source's actual-record/common-span interface, not silently assumed.

## 3. Actual two-site native realization
For each list edge t-1 -> t use the actual ownership-checked Feynman Hamiltonian

 g_t [ |C_t><C_(t-1)| tensor U_t tensor |o_(h_v)><o_(h_v)|_(r_t) + adjoint ].

For a data-touching gate, r_t is that one actual resource. For U_tab, use a designated r0 in R_v as the ownership-checked partner, exactly as allowed in the governing GPT implementation. The Hamiltonian thus acts on the grouped hub and ONE resource, never all its locks at once.

Acquire and consistency-check ALL resources R_v before clean computation, not just the correction target. Preserve distinct A and C families, complete A_last -> C_0,0 commitment, separately workspace-label-resolved complete terminal/abort resets, failed-test leaves at every required phase/test, and reset-before-release. There is no cleanup in C or attached abort phases. Do not change the forest convention on malformed locks.

The hub has r+1 workspace bits. Its clock alphabet has O(rL+r) labels under the standard failed-test construction. Its local Hilbert dimension is at most a fixed clock/monitor factor times 2^(r+1). Each hub has r resource neighbors. Each resource belongs to at most 1+the distinct graph degree many read footprints. The total apparatus remains bounded degree with Hamiltonian body size two and on-site resets. All constants may be large, but none depends on block size or computation horizon.

## 4. Full-Hilbert forest and prefix semantics
Use precisely the source forest gauge F_C=product_h F_h. On a fixed ownership mask, each available C-chain component starts its gauge at identity; across an available edge V_t=U_t V_(t-1). Attached abort leaves use the parent's V_t; A/Q and their leaves use identity. Every U_t here is a computational-basis permutation, so EVERY forest V_t is a permutation, even on arbitrary dirty workspace and on a component that starts midway through the list.

The source's good-history projector at hub v requires the correct clock/own-lock consistency and W_v=0 in the forest frame; write B_v=I-P_good,v. In a good C prefix the own mask is full and the prefix starts at C_0. On such a prefix:

- during all extraction gates and the table gate, ALL resource bits are unchanged from canonical forest data;
- after the one final correction gate, the target v equals the strict external-majority/tie-retain answer m_v(y), and all other resource bits remain unchanged.

These are statements about the actual prefix unitary on the whole clean input subspace. They do not interpret a coherent Feynman walk as a classical clock trajectory. The physical clock can be an arbitrary superposition of prefixes; the gauge and the test observable are direct sums over those labels.

## 5. Exact instantaneous physical-port witness
Fix an analysis comparison bit b for this record. Let E_x=|1-b><1-b|_x be the canonical forest-data error projector. Let P_phys,v be the physical wrong-Z-bit projector at port v. Then

       F_C^dagger P_phys,v F_C
       <= sum_(x in R_v) E_x + B_v.                 (3)

Proof: only the majority hub whose CORRECTION TARGET is v can change v in its forest payload. Every other majority hub uses v only as a Z-control, so its gauge commutes with P_phys,v. On B_v=0, all relevant prefixes have the semantics in section4. If all canonical bits in R_v equal b, both the uncorrected and corrected physical v equal b. Thus the physical wrong projector vanishes on the joint kernel of all E_x and B_v. On B_v=1 the added term B_v pays the entire projector. Every operator in this argument is diagonal in computational resource/workspace/clock/lock labels after forest conjugation, because every forest payload is a permutation. The sectorwise Boolean implication therefore proves the Loewner inequality, including coherent superpositions of clocks, ownership masks, workspace and data. There is no branchwise conditioning or positive fault trajectory assumption.

Equation (3) can be weakened to a sum of history flags over a bounded neighborhood if a design introduces multiple possible writer hubs. For the present one-target-per-vertex majority architecture, B_v alone is sufficient.

Arbitrary dirty input is NOT assumed to obey the clean majority rule. It is paid by B_v. In particular a malformed-mask C component can start after extraction, and an arbitrary A bit can flip v: these states are not omitted from (3).

## 6. Correct use with quantum reads, and what is NOT claimed
A native quantum read operation may use the physical classical port only as a Z-diagonal control. It does not need to freeze the classical port for the Boolean implication (3). In the CLASSICAL forest frame, a read Hamiltonian controlled by P_phys,v becomes controlled by the diagonal projector F_C^dagger P_phys,v F_C, whose bad sector is bounded by (3). Its support expands only to the fixed classical read/owner neighborhood.

A clean majority prefix can therefore expose a wrong physical bit even while canonical v is correct, but only if a canonical neighbor is wrong. This is why a root-only E_v bound would be false and the finite neighbor sum in (3) is required. Rooted animal potentials may be attached to each of these finitely many neighboring roots.

Do NOT assume the actual quantum-read forest gauge commutes with the classical majority forest gauge when the two do not share ownership: a controlled-X majority prefix and a Z-controlled quantum read can fail to commute. A sound receiving route is instead to compare the actual port-controlled quantum generator to the accepted fixed-b hard-coded quantum generator, whose observable and frame act on quantum apparatus only and hence commute with F_C. This note does not prove that complete receiving inequality, but it supplies its physical wrong-port projector witness.

Nor does (3) bound delayed bad payloads by the CURRENT port error. An earlier wrong read may leave a false scratch/program token after the port heals. Such effects must be paid by the fixed-b compiler's all-controller/history Lyapunov theorem or by explicit false-token creation/consumption credit. This note only locates the instantaneous source of a read error.

## 7. Clean/dirty complete-terminal algebra
The full clean payload image in (1) is spanned by computational basis vectors. Any diagonal raw disagreement-energy observable preserves this image. Consequently its pullback by U_v has no good-workspace/dirty-workspace cross block. This is the exact complete-terminal algebra needed by the source's reset-envelope argument; one must sum the actual complete separately labeled reset instrument. No individual unresolved partial reset is substituted.

Dirty abort/terminal outputs remain arbitrary bounded-support CP instruments and require the established history-token envelope with constants rebuilt for |R_v|, the new gate list and actual clocks. The finite payload specification and inequality (3) do not themselves certify those rate/resolvent constants.
