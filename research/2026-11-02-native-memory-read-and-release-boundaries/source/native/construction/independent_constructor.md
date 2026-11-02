# Independent construction framework: decoder-boundary thermal stability

Status: independently derived before inspecting the native construction. A conditional route, not a proof that generic perturbations preserve the memory. Exact-model starting facts are supplied by parent, not independently verified.

## Positive mechanism

Keep decoder-dressed logical Pauli observables A_X,A_Z,A_Y. Do not attempt to perturbatively diagonalize the entire many-body spectrum. For a bounded-support physical Pauli E, the original decoder identity should imply [E,A_i](1-P_bad(E))=0, with P_bad(E) a decoder-crossing syndrome witness projector. For Hermitian local V=sum v_a, each v_a has only O(1) Pauli components since local dimension/support are bounded. Thus coherent imperfections can act nontrivially on a recovered qubit only near rare decoder boundaries. Exact conservation is unnecessary if these boundaries remain rare in the actual perturbed stationary state.

Target hypothesis, uniformly for all allowed local interaction imperfections of local norm <=epsilon:

 Tr(tau_epsilon P_bad(r)) <= poly(N) exp[-a(epsilon,beta) L^alpha]

for the required bounded or slowly growing supports r, with a>0. tau_epsilon is the actual Gibbs state of H0+V (or the actual physical stationary state, if not exactly Gibbs). This is a noncommuting finite-temperature witness-stability theorem. It cannot be replaced by ground-band stability or global trace distance to tau_0.

## Elementary weighted-norm leverage

For ||B||<=b and B=B P, ||B||_{2,tau}^2=Tr(tau B†B)<=b² Tr(tau P), without requiring [P,tau]=0. Consequently, local commutator support on rare witnesses gives ||[H,A_i]||_{2,tau} <= O(N epsilon) sqrt(p_bad), assuming [H0,A_i]=0. Losing half the exponent is harmless. This is not the useless O(N epsilon) global generator bound: rarity multiplies the local imperfection.

For any stationary unital CP Heisenberg semigroup T_t, Kadison plus stationarity implies ||T_t B||_{2,tau}<=||B||_{2,tau}. Hence

 ||T_t A-A||_{2,tau} <= t ||L† A||_{2,tau}.

Thus an exponentially small weighted generator residual gives an exponentially long logical-observable autocorrelation lifetime. Reversible Dirichlet-form estimates can improve powers, but are not needed for the basic mechanism. A full quantum-memory theorem additionally needs an encoding/recovery lemma converting simultaneous logical Pauli autocorrelations into entanglement fidelity for an admissible initialization; this does not automatically follow from one scalar autocorrelation.

Dissipators require care: D_J†(A)=1/2(J†[A,J]+[J†,A]J). Right multiplication is not uniformly contractive in a nontracial GNS norm; either prove boundary support for the complete expression and use its operator norm, establish thermal modular bounds for J, or use a detailed-balance Dirichlet form. Do not silently use a tracial norm inequality.

## Physical bath requirement

Use fixed bath correlation time and fixed small microscopic coupling, with finite-frequency resolution or a nonsecular construction retaining nearly degenerate transition coherences. Exact secularization at each finite L can distinguish exponentially close logical-sector frequencies before the thermodynamic limit and produce a discontinuity. A merely small uniform master-equation approximation error still accumulates over exponential times; prove protection for the actual model or show that the approximation's local corrections obey the same witness estimate.

Quasi-local bath kernels need quantitative tails. Truncating a jump at fixed radius leaves a fixed error floor. Instead sum range-dependent boundary estimates against the tail, or truncate at a size-dependent radius and balance the exponents. No claim of exponential protection follows merely from the words 'quasi-local'. A nonsecular generator may fail exact Gibbs stationarity; its stationary witness estimate is an additional obligation, not free from its short-time accuracy.

## Proof program for the genuinely new step

Represent perturbations by imaginary-time connected polymers atop the exact syndrome/auxiliary partition function. Show a decoder-crossing event must be accompanied either by an original thermal contour or a connected quantum polymer of macroscopic witness size. Integrate auxiliary states without discarding thermally occupied bands. Bound polymer activity and multiplicity with constants uniform in N, then obtain positive renormalized tension for a fixed interval epsilon<epsilon_0(beta). Local virtual defects of density O(epsilon²) need not kill protection; they must be dominated by a subcritical local-stochastic defect process. This remains a hypothesis until a model-specific cluster bound is proved. Classical Peierls data alone need not imply the quantum expansion; noncommuting resonances and extended thermal backgrounds are the central obstacles.

Crucially, no all-spectrum quasi-adiabatic continuation or exact dressed conserved algebra is requested. The objects to stabilize are the probabilities of decoder-boundary witnesses and the locality of actual noise terms.

## Strong conventional comparators

1. Native two-body, bounded-dimensional, bounded-degree 3D comparator: Bacon's 3D subsystem/compass Hamiltonian. It uses precisely the natural two-body resource class; the original claim was mean-field evidence, not a generic-perturbation finite-temperature lifetime theorem. This is the clean resource-matched benchmark, rather than a 4D stabilizer code.
2. Best theorem-preserving generic compilation comparator: apply ordinary perturbative gadgets to the supplied hierarchical CSS memory. This matches spatial locality and constant ancillary dimension, but ground-band simulation errors or fixed thermal gadget defects do not by themselves transfer an exponential lifetime. A valid superiority claim must supply the full thermal/polymer witness bound above; exact gadget algebra alone is not robustness.
3. 3D subsystem toric/gauge-color-code single-shot constructions are important nearby comparisons but not native two-body proofs of passive self-correction. Published phase-diagram studies show that syndrome confinement by itself is insufficient. Their three-or-more-body checks also differ from strict two-body resources.
4. Haah/welded barriers, symmetry-enforced boundary memories, and 4D toric-code memory each relax a material requirement or lack the requested fixed-temperature/generic-perturbation conclusion. Do not present them as established same-resource solutions.

## Primary sources checked

- Dave Bacon, Operator quantum error-correcting subsystems for self-correcting quantum memories, PRA 73, 012340 (2006): https://journals.aps.org/pra/abstract/10.1103/PhysRevA.73.012340 ; original explicitly offers simple mean-field evidence in 3D.
- Bravyi, Hastings, Michalakis, Topological quantum order: stability under local perturbations: https://arxiv.org/abs/1001.0344 ; zero-temperature/low spectral-band result, not the required thermal theorem.
- Nathan and Rudner, Universal Lindblad equation for open quantum systems, PRB 102, 115109 (2020): https://journals.aps.org/prb/abstract/10.1103/PhysRevB.102.115109 ; nonsecular level-structure-independent Markov framework, not an exponential-time memory guarantee.
- Li et al., Phase diagram of the three-dimensional subsystem toric code, PR Research 6, 043007 (2024): https://kclpure.kcl.ac.uk/ws/files/363203481/Phase_diagram_of_the_three-dimensional_subsystem_toric_code_Version_of_Record.pdf ; syndrome confinement alone not sufficient.
- Kubica and Vasmer, Single-shot quantum error correction with the three-dimensional subsystem toric code (2022): https://arxiv.org/abs/2106.02621 ; active single-shot checks of weight three, distinct target.

No external mutation/contact/publication. No permissions blocker. Mathematical blocker: establish perturbed stationary witness probabilities, bath boundary-locality, and admissible quantum encoding/recovery at finite temperature.

## Comparator correction after inspecting the preferred construction's prior audit

The strongest direct native-gadget comparator is Ocko–Yoshida's exact nonperturbative two-body construction, not generic Schrieffer–Wolff gadgets or Bacon's mean-field candidate. The supplied primary-source audit in ../native_thermal_interactions_20261101/ocko_yoshida_shielding_audit.md establishes why: OY resolves non-ground sectors rather than simply ignoring them; a full thermal defect-component extension is plausible. Its simple two-clock shielding architecture does not directly apply to this actual hierarchical family, whose relevant check incidence reaches four in both CSS orientations. This is an architectural obstruction to that extension, not a universal OY no-go. Bacon remains a clean same-native-resource physics comparator but not the strongest implementation comparator. HPWL's two-body ferromagnet-mediated proposal is another serious primary prior, with size-tuned field and conditional thermal/adiabatic treatment. No historical priority claim is earned here.
