# Weak-initiation native controller: fast clearing repair and witness interface
2026-10-30. Construction-level claim with explicit remaining audit.

## Why simply weakening the first edge is insufficient
In the existing transactional model, replace only A0<->A1 by amplitude epsilon, leaving later acquisition/computation/reset edges fixed. The old full-alphabet terminal-reset certificate clears a consistent A_i by reversing to A0. From A1 it must cross the weak edge. Consequently its old g_min is O(epsilon), and it does not prove uniform fast activity clearing. Multiple partial acquisitions can also block one another.

## Native repair
For each acquiring phase A_i, 1<=i<k, add a distinct conflict-abort leaf R_conflict(i) through a hub/resource Hamiltonian edge conditioned on the *next* resource r_(i+1) carrying a label other than free, o_h, or z_h. Equivalently require another owner's label, including its cleanup label. Existing unexpected-own-label tests already handle o_h,z_h. The leaf has the ordinary complete on-site abort reset into Q0, with separately resolved workspace labels. Keep cleanup disabled while in every abort leaf. All amplitudes/rates of these new edges and resets are fixed positive constants.

These acquisition conflict leaves carry no DATA circuit prefix. A correctly initialized such leaf must be classified as good with W=0, not automatically as a history defect. Its reverse edge uses the same occupied-next-resource predicate. All old malformed-phase abort leaves keep their original bad status.

This adds only two-site hub/resource Hamiltonians and on-site complete resets. It does not assume a many-resource eligibility projector.

## Activity projection
In the full forest frame, call h ready only when its phase is A0, W_h=0, and none of its resources has o_h or z_h. Monitor ancillas may be arbitrary. Let P_h be the complement of this ready projector. These local projections commute. In the clean invariant range they reduce to the expected non-ready clock/lock indicators.

At epsilon=0, a ready h has no enabled acquisition edge, abort edge, or own cleanup edge, and its workspace refresh fixes W=0. Other owners cannot create h's owner labels. Thus no fast term creates P_h. All resolved complete-reset channels preserve the joint activity-block-diagonal algebra. This last statement needs to be checked against the exact chosen monitor realization and full frame; it must not be replaced by an expectation-only assertion.

## Bounded fast path without clearing a neighbor
From an arbitrary active h:

* inconsistent ordinary phase: use an existing failed-test abort and reset;
* abort leaf: take its reset;
* consistent C phase: follow its finite forward circuit and terminal reset;
* consistent A_i, i>=1: if the next resource is free, acquire it; if another owner holds it, take the new conflict abort; continue until commitment if no conflict is encountered;
* Q: clear h's own tags, verify, and use the complete ready reset;
* A0 with stray tags: abort/clean them; A0 with only dirty workspace: use complete workspace refresh.

No path uses A1->A0 or any weak edge. The length is bounded in terms of k and circuit length, independently of outside activity. The existing finite-rate clock/lock monitor projected-path method therefore has a route to a uniform p,T>0 for returning h to ready. It uses only actual monitors/resets and includes boundary-crossing terms in the norm budget. A new exhaustive transition audit has not yet been supplied for these additional leaves.

## Local fast witness from a proved return bound
If the path audit establishes

   exp(T L0*) P_h <= (1-p)P_h,

then the anchored local-polynomial telescoping construction of transactional regeneration applies with initial observable P_h rather than I. No-creation makes every exact and polynomial iterate supported in the P_h corner. Joint-block preservation makes every iterate commute all P_j. Approximation errors can therefore be bounded relative to P_h rather than I.

Finite support X_h can be chosen to obey

   c P_h<=X_h<=C P_h,  L0*X_h<=-P_h,
   [X_h,P_j]=0.

A lower integral bound follows from L0*P_h>=-nu P_h with fixed local nu, and the usual telescoping polynomial avoids multiplying an approximation error by an extensive generator norm. This is an exact fixed-support witness, not a finite-horizon drift average over the animal potential.

On the clean forest-gauge clock algebra, the X_h can be controller-only: Hamiltonian payloads are removed, and each terminal source has the full fixed ownership mask, so its completely summed reset intensity acts independently of DATA. A separate full-Hilbert controller-only statement is not claimed; malformed-mask coherences can invalidate it.
