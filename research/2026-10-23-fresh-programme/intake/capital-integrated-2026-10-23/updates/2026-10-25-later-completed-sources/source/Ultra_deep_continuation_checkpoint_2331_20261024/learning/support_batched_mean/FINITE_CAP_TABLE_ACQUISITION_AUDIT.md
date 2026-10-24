# Finite-cap local-table acquisition audit

This checks the sampling and confidence interface in `FIRST_CONSTRUCTION.md`. It is a conditional statistical audit of the supplied local-memory architecture, not evidence that a real apparatus satisfies that architecture.

## Required sampling contract

Let (S) be the number of trained sites, (A) the number of local modes, and (C_i\le 2^d) the set of candidate contexts at site (i). On each paid source trial, assume the full initializer independently draws a configuration from one fixed, unknown distribution. Write \(\mu_{ic}\) for the chance that site (i) has context (c). The controller reads the (d) context bits before the update, applies a mode selected from the visible history and context read, and reads the output bit after the update. The local update must have conditional mean \(p_i^a(c)\) whenever its true pre-update context is (c). Its transition noise must remain conditionally well-defined under adaptive sampling. Each new source trial costs one full initialization; it does not supply a context label for free.

There is a critical sensor qualification. A QND read does not change the underlying bit, but that alone does not make successive read errors independent. Majority amplification below requires either independent read errors conditional on the true bit, or the stronger history-conditional guarantee
\[
 \Pr(E_s=1\mid X_s,\mathcal F_{s-1})\le q_0<1/2.
\]
If only each read's marginal error is at most \(q_0\), the same error can repeat perfectly on every read; a majority then still errs with probability \(q_0\). Thus the task's single-read noise ceiling is not, by itself, a majority-error theorem.

## Simultaneous sensor and response confidence

For odd (R), the conditional error assumption and Azuma-Hoeffding give, for one majority of a fixed bit,
\[
 \Pr(\text{majority wrong})\le e_R
 :=\exp[-2R(1/2-q_0)^2].
\]
This bound allows adaptive stopping: apply it to every read block that could be opened before the public cap, then union-bound. If each trial reads all (S) sites in parallel, with (d) context bits before the update and one output bit after it, there are at most (M=T S(d+1)) majority decisions. Therefore
\[
 \Pr(\text{any acquired majority wrong})\le M e_R.
\]
For sensor failure budget \(\delta_s\), choose the smallest odd (R\) at least
\[
 \frac{\log(M/\delta_s)}{2(1/2-q_0)^2}.
\]
The paid read count is (MR) binary sensor calls. If the actual protocol rereads more coordinates, replace (M) by the literal maximum number of majority decisions under its cap.

At each visit to a site-context pair \((i,c)\), cycle through the (A) modes in a fixed order, using the next mode based only on the visit count. This obtains the first (m) outcomes in every \((i,c,a)\) table row after (Am) true visits to that site-context pair. Let
\[
 L=\sum_i A C_i\le S A 2^d,
 \qquad
 m\ge \frac{\log(2L/\delta_p)}{2\epsilon_p^2}.
\]
For each row, its first (m) response bits form a bounded martingale-difference sample with conditional mean \(p_i^a(c)\); Hoeffding-Azuma gives a simultaneous radius \(\epsilon_p\) with failure probability at most \(\delta_p\). This does not require the rows or sites to be mutually independent. It does require the mode schedule to be selected before the current response, and the local response law to have the stated conditional mean. If the implementation chooses modes from the responses in a way that changes the target row or its response law, this bound does not apply unchanged.

The clean way to handle noisy labels and context-based stopping is to define, for analysis, the first (m) samples of each row using true contexts and the same predictable mode cycle. On the event that every paid majority is correct, the observed stopping indices, actions, contexts, and response bits equal this ideal table exactly. Union-bounding the sensor event and the ideal response event proves
\[
 \Pr(\text{a returned table is invalid})\le \delta_s+\delta_p.
\]
This is an unconditional familywise statement about the output. It is not automatically a (1-\delta) statement *conditional on the algorithm returning a table*: when a required context is extremely rare, a return can be disproportionately caused by a sensor-error event. With a known lower-frequency promise and a cap chosen to make true coverage likely, the conditional guarantee follows by dividing by a lower bound on return probability. More generally, if a justified lower bound \(p_{ret}>0\) on return probability is available, then
\[
 \Pr(\text{invalid}\mid\text{return})
 \le \frac{\delta_s+\delta_p}{p_{ret}}.
\]
For example, \(p_{ret}\ge1-\delta_{cov}-\delta_s-\delta_p\) follows from the frequency cap only when a separate contraction-margin condition ensures the contraction gate passes whenever the table intervals are valid.
The remaining possibility is always reported as `UNKNOWN`, never as a filled-in row.

For two contexts (c,c'\) differing only at neighbor (j), a simultaneous row interval \([\hat p-\epsilon_p,\hat p+\epsilon_p]\) gives the valid influence upper bound
\[
 U_{ij}^a(c,c')=\min\{1,|\hat p_i^a(c)-\hat p_i^a(c')|+2\epsilon_p\}.
\]
Taking the maximum over such pairs and summing over neighbors gives an upper row-sum certificate. If each estimate is within \(\epsilon_p\), each pairwise upper bound can exceed the true influence by as much as (4\epsilon_p); hence a true row-sum margin of at least (4d\epsilon_p) is a simple sufficient condition for a target contraction threshold to pass. A failed gate means `UNKNOWN`, including when the true system is contractive but the finite interval is too wide.

## Initializer and total cost

If \(\mu_*:=\min_{i,c}\mu_{ic}>0\) is known, a simple cap with high probability of collecting (Am) visits to every site-context pair is
\[
 T\ge \max\!\left\{\frac{2Am}{\mu_*},\;\frac{8}{\mu_*}\log\frac{S\,2^d}{\delta_{cov}}\right\}.
\]
Indeed, \(N_{ic}\sim\mathrm{Binomial}(T,\mu_{ic})\), and when \(T\mu_*\ge2Am\), a Chernoff bound gives \(\Pr(N_{ic}<Am)\le e^{-T\mu_*/8}\); union-bound over at most (S2^d) pairs. This cap is conservative and can be replaced by exact binomial quantiles. If one trial probes only one site rather than updating all sites in parallel, the cap and initialization count must include the site-allocation factor; the formula above assumes every site's local response is observed on each full synchronous trial.

The paid ledger under that parallel interface is:

- (T) full initializations and (TS) local updates;
- (M=T S(d+1)) majority decisions, costing (MR) binary sensor readouts;
- at most (T S) local mode settings, plus the chosen cap and visible stopping log;
- (L\) table counts/sums and confidence intervals; and
- the arithmetic and memory to compare all context pairs and evaluate the (S\)-site contraction/coupling certificate.

If \(\mu_*\) is unknown, the finite-cap rule is simply: stop at the cap, check actual noisy counts, and return `UNKNOWN` if any required row lacks (m) observations or any contraction gate fails. A finite cap cannot ensure completion uniformly over all unknown initializer frequencies.

The obstruction is sharp. Consider two plants identical everywhere except one context (c_*\), with \(p(c_*)=0\) in one plant and (p(c_*)=1\) in the other. If the initializer reaches (c_*\) with probability \(\eta\), then after (T\) starts the transcripts are identical on the event that (c_*\) never occurs, of probability \((1-\eta)^T\). For any table accuracy (\epsilon_p<1/2), equal-prior testing has error at least \((1-\eta)^T/2\). Thus confidence (1-\delta) requires at least
\[
 T\ge \frac{\log(1/(2\delta))}{-\log(1-\eta)}
 =\Omega(\eta^{-1}\log(1/\delta))
\]
starts for small \(\eta\), even with exact context labels. The strong site-table learner sees the same data and obeys this same lower bound; adaptivity cannot learn an unvisited row.

## Future-event precision and comparator

On a valid acquired-table event, use the certified row-sum bound \(q<1\) in the stated spatial coupling recursion. For an (H\)-round target whose backward cone (F) is inside a radius-(R\) guard, the local-preparation contribution is
\[
 \eta_{prep}=|F|\big(q^k+q^{R-H+1}\big).
\]
If future-event probabilities are computed from fitted local rows rather than measured directly, and at most (J\) local transitions lie on the simulated finite-horizon event cone, a conservative additional kernel-approximation term is (J\epsilon_p) by stepwise coupling, plus the future readout error. If the future event is physically sampled after preparation, and each retained-state trial has conditional event mean within \(\eta_{prep}\) of the reference probability, then for (N\) trials
\[
 \Pr\!\left(\left|\bar Y-p_*\right|>\eta_{prep}+\tau\right)
 \le \delta_{cal}+2e^{-2N\tau^2},
\]
where \(\delta_{cal}\) is the stated source/table failure budget. This is a martingale bound for retained state, not an iid assertion. The target policy, causal cone, and duration must remain within the certified interface.

The fair comparator is an equally informed site-table model-based controller receiving the same initializer trials, noisy readouts, update outcomes, mode-setting budget, and cap. It may use adaptive site allocation, exact binomial/anytime intervals, and a hidden-context likelihood model, provided those are fitted only from the same paid observations. It can select the same modes and use the same local coupling proof. The operation is mathematically useful under the supplied physical promises, but this audit identifies no learner advantage over that retaining comparator, and it does not establish that the promises hold in a platform.
