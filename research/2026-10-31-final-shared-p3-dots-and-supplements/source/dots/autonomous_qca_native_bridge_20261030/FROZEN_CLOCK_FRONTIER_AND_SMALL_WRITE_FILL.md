# Frozen clock frontier and a bounded-hole small-write fill

Status: exact local algebraic/semantic components for a prospective purge compiler. The creation, recovery and merging of arbitrary corrupted purge epochs are NOT supplied here. This does not close the whole asynchronous theorem.

## 1. Update-overlap graph and actual guard

Use a graph whose vertices label attempted QCA update channels Φ_h. Vertex h has its own κ_h∈Z_q, q≥4, and only Φ_h increments κ_h. An edge joins any pair with overlapping quantum DATA footprints (and every additional dependency required by the buffered classical rule). Every accepted ordinary update checks that its incremented clock remains within0,±1 of every neighbor. Guards and conditional channels are evaluated after native acquisition of the whole read/write footprint, not from an early unlocked snapshot.

A finite set F is frozen: its clocks do not change during the interval. Its DATA and internal controllers may undergo arbitrary dynamics, retained-bath couplings, or erasure. All other ordinary channels obey the genuine marching guard. No repair or fault writes a boundary clock during this particular comparison interval; such writes must instead split the interval and be charged as additional marked events.

For h adjacent to f∈F, the permitted residues after an increment lie in the three-element consecutive arc {κ_f−1,κ_f,κ_f+1}. Starting at any residue, there are at most3 successive accepted increments before the next increment leaves that arc. From an initially valid incident edge the bound is2. Therefore

    # accepted ordinary channels in N(F) during the whole interval
       ≤3 |N(F)|.                                  (1.1)

This is pathwise and independent of elapsed physical time, total lattice size, or clock modulus q≥4. A count of native SUCCESS attempts is not substituted for accepted ordinary increments: identity-rejected attempts do not increase the left side.

## 2. Quantum boundary-port consequence

Let D_h be the fixed DATA footprint of Φ_h. Channels whose vertices are outside F∪N(F) have DATA footprints disjoint from ∪_(f∈F)D_f. Thus arbitrary dynamics in F can communicate with the good exterior only through:

* the initial/final DATA wires in D_F=∪_(f∈F)D_f;
* at most3 accepted boundary-channel occurrences for each h∈N(F).

Keep those boundary occurrences as open tensors, together with every internal arbitrary operation and the retained bath. The number of quantum input/output legs is bounded, conservatively, by

    2 |D_F| + 6 Σ_(h∈N(F)) |D_h|,                  (2.1)

with the appropriate fixed local Hilbert-space dimension per leg. The boundary tensor may be a correlated retained comb, not an ordered family of independent gate faults. The exterior operations remain the exact specified channels; downstream propagation of a bad boundary input is ordinary circuit propagation, not a new fault at every affected output.

Equation(2.1) is a structural open-network statement. Its use in an error norm requires the common decoder/open-tensor correctness and the global signed Boolean norm bookkeeping; see the separate `asynchronous_quantum_causal_cut_20261030` work. It is NOT a bound on the norm of an arbitrarily postselected or normalized boundary process.

Nominal bath-only evolution adds no DATA crossing. Actual perturbations coupling the bath to further physical sites are separately charged at their physical supports; a common bath is not asserted to be a fresh independent channel. Native in-flight prefixes straddling the freezing event must first be included in the finite leading rectangle, not ignored by a new guard.

## 3. Exact bounded-hole fill with a globally frozen collar

Fix once and for all a finite target set H and its full incident collar C. This radius must be chosen before the code/synchronization scale M. Clocks in H can carry an erased symbol ⊥. Suppose:

(A) the entire collar C and every already filled clock in H are frozen until the last ⊥ in H is filled;
(B) the current prescribed numerical clocks in H∪C admit a1-Lipschitz extension through all ⊥ sites;
(C) all quantum DATA and current/old control buffers at erased sites have actually been reset or are explicitly treated as arbitrary internal inputs to the boundary tensor.

For each x∈H, define a separate attempted channel. It reads H∪C nondestructively. If x≠⊥, act as identity. Otherwise solve the finite constraint problem with every currently numerical clock prescribed, choose one complete feasible extension by a fixed deterministic tie-break, and write ONLY the value at x. All other clock labels are unchanged. The actual channel pinches the clock read registers; arbitrary bath/reference correlations remain in the output instrument.

Every successful fill reduces the number of ⊥ symbols by1 and preserves (B), since the chosen full extension witnesses feasibility after its single write. Any order of successful fills therefore terminates after |H| fills with a valid numerical clock field. Native ownership serializes overlapping snapshots. The small-write/read-only compiler implements each channel using two-site Hamiltonians and onsite resolved resets; a fill-hub fault cannot change the populations of the other read-only clock labels.

The freeze condition is GLOBAL TO H: a single remaining ⊥ keeps every relevant boundary clock frozen. A merely nearest-neighbor guard is not an adequate replacement, because a moving exterior can invalidate the remaining constraint problem during sequential fills.

## 4. What an actual isolated-root rectangle would still need

The maximal-relaxation lemma supplies (B) at a bounded radius when the exterior frozen-boundary range is controlled. A proposed isolated-root protocol can inspect for a feasible boundary, set a genuine freeze/epoch flag while holding the whole read footprint, purge H through independent single-site writes, then execute §3 and release only after full validity.

However, arbitrary corruption of that epoch flag can prematurely end a partial purge. A whole implementation must retain actual boundary-freeze latches, deal with orphan ⊥ labels and overlapping beacons, and prove that their recovery does not enlarge the write radius with M or with the code's required fault count. None of that follows from §3. Nor does an ideal classical CSP solver license a large atomic physical update: its finite table must use the explicit read-only/small-write native realization.

Long physical waiting contributes a separate noise-exposure budget. The finite port count bounds nominal quantum communication across the frozen frontier; it does not suppress physical bath noise accumulated on its internal DATA. That exposure must enter the actual marked-box norm bound using the full finite waiting duration.
