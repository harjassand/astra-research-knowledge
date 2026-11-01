# Constructive noncommuting thermal encoding for a 3D quantum code

1 November2026. A theoretical algorithm, complete proof interfaces, independent internal review and finite executable checks. Not a full circuit implementation or laboratory demonstration.

## Strongest result
For the actual recursive 3D code family, sufficiently weak genuinely noncommuting local interactions, a fixed low-temperature interval and a finite ACCESSIBLE qubit bath, the construction gives polynomial-cost IDEAL thermal encoding while preserving a supplied unknown logical qubit and its external entanglement.

It replaces an interacting-Gibbs-state oracle with two constructive operations:
1. Sample the relevant syndrome/bath labels from a positive, efficiently evaluable classical distribution.
2. Prepare each label's quantum coherence by deterministic adiabatic evolution under an explicitly computable, uniformly gapped filtered-code parent Hamiltonian.

There is no exponentially unlikely global postselection and no dense arbitrary channel on a logarithmic-radius 3D ball. Small connected clusters contain O(log(N/epsilon)) spins, so their explicit matrix computations remain polynomial. The output is close to the fixed thermal overwrite admitted by the earlier exact-H storage theorem.

## Decisive new proof connection
The actual recursive code's stabilizer fillings use logarithmically many ancestry levels. A bounded-load quotient produces a bounded-degree SHORTCUT ANALYSIS graph on the existing checks/qubits. A separately audited extension of an established gap-stability proof then supplies the filtered parents' uniform gap. These shortcuts change no Hamiltonian or physical hardware; parent terms are compiled on their actual supports.

This code-specific gap/algorithm/logical-transport join is the contribution being assessed. Filtered parents, METTS-style ensembles, polymer methods and adiabatic preparation have strong predecessors, including Ge–Molnar–Cirac and the recent classical-gauge construction of Xun–Cao–Watanabe. See PRIMARY_PRIOR_CAPABILITY_GATE.md. No exhaustive novelty or priority claim is made.

## Exact scope and costs
- Known local Hamiltonian coefficients; all finite bath spins accessible during preparation. N=n+N_B is polynomial in memory size n.
- Supplied encoded logical input. Known reference-code preparation for a standalone Gibbs-state task uses ordinary ideal Clifford methods; a raw unknown input has a separately charged interface.
- Fixed construction and temperature constants. Their magnitude can be enormous; polynomial scaling is not a useful finite-size hardware estimate.
- Computational tolerance epsilon in the admitted cutoff regime, including inverse-polynomial accuracy. Encoding error is O(epsilon+beta N eta_n+sqrt(delta_tw,n)), with explicitly retained stretched-exponentially small intrinsic remainders. Not arbitrary exact accuracy at fixed n.
- Classical computation, clean workspace, coherent controls, adiabatic time, precision and Hamiltonian simulation are counted polynomially. No independent claim of practical advantage over an active FT architecture is made.

The construction remains IDEAL. A fault-tolerant processor could hold its output in an encoded representation, but releasing that state into noisy physical memory is a separate operation. Generic final gate noise, inaccessible reservoirs, uncontrolled drift and physical readout are not solved by this package.

## Read in order
1. ROOT_FILTERED_THERMAL_ENCODER_JOIN.md: complete scope and interfaces.
2. FRESH_WHOLE_AUDIT.md: independent whole-construction review and accepted hashes.
3. host/actual_hierarchical_host_filling_v2.md and host/audits/: actual analysis-graph/gap connection.
4. algorithm/filtered_parent_consumer.md and its audit/addendum: exact kernel, local expansion, polynomial compilation and logical transport.
5. algorithm/GRAM_SAMPLER_ENSEMBLE_BRIDGE.md and its audit: actual weights, positive sampling and reference-safe ensemble comparison.
6. PRIMARY_PRIOR_CAPABILITY_GATE.md: strongest established alternatives.
7. prerequisites/: inherited actual-code filling, commuting initialization and exact-H storage components.

Historical candidate/pending labels remain in frozen component files so their audit hashes can be checked. The whole receipt and clarification addenda specify what has now been joined.

## Reproducible checks
- tests/root_filtered_parent_test.py: standard [[5,1,3]] code, NOT the recursive-family proof. All16 syndrome sectors: exact filtered kernel, finite gap, Gram/connection and reference-entangled ensemble check. The initial factor-two normalization error is transparently recorded in FINITE_TEST_CORRECTION.md.
- host/actual_host_quotient_deterministic_test.py: actual5→60→1336 recursive host, bounded-load quotient and both support-connectivity implications. Output is identical across multiple hash seeds and clean-copy execution.
- prerequisites/commuting/recursive_initialization/: actual one-step4096-syndrome recognizer,60-qubit seed tests and complete finite polymer bijection.
- prerequisites/commuting/independent_audit/test_abstract_trace_bijection.py: independent exact small-circuit trace checks.

Python3, NumPy and SciPy suffice for these tests. Run scripts from their own directories. Portable helper modules are included. No governing paper body or source figure is redistributed.

## What success means
This removes a specific computational preparation assumption on a credible route toward reliable quantum matter. It is not yet a usable passive quantum memory or a civilisation-level breakthrough. The next operational gate is a fully charged noisy preparation/release/readout interface, compared against strong active fault tolerance using the same physical resources.
