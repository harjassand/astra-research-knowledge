# Execution amendments and historical cost integrity

No sampling counts, clearance target, production horizon, per-path budgets or N=10,000 admission gate changed after viewing samples.

1. The planned GNU-time wrapper was unavailable. Its failed launch is retained. Standard-library `resource.getrusage` in `measure.py` replaced it; maximum RSS is explicitly not total-container concurrent peak.
2. A validation-only N=10 trace exhausted physical horizon 200 before 5,000 events. That failed check and all its events are retained in `attempt_001`. The validation trace horizon alone was raised to 100,000,000, still bounded by 5,000 events and five seconds. Production paths kept horizon 200.
3. After the successful run, the reusable runner's initial ledger was cleaned of a hard-coded historical failed-launch entry, and an overwrite guard was added. Historical evidence remains in the original `COST_LEDGER.json`/`attempt_001`; clean replays should not pretend they experienced the old unavailable-timer failure. The C++ trajectory engine and sample/ODE computations were unchanged. This orchestration-only edit was syntax checked; a redundant full sampling replay was not run.
4. The original cost ledger contains the same initial unavailable-timer failure in both the current and archived ledgers. Reconciliation charges its observed 0.036565443-second outer command exactly once. Other failed-attempt subprocesses are distinct and all counted. Exact failed-controller CPU was never recorded; the entire elapsed failed-run-to-relaunch window is conservatively charged rather than invented.
