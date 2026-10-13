# Local reproducibility and its limits

The archived producer bytes were never executed in place. The selected scripts
ran from disposable copies under `work/replays`, with one BLAS/OMP/Numba thread.
`replay/*.json` records Python 3.12.13, macOS, NumPy 2.5.4, SciPy 1.18.1,
SymPy 1.14.0 and Numba 0.68.0, command arguments, observed elapsed times and
log hashes. This differs from the producer environment. No numerical optimizer
or fresh quantum dictionary acquisition was rerun.

| Submission | Selected local invocations | Result |
|---|---|---|
| Quantum | verify_multi, certify_policy, structural_checks, physical_polynomial_checks, acquisition_protocol | All five exit successfully; seven rational packets regenerate with their exact fields matching. Policy non-timing fields match the original exactly. Synthetic acquisition remains synthetic. |
| Chemical | verify.py | Exit success; source's 200 generated complex-balanced fixtures, exact wrong-sign/saturation failures and finite-step checks repeat. Full JSON comparison passes with the recorded floating tolerance. |
| Physical | feasibility, coupling_model, source_constrained_budget, pulse_calibration | All four exit successfully and retain their internal diagnostics. Final two-component budget and pulse output pass the recorded floating comparison. No specimen or laboratory acquisition occurs. |

[COMPARISON.json](replay/COMPARISON.json) retains an initially strict recursive
comparison, excluding timing/RSS fields. Two physical output files are not
literally identical: the feasibility JSON records different environment versions
and tiny diagnostic-error strings, while the continuum finite-field derivative
is 0.04992862708497192 versus 0.049928599684528896 e nm, a difference of about
2.74e-8. The latter exceeds the comparison's tight 1e-7 relative / 1e-10 absolute
threshold; the producer's own continuum checks still pass and its nominal
terminal dipole differs by about 1.3e-12 e nm. The mismatch is retained, not
removed by changing the comparison tolerance. These are floating diagnostics,
not interval-certified material predictions.

[OUTPUT_MANIFEST.json](replay/OUTPUT_MANIFEST.json) hashes ten saved local output
files, separately from the immutable originals. Log/receipt hashes pin each
invocation. Recorded local seconds are verification costs, not a head-to-head
scientific performance benchmark. Producer scripts use a Linux-style
`peak_rss_KiB` label; macOS native `ru_maxrss` units differ, so those rerun fields
are not treated as portable memory measurements.

The new `synthesis_checks.py` is separately authored standard-library rational
arithmetic. It checks the selected-objective defect condition, projected error
identity, retained wrong-sign counterexample, a zero safe subspace, relocation
across three hidden kinetic fixtures, caps/two resource budgets, Hessian quadratic
forms and zero-current handling. Its universal claims depend on the written
proofs in SYNTHESIS.md, not on a finite pass count.

No rerun is an independent implementation, mathematical review, historical
priority search or physical validation. Selected replay passing does not prove
that every archived exploratory script is runnable or that any general complexity
or practical scientific capability gate has closed.
