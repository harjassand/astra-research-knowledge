# Independent audit: unary resonant clock compiler

2026-11-03. Sources: `resonant_clock_compiler_20261102/resonant_rod_bound.md`, its fresh audit, `native_thermal_interactions_20261101/root_rod_audit.md`, and `temperature_uniform_protection_20261102/ROOT_ANNEALED_NATIVE_MEMORY_JOIN.md`.

## Verdict

No fatal obstruction to the exact all-qubit, at-most-three-body embedding was found. The N=1 restriction is exact. The proposed leakage trace bound is sound. Neither alone transfers the full-temperature native theorem: the new number sectors must be included as potentially flux-bearing full-circle polymers, and their rooted influence must be controlled. The generic Hamiltonian-source theorem is a separate extension, not an automatic corollary of encoding.

## Hamiltonian and exact restriction

Use K qubits indexed 0,...,K−1, n_j=(1−Z_j)/2, N=sum n_j. Replace each native |j><i|+|i><j| by sigma_i^+sigma_j^-+sigma_i^-sigma_j^+=(X_iX_j+Y_iY_j)/2. Multiplication by the corresponding single-data-qubit Hermitian Pauli gives two three-body Pauli terms; identities give two-body terms. Keep 2t sum_{j>0}n_j, internal hopping amplitude −t, both endcap amplitudes −g, and add U(N−1)^2.

N commutes with the unperturbed Hamiltonian. In the basis |j>=one excitation at j, the N=1 restriction is exactly the K-level clock, with no perturbative encoding error or factor-of-two discrepancy when the displayed exchange normalization is used. Its J0=2eta²t/K³ remains exactly the same native rod coefficient, subject to the same finite-temperature and multirod corrections.

## Leakage trace bound

For scalar absolute histories the internal path operator is

H_path = 2t sum_{j>0} n_j − t sum_{j=1}^{K−2}(b_j†b_{j+1}+b_{j+1}†b_j).

Writing H_path=sum_{ij}b_i†A_ij b_j and A>=mu I proves H_path>=mu N_path>=0. This quadratic-form argument holds for hard-core operators and does not require canonical bosonic commutators. The same single-clock statement with data labels follows by its occupation-controlled prefix gauge on the open path. Each endcap exchange has operator norm g, so their sum is >=−2g. Every N≠1 block has penalty at least U. Consequently

Tr_{N≠1} exp(−beta H_abs) <= (2^K−K) exp[−beta(U−2g)].

This bounds the absolute Duhamel measure, not merely a signed physical trace. It includes N=0, all multiple-occupation sectors, and all histories in them. It does not assert their probability is zero or that all clocks remain valid with high global probability. At positive temperature and fixed U, extensive volume generally contains leakage clocks.

## New full-circle polymers are not the old wraps

N is conserved between source insertions, so an N≠1 clock history is a full-circle object. In N>=2, particles may traverse the closing edge while the clock never becomes a one-particle vacuum. Its closing-edge parity may therefore carry the syndrome flux. The native N=1 never-zero wrap has no closing-edge hop and is flux-free; that old statement must NOT be applied to the new species.

Retain the full internal occupation trajectory and its flux parity. The absolute activity above is compatible with a new wrap species. With native KP charge a0+b beta, its charged activity is bounded by

(2^K−K) exp[−beta(U−2g−b)+a0].

This charged quantity, not the uncharged probability alone, enters the wrap KP row. Its influence on free energy must include both directly flux-bearing leakage wraps and ordinary marked-winding clusters connected to leakage wraps. Merely proving small leakage density is not the required rooted Fourier/local-influence estimate. A bound such as volume times leakage probability is insufficient for fixed-U thermodynamic-limit retention.

## Pair signs and logical algebra

Extend the gauge to a product of n_j-controlled data prefixes, using a fixed order across clocks. For an occupation pattern on one clock its controlled data Pauli is the product of the occupied prefixes. A single hop changes this by its edge factor, leaving only a closing-edge stabilizer and commutation signs against other clock occupation-prefix products. Signs therefore remain pairwise between full clock trajectories; they depend on entire occupation histories, not on one particle coordinate. This needs an explicit extension of the old algebra but introduces no necessary three-clock sign.

For a normalizer data Pauli E, set b_j=[E,P_j]. Then E times product_j Z_j^{b_j} commutes with every physical labelled exchange term: b_i+b_j equals [E,sigma_edge], including the closing edge because [E,S]=0. It commutes with the diagonal penalty. This is an exact full-Hilbert-space logical symmetry, not restricted to N=1.

Physical single-qubit X/Y baths change N. They cannot be projected out. The extended controlled-prefix Clifford sends such a contact to a bounded-prefix data operator times ancillary operators; the data support is at most K−1. A Davies transfer based on the full Gibbs unsafe-syndrome bound and exact logical conservation can thus survive with enlarged bad neighborhoods and all physical qubits counted. This does not supply that static bound, nor extend it automatically to generic Hamiltonian errors.

## Resource accounting

U(N−1)^2 = constant − U(K−2)/2 sum_j Z_j + (U/2) sum_{i<j} Z_i Z_j.

There are K(K−1)/2 penalty pairs per clock, degree K−1, peak explicit single-Pauli coefficient O(KU), and per-site summed coupling strength O(KU). In occupation-projector notation the same expression is U−U sum n_j+2U sum_{i<j}n_i n_j; changing notation does not remove the incident interaction budget. Fixed K gives volume-bounded constants but not K-independent degree or nearest-neighbor interactions. Spatial packing/range must accommodate the full penalty clique. This is O(K²) Hamiltonian terms, not O(K), despite using K physical ancilla qubits.

At fixed eta, the N=1 induced energy is polynomially suppressed, J0/t=2eta²/K³, instead of the simple ring's (g/Delta)^K. Leakage penalties and charges can retain polynomial strength requirements if their inequalities close. However the unary clock has 2^K physical states instead of K, and unrestricted generic source insertions can access all of them. The previous full-column source dimension factor K^b cannot silently be retained: a direct full-state estimate has (2^K)^b before any sharper sector-resolved argument. Thus polynomial cooling improvement is not automatically polynomial generic-imperfection tolerance.

The deterministic scale-eight source uses conservative K=180; the distinct published random-embedding source can have K<=7. Do not interchange their geometry or thresholds. No matched-resource active-memory advantage, noisy WRITE construction, stationary-state preparation algorithm, or useful practical operating point follows from this compilation audit.

## Concrete static closure route

There is a simple way to preserve the native constants rather than discard the extension. Impose the ORIGINAL total wrap budget on the sum of species:

W_native(b)+W_leak(b) <= eta²/K,
W_leak(b) <= (2^K−K) exp[−beta(U−2g−b)].

The native ordinary-root and wrap-root overlap rows then hold unchanged: both kinds of wraps occupy the full time circle, same-clock exclusion is hard core, and other-clock pair factors have modulus one. Every Fourier monomial containing a is marked either by an ordinary winding rod on a or by a flux-bearing leakage wrap on a. The old ordinary marked-root estimate already includes leak-connected clusters in its unchanged exp(a0+b length) charge. Marking a leakage wrap contributes at most

e^{a0} W_leak(b)/beta

to the rooted absolute free-energy coefficient sum, since a wrap has no free start integral. Thus the existing relative remainder can be enlarged by

e^{a0} W_leak(b)/(beta J0).

Spatial inflation should be applied to this new root consistently with the old convention; any fixed extra root factor can be explicitly paid by its leakage budget. Under these inequalities and the explicitly extended pair-history identity, the static local-influence argument appears to close. This is stronger than a mere leakage-density estimate and avoids a global all-valid-sector event. It still does not transfer the separate generic-source theorem without its new full-state dictionary accounting.
