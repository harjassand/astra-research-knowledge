# Constructive positive sampler for the actual interacting syndrome marginal

3 November 2026. Mathematical construction using the previously audited actual decoder-trace bijection and the certified K7 rod expansion. This is an ideal, finite classical algorithm, not local thermalization or a noisy physical loader.

## Statement and target

Let V be the actual valid redundant-check syndrome space of the fixed-ell random recursive code, and use precisely its supplied deterministic decoder, including the modified whole level-2 terminal decoder. Write s_a=(-1)^{sigma_a}. Let H_anc(s) be the exact Clifford-normal-form ancilla Hamiltonian, with every even and odd ring sector retained, and

    Z(s)=Tr exp(-beta H_anc(s)),   F(s)=-log Z(s)/beta.

The target is p(s)=Z(s)/sum_{u in V} Z(u), supported exactly on V. Equal stabilizer-sector dimensions cancel. No product approximation to Z(s) is made. For fixed model parameters in the certified rod regime, and sufficiently large but fixed beta in a fixed bounded interval, the construction below samples p to TV error delta in time polynomial in n/delta. Constants can be enormous and are not practical estimates.

The inputs needed from earlier work are: (i) the actual canonical trace bijection, bounded-degree O(n) trace host and |gamma|<=A |T_gamma|; (ii) the full Hamiltonian's exact finite-sector normal form, including spectator phases; (iii) the certified rod KP bounds and marked remainder epsilon<1 (the current point permits epsilon=1/4). These are substantive imported interfaces, not consequences of ordinary Peierls counting.

## 1. Constrained support and no witness multiplicity

Use the exact full-input-stencil traces of ROOT_DECODER_TRACE_POLYMER_LEMMA.md with the actual binding in independent_audit/ACTUAL_RECURSIVE_SAMPLER_BINDING_RECEIPT.md. Include cancellation gates, every required active fanout gate and exact truth-table values. Do not permit arbitrary zero decorations. The deterministic trace of an accepted syndrome has a unique connected-component decomposition. Conversely every compatible collection of individually accepted connected traces has exactly that union as its deterministic execution. Thus collections and valid syndromes are in bijection, not merely surjective.

Use the union of the X- and Z-validator hosts. Their validity constraints can be separate, but their Gibbs law generally is NOT a product after F is included. Each collection C corresponds to top support T(C)=disjoint union T_gamma and hence to one actual valid CSS syndrome. Hard-core insertions/deletions preserve validity exactly, including redundant relations. Logical representatives and downward correction expansion are not part of the sampler's counting measure.

## 2. Two distinct cluster bounds

The previously certified marked expansion supplies

    F(s)=C-J sum_a s_a+R(s),
    sup_a sum_{B containing a}|r_B| <= epsilon J,

where R=sum_B r_B product_{b in B}s_b. Therefore inserting a compatible trace gamma, which changes previously zero top syndrome bits to one, costs at least

    F(C+gamma)-F(C) >= 2(1-epsilon)J |T_gamma|.

A stronger spatial moment is needed for interaction-dependent mixing and computation. It need not have a small constant relative to J.

Multiply every ordinary-rod and wrapping-rod activity by exp(t), with t=0.01. At the certified point the strongest KP left side becomes at most .052169223 exp(.01)<.054; the second becomes .026816408 exp(.01)<.04. The wrapping condition retains slack in the cold regime. Thus the same KP theorem applies to the tilted activities. A cluster with spatial ring support A has |A| no larger than its number of polymer occurrences. Standard rooted-cluster domination, rooted on any rod/wrap on ring a, now gives

    sup_a sum_{clusters whose support A contains a}
       exp(t|A|) |cluster weight|/beta <= C_t(beta),

    C_t(beta)=exp(a+t) M(b)+exp(a+t+b beta)Q_beta/beta.

This is the unmarked bound and includes flux-independent clusters. It is consequently conservative but avoids any need to improve the delicate marked estimate. Complete trajectory species are retained: each cluster's syndrome dependence is a single character times a scalar coefficient, and its absolute coefficient is bounded by the same absolute cluster weight. Cross-ring signed phases are never treated as positive Gibbs weights.

For the non-singleton Fourier terms f_B of F, this yields

    K := sup_a sum_{B containing a, |B|>=2} |B| |f_B|
       <= C_t(beta)/(e t).

Indeed |B|<=|A| and x<=exp(tx)/(e t). Singleton terms have zero mixed difference and need not enter K. C_t and K have uniform finite upper bounds for beta in the stated cold fixed interval (indeed the wrap term decays). The numerical scale is conservative, roughly K<=.012 Delta, rather than O(J). This worsens the temperature threshold but does not alter polynomiality at sufficiently low fixed temperature.

## 3. Exact positive interacting chain

For a compatible absent trace eta use birth rate

    b_eta(C)=exp[-beta(F(C+eta)-F(C))],

and remove each present trace at rate one. All rates are positive. Detailed balance holds for the exact measure proportional to exp[-beta F(s(C))], and the canonical bijection makes its pushforward exactly p. This is a Gibbs sampler for the genuine constrained marginal, not an assertion that physical Davies dynamics mixes rapidly.

Let m_gamma=|gamma| and let c bound the number of labeled size-m traces rooted at a host object by c^m. Coercivity gives the envelope

    b_gamma(C)<=a_gamma=exp(-kappa m_gamma),
    kappa=2 beta (1-epsilon)J/A.

Let G=sup_v sum_{gamma containing v} m_gamma a_gamma. Then G<=sum_{m>=1} m c^m exp(-kappa m). Every top syndrome coordinate is represented by a host object, so the corresponding top-site sum is also at most G. Let h be the bounded number of host roots per trace object that can create a stencil conflict. The hard-core disagreement sum is at most h G m_gamma.

For adjacent configurations C and C+gamma and an eta insertable in both, singleton energies cancel in the mixed difference. Hence

    |b_eta(C+gamma)-b_eta(C)|
      <=4 beta a_eta sum_{B meeting T_gamma and T_eta}|f_B|.

Summing m_eta times this quantity and then rooting eta at a top site in B gives

    sum_eta m_eta |birth-rate difference|
      <=4 beta G sum_{B meeting T_gamma}|B||f_B|
      <=4 beta G K |T_gamma| <=4 beta G K m_gamma.

Couple common deaths identically and births by shared thinning. Weighted symmetric-difference distance is the path metric on legal collections. Death of gamma decreases distance at rate m_gamma; hard conflicts and soft rate mismatches are bounded above as displayed. Thus contraction holds with

    theta=G(h+4 beta K)<1.

More explicitly, put q=c exp(-kappa). Then G<=q/(1-q)^2. It suffices to enforce q<=1/2 and 8q(h+4 beta K_max)<=1. The threshold is computably searchable from the fixed trace-table constants, certified J lower bound and a uniform certified K_max, rather than an unspecified mixing oracle. Since G decays exponentially in beta and K is bounded, theta<=1/2 holds above a sufficiently large fixed beta threshold. This remains true even though the crude K/J is enormous. It is not legitimate simply to use the passive-memory temperature threshold; sampling may require a colder fixed operating point.

For host size N=O(n), compatible collections have total trace size<=N, so diameter<=2N. The TV mixing error at time T is at most 2N exp[-(1-theta)T]. Taking T=log(2N/delta_mix)/(1-theta) suffices.

## 4. Finite dictionaries and interacting truncation

Enumerate every connected, canonically labeled trace of size<=L_tr, validate its exact deterministic execution, and keep it once. The dictionary has size at most N sum_{m<=L_tr}c^m. For the full interacting law, detailed-balance insertion/deletion pairing gives

    Pr(gamma present)<=a_gamma.

Therefore the probability any omitted trace occurs is at most N sum_{m>L_tr}c^m exp(-kappa m). Choosing L_tr=O(log(n/delta)) makes this below delta_tr. The law conditioned on no omitted trace is exactly the same interacting chain restricted to this dictionary; no independence assumption is used.

## 5. Deterministic relative-weight oracle from finite ancilla matrices

A convergence theorem alone is not an implementable oracle. Here is a concrete finite one. On a connected ring subset A define

    Phi_A(s_A)=sum_{C subseteq A}(-1)^{|A\C|} log Z_C(s_C),

where H_C=<0_(C-complement)|H_anc|0_(C-complement)> is the vacuum matrix-element restriction, NOT a partial trace or thermal boundary condition. It retains the full k-qubit ancillas of every ring in C and all internal spectator phases. Thus omitted rings contribute no rods or wraps; interactions among retained trajectories are unchanged. Define Z_empty=1. This boundary convention is essential.

Möbius inversion extracts exactly the linked clusters whose spatial support is A. Disconnected A give zero because the restricted trace factorizes across disconnected components. Therefore

    log Z(s)=sum_{connected A} Phi_A(s_A).

Truncate to |A|<=L_F. The tilted rooted bound gives uniformly in s

    |log Z(s)-log Z^(L_F)(s)|
       <= beta n_ring C_t exp(-t L_F).

The notation log Z^(L_F) means the truncated real-valued logarithm, not the logarithm of a truncated signed partition series. Exponentiating it is always positive. Taking L_F=O(log(n/u)) gives uniform log-weight error u. Consequently normalized finite-precision approximate target weights have density ratios in [exp(-2u),exp(2u)], and every insertion ratio has relative error at most exp(2u)-1. This is a relative error guarantee for weights/rates, not a pointwise relative guarantee for probabilities removed by trace truncation; the overall sampling guarantee is TV.

There are n_ring exp(O(L_F)) connected sets. For each C subseteq A the explicit matrix has dimension at most 2^(7|C|), is Hermitian, and has polynomially describable entries of norm O(|C|) at fixed parameters. Certified matrix-exponential/trace or eigenvalue approximation evaluates its positive trace and log to any required additive precision with exp(O(L_F)) work and polynomial precision cost. Charge the 2^|A| inclusion-exclusion terms and precision needed for cancellation. The total number of such terms is still n_ring exp(O(L_F)); For a final log-weight budget u, allocate u/2 to spatial truncation and u/2 to all numerical errors; requesting error (u/2) divided by this count makes all roundoff contributions <=u/2. The combined error is then u, as required for the displayed density ratio. There is no exponentially small acceptance/rejection probability in this oracle and no stochastic sign cancellation. Dense local matrices, not the global 2^(7n_ring) matrix, are evaluated.

All claims here use fixed beta, Delta, ell and k. Uniform polynomial complexity when beta or ell grows with n is NOT asserted. Local finite-matrix computation at very large fixed beta is an enormous allowed constant.

## 6. Finite simulation and error accounting

Use the finite dictionary and unit birth-proposal/unit death-proposal clocks for each dictionary entry. Since exact births are <=a_gamma<=1, total proposal rate is 2 N_dict. A legal birth is accepted with probability b_gamma(C); absent deaths and incompatible births are null. Approximate log-ratios to additive error nu, exponentiate with certified precision and clamp acceptance to [0,1]. This changes each proposal kernel by O(nu); clamping cannot increase its distance from the exact probability.

Set R=2 N_dict and run for T above. Cap the Poisson event count at ceil(2RT+2log(1/delta_cap)); the standard exponential moment at log 2 bounds cap overflow by delta_cap. Approximate Poisson sampling and each transition with total budgets delta_pois and delta_num, allocating per-event error delta_num/cap. Trace truncation, mixing, cap, Poisson and numerical errors sum to the requested delta. Computing the oracle to the corresponding inverse-polynomial precision keeps L_F logarithmic, dictionary sizes polynomial, and the capped number of events polynomial.

The numerical relative-log-weight guarantee is also independently useful: if one chooses to simulate the exact chain associated with the uniformly truncated log weight, its normalized stationary measure differs multiplicatively by exp(±2u). The direct per-step coupling above avoids needing to re-prove its mixing bound.

## Consequence and limits

This fills the interacting constrained-syndrome sampling interface for the exact finite-temperature K7 rod Hamiltonian, conditional on the previously earned normal form, rod bounds and canonical actual trace representation. It is not the ideal native-check Gibbs distribution and does not discard wrapping, odd-parity or finite-density excitations. It is compatible with a separate conditional ancilla Gibbs-state preparation theorem.

It does not alone prepare that conditional quantum state, supply an encoded logical input, tolerate generic uncontrolled perturbations or fixed-rate gate noise, certify a practical temperature, or establish a passive return-to-equilibrium rate. These remain separate obligations. All stated classical transitions are positive, and signed quantum histories enter only a deterministic, absolutely controlled local computation.

## Independent audit corrections

The independent actual-sampler audit returned qualified mathematical PASS. Its three requested clarifications are incorporated above: exact vacuum matrix-element restriction, explicit proposal rate R, and split truncation/roundoff budgets. Physical noisy WRITE remains a separate gate.
