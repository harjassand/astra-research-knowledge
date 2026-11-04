# Acquiring a hidden code and correcting logical Bell samples

This reproducible finite audit accompanies the analytic construction. It checks the acquisition, graph reconstruction, Pauli-phase bookkeeping, classical error correction, and logical learning operations. It is not a hardware experiment, a threshold estimate, or a finite-bandwidth device simulation.

## Run

```bash
python latent_code_bell_check.py
```

Requirements: Python 3, NumPy, and a C++17 compiler available as `g++`. NetworkX does not need to be installed. The default decoder is the polynomial integer-weight blossom algorithm vendored from NetworkX 3.4.2 in `latent_code_blossom.py`; its BSD license is retained there and in `latent_code_networkx_LICENSE.txt`.

An exact exponential defect-matching routine is retained only for finite comparison:

```bash
python latent_code_bell_check.py --matching dp --output latent_code_bell_result_dp_repeat.json
```

The default command writes `latent_code_bell_result.json` and uses sparse parity-collision acquisition. The exhaustive acquisition remains available:

```bash
python latent_code_bell_check.py --acquisition exhaustive --output latent_code_bell_result_exhaustive_repeat.json
```

Its complete earlier result is preserved as `latent_code_bell_result_exhaustive.json`; the earlier dynamic-programming matching result is preserved as `latent_code_bell_result_dp.json`. The fixed seed is 4112606. The run also generates the intermediate measurement file `latent_code_calibration.bin` and builds the selected scanner executable.

## What is generated and what is learned

The calibration source is a mixed stabilizer state inside a square `[[50,2,5]]` toric-code block. A random qubit permutation and independent random single-qubit Cliffords obscure its elementary checks. Physical measurement outcomes are sampled from their exact stabilizer-algebra distribution: for each product measurement basis, binary linear algebra finds the stabilizers diagonal in that basis, including their signs, and samples uniformly from the resulting affine outcome space. Independent readout flips give local Pauli visibility 0.99.

Calibration uses 1,000 independent random product bases and 256 fresh source copies for each basis: 256,000 copies in total. The scanner receives only the measured bases and outcomes. In the default algorithm, the first 12 rows are used for discovery and the remaining 244 fresh rows for verification. For every pair of wires, the scanner forms the exclusive-or of their 12-bit columns and identifies this key with its complement. Equal keys on disjoint wire pairs propose a weight-four signed parity check. Each proposed quartet is verified only on the remaining 244 rows, with threshold `|mean| > 1/2`. Discovery data are never reused for verification.

This run forms 1,225,000 pair records, performs 367,551 collision comparisons, discards 27,744 comparisons with overlapping pairs, and independently verifies 113,269 distinct pattern/quartet proposals. It accepts 495 pattern/check instances and recovers all 50 unique checks. The default collision cap is 258,333,334, corresponding to a runtime-abort budget of 0.003; exceeding the cap causes an explicit failure rather than unbounded work. Sorting pair records gives deterministic preprocessing cost. See `latent_code_collision_lemma.md` for the discovery, verification and capped-runtime bounds.

The preserved exhaustive scanner instead tests all 230,300 four-wire supports per basis: 230,300,000 pattern/support tests, using threshold 0.75 on all 256 rows. Both acquisition methods recover exactly the same checks and leave all subsequent seeded Bell-learning outcomes unchanged. The sparse method trades a modest polynomial number of calibration copies for substantially less classical work; the separate minimum-sample theorem uses a single random-basis batch and exhaustive candidate enumeration.

All 50 elementary checks are recovered, with no false positives or missed checks in this seeded run. The ground-truth check set is used only to audit the output. From the recovered checks, the code constructs the locally anticommuting-check graph, bipartitions it, acquires the primal and dual syndrome graphs, and obtains logical representatives by binary elimination. Both check matrices have rank 24, leaving two logical qubits.

The code then certifies the acquired cellulation: every face and vertex link is a simple four-cycle, every edge has two endpoints and two incident faces, the complex is connected and orientable, its Euler characteristic is zero, and the checks commute. The `X` and `Z` distances are computed from the acquired graph, rather than copied from the source constructor. For each graph, the two acquired opposite logical representatives label a four-sheet homology cover. Breadth-first searches from each `(vertex,0)` to `(vertex,nonzero_sheet)` find the shortest nontrivial closed walk. Both acquired distances equal five.

## Bell measurement and noise

The quantum readout is a fixed laboratory Bell measurement on corresponding wire pairs. No learned local Clifford is applied as a quantum gate. The interpretation changes classically: if the laboratory bits report the eigenvalues of `XX` and `ZZ`, the `YY` bit is their exclusive-or plus one, because `YY = -XX ZZ`. The audit explicitly maps recovered-frame outcomes to laboratory outcomes, inserts faults in laboratory coordinates, and maps back with this affine rule.

Because the laboratory Bell readout is fixed, all quantum experiments may finish before the code or decoder is computed. Calibration and Bell records can be processed afterward. Classical acquisition time therefore causes no quantum-memory hold; the delay between the two copies still requires its own physical error budget.

Each pair is independently faulty with the stated probability. On a faulty pair, one of the three nonzero two-bit outcome flips is chosen uniformly. This is a Pauli fault model on pair support. The analytic theorem's extension to arbitrary completely positive faults on a stochastic support is not claimed to be numerically simulated here.

Each observed syndrome is decoded by minimum-weight matching using graph distances and shortest paths acquired from the checks. The default algorithm is weighted blossom, with maximum cardinality and positive integer weights chosen so that maximum weight is equivalent to minimum total distance. The original implementation's integer optimality assertions remain enabled. Minimum-weight matching is polynomial in the number of defects; the optional dynamic-programming comparison is exponential.

## Logical learning audits

For each experiment the logical state is either maximally mixed or `(I+P)/2^k`, with an unknown nonidentity logical Pauli `P`. Exact logical Bell rows are sampled from the appropriate affine hyperplane, then lifted to physical Bell rows satisfying the acquired code constraints. After physical faults and classical correction, binary elimination on differences of the logical rows distinguishes the two hypotheses and identifies the unsigned Pauli. The transpose phase, including `Y`, is included. The sign of `P` is not identifiable from these two-copy data and is not claimed.

The single-block audit performs 200 experiments: 100 null states and 100 unknown Pauli states. Each uses 24 Bell rows. At pair-fault probability 0.01, the seed generates 2,314 actual pair faults across 4,800 rows; there are no logical-row or learning failures.

A separate global-data audit reuses the acquired block 16 times, giving 800 physical wires and 32 logical qubits. It performs 10 experiments with 80 rows each, at pair-fault probability 0.003. The seed generates 1,906 actual pair faults, with no logical-row or learning failures. **Calibration is not rerun on the full 800-wire register.** This second calculation tests the global hidden-correlation data path; the full-register acquisition guarantee is analytic.

The matching implementation changed from dynamic programming to blossom after the first audit. Both runs preserve the seed and all reported counts and outcomes; timing and implementation metadata differ. Results do not establish an empirical threshold, an optimized success curve, or performance outside the explicit simulation model.

## Completing the sign with a known encoded reference

The calibration also retains the signed checks in `latent_code_acquired_signs.json`; 18 of the 50 check bodies have negative sign in the seeded hidden frame. These signs are verified against ground truth only after acquisition. They are needed to prepare a reference in the same signed codespace.

For each unsigned Pauli actually learned in the preceding experiments, the program constructs a known pure stabilizer reference whose target Pauli eigenvalue is +1. The reference contains the acquired signed checks and one selected Pauli eigenstate per logical qubit. Its full independent commuting generator specification is checked and saved in `latent_code_reference_specifications.json`. A fresh specimen/reference Bell row then reveals the sign through the corrected target-parity outcome. The specified noisy physical reference factory is not simulated; its construction and approximation budget are supplied separately in the theorem note.

The separate sign audit uses seed 4112607 and preserves the preceding audit counts. There are 100 additional small-block specimen/reference pairs, equally divided between positive and negative signs. With 43 actual pair faults, no logical-row or signed-readout failures occur. Five additional global targets are checked on 800 physical wires, with seven actual pair faults and no failures; this again reuses the small acquired block.

## Exact certificate for sparse acquisition

```bash
python latent_code_collision_certificate.py
```

The existing 50-wire acquisition parameters have an exact rational failure bound below 0.009278, including missed checks, collision-cap abort and held-out verification errors. This is a model-dependent analytic bound, not an empirical error estimate.

A second point uses 11,552 physical wires, fault bounds `q = q_c = 3/1000`, 1,848 random bases, 28 discovery rows and 348 fresh verification rows per basis. It uses 694,848 calibration copies. Adding 74 Bell pairs gives 694,996 source copies and a certified learning/readout failure bound below 0.007220. The signed completion adds one fresh specimen and one known encoded reference: 75 corrected rows, 694,998 prepared banks, 866,400 physical Bell gates, and error below 0.007251. Its runtime cap and operation counts are recorded explicitly. Separate factory and any control-approximation budgets are not included. This larger point is not simulated.

## Separate exact finite parameter certificate

```bash
python latent_code_parameter_certificate.py
```

This preserves the earlier **minimum-sample, all-candidate acquisition** certificate, not the sparse collision learner's count: 32 logical qubits, distance 19, 11,552 physical qubits per copy, local fault bounds `q = q_c = 3/1000`, 260,000 calibration copies and 74 Bell rows. Every assertion uses exact rational arithmetic. A positive Taylor polynomial bounds the required exponential from below, giving a rational upper bound on the calibration failure probability. The total learning/readout failure bound is below 0.007508.

The separate specimen-source failure probability `delta_src` is **not included**. Local source faults may already be included in `q`; any additional logical or nonlocal preparation failures must be supplied and added separately. The certificate does not establish a device noise model or an economical specimen factory. Results are saved in `latent_code_parameter_certificate.json`.

## Provenance

The blossom implementation is extracted from:

https://github.com/networkx/networkx/blob/networkx-3.4.2/networkx/algorithms/matching.py

Only `max_weight_matching` and `matching_dict_to_set` are included. NetworkX dispatch decorators and imports are removed, and the helper's invalid-matching exception is changed to `ValueError`. A minimal local graph adapter supplies the interface. The matching algorithm is otherwise unchanged. The full upstream BSD notice is included.
