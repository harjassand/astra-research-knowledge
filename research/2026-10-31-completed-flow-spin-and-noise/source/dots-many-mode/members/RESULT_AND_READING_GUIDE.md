# Many noncommuting telegraph noises: complete simulation construction

Research checkpoint, 31 October 2026. Read with the separately dated, source-bound independent mathematical reviews. Candidate filenames and their original headers are preserved; later receipts specify which completed versions passed internal mathematical review.

## What the result enables
The construction simulates a quantum system driven by many independent, temporally correlated telegraph noises, even when their system operators do not commute. It retains the noise memory across prescribed intervention times. It avoids processing a full list of the rapid classical sign flips, and it does not replace the finite-rate noise with a white-noise limit.

Its simulator overhead is polynomial in the number of modes, the physical drift/diffusion resources, input bit lengths, logarithms of the switching rates, and logarithm of inverse requested error. All supplied operator-encoding costs are charged. Arbitrary consumer operations at the intervention slots are external costs or must be added separately. This is a theoretical finite-circuit existence result, not an optimized gate estimate or an implemented quantum compiler.

## Precise model
For independent stationary symmetric signs xi_i with flip rates lambda_i, the system Hamiltonian is

H(t)=H0+sum_i sqrt(gamma_i lambda_i) xi_i(t) A_i.

H0 and A_i are bounded Hermitian operators. Let alpha0 and a_i be their supplied block-encoding normalizations, and Gamma=sum_i gamma_i a_i^2. The noise operators may be arbitrary and mutually noncommuting. Parameters and prescribed control times have finite rational or certified descriptions. Encodings are exact or precision-capable, with their precision-dependent costs paid.

For a finite horizon T, p prescribed control slots and error epsilon, the target bound is polynomial in

r, 1+alpha0*T+Gamma*T+p, input/register lengths,
log(2+sum_i lambda_i*T), and log(1/epsilon),

plus the supplied encoding and consumer-operation costs. The error is unconditional output trace norm, uniformly over reference-entangled inputs, arbitrary instruments and adaptive operations at the prescribed slots, with all external outcome records retained. The internal reservoir, event times, source registers and counter stay private.

## The mechanism
1. Replace each classical sign by a ground-initialized amplitude-damped qubit, coupled transversely through its X observable. A closed moment hierarchy proves exact equality of the whole controlled system process, not just its final state.
2. The new positive trajectory representation has jump-count generating function bounded by exp[Gamma*T(exp(theta)-1)]. This controls expected count and tails independently of the rapid switching rates. It is not a Poisson thinning or pathwise-intensity bound.
3. Construct the expensive no-jump operation rather than assume it. A positive Metzler majorant factors into two-state kernels. Their Doob transforms have slow upward rates and fast downward returns. Endpoint-conditioned virtual bridges generate the needed operator averages with a bounded number of events and explicitly priced finite precision.
4. Compile the complete first-event isometry, including no event and all first-event times/types. Its normalization is integrable and permits amplification; amplifying a lone nonunitary no-jump operator would not preserve the right probabilities.
5. Factorized row/column preparations avoid enumerating 2^r reservoir states. Shorter windows keep their normalization bounded, while the complete isometry uses only polynomial amplification overhead. Weighted Schur bounds prevent an exponential error loss.
6. Preserve the physical reservoir qubits across every event and intervention. Count-augmented capped dynamics, common-uniform time coordinates and explicit duration errors close the finite controlled-process comparison.

## Reading order
- EXACT_DAMPED_ANCILLA_AND_COUNT_BOUND.md and DAMPED_ANCILLA_COUNT_REVIEW.md: exact representation and count bound.
- METZLER_BRIDGE_FIRST_EVENT_COMPILER_CANDIDATE.md, FINITE_BIT_FIRST_EVENT_COMPLETION.md and TWO_MODE_WHOLE_REVIEW.md: complete two-mode construction and its numerical/source details.
- FACTORIZED_MANY_MODE_EXTENSION_CANDIDATE.md, FINITE_BIT_MANY_MODE_COMPLETION.md and MANY_MODE_WHOLE_REVIEW.md: separately reviewed extension to a variable number of modes.
- FAILED_SCALAR_PATH_JOIN.md: why merely retaining uniformly accurate scalar integrated paths is insufficient for noncommuting operators.
- PRIMARY_COMPARATORS_AND_SCOPE.md: ordinary methods and limits of the comparison.

## Checks and limitations
Small dense two-mode checks compare the alternative dilation with the classical-sign generator and check tilted jump moments. Virtual-bridge Monte Carlo checks test the operator-weight identity. Factor-normalizer checks cover up to 64 modes and rates spanning many orders of magnitude. These are diagnostics, not certified sampler implementations or quantum-circuit execution. The mathematical proofs and their scoped reviews carry the guarantees.

No historical novelty, optimality, practical speedup, experimental demonstration or reduction of physical device noise is asserted. The result does not acquire unknown noise parameters or free operator encodings. Independent source processes are required; arbitrary cross-correlated switching generators are not covered. Prescribed timing is required; unrestricted adaptive intervention times and exposed private event records are outside scope. Normalizing an arbitrarily rare postselected outcome can amplify error. Statistical observable estimation still pays its own sampling costs.

Earlier delivered recovery and single-operator archives remain unchanged. This is a separate research checkpoint, not a claim of publication or integration elsewhere.

The final many-mode review uses the included filename for its earlier review reference. Only that source-location label was normalized for this edition; its mathematical text and all source checksum bindings are unchanged.
