# Acquire the island along one retained trajectory

24 October 2026. This strengthens the first construction: the learner need not call a full-process initializer even during acquisition. It is not a claim that the relevant contexts necessarily appear. Exploration has a finite cap and missing contexts return UNKNOWN. The guard/coupling construction and its supplied physical completeness assumptions remain as stated in `FIRST_CONSTRUCTION.md`.

## Precise sensor and time contract

Cells are clocked native binary memories. They do not change between requested update pulses. Repeated readout is nondemolition and takes a stated positive time/cost per read; the native clock is held during those reads. This stability/gating is supplied apparatus structure, not a free idle control inferred from counts. At each read of a fixed bit X, the probability of an incorrect output, conditional on the full physical state and all prior history/noise, is at most e_s<1/2. Conditional independence is sufficient but not necessary. A mere marginal error ceiling is insufficient: a persistent sensor flip could defeat majority voting.

During preparation, the controller performs only fixed public update pulses and emits no state/bath readouts. Its public word and completion time are retained. The microscopic update-noise trajectory is not measured or made a continuation input; this is the stipulated ordinary stochastic channel, not a hidden sampled-controller-word key. If that trajectory is logged, the unconditional coupling bound need not be valid after conditioning on the log. Future policies see only the declared sensor support A, apart from previously frozen calibration information shared by the comparison. They do not read distant cells during the evaluated future protocol.

## Observation-driven coverage, without a context sampler

Let B be the trained finite guard, C contain B and all its immediate physical parents, and U the finite set of candidate controls. Fix a public exploration schedule on C, such as alternating controls in synchronous rounds. Start from the existing unknown field. Before each round, read each cell in C an odd number r of times and form a majority. Apply the scheduled local updates in parallel using the old field. Then read each cell in B r times. For every i in B, current control a and observed neighborhood z, retain the first m post-update majority bits at that row. Later responses at an already full row may be discarded; all their actual sensing/actuation is still charged. Stop when every required row is full or after a fixed T_max rounds. No full initializer, exact bit label or forced-context intervention is used.

Every majority decision is incorrect with probability at most

    exp[-2 r (1/2-e_s)^2],

by Hoeffding-Azuma for the conditional bit-error indicators. There are at most T_max (|C|+|B|) majority decisions, so a union bound controls any wrong acquired context or response bit. Holding the cells fixed and paying all r raw reads are essential. The same true bit may be read in several decisions; no independence across decisions is needed for the union bound.

On the event that every majority is correct, context selection at a row is predictable before its update noise. The physical Markov rule gives

    Pr(X_i(new)=1 | entire prior, current context z, scheduled a)
       = p_i^a(z).

Hence the first m visits to any fixed row provide a Bernoulli martingale sequence with this constant conditional mean. If the row has fewer than m visits by the cap, the algorithm does not certify it. Without conditioning on eventual coverage, the probability that a completed row's empirical mean misses p_i^a(z) by w is at most 2 exp(-2m w^2). One way to formalize noncompletion is to preassign each row a fresh Bernoulli tape and consume its next bit on each visit; unused tape bits do not constitute physical observations. An equivalent stopped-martingale proof augments after the finite cap only for the probability bound. Summing over M=|B| |U| 2^d rows gives

    Pr(returned table/certificate invalid)
      <= T_max(|C|+|B|) exp[-2r(1/2-e_s)^2]
          + 2M exp(-2m w^2).                         (1)

This is an unconditional failure-and-return guarantee. It must not be divided into a claimed conditional-on-success confidence without a lower bound on the return probability. The realized data can show full coverage within the cap; they do not prove a uniform runtime or coverage bound over the architecture class. Frozen, rare, disconnected or adversarial contexts can force UNKNOWN. With a separately justified visitation floor, one could derive a runtime bound; no such floor is supplied here.

For every completed local response table, form confidence intervals [max(0,p_hat-w),min(1,p_hat+w)]. An upper influence bound for parent j is the maximum, over pairs of contexts differing only in j, of max(U(z)-L(z'),U(z')-L(z)). This includes *all* parents of boundary sites, not only internal guard parents. Select legal per-site modes minimizing the certified row sum. If the maximum selected row sum is below one, the deterministic guard mode vector has the acquired contraction certificate. An ordinary retaining local-table controller can make exactly the same choice.

Noisy readout uncertainty is not confused with Bernoulli update noise: the first term of (1) pays misclassification of the hidden native bits, while the second pays statistical estimation of their stochastic update probabilities. Both are needed.

## Whole-operation costs

At most T_max|C| site-update pulses, T_max synchronous update rounds, T_max r(|C|+|B|) raw sensor reads and their hold/read latency are paid in acquisition. Retained row counts require O(M log m) bits; the streamed trajectory need not be stored. Computation includes majority processing, row/context identification, interval construction and mode search. The source must expose only actual noisy reads, never its hidden context index or response table.

Each preparation then pays k|B| native updates and k fixed public rounds, no controller-selection bits, and no internal measurement record. The all-history local future-TV certificate is obtained from the acquired influence matrix by the substochastic first-hit/coupling proof. Spatial volume |B| and the future causal cone size are explicit. On a general bounded-degree graph they can grow exponentially with guard radius/horizon; polynomial volume is an extra physical geometry assumption. Repeated later event means use the same bounded-bias martingale argument as the earlier reset theorem, with the declared finite-horizon target and no full-system reset claim.

## Literal root refinement retained once

```text
Potential consequential next gain within your honest local clocked interface: tables can be acquired along one retained trajectory with a deterministic public exploration schedule, using first N visits to each context/mode; conditional fresh update noise suffices for visit-stopping concentration, so acquisition may need ZERO full initializers too. No context sampler needed; fixed exploration budget and missing contexts=>UNKNOWN, report realized rare-context cost. This could change initializer dependence rather than just replace the rank promise. Please evaluate if feasible/scientifically useful, without discarding current proof or assuming visitation rates. Also price |guard| explicitly: bounded degree alone can give volume exponential in H/logaccuracy; polynomial spatial-grid volume is extra structure if claimed. Conventional local-table learner receives the same and can tie.
```
