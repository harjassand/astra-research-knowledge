# Root join candidate: constructive thermal syndrome preparation for the actual recursive 3D memory

1 November 2026. Awaiting whole actual-binding review. Ideal commuting-state preparation only.

## Claim
Fix the actual random-embedding RX/RZ code family, its fixed construction parameter ell, all actual redundant check coordinates, and the SAME deterministic decoder used to define the protected logical subsystem, including the whole level-2 terminal decoder of source §5.1.1. Let H0=sum_a J_a(I-S_a)/2, with known efficiently computable positive couplings in a fixed bounded interval.

There is a sufficiently large but fixed beta0 such that, for beta>=beta0 in any fixed finite interval, the classical Gibbs distribution on valid syndromes can be sampled to total variation epsilon in time polynomial in n/epsilon. Fixed-ell local preprocessing, gate tables, memory and precision are charged and may be enormous. This is a constructive ideal sampler, not a passive local thermalization/mixing result.

With a supplied encoded ground-state logical input and ideal application of the matched decoder's Pauli representative, it yields the thermal logical-encoding channel of the commuting model. TV error epsilon gives reference-safe trace-norm channel error at most2epsilon. The encoded input may be entangled with an arbitrary external reference.

## Earned or audited interfaces
1. Source §§4.1–4.3 gives local zero-preserving coarse syndrome reduction, alternating factor-one and factor-one-half contraction and local correction identities. The memory's final decoder is the modified §5.1.1 level-2 block, not an unmodified five-qubit seed.
2. Actual binding constructs an ALL-input local recognizer: local image tests, explicit coordinatewise reconstruction checks, and the finite terminal image test. Acceptance implies global syndrome validity by telescoping the checked chain-map identities; validity implies acceptance by the source's cleaning theorems.
3. Full-input gate stencils mark cancellation gates. The abstract separately reviewed trace lemma gives unique decomposition into independently valid components and exact recombination of compatible components.
4. The actual decoder's total active footprint is at most A|sigma|, with A independent of family level. Its typed host has O(n) objects, bounded degree and finite labels for fixed ell. Downward physical correction expansion is excluded from this footprint and charged separately after sampling.
5. The exact positive gas has weight w_gamma=exp(-beta sum_a J_a sigma_gamma,a), not guessed coarse-grained energies. Hence w_gamma<=exp(-beta J_min|gamma|/A). All valid syndrome eigenspaces have equal dimension, so no error-representative multiplicity distorts the weights.
6. Low activity admits established polymer samplers. The root's explicit truncated dictionary/birth-death proof is a conservative polynomial fallback. Chen et al1901.06653v6 gives a stronger potentially near-linear classical sampler once the local membership/weight contract is implemented in its computational model. The sampler itself is established machinery, not our invention.

## Conservative constructive costs
Let Delta and M bound typed host degree and local labels. Enumerate connected labeled traces of size at most L=C log(n/epsilon), locally validate them, and weight their top syndrome energy. The number of candidates is at most O(n)(c Delta M)^L. For sufficiently low fixed temperature, the omitted polymer mass is O(n)q^L with q<1. On the finite dictionary, birth rate w_gamma and death rate1 satisfy the weighted path-coupling contraction whenever sum_incompatible_eta w_eta|eta|<=theta|gamma|, theta<1.

Uniformize at R=sum_gamma(1+w_gamma) and simulate time t=log(2N/epsilon)/(1-theta). Cap the Poisson event count at ceil(2Rt+2log(1/epsilon_cap)); the cap failure probability is at most epsilon_cap by the mgf at log2. Approximate each transition probability to per-event TV error at most epsilon_prob divided by the cap. Truncation, mixing, cap and finite-precision errors are separately allocated within epsilon. No exact-real or unbounded-runtime sampler is necessary.

The stronger established sampler should replace this dictionary method where the supplied local membership implementation meets its contract. Gate-table preprocessing and bit-complexity remain explicit even when the word-RAM sampler is near-linear.

## Quantum operation
For sampled sigma, use the matched representative E_D(sigma). Applying it to Enc0(rho_LR) gives the decoder-frame state rho_LR tensor |sigma><sigma|. Averaging over exact Gibbs syndrome weights gives rho_LR tensor tau_syndrome. Orthogonality of syndrome blocks makes the trace-norm discrepancy exactly sum_sigma |p(sigma)-p_tilde(sigma)| for every input/reference state, hence at most2epsilon.

Classical reconstruction through the hierarchy is polynomial; actual correction is a product of single-qubit Paulis, but addressing, signal propagation, gate duration, always-on interactions and faults are NOT free. A separate ideal stabilizer encoder can be synthesized by known Clifford methods; this document does not certify its noisy physical implementation.

## Consequence and non-claims
This directly addresses ideal initialization of the actual commuting 3D code despite non-LDPC metachecks. It is not merely another bound on an already specified sampler: the exact constructible syndrome representation is the missing operation being supplied.

It does not prepare the actual joint Gibbs state of H0+generic noncommuting V and an inaccessible bath. Replacing that state by H0 Gibbs can create an extensive disturbance, however small the local V. It does not establish a constant-noise physical write/read threshold or a return-to-equilibrium theorem after noisy writing. Those remain the decisive end-to-end gates against an active fault-tolerant memory with identical control and entropy-export resources.

No practical constants, experimental result, peer review, or priority claim is asserted. The actual code and decoder are due to Balasubramanian–Davydova–Lin2605.10943v1; polymer sampling is established prior machinery. The contribution assessed here is the actual decoder-trace representation, validity recognition and resulting constructive initialization join.
