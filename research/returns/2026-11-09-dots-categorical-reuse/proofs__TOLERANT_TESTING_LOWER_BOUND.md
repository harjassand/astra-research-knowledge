# A worst-case expected-query lower bound from tolerant testing

9 November 2026. Analytic reduction only. This note does not change any earlier frozen construction, claim historical novelty, or report an implementation or experiment.

## 1. Contract and result

Fix a known alphabet [d], d >= 2. A universal algorithm receives an actual distinguished X with law P and has independent sample access to P and Q, plus independent internal randomness. It receives no distribution-dependent advice, probability evaluations or shared source seeds. It halts almost surely, preserves the supplied X, and outputs Y with law exactly Q. For every P,Q it promises

    Pr(X != Y) <= TV(P,Q) + eta.

Let C(d,eta) be a finite uniform upper bound on its expected number of NEW source queries, excluding the supplied X. Arbitrary adaptive allocation between sources and unbounded stopping are allowed. Then, for sufficiently small positive eta (an absolute constant range),

    C(d,eta) + 1 = Omega(d / [eta log d] + sqrt(d) / eta).

The implicit constants are inherited from the primary tolerant-testing lower bound. This is a worst-case expected-cost statement. It is not an instance-specific lower bound at P=Q, a numerical call-count certificate, or a lower bound for an algorithm with probability access.

Consequently the reviewed O(d/eta) construction is within a logarithmic factor in d of the optimal worst-case expected query order under this information contract. The reduction does not prove the factor log d necessary or removable. It is independent of the latency/moment obstruction: no exponential-moment assumption is needed here.

## 2. Primary theorem used

Canonne, Jain, Kamath and Li, *The Price of Tolerance in Distribution Testing*, COLT 2022, PMLR 178, pages 573–624. Theorem 3.1 and Corollary 3.2 of arXiv:2106.13414 (Theorem 7 and Corollary 8 on page 10 of the published PDF) state a sample lower bound for distinguishing an unknown P satisfying

    ||P - U_d||_1 <= epsilon_1

from one satisfying

    ||P - U_d||_1 >= epsilon_2,

with success probability at least 4/5. For epsilon_1 < epsilon_2 < c, where c>0 is an absolute constant, the lower bound is

    Omega( [d/log d] {epsilon_1/epsilon_2^2
                       + (epsilon_1/epsilon_2^2)^2}
           + sqrt(d)/epsilon_2^2 ).

Sources inspected on 9 November 2026:

- https://proceedings.mlr.press/v178/canonne22a.html
- https://arxiv.org/html/2106.13414 (Theorem 3.1 and Corollary 3.2)
- https://proceedings.mlr.press/v178/canonne22a/canonne22a.pdf

The paper uses L1 thresholds in the formal theorem. The factors of two in the next section explicitly translate total variation. This note imports the published testing theorem; it does not reproduce its approximation-theoretic proof or claim a new tolerant-testing result.

## 3. Independent repetition turns coupling into testing

Set Q=U_d, which the tester can generate using its own randomness. Let 0<eta<min(c/8,1/8), where c is from the primary theorem. For the unknown P, define

    delta(P) = Pr(X != Y)

for one fresh execution of the hypothetical coupling algorithm. Exact marginals imply the coupling inequality, so

    TV(P,U_d) <= delta(P) <= TV(P,U_d)+eta.

Run t=ceil(64/eta) independent executions. In every execution generate a fresh input X~P; use disjoint fresh source samples and independent internal bits. Let B_j record disagreement. These are independent Bernoulli variables of common mean delta(P).

Declare FAR when sum B_j >= 3 eta t, and CLOSE otherwise. No estimation of P's probabilities is used.

- Under TV(P,U_d)<=eta, delta(P)<=2eta. Stochastic domination and the multiplicative Chernoff bound give

      Pr(FAR) <= exp(-eta t/5) <= exp(-64/5).

- Under TV(P,U_d)>=4eta, delta(P)>=4eta. The corresponding lower-tail bound gives

      Pr(CLOSE) <= exp(-eta t/8) <= exp(-8).

Thus either testing error is less than 1/100 before adding a work cap. The noninteger threshold is interpreted by the exact comparison of the integer sum to the stated real number; rational eta makes the comparison rational. Irrational choices are unnecessary.

## 4. Expected cost can be converted to a fixed sample budget

The expected total number of source draws across the t executions, including all t newly generated distinguished inputs, is at most t(C+1). The uniform reference draws need not count toward an unknown-P testing lower bound, but charging them only makes the reduction more conservative.

Abort the TESTER if this total would exceed

    M = ceil(20 t (C+1)).

On abort it returns an arbitrary fixed answer. Markov's inequality bounds the abort probability by 1/20, separately for every P. Therefore the capped tester has success probability greater than 4/5 under both promises. It uses at most M samples from the unknown P and otherwise only known-distribution randomness. One can equivalently supply it a predetermined batch of M P samples and reveal them as requested.

This cap belongs only to a testing reduction. It is NOT being imposed on the exact coupling algorithm and does not purport to preserve exact Q after a global timeout. The tester is allowed a small decision error, which is why this operation is legitimate here.

For 0<eta<=1, t<=65/eta and M<=1300(C+1)/eta+1. Knowledge of a chosen valid bound C suffices to specify this tester. For a lower-bound contradiction one may fix any claimed uniform bound in advance. No executable procedure for estimating the algorithm's worst-case expectation is assumed.

## 5. Substitute the primary thresholds

The two testing promises above correspond to

    epsilon_1 = 2 eta,  epsilon_2 = 8 eta.

Hence

    epsilon_1 / epsilon_2^2 = 1/(32 eta),
    (epsilon_1 / epsilon_2^2)^2 = 1/(1024 eta^2),
    1/epsilon_2^2 = 1/(64 eta^2).

The primary theorem forces

    M = Omega(d/[eta^2 log d] + sqrt(d)/eta^2)

in this fixed absolute range of eta. Combining this with the preceding upper bound on M proves the claimed result for C+1. All randomness used to generate the known U_d source is auxiliary randomness and provides no information about P.

## 6. Interpretation and limits

- The new lower bound includes adaptive allocation, random stopping and universally exact processing, unlike the earlier fixed-batch comparison.
- It charges the fresh input needed for each independent invocation. Dropping this +1 would be an invalid reduction for a method given a free actual sample.
- It proves a worst-case bound only. It does not assert that the unknown P attaining the hard case is uniform, or that the earlier equal-uniform work example has this lower bound.
- It does not address amortized coupling of many outputs with a reusable learned state, advice-dependent procedures, approximate Q marginals, or consumers that only need one expectation rather than a full new joint sample.
- The log-factor comparison has no useful explicit finite-d constant from this note. It must not be substituted for a measured resource benchmark.
- Primary tools already include tolerant distribution testing, residual coupling and Bernoulli factories. The reduction and the explicit locally capped sampler require a focused priority search before any novelty claim.

Independent challenge is requested separately. No code, experiment, source acquisition or external communication was performed for this note.
