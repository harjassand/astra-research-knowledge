# Energy-controlled logical dynamics and reset-free sign epochs
31 October 2026

## What this checkpoint earns

This package takes the source energy investigation beyond jump counts. It proves a complete logical-system error bound using actual source occupation, then constructs a positive private-sign protocol and reset-free epochs. The task retains the system, arbitrary reference and admitted system-only control records. It deliberately discards the bath and private sign registers. It is not the earlier full-source simulator, a hardware experiment, or a civilisation-changing breakthrough claim.

The strongest concrete result is a rigorously certified SAME-APPARATUS operating window for ordinary system-Z twirling. At source rate 1,000,000 and time one, with the explicitly fixed cold qutrit source:

- An explicit input and Pauli observable prove the unpaired logical error exceeds 0.0002266611872732366.
- A certified complete-channel upper bound puts the privately Z-twirled error below 0.000000988465317203069.
- Therefore tolerance 0.0001 is genuinely failed by the first and met by the second. This is not a comparison of loose sufficient rate bounds.

The matrix exponential calculation uses exact Gaussian integers and analytic norm remainders, not floating expm. The paired operation IS ordinary Z twirling; no advantage over twirling is claimed. A direct standard generalized-amplitude-damping circuit remains cheaper when the implementation may be chosen freely. The fixed-apparatus example does not demonstrate a new cooling capability or practical quantum speedup.

## Read in this order

1. SAME_APPARATUS_CERTIFIED_OPERATING_WINDOW.md with SAME_APPARATUS_AUTHOR_INDEPENDENT_CHECK.md, its exact arithmetic script, replay test and saved matrices/report.
2. ENERGY_FIRST_CORRECTOR_CANDIDATE.md with ENERGY_FIRST_CORRECTOR_INDEPENDENT_REVIEW.md. The off-diagonal corrector leaves a purely excited-sector residual, including actual recycled jumps. Its cost is controlled by the actual Lyapunov energy and the supplied injection constants. No global source inverse is assumed in that error certificate.
3. DARK_SOURCE_LOGICAL_REDUCTION_CANDIDATE.md with DARK_LOGICAL_REDUCTION_INDEPENDENT_REVIEW.md. The general complete return bound gives an analysis resolvent; the implemented effective jump stack uses the acquired positive no-jump operator, source reference preparation and interaction encoding. A norm bound is not a free optimal block-encoding normalization.
4. PRIVATE_SIGN_PAIR_REDUCTION_CANDIDATE.md with its independent review. One fresh private global interaction sign suppresses the leading finite-rate error. Both physical signs must have the same source generator and system Hamiltonian. This is a positive channel mixture, not postselection or negative-weight extrapolation.
5. RESET_FREE_SIGN_EPOCH_COMPILER_CANDIDATE.md with RESET_FREE_SIGN_EPOCH_INDEPENDENT_REVIEW.md AND RESET_FREE_SIGN_EPOCH_FINAL_BINDING.md. Uniformity over actual joint inputs permits logical-marginal composition without resetting the bath. The final source explicitly incorporates the old-controller and rounded-schedule qualifications. Error is linear in total logical time/control count with inverse-rate scaling under the stated constants. Sign-setting frequency need not track the rapid source rate.
6. RESET_FREE_SIGN_EPOCHS_AND_ACCESS_COST.md and SIGN_EPOCH_ACCESS_INDEPENDENT_REVIEW.md. Actual system involution gates can implement a sign branch where the complete interaction is odd and H0 is invariant. Gate errors are charged. Arbitrarily reversing an unknown analog coupling is not supplied. Continuous logical-X drift obstructs the proposed simple odd repetition-code parity implementation unless compensating control is acquired.
7. ODD_INTERACTION_COLD_CHANNEL_AND_ROUTING.md with COLD_SELECTION_ROUTING_INDEPENDENT_REVIEW.md. This is a DIFFERENT inverse-rate result: actual cold preparation plus odd interaction and homogeneous jump outputs. Splitting jump outputs changes the generator, even though the stated energy certificate and leading target are preserved. Implementing that split and odd interaction is not free.
8. SHARED_BATH_LOCAL_SIGN_OBSTRUCTION.md and SHARED_SOURCE_LOCAL_FAULT_OBSTRUCTION.md with their combined independent receipt. These preserve the decisive failure of the proposed size-independent local-fault inference.

All filenames above are in quantum_effective_channel_20261031. Headings saying candidate are historical; only the exact versions bound by their receipts are received. A receipt for an earlier version is not silently transferred; the final epoch binding is explicit.

## The failed many-qubit promotion matters

A shared source can create correlated high-weight errors despite excellent energy or jump-count behavior. One finite-rate counterexample uses at most one source jump and no injected energy. A complementary shared-telegraph example yields polynomial rather than exponential high-weight Pauli-fault tails after independent local signs.

Independent LOCAL signs do not generally preserve the leading target separately in each branch: averaging channel exponentials is not exponentiating the averaged generator. This is distinct from the accepted GLOBAL plus/minus sign, whose quadratic target is identical in both branches. The counterexamples have shared unbounded fanout and do not disprove bounded-degree constructions, different refresh schedules, collective-noise codes or all fault tolerance. They establish that spatial/high-order structure must be earned. No scalable correction theorem or practical many-qubit advantage is claimed here.

## Costs and scope

The positive operator called energy is a Lyapunov/excitation operator, not an assumed thermodynamic Hamiltonian. Actual initial energy, source gap/drift constants, C or r_E, preparation, operator encodings, controls, precision and sign implementation are paid inputs. The source generator has the explicitly stated dark purely dissipative form; arbitrary additional source Hamiltonians cannot be inserted into the effective-stack formulas for free.

System-only instruments retain all outcome branches. No bound conditional on a rare selected outcome is promised. Source measurements/interventions and final bath outputs are excluded. Private sign bits must be independent on entry and old controller bits must stop influencing later hardware. Exposing the private sign changes the output task and can destroy the improved channel bound.

Generalized-amplitude damping, adiabatic elimination, covariance/Gram constructions, positive error mixing, randomized compiling and memory-aware randomization all have strong predecessors. SIGN_PAIR_PRIMARY_COMPARISON.md records inspected primary sources, including Campbell and Winick et al. A finite literature check does not establish novelty.

## Evidence and reproduction

The ordinary proofs and their scoped source-bound receipts are separate from diagnostics. check_quantum_effective_stack_initial_unital.py/JSON preserve the initial unsuccessful attempt to exhibit nonunital leading dynamics; the corrected Z/Y fixture is separate. Other floating Choi numbers are diagnostics, not certified diamond enclosures. Only the exact-arithmetic operating-window construction carries the stated rigorous numerical tolerance decision.

The reset-free diagnostic keeps the actual source through three epochs and two weak instruments, retaining all four outcome records. It also shows that exposing the sign loses the observed inverse-rate improvement, and that more sign epochs need not improve a short fixed example. It is not a replacement for the proof.

Run originals only in a disposable extracted copy because some scripts overwrite their JSON. Read-only exact replay:

    OPENBLAS_NUM_THREADS=1 python3 -B quantum_effective_channel_20261031/test_same_apparatus_certificate.py

Other check_*.py scripts reproduce their stated small finite diagnostics, not every possible input or a quantum gate backend. Used environment: Python3.12.14, NumPy2.3.5, SciPy1.17.0. No software installation or physical equipment was used. MANIFEST.json records exact unchanged source bytes and SHA-256 hashes; these are integrity checks, not independent review by themselves.
