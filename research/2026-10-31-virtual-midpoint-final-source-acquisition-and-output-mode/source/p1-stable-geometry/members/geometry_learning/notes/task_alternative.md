# Task-first alternative: endpoint knowledge versus temporal tasks

31 October 2026. Independent mathematical investigation for the next cumulative-intelligence construction.

## Result and decision

A small, fully explicit counterfixture separates three questions that should not be conflated:

1. Is the retained representation small and stable?
2. Does the actual acquisition interface identify the operations needed by the future task?
3. What is the physical cost of acquiring the missing operation?

The fixture has a two-dimensional endpoint model with a perfectly stable Euclidean realization. Adding the constant gives a three-dimensional space that is already invariant under both transition and observation multiplication. Nevertheless, every possible endpoint-return experiment has the **same complete distribution in two different sources**, while the probability of three successive positive observations differs.

Allowing intermediate observations repairs the information deficit. In a supplied two-model family with scalar parameter c known, the missing operation coefficient is a single sign. Its optimal acquisition cost is

    Theta(c^(-4) log(1/delta))

physical transitions, even for adaptive learners that retain every observed label, choose arbitrary episode lengths, and restart from the true stationary distribution. A simple triple-product estimator attains this rate. Thus the extra cost is real observability cost, not a bad coordinate system or an inefficient learner.

This is a decisive obstruction to promoting endpoint Gram knowledge into a reusable temporal-event model. It is **not** a new general predictive-multiplication mechanism: Astra N1251 and established observable-operator models already supply that mechanism. It is also not an architecture-specific advantage or a general model-acquisition theorem. Its best role is a clean task gate and an acquisition-cost stress test for the root construction.

## 1. Future task and honest source

The future task is to calculate

    p = Pr(Y_0 = Y_1 = Y_2 = +1),

where Y is a binary observation of a stationary hidden reversible Markov chain. This is the smallest nontrivial temporal conjunction, and a simple building block of finite-horizon monitoring and reliability calculations.

The initial source interface permits independent episodes started from the actual stationary distribution. During an episode, the learner executes the one available transition kernel an arbitrary number n of times and receives only the initial and final binary observations, or their product. Every transition and every stationary preparation is charged. This is exactly sufficient for all one-control scalar Gram returns

    <K^u f, K^v f>_pi = <f, K^(u+v) f>_pi.

No hidden state is exposed, copied, or reset to a selected microscopic state. Each endpoint episode terminates without a handle to continue that same hidden trajectory through another observed endpoint call. If consecutive calls can continue the same hidden trajectory and expose their shared endpoint labels, that capability already supplies intermediate observations, and the endpoint impossibility does not apply to it. The endpoint lower bound allows the learner the full pair of endpoint labels within each reset episode, which is stronger than returning only their product.

The proposed repair is a different, explicitly richer interface: the learner may record the label at every intermediate step. This is a new physical observation capability; it is not manufactured by postprocessing endpoint data. Resets still prepare only the genuine stationary distribution.

## 2. Four-state construction

Fix 0 < c < 1/8. Let

    pi = (1/4, 1/4, 1/4, 1/4),
    f  = (1, 1, -1, -1)^T,
    g  = (1, -1, 0, 0)^T,
    h  = (0, 0, 1, -1)^T,
    J  = (1/4) 1 1^T.

Define two transition kernels

    K_+ = J + c(f g^T + g f^T),
    K_- = J + c(f h^T + h f^T).

Both matrices are symmetric and row-stochastic. Every entry is at least 1/4 - 2c > 0. They are therefore irreducible, aperiodic, and reversible for the same full-support pi. Both are contractions on L2(pi). The visible observation is Y_t = f(X_t).

For the concrete rational case c = 1/10,

    K_+ = (1/20) [[9,5,3,3],
                  [5,1,7,7],
                  [3,7,5,5],
                  [3,7,5,5]],

    K_- = (1/20) [[5,5,7,3],
                  [5,5,7,3],
                  [7,7,1,5],
                  [3,3,5,9]].

The smallest transition probability is 1/20; there is no inaccessible microscopic component.

Write v_+ = g, v_- = h, and sigma = +1 or -1. Direct calculation gives

    K_sigma f = 4c v_sigma,
    K_sigma v_sigma = 2c f,
    f .* v_sigma = sigma v_sigma.

Here .* is pointwise multiplication.

## 3. All endpoint transcripts are exactly indistinguishable

For every nonnegative integer r,

    E_sigma[Y_0 Y_(2r)] = (8c^2)^r,
    E_sigma[Y_0 Y_(2r+1)] = 0.

Proof: K_sigma^2 f = 8c^2 f, <f,f>_pi = 1, and <f,v_sigma>_pi = 0.

Each stationary Y_t is uniformly distributed on {-1,+1}. Consequently the **complete endpoint-pair distribution** at lag n is

    Pr_sigma(Y_0=s, Y_n=t) = (1 + st mu_n)/4,

where mu_n is the common correlation above. The distribution is independent of sigma, not merely its first moment.

This remains true under any adaptive sequence of endpoint experiments. Conditional on a common prior transcript, both worlds induce the same distribution for the learner's next chosen lag and its endpoint observations. Induction gives identical full transcript laws. Internal randomization, arbitrary retained memory, unbounded arithmetic, infinitely accurate moment estimates, and arbitrarily long endpoint episodes do not help.

The statement also holds if constants and the readout 1 are included: all additional constant/mean correlations are identical.

## 4. The temporal task differs

Reversibility gives

    E_sigma[Y_0 Y_1 Y_2]
      = <K_sigma f, D_f K_sigma f>_pi
      = sigma 8c^2,

where D_f multiplies a function by f. Since

    1_{Y=+1} = (1+Y)/2,

expanding the three factors yields

    p_+ = 1/8 + 2c^2,
    p_- = 1/8.

For c=1/10, these probabilities are 29/200 = 0.145 and 1/8 = 0.125.

**Endpoint impossibility theorem.** For any epsilon < c^2, no learner using only the endpoint interface can estimate p to additive error epsilon with success probability greater than 1/2 in both worlds. The good-output intervals are disjoint, while the output distribution is identical. The same argument permits no uniformly valid relative error below

    (p_+ - p_-)/(p_+ + p_-) = 8c^2/(1+8c^2).

At c=1/10 this threshold is 2/27, approximately 7.4 percent. This obstruction persists after literally unlimited endpoint acquisition. It is not a sample-complexity statement about a weak baseline.

## 5. Perfectly stable coordinates do not repair missing information

Let a = 2 sqrt(2) c and q_sigma = sqrt(2) v_sigma. Then (f,q_sigma) is an orthonormal basis for the endpoint-reachable space, and both endpoint models have the same matrix

    K_endpoint = [[0,a], [a,0]].

Its Euclidean operator norm is a < 1. The raw word basis (f,Kf) has Gram matrix diag(1,a^2). Whitening produces exactly the displayed stable model in both worlds. At c=1/10 the raw condition number is only 12.5.

Adding the constant gives the orthonormal basis (1,f,q_sigma), in which

    K = [[1,0,0],
         [0,0,a],
         [0,a,0]],

    D_f = [[0,1,0],
           [1,0,0],
           [0,0,sigma]].

Within each world, its three-dimensional feature space is invariant under both operations. The displayed abstract transition matrices coincide, while the observation matrices differ only in sigma. Both operators have Euclidean norm at most one. Thus even **dimension growth is unnecessary**: the missing information is a coefficient of the observation multiplication operator on an already acquired direction. K alone does not determine it.

This does not contradict N1251, which explicitly acquires observation multiplication or makes a label-local dictionary. It illustrates why that premise cannot be dropped or inferred from transition closure.

## 6. Paid repair: upper bound

For the upper bound, supply the two-model family above and the value c. Only sigma is unknown. This is a stronger structural promise than generic model learning and is stated openly.

Run independent stationary two-transition episodes and record all three labels. For episode i retain

    R_i = Y_0 Y_1 Y_2 in {-1,+1}.

Its mean is sigma 8c^2. Choose the sign of the sample mean, breaking a zero tie arbitrarily. Hoeffding gives

    Pr(wrong sign) <= exp(-32 n c^4).

It suffices to use

    n = ceil(log(1/delta)/(32c^4))

episodes. The physical bill is n genuine stationary preparations, 2n kernel transitions, and 3n label readings. If preparation and reading costs are C_prep and C_read, the acquisition bill is

    n (C_prep + 2 C_transition + 3 C_read).

Computation uses O(n) additions of one-bit signs and an O(log n)-bit counter; the reusable model choice is one bit. All previous endpoint acquisition, if performed, remains an additional sunk cost.

No inverse Gram matrix is needed by this optimal fixture-specific experiment. Normalizing the small mode in a representation does not amplify the observed signal in a physical episode.

## 7. Matching lower bound for complete adaptive record learners

The lower bound grants the richer interface from the outset: every intermediate label may be recorded, episode lengths may be chosen adaptively, and the full history may be retained. It therefore applies to optimal likelihood, model-based, spectral, Bayesian, or other retaining learners.

For a fixed world sigma and a visible history ending in Y_t, let alpha_t be the conditional hidden-state law and define

    F_t = alpha_t f = Y_t,
    G_t = alpha_t v_sigma.

For a fresh stationary episode, G_0=0 after the first visible read. Direct summation of the transition probabilities gives

    Pr_sigma(Y_(t+1)=s | history) = 1/2 + 2c s G_t.

The filtering update is

    G_(t+1) = 0,                              if s != sigma,
    G_(t+1) = 4c Y_t/(1 + 4c sigma G_t),      if s = sigma.

The invariant bound |G_t| <= 8c follows by induction. Indeed, if |G_t| <= 8c, the denominator has magnitude at least 1-32c^2 > 1/2, so the next nonzero G has magnitude at most 8c.

Compare both models on the **same observed history**. If the final label is +1, G_t is zero in the minus world; if it is -1, G_t is zero in the plus world. Therefore one model's next-plus probability is exactly 1/2 and the other's differs from it by at most 16c^2. Both next-plus probabilities belong to [1/4,3/4].

For Bernoulli probabilities p,q, the elementary inequality

    KL(Ber(p) || Ber(q)) <= (p-q)^2/[q(1-q)]

therefore yields, in either direction,

    one-transition conditional KL <= (4096/3)c^4 < 2048c^4.

The initial stationary label has the same law in both worlds. Reset decisions, episode-length decisions, internal randomness, and other learner computations introduce no additional source information. By the KL chain rule, an adaptive transcript using N actual transitions satisfies

    KL(P_+ transcript || P_- transcript) <= 2048c^4 E_+[N].

The same bound holds in the reverse direction. A randomized stopping time with finite expected N is covered by truncation; recording only selected labels cannot increase KL by data processing.

Any output that distinguishes the worlds with error at most delta < 1/2 must satisfy

    KL(P_+ transcript || P_- transcript)
        >= kl(1-delta, delta)
        = (1-2delta) log((1-delta)/delta).

Consequently,

    E_+[N] >= kl(1-delta,delta)/(2048c^4),

and likewise under the other world. For delta <= 1/4 this is Omega(c^(-4) log(1/delta)). Together with the two-transition estimator, this proves the claimed optimal transition order.

It also proves the lower bound for the temporal probability task whenever its required additive accuracy is below c^2, because thresholding the estimate at 1/8+c^2 distinguishes the worlds.

The constants are deliberately conservative. The theorem concerns transition counts. Arbitrarily expensive stationary preparation can change which episode schedule minimizes total weighted runtime, but it cannot remove this transition lower bound. The simple upper bound explicitly retains preparation cost instead of assuming it is free.

## 8. Reuse and the strong ordinary comparator

Once sigma is correctly acquired within this **known two-model family**, the kernel is known exactly, because c and the two candidate descriptions were supplied. Every later binary record probability can then be evaluated by matrix multiplication without further source episodes. A deterministic finite-state monitor with q states and horizon L can be evaluated by a forward recursion on the four hidden states and q monitor states in O(Lq) fixed-precision arithmetic operations. The total future description and execution work is paid for each requested monitor; outputting the whole exponential record table is not called cheap.

If c is a supplied rational and exact probabilities are wanted, numerator bit length grows O(L times the coefficient bit length); the bit arithmetic must be charged. If c is an unknown continuum parameter, finite noisy data do not acquire an exact model, and unbounded-horizon exact reuse is unavailable. The sign-learning theorem is not a license to omit that precision cost.

An ordinary retaining hypothesis-testing or likelihood learner uses exactly the same triple experiment and attains exactly the same lifetime bill. There is no defensible separation from a strong retaining learner. The demonstrated phenomenon is that a specifically acquired missing operation can unlock future tasks, while the exact acquisition interface and signal strength determine whether doing so is economical.

For the broader program, this fixture should be used to reject any claim that stable endpoint coordinates alone provide arbitrary temporal, conditional, or reactive computations. It should not replace a positive construction with an artificially restricted baseline.

## 9. Relation to existing sources actually read

Read the complete reviewed Astra N1251 operation-algebra source:

https://github.com/harjassand/astra-research-knowledge/blob/ceaef853be46099e0e3446d0778160f26ef962fe/research/2026-10-29-controlled-preparation-and-learning-returns/source/p1-acquired-cancellation/new_science/alternative_frontier/reviewed_versions/ACTUAL_OPERATION_ALGEBRA_d45b664203b4.md

It already constructs actual chronological weighted moments, separately requires visible multiplication closure, and obtains complete visible-program laws when those operations are acquired. Its finite-kernel version explicitly retains horizon factors and scope limitations.

Read complete ROOT_REVIEW_AND_CORRECTIONS.md at the same revision:

https://github.com/harjassand/astra-research-knowledge/blob/ceaef853be46099e0e3446d0778160f26ef962fe/research/2026-10-29-controlled-preparation-and-learning-returns/source/p1-acquired-cancellation/new_science/ROOT_REVIEW_AND_CORRECTIONS.md

Its correction 2 explicitly separates pulse closure from label multiplication closure. The text credits the predictive-multiplication obstruction as an existing root construction. Therefore no general novelty claim is made here.

Also read complete FINITE_PULSE_CAUSAL_CLOSURE.md at the same revision, especially the separate observation-projector defects and its explanation that missing multiplication operations, rather than microscopic states, are acquired:

https://github.com/harjassand/astra-research-knowledge/blob/ceaef853be46099e0e3446d0778160f26ef962fe/research/2026-10-29-controlled-preparation-and-learning-returns/source/p1-acquired-cancellation/new_science/FINITE_PULSE_CAUSAL_CLOSURE.md

Established primary literature:

- Herbert Jaeger, A short introduction to observable operator models of stochastic processes (1998), https://www.ai.rug.nl/minds/uploads/jaeger.98.emcsr.pdf. Read the operator construction and probability formula; observation-specific operators are the standard way to represent complete sequence probabilities.
- Daniel Hsu, Sham Kakade, Tong Zhang, A Spectral Algorithm for Learning Hidden Markov Models (COLT 2009), https://www.learningtheory.org/colt2009/papers/011.pdf. Read the model and source definitions, comparison with OOM/PSR, and spectral-identification conditions. The paper is a strong ordinary comparison, not a free generic learner for arbitrary weakly observable sources.

Neither the retrieved source material nor the finite computation below establishes historical novelty of this particular four-state fixture or the KL argument.

## 10. Executed verification and scope

Own check script: check_task_alternative.py.
Output: task_alternative_checks.json.

The script uses exact rational arithmetic for c in {1/10,1/16,1/32}. It checks stochasticity, strict positivity, reversibility, the two invariant-space identities, all endpoint correlations through lag 24, all length-three probabilities, and filtering identities for every binary history through length eight. It separately evaluates the numerical conditional-KL ratio; the largest checked ratio KL/c^4 was below 185, within the analytic bound 2048.

The all-lag indistinguishability and arbitrary-history lower bounds follow from the proofs above, not from finite enumeration. No physical samples were acquired. No original producer scientific programs were run. No external communication or publication occurred.
