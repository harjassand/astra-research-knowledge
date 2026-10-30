# Audit of fixed-iteration Tanner classical locality
2026-10-30. Independent primary-source check of NOISY_CLASSICAL_ORDINARY_COMPARATOR.md.

## Verdict
PASS for a fixed number of parallel iterations, with fixed local code degree, bounded physical edge delays, bounded local fanout, fresh per-round scratch, and physical application of the correction mask. No global reduction, global parity, or global maximum is hidden in the quoted parallel algorithm. The constant-spread argument does not extend unchanged to the final O(log n)-iteration decoder.

## Primary check
Inspected Gu–Tang–Caha, https://arxiv.org/html/2306.12470 , Section 4.1, Algorithms 3–4 and Theorem 4.20.

- The initial minimum-weight syndrome preimage is computed inside the fixed-size Q(v). The source explicitly sets the mask to zero when no preimage exists. A faulty/invalid local syndrome therefore has a defined finite table entry.
- A square receives exactly two initial local-mask contributions from the relevant diagonal vertex class; its initial mismatch is their XOR.
- Algorithm 4 serializes the four vertex types. Every square has exactly one vertex of each type, so views within one type are disjoint.
- The test written as |Z|-|Z+x_v| is local: outside Q(v), x_v is zero and the terms cancel. Maximizing |x_v| and minimizing its row/column decomposition are finite searches inside Q(v), not global optimizations.
- The four accumulators are componentwise bit arrays, not global numerical counters. Updates touch Q(v) only. The final correction is the initial local guess XOR two accumulator bits at that square.

These facts synthesize to a Boolean circuit of depth D_c=O(j) with constants depending on the fixed local tables, where j is the number of parallel iterations. Fixed-size truth tables can be implemented using bounded-fanin gates and fixed-depth copy trees. Thus each faulty gate has a correction-output cone bounded by q_c max(1,F_c)^(D_c+1), independent of n when j is fixed.

## Exact caveats
1. Fix deterministic tie-breaking in all local searches. This is part of the finite nominal gate definition, not an extra reliable computation.
2. Include the no-solution-to-local-syndrome default in that definition. One must not assume noisy local syndromes are all valid.
3. Shared-memory notation in the pseudocode is not itself a physical architecture. The comparator's per-square/neighbor registers and bounded edge messages are a legitimate realization, provided their propagation time and faults are counted.
4. A global clock, global reset line, or unbounded-fanout bus is not a single bounded local fault. The stated result assumes a schedule, not a fault-tolerant autonomous implementation of that schedule.
5. Theorem 4.20 supplies the reduced-weight contraction for the actual parallel output. Applying a minimum STABILIZER representative in the induction is valid because it leaves the syndrome and correction output unchanged. Replacing by an arbitrary minimum same-syndrome representative would not be valid.

Consequently the parent's removal of ideal classical gates is sound for constant-iteration scheduled MEMORY rounds under a local fault-location model. The finite-depth classical CPTP construction and coherent-span argument in BILATERAL_SCHEDULED_CPTP_ADDENDUM.md supply the corresponding retained-bath operator proof. This audit is not an independent audit of every result in arXiv:2610.03684.
