# Independent actual clearance weak-CLT audit

Read `SOURCE_BOUND_ACCEPTANCE.md`, then `MATHEMATICAL_REVIEW.md`.
`DETERMINISTIC_PARAMETER_BINDINGS.md` keeps the previous scalar/functional
numerics separate and records the precise newly earned identification.

Self-contained read-only replay (installed Python and SymPy required):

    python verify_audit.py

To additionally recheck every controlling original source and all previous
parameter receipt pins in the original workspace:

    python verify_audit.py --original-root producer-workspace/57d8dd795b13

The verifier checks immutable files before running both checkers in temporary
directories and compares exact output bytes. It never runs writing tests in
an original source tree. The 63 old parameter bindings are optional at relocation
because their numerical runtime is not duplicated here; their exact records and
controlling receipt/proof/certificate snapshots are included. No new numerical
solver acceptance is implied by either verification mode.

`prepare_snapshot.py` and `check_parameter_bindings.py` record the one-time audit
construction/readback and are NOT reproduction entrypoints in a frozen audit.
They write adjacent outputs; use the read-only verifier instead.
