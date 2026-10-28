# Source costs, conditioning and replay

## Completed computation

All new work used the existing local Python runtime, with BLAS/OMP threads1.
The times below are each script's reported computational wall time; startup,
reading, derivation and documentation are additional. They are not a CPU-time
or optimized performance benchmark.

| Stage | Seconds | Acquired numerical information |
|---|---:|---|
| Contact-jet source and unchanged uniform control | 7.173 | Complete open n2..6 Kubo/equal-time Sz/D forms |
| Exact contact algebra, literal histories and dimer limits | .115 | Nine exact spin identities; D/K identities; finite controls |
| Two finite bilocal separations and matched controls | 1.350 |17 distinct integrated three/four-point correlations |
| One augmentation of the frozen ten-vector span | 3.502 |32 additional three-point cross correlations;16 full eigensystems |
| Same49 sources, Gauss32 convergence replay | 6.023 | No new source family;8960 ordered-word trace calls |

The first bilocal stage used4356 ordered-word traces, including its controls;
augmentation used3136. An ordered-word trace sums ALL initial magnetization
sectors and follows every ladder transition. These are not4356/3136
single-eigenvalue or low-energy evaluations. The two bilocal separations
share each full eigensystem.

New four-point forms have at most625 physical states (n4, largest M block85).
New three-point cross forms have at most3125 states (n5, largest block381).
The contact-jet/control second form still uses the full15625-state n6 source,
largest block1751. No p8 physical system was acquired. Full eigenvectors,
observable transforms and dense propagator products cost additional storage;
peak RSS was not instrumented.

Gauss8 versus16 differences reach4.82e-8 relative in the augmented source.
Checking every SAME source at Gauss32 reduces the maximum16/32 discrepancy
to3.03e-15. This addresses numerical stability of the preview; it does not
turn convergence into a rigorous quadrature interval. Small negative residual
Gram eigenvalues at roundoff scale are retained in the output, not clipped
into a claimed certificate.

## Prior data are not free oracle inputs

The frozen ten-vector source already required75 Kubo/equal-time trace pairs
and33.771 seconds in its recorded run. The full six-site spin-list moment
preview used33 distinct complete angular spectra (49.943 seconds), and the
ordinary scalar26-vector control took3.990 seconds. Those are pre-existing
numerical acquisitions, separately receipted in the frozen sol10 directory;
they are reused, not reacquired or silently assumed exact here. Their own
cost report also charges earlier source families and prior exact work.

The present twelve-vector comparison preserves the old ten-by-ten blocks
exactly, uses only the two new time features, and records all cross sources.
It is not an additional fugacity search. The same source/eigensystem
information is supplied to the unprojected comparator. That comparator can
be cheaper if run alone because it need not perform the global-time integral.
No speedup follows from sharing eigensystems in this experiment.

MED, BS-CMI, thermal-MPO, QBP and ordinary response/Galerkin methods remain
entitled to the same Hamiltonian, boundary, beta and precision information.
This test compares actual source spans; it is not a completed end-to-end
benchmark against those methods and makes no superiority claim.

## Conditioning and precision debt

The projected old/new Gram conditions are2.65376e5 and4.44189e5. All12 modes
survive cutoffs1e-8,1e-10,1e-12. Leading-Ritz coefficient l1 squared/G norm
grows3.58→51.33; minres amplification grows3.11→24.05. Those amplification
factors must multiply any common entrywise source-error budget before a
validated quadratic-form claim. The small variance gain is not free accuracy.

The available validated Kubo/Sylvester interface covers the contact jet's
two-point observable forms, with norm bounds ||D||<=72 at beta3 and
||K||<=324 on its shared dimer. It has not acquired this complete source
family. Finite bilocals require additional three/four-point observable
transport, complete cross-M bookkeeping and rigorous piecewise integration.
No generic two-point certificate, floating-point eigensystem, or degree32
agreement is substituted for those missing physical-input enclosures.

Both scalar endpoints are retained. The best numerical ratio interval is
[.91042383,.98314539]; its resulting connected width .07536514 is101297 times
the required7.44e-7. The all-other-mode tail is only1.39116e-18. At the
current upper endpoint the local relative-ratio tolerance is3.96e-8, whereas
the preview's relative ratio width is7.99%. A conditional current-Temple
target would require another3.810-fold variance reduction, far beyond this
family's2.68% reduction. No costly source validation was justified.

## Replay

Run from the workspace root; commands write only this owned sol11 directory.
The frozen sol10 builder/inputs and sol9 A5 moment file are read-only
dependencies recorded in INPUT_RECEIPTS.json. Their manifests and full data
remain preserved in place. Sympy is used only for small exact spin identities.

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol11_operation_discovery_20261028/dominant_mode_operation/code/contact_jet_preview.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol11_operation_discovery_20261028/dominant_mode_operation/code/bilocal_time_preview.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol11_operation_discovery_20261028/dominant_mode_operation/code/frozen_span_augmentation.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol11_operation_discovery_20261028/dominant_mode_operation/code/derive_and_check_contact.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol11_operation_discovery_20261028/dominant_mode_operation/code/quadrature_stability.py
PYTHONDONTWRITEBYTECODE=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol11_operation_discovery_20261028/dominant_mode_operation/code/ratio_readout.py
```

All source entries, matrices, Ritz/minres readouts, controls and logs are
retained. Replay changes their timing fields and manifest hashes. Hashes and
replay establish version/integrity scope, not certified thermal values or a
new scientific advantage. No paid compute, physical acquisition, outreach,
automation, goal, new worker or protected-chat action was performed.
