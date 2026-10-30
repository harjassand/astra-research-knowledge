# Exact physical-edge / canonical-edge witness for majority forest prefixes
30 October 2026. Finite-payload lemma supplementing `NATIVE_MAJORITY_PAYLOAD.md` (frozen payload SHA256 `65cecd2d3d67b1f4da5a21877c8432209c2e635d4944ad8d39899b630216d614`). No previous source is overwritten.

## 1. Statement
Use exactly the strict edge-energy-minimizing payload, one writer hub h_w per classical resource w, full-Hilbert ownership-mask forest F_C, and good-history projectors P_good,w=I-B_w specified in the payload note. Resource read gates use computational Z controls; only h_w's final conditional-X gate writes resource w.

For a nonloop physical graph edge e={u,v}, let S_e^phys be its physical disagreement projector. In canonical forest coordinates let S_f be the disagreement projector for edge f. Let

 J(e)=Star(u) union Star(v),

where Star(w) is the set of nonloop positive-weight graph edges incident to w. Use either all graph edge labels or one representative per distinct parallel-edge support; in the latter convention choose the same representatives for the right-hand side. In particular e or its representative belongs to J(e). Then

 F_C^dagger S_e^phys F_C
 <= sum_(f in J(e)) S_f + B_u+B_v.                 (E1)

This is a Loewner inequality on the ENTIRE controller/workspace/data Hilbert space, with an arbitrary reference and retained bath. It does not condition on measured clock trajectories. Its constants and support are independent of record-block size. For a loop e={u,u}, the left side is identically zero.

## 2. Only the endpoint writer forests matter
For w not in {u,v}, F_w commutes with S_e^phys: its sole possible data-target update is on w, whereas u and v can enter its gate list only as Z controls. Hub-only table gates also commute. The governing forest factors mutually commute because their nontrivial resource actions are restricted to actual owner tags. Consequently all nonendpoint factors cancel in F_C^dagger S_e^phys F_C.

Likewise, for the bit-Z observable at an endpoint,

 F_C^dagger Z_w F_C = F_w^dagger Z_w F_w.

This cancellation is on the full ownership-mask direct sum, not an assumption that two overlapping clean computation phases can both own the same resources. Indeed such simultaneous ownership is forbidden by the physical owner labels. Missing-lock path components retain the source's forest-start-at-identity convention.

## 3. Exact diagonal parity identity
Every individual gate in the payload is a computational-basis permutation on arbitrary workspace. Hence all forest factors are permutations on each clock/lock block, and all transformed bit/disagreement projectors are diagonal in the common canonical computational/workspace/clock/lock basis.

On each such basis label define c_w as the Boolean difference between the physical output bit at w after the full forest map and its canonical input bit. This definition is valid even on dirty histories. The exact identity is

 sigma_e^phys = sigma_e^canon XOR c_u XOR c_v.       (E2)

No update ordering is inferred from (E2). It is simply the parity identity for the simultaneous full-forest unitary evaluated on a basis label.

On B_w=0, the prefix semantics from the payload note apply:
- before the single final conditional-X, c_w=0;
- after it, c_w=f_w(y), where f_w is the strict edge-energy-improving flip decision evaluated on the CANONICAL resource input string y;
- on the identity-gauge good A/Q phases, c_w=0.

If all canonical incident disagreements S_f, f in Star(w), vanish, every positive-weight external neighbor equals canonical w. Then its disagreement weight O_w is zero, so strict improvement cannot select a flip. Therefore, as a Boolean implication on good histories,

 c_w=1 => there exists f in Star(w) with sigma_f^canon=1.

On bad histories no such implication is assumed; B_w pays the exception. This is important for a missing-lock component that starts midway through the list or for arbitrary dirty A/workspace values.

## 4. Proof of the operator inequality
If every right-hand-side projector in (E1) is zero, then canonical sigma_e=0, both endpoint histories are good, and every canonical edge incident to either endpoint has zero disagreement. Section3 gives c_u=c_v=0. Equation (E2) then gives physical sigma_e=0.

Thus physical edge occupancy implies the Boolean OR of the bounded canonical edge set and the two endpoint history flags. Since the observables are simultaneously diagonal, the Boolean OR is bounded by their ordinary sum and yields (E1) as a full operator inequality. No classical-noise probability model or diagonal input-state assumption is used: the inequality holds when tested against arbitrary coherent states.

One could derive a looser sum with sigma_e counted three times by separately bounding c_u,c_v; the kernel argument above removes this unnecessary multiplicity.

## 5. Multiplicity, geometry, and limits
The footprint J(e) has at most 2d distinct check labels (or fewer after merging parallel supports). Each canonical edge is a possible witness for only a bounded number of physical edges, and each writer-history flag B_w witnesses only the bounded star at w. These are the finite overlap constants required for an animal completion or local-OR transfer.

A physical multiedge disagreement is the same Boolean projector for each parallel label. Repeating the inequality for those labels adds a fixed multiplicity factor. Self-loops never contribute an occupied disagreement check. No graph edge connecting arbitrary distant noise partners is introduced by this lemma.

The lemma is stronger than a wrong-bit witness for this purpose: it depends only on local disagreement checks and dirty writer histories, not on an externally chosen raw-record bit b or on an entire error component.

It supplies a necessary local ingredient for comparing a physical-data rooted potential before destructive controller reset to a stronger old native potential. It does NOT by itself establish the full weighted-animal inequality: that step still needs explicit connected completion, root preservation, witness congestion, history-token multiplicity, and theta/exponent margins. Nor does it prove the scheduled reset or growth operation noise-free. Physical data are unchanged by a bare controller reset, but the forest-coordinate data can change, which is precisely why the physical-to-canonical comparison must be made before erasing the controller state.

## 6. Noncommuting external readers
Only the classical majority forest is used here. A quantum read operation that uses the physical port as a Z control need not share a lock for (E1) to remain an instantaneous observable identity. This does not make an actual quantum-read forest commute with the classical forest. A joint native receiving proof should use the previously identified fixed-baseline quantum comparison or separately establish its frame/ownership algebra. Delayed bad programs must still be priced by history/token credits rather than current edge occupation.
