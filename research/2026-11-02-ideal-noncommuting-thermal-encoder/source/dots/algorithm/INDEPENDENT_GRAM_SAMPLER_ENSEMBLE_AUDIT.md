# Independent Gram–sampler–ensemble audit

2026-11-01. Audited `GRAM_SAMPLER_ENSEMBLE_BRIDGE.md` against the previously audited finite-β polymer and thermal-encoding interfaces and the supplied trace-gas sampler interfaces.

## Verdict

**PASS-CONDITIONAL (analytic/constructive join).** No fatal flaw found in the uniform operator Gram bound, connected-label-set resummation, restricted-trace evaluation, joint sampler coupling, or reference-safe ensemble comparison. This is NOT a completed filtered-code preparer: parent-gap, representable parent dynamics, logical transport/frame, and implementation accuracy remain separate gates. The existing filling, decoder-trace gas, and distance inputs must actually hold. The O(η_n) accuracy floor is real and correctly retained.

## 1. Uniform operator Gram

The previous scalar trace argument lifts to the operator compression W_a†(·)W_a. Different event components cannot cancel a nonzero syndrome because the generous event graph places an edge whenever a reference generator meets both components. Components below the logical cutoff therefore compress to scalar multiples of I_L. Bath-only components are scalar at all sizes. The exceptional memory-touching components remain 2×2 matrices; the norm of their product is bounded by the product of norms, without assuming trace or matrix factorization. Excluded-region scalar partition ratios then give an operator-norm remainder O(nq^L0), uniformly in the full reference label and in s∈[0,β].

Since the scalar partition is positive and G_a(s) is Hermitian positive, recentering at g_a=TrG_a/2 is legitimate. If the uncentered error is at most u<1, the centered remainder is at most 2u/(1−u). Thus the claimed η_n bound follows after a constant change. It establishes neither a parent spectral gap nor trivial non-Abelian transport.

## 2. Label-set Möbius resummation

For |U|<L0, every component in the Hamiltonian restricted to perturbation labels B⊆U is small. Consequently F_B is exactly the scalar restricted-gas partition, not just an approximation. Absolute convergence permits grouping the log expansion by the union of labels. Möbius inversion extracts precisely the terms with union U, including arbitrarily repeated polymers whose union is U. Disconnected U gives zero by exact factorization of the restricted gas.

Keeping |U|≤L therefore includes all terms with small union even if their total multiplicity exceeds L. Every omitted term has union>L and hence total multiplicity>L, so the weighted KP tail supplies the claimed C N q_1^L bound. Enumeration of connected vertex subsets on a bounded-degree graph is exponential in L, not Bell-number growth. The extra 2^|U| subset sum is still exponential in L. For L=O(log(N/δ)), both costs are polynomial in N/δ with fixed microscopic constants.

### Support-moment clarification

Assign each grouped κ_U an explicit polynomial-radius envelope D_U containing the dependence supports of all constituent polymers. Bound

    sup_j Σ_{U:j∈D_U} |D_U| sup_a|κ_U(a)|

using the weighted anchored cluster estimates and the polynomial number of anchors whose envelopes can reach j. This is Oβ(ε). It is not literally enough to invoke triangle inequality against arbitrary *minimal* old supports D_C, because enlarging a support can newly count coordinates. The anchored counting already available in the polymer proof fixes this without adding a hypothesis. Use this enlarged-envelope bound for the truncated Φ_L sampler as well.

## 3. Restricted traces have no hidden global exponential oracle

Let K_U consist of the reference Hamiltonian terms meeting original perturbation supports in U. Every omitted reference term commutes with K_U and V_B. Their exponentials cancel exactly, leaving an operator supported on O(|U|) qubits. Its matrix dimension and Pauli-basis expansion cost are exponential only in O(L). Stabilizer membership and a generator representation for each local Pauli are polynomial-time binary linear algebra on the known full check matrix; valid redundant syndrome coordinates ensure representation-independent signs. Filling is used analytically for support control, not as an unimplemented computational oracle.

The proposed lower bound is correct. Jensen applied to the spectral measure of H_ref+V_B in the normalized P_a state gives

    F_B≥exp[−s τ_a(V_B)]≥exp[−s||V_B||].

Thus taking logarithms has at most exp(O(L)) conditioning. Local matrix exponentials may themselves have exp(O(L)) norms, but at L=O(log(N/δ)) this is polynomial and costs only O(L+log(1/δ)) extra precision bits. The sum over exponentially many local Pauli coefficients similarly adds only O(L) bits. Numerical errors across the N K^L 2^L evaluations can be allocated polynomially; exact real numbers are unnecessary.

For a fully instantiated algorithm, use computable conservative upper constants for the analytic moment bound and activity envelopes, not an unevaluated Oβ(ε). They can be obtained from the explicit graph/locality/filling constants and the convergent polynomial-times-geometric series; no maximization over all full syndromes is required. This is a constants-instantiation obligation, not an exponential oracle.

## 4. Joint memory/bath sampler

Detailed balance holds for the stated memory births/deaths and bath conditional heat baths. For a memory-polymer discrepancy γ, the potential-induced changes in common births sum to at most 4B ε_Φ m_γ. The sum of bath-update disagreement probabilities is at most ε_Φ m_γ: the conditional log-odds double difference costs ≤4 sup|φ_C|, and the logistic derivative contributes 1/4. Hard incompatibility contributes θ_h m_γ; death removes m_γ.

For one bath-bit discrepancy, its own conditional update couples exactly because its conditional law depends only on the other coordinates, which agree. Other bath updates cost at most ε_Φ and changed memory births at most 4B ε_Φ. Thus the displayed strict contraction condition is sufficient. The legal remove/insert path metric for memory configurations can be combined with ordinary bath Hamming paths.

The Papangelou birth envelope controls omitted trace polymers uniformly in b by the removal/insertion pairing. The truncated dictionary and bath-bit clocks have polynomial total size, and evaluating Φ_L globally at each proposed move is still polynomial. Finite-time numerical transition errors can be charged to the accepted Poisson cap. No low-density assumption for bath *bits* is used; the small parameter is the perturbative potential, while the onsite product law is handled exactly.

## 5. Canonical ensemble comparison

With G_a=g_a(I+R_a), ||R_a||≤η_n, replacing G_a^(−1/2) by g_a^(−1/2) changes each normalized isometry channel by O(η_n) in diamond norm; averaging preserves that bound. The remaining sum is exactly

    T(σ)=2 sqrt(ρ_H)(σ_L⊗I)sqrt(ρ_H),

because the W_a frames are matched to the same decoder. Arbitrarily chosen sector gauges would invalidate this identity, so the frame requirement is essential and correctly explicit.

For an arbitrary reference of dimension at most the logical dimension, expand the two sandwich factors and use Schatten Cauchy–Schwarz. The Hilbert–Schmidt norm of sqrt(ρ_H)−sqrt(ρ_bar) is at most sqrt(δ_tw). Tensoring the reference only introduces a fixed logical-dimension factor. Hence the diamond comparison with overwrite is O(η_n+sqrt(δ_tw)). The intermediate T need not be exactly trace preserving; the norm comparison does not require it.

Changing ensemble weights by TV ε_samp costs at most 2ε_samp in diamond norm, and uniform sector-isometry channel error adds ε_iso. The final error expression is therefore correct. It is reference-safe quantum preparation, conditional on actually implementing the isometries in the matched frame.

## Scope and unresolved gates

- Require L<L0 and retain the O(η_n) floor; increasing the cutoff past distance is not justified by this construction.
- Runtime polynomial in N/δ is not polynomial in log(1/δ), and the fixed exponents/constants may be enormous.
- Known efficiently computable finite-bath Hamiltonian coefficients are required and appropriately charged.
- Parent-gap, efficient parent simulation, transport/holonomy correction, and physical gate-fault robustness are not proved by this receipt.
- The inherited actual trace representation and geometric filling are external earned inputs to this audit, not conclusions of it.

No denied source was accessed. This audit used the supplied artifacts and direct algebraic/combinatorial derivations.

## Update: direct reference proof and finite-bath transport supplement

The current main file replaces the dimension-factor sandwich proof with the operator A_ρ=sqrt(2)(sqrt(ρ)⊗I_R)(|ξ⟩⊗I_G). This stronger formulation checks directly: ||A_ρ−A_bar||_2²=2Tr[(sqrtρ−sqrtρbar)²(ξ_L⊗I_G)]≤2δ_tw; ||A_ρ||_2≤sqrt(2), while ||A_bar||_2=1. The resulting <4sqrt(δ_tw) output trace-norm bound is valid for arbitrary reference dimension.

The appended real-s transport estimate also checks. The exact canonical-frame connection has matrix elements

    A_ij=G'_ij(√λ_j−√λ_i)/[2√λ_i√λ_j(√λ_i+√λ_j)],  A_ii=0.

Near-scalar Gram gives |A_ij|≤Cη_n|G'_ij|/g. Since ||G'||≤||H||λ_max(G), the logical two-dimensional connection is O(η_n||H||)=O(Nη_n) for a finite accessible bath. Its integrated canonical-versus-parallel transport mismatch is O(βNη_n). This does not require a complex-s derivative estimate and is sufficient when N is polynomial in n. It remains conditional on the parent path actually having these filtered ground spaces and on a separate gap/adiabatic theorem. No gap is inferred from Gram flatness.

Optional sharper analytic route: complex-s Duhamel/KP on fixed-radius disks gives a zero-free scalar factor and hence holomorphic normalized R=G/g−I. If ε is chosen to ensure convergence up to |s|≤β+r0, Cauchy bounds R' by Cnq(β+r0)^L0/r0. Writing G=g(I+R) in the exact connection cancels g'/g and the first-order R' terms, leaving ||A||≤C||R||||R'||. This route is also sound, but unnecessary for the finite-bath accuracy gate.
