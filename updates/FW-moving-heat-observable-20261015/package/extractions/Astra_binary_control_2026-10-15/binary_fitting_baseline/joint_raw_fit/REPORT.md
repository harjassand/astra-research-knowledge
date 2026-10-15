# Stronger noisy comparator: jointly fit raw baseline, singletons, and couplings

This supplements and supersedes the noisy-comparison interpretation in ../REPORT.md. Earlier results are preserved. All data are synthetic; no hardware inference or novel global learner is claimed.

## Result

The random-design advantage persists after removing the frozen-noisy-baseline/singleton weakness. With identical calibration readings, all 12 ground truths, and the same 12 B initializations, jointly fitting f0, a, and B gave:

| Metric, selected models | Two-anchor | Equal-count random |
|---|---:|---:|
| Median heldout RMSE | 0.007220 | 0.001015 |
| Worst heldout RMSE | 0.01724 | 0.001468 |
| Median full-table RMSE | 0.006523 | 0.0007592 |
| Worst full-table RMSE | 0.01220 | 0.0009388 |
| Worst full-table absolute error | 0.04405 | 0.004637 |
| Selected optimizer success flags | 12/12 | 12/12 |
| Individual optimizer success flags | 140/144 | 144/144 |
| Starts within 1% of best observed training RMSE | 62/144 | 73/144 |
| Sum of fitting time | 20.58 s | 12.35 s |

Random has lower heldout RMSE and lower full-table RMSE on every one of the 12 paired ground truths. Heldout sets differ between designs, so the full-table comparison on identical test inputs is also included. The noisy truth-generating matrices are exactly the same as in the original report: full-system condition numbers 1.386–1.774 and minimum weighted shifted margin 0.719. This is a robust pattern within this small constructed ensemble, not a population-level result. Two-anchor training sets restrict nonanchor support to at most two nodes; extrapolation to large nonanchor supports is a plausible contributor, not an independently isolated causal finding.

## Fairness and implementation

Each model uses all Q raw-mean observations, including the baseline and singletons, with equal least-squares weight. Every setting has four independent readings at raw SD 0.001, hence mean SD 0.0005. Unlike subtracting and freezing noisy calibrations, this raw-mean objective retains the original independent equal-variance errors. Raw reads are loaded unchanged from the earlier NPZ receipts. Fits are initialized with measured baseline/singleton estimates; true f0/a/B are not used in any initializer, loss, or model selection.

The parameter vector is (f0,a,B_offdiag), with raw model f0+aᵀx. Each setting uses x=(I+B_SS)^−1 1, y=(I+B_SS)^−T a_S and derivatives df/df0=1, df/da_i=x_i on active coordinates (zero elsewhere), df/dB_ij=−y_i x_j. A finite-difference check across all parameter blocks has max absolute discrepancy 1.68e-9.

The 12 B starts, bounds [-0.6,0.6], maximum 1000 evaluations, and 1e-11 tolerances are unchanged. f0 and a are unbounded real parameters. There is no oracle-near initializer in this experiment. All selected models have positive optimizer termination flags; these are convergence flags, not proof of a global minimum. The selected raw-mean training RMSE ranges 0.0000398–0.000287 for two-anchor and 0.000109–0.000327 for random, all below mean noise SD. The 1% comparison only counts starts near the best observed objective, not certified globally successful starts. Every fitted model has positive checked Euclidean shifted margin: minima 0.507 and 0.521 respectively. Passivity was not imposed during optimization.

## Reading and compute accounting

No new calibration settings or readings were acquired: Q remains 28,44,64,88,116,148 for m=5,...,10, with 4Q readings per design/instance, already including all m+1 baseline/singleton settings. The two designs share raw values at overlapping settings. The refit adds 288 nonlinear optimizations and 33.38 seconds wall time (32.93 seconds summed optimizer time). This is additional to the earlier 576-fit, 44.06-second main experiment and preserved three-start pilot. All-table validation still enumerates 2^m synthetic truth values and is not charged as a purported polynomial physical acquisition; experimental exhaustive validation would require the additional unacquired settings and chosen repeats described in the main report.

## Practical conclusion

The stronger baseline does not rescue a practical advantage for the fixed two-anchor schedule here. Its generic local-identifiability algebra remains useful, while this empirical result cautions against pursuing it as an acquisition improvement without studying conditioning, anchor selection, support diversity, and calibration noise. The comparison is a baseline improvement, not an original acquisition capability. It neither disproves generic exact identifiability nor establishes a uniform finite-noise guarantee for random designs.

## Reproduction and outputs

From the parent directory:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python joint_fit.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python joint_summary.py

Source: ../joint_fit.py and ../joint_summary.py. This directory contains results.json (all 288 starts), selected_results.csv (24 selected models), all_table_selected_errors.csv, 24 NPZ files with every restart's parameters/predictions/errors, and metadata.json. ../joint_fit.log records live outcomes. Original experiment files remain unchanged.
