# Transactional regeneration tail certificate

- `ACTUAL_RESET_INSTRUMENT_TAIL.md`: bounded local paths from arbitrary dirty/full-alphabet states, finite-rate monitor success probability, and actual no-terminal-or-abort-reset CP diamond tail.
- `JOINT_LOCAL_LYAPUNOV_TAIL.md`: finite-support killed-generator witness and spatially extensive joint tails, including interacting exteriors.
- `check_reset_paths.py` / `.json`: exhaustive 58,320 full-alphabet path checks and 44,550 short C/R path checks against the supplied transactional generator fixture snapshot.
- `transactional_flags_source_snapshot.py`: unchanged snapshot of construction worker's clock-transition regression source, retained for reproducibility. Running the path regression executes only the transition-definition prefix, not the snapshot's original output-writing main block.

Status: mathematical construction under the explicit local generator, bundled-reset, and finite-rate monitor assumptions. The clock-edge regression passes. No independent review receipt is claimed here. No DATA-instrument serialization, logical-data threshold, or passive thermal memory conclusion is claimed.

The killed maps delete only the gain terms of ACTUAL separately recorded target resets and retain their losses. Structural bad-weight contraction is not used as a proxy for reset occurrence. Distinct A_k/C0 and disabled cleanup in all R phases are material changes from the prior model; no old C-to-A rollback is reused.

Reproduce: `python check_reset_paths.py`.
