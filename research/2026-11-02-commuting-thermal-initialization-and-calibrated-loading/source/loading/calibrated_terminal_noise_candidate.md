# Candidate: calibrated terminal-noise compensation for the actual commuting memory

2026-11-01. Independent positive-constructor continuation. **For independent review.** Conditional on the parent's actual accepted-decoder-trace polymer bijection and standard low-temperature witness bound. This is a narrowly calibrated, independent terminal-Pauli-noise result, not arbitrary-noise FT, a generic interacting Gibbs-state loader, or a practical threshold claim.

## Outcome and scope

Sample a deliberately pre-distorted syndrome distribution, apply the fixed decoder Pauli representative to a supplied encoded input, and allow a known independent physical Pauli-noise layer. At sufficiently small FIXED noise relative to the chosen FIXED temperature, the pre-distorted distribution is positive and admits a candidate polynomial-time positive sampler. Every partial-noise syndrome law obeys a perturbed Peierls estimate. Consequently the final syndrome law is exactly Gibbs, while a union bound makes logical-frame mistakes stretched-exponentially rare. This yields full reference-safe trace-distance closeness to the ideal commuting equilibrium-overwrite channel, not merely an initial logical overlap.

The latter is the important bridge: once full output-channel closeness is earned, subsequent CPTP evolution adds the loading discrepancy only once. One may attach an independently established commuting Davies storage theorem. One may NOT replace the required actual noncommuting interacting Gibbs state by this commuting state and invoke the exact-generic-H theorem.

## 1. Exact inverse-noise identity

Use the complete valid syndrome space S, including redundant-check coordinates, for the actual H0. Let pi(s)=Z^(-1) exp[-beta E(s)], E(s)=sum_a J_a s_a. Fix bounded-support physical Pauli fault labels i=1,...,M, with bounded label overlap, each independently present with probability q_i<1/2. Let d_i be its syndrome shift and F_i the permutation s->s+d_i. Pauli phases are irrelevant. The syndrome channel is

 C_i=(1-q_i)I+q_i F_i,
 C_i^(-1)=[(1-q_i)I-q_i F_i]/(1-2q_i).

All these syndrome permutations commute. Define

 pi_pre=(product_i C_i)^(-1) pi.

The inverse preserves total mass. Positivity, not normalization, is the nontrivial question. The same construction is required for EVERY subset I of labels; write pi_I=(product_{i in I}C_i)^(-1)pi.

For valid s,

 pi_I(s)/pi(s) = [product_{i in I}(1-q_i)/(1-2q_i)] Z_I(s),
 Z_I(s)=sum_{F subset I} [product_{i in F}(-r_i)] exp[-beta(E(s+d_F)-E(s))],
 r_i=q_i/(1-q_i).

This is an identity on the actual constrained syndrome space, not an independent-check approximation. Translations by physical errors preserve validity. The expression Z_I(s) can also be defined on invalid bitstrings for local calculations without assigning them probability.

## 2. Signed error-island gas: positivity and local potential bounds

Make a graph on physical fault labels: connect two labels if their affected check sets overlap. Its degree is bounded by a fixed constant D. A connected nonempty error set gamma is a polymer, incompatible with sets at graph distance at most one. If error sets are disconnected in this graph, their energy increments add. Thus Z_I(s) is exactly the hard-core signed polymer partition function with

 z_gamma(s)=product_{i in gamma}(-r_i) exp[-beta(E(s+d_gamma)-E(s))].

Let B bound the sum of J_a over checks affected by one fault label. Uniformly in s,I,

 |z_gamma(s)| <= u^|gamma|,  u=max_i r_i exp(beta B).

Choose u below a sufficiently small constant depending only on D, with strict margin. The usual Kotecky-Preiss condition can be checked directly: rooted connected-set counting is exponential, and

 sum_{eta incompatible gamma} |z_eta| exp(2|eta|)
 <= (D+1)|gamma| sum_{k>=1}(e(D+1))^(k-1) u^k exp(2k)
 <= |gamma|

when u is small enough. The spare exponential factor controls tails and polynomial size moments. This uniform majorant applies also when any set of labels is deleted.

The convergent cluster expansion makes Z_I nonzero on the entire real interpolation from zero fault rates to the chosen rates. It starts at 1 and stays real, so Z_I(s)>0. Therefore every pi_I is a genuine positive normalized probability measure.

Write Phi_I(s)=log Z_I(s)=sum_C phi_C(s), with C a connected multiset cluster of error polymers. Its dependency set A_C consists of the check bits touched by that cluster. The coefficient is the usual Ursell coefficient times the product of z_gamma(s); it depends ONLY on s restricted to A_C. The same absolute activity majorant, with the spare exponential, gives constants K_0,K_1 independent of n and I such that

 sup_a sum_{C:a in A_C} sup_s |phi_C(s)| <= K_0 u,
 sup_a sum_{C:a in A_C} |A_C| sup_s |phi_C(s)| <= K_1 u.

The inequalities also hold with an exponential total-cluster-size weight after shrinking u further. They follow by anchoring at one of the bounded number of fault labels touching a, applying the rooted cluster bound, and absorbing |A_C|<=const*sum_gamma|gamma| into the spare exponential.

For a syndrome modification tau supported on T,

 |Phi_I(s+tau)-Phi_I(s)| <= 2 K_0 u |T| =: kappa |T|.

For disjoint modifications supported on T and T', the mixed difference is bounded by

 |Delta_T Delta_T' Phi_I| <= 4 sum_{C:A_C meets T and T'} sup_s |phi_C|.

These are uniform supremum estimates, not expectations in a presumed invariant cone.

## 3. Peierls estimate for EVERY noise prefix

Constants in pi_I independent of s cancel in ratios. The previous bound gives

 | log(pi_I(s)/pi_I(s')) + beta(E(s)-E(s')) | <= kappa |s-s'|.

For the actual removable witnesses, the original witness-removal injection therefore applies with beta J_min replaced by beta J_min-kappa. Keep a strict low-temperature margin. The same enlarged bad-syndrome set then has, uniformly over I,

 pi_I(Bad) <= poly(n) exp[-c n^eta] =: b_n.

This uses the actual code witness theorem and fixed decoder; it is not a new general quantum-code threshold.

Now apply the physical independent fault labels in any fixed order. After the first t labels, its syndrome marginal is exactly

 pi_t = (product_{i>t} C_i)^(-1) pi = pi_{I_t}.

Thus every prefix has bad probability at most b_n. Each bounded-support Pauli fault acts trivially on the decoded logical algebra outside the admitted Bad set. Starting with the fixed decoder representative E_D(s), the probability of ANY logical-frame fault is at most M b_n by a union bound over prefixes. This controls the joint syndrome/error history; a final Gibbs marginal alone would not.

At the endpoint pi_M=pi exactly. Split histories into those with and without logical-frame faults. On a good history, the final state in syndrome s is precisely E_D(s) Enc0(rho_LR) E_D(s)^dagger. On a bad history it differs by a logical Pauli. Therefore, uniformly for reference-entangled inputs,

 || Loaded_noisy(rho_LR)-Ideal_thermal_overwrite(rho_LR) ||_1 <= 2 M b_n.

An approximate initial sampler of TV error epsilon adds at most 2epsilon by contraction. No global inverse-density bound is used. The construction does not assert an invariant local-stochastic cone under thermal dynamics.

## 4. Positive sampling on the actual trace host

Assume the parent's accepted trace representation: valid syndromes biject with compatible collections Gamma of typed trace polymers gamma, on a bounded-degree O(n)-size host, with weights w_gamma=exp[-beta E(s_gamma)] <= exp[-a|gamma|], and local polynomial membership tests. Top syndrome supports are disjoint in a compatible collection. The pre-distorted target becomes the POSITIVE measure

 mu_pre(Gamma) proportional to product_{gamma in Gamma}w_gamma * exp[Phi(s_Gamma)].

It is NOT an independent hard-core polymer gas; Phi supplies weak soft interactions. Sampling signed weights or global rejection of exp[Phi] would be invalid/inefficient.

Consider continuous-time births and deaths: each present polymer dies at rate1; a compatible absent gamma is born at rate

 b_gamma(Gamma)=w_gamma exp[Phi(s_Gamma+s_gamma)-Phi(s_Gamma)].

Detailed balance holds exactly. Since |Delta_gamma Phi|<=kappa|gamma|, birth rates are dominated by wtilde_gamma=w_gamma exp(kappa|gamma|). Implement births with this state-independent proposal rate and the corresponding acceptance probability <=1.

Use weighted symmetric-difference distance sum of polymer sizes. For configurations differing by one polymer eta, couple common births and deaths. Its death decreases expected distance at rate |eta|. Extra disagreements arise from:

(a) hard-core incompatibility: summed weighted birth rate <= a_hard |eta|, where a_hard is controlled by the standard rooted first moment of wtilde;

(b) compatible births with different acceptance rates: the mean-value inequality bounds their rate discrepancy by wtilde_gamma |Delta_gamma Delta_eta Phi|. Using the mixed bound above, sum over gamma first. If

 L_1 = sup_host_vertex v sum_{gamma containing v} |gamma| wtilde_gamma,

then the sum over gamma whose top support meets A_C is <= |A_C| L_1 (up to the fixed mapping/incidence constant). Sum over C touching the top support of eta and use the anchored second bound. The result is <= const*L_1*K_1*u*|eta|.

At sufficiently low temperature and small u, choose a_hard+const*L_1*K_1*u<1. Weighted path coupling gives contraction at a fixed positive rate. The state's distance to any other state is O(n), so continuous-time mixing is O(log(n/epsilon)). This is an algorithmic trace-polymer chain, NOT the physical single-spin Gibbs dynamics.

### Explicit polynomial fallback and errors

Truncate trace polymers at K=O(log(n/epsilon)). The probability of a particular present polymer is at most wtilde_gamma by the deletion-ratio bound. Rooted exponential tail summation bounds omission probability by O(n exp[-cK]). Enumerate all typed connected host candidates up to K, validate them locally, and retain accepted polymers. Their number is polynomial in n/epsilon for fixed constants, even though those constants may be enormous.

Truncate Phi's error-cluster expansion at total polymer size L=O(log(n/epsilon)). Uniform tail bounds give sup_s |Phi-Phi_L|<=epsilon_1. Hence the exact and truncated normalized positive measures differ in TV by at most exp(2epsilon_1)-1. The same influence bounds apply to the truncated expansion, preserving contraction. Bounded-degree connected-cluster enumeration with computable weights evaluates Phi_L in n exp[O(L)] time by established algorithmic cluster-expansion methods; see sources below. This avoids a naive n^L enumeration.

Uniformize the finite birth/death chain using an explicitly computed polynomial upper bound on total proposal/death rates. After polynomially many discrete updates it has the required TV accuracy. Approximate each acceptance probability to additive epsilon_2 divided by the charged number of updates; standard stepwise coupling bounds the additional TV error by epsilon_2. Couplings, exponentials, weights and random bits require polynomially many precision bits. No exact-real oracle or signed-probability sampler is assumed.

The hard-core-plus-soft-influence path-coupling proof above is the new interface requiring independent audit; the cluster-expansion and enumeration machinery are established methods. This note does not substitute a citation for its actual constrained-trace binding.

## 5. Physical assumptions and comparison gate

- The encoded unknown input is supplied, or its active FT encoding error is charged separately. This construction does NOT prove generic noisy active encoding leaves only a known independent terminal channel.
- The decoder representative is a product of single-qubit Paulis and can be commanded in parallel after classical computation/routing. The noise model assumes a calibrated independent Pauli channel AFTER that layer, independent of sampled syndrome and logical input. Idle noise during sampling/control, coherent correlated noise, and always-on dynamics during pulses are not silently included.
- A model with switchable commuting protecting terms or justified calibrated effective terminal channel is a narrower physical model than the target generic exact spin environment. Bounded control strength means nonzero gate duration; that duration and switching/control assumptions must be stated.
- No physical reset is required just to apply the final Pauli layer. Classical randomness and computation, preparation of the supplied encoded input, calibration samples, and any thermal ancillas used to realize/test the channel are charged resources. Active FT receives identical resources.
- Noise tolerance scales conservatively like q <= const exp[-beta B]. Colder preparation can make the admissible final noise much smaller. This is a restricted mechanism, not competitive-threshold evidence.
- Calibration need not be infinitely precise: for Bernoulli Pauli factors, product-channel telescoping gives diamond distance <=2 sum_i|q_i-qhat_i|. Accuracy O(delta/M) per parameter makes calibration error additive O(delta) at the endpoint. Under truly stationary iid common-q noise, estimation to this accuracy uses O(M^2 delta^-2 log(1/alpha)) samples at confidence1-alpha. These samples/time are charged. Fixed calibration error density, drift or unknown correlations reopen the gap.
- Readout remains ideal or separately protected/charged. Full quantum readout must not be replaced by destructive classical syndrome/Pauli measurement without stating the changed task.

## 6. Finite actual-geometry checks and failure region

Scripts test the actual one-square RX ell3 fixture (19 qubits, 12 Z checks, 2048 valid syndromes), not the large recursive logical-memory decoder. Direct inverse/forward and every-prefix identities hold to floating-point accuracy; 80-digit checks confirm:

 beta=2, q=.001: min pi_pre=-0.000222748743457595758..., INVALID probability;
 beta=4, q=1e-7: min pi_pre=-1.7937154302853424e-23, ratio=-.01458214094, genuinely INVALID;
 beta=4, q=1e-9: positive, minimum ratio=.98981175616.

The negatives persist at 80 digits, with inverse-forward L1 errors about 1e-80. They explicitly falsify an unrestricted-noise reading. At beta=2,q=1e-5 the double-precision test is positive. Files: test_calibrated_terminal_inverse.py, calibrated_terminal_inverse_results.json, test_calibrated_inverse_highprecision.py, calibrated_inverse_highprecision_results.json.

## Sources and originality boundary

- van Enter, Fernandez, den Hollander, Redig, arXiv:math-ph/0105001, https://arxiv.org/pdf/math-ph/0105001 : parent identified Section4's forward-noise error-island expansion. The signed backward-noise positivity step and constrained syndrome/logical-prefix interface here require their own argument; no claim of inventing error-island expansions is made.
- Mann and Minko, *Algorithmic Cluster Expansions for Quantum Problems*, https://arxiv.org/abs/2306.08974 and https://doi.org/10.1103/PRXQuantum.5.010305 : bounded-degree/rank polymer-cluster enumeration and log-partition approximation framework. It supports computation of the small signed-cluster correction, not automatic sampling of a signed law.
- Helmuth, Perkins, Regts, *Algorithmic Pirogov-Sinai theory*: standard zero-free polymer algorithm machinery; the actual constrained trace representation and soft-interaction sampler binding are separate obligations.
- Bombin et al., https://arxiv.org/pdf/0907.5228 : established sudden-noise thermal logical robustness. The exact prefix-inverse identity here is used to avoid asserting that an arbitrary noisy Gibbs perturbation is stationary or lies in an invariant local-stochastic cone.

Status: candidate mechanism with explicit positivity, prefix logical lift, and sampler derivation, awaiting independent audit. It is not a claimed completed robust physical loader for generic noise or generic H.

## Addendum: exact necessary population-floor bound

The small-noise/temperature tradeoff is not only a sufficient-cluster-bound artifact. Since all syndrome channels commute, place any C_i last. Its input distribution is nonnegative if a positive precompensation exists. For the pair s,s+d_i, the last binary channel gives output values (1-q_i)a+q_i b and q_i a+(1-q_i)b with a,b>=0. Hence their ratio lies between q_i/(1-q_i) and its reciprocal. Exact Gibbs output therefore necessarily requires

 q_i <= 1/[1+exp(beta max_{s valid}|E(s+d_i)-E(s)|)].

This is an exact necessary condition for positive precompensation for that factor. Multiple-site consistency may impose stricter conditions. It makes the same-resource comparison particularly important: there is no reason to infer a favorable operational threshold from existence of this calibrated mechanism.
