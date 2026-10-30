# Whole-scoped independent receipt: ideal atomic SSF with continuous local quantum noise
2026-10-29. Mathematical audit; no publication or physical-controller theorem.

Integrated source:
`producer-workspace/FULL_ANIMAL_KILLED_BASIN_CANDIDATE.md`
SHA256: b2981ef69f958aa461a3cb0d4753fa0fbc1e27bb9430c0bffd7f8687b09436ff.

This receipt combines an independent check of this source's actual mixed-graph Sections 0–3 with the separately accepted boundary/killed Sections 4–5 and support/decoder Section 7. It does not transfer a check-only graph receipt without verifying the change of definitions.

## Verdict
**No remaining mathematical composition defect was found for the stated IDEAL ATOMIC model under the precise hypotheses below.** The mixed dummy/check graph discharges the FGL container contract; the full-animal progress proof supplies the required clean drift; its potential and constants are exactly compatible with the reviewed edge barrier and killed-process construction. The resulting decoded logical channel bound covers sustained bounded local Hamiltonian and Lindblad DATA/common-bath terms with a fixed initially logical-independent bath, without Pauli twirling, positive jump-location assumptions, added dephasing, or added depolarization.

This does NOT establish the analogous result for the finite-duration transactional controller. Its actual completion process has no supplied instantaneous atomic drift. It also does not certify noisy operational extraction, arbitrary initially logical-correlated baths, or fixed-dimensional geometric constant-rate hardware.

## 1. Exact code and atomic-operation assumptions
Use a fixed-degree quantum expander-code family satisfying FGL's expansion hypotheses, in particular delta<1/16 and 0<beta<beta_1=1-16delta. The candidate family must contain FGL's permitted flips. The small-error confinement constant and cutoff are those of the actual family, not inferred from bounded degree alone. FGL Proposition 14 and Lemmas 15/17 provide the imported unweighted facts.

Every active hub performs an accepted current-syndrome flip whenever one exists; its full read footprint contains the support of every consulted/changed check. All footprints and candidate counts are uniformly bounded. Hub rates have a positive uniform LOWER bound for drift and a finite uniform UPPER bound for the total local norm budget in the Duhamel comparison. The fixed-rate lambda model explicitly stated in the source meets both. Arbitrarily large rates satisfying only a lower bound are not covered by the final O(N) budget without an extra assumption.

Use sectorwise minimum-Hamming-weight syndrome representatives. They are stabilizer-reduced; their subsets are reduced. A global minimum full-Pauli-support representative need not meet this requirement and is not substituted.

## 2. The ACTUAL mixed graph meets the container contract
For each DATA site x, the source's J_x contains its unique dummy vertex and all checks incident to x or changed by a hub whose FULL read footprint contains x. Every J_x has bounded cardinality D0 and bounded incidence.

If J_x,J_y share a check q, choose a DATA site v in q's support. If q entered J_x through a hub, both x and v lie in that hub's full read footprint; if q is directly incident to x the path is even shorter. The same applies to y. Hence dist_G0(x,y)<=2. G=G0^2 therefore contains an edge whenever two J sets intersect. G0 must already include full read/check footprints and the full declared local operator patches used later, with bounded degree.

For each G-component C of a representative E:
- Dummy vertices of C are connected by G edges inside the mixed graph H.
- Every check in J(C) attaches to one of these dummies, making J(C) connected.
- Distinct J(C) are disjoint, since an overlapping check would join error vertices in G.
- An occupied check in J(C) has an incident erroneous site y. That check belongs to J_y, so intersection forces y into C. The same is true of every incident erroneous site. Thus J(C) contains EXACTLY sigma(C) among occupied checks, not merely a subset. Component syndromes do not cancel.
- |J(C)|<=D0|C|. Confinement for |C|<ell gives |sigma(C)|>=h|C| and therefore b0=D0/h.

The dummies are always empty and are not physical systems. They increase animal size and the finite graph constants but do not affect a syndrome flip, its sign, or any Pauli orbit. They resolve connectivity without creating a new physical assumption.

## 3. FGL mass gives actual assigned hubs, not restricted fictitious moves
An accepted hub contains an occupied changed check and hence an erroneous site in its read footprint. All errors in that footprint belong to the same G-component. Its chosen changed-check set is contained in that component's J(C), and the assignment is unique.

A candidate supplied by FGL for E restricted to C has an occupied changed check, so its footprint meets C. All global errors in that footprint are then already in C. Its entire syndrome evaluation agrees globally and locally; it is truly accepted globally. If candidate syndrome size is at most B and there are at most M candidate identities per hub, Proposition 14 gives

  g_C >= kappa |sigma(C)|,   kappa=c1/(B M).

A more wasteful packing-derived constant is also valid. The actual chosen accepted move may differ from the candidate counted by FGL, but remains in the same J(C). Let nu bound the number of hubs whose possible changed-check sets contain a fixed check. Bounded LDPC/read incidence supplies this constant. All abstract weighted-progress inputs are thereby discharged.

## 4. Weighted drift in THIS graph
Section 1's per-move ratio is identical to the accepted check-only proof: dummy vertices are unchanged, so they cancel in the comparison. Increasing A intersects the changed-check clique D, making A union D connected. The exact ratio is bounded below by exp(a m_-)theta^{m_+}; at most 2^k sources share a completion. The displayed sufficient condition leaves at least half the negative loss of every D-containing animal.

The source's Section 2 first bounds the OCCUPIED-weight sum rather than |A|f_A. This variant is valid:
- Covered animals assign k_A f_A to intersecting hubs with threshold kappa k_A/4 and incur the stated 2^k0 theta^(-u k0) factor.
- An uncovered animal has more than half its occupied mass in poor components.
- A poor C has at least kappa|sigma_C|/2 active supports wholly outside A. Incidence gives at least rho|J(C)| new occupied checks, rho=kappa h/(2nu D0).
- Completing just C gains theta^(-(rho-u)|J(C)|), which pays the at-most 2^|J(C)| preimages.
- Summing |sigma_C|<=g_C/kappa over completed containers counts distinct contained actual hubs, not an uncontrolled number of components.

The k_A=0 case causes no exception: it is covered with zero occupied-weight charge. Finally sparse animals have f_A<=theta^(u|A|/2); their |A|-weighted total is O(N) by bounded-degree animal counting. Non-sparse animals satisfy |A|<=2k_A/u. This proves precisely (2.8), with W>=V.

The FULL finite-volume animal sum is essential. It is finite for each finite N, and no cutoff-truncated potential is used in the completion maps. Vacuum and sparse bounds alone use convergent infinite geometric majorants.

## 5. Continuous DATA/bath noise bound
A declared DATA patch Z changes only a bounded set T_Z of syndrome checks under its local Pauli algebra. Its syndrome orbits are invariant under every joint DATA-on-Z/bath operator. The orbitwise minimum of V therefore commutes with such operators. Subtracting that minimum gives the stated Loewner commutator/dissipator inequalities with the joint operator norms.

For every syndrome in an orbit,

  Omega_Z(V) <= theta^(-k_noise) sum_{A:A intersects T_Z} f_A.

This follows by bounding the range of a sum by the sum of ranges and noting that one f_A has orbit ratio at most theta^(-k_noise). Terms with A disjoint from T_Z have zero range. Bounded incidence of the DECLARED local patches then gives

  sum_Z Omega_Z(V)<=C_osc W.

Dummy vertices remain fixed, and |A intersect checks|<=|A| makes their presence harmless. No dependence on the number of bath degrees of freedom enters. A retained common bath may correlate distinct patches and need not be reset.

The joint data-acting norm budget must be the stated one, uniform in time, with bounded patch incidence/range. A bound on reduced-DATA dynamics, a per-term bound with unboundedly many incident terms, or unrestricted all-pairs bounded-cardinality supports is not sufficient. Bath-only evolution is allowed when the joint propagator is well-defined; it commutes with V,P and contributes no boundary term.

Combining the global noise Loewner bound with the diagonal clean drift yields the restricted operator inequality P L*V P <=-(gamma-epsilon C_osc)PWP+bNP. This is the exact inequality required by the reviewed compression proof, including off-diagonal quantum noise; it is not a classical trajectory approximation.

## 6. Compatible explicit parameter order
Take common worst-case constants for both CSS sectors. One sufficient order is:

1. Choose the code beta in (0,beta_1), the full declared support patches, G0,G,H, and all fixed incidence/constants.
2. Set rho=kappa h/(2nu D0), and choose

   0<u<min{1, rho/2, 2beta/(1+beta), h/(4D0)}.

   Put c=1-u. This enforces both the per-move beta condition and the source-edge barrier condition.
3. Choose theta>0 sufficiently small for A0 theta^(u/2)<1, 2theta^(rho-u)<=1, and every bounded-size per-move charging inequality. These are finitely many compatible conditions. Put Ltheta=log(1/theta).
4. Compute C_cov, gamma, b and C_osc; choose epsilon C_osc<gamma/2.
5. Choose ell=floor(c_cut sqrt(N)) with c_cut strictly below the family's confinement and distance coefficients. For sufficiently large N, ell>=8s, ell<distance, and all |C|<ell satisfy FGL confinement/progress.
6. Choose N0 large enough that the combined encoded vacuum value C_vac N is smaller than M=exp(Ltheta h ell/8)/2. Exponential-in-sqrt(N) growth guarantees such an N0.

All choices through step 4 are independent of N. Constants may be extremely unfavorable. A finite-size arbitrary HGP fixture is not certified by this asymptotic existence argument.

## 7. Exact handoff to the separately reviewed barrier/killed proof
The mixed H and J_x used here are the SAME objects in the reviewed Sections 4–5. For every connected component K of E union Z union F, J(K) is connected even when K includes non-error sites, because all its dummy vertices and G edges are included. |J(K)|<=D0|K|. Thus the reviewed high-source-V estimate uses exactly this full-animal term, with no graph conversion or potential mismatch.

The local patch bound s and graph cliques must include full nominal Kraus supports (read projectors plus corrections), noise h/K supports and K†K supports. K†K stays on the same DATA patch. This is stated in Section 7 and is needed for both canonical logical identity and cross-loss exits. k_max likewise includes nominal and noisy patches and may safely count the union of affected checks in both sectors.

The independent killed-basin audit accepts: componentwise canonical replacement, high SOURCE barrier, CP/TNI compression with complete loss, adjoint deletion of positive exit gains, common boundary-source projector including K†K, completely bounded Duhamel comparison, and scalar killed logical map with the fixed initial bath. Its initialization refresh is exactly the b298 source reviewed here. This receipt discharges that audit's previously external weighted/container premises rather than assuming them.

For two CSS sectors choose V=V_X+V_Z and W=W_X+W_Z, require both canonical representatives component-safe, and use a common low-V threshold. Clean opposite-sector feedback commutes with the other syndrome. Noise bounds add with common worst-case constants. Every retained local operator block has identity canonical logical action in both sectors, up to ancillary syndrome phases.

The O(N) total norm budget Gamma_N follows from bounded patch/Kraus incidence and bounded clean rates, plus the noise budget; bath-only terms are excluded because their compression difference vanishes. The reviewed comparison then gives

  ||Dec E_t Enc-id_L||_diamond
  <=min{2, C N^(3/2)t exp[-Ltheta h ell/16]},  N>=N0,

for a fixed initially logical-independent bath and arbitrary logical/reference input.

## 8. Decoder and scope
The fixed canonical sector decoder is a valid mathematical terminal channel. Section 7 also permits replacing it by ideal complete-syndrome measurement followed by deterministic SSF scans: accepted moves do not increase full V, the local edge barrier preserves component safety below M, and integer syndrome weight decreases. A no-change scan with nonzero syndrome contradicts the verified active-hub bound. Each step has identity canonical logical action, so the decoder is correct on the entire killed subspace, including coherent syndrome/bath states. It needs O(N^2) naive classical work and ideal terminal operations.

Neither decoder claim grants reliable physical processing while noise continues, arbitrary quantum retrieval hardware, or a finite-duration-controller theorem. The latter needs a genuinely new transfer of the atomic weighted drift to the retained coherent transactional scheduler. The earlier Poisson-kick compiler theorem does not supply that transfer for general continuous noise.

## Receipt dependencies and actions
Read the integrated b298 source, the independent BOUNDARY_KILLED_REVIEW.md and INITIALIZATION_REFRESH_RECEIPT.md, and used the direct FGL checks and weighted-progress audit from this review sequence. No accepted source was edited. No denied access, external mutation, publication or novelty claim occurred.
