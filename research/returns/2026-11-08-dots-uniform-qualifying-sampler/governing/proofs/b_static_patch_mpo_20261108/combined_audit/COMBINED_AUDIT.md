# Independent combined audit: uniform polynomial work in the qualifying regime

> Release-copy note: this historical proof/review snapshot has presentation-only edits recorded in SOURCE_PROVENANCE.json. Mathematical content is unchanged. Current status and superseded steps are identified in START_HERE.md and DEPENDENCY_MAP.md at the package root.

8 November 2026. Independent combined review. This is a mathematical and resource audit, not an implementation benchmark or scientific-priority determination.

## Verdict and exact scope

I find no remaining mathematical or finite-bit blocker in the stated combination, after the input and failure-accounting clarifications recorded below. The construction supports a finite-bit randomized full-output sampler with work

    poly(B_input) (n/epsilon)^(C_rho0)

uniformly over the **qualifying accumulated-noise regime**, at a fixed rational upper bound rho0 on grouped coupling strength divided by replacement rate. This is not a theorem for all physical times. It is not a uniform bound when rho0 grows with the input, nor a practical algorithmic performance claim.

The input must be a static rational Hermitian Hamiltonian with at most one GROUPED onsite term per qubit and one GROUPED term per nearest-neighbor square-lattice edge. Repeated contributions on a support must first be added. The norm bound h applies to that sum. Inputs are rational product densities; the requested output is the full computational-basis joint law. Every qubit has the same positive rational replacement rate gamma. Time and 0<epsilon<=1/2 are rational. No correlated inputs, time-dependent fields, nonunital baths, arbitrary-degree graph, or higher-arity extension is established here.

The new patch proof is used together with the repaired two-body activity construction, not the rejected literal multi-site word formula. The phase/cut-count algebra is an explicitly imported primary theorem. I checked its relevant coefficient formula and the new specialization, and used the separate exact-gauge audit as an additional independent check. I have not re-proved the entire primary paper's phase-filter theorem. That is an ordinary cited mathematical dependency, not an unpaid oracle.

The reviewed theorem and proof hashes, plus all inspected analytic dependencies, are bound by `combined_reviewed_sources.sha256`. Historical files retain their earlier conditional/open status; this audit concerns the combination specified in THEOREM_AND_COST.md, not retroactive relabeling of the older results.

## 1. Physical input, geometry and threshold

The sufficient original b=8 contract is correctly instantiated as

    r8(tau)=307584+ceil(60 rho0 tau),
    tau >= 76932+2ceil(log2 r8(tau)),  tau=gamma T.

The constants follow from c=200(8+4)=2400, 128(c+3)=307584, and 4+32(c+4)=76932. A fixed sufficiently large threshold exists at each fixed rho0 because the right side grows logarithmically while tau grows linearly. A certified continuous upper logarithm, as in the older base-selection proof, gives a terminating rational doubling procedure that ensures the inequality for all larger actions. Testing the actual supplied time does not authorize increasing that time or modifying the experiment.

The grouped-support condition is essential: a long list of norm-one contributions on one edge could otherwise violate both the claimed physical strength and the coefficient-incidence bound. This loophole was corrected during this audit. Expanding the grouped qubit terms into Paulis gives fixed incidence at most63 and coefficient magnitude at most h. Thus the Pauli contraction constants depend only on the fixed ratio promise.

Disconnected original site components must be handled independently (with divided TV budget), or retained as a sparse geometry. Padding the global bounding rectangle is not polynomial in the site count if disconnected sites have enormous binary-encoded coordinate gaps. This was also corrected. A connected activity patch does have controlled span; translating it costs the original coordinate-bit length and does not create a new large numerical parameter. h=0 has an exact independent-noise branch, avoiding a division by a zero coherent scale.

The tilted-layer construction has the needed properties: nearest-neighbor edges change floor(x+alpha y) by at most one; connected patches have no intervening empty layer. The collision estimate yields a paid rational slope with maximum layer occupancy O(N^(3/4)). The O(N^3) search and the local tensor dimensions 16^w are charged. Empty padding never stands in for an uncharged physical interaction.

## 2. The spatial activity and normalization dependency survives

The controlling word identity is FIRST_DISCOVERY_PROOF.md. A non-null two-body commutator word discovers at most one vertex per factor. Before each retained path's target arrival, the allowed interval excludes ALL future retained path vertices and the WHOLE multi-site target. This rules out the earlier alternative-arrival defect. Every geometrically non-null word has one discovery skeleton; a non-skeleton interval can contain return trips after arrival, so roundtrip histories are not discarded.

Onsite replacement insertions preserve support and introduce no switch label. Erasing them for the discovery classification and restoring them in their unique intervals retains full noise in every allowed-subset propagator. No dissipator is commuted past an interaction. The growing Schatten exponent and the central-label norm factors telescope along physical time. Shared boundary labels do not become artificial high-degree physical vertices.

The sparse-mark bound uses a separated positive fraction of far interface strips and pays all label, subset and local-normalization factors. The dense-mark bound invokes the finite-patch erasure estimate with the actual larger site-per-mark bound. These two cases give |w(C)|<=exp(-b|V(C)|) under the specified scalar contract. They do not rely on a strict-support or exact-light-cone claim.

Boolean edge-subset inversion gives an exact compatible-polymer identity because SWITCHED generators factor over disconnected edge components from the original product boundaries. It does not assert that independent spatial truncations of the full evolution factorize. Isolated block normalizers are at least1/2. Consequently evaluation divides by local products, never by the exponentially rare global prefix probability.

The same argument holds for rational positive site-product effects of trace2: each block effect has normalized trace one and norm at most2^a, so its centered factor has normalized trace norm at most2 and Schatten-(1+1/a) norm at most3. Tetrahedral membership effects satisfy these conditions. This checks both warm boundaries, including the adjoint Hamiltonian-sign reversal.

The connected-polymer count 64^v and the doubled-envelope KP test have slack. For tail exponent kappa=b-7, the root bound is at most 2 sum_(v>=2)(64e^-6)^v<1. Pinned log derivatives are bounded by e^v. These control input ACTIVITY errors at logarithmic precision O(L+bv), rather than the unnecessarily stronger historical termwise O(m^2) physical-oracle tolerance. Classical connected-graph integers may still need O(m^2) arithmetic bits, which are separately paid. The later clipped-activity improvement may be used but is not necessary to this one-level closure.

For each retained cluster total size m=O(1+L/(b-7)), connected unions, edge polymers and bounded-total-size multisets can be enumerated in n exp(O(m)). The incompatibility connected coefficient uses a subset recurrence, not an enumeration of all graphs on m objects. All signed sums are numerical algebra, not positive trajectory sampling. The zero-free interpolation fixes a real logarithm; stable logistic normalization supplies positive conditional probabilities.

## 3. Why retiling the child does not hide a correlated restart

For a parent activity patch, the original input R and effect A remain physical-site products. The warm-boundary constructor evolves each for action sigma. Querying either warm boundary against a rational tetrahedral product probe is exactly ANOTHER product-input/product-effect scalar experiment at sigma. For the adjoint boundary, the Hamiltonian sign is reversed and the two product boundaries are exchanged. No already-evolved correlated state is replaced by a product state.

The child's generator contains exactly the parent's retained local interactions, with deleted interfaces still deleted. It can be tiled afresh. A connected parent patch may be padded with decoupled maximally mixed input/effect-I sites; these multiply the scalar by one and the normalized boundary operators by identities. They do not alter Schatten or Pauli norms. The bounding rectangle has at most polynomially many sites in that connected patch's size, so its only global cost here is O(log N_parent) in the child's logarithmic budget. The evaluator builds only the child's own local activity patches, not a dense state of that entire rectangle.

This is the pivotal distinction from the previously rejected final-slab product restart and inherited-entangled-probe shortcuts. The construction retains compact product boundaries at the recursive interface.

## 4. Explicit uniform resource substitution

Choose log-marginal precision and conditional failure budgets of order epsilon/poly(n). Let L=O(log(n/epsilon)), including all union-bound and query-count factors. The global/scalar mixing shortcuts imply tau=O(L) whenever nontrivial evolution work remains. They test rational action against certified logarithmic bounds, so an exponentially large encoded T does not force a loop of numerical length T.

The adaptive parent activity construction has

    N_parent=O_rho(tau^2+tau L)=O_rho(L^2).

Its finite base interval is already polynomial with an enormous rho-dependent constant exponent. Outside that base, sigma=s_base+2ceil(log2(tau+2)) is strictly below tau/3 and is itself qualifying. The old norm, discovery and sparse-propagation contracts give at most exp(O_rho L) membership calls and log budget L'<=A_rho L. This nontrivial accuracy inflation is retained, not ignored.

Retiling each membership scalar at sigma gives

    N_child=O_rho(sigma^2+sigma L')=O_rho(L log(L+2)).

Every switched child scalar is evaluated to absolute error eta=exp(-O_rho L). Its positive product output effect has norm at most2^N_child, so channel accuracy eta*2^-N_child is sufficient. Hence E=log(1/channel error)=O_rho(N_child+L). There is no rare-prefix denominator and no replacement of absolute normalized-value accuracy by physical shot accuracy.

Use dense rational evolution if N_child=O_rho L. Its dimension costs exp(O_rho L), while degree and bits are polynomial in action, N_child, L and inherited input bits. In the remaining branch N_child>L' up to an allowed fixed constant, sigma=O_rho(log N_child) and E=O_rho N_child. These facts are needed to invoke the new static-patch asymptotic regime; they are not true for every arbitrary small patch without the dense branch.

For the MPO branch, the displayed exponent is bounded by a fixed polylogarithmic factor times N_child^(7/8). Therefore it is at most O_rho(L): for every fixed k, L^(7/8)(log(L+2))^k/L is bounded on L>=1. This is a uniform bound, though its finite constant can be huge. The phase count, growing local dimension, M^q coefficient enumeration, raw-update ranks, exact rational gauges and true-tensor minor bit resets are all included in that exponent. Input denominator bit lengths multiply as polynomial bit costs, not as numerical inverse-gamma action.

The child activity enumeration is itself exp(O_rho L). Multiplying it by the direct patch cost and then by the outer membership count remains exp(O_rho L). No further time recursion or unpriced membership call is left. The fixed multiplier A_rho occurs once. This is the actual improvement over the prior exp[L exp(O_rho(log* tau))] bound.

## 5. Finite precision, random bits and output law

All Hamiltonian and state encodings are inherited rational data; the queried tetrahedral probes add only constant-bit local entries. In the physical Pauli basis the generator entries are rational real numbers. Dividing by gamma charges its encoded bits while bounding the normalized numerical local strength by a rho-dependent constant.

The direct patch computation is a deterministic rational approximation. It does not require stable floating SVD or a free Schmidt-rank oracle. Exact rank sweeps use materialized finite MPO matrices; the gauge-reset proof charges possible small pivot minors by their numerator/denominator bit lengths. The source phase decomposition is only a rank proof and need not be numerically evaluated.

The outer Fourier discovery remains randomized, but has fixed sample/query/node caps, bounded membership values, coefficient clipping and common-dyadic rounding. Failed estimates cannot force an unbounded sparse norm or number of propagation steps. Both discovery error and later propagation error are paid in the two-sided coefficient2 pairing, not converted one-sidedly into a rare-probability relative estimate. The sibling auditor separately rechecked the coefficient contractivity and finite sparse propagation algebra.

At each output bit, conditional on the actual previously sampled prefix AND internal history, fresh scalar estimators obey uniform error/failure guarantees. Averaging their next-bit kernels gives TV error at most the good-estimate contribution plus failure probability plus the bounded-coin rounding error. Sequential coupling sums those errors. One must not condition the full output distribution on a global success event; the theorem now explicitly uses the valid per-history argument. The final guarantee is unconditional TV distance, with bounded work on unsuccessful random branches as well.

## 6. Independent finite checks

`check_combined.py` and `combined_checks.json` provide independent diagnostics:

- Two noncommuting Y-containing three-qubit examples verify product-boundary adjoint reversal, exact block-Möbius reconstruction and identity padding to a four-qubit rectangle. Maximum discrepancy is4.45e-16.
- All218 connected subsets of a3-by3 square and6,009 rational candidate slopes satisfy the edge-layer-span and no-missing-layer invariants and the stated collision envelope.
- Five rational ratio choices, including zero and10^6, verify the exact b=8 constants and20 successive doubled qualifying actions.

These are small checks of interfaces and constants, not evidence for asymptotic speed, certified floating-point error bounds or an executed end-to-end sampler. The analytical arguments, not these tests, establish the claimed scaling.

## 7. Prior and remaining limits

Primary-source checks confirmed the relevant boundaries:

- Mackay et al., [Optimal low-rank compression of quantum dynamics](https://arxiv.org/html/2609.27497v1), Proposition49 and the Liouvillian construction, supply the coefficient cut-count/MPO algebra. Their construction is explicitly in an exact-arithmetic model; the rational interpolation/minor accounting is separately necessary here.
- Nelson et al., [A polynomial-time classical sampler for noisy quantum circuits from statistical mechanics](https://arxiv.org/html/2610.00548v2), already combine polymer normalization, hypercontractivity and Pauli/tensor-network techniques for the discrete-circuit sampling problem. The present architectural combination is not a new general principle. Their fixed-noise-per-layer statement alone is not a uniform continuum Trotter theorem.
- Angrisani et al., [Dissipation accelerates quantum and classical simulation of open-system dynamics](https://arxiv.org/html/2609.40174v2), supply continuous-time coefficient/weight regularity and sparse propagation. Their normalized-Hilbert–Schmidt and ensemble expectation results do not by themselves provide worst-case rare-prefix relative accuracy. That is what the product-boundary activity/discovery chain must additionally pay.

I found no contradiction with these prior statements, or with the earlier product-oracle, Bell-sampling and pathwise-shallow-probe counterexamples. The new constructor uses the explicit static rational generator, not one of those restricted oracles. This limited search is not a scientific novelty or priority clearance.

The qualifying threshold and exponent constants are enormous. All nontrivial times below the sufficient contract remain outside this theorem unless covered by a separate solved case or mixing shortcut. Fixed-time polynomiality in that early interval does not follow merely because its length is bounded. The full all-time B goal remains unresolved. Any package should say **uniform polynomial sampler in the qualifying late regime; early times remain open**, retain correction history and proof dependencies, and avoid practical or novelty claims. This result is materially stronger than the previous log-star upper bound, but does not justify a general-B completion claim.
