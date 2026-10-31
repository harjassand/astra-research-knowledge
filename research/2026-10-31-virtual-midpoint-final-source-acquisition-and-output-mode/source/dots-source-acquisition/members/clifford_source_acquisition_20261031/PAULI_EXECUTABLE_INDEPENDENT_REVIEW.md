# Independent exact sparse-Pauli acquisition code review

## Verdict and binding

**PASS for the exact classical acquisition/LCU-specification module.** I read the entire implementation and supplied test file, independently ran the supplied tests, and added and ran a separate adversarial/dense suite. This is not quantum circuit synthesis or implementation of the downstream simulation compiler.

Bound implementation: `acquire_pauli_coupling.py`, 6,838 bytes, SHA-256 `983e5d59f2fa6057d3b953c7f4e92855563995d90675c5e0fdd0b3f0c820cb50`.

Bound supplied test: `test_pauli_coupling.py`, 5,478 bytes, SHA-256 `edd32c6dd55216556452a485f74484cd9e308298d44d3e088ba7f90be7e20779`.

Additional test: `test_pauli_independent_adversarial.py`, 4,561 bytes, SHA-256 `930ec634e0edf85653f870b9e2b4b9289b9d15891eb6a773a1c088eed5839bf6`. Its result `pauli_independent_adversarial_checks.json` has SHA-256 `034cab15ac1f4e2a170e9cb455fe920a47eeb689f98df48c1d7f7bfa40c99e06` and records the same bound implementation hash.

The imported source verifier is the separately repaired and accepted `acquire_clifford_source.py`, SHA-256 `d838ceb019302861375671da683467ab82514cd45e6eff6e86a5990e8664b1f0`. Its previous zero-only persistence forgery is not admitted by this dependency. The separate consumer specification and its receipt remain the mathematical execution interface; this module only emits its exact classical ingredients.

## 1. Input validation and signed expectations

The module first verifies the actual source program/certificate and requires status accepted_pure_return. It then requires an explicit finite term list, positive integer system register size, integer Pauli masks in range, and exact integer or syntactically restricted rational-string coefficients. Python bools are not accepted as integer coefficients or masks, floating-point values are rejected, and zero denominators raise a validation error. No expression evaluation or source learning is performed.

The Hermitian Pauli represented by masks x,z is i^{popcount(x and z)} X^x Z^z. Exact elimination against the signed stabilizer basis computes the correct expectation. A remaining nonzero label gives zero expectation; a zero label gives +1 or -1 according to the accumulated phase. The phase assertion rules out an impossible imaginary expectation for a Hermitian stabilizer member. Tests explicitly exercise negative stabilizers, mixed Y strings, entangled states and complex preparations.

This public expectation helper is used internally only after the source certificate has been verified. It is not independently a validator for arbitrary user-supplied malformed stabilizer generators.

## 2. Rational aggregation and centering

Duplicate original terms are combined with exact Fraction arithmetic and canceled terms removed. Means are aggregated by system Pauli string. Subtracting these mean terms on the source identity gives the centered operator. The implementation rechecks every residual system-string mean symbolically and asserts that it is exactly zero.

The returned original, mean and centered LCU bounds are the exact sums of absolute rational coefficients in their respective combined lists. They are acquired upper bounds, not claimed exact operator norms. Triangle inequalities give centered_bound<=2 original_bound and mean_bound<=original_bound; these are also asserted. Combining terms may improve the bounds without requiring an operator-norm computation.

The mean is retained in the output and in the model identity. A nonzero system mean is not silently erased from Hsys+sqrt(lambda)K. Scalar system-identity mean is reported separately and may be omitted only because its commutator vanishes. The final source names the field `physical_mean_commutator_is_zero`, explicitly allowing a nonzero scalar-only mean without asserting that Hbar is literally zero. It retains `scalar_mean`, `nontrivial_mean_lcu_bound` and the global-phase note. This naming clarification was made during review, not a change to the exact centering identity.

## 3. Executed checks

The supplied suite completed with exit zero: 25 pure-source cases, 976 signed Pauli expectation comparisons, 25 dense mean/centering identities, maximum numerical residual 4.9926e-15, explicit scalar/nontrivial mean preservation, nine malformed coupling cases, and rejection of a forged source certificate.

The independent supplemental suite completed successfully with a different random seed and direct comparison to the ORIGINAL intended source preparation rather than the finder's synthesized preparation:

- 32 random pure-source cases with one through four source qubits;
- all source Hermitian Pauli masks in those cases, totaling 2,720 signed expectations;
- 32 dense mean and centered-operator identities, maximum numerical residual 2.187e-14;
- exact cancellation of opposite rational coefficients with 521-bit numerator and 257-bit denominator scales;
- preservation of a negative scalar-only mean and a nonzero centered coupling;
- the empty-list exact-zero branch;
- 37 rejected malformed specifications, including bools, floating-point/nonfinite values, out-of-range masks, missing fields, malformed rationals and zero denominators.

These dense floating-point checks are diagnostics. The acquisition itself uses exact GF(2)/phase and rational arithmetic. No dense state table is used by the module.

## 4. Resource and implementation scope

All emitted lists have polynomial size in the explicit input term count and register widths. Rational addition and multiplication have polynomial bit complexity in aggregate input coefficient lengths. Following review, the final source prepares the canonical signed membership tableau and pivots once per acquired term list, then reuses them both for term means and for the symbolic recheck. Each expectation uses O(n) operations on O(n)-bit masks, giving a conservative O(n^2) bit bound after preprocessing. The one-off convenience wrapper still prepares its own table; repeated callers should use the explicit prepared-membership interface. Certificate validation costs are paid once per acquisition invocation or separately cached immutably as documented.

The output is a classical exact term/LCU specification. It does not prepare coefficient states, synthesize rotations, implement SELECT, implement the mean Hamiltonian, or run the retained-source compiler. Those costs and precision budgets remain paid in the separately reviewed consumer interface. Arbitrary succinct Boolean diagonal operators are not sparse Pauli lists; arbitrary computable-real sign/zero tests and unknown-source learning are not supplied. There is no practical advantage, classical hardness or novelty claim.
