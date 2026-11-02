# Native two-body thermal memory: construction and precise scope

2026-11-01. Root reconciliation. Status: component proofs and the integrated statement have passed internal independent mathematical review under the assumptions below. This is a mathematical model construction, not a laboratory device or generic-noise theorem.

## Capability
The actual hierarchical three-dimensional CSS memory can be implemented by bounded-dimensional auxiliary clocks and geometrically local two-body interactions, at fixed interaction and temperature ratios independent of volume, while retaining its rare-decoder-crossing thermal protection under a specified bounded-rate Davies bath. Auxiliary clocks are fully thermally populated; no all-clocks-ground assumption is used. The physical Hamiltonian, encoding and bath hypotheses below are essential.

## Native construction and exact algebra
Use the actual source family with bounded check weight w<=7, bounded overlap degree, bounded geometric check diameter and one logical qubit. Pad each stabilizer product to K=7 one-site Pauli/identity factors. Give each check a seven-level clock, with energy Delta on every nonzero level and cyclic hopping -t times its associated data Pauli. Each nonidentity hopping term couples one clock to one data qubit; identity hops and clock penalties are onsite. All constants, local dimensions and density are independent of memory size. Arbitrary qubit-qudit two-body Hermitian couplings are admitted, not a restricted natural exchange interaction or qubit-only hardware.

The bounded-depth ordered controlled-prefix unitary U transforms the entire Hamiltonian into H_anc(S), whose data dependence consists solely of the commuting original stabilizers. The exact edge formula and local implementation of U are in exact_clock_algebra_receipt.md. This is full-spectrum algebra, not a Schrieffer–Wolff approximation. Shared-data X/Z anticommutation survives as ancillary pairwise trajectory signs; it is retained, not ignored. Every decoded logical observable commutes exactly with H_anc(S).

## Full thermal spectrum
The exact auxiliary trace has an excursion gas on the imaginary-time circle. Excursions away from clock zero are temporal rods; histories never reaching zero are wrapping rods. Pair factors are 0 or +/-1. The Ueltschi signed continuum gas theorem applies with explicit Kotecky–Preiss charges; beta*t need not be small.

Let r=t/Delta, B=beta*Delta, D count a clock and its overlap neighbors. Set mu>=0 for distance measured in the overlap graph, Dbar=D exp(mu), a0=64Dbar r^2, b=32Dbar t^2/Delta. Sufficient conditions are

 a0<=log2,
 2r+32Dbar r^2<=1/2,
 (K-1) exp[-beta(Delta-2t-b)+a0]<=r^2.

Then for every formal syndrome flux s, including every valid physical syndrome,

 F_beta(s)=-beta^-1 log Tr_anc exp[-beta H_anc(s)]
 =c_beta-J0 sum_g s_g+sum_nonempty A r_A product_(g in A)s_g,
 J0=2t^K/Delta^(K-1),
 sup_g sum_(A contains g) exp[mu diam(A)]|r_A|<=epsilon J0,

where a conservative explicit epsilon is

 exp(-B) sum_(j=0)^(K-2) B^j/j! +2^K r^2/(1-4r^2)+64K2^K Dbar r^2.

The proof and a second independently derived hopping-coefficient bound are in root_rod_audit.md and thermal_cluster_audit/EXACT_ROD_FREE_ENERGY_LEMMA.md. Diameter is ambient overlap-graph distance; conversion to physical diameter charges the fixed edge range. Thermal wrap terms and finite-beta normalization are explicitly included. Arbitrarily pinned excited external clocks are NOT covered.

Choose r sufficiently small, then B sufficiently large to make epsilon<1 and 2beta J0(1-epsilon) exceed the actual source's fixed low-temperature threshold. Since beta J0=2B r^K, these conditions are compatible. For a fixed desired J0, Delta=J0/(2r^K), t=r Delta and beta=B/Delta. All are fixed in volume, but the sufficient constants can be extremely large. No practical operating-point claim is made.

## Actual-code witness transfer
For syndromes differing on T, |R(s)-R(s')|<=2epsilon J0|T|. The actual source's bad-witness surgery removes a valid top coboundary tau contained in the syndrome. Its Gibbs probability ratio is therefore bounded by exp[-2beta J0(1-epsilon)|tau|]. Condition on the other CSS syndrome before applying the source witness enumeration; independent X/Z thermal distributions are unnecessary. The separate TRACE_WITNESS_TRANSFER_AUDIT.md binds the exact source statements and enlarged local-contact good set. This is the required local-ratio statement, not an O(epsilon*n) global energy approximation.

The result is p_bad<=poly(n) exp[-c n^eta] for fixed sufficient parameters, with the inherited source exponent and actual enormous construction constants. A fixed-size footprint enlargement changes only the polynomial prefactor and fixed constants.

## Dynamical consumer and endpoints
In decoded coordinates H_anc(S)=I_L tensor H_Ga. The ideal initial encoding is xi_LR tensor tau_Ga, the true Gibbs gauge/clock state, transformed back by U; terminal decoding undoes U and uses the original decoder. This explicitly requires ideal endpoint operations and access to clocks. Efficient or noisy physical loading/readout is not supplied by this theorem.

Assume a Gibbs-stationary Davies semigroup from bounded-local native contacts with uniformly bounded spectral rates, independent channels or bounded local correlation blocks, and total strength Gamma=O(n). Charge a bounded Lamb shift separately, or omit it by the model convention. Full degenerate Bohr-frequency blocks must be retained. No arbitrary rank-one splitting that resolves the logical qubit is permitted.

The established Chesi–Loss–Bravyi–Terhal thermal criterion applies: spectral projection preserves the protected data algebra because the full Hamiltonian is exactly syndrome-only. Sum-frequency pinching avoids counting exponentially many frequencies. The reference-safe bound from dynamics_audit/CONDITIONAL_DAVIES_CONSUMER.md is

 error(T)<=min(2,12 Gamma T p_bad).

Thus a stretched-exponential retention time follows in this precise semigroup model. This is not a uniform microscopic finite-coupling derivation of Davies dynamics over those times, nor the earlier exact autonomous spin-bath theorem. Exact algebra, not continuity in a generic perturbation, is crucial.

## Strongest established comparisons
Hopping/clock gadgets are established: Koenig, arXiv:0901.1333, gives ordered-product low-energy gadget machinery. Ocko–Yoshida, arXiv:1107.2697, supplies stronger nonperturbative two-body constructions for toric/quantum-double settings. The latter's shielding factorizes ground-compatible sectors; real equality defects restore interactions. A simple CSS extension needs at most two incident gadgeted X checks per data site for two-body shielding. The actual n=1336 fixture has incidence four in BOTH orientations, so that direct substitution does not close this family's gate. This is not a no-go for all OY extensions.

The new work claimed here is the explicit full-spectrum signed-clock thermal free-energy control and its binding to this actual family's witness and protected bath consumer. Neither the basic clock gadget, the general cluster theorem, nor the thermal-memory criterion is claimed as new. Historical novelty beyond this comparison has not been established.

## What remains decisive
The construction removes the many-body-interaction requirement within an exact model. It does not yet earn robustness to generic native interaction imperfections, a realistic microscopic bath over exponential times, cheap physical preparation/readout, or practical constants. These are the next implementation gates, not details to hide behind further model coverage. The scientific north star remains a broadly enabling reliable quantum capability; this package is an intermediate obstacle-removing construction, not a claim that civilisation-changing hardware is solved.
