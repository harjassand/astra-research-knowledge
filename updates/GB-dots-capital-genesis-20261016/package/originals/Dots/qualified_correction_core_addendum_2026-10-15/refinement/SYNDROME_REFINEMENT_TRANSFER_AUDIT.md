# Independent audit: stabilizer-refined correction transfer

Date: 2026-10-15. Separate from the finalized overlapping-pulse packet.

## Verdict

PASS. Replacing a completed coarse correction by a genuine stabilizer-measurement refinement preserves its transitions on every encoded Pauli orbit and preserves the universal support/common-decoder argument, including coherent sums and joint bath/reference inputs. It also remains compatible with the global subset-moment proof when inserted as a frame-independent exact instrument in the same deletion-stable dilation model.

This is a transfer to a different physical channel. It does not prove equality on syndrome coherences, qualify noisy measurements, or certify an unexamined controller implementation.

## 1. Exact refinement identity

Assume the completed correction has Kraus K_j=Q_j Pi_j, with an orthogonal stabilizer-function resolution sum_j Pi_j=I. Measure commuting code stabilizers whose joint nonzero eigenspace projectors R_s resolve every decision Pi_j. Equivalently, for a deterministic label map j(s),

Pi_j=sum_(s:j(s)=j) R_s.

Then Pi_j R_s=1_(j(s)=j) R_s, and the refined instrument has Kraus L_s=Q_(j(s)) R_s. It is CPTP because sum_s L_s†L_s=sum_s R_s=I. If D_R(X)=sum_s R_s X R_s, its memory channel is exactly

C_ref=C D_R.

Mere commutation of measured checks with Pi_j is not enough: the measured spectral labels must actually determine j. The assumed equality above is the required refinement test.

## 2. The actual sweep decision checks suffice

For one primal sweep attempt, the source defines each active Pi_(v,O) by all eight incident edge-stabilizer eigenvalues: the four incoming defects must be absent and the four outgoing defects must equal the specified nonempty even subset O. There are six size-two choices and one size-four choice, hence seven active patterns.

Measuring these eight commuting checks gives

R_s=product_(e incident to v) [I+(-1)^(s_e) S_e]/2.

These projectors are orthogonal and sum to identity. Algebraically inconsistent labels have R_s=0 and are discarded. Each active Pi_(v,O) is exactly the corresponding full-pattern R_s; the inactive completed projector is

Pi_0=I-sum_active Pi_(v,O)=sum_(all other nonzero labels s) R_s.

Thus the aggregate inactive branch is genuinely refined, not silently treated as if it already measured the individual bits. The dual sector has the same construction.

Each four-dimensional edge check involves six plaquettes. The union of the eight incident checks contains 24 plaquettes, because every plaquette in the union meets two of those edges. This is bounded uniformly in system size for the sufficiently large nondegenerate periodic lattices used by the theorem. The paired correction faces are already in this neighborhood. The product of the eight checks is identity, so odd local parity labels are zero; this dependency causes no incompleteness. No assertion that all remaining local labels must be globally realizable is needed.

Ordinary exact commuting-check extraction plus finite lookup and the prescribed conditional Pauli therefore implements the required refined instrument in principle. Actual ancilla placement, private ancilla reset/discard, gates, measurement/readout correctness, duration, and full reservation/noise geometry must be specified and counted. Bounded data support alone does not establish those physical assumptions.

## 3. Equality on full logical orbits

Let V encode the entire code space, and let E be any Pauli. Every measured stabilizer S has one eigenvalue on E V, independent of the logical vector. Exactly one nonzero R_s therefore satisfies R_s E V=E V, while all other R_t annihilate it. Its coarse decision is the same unique j for which Pi_j E V=E V. Both instruments consequently apply the same memory operator Q_j E V.

This equality is an equality on the logical input map, not just on a chosen logical state. It survives arbitrary logical/reference/bath entanglement on that orbit. The refined outcome can record a more detailed syndrome, but that record is independent of the logical vector within the orbit.

The channels differ on general cross-orbit coherences inside a coarse branch. For example, an off-diagonal operator between two distinct refined inactive sectors survives Pi_0 X Pi_0 but is removed by D_R. This difference is real and has been acknowledged in the candidate.

## 4. Coherent histories and the same decoder

Expand each allowed local fault in memory Paulis with chronological auxiliary coefficients. In a fixed refined physical record, each R_s kills or preserves every Pauli-orbit term, then applies precisely the original decision Q_j. Thus refinement may remove terms from that record and split histories among different records; it cannot introduce a new Pauli support or a correction transition absent from the original support certificate.

If the certificate guarantees that one fixed decoder maps every admitted Pauli history to scalar logical identity, the same is true for every surviving term in each refined Kraus record. Sum the coefficients coherently inside that record, keeping all bath-factor order and relative phases. The decoded Kraus operator is still I_logical tensor B_record.

This proves the good CP subchannel factorization without pretending that a coherent sum of histories is a positive Pauli mixture. Good records remain trace-nonincreasing, and the established bath-defect completion applies after all physical outcomes are summed for the uniform probability estimate. A normalized selected measurement outcome is not a substitute for that complete CP argument.

## 5. Compatibility with global moments and completion locality

The subset-character estimate permits arbitrary frame-independent background operations in a common unitary dilation. Replacing coarse C by the exact refined instrument changes that background but does not create additional explicit dependence on any private frame. With independent ancilla initialization and one common controlled dilation under all coupling deletions/interpolations, the mixed-Duhamel and L2-projection proof remains valid.

The completion-time locality argument also remains valid when the full measurement/ancilla support is included in the reservation. Any relocated pulse memory factor must commute with every measurement circuit or projector it crosses. Full-support cleanliness, rather than vertex separation or the older smaller support, is required.

As before, only clean fully completed/unframed pulse variables are Fourier transformed. Pending seeds remain unselected; endogenous measurement outcomes remain in the common dilation and are summed at the effect level. The extra refined labels are genuine physical records, but any later use must satisfy the existing locality, uniform norm, timing, and deletion-stability assumptions. The labels do not authorize arbitrary feedback. Finite bath/retained-output conventions remain unchanged.

The result transfers the proof structure and existence of suitable bounded-geometry constants. It does not certify unchanged numerical thresholds, unchanged durations, or unchanged collision/noise budgets without recounting the implementation.

## 6. Exact checks

../checks/refinement/check_syndrome_refinement.py was created and run successfully. It verifies:

- the 24-plaquette union of the eight four-dimensional incident edge-check supports;
- seven active labels and exhaustive assignment of the remaining labels to the inactive aggregate, with the even-parity dependency respected;
- exact C_ref=C D_R in a small stabilizer code on every matrix unit;
- equality of coarse/refined action on every full-syndrome logical orbit matrix unit;
- CPTP completeness of the refined instrument;
- a concrete inactive-sector coherence preserved by C and removed by C_ref.

The small-code calculation is supplementary; the general spectral-projector and common-decoder arguments above establish the transfer.

No obstruction was found within the explicit hypotheses. The decisive requirements are actual decision refinement, bounded full reservation, an exact bath-independent correction implementation, and preservation of the common-dilation assumptions.
