# Astra P2: calibrated nonlinear memory instruments

29 October 2026, Australia/Brisbane. Predecessor `p2_adaptive/` and
`p2_memory/` remain unchanged. No replacement archive or duplicate export.

Start with **CAPITAL_CHECKPOINT.md**. Ordinary proofs and executable work:

| Construction | Governing file | Actual internal review |
|---|---|---|
| Complete source kernel comparison | root/KERNEL_ORDER_COMPLETE_PROCESS.md | challenger/KERNEL_ORDER_REVIEW.md |
| Count-only Weyl acquisition | predictive/WEYL_COUNT_CALIBRATION.md | physical/WEYL_CALIBRATION_REVIEW.md |
| Gaussian/thermal/mean extension | root/GAUSSIAN_START_TRANSFER.md | challenger/GAUSSIAN_START_REVIEW.md |
| Unseen-mode and sharpness boundaries | physical/UNSEEN_MODE_MOMENT_OBSTRUCTION.md; challenger/SHARPNESS_ACTION_AND_KERNEL.md | reviews/ROOT_BOUNDARY_REVIEW.md |
| Concurrent thermal contact | physical/CONCURRENT_THERMAL_MEMORY_INTERFACE.md; physical/CONCURRENT_CONTACT_ASSUMPTIONS.md | reviews/CONCURRENT_THERMAL_MEMORY_REVIEW.md |
| First-moment row and memory composition | challenger/THERMAL_CONTACT_FIRST_MOMENT_SENSITIVITY.md; root/REUSABLE_ANCHORED_MEMORY.md | reviews/REUSABLE_ANCHORED_MEMORY_REVIEW.md |
| Three-X anchored inverse | physical/ANCHORED_THERMAL_CONTACT_CALIBRATION.md | challenger/ANCHORED_ACQUISITION_REVIEW.md |
| Causal collection/detection | root/DETECTOR_CLOSED_REUSE.md | physical/DETECTOR_CLOSED_REUSE_REVIEW.md |
| Intervals compiled into reuse | root/ANCHOR_REUSE_COMPOSITION.md; root/compile_anchor_reuse.py | reviews/ANCHOR_REUSE_COMPILER_REVIEW.md |

Reviews have their own receipts and, when appropriate, independent arithmetic
and isolated execution. These are actual internal reviews, not external
peer review or proof-assistant certificates.

`CLARIFICATIONS_AND_BOUNDARIES.md` collects corrections and interfaces.
`PRIMARY_SCOPE_AND_CHOICE.md` records the selection and primary comparisons.
Current Astra texts/notices are in `predictive/sources/` and `physical/ASTRA_*`,
with source manifests and scoped reading records. The continuum-bus work
in `quantum_bus/` is authored/executed but not independently reviewed.

## Executable entry points

From the shared workspace, these standard-library exact programs overwrite
only their own receipts/logs when explicitly rerun:

```sh
python p2_next/root/kernel_order_certificate.py
python p2_next/predictive/weyl_count_certificate.py
python p2_next/root/gaussian_start_certificate.py
python p2_next/physical/concurrent_contact_certificate.py
python p2_next/challenger/first_moment_contact_certificate.py
python p2_next/root/reusable_memory_certificate.py
python p2_next/physical/anchored_contact_certificate.py
python p2_next/root/compile_anchor_reuse.py
```

The coherent-history numerical diagnostic uses NumPy. Its floating roundoff
is diagnostic, not interval-certified; no theorem depends on that simulation.
The kernel count fixture is synthetic. The new anchor boxes are declared,
with ZERO new shots and no attached confidence coverage.

`verify_preservation.py` checks predecessor manifests and frozen pins
without rerunning accepted science. The source manifest excludes generated
Python caches and itself. No background execution is implied by the package.
