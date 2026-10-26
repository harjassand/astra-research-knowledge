## ASTRA Pro3 — Exact recovery across changing feedback and time

I found a tractable class that improves on the previous mixed-feedback global solver.

For a scalar source

\\[ F_t(x)=mx+A(t,x), \\]

assume the independently supplied contract

\\[ |A(t,x)-A(s,y)|\le a|x-y|+v|t-s|, \\]

and require each future feedback gain \\(K_j\\) to satisfy \\(m-K_j>a\\).

The previous solver treated different feedback controllers as a generally nonconvex joint problem, using rational box subdivision to obtain conservative bounds. In one spatial dimension, that problem can instead be solved exactly by enumerating the possible orderings of equilibrium positions. Each ordering produces linear inequalities, even when future controllers and operating times differ.

The construction also handles bounded, correlated historical sensor errors. It returns an exact feasible range over the declared Lipschitz source class, not merely an outer enclosure.

### Executed controls

Using four noisy forward experiments on a nonlinear, time-dependent source, I compiled six later two-equilibrium questions. No source evaluations were needed when those questions arrived.

| Later question | Separate-equilibrium error radius | Exact joint radius | Reduction |
| -------------- | --------------------------------- | ------------------ | --------- |
| 1              | 0.07538                           | 0.01725            | 4.37×     |
| 2              | 0.10873                           | 0.02365            | 4.60×     |
| 3              | 0.05529                           | 0.02184            | 2.53×     |
| 4              | 0.15816                           | 0.03113            | 5.08×     |
| 5              | 0.09150                           | 0.02755            | 3.32×     |
| 6              | 0.08626                           | 0.02186            | 3.95×     |

All bounds use exact rational polyhedral calculations. At each extreme, the programme constructs a globally admissible Lipschitz source that attains the claimed endpoint. This supplies matching information-theoretic witnesses for the observed interval widths.

A deliberately inconsistent pair of noisy measurements was also rejected.

The construction uses classical McShane–Whitney extension mathematics. Its value is as an executable acquisition-to-operation procedure; neither the extension theorem nor the ordering technique is claimed as historically novel.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://doi.org\&sz=32)

ScienceDirect



### Extension to newly assembled nonlinear networks

The same principle extends beyond two separate inverse queries. Suppose a later scientific operation specifies

\\[ mz_i+A(t_i,L_i z)=p_i, \\]

where \\(L_i z\\) is a newly chosen linear combination of several system states. The cross-couplings may be positive or negative.

Under a supplied contraction condition, the network has a unique equilibrium. Because each unknown source input \\(L_i z\\) is affine in the future state, its ordering relative to all retained measurement locations again produces linear consistency constraints.

I implemented this for four newly specified two-state networks, reusing the same four noisy observations. Across 12 later questions, all exact extremal bounds were supported by globally compatible source witnesses.

| Later network       | Sharp error for state difference | Without shared-source constraint | Reduction |
| ------------------- | -------------------------------- | -------------------------------- | --------- |
| Signed network 1    | 0.01088                          | 0.10034                          | 9.22×     |
| Signed network 2    | 0.02604                          | 0.12114                          | 4.65×     |
| Cooperative network | 0.05140                          | 0.10072                          | 1.96×     |
| Signed network 3    | 0.00225                          | 0.05555                          | 24.7×     |

All four use zero additional native source calls after acquisition.

The solver is exact but not dimension-free: enumerating input orderings can become factorially expensive. Its main significance is a complete, finite experiment-to-network representation for this scalar shared-law class, not a claim of efficient general nonlinear network solving.

### Calibration imposes a genuine information limit

The shared-calibration experiment established that some scientific uncertainty cannot be removed by taking more measurements through the same instrument.

For two source models indistinguishable at every possible sensor input, the future equilibrium contrast retains an unavoidable error radius of \\(1/12\\), even after arbitrarily many adaptive measurements.

In the executed broader source family:

| Acquisition method                                     | Certified error radius |
| ------------------------------------------------------ | ---------------------- |
| Treat common bias independently at each sensor reading | 0.41815                |
| Retain the shared calibration parameter                | 0.10187                |
| Add another reading using the same biased sensor       | 0.10187                |
| Obtain an independent exact sensor calibration         | 0.00417                |

The conclusion is operational: a scientific learner must sometimes acquire a new measurement capability, rather than collect more observations with an instrument whose information is fundamentally ambiguous.

### Second attack: weaker physical assumptions

I then removed the quantitative upper Lipschitz assumption entirely.

For a stationary scalar response whose residual is continuous and nondecreasing, retained observations still support sharp inverse-response bounds using only order constraints.

Four initial native readings supported eight later force-controlled questions with no further acquisition. A targeted fifth reading reduced one chosen error radius from 0.06878 to 0.02898, approximately 2.37×.

This transfers less structure than the quantitative Lipschitz model, but it requires a weaker regularity premise. Stationarity and monotonicity remain supplied assumptions.

### Preserved work

Complete governing proofs

Exact scalar consistency theorem, network compilation, temporal transfer, calibration-gauge lower bound, weaker monotonicity theorem and limitations.

Reproducible scientific research bundle

Five Python investigations, five actual results files, clean-replay verifier, complete proof note and verified SHA-256 manifest.

All five investigations passed independent clean-directory execution, with byte-identical saved results. The archive passed its integrity and hash checks.

Scientific assessment: The strongest result is an exact compiler for unforeseen scalar-source networks, including signed feedback and bounded time variation, with a separate mechanism for correlated calibration uncertainty. It does not resolve general vector-valued mixed feedback.

The central unresolved problem remains acquiring physically justified source contracts. In particular, finite observations cannot establish unrestricted global regularity. An equally informed classical retaining programme can reproduce these methods.

The new results are preserved locally. The Astra GitHub repository was not modified.