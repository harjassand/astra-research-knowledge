# Narrow review of the root's coefficientwise Pauli-branch interface

2026-10-29. Reviewed PAULI_BRANCH_INTERFACE.md; full forest-gauge identities remain the responsibility of its independent audit.

The coefficientwise linear-algebra claim is correct in the following exact form. If good-range projectors P_in,P_out act only on controller/workspace/bath-independent ancillary registers, and a Kraus operator K on data plus controllers/bath satisfies

    (I-P_out) K P_in=0,

then writing K=sum_P P_data tensor B_P in a complete linearly independent data-Pauli basis gives

    (I-P_out) B_P P_in=0

for each coefficient P. This follows by applying the dual Pauli coefficient functional. It does not require the coefficients to be positive, stochastic, or independent.

This works only for good-range inclusions that truly hold at the Kraus/instrument branch level; an averaged expectation bound on bad weight is not such an inclusion. Controller-only projectors are essential: a data-dependent projector could couple different Pauli coefficients and invalidate the inference.

Assuming the audited full-Hilbert gauge and exact unmarked emission semantics, the ensuing common-correctable-span reasoning is sound. Physical primitive/reset records and mark assignments can be held fixed while Pauli components are expanded algebraically. Same-syndrome coherence is retained.

Two limitations must remain explicit:

1. Actual reset/monitor records are generally data/controller dependent. Their conditioned distributions cannot be treated as independent ideal Poisson hub schedules, nor can a norm estimate be renormalized after a rare record.
2. A marked emission is not itself an independent rate-ε primitive kick. The Poisson CPTP one-block and long-time estimates require a separate joint bound for all malformed-emission mass and missed-service cells assigned to a fixed certificate. Coefficientwise semantics alone does not give that probability bound.

The root's file already acknowledges these distinctions. It provides a legitimate semantic interface, conditional on the gauge audit, but does not alone import the ideal-clock probability calculation.
