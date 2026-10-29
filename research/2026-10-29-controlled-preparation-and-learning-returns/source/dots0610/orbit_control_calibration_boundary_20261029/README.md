# Encoder and control calibration boundary, 2026-10-29

Status: author proofs and executable diagnostics complete; independent
receiving review pending. Do not treat a quick algebra sanity check as review.

Governing files:
- THREE_AXIS_MEMBERSHIP_v1.md: actual three-axis zero-magnetization measurements
  bound singlet leakage by12/5 times observed failure, independent of n.
- OPERATIONAL_CALIBRATION_BOUNDARY_v1.md: indistinguishable wrong-encoder and
  inverse-control counterexamples, plus the stable-isolated-endpoint bridge
  sqrt(e_service)<=sqrt(delta_roundtrip)+sqrt(p_source)+2sqrt(eta_leakage).
- ACQUIRED_CONTROL_ERROR_ACCOUNTING_v2.md: explicitly acquired native-gate
  confidence bounds and deployed-use counts, including matching Bell controls.
- check_calibration_boundary_v1.py/.json: spin1..50, full n2/4/6/8 operators,
  36 endpoint/source examples and the GHZ counterexample.

What this changes: exact encoder/decoder matrices are not required for one
conditional certification interface. Actual code-membership, actual round-trip,
and actual gate-reference tests provide the needed quantitative inputs.

What is still assumed: stable, isolated endpoint and primitive channels when
transferring calibration; trusted preparation/readout references; actual private
randomness and the complete source boundary. Arbitrary retained memory is
allowed in the source, not silently transferred to uncalibrated endpoint baths.
A stale finite bank cannot certify arbitrary future endpoint drift.

Strong comparator: full-path logical two-basis tests automatically include
actual encoder/source/decoder/control errors and can require only a constant
number of tests as outer block length grows. They remain the stronger default
without independent stable-control evidence. No total-cost advantage is claimed.

Run: OPENBLAS_NUM_THREADS=1 python3 check_calibration_boundary_v1.py
Requires Python3, NumPy, SciPy. No external data.

## Completed review and exact shared-memory obstruction
The three-axis theorem, stable endpoint transfer and control-debit supplement
have completed substantive independent review at their stated scope:
../control_calibration_audit_20261029/REVIEW_RECEIPT.json.

SHARED_MEMORY_COUNTEREXAMPLE_v3.md and its executable check add a stronger
boundary: even freshly interleaved membership, round-trip and matching tests
can ALL pass while every actual service is logical Z, if endpoints and source
share one bath bit. The source's physical channel itself is identity. This
shows operational noncomposability, not merely stale statistical evidence.
It requires its own independent addendum review beyond the first receipt.

OPTIMIZED_MODULAR_ROLE_ALLOCATION_v4.md gives the weighted role allocation from
the square-root transfer. It improves the conservative threefold bound but
still loses statistically to full-path logical verification; no advantage is
asserted. Full operation testing or independently warranted physical control
isolation remains essential under shared-device memory.

At 2026-10-29 04:51 UTC the separate shared-memory counterexample and optimized
role-allocation algebra completed independent substantive review:
../control_calibration_audit_20261029/shared_memory_addendum/REVIEW_RECEIPT.json
SHA256 acc364f701f9948bc587bdc46d0b7485a82edd98a27f31ab87816271dc4e307b.
The reviewer verified the complete logical-data/bath map on matrix units,
including coherent and correlated initial bath inputs, not only the two
classical flag values. The original calibration-theorem receipt is unchanged.
