# Noisy classical controller bits fit the same theorem

29 October 2026. This is a literal corollary of PROOF.md, not an acquired
classical controller threshold.

Adjoin c physical controller bits to the data code. Extend the stabilizer
group by Z_i on every new bit. The extended code has the SAME protected
logical qubits and distance d: a normalizer Pauli on the new bits is a
product of Z_i stabilizers and has no logical action. A fixed classical
program/clock initialization is simply a choice or mixture of the new
syndrome values, independent of the unknown logical state.

A local Boolean update of a target bit, conditional on local controller
bits and data syndromes, is implementable as follows: measure their
commuting Z/check values and the old target bit, apply X_target exactly
when the old and desired bit differ, and discard the measurement outcomes.
Its Kraus operators are Pauli times check-projector. A classically
controlled data correction has the same form with a data Pauli. Local
copy, comparison, bounded fan-in logic and classical bit reset all fit
this rule; a physical multi-bit operation must still pay its actual
bounded support and time rather than assume a free word operation.

Add finite-rate dephasing on the new Z_i, in addition to the data check
dephasing. It does not change any classical update or classical bit
probability. Arbitrary local CPTP noise, including coherent controller
errors and unbalanced clock resets, remains admitted on these physical
bits. There is no noiseless classical register. The proof of normalizer
closure and the Poisson-cut exposure bounds applies on the extended
check list. The parameter n counts these controller bits and the local
incidence/support constants must include their update/fault apparatus.

Every purely controller-supported normalizer is already a stabilizer.
Thus a controller-only coherence component need not be declared quantum
bad merely because it is large; the distance-size test in PROOF(9) is a
convenient sufficient condition, not a characterization. Large classical
corruptions can nevertheless cause uncontrolled future data Pauli errors.
They are **not repaired by dephasing** and remain part of the classical
persistence event delta_cl.

This gives a useful separation. A repairing classical controller can be
designed using ordinary reliable asynchronous computation, while finite
check dephasing controls the additional quantum coherences that its
physical bits can acquire. But one must actually prove its sustained-noise
restoring property together with its data-feedback algorithm, at real
local-bit/gate rates. A generic self-stabilizing clock theorem after a
quiet interval is insufficient. Gacs's existing noisy asynchronous
classical machinery is a strong ordinary candidate, not a free oracle.

It also does not suffice to import an active decoder which has noiseless
polylog-sized word registers and instantaneous comparisons. A local-bit
implementation can add unbounded latency, and protecting those bits may
alter the required message velocity or fault model. The concrete joint
data/controller eroder certificate is still the decisive gate.

The autonomous quantum data operations here are only commuting-check
measurements and conditional Paulis. Arbitrary coherent universal gates,
which can spread the bra/ket Pauli difference, are outside this corollary.
No quantum-state cloning, discarded-state rewind or coherent copy of an
unknown clock/data history is used.
