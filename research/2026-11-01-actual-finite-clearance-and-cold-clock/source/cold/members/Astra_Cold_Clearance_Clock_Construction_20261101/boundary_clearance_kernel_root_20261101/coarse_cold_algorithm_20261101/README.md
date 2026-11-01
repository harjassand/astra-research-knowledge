# Prospective coarse cold receiver — author freeze

Run the COMPLETE new algorithm (three coarse scalar passes, including the distinct
verifier, then both fixtures):

    python run_cold.py

Run only static cost/source checks without another scalar solve:

    python check_static_cost.py

Copy this directory and its source-bound workspace-relative dependencies before
replay. The source manifest paths are relative to the workspace root two levels
above this directory. The complete algorithm writes adjacent fresh outputs.

- `COLD_ALGORITHM_AND_BIT_COST.md`: mathematical precision, explicit machine,
  arithmetic/control/storage/I/O accounting, scientific join and limitations.
- `COARSE_CERTIFICATE.json`: fresh width below8.678e-8, not the old fine scalar.
- `INDEPENDENT_COARSE_CHECK.json`: different-implementation exact replay.
- `COARSE_WINDOWS.json`: separate slightly enlarged two-fixture outputs.
- `RESEARCH_LEDGER.json`: every construction-branch numerical run and preserved
  old ledgers; no failed scalar candidate is omitted.
- `AUTHOR_FREEZE.json`: complete file hashes and old-output preservation bindings.

Prospective upper bound: fewer than3e20 abstract bit steps, including the source
input, all three scalar passes, verification and both fixture evaluations. This
is NOT a CPython/wall-time bound or a retrospective research-cost reduction.
AtN=1e25 it is below the2e21−1 literal-event history lower bound, but establishes
no advantage over ordinary non-enumerative validated/retained predictors.
Independent ordinary receiving review is required before accepting these new
algorithmic and numerical claims. Existing accepted windows and old cold ledgers
are not changed.
