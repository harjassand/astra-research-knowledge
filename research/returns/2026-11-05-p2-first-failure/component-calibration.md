# Sharp calibration of independent-component first-failure predictions

This is P2's second mathematical result, with a broader failure-rule scope than the network computation algorithm. Read the [complete proof, theorem and model](package/research_note.tex#L58-L164) or the [PDF report](package/research_note.pdf).

## Exact scope and finite perturbation law

There are m independent binary components, initially all working. Component i has constant positive failure rate a_i and repair rate b_i. The failure set is any **nonempty monotone rule** with the all-working state safe. Let M be the all-working mean time to first failure.

If every failure and repair rate has log error at most eta,

```text
|log(a_hat_i/a_i)|<=eta,   |log(b_hat_i/b_i)|<=eta,
```

then

```text
exp(-(2m-1)eta) M <= M_hat <= exp((2m-1)eta) M.
```

The coefficient `2m-1` is optimal over this model class. It counts physical components, not the `2^m` configurations or exponentially many transition copies of one component rate.

For `F(t)=Pr_all-working(tau_failure<=t)`, simultaneously for every `t>0`,

```text
exp(-2m eta) F(t) <= F_hat(t) <= exp(2m eta) F(t).
```

The deadline statement is a **robustness law**, not by itself an efficient method for computing the entire failure-time distribution. Likewise, the general monotone-predicate scope does not automatically supply the all-terminal algorithm's required static counting procedure. [Theorems](package/research_note.tex#L58-L97).

## What the proof acquires

Condition on the other components' trajectories and on component i's repair marks. Survival requires its failure Poisson process to avoid a determined set of dangerous intervals, yielding `S(t)=E[1_G exp(-a_i L_t)]`, with L_t independent of a_i. An entropy inequality and all-working monotone coupling give

```text
-1 <= partial(log M)/partial(log a_i) <= 0
partial(log M)/partial(log b_i) >= 0.
```

Scaling every rate by c divides M by c, so the signed log sensitivities sum to -1. Their total absolute value is therefore at most `2m-1`. Integrating along a finite log-rate perturbation proves the mean bound. The argument handles **all configuration transitions sharing one physical rate together**, rather than applying an explicit-state bound independently to every transition. [Mean proof](package/research_note.tex#L98-L144).

For m identical parallel components with failure a much slower than repair b,

```text
M(a,b) ~ b^(m-1)/(m a^m).
```

Replacing a by `a exp(-eta)` and b by `b exp(eta)` changes the mean asymptotically by `exp((2m-1)eta)`, establishing sharpness. The deadline proof and this example are supplied separately. [Source](package/research_note.tex#L145-L164).

## Acquire the local rates and pay for rare local events

For a local exponential rate r, observe N_cal complete dwell times Y_j and use `r_hat=N_cal/sum_j Y_j`. For `0<eta<=1`, the source bounds log-rate error probability by `2 exp(-N_cal eta^2/3)`. Thus

```text
N_cal = ceil(3 eta^-2 log(4m/delta_acq))
```

suffices simultaneously for all `2m` rates. With `eta=Theta(epsilon/m)`, a sufficient total dwell-observation count is `O(m^3 epsilon^-2 log(m/delta_acq))`.

That count is not observation time. Expected aggregate component exposure is

```text
N_cal sum_i(1/a_i+1/b_i).
```

If every local rate is at least r_-, parallel monitoring has high-probability elapsed-time bound `O((N_cal+log(m/delta))/r_-)`. A very rare local transition remains expensive to learn passively. State access, preparation, missed events, classification errors and timestamp uncertainty must be included in valid rate intervals. The report contains no physical measurements. [Acquisition](package/research_note.tex#L165-L189).

## Relation to earlier results, evidence and limits

The source credits existing single-transition sensitivity bounds and the time-scaling sum rule, as well as Astra's explicit-state N1596 comparison. Its additional argument is component-group control without an exponential configuration-count coefficient. Separate in-session constructive derivations and numerical diagnostics are reported; no new audit or simulation was run for publication. The [recorded diagnostics](package/results.json) and [original program](package/check_reliability.py) are available directly.

This theorem calibrates a specified independent, time-homogeneous model. It does not infer independence, eliminate hidden common-cause failures, certify model completeness or establish practical superiority. An unobserved catastrophe can materially change a long-lifetime prediction without appearing during short passive observations. [Physical boundary](package/research_note.tex#L406-L415).

[Mean first-disconnection algorithm and complete package](README.md) · [Other supplied results](../README.md)
