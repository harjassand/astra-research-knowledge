# Local energy/occupation admission for quantum faults
31 October 2026

## The earned operation

This package supplies a checked local high-order fault-amplitude admission, plus an executable compiler for a declared finite model. It goes beyond a mean jump count or marginal error bound: every selected set of circuit locations receives an inclusive amplitude bound of the form eta^k, with no total-device-size factor. Coherent source transport and all exterior interactions remain ON.

The source has local loss, bounded ongoing excitation and occupation-controlled unwanted interactions. Its initial finite quantum state may be warm, entangled and correlated with the system/reference. The loss/injection reservoir inputs are initialized as required by the stated Markov model. No pure source preparation, repeated source reset, private Pauli keys, Gaussian bath approximation or inference of product faults from marginals is used.

In physical units the reviewed resource corollary gives

    eta <= 16 exp(1/4) c g (1+a tau)/(gamma lambda),

under its explicit contour-radius condition. Here c is actual unwanted coupling strength, lambda the loss lower bound, gamma the loss-relative transport margin, g the maximum sources assigned to a location, a the physical injection bound and tau the maximum location duration. Actual integrated control mismatch is separately charged. eta is an AMPLITUDE parameter, not a Pauli probability or a newly established threshold.

Ordinary non-Markovian fault-tolerance machinery is the consumer. Its code, preparations, recovery, readout, support and control premises remain real requirements. This package does not construct a laboratory device or prove that a chosen numerical eta is below an applicable hardware threshold.

## What makes the proof work

A backward product occupation weight controls one COMMON complex-parameter jump-history dilation, not separately normalized trajectory channels. The source loss/transport inequality bounds the logarithm of its norm by the number of selected locations, rather than total source volume. Multivariate Cauchy extraction then controls every inclusive selected fault amplitude. The initialized-isometry domain is explicitly bound by the review; no arbitrary incoming field state or arbitrary unitary-extension norm is claimed.

The stated dark, non-source-creating interaction structure and bounded activation are essential. Fixed-diffusion/source-creating interactions are not silently covered. A large source bandwidth alone is not charged when it cancels from the actual weight inequality, but actual transport and activation costs remain.

## Read the bound sources together

All science files below are in local_energy_fault_admission_20261031:

- QUANTUM_OCCUPATION_LOCAL_ADMISSION_CANDIDATE.md and INDEPENDENT_LOCAL_ADMISSION_REVIEW.md: complete microscopic proof and its initialized-field/receiver qualifications.
- LOSS_TO_COUPLING_RESOURCE_COROLLARY.md and LOSS_TO_COUPLING_INDEPENDENT_REVIEW.md: optimized physical units, including the paid control cap. The fixed-radius exponential dependence on a tau need not be paid when the contour is optimized.
- KNOWN_MODEL_COMPILER_SPEC.md, acquire_local_admission.py and KNOWN_MODEL_COMPILER_INDEPENDENT_REVIEW.md: actual exact-rational input acquisition and externally bound certificate verification. The final specification-only binding at the end of the review is intentional.
- SHARED_SPECTATOR_GUARD_EXTENSION.md and SHARED_SPECTATOR_INDEPENDENT_REVIEW.md: an independently checked corollary allowing bounded operator-valued transport and arbitrary spectator memory/dynamics under the stated propagator/domain premises. It removes a need to acquire the spectator spectrum CONDITIONALLY on genuine guarded interactions and acquired coefficient norms. It does not create those guards. The rank obstruction and unguarded-coupling counterexample are retained.
- GUARD_BANDWIDTH_AND_ACTIVITY_NOTE.md and GUARD_ACTIVITY_INDEPENDENT_REVIEW.md: canonical loss/injection mean and exponential-moment accounting. Cooling bandwidth is distinct from jump activity. Neither is automatically heat, power or engineering feasibility; if injection grows with loss, that resource dependence must be paid.
- PRIMARY_COMPARISON_AND_CONSEQUENCE_BOUNDARY.md: actual strong prior comparison and limits.

The raw-local-operator acquisition framework and an unreviewed explanatory expansion are deliberately excluded. The executable accepts the stated qubit occupation grammar; it does not automatically receive the shared-spectator, qutrit or raw-matrix generalizations. Names still containing 'candidate' are historical; exact source-bound receipts govern only their stated versions.

## Executable capability and paid costs

The compiler reads an explicit graph OR an explicitly defined uniform-chain finite program; global occupation-times-Pauli couplings; a complete gate/idle schedule; declared control-error evidence; and an externally supplied consumer amplitude budget. It derives local bounds and rejects source creation, missing idle exposure, simultaneous source fanout and cross-patch couplings. It does not omit exterior nodes to manufacture a local estimate.

A separate external specification is mandatory for verification. Control-evidence and consumer-contract hashes are bound, NOT inspected or authenticated. PASS is conditional mathematical admission for the declared model. A consistent NOT_ADMITTED record can verify as a record but is not admission; use verify_admitted or the CLI --require-admitted option when PASS is required. Rejection does not prove that no better construction exists.

Verified examples:

- Four explicit sources and three edges: eta=27/1749979, below the supplied 1/10000 budget.
- A known finite program for a million-source open chain: eta=9/262499993, below the supplied 1/1000000 budget, with no exponentially large source-state table. This is NOT acquisition of a million unknown couplings.
- An explicit 10,000-source graph is actually inspected vertex-by-vertex and edge-by-edge. Input length, exact arithmetic and schedule checks are paid.

The displayed benchmark timers start with parsed specifications; they exclude fixture construction, file I/O and physical calibration. Gate synthesis, preparations, source implementation, routing, reset/readout and the downstream fault-tolerant computation are not supplied by a fast classical certificate check. Large declared loss/coupling ratios have not been experimentally realized here.

## Strong comparisons and limits

The raw integrated-Hamiltonian test fails the sample budgets, but failure of one sufficient test is not a lower bound against all conventional methods. Ng–Preskill already gives microscopic Gaussian correlation admission beyond raw high-frequency operator norms. AGP/AKP, leakage-reduction theory, randomized compiling and accessible Astra receivers retain their own stronger operations where applicable. Our ordinary consumers may use this derived occupation certificate; doing so does not erase that ingredient, but its historical originality and practical advantage remain unestablished.

The meaningful research result is a constructed local certificate and compiler, not a new threshold, universal noise model, physical guard factory, or civilisation-changing breakthrough claim.

## Reproduce and distinguish evidence

The compiler/test suite uses the Python standard library. Source-dynamics diagnostics additionally use NumPy/SciPy and double precision. Their small Gram/effect tests are not certified numerical bounds; the ordinary operator proof supplies the theorem. The qutrit weight diagnostic does not by itself upgrade the received qubit-transport theorem.

Read-only certificate checks from the archive root:

    python3 local_energy_fault_admission_20261031/acquire_local_admission.py local_energy_fault_admission_20261031/explicit_fixture_input.json --verify local_energy_fault_admission_20261031/explicit_fixture_certificate.json --require-admitted
    python3 local_energy_fault_admission_20261031/acquire_local_admission.py local_energy_fault_admission_20261031/million_source_fixture_input.json --verify local_energy_fault_admission_20261031/million_source_fixture_certificate.json --require-admitted

Run test_acquire_local_admission.py, check_acquisition_independent.py and benchmark_local_admission.py only in a disposable copy: some scripts rewrite outputs. The supplied suite passed 93 checks and the independent suite 149 checks. Root also full-read code/specification and reran the supplied suite without changing its records. Numerical diagnostic counts have their separate scopes.

All copied scientific files are unchanged. MANIFEST.json records their exact SHA-256/byte lengths and the README. The ZIP membership and CRC were checked, and the two saved certificates were verified from a clean extraction. Hashes establish integrity, not scientific independence by themselves. No physical equipment, publication, external outreach or source modification occurred in preparing the package.
