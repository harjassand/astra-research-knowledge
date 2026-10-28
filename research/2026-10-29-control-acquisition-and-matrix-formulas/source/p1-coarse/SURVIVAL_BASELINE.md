# A standard all-time survival baseline without hidden-rank closure

## Result

The complete scalar survival curve of one repeatedly applied operation can be acquired with an ordinary empirical-distribution confidence band. Hidden-state identification and a finite-rank closure certificate are unnecessary for this task.

An executed software acquisition used **4,000 fresh preparations**, **62,181,306 primitive applications** and **62,181,306 coarse alive/absorbed reports**. The resulting estimator has absolute error at most **1/32 simultaneously at every repetition length**, with failure probability below **0.001**. The fixed censor cap was 1,000,000 applications per trajectory; all 4,000 observed trajectories absorbed before that cap.

This is an application of the standard Dvoretzky–Kiefer–Wolfowitz–Massart inequality. Its role in the programme is a strong existing baseline, not a claim of a new learning principle. It shows that the absence of a closed hidden-state representation does not by itself prevent an all-time guarantee for a single monotone survival curve.

## Observable task and acquisition

Prepare the same source distribution independently on each trial. Apply one fixed operation repeatedly and observe whether the source remains alive or has irreversibly absorbed. Reports are exact and nonintrusive. Let T denote the absorption time, allowing T=infinity. The requested response is

\[
S(h)=\Pr(T>h),\qquad h=0,1,2,\ldots.
\]

A death at step t contributes to survival through step t−1 and not at step t. The future query is a repetition length h; no change of operation or preparation is included in this scalar task.

Choose a fixed finite censor cap C before acquisition. On each trial, stop at absorption or after C applications and record

\[
Y=\min(T,C+1).
\]

The value C+1 is a censor flag, not a claim that absorption occurs at that time. It includes every trajectory still alive after C, including trajectories that will never absorb. Every primitive application and report until the actual stopping point is charged. Each trial receives a fresh preparation; a coarse alive report does not restore the initial hidden-state distribution.

For n recorded values Y_1,...,Y_n, define

\[
\widehat S(h)=
\begin{cases}
n^{-1}\sum_{j=1}^{n}\mathbf1\{Y_j>h\},&0\le h\le C,\\
0,&h>C.
\end{cases}
\]

Let m be the number of censor flags. The confidence radius is epsilon+m/n, where epsilon is chosen through the ordinary DKW inequality.

## Ordinary proof, including censoring and never-absorbed mass

The variables Y_j are independent samples of a finite-valued random variable. Their empirical distribution function satisfies

\[
\Pr\!\left\{\sup_y|\widehat F_Y(y)-F_Y(y)|>\epsilon\right\}
\le 2\exp(-2n\epsilon^2).
\]

This is the DKW–Massart inequality; it holds for arbitrary distribution functions, including discrete distributions.[1]

On the complementary event, for every integer h≤C,

\[
\Pr(Y>h)=\Pr(T>h)=S(h),
\qquad |\widehat S(h)-S(h)|\le\epsilon.
\]

For h>C, monotonicity of survival gives

\[
0\le S(h)\le S(C)
\le\widehat S(C)+\epsilon
=m/n+\epsilon.
\]

Because the estimator is zero there, the same event establishes

\[
\boxed{\sup_{h\ge0}|\widehat S(h)-S(h)|\le\epsilon+m/n.}
\]

There is no additional confidence charge for the unbounded set of repetition lengths. There is also no separate unobserved-tail assumption: the finite censor flag is the observation that bounds the entire later tail.

In particular, the never-absorbed probability is at most m/n+epsilon on this event. The method does not assume eventual absorption. If many samples remain censored, the radius becomes loose and reports that limitation honestly. In the executed receipt m=0, so the radius is epsilon, while a small nonzero never-absorbed mass remains statistically possible.

Stopping a trajectory when it has truly absorbed changes no observation relevant to its lifetime. When every acquired trajectory has already absorbed, the overall simulator can finish before the predetermined cap. This early completion does not turn the cap into an adaptively selected censor threshold.

## Executed acquisition and complete native costs

The private fixture is the same two-rate source used by the coarse-memory experiments:

\[
A_g=\operatorname{diag}(1-g^3,1-g),\qquad g=1/32,
\]

with an equal mixture of its two live states at preparation. Each trial privately chooses the slow or fast component with equal probability, then uses exact integer random draws for absorption at each step. Its survival law is

\[
S(h)=\tfrac12(1-1/32768)^h+\tfrac12(1-1/32)^h.
\]

The learner is given neither the component label nor these rates. The private formula is used only for a diagnostic after inference. The empirical-distribution certificate would have the same validity for another lifetime distribution, including one with arbitrarily many hidden states or positive never-absorbed mass.

The acquisition uses n=4,000, C=1,000,000 and epsilon=1/32. Thus

\[
2n\epsilon^2=125/16,
\qquad 2e^{-125/16}<0.001.
\]

The inequality is checked using a finite rational lower bound on exp(125/16), so the stated confidence does not depend on floating-point exponentiation.

| Resource or output | Executed value |
|---|---:|
| Fresh preparations | 4,000 |
| Primitive applications | 62,181,306 |
| Coarse alive/absorbed reports | 62,181,306 |
| Fixed per-trial censor cap | 1,000,000 |
| Censored trajectories | 0 |
| Last observed absorption time | 234,748 |
| Simultaneous all-length error bound | 1/32 |
| Failure probability upper bound | 0.001 |

The action and report totals equal the exact sum of the recorded lifetimes capped at C. They include the long slow trajectories. The small preparation count therefore does not conceal the physical evolution and observation bill. The private floating diagnostic reports a maximum error of approximately 0.0168562; the rigorous statistical guarantee remains 1/32.

This was an integer-RNG software experiment. Instrument calibration, physical preparation time and hardware execution time were not measured. Independent trials and truthful nonintrusive absorption reports are the experimental premises of this baseline.

## Relation to the rank lower-bound witness

`COARSE_MEMORY_ACQUISITION.md` studies a different question on the same source and coarse observation interface. Its determinant

\[
\Delta_L=S(2L)-S(L)^2
\]

is positive for the source. Certifying this rejects a one-dimensional time-homogeneous linear realization and proves that at least two linear features are required. It does not prove that two features suffice, acquire a closed two-state model, or certify every future response.

The pilot-selected block witness answered that dimension lower-bound question using 12,048 fresh preparations, 522,817 primitive applications and 18,847 coarse reports. The survival baseline answers the all-length scalar-curve question with 4,000 preparations but 62,181,306 applications and reports. Those resource totals belong to different outputs; they are not an efficiency comparison for an identical task.

The DKW estimator does not obtain a hidden-rank upper bound. It simply makes one unnecessary for the requested survival curve. This distinction prevents two incorrect conclusions: that a rank lower-bound witness has already acquired a reusable closed model, or that lacking such a model rules out all-time scalar prediction. The standard survival estimator supplies that prediction directly, while paying for enough physical observation of lifetimes.

## Reuse scope and limits

The confidence event is simultaneous over every repetition length of the one operation. A later user may select h after inspecting the acquired curve without a new confidence penalty. The stored empirical survival function is a finite representation of that scalar answer, and the censored tail bound controls its continuation.

The guarantee does not extend to unexecuted switching programs, another initial distribution, or an arbitrary receiver. Survival is monotone, which is precisely why a bound on S(C) controls all larger h. General signed or oscillatory port responses do not have this property. Learning separate survival curves for individual operations also supplies no automatic joint switching law.

The exact-report DKW theorem used here is an iid sampling result. The separate conditional live/dead sensor-error extension for the boundary compiler does not automatically furnish a dependent-noise DKW theorem for this lifetime estimator.

## Preserved implementation and review

The executed acquisition and inference are in `core/survival_distribution_baseline.py`. Its raw lifetimes are preserved in `results/SURVIVAL_DISTRIBUTION_RAW_RECEIPT.json`, and its certificate and complete ledger in `results/SURVIVAL_DISTRIBUTION_BASELINE.json`.

An independent exact replay checked every lifetime, censor flag, action/report total, preparation count and the rational confidence calculation without generating new trajectories. Its ordinary review is `branches/dynamics/SURVIVAL_DISTRIBUTION_BASELINE_REVIEW.md`; its checker and receipt are `replay_survival_distribution_review.py` and `SURVIVAL_DISTRIBUTION_REVIEW_RESULTS.json` in the same directory.

[1] P. Massart, “The Tight Constant in the Dvoretzky–Kiefer–Wolfowitz Inequality,” *The Annals of Probability* 18(3), 1269–1283 (1990). [DOI: 10.1214/aop/1176990746](https://doi.org/10.1214/aop/1176990746).
