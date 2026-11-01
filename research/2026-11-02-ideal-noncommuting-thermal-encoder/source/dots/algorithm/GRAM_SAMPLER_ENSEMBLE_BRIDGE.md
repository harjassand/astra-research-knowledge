# Actual filtered-code preparer: Gram, constructive sampler, and ensemble bridge

2026-11-01. Analytic construction, not an assumed Gibbs/TFD oracle. The parent gap/transport and physical gate-fault questions are separate. Finite accessible qubit bath only, N_B≤poly(n), known efficiently computable local couplings. Write N=n+N_B. The inherited actual filling, decoder-trace, distance, and finite-β polymer interfaces are used explicitly.

## 1. Uniform operator-valued Gram estimate

Let a=(σ,b) be a valid memory syndrome and complete onsite bath bit string. Let W_a:C²→P_a H be the isometry whose logical frame is the SAME protected decoder frame. H_ref=H0_memory+onsite bath fields, E_a its reference energy. For s∈[0,β], define

    G_a(s)=W_a† e^(−sH) W_a.

The Duhamel expansion from polymer_bridge.md is an OPERATOR expansion before taking its logical trace. Every disconnected event component has zero syndrome separately whenever its total product survives compression. Every component smaller than L0=floor((d−1)/b0) therefore compresses to a scalar; b0 includes enlarged patches and their bounded-size stabilizer connectors. All bath-only components are scalar at every size. Integrating their scalar gas and keeping every memory-touching component of size≥L0 as an exceptional logical matrix gives

    G_a(s)=e^(−sE_a) Z_small,a(s)[I+E_a^log(s)],
    ||E_a^log(s)||≤exp[B_n(s)]−1,
    B_n(s)≤C n q(s)^L0,
    q(s)=K(exp[s ε exp(c s)]−1).

Exactly the same excluded-region scalar partition ratios and product operator-norm bound used for the Gibbs trace prove this statement. No factorization of logical matrices is assumed. The count is anchored at memory-touching labels, hence n rather than N. The scalar Z_small is real and positive by the inclusion-exclusion/zero-free argument already audited.

Choose ε so q(β)<q_*<1 and n q_*^L0≪1. Since s≤β, the estimate is uniform in a, b, s, and reservoir volume. Define g_a(s)=TrG_a(s)/2. Recentring at the trace gives

    G_a(s)=g_a(s)[I+R_a(s)],
    TrR_a(s)=0,  ||R_a(s)||≤η_n:=C' n q_*^L0.

At s=0 the remainder is exactly zero. This is a uniform two-dimensional matrix estimate, not only a scalar weight comparison or an average-over-syndromes assertion. It gives no adiabatic holonomy theorem by itself.

## 2. Positive scalar potential for actual block probabilities

At s=β, actual block weights are

    p_a=TrG_a/Z_H ∝ e^(−βE_a) Z_small,a [1+r_a],
    |r_a|≤O(η_n).

Let Φ(a)=log Z_small,a. Its convergent scalar log-polymer expansion can be assigned supports D_C in joint syndrome/bath coordinates. Polynomial-radius stabilizer fillings imply |D_C|≤poly(m_C), and a coordinate j can belong only to clusters with anchors within polynomial distance in m_C. Weighted cluster convergence therefore gives the stronger moment needed by the interacting sampler:

    ε_Φ := sup_j Σ_{C:j∈D_C} |D_C| sup_a|φ_C(a)|
          ≤ C Σ_{m≥1} poly(m) q_*^m = O_β(ε).

Bath-only activities depend on local bath Z signs; memory activities can use the polynomially enlarged filling region. This bound is uniform over all valid a. The approximating distribution

    p_small(a) ∝ e^(−βE_a+Φ(a))

is positive and has TV distance O(η_n) from actual p. It does not require sampling signs of individual cluster activities.

### Explicit accuracy floor

The simplest algorithm below returns actual p with error O(δ+η_n), not an arbitrary-precision exact oracle. Its quantum label cutoff must satisfy L<L0. This covers every inverse-polynomial δ for sufficiently large n, and a stretched-exponential range. The η_n floor is also the uniform Gram approximation error used by the ensemble construction. No claim of arbitrary precision below that floor is smuggled into the sampler.

## 3. Constructive evaluation without Bell-number cluster enumeration

Naively listing all polymer-cluster partitions of total size L could be quasipolynomial. Avoid that by a connected LABEL-SET Möbius expansion, resumming repeated insertions.

For a finite label subset B let

    F_B(a)=τ_a[e^(sH_ref)e^(−s(H_ref+V_B))],
    V_B=Σ_{u∈B} V_u,  τ_a(X)=Tr(P_a X)/2.

For |U|<L0, every restricted component is small, so F_B is exactly the scalar restricted-gas partition for each B⊆U. Define

    κ_U(a)=Σ_{B⊆U}(−1)^(|U\B|) log F_B(a).

These are the log-clusters whose UNION of labels equals U, including all repeated-polymer occurrences. If U is disconnected in the generously enlarged event graph, κ_U=0. The connected-set potential

    Φ_L(a)=Σ_{connected U, |U|≤L} κ_U(a)

contains exactly the small-gas log-clusters with union support≤L. Every omitted cluster has total label multiplicity>L, so weighted KP convergence yields

    sup_a |Φ(a)−Φ_L(a)|≤C N q_1^L

for a fixed q_1<1 after absorbing harmless constants. Assign each grouped κ_U an explicit polynomial-radius envelope D_U around a deterministic anchor of U, containing the local checks and fillings of every Pauli supported on the enlarged U region. Its cardinality and radius are polynomial in |U|. The anchored moment bound for the regrouped potential follows by weighted cluster counting with THESE enlarged envelopes: a coordinate can be in D_U only for polynomially many size-m candidate anchors, and cluster total multiplicity m is at least |U|. It is not a bare triangle-inequality assertion about previously minimal cluster supports. Choose L=C_β log(N/δ)<L0. There are at most N K^L connected label sets; each needs 2^|U| restricted block traces, not a sum over Bell-many partitions. This is polynomial in N/δ for fixed microscopic constants.

### Each restricted trace is computable in polynomial time

Let K_U contain only H_ref terms meeting original perturbation supports in U. Every omitted reference term commutes with V_B and K_U, so exactly

    F_B(a)=τ_a[e^(sK_U)e^(−s(K_U+V_B))].

The operator on the right acts on O(|U|) qubits. Compute its matrix on dimension 2^O(L), then its Pauli expansion. For a Pauli term, its bath expectation is zero unless bath factors are I/Z; in the latter case the bath contribution is the known b-character. Its memory expectation is zero unless the Pauli is a stabilizer, or equals its known stabilizer syndrome character otherwise. At |U|<L0 no nontrivial logical Pauli survives. Stabilizer membership and a generator representation are computable by ordinary binary Gaussian elimination on the full known check matrix; all redundant checks are retained. This is polynomial in N even without a specially optimized local filling algorithm. No table over all assignments to the potentially polylogarithmic-volume envelope D_U is constructed: each Markov-chain query evaluates the matrix/Pauli character at its current valid a, using the same precomputed local operator coefficients and stabilizer row reduction. Tabulating 2^|D_U| would be an unjustified quasipolynomial/exponential cost and is unnecessary. Polynomial-radius filling is needed for the analytic support bound, not an uncharged computational oracle.

The local matrices have norm O(L) at fixed β. A Taylor series with scaling/squaring computes their exponentials to additive error ζ in time polynomial in their dimension, L and log(1/ζ). Positivity is quantitatively safe: by convexity/Jensen,

    F_B(a)≥exp(−s||V_B||)≥exp(−sε|B|),

while the Duhamel norm bound gives F_B≤exp(x|B|), x=sε exp(cs). Thus log evaluation has only polynomial condition number for L=Olog(N/δ). Inclusion-exclusion uses 2^L terms; choose each log precision at most δ/[poly(N) K^L 2^L]. Its bit requirement is O(log(N/δ)) with fixed constants. Known Hamiltonian coefficients and β must be supplied to this accuracy. No exact-real oracle or global 2^N exponential is used.

## 4. Joint positive sampling: trace births/deaths plus bath heat bath

Use the accepted actual memory decoder-trace gas. A legal configuration Γ is a compatible collection of recognized trace polymers γ, with size m_γ and top syndrome support S_γ; σ(Γ) is valid and decomposition/recombination are exact. Its bare weight is Π_γ w_γ with w_γ=exp(−βE(σ_γ)). Bath bits have the product onsite Gibbs distribution π_B^0(b). Target the explicitly positive finite approximation

    π_L(Γ,b) ∝ [Π_γ w_γ] π_B^0(b) exp[Φ_L(σ(Γ),b)].

Memory moves: remove each present γ at rate1; insert an absent compatible γ at rate

    w_γ exp[Φ_L(σ+σ_γ,b)−Φ_L(σ,b)].

Bath moves: update each bath bit at rate1 to its EXACT two-state conditional Gibbs law for π_L, evaluated from Φ_L and its onsite field. These moves satisfy detailed balance for π_L.

Let a_γ=w_γ exp(2ε_Φ m_γ). Assume the already earned low-temperature trace activity bounds with these slightly enlarged activities:

    Σ_{η incompatible γ} m_η a_η ≤ θ_h m_γ,
    B= sup_(memory syndrome j) Σ_{η:j∈S_η}m_η a_η <∞.

Low temperature plus ε_Φ=Oβ(ε) makes these bounds strict after shrinking ε. Couple memory birth proposals at a_η, deaths identically, and bath heat-bath updates by maximal coupling. Use weighted path metric m_γ for a trace discrepancy and1 for a bath bit discrepancy.

For one memory-polymer discrepancy γ: death removes m_γ; incompatible births cost at most θ_h m_γ; changed compatible birth rates cost at most4Bε_Φm_γ as in the accepted interacting-sampler proof. Bath conditional probabilities cost at most ε_Φm_γ, because the logistic derivative is≤1/4 and each double potential difference is≤4Σ_{C touching both changed supports}sup|φ_C|.

For one bath-bit discrepancy: its own heat-bath update coalesces at rate1; changed memory births cost≤4Bε_Φ, and other bath updates cost≤ε_Φ. Thus

    θ_h+(4B+1)ε_Φ<1

suffices for uniform path-coupling contraction. Bare bath defect probabilities need not be small: their product part is handled by heat-bath updates, not a low-activity bath-polymer assumption.

Truncate the actual trace dictionary at L_mem=C log(n/δ) using the Papangelou upper activities a_γ. Its omitted mass is≤Σ_large a_γ=O(δ), uniformly in b. On the finite dictionary, a dominating clock of rate

    R=N_B+#dictionary+Σ_γ a_γ

has polynomial size. Mixing time is logarithmic in the finite weighted diameter divided by the contraction margin. Use the already accepted Poisson cap and per-transition precision allocation. Computing Φ_L twice or once per candidate bath outcome costs polynomial time by Section3, even if no locality optimization is made. Truncation, mixing, cap, potential approximation, and transition precision each receive a specified share of δ. Total runtime is polynomial in N/δ with potentially enormous fixed degrees/constants, and output TV distance to actual p is O(δ+η_n).

## 5. Canonical filtered-code ensemble versus actual thermal overwrite

At final β set F=e^(−βH/2), G_a=W_a†F²W_a, and define canonical filtered isometry

    V_a=F W_a G_a^(−1/2).

The ideal ensemble channel is

    E_can(σ)=Σ_a p_a V_a σ V_a†,
    p_a=TrG_a/Z_H.

Write G_a=g_a(I+R_a), ||R_a||≤η_n. Removing each inverse square-root correction changes the summed channel in diamond norm by O(η_n), because Σ_a p_a=1 and ||F W_a/sqrt(g_a)||²≤1+η_n. What remains is exactly

    T(σ)=(2/Z_H) F [Σ_a W_a σ W_a†] F
         =2 sqrt(ρ_H)(σ_L⊗I_syn,bath)sqrt(ρ_H).

The identity Σ_a W_a σ W_a†=σ_L⊗I requires the matched decoder frame and is why arbitrary independent sector logical gauges cannot be substituted.

Let ρ_bar=I_L/2⊗τ and δ_tw=||ρ_H−ρ_bar||1 be the earned actual-Gibbs logical-twirl error. Square-root continuity gives

    ||sqrt(ρ_H)−sqrt(ρ_bar)||_2²≤δ_tw.

For an arbitrary pure logical-reference input |ξ_LR⟩, let G denote syndrome+bath and form A_ρ=sqrt(2)(sqrt(ρ_LG)⊗I_R)(|ξ_LR⟩⊗I_G), with tensor factors reordered consistently. This is an operator from G to LGR, not a full-rank tensor product of ρ with an identity reference. Then

    ||A_ρ−A_ρbar||_2²
      =2 Tr[(sqrt(ρ)−sqrt(ρ_bar))²(ξ_L⊗I_G)]≤2δ_tw,
    ||A_ρ||_2≤sqrt(2),  ||A_ρbar||_2=1.

The corresponding output density operators are A_ρA_ρ† and A_ρbar A_ρbar†. Hence their trace-distance is at most (sqrt(2)+1)sqrt(2δ_tw)<4sqrt(δ_tw), independently of reference dimension. Mixed inputs follow by purification or convexity. Thus

    ||E_can−E_overwrite||_diamond
       ≤C η_n+4 sqrt(δ_tw),
    E_overwrite(σ)=σ_L⊗τ.

For sampled weights with TV error ε_samp, the channel changes by at most2ε_samp. If each filtered-sector isometry is implemented with uniform diamond error ε_iso, the total error adds ε_iso. Therefore the preparation error feeding the exact-H storage theorem is bounded by

    C η_n+C sqrt(δ_tw)+2ε_samp+ε_iso.

This is an explicit weighted ensemble, not a purification oracle or an assertion that e^(−βH/2) acts unitarily. The square root of δ_tw weakens a stretched-exponential constant but preserves stretched-exponential smallness.

## 6. Remaining preparation gates and non-claims

1. The proposed frustration-free parent path must have a uniform-enough gap and efficiently representable/evolvable interactions. Other agents own that proof; it is not assumed earned here.
2. Adiabatic transport must implement V_a in the matched logical frame, or a known correctable logical unitary. Near-scalar Gram does NOT by itself justify ignoring non-Abelian transport. Other agents own transport analysis.
3. Uniformity over every a is necessary because the sampler can produce any allowed sector. The Gram estimate here is uniform; any parent-gap/transport claim must be equally uniform or include a quantified bad-sector probability.
4. This is a finite accessible bath with all couplings known and charged during preparation. It does not prepare an inaccessible/infinite bath, prove cheap initialization, or prove physical gate-fault tolerance.
5. The scalar sampler's O(η_n) floor is explicit. Arbitrary accuracy below that floor would require retaining exceptional logical-polymer contributions, not merely increasing the connected-small-set cutoff beyond distance.

Relevant earned inputs: `producer-workspace/polymer_bridge.md`, `thermal_encoding_bridge.md`, `independent_polymer_audit.md`; `producer-workspace/ROOT_RECURSIVE_THERMAL_SAMPLER_JOIN.md` and `ROOT_INTERACTING_POLYMER_SAMPLER.md`. No denied source was accessed.

## Reviewed finite-bath transport supplement (does not prove parent gap)

No complex-s derivative hypothesis is needed for the required accuracy. For the canonical frame V_a(s)=e^(−sH/2)W_a G_a(s)^−1/2, the exact connection is

    A=V_a†V_a'=(1/2)G^−1/2 G' G^−1/2+G^1/2(G^−1/2)'.

In an eigenbasis of G with eigenvalues λ_i, its diagonal is zero and

    A_ij=G'_ij (sqrt(λ_j)−sqrt(λ_i))
           /[2sqrt(λ_i)sqrt(λ_j)(sqrt(λ_i)+sqrt(λ_j))].

Near-scalar Gram gives |A_ij|≤C η_n |G'_ij|/g. Also G'=−W_a†e^(−sH/2)H e^(−sH/2)W_a, so ||G'||≤||H|| λ_max(G). Since logical dimension is two,

    ||A||≤C η_n||H||=O(Nη_n).

For fixed β and N polynomial in n, integration yields exponentially small canonical-versus-parallel holonomy error O(βNη_n). This is the already independently reviewed finite-accessible-bath bound supplied by root (FILTERED_PARENT_CONSUMER_AUDIT.md); a sharper complex-analytic derivative estimate is unnecessary for the preparation gate. The separate parent-path proof must still establish a uniform gap and quantified adiabatic approximation to this groundspace transport.
