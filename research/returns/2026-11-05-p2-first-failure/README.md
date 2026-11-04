# P2 — compute the full mean time to first disconnection

**Read the [complete proof report](package/research_note.pdf) and [LaTeX source](package/research_note.tex).** A separate result, the [sharp component-calibration theorem](component-calibration.md), has a broader monotone-failure scope. The report supplies analytic proofs and reports separate in-session constructive derivations and numerical diagnostics. This publication preserves those scopes and performs no new reproof, scientific execution or novelty audit.

## Exact model and algorithmic guarantee

A known connected undirected graph, with at least two vertices and m edges, has independent two-state components. Parallel edges are allowed. Edge i fails at constant rate `a_i>0` and repairs at rate `b_i>0`. Repairs continue until the working subgraph first disconnects. Starting with all edges working, the requested quantity is the complete mean first-disconnection time M, including every repair, intermediate residence and unsuccessful approach to failure.

For positive rational rates, the construction returns `[L,U]` with confidence `1-delta`, containing M and satisfying `U/L<=1+epsilon`. Its work is polynomial in graph size, input bit length, inverse accuracy, `log(1/delta)` and

```text
g^(-1),  g = min_i(a_i+b_i) / sum_i(a_i+b_i).
```

If `kappa_gamma=max_i(a_i+b_i)/min_i(a_i+b_i)`, then `g^-1<=m*kappa_gamma`. Dependence is on the **value of the refresh-rate contrast**, not its logarithm. An exponentially large contrast can therefore be expensive. There is no lifetime-sized or inverse-stationary-failure-probability cost factor in the construction. [Model and theorem](package/research_note.tex#L58-L97).

This is a conditional model theorem. Independence, topology, exponential rates and a complete failure rule are premises; they are not certified by observing ordinary local behavior.

## The acquired static-to-dynamic operation

Uniformize the process at `Lambda=sum_i gamma_i`, `gamma_i=a_i+b_i`: choose i with probability `gamma_i/Lambda`, then redraw it failed with probability `a_i/gamma_i`. Self-updates are retained. If M_* counts updates, physical time is exactly `M=M_*/Lambda`.

The stationary law pi is a product distribution; let `p=pi(B)` for the disconnected set B. The source invokes **Karger's corrected all-terminal unreliability approximation algorithm**, including heterogeneous independent edge probabilities. It then earns a sampler for `pi(.|B)` by sequential self-reduction: query each next edge in its two fixed states, contract forced working edges, delete forced failed edges, and choose with the conditional weights. Each sample uses at most `2m` static calls, with explicit inverse-polynomial accuracy and failure allocation. It is computational sampling, not a demand to physically prepare a rare failed network. The supplied code does **not** implement the general-purpose Karger algorithm. [Uniformization and conditional sampling](package/research_note.tex#L190-L208).

From a conditioned failed state, simulate `k+1` ordinary updates. Count Z=1 only when the network becomes safe on the first update and remains safe through the whole short path. Reversibility gives

```text
p E[Z] = Pr_pi(tau_B=k+1).
```

This positive Bernoulli experiment corrects repeated failure crossings without subtracting nearly equal survival probabilities. [Short-path identity](package/research_note.tex#L246-L260).

Let `1-lambda` be the leading eigenvalue of the kernel killed on B. The report bounds

```text
g p <= lambda <= p/(1-p).
```

For `H_m=sum_(j=1)^m 1/j`, choose

```text
k = ceil((H_m+log(1/xi)+2)/g).
```

In the rare branch, selected by a certified upper bound on p,

```text
(1-2xi)lambda <= p E[Z] <= (1+xi)lambda
E[Z] >= g(1-2xi).
```

Thus the useful conditioned trial is inverse-polynomial even when stationary failure is exponentially rare. The construction uses `O(g^-1 xi^-2 log(1/delta))` trials, each with `O(g^-1 log(m/xi))` updates. Conditional sampling, random bits, arithmetic and confidence failures are paid. [Spectral and useful-trial bounds](package/research_note.tex#L209-L228), [rare branch and finite work](package/research_note.tex#L261-L311).

## The all-working state and the nonrare branch are included

A stationary flux alone is not the requested initial condition. Let C be the update at which every component has refreshed at least once. Its last redraws give exactly the stationary product law, and monotone coupling yields

```text
M_pi <= M_* <= M_pi+E[C],   E[C]<=H_m/g
1/lambda-1/g <= M_* <= 1/lambda+H_m/g.
```

These additive mixing-scale corrections are controlled relative to the lifetime in the rare branch. When the rare gate fails, the certified lower bound on p is inverse-polynomial; ordinary simulation, a second-moment bound, capped paths and median-of-means finish the nonrare case. The algorithm does not assume a useful plateau or leave an intermediate parameter region unresolved. [Initialization](package/research_note.tex#L229-L245), [nonrare branch and arithmetic](package/research_note.tex#L312-L334).

## Rates, physical observations and model completeness

The [calibration result](component-calibration.md) propagates simultaneous log-rate error eta with coefficient `2m-1`. Choosing `eta=Theta(epsilon/m)` gives a sufficient total local dwell-observation count `O(m^3 epsilon^-2 log(m/delta_acq))`. But the expected aggregate component exposure is

```text
N_cal sum_i(1/a_i+1/b_i).
```

A rare local transition remains expensive to observe. Component-state access, preparation, missed events, timing uncertainty and readout error must be reflected in valid rate intervals. There were no physical measurements. [Physical acquisition](package/research_note.tex#L165-L189).

The theorem excludes unmeasured common-cause jumps, cascades, shared repair crews, non-Markov ageing, unknown topology and hidden failure variables. The efficient computational result is for all-terminal disconnection, not automatically arbitrary terminal subsets or arbitrary monotone predicates. The calibration theorem's broader predicate scope must not be silently transferred to the algorithm.

An omitted independent catastrophe at rate `2/M` can reduce a predicted M-scale mean to at most `M/2`, while appearing with probability at most `2T/M` during aggregate observation time T. If `T<<M` and no justified intervention exposes that mechanism, silence cannot certify its absence. **Earning physical model completeness remains open.** [Boundaries and information barrier](package/research_note.tex#L406-L415).

## Strong ordinary comparators

Static all-terminal unreliability approximation, polynomial stationary failure-frequency approximation, reactive-flux corrections, reversible spectral methods and explicit-state short-data first-passage methods already exist and are credited. The source's proposed contribution is their complete constructive connection for a succinct component network, with a useful-trial lower bound, actual initial-state correction and component-level calibration law. Historical priority and practical superiority on general networks are unestablished.

Reciprocal stationary failure frequency is not the full mean in general. For two parallel edges with `(a_1,b_1)=(a,1)` and `(a_2,b_2)=(1,1)`, the source gives `nu=a/(1+a)` and `M=(a^2+3a+4)/(a(a+3))`, so `M nu ->4/3` as a tends to zero, despite rare stationary failure and bounded refresh contrast. [Comparison and counterexample](package/research_note.tex#L335-L354).

## Executed synthetic evidence, with its better comparator

The reported 40-identical-parallel-edge experiment has `p=2^-40`, `Lambda=80`, `g=1/40`; the conditional failed state is uniquely all-down, so no general static oracle is implemented in that run.

| Producer-recorded quantity | Value |
|---|---|
| Short-path trials / maximum updates each | 100,000 / 601 |
| Actual updates with early stopping | 29,288,065 |
| Successful no-return trials | 48,642 |
| Estimated mean | 28,255,201,980.18 |
| Reported 99% interval | [27,939,289,597.80, 28,578,347,381.32] |
| Exact birth–death reference | 28,233,101,920.17 |
| Reciprocal stationary failure frequency | 27,487,790,694.40 |

The rational interval includes spectral and initial-state corrections. Its statistical guarantee assumes independent uniform random choices; the actual program uses a reproducible NumPy PRNG. The **exact conventional birth–death solver is the better method for this symmetric example**. The short-path run tests the estimator and correction, not superiority over that solver. Small-system perturbation diagnostics are floating-point checks, not formal verification or physical validation. [Executed evidence](package/research_note.tex#L355-L405).

## Complete files

| Artifact | Link |
|---|---|
| Full proofs | [PDF](package/research_note.pdf), [LaTeX](package/research_note.tex) |
| Sharp rate-calibration result | [Standalone entry](component-calibration.md) |
| Producer reproduction instructions | [README](package/README.txt) |
| Recorded experiments | [parallel_experiment.json](package/parallel_experiment.json), [results.json](package/results.json) |
| Original scientific programs, not run during publication | [check_reliability.py](package/check_reliability.py), [parallel_experiment.py](package/parallel_experiment.py), [make_figure.py](package/make_figure.py) |
| Supplied figures | [PNG](package/figures/reliability_results.png), [PDF](package/figures/reliability_results.pdf) |
| Original package | [astra_p2_first_failure_research.zip](original/astra_p2_first_failure_research.zip) |
| Visible return and issued prompt | [Preserved capture](P2_FIRST_FAILURE_20261105_RETURN.txt) |
| Byte hashes and provenance | [SOURCES.json](SOURCES.json) |

All original ZIP/member bytes are retained. The public capture changes only its local ZIP download locator; source-time Library/sandbox links in the quoted answer are history, and the file links above are the public routes. This is direct GitHub publication with no large retrieval-index rebuild or new scientific audit. [Other supplied results](../README.md).
