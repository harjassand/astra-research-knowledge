# Local reproduction

Observed environment: Python3.12.14, NumPy2.3.5, SciPy1.17.0. The partial-row LP constructor uses SciPy/HiGHS only to propose; all acceptance inequalities are evaluated using exact fractions. Other main constructors are standard-library Python. This records the environment, not a claim of cross-version deterministic LP proposals.

From the archive root, for example:

```sh
python stochastic_coverage_pending_20261031/coverage_boundary.py > producer-workspace/coverage_replay.json
cmp producer-workspace/coverage_replay.json stochastic_coverage_pending_20261031/results.json
python stochastic_coverage_pending_20261031/independent_audit/verify_coverage.py
```

Each package's independent verifier imports its own frozen candidate source for generating challenge inputs, but independently reconstructs the supplied certificate equations/inequalities from raw reaction lists rather than delegating the acceptance check back to the constructor. See the review for its exact role.

Other main replay commands are:

```sh
python stochastic_phase_boundary_general_20261031/phase_boundary_general.py
python stochastic_nonlinear_boundary_20261031/nonlinear_boundary.py
python stochastic_protected_boundary_20261031/protected_boundary.py
python stochastic_partial_rows_pending_20261031/partial_boundary.py
```

The two-inactive cubic activation challenge is intentionally separate and expensive:

```sh
python stochastic_nonlinear_boundary_20261031/independent_audit/two_inactive_challenge.py
```

It previously required about340 seconds and4,769-bit solved fractions; no fast-runtime guarantee is made. The exact same-network protected comparison can use its included reviewed receipt instead of rerunning that expensive clock:

```sh
python stochastic_protected_boundary_20261031/independent_audit/same_network_comparison.py
```

Do not attempt to expand the coverage Foster constant merely to replay its proof. It is deliberately a factored rational-power expression with recorded exponents and expansion-size bounds. Exact master-bound checks use bounded-jump quotients. No simulation is required or accepted as a proof.

`SHA256SUMS` binds all payload bytes; `ALLOWLIST.json` specifies exact archive membership and original local source mapping. The archive verification receipt is kept alongside the ZIP rather than inside its own hash cycle.

The separately reviewed first-hub clock comparison is replayed from its original path, with adjacent package dependencies retained:

```sh
python stochastic_single_token_pending_20261031/compare_clock.py
python stochastic_single_token_pending_20261031/independent_audit/verify_single.py
```
