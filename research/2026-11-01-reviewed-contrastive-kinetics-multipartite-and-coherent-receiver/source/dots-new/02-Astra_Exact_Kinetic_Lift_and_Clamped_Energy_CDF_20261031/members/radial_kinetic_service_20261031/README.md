# Exact homogeneous kinetic lift and finite clamped-energy consumer

**Theorem separately accepted; executable author-frozen for whole review.**
See `EXACT_KINETIC_LIFT_CANDIDATE.md` and its source-bound theorem receipts in
`audit_kinetic_lift_20261031_2143/`. They do not automatically accept the executable.

- `receive_kinetic.py`: standard-library raw model acquisition, exact protocol
  Gamma-Poisson CDF enclosure, and external-task receiving verifier.
- `check.py`: exact symbolic identities, rational interval checks, malformed
  model/task/certificate refusal, all four saved replays and stronger ordinary
  Gaussian comparator. SymPy/scipy are test dependencies only; scipy values are
  diagnostic crosschecks, not proof premises.
- `EXACT_ARITHMETIC_AND_COSTS.md`: finite numerical proof and complete cost scope.
- `MISSING_OPERATION_JUDGMENT.md`: useful consequence, ordinary machinery that
  already wins, real Euclidean counterexample and still-open autonomous latency.
- `results.json`, `check_results.json`: actual results and replay evidence.
- `small_raw_fixture.json`, `small_certificate.json`: supplied standalone raw case.
- `*_BEFORE_*_CORRECTION.md`: preserved theorem correction history, not current
  accepted source; no executable was ever accepted against those old versions.

Run `python -B check.py` in this directory to actually recompute all four saved
cases. Runtime environment used: Python3.12.14; test SymPy1.14.0/scipy1.17.0.
All resources are local. No hardware or biological operation, upload, purchase,
publication or outreach is performed. Original accepted archives are unchanged.

Observable: terminal energy CDF under the DECLARED external clamp protocol.
The separate theorem also proves exact all-start autonomous (Y,U) path-law
reduction for the declared tensor. The finite executable does NOT compute an
autonomous hitting time or alter an unknown physical system. Model membership
and actual actuation remain unauthenticated. The singular origin is excluded;
alpha>=1 ensures it is unvisited from admitted positive initial energy. The
finite CDF backend currently requires integer alpha, and may return UNKNOWN
under honest resource/precision limits.
