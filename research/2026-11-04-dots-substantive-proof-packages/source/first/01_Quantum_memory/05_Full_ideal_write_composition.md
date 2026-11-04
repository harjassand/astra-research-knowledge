# Actual RX/RZ host and full ideal WRITE composition audit

3 November 2026. Verifies the host interface and channel composition for `UNARY_FULL_SYNDROME_INTERACTING_SAMPLER.md`. The new source/weighted-remainder analytic estimates are independently audited elsewhere, not re-proved here.

## 1. Actual source-host binding is present

The relevant receipt is:
`/workspace/shared/reachable_memory_loading_20261101/independent_audit/ACTUAL_RECURSIVE_SAMPLER_BINDING_RECEIPT.md`.

I checked its stated frozen hashes against the current files:
- `recursive_initialization/actual_decoder_binding.md`: SHA256 `61a0a149960cfe21beb30d0d4a91f2553932227675e6dbb26514c5501cdbf685`.
- `ROOT_RECURSIVE_THERMAL_SAMPLER_JOIN.md`: SHA256 `a28c7243fd3136019e4df64e7ffaa7da1912573e43e6587412c3c157fc7e3879`.

Both match exactly. This binding concerns the actual MAIN RANDOM-EMBEDDING RX/RZ recursive family and its Sections 4–5 decoder, including the modified whole level-2 terminal decoder of Section 5.1.1. It is not restricted to the later explicit-embedding candidate. The source text states the main construction's bounded degrees zv=7 and ze=4, while explicitly leaving the explicit variant's full lifetime proof for future work. Any earlier summary that the random family lacked an admitted syndrome trace representation was too broad.

The exact existing contract includes all redundant check coordinates, local image/reconstruction checks, a fixed total zero-preserving deterministic gate table, complete stencils, cancellation gates, and complete nonzero-wire fanout. These give a canonical bijection, not a multiply counted cover.

Each nonzero TOP syndrome coordinate is marked once as its own external input object. Thus a unique charged owner exists and |T_gamma|<=m_gamma has coefficient ONE. The reverse inequality is m_gamma<=A|T_gamma| with A=12S, where S is the fixed local stencil charge from the source binding. A may be enormous but is independent of system size. The downward physical Pauli expansion is not included in the activity trace and must be reconstructed and charged separately after sampling.

The validator host has O(n) objects, bounded degree and finite alphabet at fixed construction parameter ell. Its constants, tables and incidence lists are constructible with charged fixed-parameter preprocessing. This is not a uniform polynomial in ell.

## 2. X/Z joint law

The valid CSS syndrome spaces factor, but the actual unary free-energy correction can couple X and Z signs. Therefore take the disjoint union of the two validator hosts and run ONE interacting polymer chain on it. Compatibility still describes exactly the full valid syndrome set. Cross-sector potential terms are evaluated in that single chain. Independent X and Z sampling after adding the correction would be wrong.

With constant equal syndrome eigenspace dimensions, the target weight is exactly exp(-2 beta J |sigma| - beta R(sigma)); there is no additional count of error representatives. Every chain rate is a positive exponential. Signed Fourier coefficients are evaluated, not sampled as signed probabilities.

The note's conservative bound a_gamma=w_gamma exp(2 epsilonPhi m_gamma) is valid under its stated epsilonPhi<=.01 and B chosen proportional to A. A sharper alternative retains |T_gamma|:
a_gamma=exp[-2(B-epsilonPhi)|T_gamma|] <=exp[-2(B-epsilonPhi)m_gamma/A].
This removes a needless A penalty if one later fixes g and increases beta. Either version is valid with the note's current constructive choice: choose fixed B using A and host constants, then reduce g until beta=B/J has the required small dimensionless correction and thermal tails.

## 3. No hidden exponential-volume oracle

Connected hulls and validated trace polymers truncated at O(log(n/epsilon)) have exponentially many candidates in their TRUNCATION SIZE, hence polynomially many in n/epsilon at fixed parameters. Finite-clock matrix dimension is (2^K)^O(log(n/epsilon)), not 2^n.

For Fourier coefficient evaluation, H_B(s_B) must be generated directly from the explicit clock-only common-frame formula, including formal local sign assignments that may not extend to valid global syndromes. The absolute majorants must hold for that extension; their uniform treatment of flux signs is the appropriate justification. Do not construct a conditional Hamiltonian by diagonalizing the global data syndrome eigenspace. The latter would hide exponential work. The actual sampling chain itself stays on valid syndromes throughout.

Finite-region log-partition Mobius subtraction extracts connected spatial hulls exactly when the common-frame exterior-reference restriction is consistent. All assignment enumeration, Fourier transforms, dense matrix functions, and required absolute precision cost exp(O(KL)) for region size L. beta can be astronomically large but is fixed before n varies. This is polynomial existence, not practical efficiency.

## 4. Reference-safe full ideal encoding

Fix the same decoder frame used in the storage theorem. Let Enc0 encode an arbitrary logical-reference input xi_LR into the zero-syndrome data state. A supplied encoded input suffices; otherwise an ideal stabilizer Clifford encoder can be synthesized with polynomial classical/gate work from the explicit check matrices.

For sampled sigma, apply the matched representative E_D(sigma), prepare the full conditional ancillary Gibbs state tau_sigma using the audited thermofield circuit, discard its purification half, and apply the common prefix-frame unitary in the physical direction. The prefix unitary is a known product of controlled Pauli gates, not an oracle. Its local gates, routing, ancillas and duration must be charged.

This produces the target thermal LOGICAL encoding, not the full Gibbs state with a maximally mixed logical subsystem unless xi_L is maximally mixed. All number sectors are retained in tau_sigma. Because the common-frame Hamiltonian is identity on the logical subsystem, preserving an arbitrary external reference poses no additional preparation difficulty.

In trace-distance convention D=||.||_1/2, if classical sampling error is delta_cl, the conditional Gibbs preparation error is uniformly at most delta_q over valid sigma, and the encoded-input/gate implementation errors total delta_impl, the full preparation error is at most

D(output,target) <=delta_cl+delta_q+delta_impl.

This follows by the classical mixture bound, convexity, and CPTP/unitary contractivity. It has no dependence on reference dimension and no multiplicative 2^n factor. Subsequent identical storage/decoding adds this preparation error once, not per time step.

## 5. Exact remaining physical gate

Subject to the new source-hull and weighted-free-energy estimates passing their analytic audit, the admitted host representation and explicit algorithms give a complete polynomial IDEAL ACTIVE isolated-memory thermal WRITE at fixed sufficiently cold parameters.

This does not prepare a correlated inaccessible-bath equilibrium state. It does not prove a constant-rate noisy terminal transfer into bare physical memory: fault-tolerant internal computation alone does not bound the global disturbance of O(n) final output errors. A decoder/basin admission theorem matched to the actual noise and storage dynamics remains required. No end-to-end practical advantage over an active memory with the same controls, reset, routing and refrigeration resources follows.

## 6. Explicit error allocation and operation count

For requested trace-distance accuracy epsilon, set delta_cl=epsilon/4, delta_q=epsilon/2, delta_impl=epsilon/4. Divide delta_cl among trace truncation, potential truncation, mixing, Poisson cap and finite-precision probabilities. Divide delta_q among creation-log truncation, finite-coefficient error, adiabatic error and Hamiltonian-simulation/synthesis error. Delta_impl covers any approximation to input encoding and final prefix/decoder circuitry; ideal Clifford gates can implement the data portions exactly. Every sub-error is inverse-polynomial in n/epsilon; there are polynomially many operations, so per-operation synthesis budgets remain inverse-polynomial.

The classical random draw is independent of the unknown incoming logical state. Enc0 acts coherently on that input and initialized ancillas; no tomography or classical description of xi is used. The bound therefore holds as a channel bound on arbitrary entangled input, equivalently half-diamond distance at most epsilon.

Let p be the fixed exponent arising from the trace-host alphabet/degree, clock dimension, convergence rates and finite-region arithmetic. Dictionary construction, evaluating potential differences and simulating the capped birth/death chain cost at most (n/epsilon)^p times fixed-parameter constants. The conditional thermofield parent has a uniform constant gap, ||P'||=O(n), ||P''||=O(n), and computable terms on O(log(n/epsilon)) clocks. A conventional adiabatic bound permits runtime O(poly(n)/epsilon), for example a conservative O(n^2/epsilon) after absorbing the fixed gap and derivative constants, followed by polynomial-cost Hamiltonian simulation. Dense decomposition/synthesis of each retained local term costs exp(O(K log(n/epsilon))), still polynomial at fixed K. Each physical logical encoder uses polynomial Clifford work, each decoder representative is a computed Pauli string, and the common prefix unitary has O(n K) controlled-Pauli operations at fixed check incidence.

A strictly local control architecture may route these operations with a polynomial overhead using swaps and clean ancillas. This is an ideal active-circuit simulation statement, not a constant-depth assertion, and does not claim that the preparation parent itself has the passive device's three-body interaction form. Storage begins after the prepared state is transferred to the passive Hamiltonian; coherent control during WRITE is an explicit resource assumption.

## 7. Independent review and two precision clarifications

Independent end-to-end review returned qualified PASS in `/workspace/shared/UNARY_END_TO_END_WRITE_INDEPENDENT_AUDIT_20261103.md`, conditional on the separately imported analytic cluster and parent estimates. It independently matched the two frozen host hashes and checked positive sampling and reference-safe composition.

Implementation error delta_impl is a reference-safe channel budget, for example a sum of half-diamond-norm gate errors, not an unentangled test-state infidelity. The subsequent contractivity statement requires the SAME admissible storage channel and bath initialization. Closeness of isolated system marginals does not control storage with different initial system-bath correlations.
