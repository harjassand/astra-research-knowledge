Run from this directory. The pure symbolic/high-precision scripts use the retained read-only sympy/mpmath dependency at ../capability_backward_bridge/code/vendor and can use the bundled Python3.12 runtime. The SciPy field/action scripts use system Python3.14 with the retained read-only compiled dependencies at ../positive_current_operation/vendor. An initial3.12/SciPy ABI mismatch was corrected; no physical result relied on that failed invocation.

Pure math:

- `python code/axis_structural.py`
- `python code/web_and_label_identities.py`
- `python code/reference_well.py`
- `python code/elliptic_checks_and_limits.py`
- `python code/certify_reference_tube.py`
- `python code/certify_candidate_tube.py`

For action/volume calculations, use Python3.14 and set OPENBLAS_NUM_THREADS=2,OMP_NUM_THREADS=2:

- `python3 code/finite_action.py`
- `python3 code/action_calibration.py`
- `python3 code/parameter_action.py`
- `python3 code/validate_parameter_action.py`

The last two construct the guarded candidate, match actual finite tube volume and integrate all located local well classes. The actual-action validation takes about4.3 seconds on this host. Runtimes in result JSON are per invocation, not total research/billable cost.

`find_strength_critical.py` preserves a failed limited repair search; it need not be rerun to reproduce the accepted findings. `parameter_action_first_attempt.json` and `FIRST_ATTEMPT.md` preserve the earlier inadmissible locator/guard outcome.

All fields and actions are dimensionless source-model calculations. No experimental calibration, broad fixed-wall confinement, global optimizer guarantee, finite-wire engineering or superiority over current ordinary QI/QS is claimed. Manifests record transport/provenance only. Completed older folders were read only and remain frozen.
