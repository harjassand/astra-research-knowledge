# Root review: measured charged-error fallback

29 October2026. Whole-read c_charged_controller/MEASURED_FALLBACK.md and
directly read Han et al.2609.20537v1 Lemma16 and AppendixC.3–C.7, including
the ordered frozen-slot maps, syndrome-subset CP contraction and local-CPTP
extension. ACCEPTED at the measured,record-assisted,ideal-primitive scope.
This does not accept an unmonitored autonomous charged-error memory.

The exact nominal-check interaction picture preserves locality up to the
stated fixed support inflation. Its GKSL summands have a warranted weighted
incidence budget J. The per-qubit integrated fine-slot difference strength
is <=J tau, independently of the number of Trotter slices. Frozen marked
slots need not commute; unmarked slots are resummed to chronological CPTP
maps before norms are taken.

The MW half-coverage statement and marked physical-region organization are
ordinary Han machinery. Root checked their exact hypotheses and supporting
Pauli/syndrome argument in the primary. Replacing the crude slot-count factor
by product(1+z a_alpha) is valid. Since every marked nonzero collection needs
>=|U|/(2r) slots and total weight touching U is <=J tau |U|, the optimized
Chernoff estimate gives (2erJ tau)^(|U|/(2r)). It has no residual depth factor.
The connected-region count and exp(Xi)-1 resummation therefore pass uniformly
to continuous-time finite-n propagators. No stochastic Pauli reduction or
O(n tau dt) error is retained.

The record-preserving improvement also reconstructs. Retaining orthogonal
syndrome labels keeps every restricted recovery sum CP trace-nonincreasing
with diamond norm<=1. Small configurations are scalar identity in EACH
record branch. Their record measure may be signed: positivity is not
granted. Comparing the actual record law at maximally mixed logical input
to that signed measure costs B; triangle inequality yields the full
instrument bound2B. Uniformity over virtual Pauli frames then allows CPTP
hybrid composition over the actual retained histories, without a square-root
loss or a factor equal to the syndrome alphabet.

Pauli-conjugated nominal Hamiltonians remain commuting signed checks, scalar
on the codespace. Conjugated local noise has the same support/norm bounds.
Frame updates can consequently be DEFINED offline without being applied to
the data during storage. The readout actually consumes the retained record
and the initial sampled syndrome. No information-free decoder or physical
controller adaptation is assumed.

Accepted result: perfect periodic syndrome extraction and record-assisted
nominal MW decoding yield the stated all-input continuous-time charged-
Hamiltonian/unbalanced-GKSL error bound. The generic active-QEC mechanism
and primary cluster resummation are established tools, not rediscovered
novel principles. The weighted continuous-time bound and record interface
are the scoped constructions reviewed here.

Costs remain explicit: a global fast clock, perfect local measurements and
resets, O(nm) reliable classical record bits/work over m rounds, and a finite
but potentially exponential offline MW decoder. Noise during extraction,
persistent bath memory, bounded-time efficient readout and throwing away
the record are NOT covered. No new trajectory, native finite-code replay,
hardware test, practical threshold or world-priority claim was performed in
this root review. The data-only fixed thermal controller remains unproved
for arbitrary unknown charged errors.

Primary source: https://arxiv.org/html/2609.20537v1 .
