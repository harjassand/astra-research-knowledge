# Independent full-Hilbert forest-gauge audit
2026-10-29. No publication. Source snapshot hashes: SOURCE_SHA256.txt.

## Verdict
The full-Hilbert gauge and exact retained-quantum-controller DATA-instrument compiler are valid for the specified reset-first transactional generator. I found no algebraic counterexample. They are stronger than the earlier episode count, but do not by themselves prove a DATA threshold or an input-independent classical scheduler.

This verdict assumes the fixed finite circuits, bounded neighborhoods and degree, complete label-resolved overwrite resets, distinct abort leaves, ownership check on every gate (including hub-only gates), and no cleanup in any R phase. Removing those premises invalidates parts of the proof.

## Transition-level audit
For a fixed own-mask, deleting missing-ownership edges leaves a forest. Define V at the leftmost vertex of each segment to be identity and recursively multiply the gate along each present edge. Copy V onto each attached abort leaf. A/Q and their abort leaves have identity gauge. Every product acts only on private W and actually owned DATA. The statement holds for arbitrary, including malformed, masks.

1. Computation: V_destination^dagger U V_source=I on every enabled edge. A hub-only gate is still ownership-gated, so precisely the same identity applies. It cannot be treated as unconditional after a missing lock.
2. Abort: its two endpoints have exactly the same V. Whether the failed predicate is enabled does not affect the intertwiner.
3. Acquisition/cleanup: the transitioning owner's gauge is identity in A/Q. Every other owner's mask is unchanged by free↔o_h or o_h↔z_h. Hence these transitions commute with all other frame factors. Disabling R cleanup is essential.
4. z_h→free: neither label is usable ownership for any owner. All frame factors are unchanged, even when h itself is in C/R.
5. Commit: A_k and C_0 both have identity gauge for every mask, including malformed sources. Workspace overwrite does not introduce a gauge correction.
6. Ready and A/Q workspace refresh: identity owner gauge and unchanged other gauges.
7. Terminal and C-abort: their transformed individual Kraus operators are K_s V_source. Source-mask control is coherent. All other owners' factors cancel, and Q_0 has identity owner gauge.
8. Loss: summing the separately labeled complete workspace-overwrite Kraus channels gives the source-phase projector tensor I_W. It commutes with the frame. Thus the no-jump generator has no hidden DATA dependence. Omitting the s=0 self-loop from an overwrite bundle, or coherently summing s, would require a new calculation and is not covered.
9. Workspace-blind clock/lock monitors commute with the frame, including coherent monitor couplings diagonal in those labels. A different monitor interacting with W is not automatically covered.

## Global frame and local faults
The factors commute as operators, not merely after sampling masks: they are diagonal in the shared lock controls, and within each control block the nontrivially addressed DATA sites are disjoint. The combined frame is a bounded-depth finite-range unitary by bounded-degree coloring.

For a local physical Kraus operator K_X, factors disjoint from X commute with K_X and commute with all other factors, so they cancel from F^dagger K_X F. Only the union of the original intersecting factor supports remains. There is no iterative support-growth chain. The same conclusion applies to the local CPTP map with a retained reference/bath.

The output identity is exact at every finite horizon when both the input and final output are transformed consistently. For physical clean A/Q initialization the initial frame is identity; arbitrary initialization requires applying the initial frame explicitly. Bare physical DATA mid-computation are not dressed DATA. An explicit final bounded-depth F^dagger decoder, or an independently justified drain, is required for that interface. A drain has no deterministic finite completion deadline merely from finite reset rates.

## Off-diagonal and reset-record issue
A diagonal-in-mask gauge does NOT measure/dephase the masks. For source controls a,b an off-diagonal block evolves through a reset as

    rho_ab -> sum_s (K_s V_a) rho_ab (K_s V_b)^dagger.

This identity is the exact conjugate of the physical reset, including arbitrary reference entanglement. Replacing it by a classical mixture retaining only a=b generally changes the map. An actual-record event remains an unnormalized CP map; one may sum or coarse-grain events, but not divide by their probabilities and retain an unconditional norm estimate.

## Exact retained-controller decomposition: yes, with a restriction stated
On the good h sector in the dressed frame, W_h=0 and a terminal source has all h locks. Restricting its terminal Kraus operator to that source gives

    (controller source projection and C_L→Q_0 transition) tensor <s|V_L|0>_DATA.

Consequently, after summing syndrome labels s, that event map is the controller transition tensor the intended Phi_h, even when the input DATA are entangled with the controller. Retaining s gives the corresponding intended Kraus-resolved instrument instead. Between reset events the Hamiltonian, monitor operations, and full no-jump loss terms are controller-only. This proves the exact augmented-controller instrument decomposition without an independent schedule assumption.

A kick and every marked terminal/abort can instead be retained as a bounded-local operation on DATA plus controller/workspace. Once the first terminal/abort reset following the most recent contaminating kick puts a marked hub into Q_0, its workspace is zero and its good sector is invariant until another relevant kick. Thus the one-kick bound and the finite multi-kick charge to preceding kicks are structurally consistent. Fault maps may share quantum memory; they are not independent replacements.

This decomposition does not imply that a malformed controller has an autonomous DATA-independent marginal law. Its coherent controlled DATA-reset instruments can transfer DATA correlations into controller coherences. Actual reset order/timing and syndrome records must remain in the augmented instrument unless a justified coarse-graining is proved.

## Independent numerical evidence
check_blocks.py is independently written, not copied from the author's test. It uses two hubs sharing two resources, five possible labels per resource, 14 phases per hub, private qubit workspaces and two DATA qubits. The three noncommuting gates include an ownership-gated genuinely hub-only rotation. It checks 36,810 matrix identities: frame commutation/unitarity, computation, abort leaves, acquisition, cleanup, unconditional z reset, commit, individual reset formula, and complete losses. Maximum residual: 4.45e-16 (rounding up).

An explicit coherent superposition of two ownership masks, including an external qubit reference, compares the full conjugated terminal channel to the controlled formula. Residual: 2.81e-17 (rounding up). The output off-diagonal mask block has Frobenius norm 0.35468: dephasing masks would therefore fail this test. JSON results are saved. This is a finite regression, not a proof for arbitrary architectures; the algebra above supplies the general argument.

## What remains before a DATA threshold
- A specified fault-tolerance theorem for a retained quantum scheduler/controller, or a separate reduction to the classical/adaptive circuit interface that the chosen theorem actually accepts.
- Joint multi-witness probability/norm estimates. An exact local instrument decomposition does not prove factorized local-stochastic probabilities at completed-update indices. Normalizing record branches is especially dangerous.
- Physical waiting/storage exposure and finite-rate coverage/healing bounds for this changed one-way-commit architecture; earlier reversible healing paths cannot be imported unchanged.
- Multi-kick clustering and correlations between long-lived marked controllers and future update opportunities, with uniform bounds rather than only a finite emission count.
- A finite-horizon logical output/decoder convention and its fault accounting.
- Thermodynamic implementation assumptions remain driven-reset assumptions; the gauge establishes no passive equilibrium or finite-fuel lifetime result.

These are threshold-level obligations, not counterexamples to the exact conjugacy.

## Exact-version receipt: retained-controller note
At 2026-10-29 22:34 UTC I read the complete current bytes of
`producer-workspace/RETAINED_CONTROLLER_DATA_DECOMPOSITION.md`.
Its SHA-256 is appended to SOURCE_SHA256.txt. The note's good-source restricted operator identity, syndrome coarse-graining distinction, controller-only no-jump maps, local kick support, finite marked-emission count, and finite-record CP/TNI caveats agree with this independent audit. This is an exact-version acceptance of that instrument decomposition, not an acceptance of a DATA-threshold theorem.
