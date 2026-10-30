# ATG fixed-baseline receiver: exact source identity, remaining native hypotheses
2026-10-30. Conditional receiving interface; no autonomous factory theorem.

Use the actual Alternating Tanner Graph construction of Bergamaschi–Liu, arXiv:2411.04405v1, section3.2 equations9–14. After bulk X measurements, regard every recorded bit as a physical classical Z_R bit. Bulk meta-checks become local parity checks of two neighboring same-type check records and the intervening DATA-readout records. Each boundary Z check is tied to its adjacent terminal check record; each boundary X check to the adjacent penultimate check record. Hence the ideal joint boundary/record state is already zero-syndrome for bounded-weight/bounded-incidence relative checks, without applying the dense final Pauli frame.

Primary source: https://arxiv.org/html/2411.04405v1
Independent algebra and the new joint-code confinement limitation are in review_factory/CQ_ATG_ANALYSIS.md.

## An alternative to correcting the entire spacetime cq code
Freeze the captured raw record in actual reliable classical memory, and correct only the quantum boundary relative to the local adjacent check-record signs. The root's proposed persistent-wrong-baseline native theorem would tolerate a fixed sparse discrepancy D between these local signs and the syndrome of the chosen output frame. This avoids assuming the new spacetime code has the old Tanner energy confinement.

Here is the exact source-side identity that makes D accessible. Work on one Pauli component of a Clifford source fault expansion. Let s be ideal raw bulk outcomes, f the measurement/capture flips, and m=s+f the actual captured record. Let b extract the local boundary baseline signs from those records. Let E_B be the physical Pauli on the quantum boundaries before memory starts. Boundary stabilizer eigenvalues are

 sigma(actual boundary)=b(s)+sigma(E_B)=b(m)+b(f)+sigma(E_B).

Let P(m) be the eventual ATG Pauli-frame correction (inversion irrelevant for binary syndromes). Suppose its corrected output lies in the Pauli branch E_rep|target>. Then

 D(m):=b(m)+sigma(P(m))
      =sigma(E_rep)+b(f)+sigma(E_B).

For check incidence nu, this gives

 |D(m)| <= nu (|E_rep|+|E_B|)+|b(f)|.

The frame and D are indexed by the ACTUAL captured record, not an inaccessible ideal trajectory. Thus a deterministic source good-support theorem bounding E_rep, E_B and f would provide the fixed-target density needed by the receiver. For several coherent Pauli components sharing the same actual m, D(m) is common; a uniform componentwise good-support statement gives a common correctable span. No coefficient norm bound follows merely from the stochastic source theorem.

## Why this is not yet a construction
1. Need the root's full-Hilbert native drift theorem with persistent wrong target signs, not just scheduled decoder contraction. Sign bits must be real stable classical registers; faulty reads and dirty prefixes remain charged.
2. Need actual capture of random measurement bits into legal reliable-classical-memory states. A constant-rate initial logical capture flip may be charged as an additional local source-record fault f; exponentially accurate agreement with the pre-capture outcome is unnecessary. Stable later retention and joint locality across records ARE necessary. Ideal copying/ARM/DONE is not supplied.
3. Need a deterministic ATG good-fault-support certificate compatible with the full retained-bath norm expansion. A local-stochastic Pauli theorem alone cannot be substituted for this.
4. Final physical frame computation/application and acceptance still need an actual controller. Conjugating an accumulated physical Pauli error by P(m) preserves its support; this removes one artificial dense-error concern, not the actual late-command problem.
5. Memory lifetime must cover the real decoder/runtime with the correct exponents and hardware cost.

This source identity is complementary to ONE_AXIS_HERALD_TWIRL.md. Neither route inherits a universal autonomous threshold.
