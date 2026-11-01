# Stage two: coupled Gaussian memory consumer

Start with [REPORT.md](REPORT.md). The construction is author-derived and awaits independent review.

* [Main proof](COMPILER_PROOF.md)
* [Finite arithmetic and count details](FINITE_BIT_DETAILS.md)
* [Complete prior-pipeline comparison](PRIOR_COMPARISON.md)
* [Failed compressed-dilation shortcut](DILATION_FAILURE.md)
* [Primary source receipts](source_receipts.json)

All scripts use Python 3 with NumPy and mpmath; the figure also uses matplotlib. No SciPy or internet is needed for the mathematical checks. Dense matrices and permanents in tests are **validation definitions**, not the scalable quantum implementation. The source-collection script alone accesses the internet.

```
OPENBLAS_NUM_THREADS=1 python3 research/2026-11-02-forward-loss-clock-coupled-gaussian-memory/source/sol2/loss_clock.py
OPENBLAS_NUM_THREADS=1 python3 research/2026-11-02-forward-loss-clock-coupled-gaussian-memory/source/sol2/generic_gaussian_checks.py
OPENBLAS_NUM_THREADS=1 python3 research/2026-11-02-forward-loss-clock-coupled-gaussian-memory/source/sol2/retained_process_check.py
OPENBLAS_NUM_THREADS=1 python3 research/2026-11-02-forward-loss-clock-coupled-gaussian-memory/source/sol2/reduction_comparator.py
python3 research/2026-11-02-forward-loss-clock-coupled-gaussian-memory/source/sol2/make_figure.py
```

Results:

* [Coupled source/amplification/clock checks](results/loss_clock_checks.json)
* [Multi-port/dark-mode/count checks](results/generic_gaussian_checks.json)
* [Retained multi-event qubit channel](results/retained_process_check.json)
* [Ordinary reduced-memory comparator](results/reduction_comparator.json)
* [Dilation-overlap obstruction](results/dilation_overlap_failure.json)
* [First-stage preservation check](results/first_stage_preservation.json)
* [Exported scientific figure PDF](results/loss_clock_construction.pdf)

The first return and its sources remain in the parent directory; its independent frozen copy was not edited. No additional worker, model, hardware, outreach, publication, goal or automation was used in this stage.
