## Astra Pro3 — New result: task-specific uncertainty certificates

The research has advanced beyond the earlier bounded-noise reconstruction. The learner can now exploit the particular intervention being requested, rather than applying the same conservative uncertainty allowance to every possible history.

For the retained Gram representation

\\[ S=C^\mathsf TW^{-1}C+E,\qquad E\succeq0, \\]

the observations bound the unresolved residual diagonals by \\(E\_{ii}\leq\rho_i\\).

The new result is that, for a fixed intervention, the worst residual effect can be calculated using a single rank-one completion, provided a checkable positivity condition holds. Otherwise, the procedure falls back to a universally valid, more conservative bound.

This is an optimality statement for a specified relaxed PSD-completion uncertainty set—not a claim that the learner has identified the true microscopic network.

The first exact-rational execution reused the same 510 noisy source readings and tested 50 previously unseen intervention histories.

| Measurement                                  | Earlier certificate | New certificate |
| -------------------------------------------- | ------------------- | --------------- |
| Median response-interval width               | 0.00007653          | 0.00004552      |
| Maximum response-interval width              | 0.00052493          | 0.00031103      |
| Additional source readings                   | 0                   | 0               |
| Correct containment of all 50 true responses | Yes                 | Yes             |

The median improvement factor was 1.68×. The rank-one optimality condition passed in all 50 histories; no exact-rank assumption about the physical source was used.

### New operation: certify optima over all continuous interventions

The passive-network response is convex as a function of actuator doses. Therefore, response improvement minus linear intervention cost is concave.

This permits a global optimality certificate over the entire 128-dimensional dose simplex, rather than a previously specified collection of candidate experiments.

I derived source-independent intervals for all 128 marginal intervention benefits from the retained noisy measurements. These intervals provide an upper bound on how much any untested action could improve the chosen objective.

Four different cost objectives were executed:

| Objective | Active controls selected | Certified regret against any allowed action |
| --------- | ------------------------ | ------------------------------------------- |
| 1         | 2                        | 0.00008852                                  |
| 2         | 3                        | 0.00011361                                  |
| 3         | 5                        | 0.00008028                                  |
| 4         | 8                        | 0.00012617                                  |

All four certificates used zero additional source readings. An independent calculation from the hidden four-node source confirmed that every one of the 128 physical gradient components lay inside its acquired interval for each objective.

This is stronger than the previous finite-menu result: the regret bounds apply to every physically admissible continuous dose allocation, conditional on the supplied passive affine-network class and the original bounded-error measurements.

I also established a relevant limitation. The simple rank-one worst-case calculation is not universally valid when its positivity condition fails. An exact two-control example shows that a rank-two residual completion can be worse than either fixed-sign rank-one alternative. The general robust bound therefore needs a convex optimization formulation or a safe fallback.

### Further result: optimal task-directed sensing

A separate exact construction established a useful information limit.

Two passive sources agreed on all 14 historical measurements but required opposite decisions on a newly specified intervention. Without another measurement, the best deterministic decision had a worst-case regret of at least 0.07057.

One additional targeted scalar reaction resolved the ambiguity and certified the correct decision with zero regret over the two possible actions.

This establishes that, for this particular task, one new experiment is both necessary and sufficient. Reconstructing the entire source would be unnecessary.

The new response certificates also passed 144 additional held-out tests across 12 synthetic noise conditions. Larger noise widened the certificates, as expected.

### Research preserved

The complete mathematical arguments, exact counterexamples, executable programmes and actual numerical results are available:

- Scientific proof and full findings
- Continuous optimization programme and verified results
- Task-conditioned PSD acquisition and results
- Information-optimal active experiment and results

Scientific standing: The strongest advance is conditional, globally certified continuous intervention optimization from retained noisy scalar experiments. It has been tested on synthetic passive networks, not real hardware.

The remaining foundational obstruction is acquiring or independently justifying the physical source-class assumptions themselves. Classical active PSD completion already provides important related techniques, and equally informed retaining algorithms can reproduce the mechanisms developed here.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://proceedings.mlr.press\&sz=32)

proceedings.mlr.press



The next research direction is therefore task-directed acquisition of physically warranted model classes, rather than further optimizing an assumed model.

The Astra GitHub repository was not modified.