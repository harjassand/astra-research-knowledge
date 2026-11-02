# Conditional native thermal-memory transfer: exact missing premise

This is a conditional construction, not a completed theorem. It makes the finite-temperature implementation gate explicit.

Let the actual bounded-degree CSS family have commuting checks S_a, one encoded qubit, local decoder crossing witnesses and the previously established positive trace-polymer representation. Pad clock loops to fixed K (e.g.7). The native Hamiltonian has fixed K-level clock ancillas and only onsite/two-body terms. The exact bounded-depth controlled-Pauli U makes U†H_nat U=H_anc(S), hence commutes with every check and every decoded logical observable.

Required premise: for every finite volume and all valid syndromes s, at fixed beta, Delta,t,

 F_beta(s):=-beta^-1 log Tr_anc exp[-beta H_anc(s)]
 =c -J0 sum_a s_a + sum_nonempty A r_A product_(a in A) s_a,

with J0=2t^K/Delta^(K-1) (or an explicitly calibrated nearby coefficient) and a volume-independent weighted-local bound

 sup_a sum_(A contains a) |r_A| <=epsilon J0.

A spatial exponential support weight is useful for construction but this unweighted influence bound alone controls syndrome deletion energies. For syndromes s,s' differing on D,

 |R(s)-R(s')|<=2 epsilon J0 |D|.

Consequently deleting a valid trace component containing m negative checks lowers F by at least 2J0(1-epsilon)m. The trace witness injection therefore receives no worse Boltzmann factor than exp[-2beta J0(1-epsilon)m]. All existing combinatorial entropy/counting constants remain explicit. This is stronger and more task-relevant than approximating the total partition function or total ground energy within O(epsilon*n).

Full clock Gibbs states need not be product states or close in global trace norm to their vacuum. Their conditional partition functions alone enter the syndrome Gibbs weights. Real clock excitations are included in F_beta.

For a Davies consumer, bounded-local native contacts become bounded-support data+ancilla contacts after U. Spectral resolution can make ancilla coefficients spatially global, but because H_anc(S) is exactly identity on the logical factor, it cannot enlarge the data Pauli footprint relevant to decoder correctness. One must prove this operator-algebra statement and charge bounded bath rates; a separate audit is in progress. No arbitrary strongly correlated bath, no generic Hamiltonian perturbation, no noisy physical loading/readout claim follows automatically.

## Fixed-resource scaling
To hold J0 constant, set t=(J0*Delta^(K-1)/2)^(1/K). Then r=t/Delta=(J0/(2Delta))^(1/K). For a fixed target epsilon, sufficiently large but VOLUME-INDEPENDENT Delta and t would suffice if the cluster premise is earned. Native local dimension K, density, interaction range and degree remain fixed. These constants may be extremely large; theoretical bounded resources are not practical hardware. The same Delta,t,temperature and noise assumptions must be used in comparisons.

## North-star connection and stop condition
The intended step removes a physical interaction-order obstacle to passive quantum protection, not merely a simulator stage-count. Its value requires a full-temperature witness theorem and operational comparison with strongest clock/nonperturbative gadgets. If the cluster premise fails, retain exact gauge structure and finite checks, but do not call the native thermal memory constructed. If it succeeds, the next decisive gaps are robustness to actual interaction imperfections and physical loading/readout; neither is solved by exact logical conservation in a calibrated Hamiltonian.
