# Actual recursive quantum code: physical local-channel phase construction

1 November 2026. Construction in progress, conditional only on explicitly inherited audited code/Gram/gap inputs and the physical geometry conditions below. This is not an autonomous/noisy hardware theorem or a historical-priority claim.

## Main proposed consequence

For the actual recursive RX/RZ family with its fixed decoder, sufficiently low fixed temperature and sufficiently small generic bounded-body local Hermitian perturbations form an OPEN sufficient domain whose Gibbs states are two-way connected to the maximally mixed ground-code state by ideal channels of physical polylogarithmic causal radius, to every prescribed inverse-polynomial whole-state trace error. Product onsite bath spins may be included when they occupy bounded-density physical 3D sites. This strengthens polynomial-time thermal preparation: the channels have a genuine physical light-cone bound. The original polynomial encoder does not itself establish that bound.

The proposed proof uses the whole architecture already present for classical gauge states in Xun–Cao–Watanabe, but binds its difficult non-product conditional ground spaces to the actual quantum code's earned parent gap. It does NOT infer local channels from shortcut-graph mixing, nor infer the full Ma–Khemani–Sang stable-clustering hypothesis from a scalar partition function.

## Admitted inputs and domain

Use the exact actual trace-polymer bijection, uniform low-activity/contraction margin, decoder contraction every two levels, scaled geometric carrier bounds, weak scalar quantum log-potential with polynomial envelopes, uniform relative rank-two Gram estimate eta_n=C n q^(c d_n), and uniform signed filtered-parent gap from the reviewed preparer. Hold construction constants fixed. Let N=n+N_B, with N polynomial in n, all onsite Hilbert dimensions bounded, physical local interactions bounded in range/body/incidence, and physical balls contain O(r^3) sites. The last condition must be stated for the bath, not inferred from N_B polynomial.

Take beta in a compact interval of sufficiently large positive values and a strict smallness inequality on V in the local interaction norm. Strict activity, potential, and gap margins survive a sufficiently small OPEN ball of arbitrary local Hermitian perturbations, including changes in reference check coefficients. Known couplings and ideal local controls/reset are constructive resources. An inaccessible reservoir is excluded.

## 1. Actual trace geometry rather than shortcut geometry

An individually valid trace gamma of mass m has at most m nonzero top syndrome inputs. By isolated replay, its coarse syndrome obeys the same every-two-level factor-1/2 contraction as the actual decoder. It cannot have a nonzero stage above 2 ceil(log_2 m)+O(1) levels; zero-preserving local gates cannot activate later without such a stage. Terminal fixed-size blocks are charged as constants.

Each one-step gate/wire stencil occupies a bounded number of adjacent geometric carriers at its own scale. Lifting a depth-h carrier moves points by O(lambda^h), using only the established forward displacement bound. A connected m-object trace therefore has physical top-support diameter at most C m lambda^(2 ceil(log_2 m)+O(1)) <= C'(1+m)^p for a fixed p. The same carrier proof contains its emitted corrections and their downward reconstruction; bounded branching bounds reconstruction cardinality polynomially in m. Root every valid polymer at its first top syndrome input. Rooted candidate count remains K^m because this top input is an actual trace object.

For incompatible truncated traces gamma,eta, their complete stencils overlap at a common host object. Its lifted physical carrier is within both polynomial envelopes. Consequently their physical roots are within O(M^p) when both masses are at most M. This is the compatibility-locality bridge missing from a bare physical-correction cardinality bound. All tests, boundary-zero conditions and matched corrections can be computed from these envelopes. The source's precise finite stencil/forward-geometry assumptions are retained; no inverse-Lipschitz embedding is needed.

## 2. Parallel local classical sampling

Choose trace and potential cutoffs M=C log(N/epsilon), below the logical cutoff. Potential dependency envelopes have radius polynomial in M. Let r_u=C M^b dominate trace, incompatibility, full decoder backward-cone and potential update radii. One may take b at least the maximum of their fixed polynomial exponents, with trace exponent 1+2 log_2(lambda); lambda is the geometric iteration scale, not the subdivision ell.

Root each birth at a top input. The summed dominating proposal rate at a root is bounded by sum_m K^m a_m=O(1); each root also has a unit death clock for its unique present rooted polymer. Add unit bath heat-bath clocks. Independent marked Poisson records are product work resources. A proposal reads only the radius-r_u neighborhood. Run for T=C log(N/epsilon); the inherited weighted path coupling bounds mixing error by epsilon, and trace/potential omission plus the Gram remainder are separately charged.

A chronological dependency path of k events has probability bounded, after a union bound over starting roots, by C N (C r_u^3 T)^k/k!. Thus k_*=C[r_u^3 T+log(N/epsilon)] suffices to cap all dependencies except with probability O(epsilon). Local Poisson record lengths and precision can likewise be capped at polylogarithmic values. Process ready events in k_* rounds with a fixed physical coloring of overlapping radius-r_u neighborhoods. There are O(r_u^3) colors. Each round is a local channel on finite classical records, not an epsilon-sized time discretization. This gives the conservative range bound

 R_class <= C r_u^4 k_* = O(M^(7b+1))

in three dimensions. A local stop/fallback after the deterministic caps defines a genuine bounded-range channel on every input; its exceptional probability is charged. This is an explicit physical causal-radius argument, not a claim that continuous-time mixing is itself a local circuit.

Apply each sampled polymer's matched Pauli correction, combining overlapping Pauli factors locally with the fixed CSS order. Routing correction control bits over their radius-poly(M) envelopes adds only polynomial-in-M range. Prepare sampled bath basis bits locally. Starting with P_0/2 yields the approximate block-diagonal ensemble sum_a p_a P_a/2.

## 3. Physically local quantum coherence recovery

Attach a classical sign register at each actual stabilizer check and bath projector. Define the local mismatch projector Qtilde_j using that register and its physical check. With s in [0,beta],

 Ltilde_j(s)=(I_C tensor exp(-sH/2)) Qtilde_j (I_C tensor exp(sH/2)),
 Ftilde(s)=sum_j Ltilde_j(s)^dagger Ltilde_j(s).

This is block diagonal in labels a, with block F_a(s). Root-connected expansions give physical exponentially decaying interactions, also for the s derivative, directly in control-plus-physical space. Do not sum norms over exponentially many labels.

Valid sectors have an earned uniform gap above their exact two-dimensional kernel. Invalid sign strings need not have a kernel or a gap. This does NOT obstruct the construction: define the filtered quasiadiabatic generator from Ftilde and its derivative on the full Hilbert space. Locality uses the physical interaction/Lieb–Robinson bound, not a global spectral gap. On each invariant valid block the filter has the correct inverse-frequency value across its uniform gap and transports its zero eigenspace. No statement about invalid blocks is used.

Use a filter with stretched-exponential time tails to obtain generator interaction tails bounded by C exp(-c sqrt(r)). Physical range cutoff r=C log^2(N/epsilon) gives global norm error O(epsilon). A coarse-block Lieb–Robinson circuit decomposition with overlap ell=C log(N r^3/epsilon) and O(r^3) slices gives depth O(r^3), gate diameter O(r ell), and causal radius O(r^4 ell)=O(log^9(N/epsilon)). Shortcut edges used to prove the gap are never gates or light-cone edges.

For maximally mixed logical input the endpoint transported state in each label is exactly the normalized projector onto exp(-beta H/2) ran B_a, regardless of degenerate holonomy. Near-scalar Gram matrices show that averaging these projectors with p_a approximates rho_H to O(eta_n). Discard the label registers. For arbitrary logical inputs use the beta-only path and the existing near-scalar Gram parallel-transport estimate, rather than assuming holonomy absent for arbitrary parameter paths.

## 4. Reverse channel

Measure/dephase the commuting local checks and the onsite bath basis, retaining local outcomes. Bounded check incidence gives fixed-depth local measurement layers. Its conditional block is B_a G_a(beta) B_a^dagger / Tr G_a(beta), which is within O(eta_n) of P_a/2 uniformly in a. Run the capped local trace recognizer/decoder: on configurations all of whose complete trace components have mass <=M, it reconstructs and removes exactly the matched correction. Compute actual gate values from an UNCHANGED copy of the original syndrome through t_M=2 ceil(log_2 M)+C levels plus one extra layer. Include each queried gate's entire backward dependency cone, including inactive inputs; fixed branching and logarithmic depth keep both its size and physical radius polynomial in M. Explore the marked full-stencil graph up to M+1 objects. Accept only exhausted components with every neighboring active-gate incidence checked and ZERO outgoing frontier. Thus no fragment of a larger trace is mistaken for a complete small component; every true mass-at-most-M component passes by isolated replay. No global success flag is needed. For other configurations use a fixed local fallback. Their total probability is O(epsilon+eta_n) by the positive scalar-law comparison and low-activity tail. Reset/discard bath spins or prepare the chosen product reference. The output is within O(epsilon+eta_n) of P_0/2.

This reverse map does not attempt to infer a hidden filtered-ensemble label from a nonorthogonal quantum state. It directly measures the actual Gibbs state and uses its independently established Gram blocks.

## 5. Costs and what is not established

Both directions have R <= C log^q(N/epsilon), with q=max(7b+1,9) sufficient under the conservative schedules. Work records and within-block Hilbert spaces are finite and of polylogarithmic physical extent. Dense synthesis of arbitrary local block maps yields at best an explicit exp(log^{O(1)}(N/epsilon)) elementary-gate upper bound here. The pre-existing polynomial encoder and this polylog-range channel theorem are different resource statements; a simultaneous polynomial elementary-gate/polylog-depth compiler is NOT established. Nearest-neighbor hardware runtime depends on the charged block synthesis, and is not asserted polylogarithmic.

The intrinsic error floor is retained: O(epsilon+poly(N)eta_n), with any additional logical-overwrite comparison terms only needed for arbitrary logical-state conclusions. For every fixed inverse-polynomial accuracy, M< c d_n and the intrinsic remainder is negligible asymptotically. This is adequate for asymptotic local-channel phase equivalence, not arbitrary precision at fixed n.

No native final-gate-noise tolerance, no passive preparation, no inaccessible bath, no practical constants, no all-annulus stable clustering, no thermodynamic phase boundary, and no high-temperature separation invariant is inferred here. These are different gates.

## 6. Stable physical local-versus-exterior correlations: a direct consequence

Let omega_0=P_0/2. If regions X,Y have no check touching both and |X|<d_n, then (omega_0)_XY=(omega_0)_X tensor (omega_0)_Y. Proof: a Pauli P_X P_Y in the stabilizer group forces each factor to commute with every generator; distance makes P_X a stabilizer, and hence P_Y is too. Conversely products of separate stabilizers are stabilizers. The Pauli expansion of the normalized code projector therefore factorizes. This argument handles arbitrary operators on the whole exterior, not only individual Pauli observables.

Dilate the forward channel with its product local work environments. If A and C are separated by r>2R plus the check range, their radius-R backward cones are disjoint. If |A_R|<d_n, the source on the two cones factorizes by the preceding lemma. The channel output consequently has zero covariance for arbitrary norm-one O_A,O_C. If its trace-norm distance from rho_H is delta, covariance of rho_H is at most 3 delta.

With R<=C log^q(N/epsilon), bounded physical density, and A fixed-size/polylog-radius with radius o(d_n^(1/3)), choose R=c min(r,d_n^(1/3)) and invert the range-error relation. This proves

 Cov_rhoH(A,C) <= C N exp[-c min(r,d_n^(1/3))^(1/q)] + C eta_n.

Keep the cutoff condition log(N/epsilon)<c d_n; it holds for this conservative choice at large n. The statement is uniform throughout a strict interior parameter domain and therefore stable under generic sufficiently small local Hermitian perturbations. If d_n>=c L^delta with physical linear size L and r<=O(L), it yields a global-distance stretched exponential with exponent min(1,delta/3)/q, plus the explicit finite-size remainder. No classical shortcut metric appears.

This is small-inner-region versus arbitrary-exterior stable clustering. It is not a proof of MKS's complete all-annulus definition for inner regions larger than the code-correctability scale. The direct phase theorem does not need that stronger assertion. The polynomial prefactor may make the quantitative bound uninformative at modest distances; this is a limitation of the conservative construction, not a claim of a microscopic correlation length estimate.

## 7. Strongest predecessor comparison and consequential claim

Ma–Khemani–Sang, https://arxiv.org/html/2509.15204v3, gives a general stable-clustering-to-channel theorem and a locally reversible circuit criterion relevant to thermal quantum memory. Its premise must be verified in the physical metric for arbitrary exterior operators. The present construction bypasses that premise, then proves the restricted stable-correlation consequence above; it does not claim their full gate-by-gate local-reversibility property.

Xun–Cao–Watanabe, https://arxiv.org/html/2610.27939v1, already establishes the low-temperature diagonal-sampling/coherence-recovery local-channel architecture for classical gauge references. Its product-sector parent-gap argument cannot simply cover this quantum code. The added binding here is the actual trace geometry, entangled rank-two gapped parents, invalid-syndrome control treatment, and quantum code-sector reverse channel. Its generic within-block gate limitations are retained rather than relabeled as efficient shallow hardware.

Thus the proposed consequential claim is an OPEN ideal quantum thermal local-channel phase attached to this actual 3D quantum-memory code, with physical stable local correlations—not merely an equilibrium storage bound or polynomial global preparation algorithm. Nontriviality against the product-state phase should be supported by an independent local-channel invariant or logical-information obstruction before being advertised as a proved phase-separation theorem. Native noisy loading remains a separate engineering/mathematical challenge.

## Review status and memory geometry receipt

LOCAL_CHANNEL_AUDIT.md records a skeptical second self-check, not independent-author peer review. No fatal counterexample was found under inherited inputs. The actual source 2605.10943v1 Theorem 1.2 and Definition 3.1/Theorem 3.16 explicitly supply bounded memory-qubit density and geometric scaling assumptions; the added bath must separately obey bounded physical density. The decoder recognition correction from that audit is incorporated above.
