# Independent audit: deterministic actual-measurement cells

Date: 2026-10-15. Read-only mathematical audit of DETERMINISTIC_MEASUREMENT_CELL_COROLLARY.md and ../deletion_null_detector_bridge/DETECTOR_SUBSET_AUDIT.md. No experimental data were opened and neither reviewed file was modified.

## Verdict
**PASS under the stated common-dilation, exact/protected measurement, complete perturbation charging, exogenous scheduling and full-reservation support assumptions.** Shared boundary records do not invalidate deletion-nullness. The full-input cell-effect product and the parent-OR union bound are valid without private frames, independent baths, independent outcomes or Markovian dephasing. The completion/common-decoder conclusion additionally requires the full-footprint stabilizer condition and the earlier support/geometry theorem; it does not follow from the probability estimate alone.

The explicit numerical check below validates the effect statements on the entire eight-dimensional input space, not merely a prepared syndrome sector or chosen bath state. It does not by itself check a nontrivial encoded-memory/common-decoder theorem.

## 1. Deletion nullness with shared boundary outcomes
At every actual boundary, retain the exact classical outcome in a protected register. The first outcome is actually acquired, or is a fixed trusted truth-table prediction from an exact premeasurement and exact intended correction. For cell c=(i,l), the predicate compares its own actual entering and exiting records, u_(i,l−1) and u_(i,l).

Set the scalar multiplier of **all** charged perturbations in that cell to zero, leaving measurements, schedules, record initializations and predicates unchanged. If every remaining operation preserves G_i throughout that cell, its ending outcome must equal its entering outcome on every branch. This is true for every input, including memory–bath entanglement, and for arbitrary real values of every other interpolation parameter. An earlier error can change both the actual entering label and the later label of this noiseless cell; it does not make the deleted cell bad.

Adjacent predicates share u_(i,l), but are diagonal in the same protected record basis. Hence they commute. Later operations may act on memory/bath, but must not rewrite the evidence or change the fixed truth-table predicate. This establishes Q_c U_(z_c=0) W=0 as an operator identity in the common dilation. It would fail if later cells compared against a stale original label, the expected correction used an untrusted wrong internal decision, a boundary measurement were only hypothetical, or the records/comparison themselves could be corrupted.

The measurement channel has a parameter-independent unitary dilation with fresh record ancillas. Summing unnormalized complete-record Kraus effects is equivalent to evaluating the commuting final projectors in that dilation. No conditional normalization or postselected small-error assumption is used.

## 2. Joint cell effects and parent union
For selected cells C, multivariate finite differences annihilate every interpolation vertex except the all-present vertex. Repeated Duhamel differentiation inserts every selected V_c once. Its chronological insertion-order simplices partition the full product of insertion times, giving norm at most product_c a_c with no factorial cost. Projection and the fixed initial isometry are contractions. Squaring proves

  F_C ≤ (product_c a_c²) I

on the entire allowed input domain. Overlapping cell times for different parents are permitted; the support assumptions are needed for deletion-nullness, not for an independence assertion.

For parent i, b_i is the OR of its actual completed-cell predicates. For distinct selected parents R, their joint OR event is contained in the union over choices of one failed cell per selected parent. Since these are commuting classical events, this is a positive-operator union inequality before pulling back through the channel. Applying the cell bound and summing gives

  F_R ≤ product_i [sum_l a_(i,l)²] I.

The factorization here is ordinary finite distributivity of the positive scalar sum, not statistical independence. Each one-cell-per-parent choice is a set of distinct cells, so the underlying lemma applies. Per-parent caps at one are obtained by dropping those parent constraints from the event and applying the already-valid bound to the retained subset; no modification of the physical dynamics is required.

With ||V_i(t)||≤J_i and fixed total weak-noise time tau_i divided into M_i equal cells, sum_l a_l²≤J_i² tau_i²/M_i. For a general prescribed partition the bound is J_i² sum_l Delta_t_l². Equal cells minimize that upper expression at fixed M_i and tau_i. This concerns a bound, not monotonicity of the actual physical error as the schedule changes. No factor counting stabilizer generators is needed because each cell predicate is a single joint-syndrome mismatch event.

## 3. Separate support/common-decoder obligation
The sufficient footprint requirement is

  Pauli(A_i) ∩ Centralizer(G_i) ⊆ phase × S_code,

with G_i a commuting subgroup of the code stabilizers. It must cover the entire accumulated data/noise/correction footprint, not merely individual Hamiltonian terms or the initial data site. It excludes both incomplete syndrome detection and a logical Pauli supported on A_i. “Every individual error term is detectable” is insufficient, because products accumulated during a cell can centralize G_i or become logical.

For a fixed genuine record, expand memory operators into Paulis while keeping all bath coefficients in chronological order. Exact boundary projections select the cell's net syndrome character. On a zero-change cell, the displayed footprint condition forces every surviving net memory Pauli to be a stabilizer up to phase. On an encoded Pauli-error orbit it is scalar independently of the logical vector; the same is true of the exact stabilizer projectors on that orbit. This is an operator expansion of a CP-record branch, not a positive stochastic Pauli mixture.

A parent with any flagged cell is conservatively charged on its whole bounded reservation, even if later flips cancel and its final syndrome returns. Moving memory factors to completion uses the prior strict cleanliness/support assumptions; bath factors are not moved. The intended exact correction remains at its justified start. Pending, externally dirty, or incomplete-measurement parents need the original separate bad-parent treatment.

Important domain distinction: the **effect inequality** applies on the whole allowed memory–bath input; the **harmless matched-history statement** is about the stipulated encoded Pauli-error histories and common-decoder certificate. An arbitrary syndrome-preserving logical Hamiltonian could satisfy deletion-null detector conditions while damaging encoded information. Such a term cannot be silently added to the support theorem merely because it preserves G_i. Full reservation, complete charging/allowed ideal-operation restrictions, and the no-logical footprint hypothesis remain substantive requirements. The existing geometry and subset-to-contour module must also be supplied before claiming a memory theorem.

## 4. Duration and ideal-resource accounting
Weak action a_c integrates the charged perturbation over its assigned cell. Total tau_i is the weak-noise exposure used in the probability factor. Total reservation theta_i must separately include exact correction, initial-sector acquisition if needed, all M_i subsequent boundary measurements, resets, comparisons, record resources and tails. Fixed times and clean classification must not depend on detector outcomes.

If boundaries are treated as instantaneous, declare that idealization. If they take time, require their exact bath-independent implementation and explicitly specify whether perturbations are absent during those operations or are included in a valid charging model. Ambient coupling during a supposedly exact readout cannot simply disappear from tau_i. Measurement errors, wrong comparisons, record corruption and incomplete final measurements are not bounded by the current ideal-detector estimate.

Increasing M_i may increase theta_i, measurement resource support, conflicts, latency and coarse constants, and may add physical errors outside this ideal model. The 1/M_i upper factor is not a free hardware limit or a claim that actual error decreases monotonically with M_i. No fresh private randomizer or continuous Markov dephaser is used here. The mechanism is the familiar ideal repeated-measurement/Zeno effect, with a joint actual-record bound.

## 5. Independent eight-dimensional CP-record check
Own source: check_deterministic_cells_independent.py. Saved results: deterministic_cells_independent_results.json. Tensor order is data A, data C, bath B. Total weak-noise duration is T=1. Checks are Z_A and Z_C. Couplings are

  V_A=0.4 X_A X_B,
  V_C=0.5 X_C Z_B,
  H_0=0.27 Y_B + 0.19 Z_A Z_B + 0.11 Z_C X_B + 0.09 Z_A Z_C Y_B.

H_0 commutes with both data checks, while ||[V_A,V_C]||=0.4; there is a genuine shared noncommuting bath. The H_0 terms preserve both sectors and serve as allowed background dynamics for the effect check. No measurement outcome or bath state is fixed in advance.

Perform actual premeasurements of A and C at t=0. Measure C at 1/3 and 2/3; A at 1/2; both at 1. The A cell actions are (1/5,1/5); C actions are (1/6,1/6,1/6). Each cell flag compares consecutive actual outcomes of its own parent. Enumerating all seven binary measurement outcomes yields 128 genuine Kraus records K_r. Every effect is summed as sum_r K_r†K_r over the corresponding record predicate, then bounded by its largest eigenvalue on the **full 8-dimensional input**.

Results:
- Complete instrument normalization: ||sum_r K_r†K_r−I||=4.495005011648175e−16.
- All 31 nonempty subsets of five cell flags obey product_c a_c² I. Largest effect/budget ratio: 0.9844466200623037.
- A parent OR: largest effect eigenvalue 0.07582127389046889 ≤ p_A=0.4²/2=0.08.
- C parent OR: 0.07969853832869839 ≤ p_C=0.5²/3=1/12.
- Both parent ORs: 0.0037584575791483692 ≤ p_A p_C=1/150.
- Joint parent probability is not the product of the two marginal probabilities in this model; the product majorant does not assert independence.
- Each of the five cells was separately deleted, once with every other multiplier equal to one and twice with seeded other multipliers in [0,1]. All 15 deleted-cell bad effects were numerically exactly zero. The boundary measurements and predicates remained unchanged.

The computation uses full dense matrix exponentials and Kraus enumeration, not Monte Carlo or author code. It is an exact finite-dimensional model evaluated in floating point, with stated numerical tolerances; it is not an interval-arithmetic proof. The analytical deletion-null argument provides the theorem. The check does not compare different M schedules and makes no actual-error monotonicity claim. No experimental files were read, and no frozen source files were edited.
