# Q54 stage 2 — sequential stress and exact compatible-task construction

**Actual outcome:** the stage1 hidden-transition obstruction survives, with tighter scope and a stronger ordinary comparator. A positive task-certificate construction is complete and agrees with conventional optimal recovery. It does not recover the missing law or establish a new capability advantage. The civilisation-changing acquisition target remains **NOT ACHIEVED**; novelty of the mathematical specializations is unestablished.

All stage1 scientific files remain unchanged; read-only fingerprints confirm all 16 files. New work is confined to stage2. No physical measurements, new sensor, target-regime probe, source-family oracle or permission change is introduced.

## Same consequential target

The target remains reliable new-regime constitutive use from safe, finite-precision measurements. The operation model is the same scalar Gaussian force-query primitive on `[0,a]`, with known stiffness bounds `m<=f'<=L`, real analyticity and `f(0)=0`. Arbitrary retained history and computation are allowed. The target force is at `b>a`.

Stage2 first attacks the strongest competing explanations, then attempts a positive representation for the same target: certify a particular force-ceiling task from all compatible laws, rather than claim to have discovered one unmeasured law.

## 1. A conventional sequential method improves the resource constants

The first-stage formula was exactly optimal for a **fixed number** of readings. It must not be interpreted as the optimum expected cost of a procedure that may stop at a random time. The established sequential probability ratio test, using the same endpoint force records and exact candidate knowledge, is a stronger conventional comparator for that objective.

For the original pair at `delta=0.025`, `sigma=0.001`, the fixed-budget optimum needs 177 readings for at most 5% error. Across 40,000 independent repetitions under each hypothesis, the ordinary SPRT gives:

| Quantity | Result |
|---|---:|
| Combined observed error | 4.27125% |
| Mean readings | 91.89994 |
| Median readings | 74 |
| 95th percentile | 222 |
| 99th percentile | 323 |
| Largest realized count | 912 |

The symmetric Gaussian test has a proved error bound of 5%; the observed fraction is diagnostic. It uses an unbounded stopping rule with finite expected count. Its mean is not a hard maximum of 92. Both the improvement and its tail costs are retained in `sequential_comparison.csv` and `sprt_raw.npz`.

A completed change-of-measure proof now covers **every** adaptive safe-query policy with finite expected count and both errors at most `p`:

```
E_j N >= 2*sigma^2*kl(p,1-p)/epsilon^2,
epsilon = max_[0,a] |f1-f0|,
kl(p,1-p) = (1-2p)*log((1-p)/p).
```

For the hidden transition, `epsilon<=A*delta*exp(-(c-a)/delta)`. Thus even the strongest possible stopping policy retains an exponential expected acquisition cost. For the tested pair, the bound is `86.47374` expected readings at nominal 5% error. No claim that the chosen conservative SPRT thresholds exactly attain that finite-sample optimum is made.

This is a substantive correction of a possible broad cost interpretation, not a failure of the explicitly fixed-n first-stage theorem. Sequential testing and its information bound are classical. [Kaufmann, Cappé and Garivier, JMLR 2016](https://www.jmlr.org/papers/volume17/kaufman16a/kaufman16a.pdf).

## 2. Boundary and domain stress

The possibility that the obstruction is caused by putting `f0` exactly at the lower stiffness limit is defeated by an interior construction. Let

```
k=(m+L)/2,
A_eta=L-m-2*eta,
H(x)=A_eta*delta*[sp((x-c)/delta)-sp(-c/delta)],
f_-(x)=k*x-H(x)/2,
f_+(x)=k*x+H(x)/2.
```

For every `delta>0` and fixed `0<eta<(L-m)/2`, both derivatives stay in `[m+eta,L-eta]`. Their safe signature remains exponentially small and their target gap stays macroscopic. The comparison kernel and stopping-time lower bound continue to apply. This is proved over the full stated parameter domain, not extrapolated from favorable widths.

Conversely, endpoint optimality must stay **pair scoped**. The alternative analytic passive pair

`g0(x)=3*x`, `g1(x)=3*x+0.5*tanh(x)*tanh(x-a)`

has derivatives in `[2,4]`, equal force exactly at `a=0.5`, and different force inside the safe interval. Endpoint-only data have no information for that pair, while an interior query does. The first-stage endpoint theorem therefore cannot be promoted into a universal sampling rule for arbitrary unknown analytic materials. This limiting example is saved in `endpoint_scope_counterexample.json` and proved in the governing file.

## 3. Stronger positive construction: certify a task from the complete law set

For each measured force interval `[y_i-r_i,y_i+r_i]`, put

`g=f-m*x`, `l_i=y_i-r_i-m*x_i`, `u_i=y_i+r_i-m*x_i`, `A=L-m`.

Include the exact anchor `x0=0`, `l0=u0=0`. The complete compatible class for `g` is monotone and `A`-Lipschitz. Its exact interval envelopes are

```
L_data(x) = max_i [l_i-A*max(x_i-x,0)]
U_data(x) = min_i [u_i+A*max(x-x_i,0)].
```

The governing proof gives an exact feasibility test and proves these are pointwise sharp. At `b>=a`, the target interval is

`[m*b+max_i l_i, m*b+min_i(u_i+A*(b-x_i))]`.

A force-ceiling predicate can be certified when every compatible law is on the same side. Otherwise the operation returns `UNKNOWN`. `SAFE` in the data files means only `f(b)<=ceiling`; it is not a general physical-safety or permission claim.

A complete analytic bridge accompanies the closed monotone-Lipschitz construction. If the finite measurement intervals have positive feasible slack, mix an extremal piecewise-linear witness with a strict interior witness, convolve with a Gaussian, and re-anchor at zero. The result is an explicit real-analytic law with `m<=f'<=L` on **all real x**, preserves every measurement interval and approaches either target bound. Four hundred such analytic functions are saved with full knots, values and widths in `analytic_witness_functions.json`. Their largest target approximation gap in the run is `2.00437e-4`; the proof permits arbitrary refinement.

Positive slack is essential. Exact noiseless data with `f(a)=m*a` force `f(x)=m*x` globally by positivity and analytic rigidity. The proof explicitly preserves this exceptional case. Closed-interval optimality also does not resolve every equality predicate at a nonattained endpoint; the implemented rule is conservative there.

This construction is a usable mathematical task certificate, but set-membership / Lipschitz interpolation is established. A separately formulated ordinary LP computes the same sharp interval. It is not a new advantage over the strongest conventional method. [Calliess, primary v3](https://arxiv.org/abs/1701.00178v3).

## 4. Withheld execution and full-domain guarantee

The predeclared protocol uses 200 cases from five materially different analytic families: single softplus, multiple softplus, oscillatory stiffness, localized arctangent response and two-frequency stiffness. Every case has 17 safe readings at `sigma=0.001`; all 3,400 simulated calibration records are saved. Family parameters and target truth are withheld from both the certificate algorithm and its LP comparator. There is no tuning or favorable-case deletion.

Each case receives four fixed target force ceilings, for 800 total tasks:

| Verdict | Count |
|---|---:|
| Certified below ceiling | 297 |
| Certified above ceiling | 101 |
| UNKNOWN | 402 |
| Observed incorrect certificates | 0 |

All 200 target intervals contain their withheld target in this execution. The calibration event itself holds for 199 of 200 records; the one miss is retained. The formal Gaussian confidence is 99% **per record**, simultaneously across that record's readings/target predicates, not a 99% campaign-wide promise. Zero observed errors is not a 100% coverage theorem.

The maximum discrepancy from the independent LP is `4.44e-16`. Full-domain proofs establish the optimality and analytic near-extremizer claims; held-out simulations check implementation. The interval width is at least `(L-m)*(b-a)=2` for every feasible record under the positive-slack analytic scope, with smallest observed width `2.0049993`. The unresolved tasks are intrinsic under the stated knowledge, rather than cases discarded from the result.

## Remaining obstacle and scientific status

The stronger positive representation certifies coarse target predicates without recovering a constitutive law. It does not expose an arbitrary hidden transition, narrow the uncertainty beyond ordinary optimal recovery, or replace the missing physical operation. That operation remains a supported transition-sensitive observation, an allowed target-regime measurement, or a justified additional quantitative structural prior.

The sequential comparator succeeds at its established task. The set-membership incumbent matches the positive construction. No incumbent failure, favorable unknown rate, physical measurement or novelty claim has been manufactured. The original consequential target remains unmet.

## Reproduction and saved objects

```
/usr/local/bin/python3 -W error /Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/trials/Q54/stage2/stress.py
/usr/local/bin/python3 -W error /Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/trials/Q54/stage2/plot.py
```

Both commands complete with warnings treated as errors.

- [Governing proof](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/trials/Q54/stage2/GOVERNING_PROOF.md): sequential bound, interior pair, endpoint scope, exact envelopes and analytic witness proof.
- [Executable construction](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/trials/Q54/stage2/stress.py): all comparisons and withheld cases.
- [Predeclared protocol](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/trials/Q54/stage2/PROTOCOL.md), [scientific notes](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/trials/Q54/stage2/RESEARCH_NOTES.md), [primary evidence](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/trials/Q54/stage2/SOURCES.md).
- `sequential_comparison.csv`, `sprt_raw.npz`, `interior_pair.csv`, `endpoint_scope_counterexample.json`.
- `withheld_cases.csv`, `withheld_measurements.csv`, `withheld_tasks.csv`, `withheld_parameters.json`.
- `analytic_near_extremizers.csv`, `analytic_witness_functions.json`, `summary.json`.
- `stage2_stress.png`, `stage2_stress.pdf`, `plot.py`.

![Second-stage stress and ordinary-comparator results](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/trials/Q54/stage2/stage2_stress.png)
