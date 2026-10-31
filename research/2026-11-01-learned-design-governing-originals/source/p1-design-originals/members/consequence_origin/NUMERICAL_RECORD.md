# Finite calculations and preserved failures

These runs are synthetic consistency checks of `PHASE_RECONSTRUCTION.md`. They are not physical experiments, demonstrations of asymptotic scaling, proof of optimal constants, or a novelty claim. Both the proposed route and the strongest ordinary comparator use the same trajectory and conditional likelihood. Exact enumeration is used only as a small-state scorer of the fitted model and the true synthetic generator.

## First run: switching control retained

Command:

```sh
python phase_experiment.py --n 7 --beta .63 --true-h .08 --observations 2000000 --count-samples 1500 --seed 49203
```

The seven-site system switched phases eight times. It therefore did **not** demonstrate the intended no-switch acquisition scenario. Its field estimate was 0.08005297 for the true value 0.08. The phase-weight calculation was 0.75350744, the fitted-model exact scorer gave 0.75389930, and the true-model scorer gave 0.75376185.

The entire result and trajectory are retained as `phase_results_k7_switching_control.json` and `phase_observations_k7_switching_control.npz`. This is a failed no-switch demonstration, not an unreported pilot selected away.

## Second run: observed no switching

To increase the finite phase barrier, the graph was changed to K9 with beta=0.55. The random seed was retained; no seed search was performed. This is a different finite instance, with its own charged observation budget.

```sh
python phase_experiment.py --n 9 --beta .55 --true-h .08 --observations 10000000 --count-samples 1500 --seed 49203
```

| Quantity | Observed value |
| --- | ---: |
| Consecutive physical update attempts | 10,000,000 |
| Physical phase switches | 0 |
| True synthetic uniform field | 0.0800000 |
| Conditional-likelihood field estimate | 0.0814147 |
| Valid field confidence rule, numerical interval | [0.0362327, 0.1279994] |
| Learned polymer contraction upper parameter theta | 0.4795394 |
| Phase-weight estimate from explicit polymer-chain counting | 0.8121635 |
| Counting interval conditional on the fitted model | [0.8038923, 0.8201177] |
| Full-state plus-phase weight for fitted model | 0.8122986 |
| Full-state plus-phase weight for true model | 0.8083864 |
| Actual synthetic model total-variation error | 0.0039122 |
| Polymer-counting error against fitted-model scorer | 0.0001351 |
| Enumerated states in the validation scorer | 512 |

The confidence interval for the field maps to a plus-phase range of [0.6574588, 0.9091482] in the small-state exact scorer. **This run therefore does not certify end-to-end absolute error 0.04.** Its realised error is much smaller than its certified statistical uncertainty. The counting interval above covers numerical sampling/counting uncertainty around the fitted model; it must not be presented as a confidence interval around the true physical phase weight by itself.

The baseline graph degree in this finite example is eight. The theorem uses fixed maximum degree for its asymptotic polynomial acquisition statement. Complete graphs growing with n would violate that fixed-degree premise and can make the local Fisher-information/positivity constants deteriorate exponentially with n. This small complete-graph check does not establish bounded-degree scaling.

The spectral gap and one-dimensional root calculations use ordinary double precision. The mathematical confidence-set and contraction arguments are explicit, but the implementation is not a formally verified interval-arithmetic package.

## Separate sampler check

Using the fitted phase weights and the explicitly constructed polymer chains, a separately seeded digital mixture sampler generated 5,000 configurations, including both phases. This verifies that the implementation can produce the unseen phase from the learned local model; it does not supply an experimental reset. The result is recorded in `phase_results.json`. Its Monte Carlo bound is separate from the field-estimation uncertainty.

## Comparator conclusion

An empirical average along the trapped physical trajectory would not recover the equilibrium mixture. That is a deliberately weak comparison and is not the claimed frontier. The strongest ordinary retained-data route—conditional likelihood followed by an established polymer sampler/counting algorithm—obtains precisely the same result as the constructed route. The full-state fitted-model solver is also a valid comparator at this small n and retains the same field uncertainty.

No computational advantage over that strongest ordinary route is established.
