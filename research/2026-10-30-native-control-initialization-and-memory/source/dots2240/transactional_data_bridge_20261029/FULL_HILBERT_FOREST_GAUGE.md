# Full-Hilbert forest gauge: exact instantaneous DATA-instrument reduction
2026-10-29. New derivation for independent review. Uses the reset-first transactional generator in RESULT.md.

## Main finding
There is an explicit local unitary change of frame that removes **every payload unitary from every Hamiltonian edge on the full Hilbert space**, including malformed clocks and missing locks. In that frame, payload changes occur only at actual terminal/abort reset jumps and at physical noise kicks. This is stronger than selecting clock paths or bounding dirty episodes: it is an exact conjugacy of the complete generator and all its reset instruments.

The output convention is the corresponding **dressed data**. Bare physical data at an unfinished clock prefix are not the same output. The construction does not furnish an update-index noise threshold or a fault-independent schedule.

## 1. Forest gauge on one owner block
Fix a hub h and a simultaneous clock/lock-label block. Write m_r=1 iff resource r has tag o_h. During C/R(C), this own-mask is invariant until a complete reset. Edge t−1→t is present iff m_(r(h,t))=1. The C_0,...,C_L path therefore breaks into disjoint path components. For each component, put V=I at its smallest-index vertex and recursively put

   V_t(m)=U_t V_(t−1)(m)

on every present edge. On an absent edge there is no intertwining condition: start the next component at I. Put V_(R(C_t,j))(m)=V_t(m), whether or not its failed-test abort edge is currently enabled. Put V=I at every A, Q, R(A), and R(Q) phase.

Define F_h as the direct sum of these V over h's phase and the locks in R_h, acting on W_h and the payloads. This is unitary. Every nonidentity V is supported only on W_h and resources **actually tagged o_h**. It never acts on a nonowned payload. In particular V_0=I for every mask.

## 2. The global frame is local and commuting
For h≠g, [F_h,F_g]=0. Both are block-diagonal in clocks and locks. Within a block, their private workspaces are disjoint and their nontrivially acted-on payload resources are disjoint because one resource cannot have two owner tags.

Let F=product_h F_h. On a finite system this is an ordinary unitary. It is implementable as a bounded-depth local unitary circuit by coloring the bounded-degree overlap graph; depth and support size are constants. For an infinite system its action on any local observable is defined by the finitely many relevant commuting factors.

Conjugation of a bounded-support local kick K by F enlarges its support by only a constant-radius neighborhood. Indeed every F_h disjoint from the original kick support commutes with K, and because the F_h mutually commute these factors cancel before any support-growth iteration. For a CPTP kick the transformed kick remains CPTP with identical complete/diamond norm. This holds with arbitrary external reference or retained bath.

## 3. All Hamiltonian payloads disappear
Use transformed state rho_tilde=F† rho F.

* A computation edge becomes the scalar clock hop because V_t† U_t V_(t−1)=I whenever its ownership projector is nonzero.
* Its attached abort leaf has the same V and also becomes a scalar hop.
* A/Q acquisition, verification, and their abort leaves have identity owner gauge.
* An acquisition/cleanup transition of h changes only non-g labels for another owner g and hence does not change g's own-mask or gauge.
* Own cleanup occurs only in A/Q, where F_h=I. Cleanup in R is disabled, which is essential. The unconditional z_h→free reset also preserves every own-mask and every F_h.
* Clock/lock-diagonal workspace-blind monitor terms are unchanged.

Thus the transformed Hamiltonian acts on controller/monitor registers only and is exactly the original clock/ownership Hamiltonian with all U_t replaced by I. No assumption of a clean history sector enters this statement.

## 4. Exact reset instruments
Commit A_k→C_0 has identity gauge at both endpoints and is unchanged. Ready, A/Q refresh, and lock cleanup resets are unchanged. Every complete bundled loss remains scalar on workspace and is unchanged.

For a terminal reset, the transformed, separately labeled Kraus operator is

   J_tilde_(h,s)=sqrt(kappa_T) |Q_0,0><C_L,s| V_(h,L)(m).

For an abort from R(C_t,j), replace V_(h,L) by V_(h,t). For aborts from R(A/Q), V=I. In each case this is an instantaneous bounded-support DATA/workspace instrument controlled by the current local ownership mask, followed by complete workspace reset. Its sum over s is trace preserving on its source block, apart from the declared scalar jump intensity.

In a clean terminal source, m is all ones and W_h=0 in the transformed frame. Hence the summed terminal data channel is precisely

   Phi_h(rho)=Tr_W[V_L (rho tensor |0><0|) V_L†].

Retaining s instead gives the ordinary Kraus-resolved subinstrument. Clean aborts are forbidden by consistency.

## 5. Complete instrument identity, not clock-path inference
Let E_R be any unnormalized physical map associated with an actual record event R formed from the declared jump/monitor instruments. Then the transformed map is exactly

   E_tilde_R = Ad_(F†) o E_R o Ad_F.

The same identity holds before summing R, after summing any collection of events, and with arbitrary reference entanglement. No Hamiltonian excursion has been interpreted as a measured path. The transformed process has arbitrary coherent controller evolution between jumps, but no intervening payload Hamiltonian: all payload instruments occur at actual reset jumps. At a fixed finite horizon the equality remains exact provided the final output is dressed by F†.

## 6. Bounded nonideal DATA-reset count for one kick
In this frame the good-sector conditions are ordinary clock consistency plus W_h=0. The existing individual-reset no-creation argument applies by unitary conjugacy. Let H_X be the bounded set of history neighborhoods affected by a local physical kick. All hubs outside H_X stay good. Every h in H_X becomes good forever after its first post-kick terminal/abort reset, which has zero workspace and phase Q_0 regardless of mask.

Therefore one kick is represented exactly by:

* one bounded-support CPTP insertion on dressed data and local controller/workspace registers;
* at most |H_X| subsequent terminal/abort DATA instruments whose source may be nonideal;
* otherwise the exact intended Phi_h at every terminal emission, with the real coherent controller and real records retained.

The full augmented-state kicked instrument has diamond norm one; its difference from the no-kick instrument has norm at most two. The common frame preserves those bounds. The finite number of nonideal resets is not obtained by independently normalizing rare record branches.

This is an exact bounded **nonideal DATA-instrument emission** statement. The nonideal maps can share retained local controller/workspace memory with the initial insertion; they are not asserted to be independent faults. Their support is bounded. Errors propagated by subsequent clean Phi_h are ordinary circuit propagation, not extra faulty insertions.

## Remaining qualification
The scheduler/controller registers have not been discarded. They may be entangled with data after a kick and can influence the actual future order/timing of clean channels. Thus this theorem is not yet a representation by a fixed or independently sampled classical scheduled circuit with bounded-arity data-only CPTP replacements. It is an exact autonomous **quantum-controller circuit instrument** with bounded nonideal DATA emissions per kick. If the target threshold theorem accepts this retained controller and actual-order interface, this supplies its missing local semantic bridge; if not, a further classicalization/serialization theorem remains necessary.

Nor does bounded emissions per kick yield a local-stochastic bound at successful-update indices: physical waiting exposure and multi-kick clustering still need their own proof. Bare physical output additionally needs a drain or the explicit finite-depth decoding frame F†.

## Coherent-mask caution and regression
Scalar bundled reset loss means the instantaneous total intensity is independent of workspace/data for a fixed clock state. It does **not** make the global malformed clock process autonomous or data-independent. The transformed terminal unitary is controlled by the quantum mask. Offdiagonal mask coherences after tracing payload can carry factors such as Tr[V_m rho V_(m')†], which depend on rho and can affect later controller interference. No mask measurement is inserted in the proof. The clean fixed-all-owned-mask committed lemma has the stronger input-independent clock law; the malformed full-Hilbert theorem does not.

`check_forest_gauge.py` performs a five-qubit workspace/payload regression with Hadamard/CNOT gates over all 29,160 arbitrary two-hub clock configurations. It checks 18 global frame types, 70 distinct Hamiltonian conjugacies, and 72 transformed reset Kraus identities; maximum numerical Hamiltonian identity error is 4.44e-16. All commuting frame and complete bundled loss checks pass. This is numerical support for, not a replacement for, the full blockwise proof; it does not separately sample offdiagonal-mask states.

## Finite multi-kick corollary (count, not stochastic-update law)
For any specified finite sequence of local CPTP kicks with classical Poisson time/location labels, maintain a classical mark for each hub. A kick on X sets the marks in H_X; a terminal/abort reset clears its hub's mark. Initially all marks are clear and all histories good. By the individual-instrument range invariance, an unmarked hub is good on every record branch. Thus every potentially nonideal DATA reset is marked. A reset consumes its mark, and the only operation that sets marks is a kick. Consequently

   number of potentially nonideal DATA reset emissions ≤ sum_kicks |H_X|.

This holds for overlapping kicks and kicks occurring during an already marked episode; double-marking a still-marked hub cannot increase the left side. It is valid at every finite horizon, counting only emitted resets and retaining unretired marked workspace/controller memory at the final dressed interface. Adding one bounded-support dressed insertion per physical kick gives at most sum_kicks (1+|H_X|) marked insertion/emission events.

This bookkeeping is postprocessing of the actual kick and reset records, not a measurement of B_h. Conditional Poisson kick-record probabilities remain their physical-time probabilities. The bound does not assert that the induced completed-update indices are local stochastic, that marked quantum instruments are mutually independent, or that controller/data correlations can be discarded.
