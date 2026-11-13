# Exact-integer finite-grid sampling candidate

## What is supported
A capped exact-arithmetic trajectory sampler for a **specific** noisy 32×32 grid circuit, 100 matching layers, pair-reset probability 3/100 and rare-gate probability 1/50. A frozen, predeclared 1,000-draw holdout had zero resource aborts. The exact-binomial-verified one-sided 99% upper confidence limit on the abort probability is 919/200000 = 0.004595. Conditional on the mathematical reduction and ideal unbiased random-bit assumptions, the fallback sampler has total-variation error at most its abort probability. This is a finite-setting statistical statement, not a deterministic error certificate, independent formal verification, novelty claim, or polynomial scaling theorem.

Average end-to-end wall time was 0.7616 seconds per draw on the research host. Maximum observed component support was 256 amplitude entries; maximum amplitude integer length was 1,070 bits. These measurements do not include a platform-independent performance guarantee. Payload counters exclude Python object overhead and transient memory.

## Exact model
Input is |0> on every site; output is the complete computational-basis bit string. Four disjoint matching layers cycle horizontal-even, horizontal-odd, vertical-even, vertical-odd on an open even square grid. At each pair independently:
- probability 1-r-epsilon: D=(3I+4i ZZ)/5;
- probability epsilon: QD, Q=(12I-5i XX)/13;
- probability r: trace both qubits and replace them by I/4.
No postselected physical outcomes, approximate gates, resampled successful category records, or omitted coherent components are allowed.

## Method and correctness boundary
The reset-segment multigraph keeps each rare-Q occurrence as a distinct edge. A graph bridge cannot participate in any surviving ket/bra interference cycle after all original reset Z outcomes and final outputs are recorded. Its Q can therefore be replaced, for this joint output law only, by a classical local XX with probability 25/169. This is not a quantum channel identity and does not permit independent simulation of separate cycle blocks. Remaining components are evolved jointly with Gaussian-integer amplitudes. Diagonal gates merge components when required. Measurements retain correlations among all unmeasured sites. Terminal-Q Z measurements can be performed early; their classical outcomes continue to control later diagonal phases.

The sampler aborts to a fixed all-zero output before exceeding 4,096 component entries or 20,000 amplitude bits. Uncapped mathematics is exact. All approximation from these resource caps is bounded by abort probability. Large-integer operations and random integer draws are included in runtime. Experimental randomness used independent OS-seeded Python PRNG streams; the exact sampling theorem uses ideal unbiased randomness.

## Limitations and comparator
At epsilon=1/20, all 20 of the corresponding 1,024-qubit pilot draws aborted. This package does not solve that regime. At epsilon=1/50 a matched five-record strong direct compact MPS baseline was faster on average (~0.559 s versus ~0.683 s for the exact component implementation); both succeeded on those five records. The exact-integer distinction is arithmetic/control of approximation, not established speed superiority. MPS had four aborts in five matched epsilon=1/20 records; our exact sampler had five. Tiny pilot counts are descriptive only.

The source code is research code and proof notes are not peer reviewed. Tiny exact checks validate algebra and chronology, not all implementation paths or asymptotic scalability. No civilisation-level capability, general noisy-circuit simulation, or hardware quantum-computing advance is claimed.

## Reproduce
Run all commands from this package directory. Python 3 with numpy, sympy, scipy is required. No network/service access is needed.

1. `python verify_package.py` verifies copied-source hashes, both frozen-source original hashes, all 1,000 recorded seeds/results, the exact rational confidence inequality, and replays three recorded draws. It does not overwrite records.
2. `python research_notes/north_compute_20261113/bridge_dephasing/check.py` reruns exact rational bridge tests.
3. `python research_notes/north_compute_20261113/affine_sampler/exact_gaussian_backend.py` reruns exhaustive tiny original-channel comparisons.
4. `python replay_holdout.py` replays all 1,000 recorded seeds and checks outputs/resource aborts; expect about 13 minutes on the original host.
5. `python research_notes/north_compute_20261113/affine_sampler/matched_mps_baseline.py` reruns the five paired category-record comparisons at both rates. It overwrites its local result JSON; save the supplied recorded version first if desired.

The original `holdout_v1.py` is preserved as provenance only: it generates NEW seeds and appends to the raw record. Do not run it in this evidence directory. Use replay_holdout.py for reproduction. Paths inside the original protocol identify the original host and are provenance, not required access paths.

Proof notes: `bridge_dephasing/THEOREM.md`, `affine_sampler/WORKING_EXACT_COMPONENT_SAMPLER.md`, and `mps_error/TRAJECTORY_TV_CERTIFICATE.md`. Evidence: `affine_sampler/holdout_v1_protocol.json`, `holdout_v1_raw.jsonl`, `holdout_v1_result.json`, `exact_component_benchmark.json`, and `matched_mps_baseline.json`.
