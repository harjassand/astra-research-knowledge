# Monitored phase-resource operation: strongest ordinary construction

Read `CONTROLLED_PHASE_RESOURCE_AND_RECEIVER.md` for the exact finite-rate all-graph operation, full cost ledger, source/port/locality premises, detector dead time, thermal channels/dark counts, ordinary Bayesian decoder, omitted-endpoint alternative, exact echo comparator and physical-receiver boundary. It is an author candidate pending independent review.

Result: ordinary environment-assisted correction already supplies this commuting operation. No novel paid quantum capability or physical receiver has been demonstrated. The useful earned simplification is that a cold-source photon-only receiver can omit the terminal source measurement entirely, paying the finite source-excitation remainder instead. The generic observable-admission theorem is not needed for this special task, and its arbitrary-initial-correlation scope is not inherited.

Files:
- `monitored_phase.py`: ordinary floating finite-source detector instruments, exact formula implementations, diagnostic parameter sweep. No trajectory sampling or hardware simulation claims.
- `certify_receiver.py`: rational/Gaussian-integer finite-model channel-risk enclosures. Includes no-record and ideal echo comparators; no floating expm enters certificates.
- `receiver_certificates.json`: exact enclosure records and decimal displays for the stated parameter grid, including photon-only operation.
- `sweep_diagnostic.json`: wider floating-only grid; ordinary echo wins in some regimes. Not rigorous numerical bounds.
- `test_monitored_phase.py`, `test_results.json`: exact frame/CQ identities, higher-precision exact replay, independent full physical source+data+detector diagnostics including thermal up jumps and dark counts.
- `MANIFEST.json`: explicit file-byte/SHA256 binding, excludes itself.

Replay (preserve accepted snapshots if later reviewed):

```
python certify_receiver.py
python monitored_phase.py > sweep_diagnostic.json
python test_monitored_phase.py
```

Python dependencies: NumPy, SciPy and SymPy. Only the certificate path uses exact arithmetic; diagnostic paths deliberately use floating exponentials. The code is an ordinary research calculation, not a hardened untrusted-input API or a physical-model acquisition tool. No original source files outside this directory were modified.
