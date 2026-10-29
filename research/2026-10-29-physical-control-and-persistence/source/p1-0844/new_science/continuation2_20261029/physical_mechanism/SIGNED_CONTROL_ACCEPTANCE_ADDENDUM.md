# Final acceptance addendum and robust-program physical-scope review

29 October 2026. Existing Astra P1 physical-mechanism receiving reviewer.

## 1. Signed theorem: requested corrections accepted

Reviewed final input: `../SIGNED_CONTINUATION_CONTROL_THEOREM.md`.

SHA-256:
`658fc39e1a991ab34669cd702b37b8cf93216b2ca7fa35d2fd52d54d2cbafb2a`.

The 23,995-byte version is preserved verbatim in
`reviewed_versions/SIGNED_CONTINUATION_CONTROL_THEOREM_658fc39e1a99.md`.

The previous review accepted the core analytic theorem and ring kernel algebra,
and requested precise joint-clock wording and explicit physical treatment of
controller latency. Both requests are satisfied in this version. Section5.3
now distinguishes endpoint-clock independence from equality of joint laws,
and Section6 explicitly avoids claiming that the conditional output-given-clock
pattern must vary with h. Section10 states the ideal instantaneous boundary
model and requires actual decision-time evolution to be included in the
kernel or protected by an actual hold.

The additional changes correctly cap the stopping functional on all reference
paths, restrict the polynomial/Chebyshev argument to endpoint-only fixed-length
calls, and include complete retained controller state and reused seeds in D
or require independent future randomization. They do not alter the accepted
central sign argument. Exact h supplied to the controller remains outside the
common-rule premise, as Section8 expressly states.

**Final disposition: accepted at the stated scopes.** No remaining correction
is requested for this version. Acceptance is mathematical and interface-
conditional: it is not acceptance of an apparatus, finite-data model
identification, practical speedup, or novelty priority.

## 2. Robust observable program: reviewed physical interface

Reviewed input: `../ROBUST_OBSERVABLE_PROGRAM.md`.

SHA-256:
`70c6946997e53e49a114a85ba4050db1b260c550d6f4329c434fc14c29cf4ec5`.

The 10,230-byte input is preserved at
`reviewed_versions/ROBUST_OBSERVABLE_PROGRAM_70c6946997e5.md`.
The mathematical receiving bound is being independently reviewed by the
record-geometry role. This review checks the physical supplier and record
scope, plus its finite implementation evidence.

The actual source-B words are T0 and T3 followed by T3 on the SAME selected
site. Both have strictly positive native-call cost; no identity branch is
used. Other sites must actually be isolated during either word. Static H_i
and fresh native increments conditional on the hidden vector are substantive
premises. Intermediate reads may be retained, but must not interrupt or
change the chosen word or the fixed random-scan schedule.

Per-site estimates use the full saved calibration outcomes from the same
deployment specimens. The controller's dyadic selector uses only these counts,
the declared clipping intervals and desired visible context. The true hidden
parameters are used separately by the numerical checker to calculate the
actual closed-loop kernel; they are not inputs to its selector. No equilibrium
ensemble, new hidden reset, or transfer to a different specimen is claimed.

Rounding w to a b-bit dyadic probability is executable with exactly b fresh
fair bits and integer comparison. Counts and rational clipping endpoints
permit exact integer arithmetic for the numerator. The conservative extra
row-TV charge 2^(-b) is valid; the implemented nearest rounding actually has
weight error at most 2^(-b-1). The physical endpoint error term requires a
separate real contract. The ideal data/model exercise does not acquire an
apparatus value for it, nor does the confidence radius cover unmodelled
calibration-readout bias, drift or crosstalk.

The manuscript carries the corrected decision-time interface: instantaneous
boundary reads and switching in the formal model, with real latency included
in the actual kernel or covered by an actual protected hold. Variable one-
or two-call durations are paid. No common-time padding or identity actuator
is inferred from equilibrium or from the target kernel's algebraic laziness.

## 3. Which records and times are covered

The observable guarantee is evaluated at each deterministic MACROSTEP count.
It is not a guarantee at arbitrary physical wall times, at data-selected
stopping times, or for the entire subsequent record. The random site choice
must retain its declared state/history-independent uniform law. The frozen
calibration-selected mixture table may depend on visible context, but new
primitive marks cannot be used to change that fixed program.

Complete pre-service D and Z can remain and may correlate with H. Uniform
pointwise calibration coverage for each fixed hidden vector gives the joint
frequentist bad-event charge beta; it is not confidence conditional on every
rare D. The macro row is conditioned on history BEFORE its fresh selector.
A bound conditioned on that newly exposed selector itself is not asserted.
This distinction is consistent with Section4's explicit exclusion of a
joint endpoint/new-key service-record bound.

Current keys, native logs and word duration may therefore remain physically
present at their real costs without being certified by this narrower objective.
Their mere retention does not affect the actual endpoint marginal, provided
the actual program ignores them for any change beyond its declared state
updates. This is a legitimate stronger ordinary comparator than requiring
all apparatus records to become autonomous.

## 4. Independent saved-data and implementation audit

`check_robust_physical_interface.py` reads the existing packed synthetic arrays;
it does not regenerate or replace them. It verifies all eight array hashes,
all 800,000 saved flip increments and all reported counts, and reconstructs
the post-calibration visible state (0,0,0,1). From counts alone it reconstructs
all 64 dyadic native selectors and checks the saved implementation table.
Only afterward does it use the declared synthetic truth to verify each actual
row. The maximum actual row error is exactly 471/327680. The maximum selector
rounding error is 301277/45670662144, below 2^(-17).

The recorded normalized-Hamming metric bound including beta is
0.028041106394505334. The corresponding magnetization expectation bound is
0.05608221278901067, for each deterministic macrostep under the stated
contract. This is not an all-times sample-path event.

The displayed magnetization discrepancy 0.0004858375861029503 is the maximum
COMPUTED from the fitted population kernels THROUGH 1,000 macrosteps; the
reported curve attains it at step10. At step1,000 the reported magnetization
error is about 2.43e-17. These are model-based distribution calculations after
synthetic calibration, not measured physical service errors. The maximum
bond discrepancy through1,000 is about0.000239614. The synthetic native
readouts and those population calculations should be described separately.

**Physical-scope disposition: accepted under the explicit fixed-H,
conditionally fresh native-noise, accurate calibration-label, isolation,
and boundary-control premises.** No additional physical obstruction was
found. The table uses real words and a literal fixed-bit selector; there is
no free identity, copied hidden state, invisible calibration transfer, or
unbounded rejection sampler in this finite implementation.
