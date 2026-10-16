# Portable reproduction and safe default

This packet contains independently written source and saved research results, not machine binaries or downloaded author code. Reading the JSON/Markdown and checking artifact hashes performs no simulation. No script is set to run automatically. The completed experiments are frozen; rerunning them is optional and must be an explicit decision.

## Source versions

ORIGINAL_VERSION_MANIFEST.json identifies each version and SHA256 source hash:
- simulator.cpp: original equal-attempt dynamics and D0 readout; phases1–2.
- simulator_equalreads.cpp: separately reviewed correction multiplier; phase3.
- simulator_readouts.cpp: separate endpoint export and D0/D1/D2 syndrome-only readouts; phase4.

The SHA256 records that include executables document the original checked environment; binaries are intentionally excluded from the portable packet. Rebuilt executable hashes can differ with compiler/platform. Source hashes and saved JSON hashes remain directly checkable.

## Optional local compilation and deterministic tests

Requires an already installed C++17 compiler and Python3 standard library; no package installation is needed.

    g++ -O3 -std=c++17 -Wall -Wextra simulator.cpp -o simulator
    ./simulator test

The selftest is deterministic algebra/geometry, not a new stochastic memory experiment. Equivalent compilation commands apply to the two separately named later sources. To test all alternative single-face recoveries, compile check_readouts_allfaces.cpp after placing it beside simulator_readouts.cpp. Its include-and-rename harness can emit an unused-function return warning; the invoked deterministic test function itself returns normally and recorded assertions passed.

## Saved results first

Read PILOT_RESULTS.md, PHASE2_RESULTS.md, PHASE3_RESULTS.md and PHASE4_RESULTS.md in sequence. They distinguish normalization, sampling, stopping conditions and post-hoc selection. Manifest and raw JSON files preserve exact parameters, seeds, RNG, event counts, readout choices and timings. The final diagnostic was selected after a failure had been observed; its policies were fixed before the replay and receive S only. It is not an unbiased additional performance sample.

## Optional reruns require an explicit decision

run_pilot.py, run_phase2.py, run_phase3.py and run_phase4.py are archived reproduction recipes, not startup scripts. They overwrite their own phase output files, so copy the packet to a new working directory first. Their gate/hash checks intentionally pin the historical reviewed binaries. A locally rebuilt binary requires fresh review and an explicitly updated hash in a new run copy; do not edit the archived manifests or silently disable checks. The older run_pilot.py relies on its gate file and the accompanying manifest; later runners additionally enforce executable hashes.

The original phase caps were180CPU seconds for phase1,180 for phase2,90 for phase3 and45 for phase4, with1GiB address limits. These are bounds, not a request to launch any rerun. Do not automatically launch larger lattices, more seeds, time sweeps or parameter optimization.

## Exact endpoint/recovery format

Phase4 endpoint files use format4d-memory-endpoint-v1 with L, rates, seed, method, multiplier, index order, sparse E face IDs and sparse S edge IDs. IDs are orientation-major, vertex axis0 slow, face orientations01,02,03,12,13,23. Decoder input is only S. Recovery files use format4d-memory-recovery-v1 with sparse R. E is accessed only afterward to check boundary(E)=S and score closed E+R. PHASE4_ENDPOINT_SHA256SUMS pins both endpoint files and all six recoveries.

## Claims intentionally not made

These experiments are ideal instantaneous one-sector Pauli trajectories with perfect readout. They are not a finite-gate/shared-bath theorem test, hardware-equivalent resource comparison, threshold estimate, exponential lifetime demonstration, population-level method ranking or proof of irreversible information loss. D1/D2 agree with D0 on strict-good-case inputs; preserving that local certificate is distinct from an unrestricted theorem extension.
