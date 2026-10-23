# New bounded computational evidence

The all-length claims are proved analytically in the TeX sources. The scripts below diagnose concrete implementation, identity and comparison risks. None compiles the final outer code or computes the channel capacity.

## Actual normalized input

gram_input_check.py uses the unchanged original token operator implementation in inherited_h_operator.py. It constructs every color-count sector of the actual input for k=4,5,6,7 at b=1/(256k), checks positivity and normalization numerically, exact charge targets to numerical precision, the weighted remainder bounds, entropy margin and analytic drift margin. It also records the nonzero commutator of the normalizer with H.

It requires NumPy and SciPy. Use single-thread BLAS for the recorded resource comparison:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python representation/gram_input_check.py

The recorded peak matrix space has dimension 3^7=2187, split into sectors. A finite positive eigenvalue is not used as an all-length positivity proof.

## Proved certificate comparison

capacity_comparison.py uses 100-digit Decimal arithmetic to evaluate the exact closed form of v_k and the proved Cycle8, Cycle9 and Cycle10 floors. It also retains the actual pair entropy and nonscalar four-call entropy improvement. It checks the concrete scalar drift window and records actual parameter-resource scales.

    python representation/capacity_comparison.py

The corrected resource upper is (3^k+16)/t. The omitted-constant version is retained only as a clearly marked historical error in evidence/. The comparison is not a capacity measurement or efficient-code estimate.

## Distinct exact identity and physical-history diagnostics

- contributions/charge_structure/exact_charge_check.py: exact rational first/last-minimum and charge-moment checks for k=2 through 11.
- contributions/hamming_response/physical_hamming_check.py: Gaussian-integer coherent histories for V=(6U+iI)/sqrt(37), full small input/prefix blocks at k=2,3, and selected four-endpoint blocks at k=4. Exact isometry and diagonal identities are distinguished from floating operator norms.
- contributions/operator_challenge/independent_delta_checks.py: independent 120-digit direct return-probability sums for the new comparison table, avoiding the main script's closed-form identity.

The optional package verifier runs only the four main new diagnostics in an isolated temporary copy; it does not overwrite these frozen outputs or replay old scientific campaigns. Execution times in each JSON are measured process bodies, not discovery, inference, total review, or receiving-integration cost.

