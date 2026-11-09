# Prior methods and application costs

## Assessment

The package is worth preserving as an algorithm-and-limits theorem: it provides an exact full-output operation, distinguishes mean from hard-cap acquisition, repairs the rare-label moment failure, and has a worst-case expected-query lower bound within a logarithmic factor. This is a theoretical assessment. No historical novelty, practical speed advantage or production readiness is claimed.

The most plausible consumer is a black-box categorical proposal followed by an expensive label-dependent response. The proposal must be cheap to sample exactly but lack usable probability or common-randomness access; a full correctly distributed updated sample must actually be required. These conditions are narrower than ordinary caching or estimation, and no acquired workload satisfying them is included.

For deterministic label responses across repeated updates, ordinary memoization is a stronger essential baseline: storing one response for each encountered label eventually needs at most d response evaluations, after which fresh independent proposals need no new response work. The one-update crossover below does not defeat that amortized strategy. For stochastic responses, caching also changes multi-output dependence unless the requested contract permits it; this packet promises the stated single returned pair, not an independent sequence of cached responses.

## Strong starting capital

The latest inspected main of `harjassand/astra-research-knowledge` was unchanged at commit `bb16dbf0e9c9b9ecaacfd10f577aedef51bd2e0e`, dated 9 November 2026 at 06:50:26 UTC. The N1691 governing source is:

https://github.com/harjassand/astra-research-knowledge/blob/bb16dbf0e9c9b9ecaacfd10f577aedef51bd2e0e/research/2026-11-04-p2-exact-stochastic-reuse/source/p2/NATIVE_RESPONSE_PREFIX_PARTIAL.txt

Its preserved content SHA256 is `a99a0a46b826983d21d5fc584e29b5ddd03a4e20ec5418c3d88e8a8eabc8f39c`. It already establishes the actual-stored-sample contract, common-atom boundary, fixed-batch empirical-coupling characterization and sharp binary mean/hard-cap laws. Its binary walk has better constants than the present general categorical construction. The current result must not be described as inventing sample reuse, residual coupling or the binary separation.

The later saved reuse discussion moved to a different consumer, estimating one expectation from a response archive. Producing an entire coupled sample can be unnecessary for that task. The present package makes no claim of improving that expectation-only operation.

## Primary antecedents and access differences

1. **Classical residual coupling.** Devroye, *Coupled Samples in Simulation*, Operations Research 38(1), 1990, and Jacob, O'Leary and Atchadé, *Unbiased Markov chain Monte Carlo methods with couplings*, arXiv:1708.03625v5, Section 4.1, provide powerful maximal/residual coupling constructions. Their probability/density-evaluation access can be much cheaper when available. The diagonal-plus-product-residual form used here is inherited machinery.

   https://luc.devroye.org/devroye-coupledsamples-1990.pdf
   https://arxiv.org/html/1708.03625v5

2. **Variance-controlled coupling.** Corenflos and Särkkä, *The Coupled Rejection Sampler*, arXiv:2201.09585v2, Sections 2–3, assumes coupled dominating proposals and evaluated acceptance ratios. Proposition 1 controls mean and variance; ensemble proposals approach maximality. Sacrificing maximality to control latency variance is therefore established prior. That stronger access does not directly realize the actual stored-X sample-only theorem, but it is a mandatory practical comparator when available.

   https://arxiv.org/html/2201.09585

3. **Dice enterprises and rational factories.** Morina, Łatuszyński, Nayar and Wendland, *From the Bernoulli Factory to a Dice Enterprise via Perfect Sampling of Markov Chains*, arXiv:1912.09229v2, provides exact transformations of unknown categorical probabilities. General rational implementability is not the contribution here. The inspected Proposition 3.10 does not supply the specific uniform cost identity or local-timeout theorem; this is a limited source finding, not proof of priority.

   https://arxiv.org/html/1912.09229v2

4. **Bernoulli races and combinatorial factories.** Dughmi, Hartline, Kleinberg and Niazadeh, arXiv:1703.04143v2, Section 3.1, and Niazadeh, Paes Leme and Schneider, arXiv:2011.03865v2, supply exact normalized selection and combinatorial factory machinery. A residual race itself is not new. The complete stored-sample law, cancellation of its mean cost and symmetric timeout are the specific operations established in this packet.

   https://arxiv.org/html/1703.04143v2
   https://arxiv.org/html/2011.03865v2

5. **A current finite-automata caveat.** Paes Leme and Schneider, *Note on Finite-Automata Bernoulli Factories for Rational Functions*, arXiv:2606.29595, identifies a problem with a broad multivariable rational characterization. This packet does not infer a universal compiler from rationality. Its finite-counter transitions are explicit.

   https://arxiv.org/pdf/2606.29595

6. **Tolerant testing.** Canonne, Jain, Kamath and Li, *The Price of Tolerance in Distribution Testing*, COLT 2022, published Theorem 7 and Corollary 8, supply the hard distribution-testing lower bound. The coupling reduction is stated in full; the published theorem remains an external mathematical dependency, not a new result of this package.

   https://proceedings.mlr.press/v178/canonne22a.html
   https://proceedings.mlr.press/v178/canonne22a/canonne22a.pdf

7. **Exact black-box attribute alignment.** Jiang, Austern, Dobriban and Klusowski, *Statistical attribute alignment for black-box generative AI via output post-processing*, arXiv:2609.31607, Sections 2–3 and Appendix A.2.2, is a close 2026 predecessor. It supplies the target attribute law and selects outputs without replacement from one generator; its objective is generator-query cost. It does not require retaining a distinguished actual old sample or bound disagreement with that sample. This is an important exact-output antecedent, but not a direct realization of the two-unknown-law retained-sample contract.

   https://arxiv.org/html/2609.31607

8. **A real exact categorical oracle.** Schmon, Doucet and Deligiannidis, *Bernoulli Race Particle Filters*, AISTATS 2019, Section 3, Algorithm 2 and Proposition 2, supplies exact resampling with intractable weights under its estimator assumptions. Section 3.1 charges the race acceptance cost, and Section 4 gives applications. This is a legitimate source-access example, not evidence that the reuse construction improves particle filtering.

   https://proceedings.mlr.press/v89/schmon19a/schmon19a.pdf

Focused primary searches did not locate the exact combined contract and bounds. This does not establish historical priority or exclude a straightforward derivation elsewhere.

## Correct response reuse contract

Suppose a stored response R has conditional law H(X,.), and the coupling's fresh randomness is independent of R conditional on X and the declared external history. The coupling must not use the response. If Y=X, retain R; otherwise acquire a fresh independent response from H(Y,.). Then the returned pair has marginal law Q(dy) H(y,dr).

Conditional independence is essential: merely not inspecting a response does not make externally correlated randomness independent. No arbitrary hidden computation state, feedback record or response-dependent selection policy is preserved by this lemma.

## A fully charged work comparison

Let c_P,c_Q be the actual conditional expected costs of each fresh source call, constant across calls for this comparison. Let W be the constant conditional expected cost of a fresh response. If these are only upper bounds, an exact crossover cannot be inferred without a corresponding incumbent lower bound.

For the original uncapped factory at equal uniform P=Q on d>1 labels, the exact comparison is

    fresh independent draw: c_Q + W(1-1/d),
    original factory: d(L-1)c_P + [1+d(L-1)]c_Q
                      + W(1-1/d)/L.

For L>1, the original factory is cheaper in this model exactly when

    W > d L(c_P+c_Q)/(1-1/d).

This excludes local integer/bit work, which must be added if material. It is not a general advantage theorem.

For the preferred locally capped sampler, A_K+B_K<=2d(L-1), so a conservative upper bill is

    c_Q + d(L-1)(c_P+c_Q) + W eta

at equal uniform sources. Thus a sufficient condition is

    d(L-1)(c_P+c_Q) < W(1-1/d-eta),

with a positive right-hand coefficient. This is sufficient, not an exact crossover, because both the capped mean and mismatch have been upper bounded.

At d=16, eta=.01, actual equal call means c_P=c_Q=c and the declared L=200, this requires

    W/c > 6368/(15/16-.01) = 2547200/371,

about 6865.8 before local work. No practical example with this verified ratio is supplied.

For a d-particle resampling round, independently invoking the generic reuse theorem for every ancestor gives an O(d^2/eta) source-oracle upper bill, compared with O(d) ordinary categorical draws. Each exact race has its own paid acceptance/runtime cost. The larger bill is not a universal lower bound against amortized couplings, but it defeats an immediate claimed particle-filter improvement. Ancestor identity, response independence and full propagation cost would also need to be checked; equal ancestor labels alone do not license arbitrary particle-state reuse.

## Expected versus deterministic and wall-time budgets

The preferred sampler has mean O(d/eta) but unbounded total stopping time. Its exponential tail has the larger O(d/eta^2) scale. It does not evade the Omega(d/eta^2) deterministic-cap obstruction. Fixed-batch empirical coupling offers a cap and efficient histogram processing; parallel acquisition can favor it despite its larger total sample count.

A query-count tail gives a wall-work tail only with suitable source runtime control, for example uniformly bounded per-call work. Conditional mean costs alone give only an expected bill. Dropping slow source outputs selectively can bias the source and is not permitted.

The eta^-3 second-moment lower bound matches the construction's eta exponent at fixed d under an exponential moment. It does not prove the tail scale or its dimension factor optimal. The expected-query lower bound needs no moment beyond the first, but is asymptotic and worst-case. Its hidden constants must not be used as finite numerical performance evidence.

## Remaining research questions

The logarithmic expected-cost gap, moment dimension dependence, sharper useful latency constants and amortized multi-output interfaces remain unresolved here. An implementation would also need source-contract tests and an acquired application. None is supplied by a symbolic call-count calculation.
