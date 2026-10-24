# Replay without changing the frozen packet

Use the Python/NumPy versions recorded in SEED_FACTORY_SOURCE_BINDINGS.json. No package was installed. Copy all manifest payloads into a NEW scratch child directory within w64's own worker folder before running anything: diagnostics overwrite their local output filenames and creation timestamps. Keep the original packet and all earlier manifests untouched.

In that copied directory, run sequentially:

    python3 coherent_sector_checks.py
    python3 seed_preserving_factory_checks.py
    python3 three_call_classifier_exact.py
    python3 native_depth_kernel_checks.py
    python3 rational_seed_factory_certificate.py

The first two runs keep every sparse native amplitude/source column but use only small classifiers; mathematical-adjoint and literal-positive-power cases are explicitly separated. The exact run checks quadratic-field normalization after every block and writes20outward-bracket error rows. The separate native kernel run checks54sector cases and12crosschecks against the exact rows. The final run verifies the integer square inequalities and full-channel rational certificate. Assertions are the numerical/finite-algebra acceptance conditions; full proof validity still needs independent reading.

Timestamps and wall-clock times differ on replay. The exact A/B polynomial coefficients, rational inequalities, call counts and certificate bound are deterministic. Floating sparse residuals may vary by platform and must stay within the script's explicit tolerances. The current record's total diagnostic wall time is about18.58seconds across these individual runs, excluding derivation, literature, earlier failed approaches, earlier review/testing and report construction. That sum is a recorded local computation cost, not a hardware execution time or claimed complete scientific development cost. All physical/source calls in these scripts are ZERO.

Check FROZEN_SEED_FACTORY_PACKET.json against original payload bytes before reviewing. Its own digest is delivered separately to root. Exact integer arithmetic verifies the finite statistics; it does not replace the native Kraus derivation, operator-extension proof, common-phase check, controlled uploader composition, primary comparison or full fresh criticism.
