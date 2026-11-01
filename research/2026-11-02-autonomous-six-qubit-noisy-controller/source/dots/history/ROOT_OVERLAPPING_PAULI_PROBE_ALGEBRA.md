# Overlapping parity probes: exact logical algebra and the unearned rate interface

Root derivation, 2026-11-01. This is an operation-specific ingredient, not a complete autonomous sensor. The separately originated sensor constructor has not yet been shown this proposal.

Let each probe p be a qubit, and let C_p(P)=|0><0|_p I+|1><1|_p P for a Hermitian data Pauli P. For distinct probes p,q,

 C_p(P) C_q(R)=CZ_pq^{omega(P,R)} C_q(R) C_p(P),

where omega is1 for anticommuting Paulis and0 otherwise. The extra phase acts ONLY on probes and commutes with every controlled-Pauli interaction.

Suppose a probe traverses a prescribed check S_p, applying controlled single-qubit Pauli factors whose product is S_p. All complete checks commute. If probes complete before joint readout, arbitrary interleaving of their data interactions can therefore be reordered as complete C_p(S_p) operations plus a graph of probe-probe CZ phases. No perfect mutual exclusion is needed to show that the ideal complete interaction is nondemolition on the data's stabilizer and logical algebras.

For chronological individual readout/discard, a dressed-observable proof is safer than moving CZ gates through X measurements. Let P_p(t) be the partial Pauli product already visited by probe p. For a data Pauli O commuting with every complete check, define

 O_tilde(t)=O prod_(p in flight) Z_p^{omega(P_p(t),O)}.

Each controlled local interaction transports this observable exactly to its updated form. At probe completion P_p=S_p, its exponent is0; hence any measurement/reset/discard of that completed probe commutes with O_tilde. The argument applies to stabilizers and protected logical Paulis. Thus ideal overlap does not itself erase protected logical information. It DOES NOT guarantee a correct individual sensor report.

In fact probe-probe CZ phases can destroy individual X-readout information. Two probes joined by one such CZ can have uniform X marginals even when the data syndrome is fixed. Therefore one cannot simply identify every readout with its intended stabilizer. Collision flags, graph-aware readout, deliberate thinning, or another actual information mechanism is needed.

A probe Z fault changes only its readout. A probe X/Y fault or a skipped/repeated controlled-Pauli interaction can introduce a Pauli error supported within that check's bounded patch. Such a data Pauli, propagated through other controlled-Pauli probes, picks up probe-Z factors but does not enlarge its DATA support. This is ordinary Clifford propagation used as an ingredient; it is not a complete fault-path probability bound.

The contemplated physical use is independently running probes rather than a global synchronized check schedule. It still must pay finite probe preparation/purity, transport, native interaction duration, probe loss, clock/controller faults, readout, and overlap-induced report corruption. Low occupancy by itself gives only an average collision estimate, not a time-uniform weighted fault admission sufficient for memory. A global error proportional to T is not an acceptable substitute.

The strongest active comparator receives the same probe paths and interactions. A global schedule may avoid collisions more efficiently; eliminating its controller is a different resource claim, not automatic throughput or fidelity superiority.

Next essential task: obtain an actual bounded-strength, apparatus-inclusive local report/error service for this or a better mechanism. No source primitive is earned by the algebra alone.
