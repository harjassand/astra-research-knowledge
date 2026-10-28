# Astra P2: finite causal bosonic memory

Research checkpoint, 28 October 2026 UTC / 29 October 2026 Australia/Brisbane.
This directory extends the frozen `p2_adaptive`, `p2_memory` and `p2_next`
tranches. It preserves proofs, executable work, exact certificates,
numerical diagnostics, actual independent internal reviews and failures.

## Main result

The completed construction converts a specified family of infinite,
non-Gaussian repeated bosonic contacts into finite, causal, completely
positive memory maps. For fixed bounded Weyl action, bounded fresh thermal
occupation, prescribed strict passive contraction and a stable first mean,
the retained memory dimension sufficient for a J-contact compression
allowance epsilon is `O(log^2(J/epsilon))`. Thermal/vacuum startup or a
separately paid initial treatment is required. Exact passive full swaps
give an output-tail statement even for arbitrary normal incoming memory.

The construction retains source–memory correlations and actual records.
It does not physically reset the retained mode, assert finite Markov order,
or make a growing quantum computer classically inexpensive. A finite
Hamiltonian compiler and an independently enclosed quantum prediction make
the representation constructive rather than merely existential.

Read [CAPITAL_CHECKPOINT.md](CAPITAL_CHECKPOINT.md) for the scientific
choice, mechanism, consequences, error ledger and remaining frontier.
[SOURCE_SCOPE_AND_CORRECTIONS.md](SOURCE_SCOPE_AND_CORRECTIONS.md) records
source ancestry and the corrections actually required in review.

## Proof and actual-review map

| Construction | Governing proof | Actual independent review |
|---|---|---|
| Exact output-port regeneration | [OUTPUT_PORT_REGENERATION.md](compact/OUTPUT_PORT_REGENERATION.md) | [PORT_REGENERATION_REVIEW.md](faults/PORT_REGENERATION_REVIEW.md) |
| Partial-swap windows and causal quantum detectors | [WINDOW_REGENERATION.md](compact/WINDOW_REGENERATION.md) | Same port review; coordinate-order correction incorporated |
| Finite Hamiltonian and CPTP contact compiler | [FINITE_CONTACT_COMPILER.md](root/FINITE_CONTACT_COMPILER.md) | [FINITE_CONTACT_REVIEW.md](compact/FINITE_CONTACT_REVIEW.md) |
| Analytic quantum witness | [QUANTUM_PORT_WITNESS.md](root/QUANTUM_PORT_WITNESS.md) | Same finite-contact review |
| Complete-process, tensor and finite-source consequences | [CAUSAL_MEMORY_CONSEQUENCES.md](root/CAUSAL_MEMORY_CONSEQUENCES.md) | [CAUSAL_CONSEQUENCES_REVIEW.md](compact/CAUSAL_CONSEQUENCES_REVIEW.md) |
| Enclosed infinite-model observable | [CERTIFIED_QUANTUM_CONTACT.md](certified_solver/CERTIFIED_QUANTUM_CONTACT.md) | [CERTIFIED_SOLVER_REVIEW.md](reviews/CERTIFIED_SOLVER_REVIEW.md) |
| Executed 100-contact floating diagnostic | [program](root/quantum_contact_diagnostic.py), [results](root/quantum_contact_diagnostic.json) | [QUANTUM_DIAGNOSTIC_REVIEW.md](compact/QUANTUM_DIAGNOSTIC_REVIEW.md) — diagnostic only |
| Exact classical reduction of real-quadrature baseline | [ABELIAN_CONTACT_REDUCTION.md](faults/ABELIAN_CONTACT_REDUCTION.md) | [ABELIAN_CONTACT_REVIEW.md](statistics/reviews/ABELIAN_CONTACT_REVIEW.md) |
| Conventional thermal-resource/counting alternative | [THERMAL_WORKLOAD_GEOMETRY.md](statistics/THERMAL_WORKLOAD_GEOMETRY.md) | [THERMAL_WORKLOAD_REVIEW.md](reviews/THERMAL_WORKLOAD_REVIEW.md) |

Each review has an adjacent `_REVIEW_RECEIPT.json` pinning its subjects and
scope. Creation-time headers such as “pending review” remain in frozen
authored files. The separately version-pinned review receipts give their
final status. These are internal scientific reviews, not external peer
review, proof-assistant verification or priority claims.

## Executable work

The saved JSON files and logs are completed executions. To replay without
overwriting reviewed artifacts, copy the relevant program and companions
into a fresh scratch directory, then run that copy.

| Program | Required companions | Output / scope |
|---|---|---|
| `compact/port_tail_certificate.py` | None | Standard-library exact arithmetic; nine dimension schedules |
| `root/finite_contact_certificate.py` | None | Standard-library exact arithmetic; three contact certificates and analytic quantum lower bound |
| `certified_solver/certify_quantum_contact.py` | None | Standard-library integer/rational enclosed source-Z calculation; matrix and final integer vectors |
| `root/quantum_contact_diagnostic.py` | `finite_contact_certificate.py`; NumPy and SciPy | Floating joint-memory/reference/record propagation through 100 contacts |
| `faults/abelian_contact_certificate.py` | NumPy and SciPy | Analytic support certificates plus floating Gaussian/Fourier comparison |
| `statistics/thermal_workload_certificate.py` | `thermal_interval_math.py`, `thermal_counts.json` | Exact directed count-confidence and thermal-model certificate; no physical data |

For example, from the workspace root:

```bash
replay_dir=$(mktemp -d producer-workspace/astra-contact-replay.XXXXXX)
cp p2_opening/certified_solver/certify_quantum_contact.py "$replay_dir/"
python "$replay_dir/certify_quantum_contact.py"
```

Independent audit programs, separate implementations and isolated replay
artifacts are retained beside the reviews. The longer diagnostic used
NumPy 2.3.5 / SciPy 1.17.0 and has no enclosed numerical error. The
one-contact source-Z calculation encloses arithmetic as well as truncation.

## Preservation

`verify_package.py` is read-only: it checks the three frozen predecessor
manifests, seven principal scientific review receipts, the separate final
synthesis audit, document links and the new
manifest. `PACKAGE_VALIDATION.json` records the completed check;
`MANIFEST_SHA256.json` pins this tranche. Bytecode caches are excluded.
No predecessor regeneration scripts were run. There is no new duplicate
archive, physical experiment or ongoing job. The manifest excludes itself,
`PACKAGE_VALIDATION.json` and bytecode; the validation record pins the
manifest's hash to avoid a circular checksum.
