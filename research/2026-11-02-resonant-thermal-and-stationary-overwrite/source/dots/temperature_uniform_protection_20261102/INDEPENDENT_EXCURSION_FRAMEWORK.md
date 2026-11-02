# Temperature-uniform protection: endpoint-pinned excursion framework

2026-11-02. Independent constructor. **Status: mechanism and exact conditional consumer; not a proved generic perturbation theorem.**

## 1. Derivation from the target, before importing a preferred framework

We want a nonzero local perturbation window v/J <= epsilon, uniform over beta >= beta0, and actual full-Gibbs logical-crossing rarity. A bare local defect has virtual ground-state weight of order (v/J)^2. Therefore neither a beta-uniform comparison with original Gibbs syndrome weights nor a bound q=exp(-beta J_eff) for bare syndrome inclusions can be correct.

The correct primitive is a **time-slice contact cost**. Thermal defects wind around imaginary time and pay exp(-beta Delta_eff). Virtual defects are finite imaginary-time excursions; an excursion meeting the observation slice pays an endpoint cost, rather than a full beta energy penalty. A one-defect creation/annihilation example has

    v^2 integral_{u,w>=0} exp[-Delta(u+w)] du dw = (v/Delta)^2.

The corresponding unpinned vacuum loop has a free time-translation integral beta and bulk weight O(beta v^2/Delta). It must be canceled against the denominator before taking absolute values. The difference is physical, not a better numerical estimate for the existing full-time-column expansion.

Desired contact parameter:

    q_eff(beta,v) <= C [exp(-beta Delta_eff) + (v/Delta)^a],
    Delta_eff >= Delta-Cv > 0,

where a>0 may be conservative and incorporate bounded local support, graph colors and coherent-amplitude losses. No claim that a=2 for correlated multi-check events is warranted: one local event can flip k checks, so joint probabilities can scale as v^2 for k defects.

The existing charged-component decoder accepts any small enough q_eff; it does NOT need q_eff to tend to zero with temperature. If all-subsets inclusion is unavailable, use only its enumerated valid removable witness family.

## 2. Exact conditional full-Gibbs consumer

Let B_e be the original decoder's bad projector for one bounded-support physical Pauli fault e, and let the deterministic geometric theorem supply witnesses W with mass m >= m_*(d), at most A^(m+c) possibilities rooted at e. Let P_W be each witness event projector with B_e <= sum_W P_W. Suppose the exact full Gibbs state obeys

    Tr(P_W exp[-beta(H0+V)]) / Tr(exp[-beta(H0+V)])
        <= C0 [C1(exp(-beta Delta_eff)+(v/Delta)^a)]^m

uniformly in volume, beta>=beta0 and witness mass. Then

    Tr(rho_beta,V B_e) <= C2 (A q_eff)^{m_*(d)}

whenever A q_eff < 1, with the usual harmless rounding/root constants. The already-established decoder geometry supplies m_* = Omega(d^alpha), or its K=2 / K<2 improvements. Choose epsilon>0 and beta0 finite so that A C1[(epsilon)^a+exp(-beta0 Delta_eff)] < 1. This establishes the sought fixed nonzero low-temperature window **if** the contact estimate is proved. It is directly a full-Gibbs estimate, not a ground-gap implication.

This conditional consumer uses the bare decoder and explicitly admits virtual defects. Dressing is an optional improvement, not logically forced by the obstruction.

## 3. What an excursion construction must prove

1. Expand local perturbations in the joint commuting-check basis, retaining actual valid syndromes and logical matrix labels. Track imaginary-time intervals carrying defects; do not replace every visited check by a full-time occupied column.
2. Sum all zero-energy/repeated moves inside an excursion before estimating. A bounded-degree norm estimate can replace Delta by Delta-Cv only if the number of available moves is charged to occupied contour geometry; vacuum degeneracies cannot be charged indiscriminately.
3. Resum vacuum loops and interactions into a normalized linked-cluster expansion. Absolute numerator/absolute denominator comparison loses exp(beta volume v^2/Delta) and is not acceptable.
4. Establish an endpoint-pinned cluster bound. Components touching the observation slice have no unconstrained imaginary-time translation. A cluster touching multiple witness sites must pay enough vertices or occupation geometry to cover them, with bounded witness entropy.
5. Distinguish time-winding thermal components from nonwinding virtual components. Bound the former by exp(-beta Delta_eff) per appropriate charged resource and the latter by powers of v/Delta.
6. Show that local stabilizer phases and actual compiler auxiliaries admit the exact normalized representation. A scalar positive worldline measure is not available for arbitrary Hermitian perturbations; signs must be controlled by a convergent normalized cluster expansion, not silently removed.
7. Preserve actual clock excited states and bath degrees of freedom. A ground-subspace SW approximation or postselection does not establish the requested full-Gibbs estimate.

These are construction requirements, not premises already supplied by ground-gap stability.

## 4. A second beta-uniform obstruction: logical-sector splitting

An exceptional perturbative history producing a logical operator has coefficient delta_L ~ J(v/J)^{Omega(d)}. Treating all such histories as a small correction gives beta delta_L, which diverges at fixed finite volume as beta -> infinity. This is not a physical instability: it is the selection of the ground state of an exponentially small effective logical Hamiltonian. But it defeats any proof relying on 'exceptional logical matrix remainder < 1' uniformly over all beta.

A genuine uniform construction must resum the effective logical evolution exactly. One satisfactory interface would be positive operators Z_eff and Z_bad on the logical space such that

    Z_eff > 0,   0 <= Z_bad <= epsilon_L Z_eff,

with epsilon_L <= C exp[-c m_*(d)], and whose traces are the exact partition function and bad numerator. Equivalently, establish the endpoint-pinned bound uniformly in the normalized effective logical state, not merely in the maximally mixed logical state. Arbitrary noncommuting signed operator activities cannot be inserted into a scalar KP theorem to claim this order inequality.

Ground-state local indistinguishability makes the desired uniformity plausible but does not prove the full thermal statement. The logical effective dynamics and the defect gas need compatible factorization or a matrix-positive domination argument.

## 5. An exactly proved benchmark, narrower than an open perturbation ball

For any bounded-depth finite-range circuit U and a commuting reference H0 satisfying the existing Gibbs witness theorem, take H=U H0 U^dagger. The exact full Gibbs state is U rho0 U^dagger at every beta. Use dressed syndrome projectors U P_s U^dagger and dressed decoder. A local physical fault E becomes U^dagger E U, supported in a uniformly bounded enlarged region. Expand this finite-support operator in its finite Pauli basis; the union of the corresponding decoder bad events obeys the original Gibbs witness bound with only local constants changed. Thus the full-Gibbs rare-bad bound and the exact-H twirl consumer are uniform over beta>=beta0. Small-angle U gives a continuous fixed-amplitude family H-H0 of weak local noncommuting perturbations, and bare measurements may show virtual defects.

This benchmark proves that finite virtual clouds are compatible with actual thermal logical protection and gives a regression test for any proposed contour theorem. It is **not** a generic open ball of Hamiltonians: the perturbed terms remain jointly commuting after conjugation. It must not be presented as the missing generic phase theorem.

## 6. Primary literature check

- Borgs–Kotecky–Ueltschi, *Low temperature phase diagrams for quantum perturbations of classical spin systems*, https://web.ma.utexas.edu/mp_arc-bin/mpa?yn=95-233 . Their classical reference is diagonal in a tensor-product basis with finitely many ground states and a Peierls condition. The space-time contour mechanism supports a fixed-small-quantum-perturbation low-temperature regime, but this is not an automatic theorem for entangled CSS checks, hierarchical geometry, or clock auxiliaries. A nonlocal Clifford change of basis can destroy the local perturbation premise.
- Bravyi–Hastings–Michalakis, https://arxiv.org/abs/1001.0344 . This is zero-temperature stability, with isolated low spectral bands; it does not establish extensive-energy Gibbs contour rarity.
- Xun–Cao–Watanabe, https://arxiv.org/html/2610.27939v1 , Theorem 1/Eq. (16): their quantum sufficient condition is beta |g| exp(C beta J)<a. Their text explicitly says fixed nonzero g does not reach T=0. Thus this very relevant full-state classical-gauge result does not close our gate.
- Watanabe, https://arxiv.org/abs/2607.00134v3 : finite-field low-temperature 3D toric-code decoded-loop order is investigated numerically; the abstract describes the thermodynamic values as conjectured, not a generic fixed-window proof.
- Zhang–Gopalakrishnan, https://arxiv.org/abs/2511.01976 : stability against weak local decoherence concerns a local noise channel applied to a commuting-Pauli Gibbs state. This does not identify a generic perturbed-Hamiltonian Gibbs state with such a noisy state; that identification is precisely a possible missing bridge.

## 7. Honest conclusion

The useful new principle is **normalized endpoint-pinned quantum dilution**, with a nonzero virtual activity floor and exact treatment of logical-sector splitting. Existing full-beta-column smallness is the wrong expansion parameter for this target. The fixed-v generic theorem remains unproved until the endpoint-pinned full-trace estimate and logical matrix normalization are constructed for the actual Hamiltonian. The benchmark and conditional consumer are rigorous; the generic contour construction is a research gate, not an earned result.

## Addendum: root's stationary-state SWAP consumer independently verified

Root has removed the logical-maxmix/dynamical beta factor. For any stationary joint state rho, fixed decoded Pauli Q with [H,Q]P_good=0 and ||[H,Q]||<=2vn, p=Tr(P_bad rho), stationarity and Duhamel give

  ||[exp(-iHt),Q]rho^(1/2)||_2 <= 2vn t sqrt(p).

For ideal external-input/logical SWAP S=(I+sum_{j=1}^3 sigma_j tensor Q_j)/2 and arbitrary input/reference state xi_AR, sum the three terms and use the trace-distance/HS inequality to obtain reference-safe error <=6vn t sqrt(p). No beta or maximally mixed logical marginal is required. The logical resummation warning in Section 4 therefore concerns proving the static contact estimate, not an obstruction in the lifetime consumer.

The concrete native dynamic-flux bridge in DYNAMIC_FLUX_ROD_LEMMA.md now closes the scalar prescribed-flux step proposed above. It is stronger than the earlier candidate file and supersedes its unresolved scalar positivity concern; it does not close arbitrary matrix-unit pins or data-gas normalization.
