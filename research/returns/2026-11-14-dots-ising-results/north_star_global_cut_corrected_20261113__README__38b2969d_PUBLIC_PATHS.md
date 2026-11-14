# CORRECTED EDITION: numerical implementation repair

The earlier global-cut archive contained a dynamic-rounding quotient-reuse defect. It is superseded, not silently edited. See `07_arithmetic_correction/INCIDENT_AND_REPAIR.md`. This edition uses a single rounding mode and separately bounded reciprocal powers, adds broader exact tests and explicit convolution runtime checks. The mathematical source/clock/proposal definitions are unchanged. Earlier occupation archives did not use this magnetic code.

The corrected full-recurrence receipt and final independent verification status are recorded in `VALIDATION_RUNS.md`. Do not infer that the original general enclosure argument was valid simply because a rounded headline survives recomputation.

# Global Ising cut-energy certificate and constructive proposal interface

## What is new

At theta=4, R=200, L=1600, n=2,560,000, original source core radius r=5 and original per-site rate-one heatbath clock, an explicitly defined GLOBAL trial potential has

    W_cut / Z_A <= exp(-6215).

Thus C_kappa/Z_A <= exp(-6215). The prior complete cut certificate at the same tuple was exp(-4136). This is a tighter upper certificate, NOT a computed exact capacity or a breakthrough in the full transition-time sampler.

The trial includes all configurations and every structural, target and original soft-source contribution. Its structural bound counts all permitted contour shapes via an area-weighted nonbacktracking-walk envelope, not only a regular droplet family. All positive overcounts and the omitted long-walk tail are paid.

An exact rejection identity converts this envelope plus an authorized auxiliary-core sampler into actual cut-energy edges. Root, tuple-order and gate-mark compensation are explicit. Missing inverse images and approximate sampling are charged. The auxiliary core does not replace the original source.

## Authoritative reading order

1. `01_global_cut/RESULT.md`: original global trial and inherited cut interfaces.
2. `MAGNETIC_MOMENT_REDUCTION.md`: physical trace and magnetic moments.
3. `UNROOTED_MARKED_REFINEMENT.md`: AUTHORITATIVE improved root/order/mark theorem and proposal.
4. `FINITE_RECEIPT_AND_ARITHMETIC.md`: original unmarked computation and numerical contract.
5. `ACTUAL_ENERGY_PROPOSAL.md`: error, acquisition and acceptance interface; its unmarked normalizer remains a valid conservative version.
6. `LIMITATIONS_AND_DEPENDENCIES.md`: scope, prerequisites, benchmark and unresolved steps.

Historical notes are preserved rather than silently rewritten: the unmarked receipt is exp(-6202), improved to exp(-6215) by the marked refinement. Statements in the older arithmetic note that no proposal is supplied are superseded by the later explicit proposal theorem. No large-instance backward sampler has been implemented or run.

## Reproduce

Requirements: Python 3 standard library; g++ supporting C++17, binary long double, fenv directed rounding; no downloaded packages or network needed.

    python run_checks.py

Runs exact geometry/moment/proposal checks, independently checks compiled arithmetic against Fraction calculations, regenerates both complete scalar/convolution bounds from the included large moment receipts, and regenerates the old benchmark. It works in a temporary copy and leaves distributed files unchanged.

    python run_checks.py --full

Additionally recomputes all THREE large perimeter-1900 magnetic recurrences before downstream checks. The original runs took roughly 107–114 CPU seconds each. Runtime/memory on another machine can differ. Only the full option recomputes those large recurrences; the default does not pretend to do so.

`SHA256SUMS.txt` authenticates every included file except itself. Hashes are reproducibility checks, not proof of mathematical correctness.

## Numerical result versus access/cost

At epsilon=1/100, original kappa inverse has log below 2593.6. The R200 new cut bound is therefore genuinely sharper than the trivial C/Z_A <= kappa bound. By contrast, an exploratory R80 structural improvement is not a best capacity improvement because original kappa is already smaller; R80 exploratory data are deliberately excluded.

The conservative original-clock lower certificate at R200 is exp(-6449). Combined with the marked upper, the proposal's certified expected attempt count is at most 2 exp(234), after the stated error allowances. This is enormous. A finite inequality to a power of n at this one tuple is NOT a uniform polynomial algorithm. The older executable auxiliary-core receipt retains the weaker, valid 2 exp(247) guarantee from exp(-6202).

No near-optimal W/C, uniform growing-R quality, full original physical decision-time bound, or civilization-changing capability is claimed. No R1000/R10000 magnetic moment run was executed.

## Optional same-cut acceptance witness

`06_optional_matched_cut/PROPOSAL_ACCEPTANCE_JOIN.md` improves the acceptance guarantee to exp(-21) using a separately acquired genuine subset of the SAME cut with perimeter <=1900. Its inverse image is all-minus and hence in the auxiliary core. The default runner regenerates its exact coefficient table and truncated receipt. This lower-bounds W_good, not C: it does not close near-optimality or decision time. The main conservative exp(234) argument remains valid independently.

To verify the archive manifest before and after tests:

    python verify_manifest.py
