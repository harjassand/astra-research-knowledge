# Beyond a scalar energy: an explicit low-energy state and its product-measurement sampler
2026-10-29. Root extension, independent review pending. Conditional counting premise unchanged.

Use the completed thermal/counting construction with internal accuracy parameter tau. Let H' be the nearby local Hamiltonian defined by the rational gates, P=Q_G^dagger Q_G, and
 A=-(r/beta)log P, sigma=P^r/Tr(P^r).
The physical product-formula bound and rounding bounds give ||A-H||<=n tau/2 (tau/4 from each). Although A itself need not be a local matrix description, sigma is explicitly described by the polynomial-size positive tensor expression P^r and exact positive rational normalization Z_r.

By the Gibbs variational identity and 0<=S(sigma)<=n ln2,
 Tr(A sigma)-E0(A)<=n ln2/beta.
Therefore
 Tr(H sigma)-E0(H)<=2||A-H||+n ln2/beta<=5n tau/4
for beta=4/tau. Taking tau=eps/2 gives a known state with energy density within eps of the true minimum, with slack. This is a witness for low energy, NOT a claim that sigma is globally close to the true Gibbs state or a particular ground state.

## Exact classical access to chosen product-Pauli measurements
For any chosen product basis, with one X,Y,or Z measurement on each of a set of DISTINCT qubits, the probability of any prefix of outcomes is
 Tr[(Pi_prefix tensor I_remaining) P^r]/Z_r.
Each local Pauli projector has Gaussian-rational entries with denominator2. Append these local matrices to the same trace tensor network. The signed-count compilation still has O(n r B) variables and constant clause density. The resulting exact rational number is nonnegative. It is strictly positive for a valid distinct-site prefix, but can be exponentially small; no supplied probability lower bound is required because it is counted exactly, not estimated by rejection from signed paths.

At each site compute the two child prefix weights. They sum exactly to the parent weight since Pi_++Pi_-=I. Draw the next outcome from their exact rational ratio, using integer rejection sampling with expected fewer than two trials. There are O(n) calls to the conditional counting routine, so the EXPECTED subexponential-volume time and polynomial-space bound is unchanged. Exact fair-bit rational sampling has unbounded geometric running time; the count computations themselves are deterministic and there are O(n) such queries. A finite random-bit cap gives only an approximate sampler with an explicitly charged failure probability. A prior choice of any product Pauli basis is allowed; it is not an arbitrary collective measurement or a state-vector reconstruction. The same construction also gives exact local Pauli expectations of sigma by adding one observable and evaluating its signed trace.

Thus the construction provides an explicit positive quantum-state description plus a classical sampler for its experimentally meaningful local measurement statistics, in addition to its low-energy guarantee. This is stronger than outputting an energy number, but weaker than preparing the state on quantum hardware. A physical implementation of the nonunitary gates would have postselection/success costs which are NOT removed here.

## Accuracy and practical limits
The sampler is exact for the rational product-formula witness sigma. It is NOT claimed to sample the original Hamiltonian's true finite-volume Gibbs distribution in total variation: near phase coexistence an O(n tau) Hamiltonian perturbation can change phase weights by order one. Energy-density proximity does not imply trace-distance proximity, fidelity to a ground state, or correctness of every observable of the original Gibbs state.

The logarithmically vanishing accuracy schedule of VANISHING_ACCURACY_ADDENDUM.md applies with a constant rescaling of eps. The imported subexponential #SAT algorithm remains an asymptotic premise, not an implemented practical solver. No historical novelty or finite-size speed advantage is asserted.

## Evaluated witness energy
Because each original rational Hermitian local term has only O(4^k) rational Pauli coefficients, O(n) exact local-Pauli trace queries compute Tr(H sigma) exactly. Thus the construction can return the evaluated energy of its explicit mixed-state witness, not merely an existence statement. This still uses subexponential counting work, not polynomial-time verification.
