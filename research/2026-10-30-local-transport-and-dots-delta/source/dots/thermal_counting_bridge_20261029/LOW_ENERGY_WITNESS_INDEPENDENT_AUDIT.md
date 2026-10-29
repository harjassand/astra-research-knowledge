# Independent audit: low-energy mixed-state witness and product-Pauli access

Date: 2026-10-29 UTC. Auditor: `challenge_thermal_counting_consequence`.

## Verdict

**Conditional mathematical PASS**, with exact sampling in **expected** subexponential time and product measurements on **distinct** sites. The imported sparse exact-counting theorem remains an explicit unverified premise of this audit. This is not quantum state preparation, true-Gibbs approximation in trace/total-variation distance, or polynomial-time classical witness verification. No historical novelty is certified.

The scalar/counting receipt remains unchanged; this audit concerns the separate `LOW_ENERGY_WITNESS_DRAFT.md` extension and its own regression test.

## 1. Energy guarantee actually follows from the norm theorem

The existing physical theorem bounds `||log P + delta H'||`, not merely a free-energy difference. Together with local rounding, it yields

`||A-H||<=n tau/2`, where `A=-(r/beta)log P`.

Since `P>0`, the state `sigma=P^r/Tr(P^r)` is exactly the Gibbs state of the generally nonlocal Hermitian A at inverse temperature beta. Its variational free energy is at most E0(A), so

`Tr(A sigma)=F_beta(A)+S(sigma)/beta <=E0(A)+n ln2/beta`.

Ordered eigenvalue perturbation and the norm bound on expectations give

`Tr(H sigma)-E0(H) <=2||A-H||+n ln2/beta <=5n tau/4`

for beta=4/tau. In particular tau=epsilon/2 gives a stronger-than-required `5n epsilon/8` upper bound. The lower bound `Tr(H sigma)>=E0(H)` is automatic. No locality of A, fidelity to a ground state, thermodynamic limit, or Gibbs correlation assumption is used.

The matrix sigma is rational-complex, positive definite, and trace one. Its polynomial-size representation is a list of local rational matrices, the ordered positive palindrome, its repetition count, and its exact positive rational trace normalization. It is not an explicitly listed exponentially large density matrix.

## 2. Exact trace insertions and conditional probabilities

Fix a Pauli X,Y,or Z on each of some distinct sites, and an ordering of those sites. Their outcome projectors `(I plus-or-minus Pauli)/2` have Gaussian-rational entries and commute across sites. For a prefix of outcomes, let Pi denote their tensor-product projector. Then the correct unnormalized mass is

`w(Pi)=Tr(Pi P^r)`.

Appending these one-site matrices to the trace circuit creates at most n further constant-locality gates. The existing signed-count compiler therefore still has `N=O(n r B+n)` variables and uniformly bounded-width/density 3-CNF. Projector denominators can be tracked per gate; alternatively rescale them to a common dyadic denominator. Either way the two children at the same prefix depth have the same denominator. The real mass is an exact difference of two counts divided by the known power of two.

For this strictly positive definite sigma and every nonzero valid prefix projector, w(Pi) is actually **strictly positive**, though it may be exponentially small. A generic implementation may handle zero child masses, but valid distinct-site Pauli prefixes in this construction do not require that branch. No lower-bound promise on a conditional probability is used.

The identity `Pi_+ + Pi_- = Pi_parent` gives exact conservation of unnormalized masses. If the common-denominator child integer numerators are a,b, draw a uniform integer in `[0,a+b)` and select the first outcome iff it lies below a. Rejection from `ceil(log2(a+b))` fair bits takes fewer than two trials in expectation. These integers have O(N) bits even under severe signed cancellation or rare-prefix conditioning.

Each sample uses O(n) deterministic exact-count queries and polynomial-space integer arithmetic. Random generation has unbounded geometric worst-case running time; the resulting exact sampler has **expected** `poly(input length,n) 2^{o(n)}` running time at the audited fixed/logarithmic accuracy schedules. A finite random-bit cap must charge a failure/approximation probability explicitly. Repeated incompatible measurements on the same qubit are not covered by this product-projector formula.

This is classical sampling of a chosen quantum measurement distribution. It does not mean an outcome bit string itself is a low-energy quantum state. It does not produce a hardware state or an arbitrary collective measurement oracle.

## 3. Exact local expectations and an evaluated energy upper bound

For a Hermitian local Pauli string O, `Tr(O P^r)` is real, although its individual path summands can be complex. The same signed counts give its exact rational normalized expectation in sigma. Every supplied rational Hermitian local h_e has a constant-size Pauli decomposition with rational coefficients. Therefore O(m 4^k)=O(n) such queries compute `Tr(H sigma)` exactly as a rational number (with polynomial input-bit overhead). This can accompany the state description as an evaluated upper bound on E0(H).

It is not a polynomial-time verification certificate: evaluating those contractions still uses the imported subexponential counting procedure. Merely writing a compact unnormalized positive tensor expression is cheap already; the consequential computational access provided by the hypothesis is normalization, contraction, and sampling.

## 4. Independent replay and software scope

I read `check_witness_sampler.py` and its JSON, copied the program into `independent_replay/`, executed the copy successfully, and compared its JSON byte-for-byte against the root result. `cmp` succeeded.

The exact test uses a two-qubit positive palindrome with noncommuting and genuinely complex gates, repeats it twice, and checks all 9 product-Pauli bases, 36 joint probabilities and 18 prefix-conservation identities. Its normalization numerator is 173284. It compares a signed phase-lift contraction with independent exact dense matrix traces; all checks pass, including equality of imaginary phase counts. This is useful evidence for projector insertion and prefix normalization, not evidence about Monte Carlo convergence.

The test does not run the imported full #SAT algorithm, instantiate a full width-3 compiler, execute random rejection draws, or prepare a quantum state. It also does not numerically validate the analytic low-energy estimate against an arbitrary input H; that guarantee was checked algebraically above. The earlier independent compiler regression certificate remains separate.

## 5. Primary comparisons and limits on interpretation

- [Buhrman, Gharibian, Landau, Le Gall, Schuch and Tamaki, arXiv:2407.03073v3 (July 2025), Theorems 1–2](https://arxiv.org/html/2407.03073): their arbitrary-local-Hamiltonian results include a classical energy estimator beating the base-2 brute-force exponent and a quantum algorithm that physically prepares a low-energy mixed state. The latter has exponential runtime `O*(2^{(1-epsilon/(2k+epsilon))n/2}/epsilon)` for error `epsilon sum ||h_e||`. The present conditional expected-subexponential *classical measurement access* is a weaker output model than physical preparation, not a direct replacement for that theorem. Appendix C also distinguishes low-energy-space support from ground-state overlap.

- [Le Gall, arXiv:2410.21833v2, Theorem 2](https://arxiv.org/html/2410.21833v2): the unguided arbitrary-Hamiltonian scalar energy algorithm already achieves `2^{O(n)}` time and polynomial space. Its guided algorithms assume useful sample/query access; such a guide is not an input promise here. Scalar estimation alone is not the new measurement-access object.

- [Bakshi, Liu, Moitra and Tang, arXiv:2403.16850v2 (February 2025)](https://arxiv.org/abs/2403.16850): their efficient classical sampling of a product-state mixture supports trace-distance approximation and physical preparation of the *actual* Gibbs state at sufficiently high temperature. The current revision states a preparation regime with inverse temperature below `1/(c d^2)` and polynomial `(n,1/accuracy)` overhead under its normalization. This is a stronger accuracy/output guarantee in a restricted temperature regime, not the same all-low-temperature energy-witness problem. Do not quote the older version's different quantitative regime as current.

- [Jiang, *Local Hamiltonian Problem with Succinct Ground State is MA-Complete*, arXiv:2309.10155v3](https://arxiv.org/abs/2309.10155): succinctness there entails a polynomial-size amplitude-computing classical circuit. A polynomial-size mixed-state tensor description whose contractions take subexponential time does not supply that promise.

- [Weggemans, Folkertsma and Cade, TQC 2024, Definition 1 and Conjecture 12](https://drops.dagstuhl.de/storage/00lipics/lipics-vol310-tqc2024/LIPIcs.TQC.2024.10/LIPIcs.TQC.2024.10.pdf): classically evaluatable states there are pure states with polynomial-time computation of O(log n)-local observable expectations. Their no-low-energy-classically-evaluatable-state conjecture is not refuted by subexponential access to this mixed state. Related no-low-energy-sampleable-state notions likewise should not be conflated with the current access guarantee.

The sampling step is a natural exact-counting self-reduction once prefix contractions are available. It should not be presented as a separately novel sampling principle. Its useful consequence is operational: a common positive low-energy witness supports all the requested product-Pauli measurement queries, instead of only furnishing an unrelated energy number for each input.

## Receipt boundary

This certificate covers the revised distinct-site/expected-time scope, the algebraic witness energy bound, the inherited linear/quasilinear exact-counting reduction under projector insertions, and the precisely stated successful test replay. It does not certify historical priority, practical numerical superiority, a polynomial-time certificate, physical preparation, true-Gibbs total-variation accuracy, or the imported #SAT theorem itself.

## Frozen version receipt (17:44 UTC)

The final reviewed witness draft includes all three clarifications: distinct-site measurements, expected exact-sampling time, and strict positivity of valid prefix weights. Its evaluated-energy paragraph also agrees with Section 3 above. Frozen files:

- `LOW_ENERGY_WITNESS_DRAFT.md`: SHA256 `7d2c97e70b3694a81cc37f4e352940b410d93f3b0c7446fe13ceb10a9ee6d9a6`.
- `check_witness_sampler.py`: SHA256 `5695f2a80005f8cb4536d0f9255fbe00eb902c580438c2bb413304d421b33dac`.
- `check_witness_sampler.json`: SHA256 `e85916745ff663a44a55aa8785487a7124e729c91e93d7b9e7c0a61aea997a4c`.

The synthesis `LINEAR_VOLUME_REDUCTION.md` was read for consistency but is deliberately outside this frozen receipt. The optional higher-order candidate is likewise outside this receipt and is not being pursued under the active task.
