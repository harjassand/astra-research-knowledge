# Whole analytic receipt: calibrated terminal-noise thermal loader

2026-11-01. **PASS of the conditional analytic construction**, retaining the explicitly supplied actual decoder-trace bijection and original witness theorem as inputs. This is not acceptance of generic noisy encoding, a noncommuting interacting-Gibbs loader, or a practical threshold. The sampler's actual signed-potential premises are checked here rather than inherited from the earlier conditional sampler receipt.

## 1. Inverse law, uniform positivity and potential

The inverse of (1-q)I+qF for an involution F is ((1-q)I-qF)/(1-2q). Physical Pauli syndrome translations commute and preserve the complete constrained valid-syndrome space, redundant coordinates included. Expanding their product gives the candidate's signed subset formula with r=q/(1-q). Every inverse preserves mass because the original channel and its inverse have left eigenvector one. Thus normalization is exact independently of positivity.

If two selected label components have disjoint affected-check sets, their energy increments add, including on invalid bitstrings used only as auxiliary local arguments. The signed hard-core error-island representation is therefore exact. An affected check may flip several times inside a component; bounding the total possible energy change by B times the number of labels remains valid despite cancellations. Hence the uniform activity bound u^|gamma| is correct.

Bounded overlap supplies bounded graph degree and a bounded number of fault labels touching each check. With u sufficiently small and a strict spare-exponential margin, the displayed anchored incompatibility sum implies the conventional absolutely convergent connected-cluster expansion, uniformly in the syndrome and every deleted-label subset I. The same criterion holds throughout real scaling of the signed activities from zero. The finite partition function starts at one, stays real, and cannot vanish, so Z_I(s)>0. This is a genuine size-independent positivity argument, not finite-volume continuity alone. Consequently every pi_I is positive and normalized.

For clarity, the cluster absolute majorant can be chosen independently of s: take the absolute Ursell coefficient times the product of u^|gamma|. Anchoring a cluster touching check a at one of its boundedly many adjacent fault labels gives an O(u) rooted sum. Its dependency size is at most a fixed constant times total polymer-label multiplicity. The spare exponential absorbs that factor and further exponential tail weights. Thus the claimed bounds on sum sup_s|phi_C| and sum |A_C|sup_s|phi_C| really follow uniformly; this does not interchange a supremum with an uncontrolled cancellation. The local increment and mixed-difference estimates then follow termwise. These are precisely the actual premises needed by the previously audited positive interacting sampler.

## 2. Every prefix and the logical lift

For any I, constants independent of s cancel in pi_I(s)/pi_I(s'). The anchored potential bound changes the original erasure energy penalty only by kappa times the number of changed check coordinates. At a strict Peierls margin the original witness injection and entropy bound therefore apply uniformly in I. For the enlarged bad set, also use the general ratio bound for bounded-weight syndrome translations; the witness-removal-only special case would not itself prove this enlargement.

Starting at pi_pre and applying the terminal channels in a fixed order leaves exactly the inverse law for the remaining labels after every prefix. These prefix identities are on distributions, not merely formal densities. Faults are independent of syndrome and input by the model's explicit assumption.

On a good current syndrome, the admitted local Pauli preserves the full decoded logical algebra. Telescoping along a history with no bad prefix yields the final decoder representative acting on the original logical input, up to an irrelevant scalar phase. Each prefix marginal has bad probability at most b_n, so union bound gives at most M b_n for any logical-frame failure. This does not presume independence of the bad-prefix events.

The final syndrome marginal is exactly pi regardless of history. On good histories the conditional logical channel is identity; on the remaining histories it is a logical Pauli channel. Replacing those remaining outputs by the ideal logical output costs at most twice their total probability, even for arbitrary entangled references. The full reference-safe output error <=2M b_n is therefore correct. Final Gibbs syndrome agreement alone would not have implied this result; the prefix argument is essential.

An initial syndrome-sampler TV error epsilon changes the full quantum preparation by at most 2epsilon, and common subsequent channels contract that discrepancy. The supplied encoded input must initially be independent of the sampled randomness and faults except through the prescribed preparation. Any error in that supplied input is a separately charged additive term.

## 3. Positive trace sampler binding

Taking the parent's trace bijection, disjoint top supports, bounded-degree finite host and low-temperature weight bound as explicit inputs, pi_pre indeed maps to a positive trace law product w_gamma times exp(Phi). The positive interacting birth/death sampler from the earlier receipt applies with anchored potential strength K_1 u and appropriately enlarged birth envelopes.

Its soft-influence contraction term is controlled by the actual O(u) anchored second moment just derived. Its hard-core term is small at sufficiently low fixed temperature by the rooted trace activity moment. One must choose temperature with BOTH the witness margin and the trace-sampler contraction margin, then choose q small relative to that fixed temperature. No signed probability law is sampled, and no exponentially small global rejection acceptance is used.

The dictionary truncation tail follows by deletion/insertion pairing: inclusion probability <= envelope activity. Potential truncation preserves an absolute anchored moment because it discards a subset of the original cluster terms. Uniform potential error controls TV after normalization. These arguments cover the actual soft interaction rather than incorrectly invoking a factorized-gas sampler unchanged.

## 4. Explicit exp(O(L)) evaluation, avoiding the cluster-partition complexity gap

A bare instruction to enumerate all partitions or multisets of size L is NOT a polynomial-time justification: naive partitions can cost exp(O(L log L)). The following elementary alternative closes the needed evaluation step without relying on an unverified attribution to Mann–Minko.

Introduce one common formal fugacity z multiplying each r_i. For a subset U of fault labels define

    Z_U(z;s)=sum_{F subset U} z^|F| product_{i in F}(-r_i)
                    exp[-beta(E(s+d_F)-E(s))].

Its constant term is one. Let g_U(z;s) be its formal logarithm truncated through degree L, computable by the usual formal-series recurrence in polynomial(L) operations once Z_U's coefficients are known. Set

    h_T(z;s)=sum_{U subset T} (-1)^(|T|-|U|) g_U(z;s).

This is support-Mobius inversion: h_T contains precisely the logarithmic monomials whose set of used labels is exactly T, including arbitrary repeated uses. Every such monomial has degree at least |T|. If T is disconnected in the affected-check graph, Z_U factors over the graph components for every U and its formal logarithm is additive, so h_T vanishes identically. Therefore

    [log Z_I(z;s)]_(degree<=L)
       =sum_{T subset I, T connected, 1<=|T|<=L} h_T(z;s).

Evaluate at z=1. The truncation is EXACTLY the cluster expansion cut at total polymer-label multiplicity L, so the previously earned uniform tail and influence estimates apply even though this is a different computational representation.

There are M exp(O(L)) connected label supports T in a bounded-degree graph, with a standard rooted connected-set enumeration. For each T, evaluating Z_U for all U subset T by enumerating F subset U costs at most 3^|T| times polynomial(L) local operations; formal logarithms and the Mobius sum add at most 2^|T| polynomial(L). Hence total evaluation costs M exp(O(L)) polynomial(L), not exp(O(L log L)). For L=O(log(n/epsilon)) this is polynomial in n/epsilon at fixed graph and convergence constants. Re-evaluating globally for each proposed birth still yields polynomial runtime; sophisticated local updates are unnecessary for the existence result.

Strict absolute convergence also supplies a complex fugacity disk of radius R>1 and uniform tail O(M R^(-L)); alternatively use the explicit spare exponential cluster weight. Rational/arithmetic approximations to the computable q_i, beta and J_a can be carried with polynomially many bits. The subset sums and formal-series recurrence involve only polynomially many arithmetic operations in n/epsilon and bounded-degree-L coefficients; conservative exp(poly(L)) conditioning bounds require only poly(L,log(n/epsilon)) guard bits. These evaluations are used to produce a positive exp(Phi_L) target and clipped [0,1] acceptance probabilities, not to sample the signed island weights.

This explicit support-Mobius method supplies the candidate's needed constructive evaluation statement. It must be incorporated or an equally precise applicable enumeration theorem supplied; the citation alone was not independently verified in this receipt.

## 5. Finite chain and numerical budgets

For the truncated trace dictionary, its size is polynomial if the assumed typed connected candidates and local membership tests have the stated quantitative bounds. Standard self-incompatibility bounds each proposal activity by the hard-core moment constant; otherwise explicitly charge a polynomial total proposal rate. With a fixed contraction margin and O(n) weighted diameter, continuous-time mixing requires O(log(n/epsilon)) time. Uniformization and a Poisson tail cutoff give polynomially many updates. Per-step acceptance error at most epsilon divided by the charged update count gives total variation error at most epsilon by stepwise coupling.

This presumes computable numerical input data and fixed quantitative convergence margins, not arbitrary real-number oracles. These are natural algorithmic inputs, but must stay explicit.

## 6. Calibration and the necessary noise floor

For independent binary Pauli factors, telescoping gives diamond distance between actual and calibrated terminal channels at most 2 sum_i |q_i-qhat_i|. It is applied FORWARD to the already sampled pre-state; no inverse-channel norm amplifies this calibration discrepancy. Build the pre-state with qhat within the proved convergence regime, then charge forward mismatch additively.

Accuracy O(delta/M) per rate suffices for endpoint error O(delta). For one genuinely common stationary iid rate, the stated O(M^2 delta^(-2) log(1/alpha)) Bernoulli samples suffice. For M unrelated rates estimated separately, a conservative total is O(M^3 delta^(-2) log(M/alpha)); it remains polynomial but should not be confused with the common-rate count. Confidence failure adds its own probability/error budget. Drift, state dependence or correlated faults are not covered.

The necessary population-floor inequality is correct. Place one binary channel last; the preceding distribution is nonnegative if any positive precompensation exists. For each nontrivial paired orbit its two outputs have ratio between q/(1-q) and its reciprocal. Substituting Gibbs weights yields q<=1/(1+exp(beta max_valid|Delta E|)). A trivial zero-shift factor only gives the already imposed q<=1/2. This is a necessary, not sufficient, condition. The numerical negatives outside conservative small-u bounds do not contradict the theorem and do rule out an unrestricted-noise interpretation.

## 7. Final scope

The supported result is a calibrated independent TERMINAL-Pauli noisy thermalization stage for a SUPPLIED encoded input and a COMMUTING target, under the inherited actual trace and witness inputs. It does not absorb idle noise during the classical sampling, unknown noise rates, coherent gate faults, arbitrary correlated faults, always-on noncommuting dynamics during the final pulses, noisy initial encoding or preparation of the actual coupled noncommuting Gibbs state. Attaching storage uses a theorem appropriate to the produced commuting target; the exact interacting-bath storage theorem cannot be invoked by swapping its initialization premise.

No fatal analytic obstruction was found within this contract. The computational proof clarification above is substantive and avoids the naive exp(L log L) gap. No source-access workaround, external contact or novelty search was performed; the argument is independently derived from the supplied candidate and previously audited sampler.

## Artifact binding and root computation supplement

Audited candidate SHA256: `363619637af3fb3d3a283ac6f1eb0e636ddaba83353a07b65095dc5d2b5fdb1a`.
Backward-noise gate SHA256: `e0e882bd403b1d9776f85dad56200a15379d956da0a8b69474e0d78145c9de5e`.
Conditional sampler SHA256: `d3c607edd5aa499776bcaeef7f692e38c998f8332adad3d7fdcde59de9989eef`.

The subsequently supplied `ROOT_NOISE_POTENTIAL_EVALUATION.md`, SHA256 `0b64aeadba53cd5a132a9f988f63f4ec8cb65c19d1b4b50d2b22b797983cd1f9`, was read and independently matches Section 4's derivation. **PASS of that supplement.** It closes the enumeration obligation without relying on a Mann–Minko theorem attribution. For an explicit conservative precision estimate, coefficients of Z_A are at most (1+u)^L in magnitude; degree-L constant-term division/logarithm recurrences can be bounded by exp(poly(L)) in magnitude and perturbation amplification. The 3^L subset operation count and number of connected supports add only polynomial(L)+log(N/epsilon) guard bits. Choose arithmetic error independently below the allocated uniform potential/acceptance budget; no exact-real computation is needed.

Parent reports that the actual trace representation now has a separate accepted independent audit. This receipt keeps that geometric/combinatorial representation as its named external input rather than silently re-certifying it. The terminal preparation and attached target in this receipt are V=0/commuting only; source Peierls protection must be enlarged for the stated fixed bounded-support fault-label algebra. The zero-shift case of the population floor imposes no new constraint beyond q<1/2.
