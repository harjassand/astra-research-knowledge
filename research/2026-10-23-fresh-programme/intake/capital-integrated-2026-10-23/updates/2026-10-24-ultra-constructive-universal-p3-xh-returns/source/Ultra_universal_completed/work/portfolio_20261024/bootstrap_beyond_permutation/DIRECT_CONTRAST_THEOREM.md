# An acquired nonselective preparation from noisy experiment contrasts

24 October 2026. The owned question and observable representation were saved in `FIRST_CONSTRUCTION.md` before peer exposure. This construction replaces the initially contemplated full-operator fit by a directly estimable contrast. It is separate from the earlier quadratic-permutation acquisition theorem and from the previous predictive-depth experiments.

## Supplied apparatus and acquired information

There is a stationary controlled stochastic process. Each primitive action has a finite visible outcome alphabet. All action/outcome histories, their conditional future experiments, and their nonselective mixtures belong to one linear observable process whose **full controlled Hankel rank is at most two**. This is an architecture promise, not something inferred from nine frequency cells. It includes all legal observation-conditioned histories, not merely the marginal open-loop sensor sequence. The empty event has probability one. Loss, termination and timing observations must be included in the specified interface or excluded by an explicit apparatus contract.

The learner is supplied: that rank upper bound; a reproducible initializer of the entire relevant process at cost C_init; legal primitive controls and their costs/durations; a finite declared preparation/control library; and independent initialized Bernoulli trials of declared event settings. It receives integer outcome counts, not exact probabilities, hidden states, transition matrices, a coordinate map, a reset control, a stationary sampler, or an equivalence oracle. The initializer is used and paid during acquisition. A conditional reset below becomes usable only after this acquisition succeeds.

Choose one legal binary continuation event G. Let p(rho)=Pr(G|rho). Actual nonselective preparations P_i from the initializer, and actual nonselective controls u in a finite library U, are measured through

    p_i = Pr(G | P_i rho0),
    q_iu = Pr(G | u P_i rho0).

Order here is chronological: P_i, then u, then G. Outcomes inside a nonselective preparation/control are discarded; G alone contributes the observed bit. No postselection is free. Every episode pays its initializer, all controls, and all outcome production/readout.

## Exact rank-two theorem

Suppose two actual preparations P_0,P_1 have g=p_1-p_0 != 0. The two test coordinates (1,p) are independent on these preparations. Together with the supplied rank upper bound, this exhausts the complete observable quotient. Consequently:

1. For every legal nonselective word u there are real constants b_u,d_u with p(u rho)=b_u+d_u p(rho) for every reachable conditional physical state rho.
2. Every event E in any finite legal future protocol, including an observation-adaptive protocol, has probability a_E+c_E p(rho).

These are linearity statements on the complete quotient. To see completeness directly, take the two tests [empty,G] and the two actual preparation rows. Their Hankel block is [[1,p_0],[1,p_1]], of determinant g. A nonsingular block of size equal to a valid rank upper bound is complete. Each future event is a linear functional on this space. Finite adaptive-event trees are sums of controlled action/outcome-word effects in the promised interface, so the same representation holds. We do not infer completeness from a small empirical minor without the rank promise.

The acquired control contrasts satisfy

    Delta_u = q_1u-q_0u = d_u g.

For any positive mixture lambda in the probability simplex on U, let S mean sampling u with fresh randomness and executing it nonselectively. Its slope is

    d_S = (sum_u lambda_u Delta_u)/g.

For a future event E, its probabilities on the two actual preparations are in [0,1]. Therefore |c_E g| <= 1. For any two reachable conditional physical inputs rho,rho', their coordinates p,p' are in [0,1]. It follows that

    |Pr(E | S rho)-Pr(E | S rho')|
      = |c_E d_S (p-p')|
      <= |sum_u lambda_u Delta_u| / |g|^2.             (1)

The bound is uniform in the input history, future horizon, common future policy, and future transcript event. Thus it bounds the total variation distance between the two **visible future transcript laws** for every such policy, with TV defined as sup_E |P(E)-Q(E)|. There is no factor for the number of future outcomes and no accumulation with the future horizon. In particular, exact contrast cancellation is an exact reset in this observable quotient, even if each individual word preserves memory.

For a countably infinite continuation under a common measurable causal policy, the same bound applies to every finite restriction. It then applies to the full trajectory laws: each measurable event can be approximated in measure by finite-coordinate events under the sum of the two laws. This uses the ordinary product sigma-algebra of the specified finite-alphabet interface. It makes no claim about unmodelled environmental records.

The factor |g|^-2 is a sound outer bound, not an assertion of tightness. A better acquired enclosure of physical coordinates or effects could improve it. A vanishing gap makes the certificate fail rather than granting a latent reachability oracle.

## Finite counts, adaptive selection, and finite precision

Declare M scalar probability settings in advance and take N independent fully initialized Bernoulli samples per setting. On the simultaneous confidence event

    |p_ihat-p_i| <= w,  |q_iuhat-q_iu| <= w,

whose failure probability is at most alpha=2 M exp(-2 N w^2), one may choose the preparation pair and any positive mixture from those same counts. For the chosen pair define

    g_lower = |p_1hat-p_0hat|-2w.

If g_lower <= 0 return UNKNOWN. Otherwise true g is nonzero and exhausts rank. Let Deltahat_u=q_1uhat-q_0uhat. For the **actually implemented** nonnegative weights, positivity gives

    |sum_u lambda_u Delta_u|
      <= |sum_u lambda_u Deltahat_u| + 2w.

Combining this with (1) yields the computable certificate

    epsilon = min(1,
       (|sum_u lambda_u Deltahat_u|+2w)/g_lower^2).   (2)

No extra multiple-comparison penalty is needed after the simultaneous event: it already covers all declared cells, and the positive mixture cannot amplify their worst error. Selecting unmeasured settings would require a new confidence allocation. If the library has no useful positive cancellation, or the bound is vacuous, the routine returns UNKNOWN for the requested tolerance; it does not certify nonexistence of another reset.

For two macros with observed contrasts of opposite signs, the zero-residual weight is exactly -Deltahat_b/(Deltahat_a-Deltahat_b). Counts are integers, so this is a rational of finite bit length. An implementation can round it to m/2^B and draw exactly B fresh fair bits. In (2), use the resulting dyadic weights and their actual residual. This pays and certifies the finite-precision approximation directly; there is no exact-real computation or rejection-time side channel hidden in sampling.

All sample counts, durations, memory, bit operations and confidence allocations are finite. For fixed bounded preparation/control/test lengths and a true basis gap bounded below by g0, a zero-fit residual yields the sufficient scaling N=O(epsilon^-2 g0^-4 log(M/alpha)) per cell. This is not a uniform completeness result from rank alone. The supplied rank bound can be wrong; this protocol does not certify it against arbitrary higher-rank alternatives. Rare reachable directions can make useful finite-noise certification arbitrarily costly.

## Repetition uses the acquired contraction, without new calibration

The same simultaneous event certifies the scalar slope directly:

    |d_S| <= eta = (|sum lambda_u Deltahat_u|+2w)/g_lower.

If eta<1, executing k copies of the SAME fitted nonselective mixture with independent private keys implements S^k. Its true scalar slope is d_S^k, even though the same estimated coefficients and confidence event are used in every copy. There is no repeated model-estimation error to add. The argument for (1) therefore yields

    epsilon_k = min(1, eta^k/g_lower).                 (4)

This bounds all visible future-event differences between any two inputs after S^k, including comparison to the actual physical target S^k(rho0). The finite-k target is different from S(rho0); do not use k=1 reference probabilities to score k>1 data. Each copy pays one actual macro, B fresh selection bits, its produced outcomes and private record handling. With the executed one-step library, the public completion time is exactly k and does not depend on the sampled words. The confidence bound for every k follows on the same calibration event, so data-dependent choice of k adds no calibration union penalty.

Repetition and contraction amplification are established operations in approximate-homing theory. The contribution here is the paid finite-count bound on the contraction, which makes a stopping depth quantitative. The saved experiment executes k=1 only; equation (4) is a proved composition corollary, not an executed k>1 test or a measured hardware speedup.

## Exactly which record is reset

The probability mixture S is a **nonselective preparation**. Its contract supplies a fresh private random key independent of the input process and past learner history. The reset controller does not release its chosen word, key, reset readouts, or any other component-dependent record to the next experiment. The reset finishes at a common public time. The physical apparatus must isolate/dispose of those records and must charge randomness, control, record handling and elapsed time. The source code is a statistical fixture; it is not a demonstrated entropy source, constant-time hardware implementation or thermodynamic erasure mechanism.

For the executed library below, a and b are genuine legal actions of equal duration one. No idle or padding is assumed. Fixed B-bit selection is part of the isolated controller contract. Retaining the sampled word can invalidate the conclusion completely: the half identity/half swap mixture resets a hidden binary state marginally, but the pair (word, future state test) still reveals the input state. If the continuation can condition on the word or a timing leak, conditional reset of every supported word is required instead. Equation (1) deliberately concerns the accessible future interface after nonselective preparation.

## What subsequent learning receives

Let rho_star=S(rho0), an actual physical preparation whose hidden description and future event probabilities need not be known. Equation (2) bounds future-event differences between S applied to any reachable conditional input and rho_star. This acquires a new reproducible preparation for a **new task initialized at rho_star**. It does not substitute for rho0 in a task requiring the original initial distribution. That requires an additional target-matching certificate, not supplied here.

Fix any newly chosen future protocol/event E before its evaluation block, possibly chosen using all previous acquired information. Let p_star=Pr(E|rho_star). Before each of N later trials, apply a fresh private S to the currently retained process state, then perform E and record its bit Y_i. Condition on the acquired calibration data, a true confidence event, and the entire accessible past. Uniformity gives

    |E[Y_i | past]-p_star| <= epsilon.

The bounded martingale differences Y_i-E[Y_i|past] obey the martingale Hoeffding bound, so

    Pr(|mean(Y)-p_star| > epsilon+tau) <= 2 exp(-2N tau^2). (3)

This proof does not call the trials iid and does not claim their joint law is within epsilon of an iid law. Their hidden memory may remain correlated, and N-trial joint errors can accumulate. For K fixed evaluation blocks use a union bound. If a future program is selected after observing its own evaluation outcomes, a separate adaptive inference rule is needed. The program may use arbitrary within-trial feedback covered by the controlled interface.

## Paid acquisition and the strongest ordinary control

An equally informed conventional controller can estimate the same two preparation contrasts and use the same positive mixture and certificate. That controller ties this operation. Full OOM reconstruction or hidden-state maximum likelihood is unnecessary in rank two; the direct contrast is the stronger simple incumbent. A controller supplied the true latent matrices has a different access model. A system-ID method learning from a single mixing trajectory can also be preferable for particular future tasks; the present result does not assert that all learning needs repeated preparations.

Let C_A be the full paid acquisition cost and C_S the per-use private nonselective preparation cost. For the **same new reference task**, the exact-repeat baseline applies the external initializer and then the same S, at cost C_init+C_S per trial. The acquired approximate preparation costs C_S, with the certified bias in (3). Break-even against that baseline requires T*C_init > C_A, after including every noncommon computation/entropy/record cost and a common requested accuracy. If the reset bias forces more later samples, that extra cost must be included too. If an exact target or tolerance below epsilon is required, this finite certificate does not replace the initializer.

More explicitly, for K future event probabilities at error allowance A>epsilon and sampling confidence beta, sufficient per-event counts are n_S=ceil(log(2K/beta)/(2(A-epsilon)^2)) for acquired preparation and n_0=ceil(log(2K/beta)/(2A^2)) for exact external initialization followed by S. If one event protocol costs C_E, the matched costs are C_A+n_S(C_S+C_E) and n_0(C_init+C_S+C_E) per new event task, with acquisition charged once over many tasks. Ignoring ceiling differences, replacement has positive lifetime savings only if n_0 C_init > (n_S-n_0)(C_S+C_E). Repeating enough tasks then amortizes C_A. A comparison that charges both methods n_S trials merely because that was the executed evaluation budget can overstate savings.

This theorem is a positive acquired-experiment operation conditional on a rank bound, successful measured gap, a useful finite library, and a private nonselective controller. It is not an advantage theorem over the same-data conventional controller, a general reset-free system learner, a priority claim, or physical validation.
