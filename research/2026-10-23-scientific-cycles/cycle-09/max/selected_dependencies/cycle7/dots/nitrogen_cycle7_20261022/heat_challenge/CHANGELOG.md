# Changes

- 2026-10-22: Initial heat challenge, conditional inventory ledger and calculation script delivered.
- 2026-10-22: Added finite-approach two-end bounds, interior-pinch feasibility condition and unchanged-feed-state no-credit result before first final delivery.
- 2026-10-22: Kept the delivered report unchanged; added THERMO_INPUT_PROOF.md, portable hashed digitization, transcribed NIST coefficient input, exact rational interval/integral/speciation verifier, raw results and measured child execution resources. Updated check_ledger.py to use the local pinned input; preserved original as check_ledger_v1.py. Ledger numerical outputs unchanged.
- Verification execution: /usr/bin/time was unavailable, so used a Python child-process resource wrapper. The first exact-rational verifier had an integer-zero/float denominator comparison failure; forced Fraction conversion fixed it. Retained failed output and resource record, then recorded successful rerun. No thermodynamic result changed.
