# Reverse radius erasure comparison

Research handoff dated 15 October 2026

## Exact capability

For any finite classical channel, the minimum erasure reveal probability needed for arbitrary-quantum-reference conditional Petz/RLD dominance is an explicit reverse-radius convex program. It has an exact small semidefinite representation and a matching weighted-simplex reference construction. For faithful classical-input quantum-output channels, including noncommuting prepared states, a matrix-harmonic radius gives the corresponding conditional Petz/RLD threshold.

For a strictly positive classical channel T with input columns t_i, the value is

C(T) = min_u max_i sum_y (T_yi-u_y)²/T_yi
     = 1 - min_p sum_y (sum_i p_i/T_yi)^-1.

Here p is an input probability vector and u is a free real center, not a probability vector. With zero channel entries, only rows positive in every column appear in the harmonic sum; an empty common support gives C=1.

For faithful prepared quantum states sigma_i, the value is

C = min_(U Hermitian) max_i Tr[(sigma_i-U)sigma_i^-1(sigma_i-U)]
  = 1 - min_p Tr[(sum_i p_i sigma_i^-1)^-1].

The exact erasure threshold is q >= C. Singular prepared quantum states are outside the CQ theorem.

For classical targets and faithful classical-input quantum-output targets, the same threshold also characterizes ordinary, unsmoothed complete SLD and binary-MMSE order. Here “complete” means allowing an arbitrary finite quantum reference; “ordinary, unsmoothed” distinguishes this operational ordering from Hermitian-smoothed order, not from reference-free comparison. The operational proof includes a signed observable compiler and a converse paying one additional coherent reference dimension. It does not equate the fixed-dimension SLD and RLD resource laws.

The erasure source reveals the classical input with probability q and otherwise produces an erasure flag. All channels preserve the untouched reference. Conditional Petz/RLD comparison subtracts reference information and permits unequal reference marginals. The constructed ordinary-complete SLD counterexamples can have equal reference marginals. All supplied encodings are separable across classical input and reference; entanglement is not required.

## Evidence

The package contains full algebraic proofs and portable exact checks, including:

- A nonsymmetric classical channel with matching primal and dual value 2/11 and a qubit-reference physical witness.
- A nonuniform weighted-frame identity and faithful binary-MMSE counterexamples.
- An exact signed compiler with negative coefficients and positive second-moment defects.
- Noncommuting three-Pauli quantum outputs with radius coefficient 3/11 and a qubit-reference physical witness; a tetrahedral benchmark has coefficient 3/16.
- A three-Pauli benchmark separating reference-free SLD 9/50, reference-free RLD 9/41, and complete threshold 3/11, with an exact faithful three-level-reference binary witness at reveal q=6/25.
- A separate well-conditioned three-level-reference quantum-output binary fixture at q=1/5 with exact MMSE gap about 0.0078550032 and all state eigenvalues strictly between 1/250 and 1/3. These are conditioning bounds, not measured noise tolerance. A separate fixed-receiver model-error bound is Delta-4 delta-8 kappa, with assumptions stated in the fixture proof.
- A bounded-loss obstruction for the exclusion-channel family.

These results are internally derived with independent mathematical reconstruction. Symbolic checks verify specified identities and examples; they are not automated proofs of every general statement. External review and historical priority remain open.

## Closest prior work

Information radii, reverse divergence radii, harmonic minimax algebra, signed variance-dominating lifts, and the observable-estimation interpretation have established precedents. They are explicitly credited in PRIOR_ART.md and the proof documents. The final overlap check also compares fixed-baseline quantum contraction/maximal-correlation theory and CQ Doeblin common-lower-bound SDPs; no decisive identification overlap was located in that bounded pass. The identification of these radii with the stated arbitrary-reference thresholds was new to this research, independently derived here; a bounded source check has not established historical priority.

## Missing operation

The mathematical compiler prescribes observables rather than simulating target outcome distributions. Experimental preparation, calibration, implementation costs, and readout-error budgets still need investigation. For the conditioned quantum-output fixture, independent IID ideal-model counts of 40,000 trials per arm suffice for an empirical sign-order error bound below 5%, while 190,000 per arm suffice for the specified two-sided half-gap confidence radius. These different guarantees exclude calibration/training costs and drift. A polynomial-size exact SDP description is not a proof of polynomial-time exact boundary decision, rational optimizers, or polynomial exact bit complexity.

## Plausible consequence and quantitative limit

The formulas turn an optimization over unbounded quantum-reference dimensions into a small convex certificate problem for these erasure comparisons. This can support reproducible channel-comparison benchmarks and guide receiver construction.

A diverging ratio of complete versus reference-free thresholds does not imply a macroscopic estimation benefit. For the m-symbol exclusion channel, every binary squared-loss advantage of the target over erasure is at most min{1,4/m}, for arbitrary priors, encodings, and finite references. Strictly positive approximations obey the corresponding bound min{1,4(1-delta)/m}. The absolute advantage therefore vanishes in the large-alphabet limit even while the threshold ratio diverges. The exact cyclic binary witness included here has a risk gap only about 2.93e-8.

No channel simulation, capacity gain, practical breakthrough, or general arbitrary-channel comparison algorithm follows from these results.

## Decisive next test

Have an external expert verify the quantum-reference radius identification, support conventions, and unsmoothed operational converse against the cited literature. For implementation, optimize an absolute bounded-loss gap under explicit preparation, receiver, and noise constraints, rather than use threshold ratios as a performance proxy.

## Reproduce

Use Python 3 with SymPy installed. From any working directory run:

python /path/to/unpacked/archive/verify_all.py

The runner checks SHA-256 integrity and executes the exact certificates with archive-relative paths. It needs no network access or original research directory. Optional solver.py additionally requires NumPy and SciPy; its numerical search only proposes a prior, and exact Fraction arithmetic certifies the reported interval. A nonzero primal-dual gap remains an interval rather than being reported as an exact solution.

See proofs/ for full derivations, AUDIT_SUMMARY.md for the independently checked scope, and PRIOR_ART.md for attribution. No source PDFs are bundled.
