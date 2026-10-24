# Retained-context acquisition: finite-data comparator boundary

24 October 2026. Short source addendum to `RETAINED_CONTEXT_ACQUISITION.md`; no novelty or advantage claim.

## What is already standard

The response-table step is ordinary adaptive tabular estimation once the native local context and chosen mode are known. For a fixed row \((i,a,z)\), each outcome on its first \(m\) predictable visits is a bounded martingale difference about the fixed conditional mean \(p_i^a(z)\). Hoeffding's martingale bound gives

\[
\Pr\{|\widehat p_i^a(z)-p_i^a(z)|>w\}\le 2e^{-2mw^2},
\]

without stationarity, independent visits, or conditioning on eventual coverage. A union bound over the finite row set remains valid when visits and stopping are history-dependent. The row intervals can then be post-processed into upper influence bounds and passed to the same robust mode selector. If the visit cap leaves any required row incomplete, returning `UNKNOWN` is the correct finite-data behavior.

The closest strong fully observed online comparator is tabular MDP estimation in UCRL2. Jaksch, Ortner, and Auer count visits to each state-action pair, form empirical transition rows, and use time-uniform confidence sets: their Lemma 17 controls failure at each time, while its proof unions over possible visit counts; Theorem 2 gives a finite-horizon regret guarantee under a finite-diameter communicating-MDP assumption. Its row radius is an \(L^1\) transition-vector radius of order \(\sqrt{S\log(At/\delta)/N_t(s,a)}\). Here the local parent configuration \(z\) and mode \(a\) play the contextual state-action role, and the target is a Bernoulli next-bit response, so the scalar interval above is simpler. UCRL2 is not itself the local-PCA theorem, but it is already a strong precedent for retaining one adaptive trajectory and maintaining count-indexed transition confidence sets. A structure-aware retaining local-table learner can use these same observed data, confidence intervals, influence calculation, and mode selector and therefore ties this procedure.

The one-stream PCA paper of Bayraktar, Lu, Maggioni, Wu, and Yang is structurally closer but does not subsume this finite stopped-row guarantee. Its single-long-trajectory Theorem 4.6 is asymptotic and assumes ergodicity plus a nonsingular limiting design matrix. Its Theorem 4.12 finite-sample guarantee is for multi-trajectory or ensemble estimators, with a sample size controlled by a design-matrix eigenvalue; it does not give this one-stream, predictably stopped context-count bound under noisy QND observations. The paper's local transition family is also a specialized empirical-neighborhood-matrix model, whereas this file estimates unrestricted binary local response rows.

For sensor errors, the stated conditional per-read bound is enough for the majority term, even with history-dependent errors: if \(E_j\) is the error indicator and \(\mathbb E[E_j\mid\mathcal F_{j-1}]\le e_s<1/2\), Azuma-Hoeffding applied to the centered indicators gives \(\Pr\{\sum_{j=1}^r E_j\ge r/2\}\le e^{-2r(1/2-e_s)^2}\). This is a standard martingale bound combined with the supplied hold/QND interface, not a new sensor-identification method. A marginal error ceiling alone would not justify it.

## No-reset and homing boundary

Even-Dar, Kakade, and Mansour's *Reinforcement Learning in POMDPs Without Resets* is a strong predecessor for learning from one uninterrupted stream. Their Theorem 4.5 gives near-optimal average reward in a connected POMDP with finite time polynomial in action/observation counts and the homing-time parameter \(K_H\), and exponential in the optimal-policy horizon. The algorithm takes an approximate reset/homing strategy as input; their random-walk existence lemma establishes a finite system-dependent homing scale, while they explicitly caution that existence alone does not make that cost useful. That result is policy-performance learning, not a finite confidence certificate for every local response row or a robust influence/mode-selection theorem. It neither provides the repeated noisy-QND read contract here nor guarantees that this deterministic exploration schedule visits all rows by its cap. Conversely, this construction promises no general homing, irreducibility, or coverage rate: it only certifies when the realized stream happens to cover all required rows and returns `UNKNOWN` otherwise.

## Assessment

The exact end-to-end interface composition—paid repeated reads of held bits, an unconditional sensor-plus-row failure bound, a robust local influence certificate, then finite guard preparation—was not located as a single theorem in the sources checked. Its statistical ingredients and local contraction argument are conventional and modular, however. The strongest fair comparison is an equally informed retaining tabular/local-system learner given the same ordered stream, read-error contract, graph, and cap, allowed to compute the same intervals and selector. Under that comparison there is no claimed algorithmic advantage; the defensible point is that the retained-context contract makes the costs, uncertainty, and `UNKNOWN` boundary explicit.

## Primary sources

1. T. Jaksch, R. Ortner, and P. Auer, “Near-optimal Regret Bounds for Reinforcement Learning,” *JMLR* 11 (2010), especially UCRL2's visit-count transition estimates and confidence sets, Lemma 17, and Theorem 2. [Journal article and PDF](https://www.jmlr.org/papers/v11/jaksch10a.html).
2. E. Bayraktar, F. Lu, M. Maggioni, R. Wu, and S. Yang, “Probabilistic cellular automata with local transition matrices: synchronization, ergodicity, and inference,” arXiv:2405.02928, especially §§4.2 and 4.5 and Theorems 4.6 and 4.12. [Primary preprint](https://arxiv.org/abs/2405.02928).
3. E. Even-Dar, S. M. Kakade, and Y. Mansour, “Reinforcement Learning in POMDPs Without Resets,” IJCAI 2005, especially Lemma 3.2, Definition 3.1, and Theorem 4.5. [Primary paper PDF](https://www.tau.ac.il/~mansour/papers/05ijcai.pdf).
