# Independent review: polynomial decoder and physical qubit port
30 October 2026. Scoped PASS for exact algebra and the repaired synthesis receiving; actual scheduled gadget/noise contracts remain received hypotheses.

## Bound inputs
POLYNOMIAL_QUDIT_TO_TANNER_QUBIT.md SHA256 b184413448e28718660708b72f755925da21144e0e133ac8fcf8ece92a0c85c8.
check_qudit_quantum_port.py SHA256 8eceff9e88301c1e0ae7354c023b200369d9719f16ae1ae871f188061885863a.
The main decoder receipt remains review_top_down/INDEPENDENT_REVIEW.md with FINAL_HASH_ADDENDUM.md; no change to its frozen main manuscript is required.

## Exact core
Distinct field evaluation points make the first d+1 Vandermonde columns independent. They can be completed simply by the remaining monomial columns through degree m-1. Gaussian elimination factors the invertible matrix into row operations implemented by SUM, nonzero multiplication and SWAP. Fourier preparation of d coefficient registers gives exactly the polynomial-code encoding. Inverting the linear map and then the Fourier preparations returns the unknown logical symbol and fixed zero ancillary registers. This is a unitary quantum inverse encoder, not a classical-value decoder.

Finite-field syndrome lookup is exactly implementable by reversible polynomial evaluation with the generalized Toffoli arithmetic. Equality indicators use Fermat's identity, with products over syndrome coordinates. Repeated variables can be copied into scratch by SUM in the computational basis, evaluated coherently, and uncomputed; no illegal cloning of arbitrary unknown states is needed. A lookup may be exponentially large in the base-code parameters, but they are fixed constants. Controlled generalized X and Z corrections follow from SUM and multiplication/phase scratch arithmetic. The exact G2 availability was rechecked against Aharonov–Ben-Or, https://arxiv.org/html/quant-ph/9906129, section5.1. The fixed polynomial computation-code gadget and arbitrary-input correction contract are imported, not independently reproved here.

Consequently the shrinking circuit has no target synthesis error at each recursion level. Actual finite reset discrepancy and physical gate noise are still charged by the approximate-target cavity and final-location fault contracts. Exact target circuit is not a claim of noiseless hardware.

## Terminal transfer
W is a transposition of two computational basis states and identity on the rest, hence exactly unitary on the full qudit-times-qubit space. On the embedded two-dimensional source subspace with target zero, it maps |0,0> to |0,0> and |1,0> to |0,1>. By linearity this transfers arbitrary reference-entangled qubits and leaves the source qudit in fixed |0>. It is not a transfer theorem for a general p-dimensional unknown state.

All terminal W/reset locations belong in the final physical stage, whose good event requires zero faults. This preserves the fixed O(x0) output floor with enlarged finite constants. A mixed-dimension gate is an actual additional hardware interface unless already supplied; merely having abstract G2 gates on qudits does not physically supply it. The manuscript states that restriction.

## Synthesis receiving repair
The original bare contraction sentence was insufficient for an arbitrary signed good-history sum. The final manuscript contains the required common-syndrome comparison. At the computation boundary use the fixed coherent isometry D retaining syndrome, so the good term equals |psi_synth><psi_synth| tensor K with K supported in common sparse syndrome space S. The all-logical cross-term correction theorem implies L tensor S is in D's image. Its inverse has a fixed CPTP extension there.

The full decoded state is positive trace one and the bad computation term has trace norm at most b_c. Hence ||K||_1<=1+b_c. Replacing only the logical factor by the exact target changes the reembedded physical comparison by at most (1+b_c)epsilon_synth. The SAME actual top-down decoder/transfer channel contracts this difference. Its bad-cardinality map acting on the target/sparse comparator contributes at most (1+b_c)b_out; its good part lies in the desired target-error span. Thus actual bad-span population is at most

    b_c+(1+b_c)(b_out+epsilon_synth).

No positivity is assigned to K, no source-noise independence is assumed, and no sparse Pauli interpretation is assigned to synthesis leakage. A reduced logical-channel decoder without retained syndrome would not justify the reembedding argument. The standalone derivation SYNTHESIS_RECEIVING.md (SHA256 397a32ed42a915a31911a64739746ddadf3ac4c1c2f101567c5ea2833d170d40) records this proof.

The global compiled target error may be exponentially small with polynomial overhead in target size for fixed p and a polynomial-size target encoder. Its exact norm/error budget must refer to the whole compiled target channel. There is no repeated per-shrink approximation penalty. The final gentle estimate and polynomial resource scaling remain as stated; neither implies practical efficiency with reasonable constants.

## Checks
Supplied p=5, degree1, length4 script replay: inverse encoder residual 1.6302709355362946e-16; entangled transfer residual zero. Saved source_replay.json.
Independent check_exact_core.py/json uses p=7, length4, degree1, verifies the full Vandermonde basis permutation on 2401 strings, the encoding isometry and reference-entangled transfer. It passes. These checks establish finite algebra only, not a fault threshold or physical implementation.

## Unchanged boundary
Accepted only with the frozen scheduled-FT/common-module/reset resources and the explicitly supplied terminal hardware. This is not an autonomous factory, arbitrary-accuracy exposed qubit delivery at fixed physical noise, a native warm-clock/ancilla theorem, detector qualification, or a claim of novel fault-tolerant computation.
