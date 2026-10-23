# One-stream observable-innovation learning: finite execution — 24 October 2026

This packet pairs the source's family-level contract with the later completed finite synthetic execution. The earlier contract's section 7 predates that execution; [the current results JSON](source/results/learning_control_results.json) supplies the run status. The learner stream and evaluator/control stream are retained as separate files. The producer receipt and its absolute-path inventory are not copied.

## Contract and operating requirements

The source family is a hidden sign state with two actions, action-conditioned independent sign innovations, and noisy sign observations. For each block, all exploration actions must be selected in advance from a fixed full-support schedule. The three adjacent observed products cancel the hidden state and share innovations only within a block, yielding six action-conditioned moments with independent blocks. Those moments identify the transition parameters and observation-noise magnitude only in the stated nondegenerate regime; zero or near-zero denominators give nonidentifiability or partial identification, not a clipped certainty.

The confidence statement is conditional on the supplied structural family and the fixed ex-ante schedule. Adaptive scripts that choose future exploration actions from observations, model misspecification, and physical reset/state access are outside it. The estimator and retaining-HMM comparator receive the same ordered public prefix and supplied model class; the known-model oracle is privileged evaluator information, not an acquired baseline.

## Recorded execution

The source reports one synthetic run: 60,000 training transitions, 12,000 pre-task validation transitions, and 75,360 total unique transitions after washout and two held-out objectives. Each held-out controller cell has 16 segments. On validation, log loss was 0.614229 nats per observation for the innovation point and 0.614231 for the retaining HMM (12,000 predictions each; neither refit during scoring).

| Held-out objective | Innovation point actual mean reward | Retaining HMM actual mean reward | Oracle actual mean reward | Innovation / HMM conditional expected regret |
|---|---:|---:|---:|---:|
| Positive output | 0.7496 | 0.7328 | 0.7508 | 0.0000174 / 0 |
| Observed switches | 0.5580 | 0.6696 | 0.5673 | 0 / 0 |

These are source-reported realized averages for one finite synthetic execution. The oracle's realized reward is not a bound on a particular sample path; conditional expected values use evaluator truth. The results establish neither statistical significance nor broad superiority. One recorded fit took 0.008 s for the innovation point and 314 s for a 16-start, 923-iteration retaining-HMM fit; these single-run timings are not a general efficiency comparison. Peak memory was not measured.

## Current evidence boundary

- The six-moment, forgetting and value certificate apply under the stated model family; the learner does not discover those structural promises.
- Point-model planner near-optimality confidence was not computed, and conditional expected values are evaluator calculations rather than learner-acquired bounds.
- Sixteen segments per cell do not establish significance. Whole-stream EM convergence is not a global maximum certificate.
- The finite synthetic run is not a physical experiment. No broad learning advantage or practical capability is established.
- This update selects only the learning subunit from the broader continuing source packet; its physical-wave, powder, PFAS-release and autonomous-CTMC contents remain separate and are not promoted by this record.

Source code and the exact run records are preserved in [the selected manifest](source_manifest.json). No scientific code or result checker was run by this integration.
