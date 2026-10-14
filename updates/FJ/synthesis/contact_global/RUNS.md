# Replay and experiment receipts

Environment: macOS; `Python 3.14.3`; `SymPy 1.14.0`. No SciPy/optimizer, network, external source, or unbounded search was used. For the Fourier algebra commands, `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1` were set.

1. Inspected the complete supplied `verify_contact_compensation.py`, copied it into this directory, changed only the generated JSON filename, then ran:

   ```text
   python3 work/FJ-contact-global/verify_contact_compensation_replay.py
   ```

   Result: all 9 exact groups passed; receipt `contact_verification_replay.json`. This replays finite algebra and rational integration. It does not certify the analytic interpolation or universal theorem.

2. Ran:

   ```text
   OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 work/FJ-contact-global/near_contact_modes.py
   ```

   Result: exact Laurent-Fourier moments, covariance ranks, Hessian blocks, Schur complements, and optimized gaps were written to `near_contact_modes.json`. Assertions verify the rotating-line ratio (h_*/h\to0), the resonant-family leading constants and positive polynomial coefficients, and the exact positive gap limits. Exit status was 0.

3. Ran:

   ```text
   OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 work/FJ-contact-global/scan_resonant_contacts.py
   ```

   Result: 10 exact rational parameter/sign variants of the resonant rank-one-mode family were checked; no case had a nonvanishing limiting reduced Schur loss. The summary is `scan_resonant_contacts.json`. This small grid is a falsification probe only, not exhaustive evidence.

4. Ran:

   ```text
   python3 work/FJ-contact-global/verify_concentration_escape.py
   ```

   Result: exact rational scaling identities for the source localized profile passed; receipt `concentration_escape_checks.json`.

All exact identities refer to the explicitly encoded Fourier families and fixed (G). The source-level contact and rank-one-convexity claims remain internally derived/unreviewed as recorded in the incoming note and N800/N803 dossiers.
