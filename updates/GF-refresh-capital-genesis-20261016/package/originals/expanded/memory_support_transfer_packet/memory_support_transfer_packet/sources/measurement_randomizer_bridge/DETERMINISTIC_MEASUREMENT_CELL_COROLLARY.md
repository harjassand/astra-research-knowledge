# Deterministic measured cells: an even simpler scheduled pulse bridge

Date: 2026-10-15. Root-proposed corollary independently checked: **PASS** under the same exact-measurement, protected-record, fixed-reservation assumptions. This result does not require private frame gates or a continuous stabilizer dephaser. Its proof uses the established deletion-null detector lemma directly.

## 1. Model

For each clean completed parent i, complete its exact bath-independent intended correction first. The initial trusted G_i label is either actually measured after correction or predicted as r_i(s_i)=s_i xor syndrome_Gi(Q_i(s_i)) from an exact trusted premeasurement and exact correction.

Divide its weak-noise interval into M_i prescribed cells I_(i,l). Measure the SAME commuting stabilizer subgroup G_i exactly at every cell boundary, retaining genuine protected classical outcomes u_(i,0),...,u_(i,M_i). The first u_(i,0) is the trusted postcorrection sector. If the initial premeasurement is before correction, its deterministic predicted label plays the same role and is represented by a fixed truth table on the trusted initial record.

Set

    d_(i,l) = 1[u_(i,l) != u_(i,l-1)],
    b_i = OR_(l=1,...,M_i) d_(i,l).

Every Hamiltonian perturbation during cell (i,l) is assigned to V_(i,l), with action

    a_(i,l) = integral_(I_i,l) ||V_(i,l)(t)|| dt.

The memory support is contained in the whole parent's stipulated A_i. All fixed measurement/record/control operations share one common dilation independent of all interpolation parameters. The full physical check, data, detector-ancilla, and record resources are reserved. Other active clean parents may share an arbitrary finite bath but are disjoint on these full memory/ancilla resources. No unrelated memory operation changes G_i within one cell. Cell times, parent times, and clean classification are exogenous and fixed.

Exact unobserved stabilizer dephasing could also be present, but is unnecessary; it cannot be used to justify unmodeled faulty measurement hardware.

## 2. Whole-dilation deletion nullness

Introduce a real parameter z_(i,l) multiplying V_(i,l), keeping every other operation and interpolation parameter unchanged. Let Q_(i,l) be the fixed projector onto the retained classical event d_(i,l)=1 in the final dilation output.

When z_(i,l)=0, the memory within that cell has no charged perturbation. All remaining operations in the cell preserve its entering G_i sector. The postboundary measurement therefore repeats u_(i,l-1) exactly for every input, every bath correlation, and every setting of all other real interpolation parameters. Later operations cannot change the protected record predicate. Hence

    Q_(i,l) U_(z_i,l=0) W = 0

as a full input-operator identity, uniformly in the other parameters.

Adjacent cells share the outcome field u_(i,l); this causes no problem. All predicates are diagonal in the SAME protected record basis and commute. Deleting the later cell compares its own actual entering label with its own next output, so earlier errors are not mistaken for failures of the deleted cell. No normalized outcome conditioning is used.

## 3. Joint cell and parent effects

For any set C of selected distinct cells, the deletion-null detector lemma gives

    F_C := W^dagger U^dagger [product_(c in C) Q_c] U W
         <= product_(c in C) a_c^2 I.                 (1)

No independent-bath, no independent-outcome, and no generator-count assumption enters.

For selected distinct parents R, the commuting classical event projectors obey

    product_(i in R) 1[b_i=1]
       <= sum_(l_i in {1,...,M_i}, i in R)
             product_(i in R) Q_(i,l_i).

Pull back this positive-operator inequality through the actual common dilation and use (1). The sum factorizes exactly:

    F_R <= product_(i in R) [sum_(l=1)^M_i a_(i,l)^2] I.

Dropping any parent constraints with a factor above one gives the capped statement

    F_R <= product_(i in R) p_i I,
    p_i = min{1, sum_l a_(i,l)^2}.                    (2)

For ||V_i||<=J_i on M_i equal-length noise cells of total weak duration tau_i,

    p_i <= min{1, J_i^2 tau_i^2/M_i}.                 (3)

There is no m_i stabilizer-generator union factor. A more general nonuniform schedule obeys p_i<=J_i^2 sum_l (length I_(i,l))^2; at fixed M_i and tau_i, equal cell lengths minimize this simple majorant. The measured joint flags need not satisfy any small chronological conditional probability.

## 4. Completion-support certificate

Require the precise full-footprint condition

    Pauli(A_i) intersect Centralizer(G_i)
       subset phase times S_code.

This is stronger than checking individual error terms and includes both detection completeness and absence of a logical supported on the accumulated footprint.

Fix a complete actual boundary record and expand all cell perturbations into memory Paulis while retaining bath factors in their original chronology. Within each cell, strict cleanliness moves only its memory factors to its boundary. The net cell Pauli E_(i,l) is supported on A_i and has measured syndrome u_(i,l) xor u_(i,l-1).

If b_i=0, every cell net Pauli commutes with G_i and is therefore a code stabilizer up to phase. On each encoded Pauli-error orbit it acts as a scalar independent of the logical state, so every cell can add no support. The exact stabilizer projectors are likewise scalar or zero on these histories. This is a fixed-record operator expansion, not a stochastic Pauli mixture.

If b_i=1, conservatively charge the whole bounded parent reservation, even when its final syndrome returns to its initial value. Because no other memory operation touches that clean reservation during its execution, all its memory error factors can instead be represented at parent completion, subject to the original support theorem's allowed bad-parent envelope. Bath factors never move. Intermediate measured projectors impose record constraints but do not introduce support outside the same reservation. Exact correction first remains at its justified prescribed start.

Thus the same actual-record good CP subchannel/common-decoder construction and the same subset-to-contour interface are available. One can also exploit a finer per-cell support record, but no such refinement is needed for the parent-level corollary.

## 5. Physical cost and boundary of the claim

The total reserved gadget time theta_i includes all M_i boundary measurements after the initial sector acquisition, the initial measurement when needed, exact correction, resets, comparison, and every allowed tail. The rate budget uses the total WEAK time tau_i; the geometric conflict/latency budget uses total theta_i. They must not be conflated.

If measurement duration is idealized as zero, state that assumption explicitly. If it is nonzero, its exact bath-independent implementation and any noise-free/charged timing assumptions must be supplied. More measurements can enlarge theta_i, resource supports, conflict degree, and guarded coarse constants. The J_i^2 tau_i^2/M_i improvement is therefore not an unqualified hardware optimization or a free limit M_i→infinity. Taking M_i as a fixed sufficiently large constant remains compatible with a bounded operation count independent of system size, provided those ideal resource assumptions hold.

An unfinished boundary measurement makes the parent pending at readout and cannot be inserted fictitiously. Corrupted measurements, records, or comparisons are outside this exact-detector result. Arbitrary ambient coherent coupling during supposedly exact readout is not silently covered.

This is the familiar Zeno measurement-suppression mechanism, here connected by an actual-record whole-dilation joint-subset estimate to the scheduled memory proof. It is not a new operation family and makes no priority claim. The continuous-dephaser/Fourier bridge in REPORT.md remains a separate valid option.

## Source dependency

The only quantum effect input beyond elementary commuting-event union bounds is ../deletion_null_detector_bridge/DETECTOR_SUBSET_AUDIT.md, Sections 1-3. Shared-bath support and common-decoder obligations are the same as REPORT.md, Section 6, and the earlier completion-locality theorem. No source or canonical theorem file was edited.
