# Same-native-H annealed hole transfer: exact source majorant and three-species checks

2026-11-02. Independent constructor check of root's ROOT_NATIVE_SYNDROME_SENSITIVE_HOLES.md, using the earned singleton-normalized source/event dictionary. This note supplies the missing simultaneous-history bound and all third-species rows. Full theorem promotion should follow independent audit of the complete join.

## 1. Finite-time energy and tail, exactly

For clock a define

  I_a,beta=integral_0^beta rho_a(ell)dell,
  J_a,beta=integral_0^beta rho_w,a(ell)dell,
  h_a,beta=I_a,beta-J_a,beta,
  delta_a=M0_a-I_a,beta=integral_beta^infty rho_a(ell)dell,
  B_a=2 beta J_a,beta.

All quantities refer to the SAME physical clock Hamiltonian. The additive reference defect activity is exp(-sum_{a in tau}B_a), obtained from the exact one-winding pressure; it is not beta times an approximate low-energy coefficient.

For a resonant clock the existing spectral tilt c=t/K^2 gives

  delta_a <=(4/3)M0_a exp(-beta t_a/K_a^2).

Equivalently retain the exact tail integral. The owned-clock raw path integral is bounded by K_a exp(beta M0_a), as in the earned dictionary.

## 2. Uniform pointwise history majorant after extracting holes

Take a concrete source history Gamma from the earned enlarged-contact dictionary. Its owned clocks are C_Gamma and its contact clocks T_Gamma=N1(C_Gamma). Its total data Pauli word E_Gamma is centralizer-valued after source closure. Below distance strip the constant phase and write its scalar syndrome character chi_E(s).

All remaining dependence on the initial syndrome is on T_Gamma: internal closing-hop signs use only owned fluxes, and exterior singleton responses use only contact fluxes. Thus

  z_Gamma(s)=chi_E(s) f_Gamma(s restricted to T_Gamma)

exactly. No polynomial filling has been included in the local function.

For an owned clock, multiply the raw absolute path density by its singleton deletion and by the inverse of the proposed hole factor:

  exp[-beta h_a,beta-beta J_a,beta s_a-B_a q_a(s)]
      =exp[-beta(h_a,beta+J_a,beta)]
      =exp[-beta I_a,beta].

This is independent of s, since s+2q(s)=1.

For an exterior winding response, write its real exponent as s_a r_Gamma,a, where r_Gamma,a is the integral of positive winding density times (B_pin-1), hence

  -B_a <= r_Gamma,a <=0.

After extracting the hole factor its modulus is

  exp[s_a r_Gamma,a-B_a q_a(s)] <=1

for both s_a=+1 and s_a=-1. Exterior nonwinding and wrap responses already have modulus <=1. Owned wrap deletion also only decreases the bound.

Therefore there is a SINGLE positive measure w(dGamma), independent of all initial syndrome values, such that

  |z_Gamma(s)| <= w(dGamma) exp[sum_{a in T_Gamma}B_a q_a(s)],

pointwise in every concrete source trajectory, and for a fixed m-label set

  integral w(dGamma)
    <= product_owned K_a exp(beta delta_a) * d_B^(b_B m)
           product_labels[exp(beta v_lambda)-1]
    <= q_native^m,

  q_native=K_max^b_c d_B^b_B exp(beta delta_max b_c)
                       [exp(beta v_dict)-1].          (N1)

This simultaneous pointwise envelope is stronger than a separate integrated bound for each syndrome. It legitimizes evaluating the local function on the variable swallowed defect configuration without an extra supremum/Fourier factor.

In particular, NO Walsh expansion of even the O(m) contact function is needed. Its entire s_T dependence becomes internal once all occupied contact checks are swallowed. Retaining the original word E_Gamma preserves the logical threshold m>=d/b_D instead of artificially inflating its support by check products.

## 3. Exact three-species reconstruction

Start from the full source/clock trace at fixed syndrome. Multiply the normalized background response by the original background partition function. After all singleton responses have been absorbed into source activities, its remaining factor is

  exp[sum_{events e, n(e)>=2} nu_+(e) chi_e(s)
                                      product_sources B_Gamma(e)].

Here nu_+ is the connected native rod-cluster measure at all-plus flux, chi_e(s) is the character of the event's winding rods, and B_Gamma(e) is the already-earned product pin in {0,+1,-1}. Expanding this exponential creates independent EVENT objects; event-event factor is exactly 1. Events may overlap because they represent the exponential of a logarithm, not disjoint physical rods.

Represent the additive singleton syndrome weights by the exact T_plus defect gas with inhomogeneous B_a. Apply the unique source/defect hole grouping, now using contact sets T_Gamma rather than just owned checks. Every occupied contact check belongs to a swallowed defect polymer, so each source's local function is fully internal.

For a group G, let m be its source label count, M its swallowed defect mass, and C_G=union of contact sets, |C_G|<=d_c m. The exact lost energy is sum_{a in tau_G intersect C_G}B_a. Therefore its absolute envelope is

  q_native^m exp[-B_min max(0,M-d_c m)].               (N2)

The weighted cancellation is exact even for heterogeneous clocks. Never replace it by exp(B_max d_c m) before summing the free capacity.

Ordinary defects and hole groups have the same mutual hard-core and scalar-character factors as in the commuting construction. An event has pair factor

  h(e,gamma)=chi_e(tau_gamma)

with an ordinary defect, and

  h(e,G)=chi_e(tau_G) product_{Gamma in G}B_Gamma(e)

with a group. Each is 0 or +/-1. All internal source/defect phases are retained in the group activity. This accounts for every original event character and source pin exactly once.

## 4. Source/defect rows inherited from the annealed group theorem

The group free-capacity bound and connected entropy use m+M, with d_c in place of b_c. Source words remain attached to their original connected USED-label components inside each group. Compressed adjoint contacts control a fixed source word against high-level defect corrections; polynomial local filling controls the reverse row componentwise. All those estimates remain unchanged because the event species adds only new scalar pair factors.

At a given fixed positive beta, choose B_min above the cold/entropy threshold and q_native below the constant activity threshold, reserving strict margins for events and tilts. The native energy tail in (N1) is separately charged, not silently dropped.

## 5. All EVENT KP rows

Let

  E_gamma=sup_clock a integral_{e: a in support(e)} |nu_+|(de) exp[gamma n(e)].

Use the already-audited inflated native rod bound, including wraps, to evaluate it. It is O(beta J D eta^2) plus the specified thermal terms, not an unconditionally beta-independent constant.

**Ordinary defect root.** chi_e(tau) can differ from 1 only if the event has a winding clock on one of its M occupied top checks. Thus its event row is at most 2 E_gamma M.

**Hole-group root.** Use |product k_i-1|<=sum|k_i-1| for |k_i|<=1. A source pin can differ from 1 only when the event touches its contact set; total contact count is <=d_c m. The event character can differ from 1 only at an occupied top check of tau_G. Hence

  event row <=2 E_gamma(d_c m+M).                     (N3)

**Event root.** Its support and winding-character set have size at most n(e). A nontrivial pair with an ordinary defect is rooted at one of those base checks. A nontrivial pair with a hole group is rooted either at an occupied top check in event support or at a source label whose contact set meets event support. Both are bounded-degree physical roots. Let delta_D,delta_occ,delta_src be the corresponding charged rooted sums of the admitted defect/group gas. Then

  defect/group row <=C n(e)[delta_D+delta_occ+delta_src]. (N4)

The rooted sums are made arbitrarily small by cold/source margins. Thus (N4) fits gamma n(e), while (N3) and the ordinary row fit the unused linear m+M charges whenever E_gamma satisfies an explicit fixed margin. No event-to-event row exists.

These are genuine three-species KP inequalities for the exact |h|<=1 gas, not a forest approximation.

## 6. Temperature and resource tradeoff

To have source admission controlled by beta v with a beta-independent numerical activity threshold over a chosen operating interval, require

  E_gamma <= E_*,

where E_* is the allocated event margin. Since E_gamma scales as beta J D eta^2 (with the actual incidence constants), colder operation may require eta^2=O(1/(beta J D)). The resonant compiler's native peak energies increase accordingly. This tradeoff is essential: the result is not a fixed-v theorem for all beta, nor a claim of practical constants.

At a fixed physically chosen positive temperature, strict B_min and E_gamma margins remove the previous extra exp(C beta J) source-hook penalty. Remaining costs include K_max^b_c, bath dimension, dictionary l1 norms, d_c, connected-animal entropy, and the compiler energy ratios. They must be substituted before claiming a useful numerical tolerance.

## 7. Tilted actual Gibbs probabilities and exceptional logical words

For a fixed witness set W, tilt each defect-bearing object by exp[h|W intersect tau_object|]. This exactly inserts exp(h sum_{a in W}q_a) at the original trace boundary. Source closure/pinching remains valid because the boundary insertion is syndrome diagonal. Events themselves carry no initial occupied syndrome and are not tilted.

The group majorant survives by reserving B_min-h on paid defects and a factor exp(h d_c m) in the source budget. The same rooted-cluster interpolation bounds the scalar partition ratio. Reserve those budgets for exceptional logical source roots as well; their actual data word support is <=b_D m, so non-scalar roots have m>=d/b_D. In the decoder frame their syndrome dependence is still the compressed character times a fixed logical matrix. The reverse filling estimate is needed only for scalar background sources.

If r_h,r_0 are the relative exceptional bounds, the ACTUAL positive Gibbs moment is bounded by

  exp(C_h |W|) (1+r_h)/(1-r_0),

and hence

  Pr(W entirely occupied) <= exp[-(h-C_h)|W|](1+r_h)/(1-r_0).

One must not apply Markov directly to a scalar truncated signed gas. The full Gibbs trace supplies positivity after exceptional control. With h above witness entropy, this gives the actual native rare-bad estimate required by the stationary-state SWAP consumer.

## Status

The source-envelope refinement and event rows check algebraically against the earned native dictionary, and preserve all clock excited states. The complete exact three-species/hole-group theorem still merits independent audit as a joined construction. No new physical Hamiltonian, bath approximation, ground-state truncation, or local positive-term deletion has been used.

## Exact exceptional phase factorization uses decoder additivity

For a logical centralizer Pauli E, chi_E(s)=(-1)^[E,D(s)] is not generally a linear character of arbitrary syndrome sums. The new exact trace-polymer reverse assembly supplies the needed stronger fact on represented configurations:

  D(sum_compatible tau_gamma)=sum_compatible D(tau_gamma).

All component corrections/branches are unchanged under assembly, the physical prepass is linear, and at most one terminal bag is active. Consequently chi_E(s)=product_gamma chi_E(tau_gamma) on every gas configuration, and likewise over the swallowed/ordinary partition. This makes the exceptional source's pairwise pins exact. It must not be justified merely by calling a logical Pauli a stabilizer character.
